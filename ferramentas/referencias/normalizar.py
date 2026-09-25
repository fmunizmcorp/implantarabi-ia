"""Normaliza as tabelas de referência brutas para CSV UTF-8 ';' fatiado.

Fonte: referencias/COMO-ATUALIZAR.md · Conferido em 2026-09-25 · Kit v0.1.0
Só biblioteca padrão. ``openpyxl`` é opcional e só é usado quando a entrada
é .xlsx (CMED, TUSS/OPME); sem ele, exporte a planilha para CSV e passe o CSV.

Uso (um subcomando por fonte; todos gravam em --saida, padrão referencias/):

  python3 ferramentas/referencias/normalizar.py cmed --pmc CMED_PMC.xlsx \
      --pmvg CMED_PMVG_PF.xlsx --edicao 20260508 --data 2026-05-09 \
      [--tuss-registros "REGISTROS ANVISA NA TUSS DE MEDICAMENTOS.xlsx"]
  python3 ferramentas/referencias/normalizar.py brasindice-medicamentos \
      --principal Brasindice_1100_Medicamentos.txt --edicao 1100 \
      [--anterior Brasindice_1094_Medicamentos.txt --complementar \
       Brasindice_1094_MedicamentosFarmacos.txt --edicao-complementar 1094]
  python3 ferramentas/referencias/normalizar.py brasindice-materiais \
      --principal Brasindice_1094_Materiais.txt --edicao 1094
  python3 ferramentas/referencias/normalizar.py simpro --tipo material \
      --arquivo SIMPRO_MATERIAL.csv --edicao "coleta 2026-04-12"
  python3 ferramentas/referencias/normalizar.py tuss-historico --arquivo X.txt --competencia 202601
  python3 ferramentas/referencias/normalizar.py tuss-registros-anvisa --arquivo X.xlsx --competencia 202601
  python3 ferramentas/referencias/normalizar.py tuss-opme --nomes-tecnicos A.xlsx \
      --fabricantes B.xlsx --envio-individualizado C.xlsx --competencia 202601
  python3 ferramentas/referencias/normalizar.py cbhpm --arquivo CBHPM_PORTES.csv
  python3 ferramentas/referencias/normalizar.py tiss --schemas DIR_XSD --versao 4.03.00
  python3 ferramentas/referencias/normalizar.py indices   # só refaz os 00-INDICE.md

Ordem recomendada: cmed → brasindice-* (usa a CMED já normalizada para
preencher princípio ativo/registro) → simpro → tuss → cbhpm → tiss.
"""
from __future__ import annotations

import argparse
import csv
import io
import re
import shutil
import sys
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ferramentas.referencias import comum  # noqa: E402
from ferramentas.referencias.comum import (  # noqa: E402
    COLUNAS_PRODUTO, normalizar_texto, numero, so_digitos)

HOJE = date.today().isoformat()

# ------------------------------------------------------------------ utilidades


def _linha_produto(**campos) -> List[str]:
    return [str(campos.get(c, "") or "") for c in COLUNAS_PRODUTO]


def _idx(nome: str) -> int:
    return COLUNAS_PRODUTO.index(nome)


def _chave_produto(l: Sequence[str]) -> str:
    return normalizar_texto(l[_idx("produto")])


def _ler_planilha(caminho: Path, marcador_cabecalho) -> List[List]:
    """Linhas a partir do cabeçalho (xlsx via openpyxl ou csv/txt)."""
    caminho = Path(caminho)
    if caminho.suffix.lower() in (".xlsx", ".xlsm"):
        try:
            import openpyxl  # type: ignore
        except ImportError:  # pragma: no cover
            sys.exit(f"openpyxl não instalado: exporte {caminho.name} para CSV e passe o CSV "
                     "(ou pip install openpyxl).")
        ws = openpyxl.load_workbook(caminho, read_only=True, data_only=True).worksheets[0]
        linhas = [list(r) for r in ws.iter_rows(values_only=True)]
    else:
        dados = caminho.read_bytes()
        try:
            texto = dados.decode("utf-8-sig")
        except UnicodeDecodeError:
            texto = dados.decode("latin-1")
        sep = max([";", ",", "\t", "|"], key=texto[:4096].count)
        linhas = [list(r) for r in csv.reader(io.StringIO(texto), delimiter=sep)]
    for i, r in enumerate(linhas):
        if r and marcador_cabecalho(r):
            cab = [normalizar_texto(str(c or "")) for c in r]
            return [cab] + [x for x in linhas[i + 1:] if any(v not in (None, "") for v in x)]
    raise SystemExit(f"cabeçalho não encontrado em {caminho}")


def _col(cab: List[str], *nomes: str) -> int:
    for n in nomes:
        n = normalizar_texto(n)
        for i, c in enumerate(cab):
            if c == n:
                return i
    raise KeyError(nomes)


def _txt(v) -> str:
    if v is None:
        return ""
    s = str(v).strip()
    return "" if s in {"-", "    -", "    -     "} or re.fullmatch(r"-+", s.replace(" ", "")) else " ".join(s.split())


def registrar(saida: Path, conjunto: str, fatias: List[Dict], meta: Dict) -> None:
    man = comum.carregar_manifest(saida)
    meta = dict(meta)
    meta["pasta"] = conjunto
    meta["linhas"] = sum(f["linhas"] for f in fatias)
    meta["bytes"] = sum(f["bytes"] for f in fatias)
    meta["fatias"] = fatias
    meta.setdefault("normalizado_em", HOJE)
    man.setdefault("conjuntos", {})[conjunto] = meta
    comum.salvar_manifest(saida, man)
    gerar_indice_conjunto(saida, conjunto, meta)
    gerar_indices_pastas(saida)
    print(f"{conjunto}: {meta['linhas']} linhas em {len(fatias)} fatia(s), {meta['bytes']/1e6:.2f} MB")


def _origem(caminhos: Iterable[Path], rotulo: str = "") -> List[Dict]:
    """Registro dos brutos (nome, tamanho, sha256). ``rotulo`` troca o nome do
    arquivo quando ele identifica quem publicou (ex.: portal de operadora)."""
    return [{"arquivo": rotulo or Path(c).name, "bytes": Path(c).stat().st_size,
             "sha256": comum.sha256_arquivo(Path(c))} for c in caminhos if c]


# ------------------------------------------------------------------ índices .md

CABECALHO_MD = ("> **Fonte:** {fonte} · **Conferido em:** {conferido}\n"
                "> **Vale para:** referência de nomenclatura e códigos ({edicao}); preço só indicativo"
                " · **Kit:** v{kit}\n")


def gerar_indice_conjunto(saida: Path, conjunto: str, meta: Dict) -> None:
    pasta = saida / conjunto
    cols = meta.get("colunas", [])
    desc_cols = meta.get("descricao_colunas", {})
    linhas = [f"# {meta.get('titulo', conjunto)}", "",
              CABECALHO_MD.format(fonte=meta.get("fonte_publica", meta.get("fonte", "")),
                                  conferido=meta.get("normalizado_em", HOJE),
                                  edicao=f"edição {meta.get('edicao', '?')}", kit=comum.KIT_VERSAO),
              meta.get("descricao", ""), "",
              "| Campo | Valor |", "|---|---|",
              f"| Fonte | {meta.get('fonte', '')} |",
              f"| Edição | {meta.get('edicao', '')} |",
              f"| Data da edição | {meta.get('data_edicao', '')} |",
              f"| Linhas | {meta.get('linhas', 0)} |",
              f"| Fatias | {len(meta.get('fatias', []))} |",
              f"| Normalizado em | {meta.get('normalizado_em', '')} |",
              f"| Licença | {meta.get('licenca', '')} — ver [LICENCAS.md]({'../' * (conjunto.count('/') + 1)}LICENCAS.md) |",
              ""]
    if meta.get("observacoes"):
        linhas += ["## Observações", ""] + [f"- {o}" for o in meta["observacoes"]] + [""]
    linhas += ["## Colunas", "", "| Coluna | Significado |", "|---|---|"]
    for c in cols:
        linhas.append(f"| `{c}` | {desc_cols.get(c, '')} |")
    linhas += ["", "## Origem (arquivos brutos)", "", "| Arquivo | Bytes | sha256 |", "|---|---|---|"]
    for o in meta.get("origem", []):
        linhas.append(f"| {o['arquivo']} | {o['bytes']} | `{o['sha256'][:16]}…` |")
    linhas += ["", "## Fatias", "",
               "Abra só a fatia da letra inicial do nome (ou use `ferramentas/referencias/buscar.py`).", "",
               "| Arquivo | Prefixo | Linhas | Bytes | sha256 |", "|---|---|---|---|---|"]
    for f in meta.get("fatias", []):
        linhas.append(f"| [{f['arquivo']}]({f['arquivo']}) | {f['prefixo'] or '—'} | {f['linhas']} | {f['bytes']} | `{f['sha256'][:16]}…` |")
    (pasta / "00-INDICE.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")


TITULOS_PASTA = {
    "brasindice": "Brasíndice (medicamentos e materiais)",
    "simpro": "SIMPRO (materiais, medicamentos, saneantes, reagentes)",
    "cmed": "CMED/ANVISA (preços regulados de medicamentos)",
    "tuss": "TUSS/ANS (terminologia unificada)",
    "cbhpm": "CBHPM (portes por código TUSS)",
    "tiss": "TISS/ANS (schemas e domínios)",
}


def gerar_indices_pastas(saida: Path) -> None:
    """00-INDICE.md de cada pasta de fonte (lista os conjuntos dela)."""
    man = comum.carregar_manifest(saida)
    por_fonte: Dict[str, List] = {}
    for nome, meta in man.get("conjuntos", {}).items():
        por_fonte.setdefault(nome.split("/")[0], []).append((nome, meta))
    for fonte, itens in por_fonte.items():
        if fonte == "tiss":
            continue  # índice próprio (gerar_indice_tiss)
        pasta = saida / fonte
        linhas = [f"# {TITULOS_PASTA.get(fonte, fonte)}", "",
                  CABECALHO_MD.format(fonte=itens[0][1].get("fonte_publica", itens[0][1].get("fonte", fonte)),
                                      conferido=HOJE, edicao="ver cada conjunto", kit=comum.KIT_VERSAO),
                  "Cada subpasta é um conjunto normalizado. Leia o `00-INDICE.md` dela para colunas e fatias.", "",
                  "| Conjunto | O que tem | Edição | Linhas | Quando usar |", "|---|---|---|---|---|"]
        for nome, meta in sorted(itens):
            sub = nome.split("/", 1)[1] if "/" in nome else nome
            linhas.append(f"| [{sub}/]({sub}/00-INDICE.md) | {meta.get('titulo', '')} | {meta.get('edicao', '')} | "
                          f"{meta.get('linhas', 0)} | {meta.get('quando_usar', '')} |")
        (pasta / "00-INDICE.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")


# ------------------------------------------------------------------ CMED

DESC_PRODUTO = {
    "fonte": "Tabela de origem (BRASINDICE, SIMPRO ou CMED).",
    "edicao": "Edição/competência da publicação usada.",
    "tipo_item": "medicamento, material, saneante ou reagente.",
    "codigo_fonte": "Código do item na própria tabela (Brasíndice: código TISS de 10 dígitos; SIMPRO: código de 10 dígitos; CMED: código GGREM).",
    "tabela_fonte": "Código da Tabela 87 (TISS) que acompanha `codigo_fonte` na guia: 05 Brasíndice, 12 SIMPRO; vazio na CMED.",
    "chave_fonte": "Chave interna da publicação (Brasíndice: laboratório-produto-apresentação).",
    "laboratorio": "Laboratório/fabricante.",
    "produto": "Nome comercial ou descrição curta, como publicado.",
    "apresentacao": "Apresentação (forma, concentração, embalagem), como publicada.",
    "principio_ativo": "Substância. CMED publica; no Brasíndice vem da CMED pelo EAN (ou registro).",
    "ean": "Código de barras (EAN-13).",
    "registro_anvisa": "Registro ANVISA (13 dígitos em medicamento).",
    "codigo_tuss": "Código TUSS (20 medicamentos, 19 materiais, 18 taxas).",
    "ggrem": "Código GGREM da CMED.",
    "generico": "S = genérico; N = não; vazio = não informado.",
    "restrito_hospitalar": "S = uso restrito a hospital/clínica (PMC costuma ser 0 — normal).",
    "qtd_embalagem": "Unidades por embalagem (quando a fonte informa).",
    "pf_total": "Preço Fábrica da embalagem (R$).",
    "pmc_total": "Preço Máximo ao Consumidor da embalagem (R$).",
    "pf_unit": "PF por unidade (R$).",
    "pmc_unit": "PMC por unidade (R$).",
    "preco_ref": "Preço único publicado quando não há PF/PMC (SIMPRO, em geral por unidade/fração).",
    "tipo_preco": "Código curto da base do preço: BRAS_PF_PMC = PF/PMC do Brasíndice (ICMS 17%; PMC 0 em restrito hospitalar é normal); CMED_ICMS17 = PF/PMC CMED com ICMS 17% (outras alíquotas em precos_extra); SIMPRO_VIG = valor vigente SIMPRO (em geral por unidade/fração, 3 casas).",
    "vigencia": "Data (AAAA-MM-DD) ou edição da última alteração de preço do item.",
    "tabela87_sugerida": "Tabela TUSS sugerida para o item: 20 medicamento, 19 material. Conferir com o contrato do convênio.",
    "precos_extra": "CMED: preços em outras alíquotas de ICMS (PF0, PF12, PF18…, PMC18…, PMVG17…).",
}

ALIQ_EXTRA = ["0", "12", "18", "19", "20", "21", "22"]


def _cmed_linhas(pmc: Path, pmvg: Optional[Path], tuss_reg: Dict[str, str], edicao: str) -> List[List[str]]:
    tab = _ler_planilha(pmc, lambda r: str(r[0] or "").upper().startswith("SUBST"))
    cab, dados = tab[0], tab[1:]
    c = {k: _col(cab, v) for k, v in {
        "sub": "SUBSTANCIA", "lab": "LABORATORIO", "ggrem": "CODIGO GGREM", "reg": "REGISTRO",
        "ean": "EAN 1", "prod": "PRODUTO", "apres": "APRESENTACAO", "status": "TIPO DE PRODUTO (STATUS DO PRODUTO)",
        "rest": "RESTRICAO HOSPITALAR"}.items()}
    pf = {a: _col(cab, f"PF {a}%" if a == "0" else f"PF {a} %") for a in ["0", "12", "17", "18", "19", "20", "21", "22"]}
    pmcc = {a: _col(cab, f"PMC {a} %") for a in ["0", "12", "17", "18", "19", "20", "21", "22"]}
    pmvg_por_ggrem: Dict[str, Dict[str, str]] = {}
    if pmvg:
        t2 = _ler_planilha(pmvg, lambda r: str(r[0] or "").upper().startswith("SUBST"))
        cab2 = t2[0]
        ig = _col(cab2, "CODIGO GGREM")
        iv = {a: _col(cab2, f"PMVG {a} %") for a in ["17", "18", "20"]}
        for r in t2[1:]:
            if len(r) > ig and r[ig]:
                pmvg_por_ggrem[_txt(r[ig])] = {a: numero(r[i]) for a, i in iv.items()}
    saida = []
    for r in dados:
        if len(r) <= c["apres"] or not _txt(r[c["prod"]]):
            continue
        g = _txt(r[c["ggrem"]])
        reg = so_digitos(_txt(r[c["reg"]]))
        extra = [f"PF{a}={numero(r[pf[a]])}" for a in ALIQ_EXTRA if numero(r[pf[a]])]
        extra += [f"PMC{a}={numero(r[pmcc[a]])}" for a in ALIQ_EXTRA if numero(r[pmcc[a]])]
        extra += [f"PMVG{a}={v}" for a, v in pmvg_por_ggrem.get(g, {}).items() if v]
        rest = normalizar_texto(_txt(r[c["rest"]]))
        saida.append(_linha_produto(
            fonte="CMED", edicao=edicao, tipo_item="medicamento", codigo_fonte=g,
            laboratorio=_txt(r[c["lab"]]), produto=_txt(r[c["prod"]]), apresentacao=_txt(r[c["apres"]]),
            principio_ativo=_txt(r[c["sub"]]), ean=so_digitos(_txt(r[c["ean"]])), registro_anvisa=reg,
            codigo_tuss=tuss_reg.get(reg, ""), ggrem=g,
            generico="S" if "GENERICO" in normalizar_texto(_txt(r[c["status"]])) else "",
            restrito_hospitalar="S" if rest == "SIM" else ("N" if rest == "NAO" else ""),
            pf_total=numero(r[pf["17"]]), pmc_total=numero(r[pmcc["17"]]),
            tipo_preco="CMED_ICMS17",
            vigencia=edicao, tabela87_sugerida="20", precos_extra="|".join(extra)))
    return saida


def ler_tuss_registros(caminho: Optional[Path]) -> Dict[str, str]:
    if not caminho:
        return {}
    tab = _ler_planilha(caminho, lambda r: "REGISTRO" in normalizar_texto(str(r[-1] or r[0] or "")))
    reg: Dict[str, str] = {}
    for r in tab[1:]:
        if len(r) >= 2 and r[0] and r[1]:
            reg.setdefault(so_digitos(str(r[1])), str(r[0]).strip())
    return reg


def cmd_cmed(a) -> None:
    saida = Path(a.saida)
    tuss_reg = ler_tuss_registros(Path(a.tuss_registros) if a.tuss_registros else None)
    linhas = _cmed_linhas(Path(a.pmc), Path(a.pmvg) if a.pmvg else None, tuss_reg, a.edicao)
    fatias = comum.gravar_fatiado(saida / "cmed/medicamentos", COLUNAS_PRODUTO, linhas, _chave_produto)
    registrar(saida, "cmed/medicamentos", fatias, {
        "titulo": "CMED — lista de preços de medicamentos (PF/PMC/PMVG)",
        "fonte": "CMED/ANVISA — Lista de preços de medicamentos",
        "fonte_publica": "https://www.gov.br/anvisa/pt-br/assuntos/medicamentos/cmed/precos",
        "edicao": a.edicao, "data_edicao": a.data, "licenca": "pública (ANVISA/CMED)",
        "descricao": "Preços regulados (teto) de medicamentos com substância, registro ANVISA, EAN e GGREM. "
                     "Serve para achar o princípio ativo, o registro e o teto legal de preço.",
        "quando_usar": "princípio ativo, registro ANVISA, EAN, teto PF/PMC",
        "colunas": COLUNAS_PRODUTO, "descricao_colunas": DESC_PRODUTO,
        "origem": _origem([a.pmc, a.pmvg, a.tuss_registros]),
        "observacoes": [
            "pf_total/pmc_total = alíquota de ICMS 17% (a mesma base que o Brasíndice usa). Outras alíquotas em `precos_extra`; use a do estado da clínica.",
            "codigo_tuss preenchido pelo arquivo oficial 'Registros ANVISA na TUSS de medicamentos' (junção por registro).",
            "Quantidade por embalagem não é publicada de forma estruturada: pf_unit/pmc_unit ficam vazios.",
        ]})


# ------------------------------------------------------------------ Brasíndice


def _ler_brasindice(caminho: Path) -> List[List[str]]:
    with open(caminho, encoding="latin-1", newline="") as f:
        return [r for r in csv.reader(f) if len(r) >= 19]


def _bras_campos(r: List[str]) -> Dict[str, str]:
    """Layout TXT D (23 colunas) ou reduzido (19 colunas).

    23 colunas: 0 cod_lab, 1 lab, 2 cod_prod, 3 nome, 4 cod_apres, 5 apresentação,
    6 PMC total, 7 PF total, 8 qtd, 9 'PMC', 10 PMC unit, 11 'PFB', 12 PF unit,
    13 edição da última alteração, 14 alíquota, 15 indicador de lista
    (S/N/T — não é "genérico" nem "restrito"; descartado), 16 EAN,
    17 código TISS Brasíndice (tabela 05), 18 genérico (S/N), 19 código TUSS,
    20 GGREM, 21 registro ANVISA, 22 código de apoio.
    19 colunas: 0–17 iguais e 18 = código TUSS.
    (Conferido cruzando EAN/GGREM/registro com a CMED e o nome "- GENERICO" /
    "(Restrito Hosp.)": o layout antigo que chamava a coluna 21 de 'tiss_med',
    a 17 de 'reg_anvisa', a 15 de 'generico' e a 18 de 'restrito' estava trocado.)
    Restrito hospitalar sai do nome "(Restrito Hosp.)" ou da CMED (mesmo EAN).
    """
    d = {"cod_lab": r[0], "lab": r[1], "cod_prod": r[2], "nome": r[3], "cod_apres": r[4],
         "apres": r[5], "pmc_total": r[6], "pf_total": r[7], "qtd": r[8], "pmc_unit": r[10],
         "pf_unit": r[12], "ed_preco": r[13], "ean": r[16].strip() if len(so_digitos(r[16])) >= 8 and so_digitos(r[16]).strip("0") else "",
         "tiss": r[17].strip(),
         "restrito": ""}
    if len(r) >= 23:
        d.update(generico=r[18], tuss=r[19], ggrem=r[20], registro=r[21])
    else:
        d.update(generico="S" if "GENERICO" in normalizar_texto(r[3]) else "", tuss=r[18], ggrem="", registro="")
    return {k: (v or "").strip() for k, v in d.items()}


def _chave_bras(d: Dict[str, str]) -> tuple:
    return (d["cod_lab"], d["cod_prod"], d["cod_apres"], d["ean"])


def _cmed_por(saida: Path) -> Dict[str, Dict[str, Dict[str, str]]]:
    """Índices da CMED já normalizada (por EAN e por registro)."""
    man = comum.carregar_manifest(saida)
    meta = man.get("conjuntos", {}).get("cmed/medicamentos")
    por_ean: Dict[str, Dict[str, str]] = {}
    por_reg: Dict[str, Dict[str, str]] = {}
    if not meta:
        print("aviso: CMED ainda não normalizada — princípio ativo ficará vazio no Brasíndice")
        return {"ean": por_ean, "reg": por_reg}
    for f in meta["fatias"]:
        for row in comum.ler_fatia(saida / "cmed/medicamentos" / f["arquivo"]):
            if row["ean"]:
                por_ean.setdefault(row["ean"], row)
            if row["registro_anvisa"]:
                por_reg.setdefault(row["registro_anvisa"], row)
    return {"ean": por_ean, "reg": por_reg}


def _bras_linha(d: Dict[str, str], edicao: str, tipo: str, cmed, extra: Optional[Dict[str, str]] = None) -> List[str]:
    extra = extra or {}
    reg = d["registro"] or extra.get("registro", "")
    ggrem = d["ggrem"] or extra.get("ggrem", "")
    generico = d["generico"] or extra.get("generico", "")
    c = cmed["ean"].get(d["ean"]) or (cmed["reg"].get(reg) if reg else None) or {}
    restr = "S" if "RESTRITO HOSP" in normalizar_texto(d["nome"]) else c.get("restrito_hospitalar", "")
    if c and not reg:
        reg = c.get("registro_anvisa", "")
    if c and not ggrem:
        ggrem = c.get("ggrem", "")
    return _linha_produto(
        fonte="BRASINDICE", edicao=edicao, tipo_item=tipo, codigo_fonte=d["tiss"], tabela_fonte="05",
        chave_fonte=f"{d['cod_lab']}-{d['cod_prod']}-{d['cod_apres']}", laboratorio=d["lab"],
        produto=d["nome"], apresentacao=d["apres"],
        principio_ativo=c.get("principio_ativo", "") if tipo == "medicamento" else "",
        ean=d["ean"], registro_anvisa=reg, codigo_tuss=d["tuss"] or extra.get("tuss", ""), ggrem=ggrem,
        generico=generico, restrito_hospitalar=restr, qtd_embalagem=numero(d["qtd"]),
        pf_total=numero(d["pf_total"]), pmc_total=numero(d["pmc_total"]),
        pf_unit=numero(d["pf_unit"]), pmc_unit=numero(d["pmc_unit"]),
        tipo_preco="BRAS_PF_PMC",
        vigencia=f"ed. {d['ed_preco']}" if d["ed_preco"] else "",
        tabela87_sugerida="20" if tipo == "medicamento" else "19")


def cmd_brasindice(a, tipo: str) -> None:
    saida = Path(a.saida)
    cmed = _cmed_por(saida)
    principal = [_bras_campos(r) for r in _ler_brasindice(Path(a.principal))]
    chaves_principal = {_chave_bras(d) for d in principal}
    compl: Dict[tuple, Dict[str, str]] = {}
    anteriores: set = set()
    arquivos_compl = [Path(p) for p in (a.complementar or [])]
    for p in arquivos_compl:
        for r in _ler_brasindice(p):
            d = _bras_campos(r)
            compl.setdefault(_chave_bras(d), d)
    if a.anterior:
        for r in _ler_brasindice(Path(a.anterior)):
            d = _bras_campos(r)
            anteriores.add(_chave_bras(d))
            compl.setdefault(_chave_bras(d), d)
    linhas = [_bras_linha(d, a.edicao, tipo, cmed, compl.get(_chave_bras(d))) for d in principal]
    adicionados = 0
    for k, d in compl.items():
        if k in chaves_principal or k in anteriores:
            continue  # já está na edição nova, ou saiu dela (descontinuado)
        linhas.append(_bras_linha(d, a.edicao_complementar or "?", tipo, cmed))
        adicionados += 1
    descont = len(anteriores - chaves_principal)
    conj = f"brasindice/{'medicamentos' if tipo == 'medicamento' else 'materiais'}"
    fatias = comum.gravar_fatiado(saida / conj, COLUNAS_PRODUTO, linhas, _chave_produto)
    obs = [
        "Layout do TXT conferido cruzando EAN/GGREM/registro com a CMED: coluna 17 = código TISS Brasíndice (vai na guia com tabela 05), 18 = genérico, 19 = código TUSS, 20 = GGREM, 21 = registro ANVISA. Restrito hospitalar vem do nome '(Restrito Hosp.)' ou da CMED.",
        "pf_unit/pmc_unit já vêm unitários da publicação. PMC 0 em item restrito hospitalar é normal.",
        "A coluna `vigencia` traz a edição em que o preço do item mudou pela última vez.",
    ]
    if tipo == "medicamento":
        obs.insert(0, f"Base = edição {a.edicao} ({len(principal)} itens). Da edição {a.edicao_complementar} "
                      f"entraram {adicionados} itens que não estão na {a.edicao} (arquivo 'Outros Fármacos', que a "
                      f"{a.edicao} recebida não traz); {descont} itens que saíram da {a.edicao} ficaram fora "
                      "(tratados como descontinuados). A edição de cada linha está na coluna `edicao`.")
        obs.insert(1, f"A edição {a.edicao} recebida tem layout reduzido (19 colunas, sem genérico/GGREM/registro): "
                      "esses campos vieram da edição anterior (mesma chave) ou da CMED (mesmo EAN).")
        obs.append("principio_ativo vem da CMED (junção por EAN; se não achar, por registro). Vazio = não achado.")
    registrar(saida, conj, fatias, {
        "titulo": f"Brasíndice — {'medicamentos' if tipo == 'medicamento' else 'materiais e insumos'}",
        "fonte": "Brasíndice (publicação licenciada)", "fonte_publica": "Brasíndice — arquivo TXT da edição",
        "edicao": a.edicao if tipo != "medicamento" else f"{a.edicao} (+{a.edicao_complementar} complementar)",
        "data_edicao": a.data or "não informada no arquivo",
        "licenca": "licenciada — incluída só como referência de nomenclatura/códigos",
        "descricao": "Nomenclatura, apresentação, EAN, código TISS (tabela 05) e TUSS, com PF/PMC indicativos.",
        "quando_usar": "nome/apresentação padrão, EAN, código TISS 05, TUSS",
        "colunas": COLUNAS_PRODUTO, "descricao_colunas": DESC_PRODUTO,
        "origem": _origem([Path(a.principal)] + ([Path(a.anterior)] if a.anterior else []) + arquivos_compl),
        "observacoes": obs})


# ------------------------------------------------------------------ SIMPRO

RE_VIG = re.compile(r"Desde\s+(\d{2})/(\d{2})/(\d{4})\s+R\$\s*([\d.,]+)")


def cmd_simpro(a) -> None:
    saida = Path(a.saida)
    por_codigo: Dict[str, List[str]] = {}
    ignoradas = 0
    with open(a.arquivo, encoding="utf-8", errors="replace", newline="") as f:
        for r in csv.DictReader(f, delimiter="|", quoting=csv.QUOTE_NONE):
            cod = (r.get("CODIGO") or "").strip()
            m = RE_VIG.search(r.get("VIGENCIA_ATUAL") or "")
            desc = " ".join((r.get("DESCRICAO") or "").split())
            if not re.fullmatch(r"\d{1,12}", cod) or not m or not desc:
                ignoradas += 1
                continue
            vig = f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
            base = desc.rstrip(".").strip()
            if ". " in base:
                produto, fabricante = base.rsplit(". ", 1)
            else:
                produto, fabricante = base, ""
            linha = _linha_produto(
                fonte="SIMPRO", edicao=a.edicao, tipo_item=a.tipo, codigo_fonte=cod, tabela_fonte="12",
                laboratorio=fabricante.strip(), produto=produto.strip(), apresentacao="",
                preco_ref=numero(m.group(4)),
                tipo_preco="SIMPRO_VIG",
                vigencia=vig, tabela87_sugerida="20" if a.tipo == "medicamento" else "19")
            ant = por_codigo.get(cod)
            if ant is None or vig > ant[_idx("vigencia")]:
                por_codigo[cod] = linha
    linhas = list(por_codigo.values())
    conj = f"simpro/{a.tipo}"
    fatias = comum.gravar_fatiado(saida / conj, COLUNAS_PRODUTO, linhas, _chave_produto)
    registrar(saida, conj, fatias, {
        "titulo": f"SIMPRO — {a.tipo}",
        "fonte": "SIMPRO (publicação licenciada), via coleta de portal de operadora que publica a tabela SIMPRO",
        "fonte_publica": "coleta de portal de operadora que publica a tabela SIMPRO",
        "edicao": a.edicao, "data_edicao": a.data or "", "licenca": "licenciada — incluída só como referência de nomenclatura/códigos",
        "descricao": "Descrição, fabricante, código SIMPRO (tabela 12) e valor vigente com data.",
        "quando_usar": "item sem Brasíndice (materiais sobretudo), código SIMPRO (tabela 12)",
        "colunas": COLUNAS_PRODUTO, "descricao_colunas": DESC_PRODUTO,
        "origem": _origem([Path(a.arquivo)], a.rotulo_origem or f"SIMPRO_{a.tipo.upper()}_coleta.csv"),
        "observacoes": [
            "`produto` e `laboratorio` foram separados no último '. ' da descrição publicada (ex.: 'SERINGA 10ML. FABRICANTE.').",
            "Campo bruto 'Desde dd/mm/aaaa R$ x,xxx' separado em `vigencia` (AAAA-MM-DD) e `preco_ref`.",
            f"Código repetido: ficou a vigência mais recente. Linhas inválidas ignoradas: {ignoradas}.",
            "Colunas sempre vazias ou constantes na coleta (capítulo, grupo, especialidade 'Todas'…) foram descartadas.",
        ]})


# ------------------------------------------------------------------ TUSS

COLS_TUSS_HIST = ["competencia", "codigo_terminologia", "terminologia", "codigo_termo", "termo",
                  "inicio_vigencia", "fim_vigencia", "fim_implantacao", "tipo_acao"]


def _data_br(v) -> str:
    if v is None or v == "":
        return ""
    if hasattr(v, "strftime"):
        return v.strftime("%Y-%m-%d")
    m = re.match(r"(\d{2})/(\d{2})/(\d{4})", str(v))
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else _txt(v)


def cmd_tuss_historico(a) -> None:
    saida = Path(a.saida)
    dados = Path(a.arquivo).read_bytes()
    try:
        texto = dados.decode("utf-8")
    except UnicodeDecodeError:
        texto = dados.decode("latin-1")
    rows = list(csv.reader(io.StringIO(texto), delimiter="\t"))
    linhas = []
    for r in rows[1:]:
        if len(r) < 9:
            continue
        linhas.append([_txt(r[0]), _txt(r[1]), _txt(r[2]), _txt(r[3]), _txt(r[4]),
                       _data_br(r[5]), _data_br(r[6]), _data_br(r[7]), _txt(r[8])])
    fatias = comum.gravar_fatiado(saida / "tuss/historico", COLS_TUSS_HIST, linhas,
                                  lambda l: normalizar_texto(l[4]))
    registrar(saida, "tuss/historico", fatias, {
        "titulo": "TUSS — histórico de alterações (inclusões, alterações, inativações)",
        "fonte": "ANS — Padrão TISS, Histórico da TUSS",
        "fonte_publica": "https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss",
        "edicao": a.competencia, "data_edicao": a.competencia, "licenca": "pública (ANS)",
        "descricao": "Registro das mudanças da TUSS na competência (não é a tabela TUSS completa). "
                     "Útil para saber se um código foi incluído, alterado ou inativado.",
        "quando_usar": "conferir se um código TUSS mudou/foi inativado",
        "colunas": COLS_TUSS_HIST, "descricao_colunas": {
            "competencia": "Mês/ano da publicação.", "codigo_terminologia": "Número da terminologia (19 materiais/OPME, 20 medicamentos, 64 forma de envio à ANS, 38 mensagens).",
            "terminologia": "Nome da terminologia.", "codigo_termo": "Código TUSS do termo.", "termo": "Descrição do termo.",
            "inicio_vigencia": "AAAA-MM-DD.", "fim_vigencia": "AAAA-MM-DD (vazio = vigente).",
            "fim_implantacao": "Prazo para operadoras/prestadores implantarem.", "tipo_acao": "Incluído, Alterado, Inativado…"},
        "origem": _origem([Path(a.arquivo)]),
        "observacoes": ["O kit não traz a TUSS completa de procedimentos (terminologia 22); para procedimentos use `cbhpm/portes` (código TUSS + descrição) e o contrato do convênio."]})


def cmd_tuss_registros(a) -> None:
    saida = Path(a.saida)
    reg = ler_tuss_registros(Path(a.arquivo))
    linhas = sorted([[t, r] for r, t in reg.items()])
    fatias = comum.gravar_fatiado(saida / "tuss/registros-anvisa-medicamentos", ["codigo_tuss", "registro_anvisa"],
                                  linhas, lambda l: l[0], fatiar_por_letra=False)
    registrar(saida, "tuss/registros-anvisa-medicamentos", fatias, {
        "titulo": "TUSS — registros ANVISA dos medicamentos (terminologia 20)",
        "fonte": "ANS — arquivo auxiliar 'Registros ANVISA na TUSS de medicamentos'",
        "fonte_publica": "https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss",
        "edicao": a.competencia, "data_edicao": a.competencia, "licenca": "pública (ANS)",
        "descricao": "Liga o registro ANVISA (13 dígitos) ao código TUSS do medicamento.",
        "quando_usar": "achar o código TUSS a partir do registro ANVISA",
        "colunas": ["codigo_tuss", "registro_anvisa"],
        "descricao_colunas": {"codigo_tuss": "Código do termo na terminologia 20.", "registro_anvisa": "Registro ANVISA (só dígitos)."},
        "origem": _origem([Path(a.arquivo)])})


def cmd_tuss_opme(a) -> None:
    saida = Path(a.saida)
    pub = "https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss"
    if a.nomes_tecnicos:
        tab = _ler_planilha(Path(a.nomes_tecnicos), lambda r: normalizar_texto(str(r[0] or "")) == "CODIGO DO TERMO")
        cols = ["codigo_tuss", "termo", "modelo", "fabricante", "inicio_vigencia", "fim_vigencia",
                "fim_implantacao", "registro_anvisa", "classe_risco"]
        linhas = [[_txt(r[0]), _txt(r[1]), _txt(r[2]), _txt(r[3]), _data_br(r[4]), _data_br(r[5]),
                   _data_br(r[6]), _txt(r[7]), _txt(r[8])] for r in tab[1:] if r[0]]
        f = comum.gravar_fatiado(saida / "tuss/opme-nomes-tecnicos", cols, linhas, lambda l: normalizar_texto(l[1]))
        registrar(saida, "tuss/opme-nomes-tecnicos", f, {
            "titulo": "TUSS — nomes técnicos ANVISA de OPME codificados", "fonte": "ANS — tabela auxiliar OPME",
            "fonte_publica": pub, "edicao": a.competencia, "data_edicao": a.competencia, "licenca": "pública (ANS)",
            "descricao": "Nomes técnicos de órteses, próteses e materiais especiais (OPME) com código TUSS.",
            "quando_usar": "código TUSS de OPME pelo nome técnico", "colunas": cols,
            "descricao_colunas": {c: "" for c in cols}, "origem": _origem([Path(a.nomes_tecnicos)])})
    if a.fabricantes:
        tab = _ler_planilha(Path(a.fabricantes), lambda r: normalizar_texto(str(r[0] or "")) == "REGISTRO ANVISA")
        cols = ["registro_anvisa", "classe_risco", "fabricante_nacional", "fabricante_internacional", "pais"]
        linhas = [[so_digitos(str(r[0])), _txt(r[1]), _txt(r[2]), _txt(r[3]), _txt(r[4])] for r in tab[1:] if r[0]]
        f = comum.gravar_fatiado(saida / "tuss/opme-fabricantes", cols, linhas, lambda l: normalizar_texto(l[2]))
        registrar(saida, "tuss/opme-fabricantes", f, {
            "titulo": "TUSS — fabricantes dos materiais e OPME (por registro ANVISA)",
            "fonte": "ANS — tabela auxiliar de fabricantes", "fonte_publica": pub, "edicao": a.competencia,
            "data_edicao": a.competencia, "licenca": "pública (ANS)",
            "descricao": "Registro ANVISA → fabricante nacional/internacional e classe de risco. Fatiado pela letra do fabricante nacional.",
            "quando_usar": "descobrir o fabricante de um material pelo registro", "colunas": cols,
            "descricao_colunas": {c: "" for c in cols}, "origem": _origem([Path(a.fabricantes)])})
    if a.envio_individualizado:
        tab = _ler_planilha(Path(a.envio_individualizado), lambda r: normalizar_texto(str(r[0] or "")).startswith("NOME TECNICO"))
        cols = ["nome_tecnico", "codigo_tuss"]
        linhas = [[_txt(r[0]), _txt(r[1])] for r in tab[1:] if r[0] and len(r) > 1 and r[1]]
        f = comum.gravar_fatiado(saida / "tuss/opme-envio-individualizado", cols, linhas,
                                 lambda l: normalizar_texto(l[0]), fatiar_por_letra=False)
        registrar(saida, "tuss/opme-envio-individualizado", f, {
            "titulo": "TUSS — OPME com envio individualizado à ANS (Tabela 64)", "fonte": "ANS — tabela auxiliar",
            "fonte_publica": pub, "edicao": a.competencia, "data_edicao": a.competencia, "licenca": "pública (ANS)",
            "descricao": "Nomes técnicos de OPME que precisam ser enviados de forma individualizada.",
            "quando_usar": "raramente (OPME)", "colunas": cols, "descricao_colunas": {c: "" for c in cols},
            "origem": _origem([Path(a.envio_individualizado)])})


# ------------------------------------------------------------------ CBHPM


def cmd_cbhpm(a) -> None:
    saida = Path(a.saida)
    tab = _ler_planilha(Path(a.arquivo), lambda r: "CODIGO_TUSS" in normalizar_texto(str(r[0] or "")).replace(" ", "_"))
    cols = ["codigo_tuss", "codigo_cbhpm", "descricao", "porte", "custo_operacional_uco", "pagina_publicacao"]
    linhas = [[_txt(x) for x in r[:6]] for r in tab[1:] if r and r[0]]
    f = comum.gravar_fatiado(saida / "cbhpm/portes", cols, linhas, lambda l: l[0], fatiar_por_letra=False)
    registrar(saida, "cbhpm/portes", f, {
        "titulo": "CBHPM 5ª edição (2008) — portes por código TUSS",
        "fonte": "CBHPM 5ª edição (publicação licenciada da AMB)", "fonte_publica": "CBHPM 5ª edição (2008)",
        "edicao": "5ª (2008)", "data_edicao": "2008", "licenca": "licenciada — incluída só como referência de nomenclatura/códigos",
        "descricao": "Procedimento (código TUSS e CBHPM, descrição) com porte e custo operacional (UCO).",
        "quando_usar": "nome e código de procedimento/serviço; porte quando o contrato for CBHPM",
        "colunas": cols, "descricao_colunas": {
            "codigo_tuss": "Código TUSS (terminologia 22).", "codigo_cbhpm": "Código na CBHPM.",
            "descricao": "Descrição extraída do PDF (pode ter cortes/ruído de extração).",
            "porte": "Porte CBHPM (ex.: 2B).", "custo_operacional_uco": "Unidades de custo operacional.",
            "pagina_publicacao": "Página no livro."},
        "origem": _origem([Path(a.arquivo)]),
        "observacoes": ["Edição antiga (2008): o VALOR do porte depende do contrato (edição da CBHPM, deflator/inflator). Use o porte/código como referência, nunca como preço.",
                        "Descrições vieram de extração de PDF; algumas linhas trazem texto de cabeçalho junto."]})


# ------------------------------------------------------------------ TISS

XSD_UTEIS = ["tissV4_03_00.xsd", "tissSimpleTypesV4_03_00.xsd", "tissComplexTypesV4_03_00.xsd",
             "tissGuiasV4_03_00.xsd", "tissWebServicesV4_03_00.xsd", "tissAssinaturaDigital_v1.01.xsd",
             "xmldsig-core-schema.xsd"]

# Tabela 87 (tabela de tabelas) — códigos que aparecem nos domínios dm_tabela* do XSD
# e no domínio do convênio do Sistema Rabi (05, 12 e 97 ampliados em 24/09/2026).
TABELA_87 = [
    ("00", "Tabela Própria das Operadoras", "XSD dm_tabela (comentário oficial)"),
    ("05", "Brasíndice", "XSD dm_tabelaGeral; domínio do convênio no Rabi"),
    ("12", "SIMPRO", "XSD dm_tabelaGeral; domínio do convênio no Rabi"),
    ("18", "TUSS — Taxas hospitalares, diárias e gases medicinais", "XSD dm_tabela (comentário oficial)"),
    ("19", "TUSS — Materiais (e OPME)", "XSD dm_tabela (comentário oficial)"),
    ("20", "TUSS — Medicamentos", "XSD dm_tabela (comentário oficial)"),
    ("22", "TUSS — Procedimentos e eventos em saúde", "XSD dm_tabela (comentário oficial)"),
    ("90", "Tabela própria de pacote (conferir descrição exata no componente organizacional TISS)", "XSD dm_tabela (sem comentário)"),
    ("97", "Taxa Própria (domínio do Sistema Rabi)", "manual Rabi, configurações do convênio"),
    ("98", "Tabela própria de pacotes (conferir descrição exata no componente organizacional TISS)", "XSD dm_tabela (sem comentário)"),
]


def extrair_dominios(xsd_texto: str) -> List[List[str]]:
    """(dominio, codigo, descricao) de cada simpleType com enumeration.

    A descrição vem dos comentários '<!-- CODIGO descrição -->' dentro do tipo,
    quando existem (o XSD só publica os códigos; a descrição oficial fica no
    componente organizacional/terminologias TUSS).
    """
    saida = []
    for m in re.finditer(r'<simpleType name="(dm_[^"]+)">(.*?)</simpleType>', xsd_texto, re.S):
        nome, corpo = m.group(1), m.group(2)
        codigos = re.findall(r'<enumeration value="([^"]*)"\s*/>', corpo)
        if not codigos:
            continue
        coment = {}
        texto = " ".join(" ".join(c.split()) for c in re.findall(r"<!--(.*?)-->", corpo, re.S))
        for cod in codigos:
            if not cod:
                continue
            mm = re.search(r"(?<![\w])" + re.escape(cod) + r"(?![\w])\s*[-_–]?\s*"
                           r"([^*]+?)(?=\s+\d+\s*[-–_]\s|\s+[-_–]?\s*\d{2,}(?![\w,.])|\s*\*|$)", texto)
            if mm and re.search(r"[A-Za-zÀ-ú]", mm.group(1)):
                coment[cod] = mm.group(1).replace(" _ ", " — ").strip(" -_–")
        for cod in codigos:
            saida.append([nome, cod, coment.get(cod, "")])
    return saida


def cmd_tiss(a) -> None:
    saida = Path(a.saida)
    origem = Path(a.schemas)
    dest = saida / "tiss" / f"schemas-{a.versao}"
    dest.mkdir(parents=True, exist_ok=True)
    copiados = []
    for nome in XSD_UTEIS:
        src = origem / nome
        if src.exists():
            shutil.copyfile(src, dest / nome)
            copiados.append(src)
    simple = origem / f"tissSimpleTypesV{a.versao.replace('.', '_')}.xsd"
    dom = extrair_dominios(simple.read_bytes().decode("latin-1")) if simple.exists() else []
    f = comum.gravar_fatiado(saida / "tiss/dominios", ["dominio", "codigo", "descricao"], dom,
                             lambda l: l[0], fatiar_por_letra=False)
    registrar(saida, "tiss/dominios", f, {
        "titulo": f"TISS {a.versao} — domínios (enumerações dm_*) do XSD",
        "fonte": f"ANS — Padrão TISS, componente de comunicação {a.versao} (tissSimpleTypes)",
        "fonte_publica": "https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss",
        "edicao": a.versao, "data_edicao": "", "licenca": "pública (ANS)",
        "descricao": "Lista de todos os domínios aceitos no XML TISS com seus códigos; descrição só quando o XSD traz comentário.",
        "quando_usar": "validar um código de domínio do XML (tabela, tipo de atendimento…)",
        "colunas": ["dominio", "codigo", "descricao"],
        "descricao_colunas": {"dominio": "Nome do tipo no XSD (dm_…).", "codigo": "Valor aceito.",
                              "descricao": "Comentário do próprio XSD (vazio quando o XSD não descreve)."},
        "origem": _origem([simple] if simple.exists() else [])})
    f87 = comum.gravar_fatiado(saida / "tiss/tabela-87", ["codigo", "descricao", "base"],
                               [list(x) for x in TABELA_87], lambda l: l[0], fatiar_por_letra=False)
    registrar(saida, "tiss/tabela-87", f87, {
        "titulo": "Tabela 87 — tabela de tabelas (referência do código do item)",
        "fonte": "ANS (XSD TISS dm_tabela/dm_tabelaGeral) + manual do Sistema Rabi (domínio do convênio)",
        "fonte_publica": "https://www.rabisistemas.com.br/manual/modulos/configuracoes.html",
        "edicao": a.versao, "data_edicao": "", "licenca": "pública (ANS)",
        "descricao": "Diz de qual tabela é o código do item na guia: 20 medicamento TUSS, 19 material TUSS, 05 Brasíndice, 12 SIMPRO…",
        "quando_usar": "escolher a tabela 87 de produto/serviço/taxa no convênio",
        "colunas": ["codigo", "descricao", "base"],
        "descricao_colunas": {"codigo": "Código da tabela.", "descricao": "Descrição.", "base": "De onde veio a descrição."},
        "origem": [],
        "observacoes": ["Não confundir: Tabela 36 = indicador de acidente; Tabela 87 = tabela de tabelas.",
                        "Qual tabela usar no convênio (TUSS 20/19 ou 05/12) é definido pelo contrato do convênio."]})
    gerar_indice_tiss(saida, a.versao, copiados)


def gerar_indice_tiss(saida: Path, versao: str, copiados: List[Path]) -> None:
    pasta = saida / "tiss"
    sch = pasta / f"schemas-{versao}"
    linhas_sch = [f"# Schemas XSD TISS {versao}", "",
                  CABECALHO_MD.format(fonte="ANS — Padrão TISS, componente de comunicação", conferido=HOJE,
                                      edicao=f"versão {versao}", kit=comum.KIT_VERSAO),
                  "Cópia dos XSD oficiais úteis para validar/entender o XML de faturamento. Não edite.", "",
                  "| Arquivo | Bytes | Para que serve |", "|---|---|---|"]
    uso = {"tissV4_03_00.xsd": "raiz da mensagem TISS",
           "tissSimpleTypesV4_03_00.xsd": "domínios (dm_*) e tipos simples — ver ../dominios/",
           "tissComplexTypesV4_03_00.xsd": "estruturas (beneficiário, procedimento, outras despesas…)",
           "tissGuiasV4_03_00.xsd": "guias (consulta, SP/SADT, honorários, outras despesas)",
           "tissWebServicesV4_03_00.xsd": "mensagens de webservice", "tissAssinaturaDigital_v1.01.xsd": "assinatura digital",
           "xmldsig-core-schema.xsd": "XML Signature (W3C)"}
    for p in sorted(sch.glob("*.xsd")):
        linhas_sch.append(f"| [{p.name}]({p.name}) | {p.stat().st_size} | {uso.get(p.name, '')} |")
    (sch / "00-INDICE.md").write_text("\n".join(linhas_sch) + "\n", encoding="utf-8")
    man = comum.carregar_manifest(saida)
    linhas = ["# TISS/ANS (schemas e domínios)", "",
              CABECALHO_MD.format(fonte="ANS — Padrão TISS", conferido=HOJE, edicao=f"versão {versao}", kit=comum.KIT_VERSAO),
              "| Pasta | O que tem | Quando usar |", "|---|---|---|",
              f"| [schemas-{versao}/](schemas-{versao}/00-INDICE.md) | XSD oficiais ({len(list(sch.glob('*.xsd')))} arquivos) | validar/entender o XML TISS |"]
    for nome in ("tiss/dominios", "tiss/tabela-87"):
        m = man["conjuntos"].get(nome, {})
        sub = nome.split("/")[1]
        linhas.append(f"| [{sub}/]({sub}/00-INDICE.md) | {m.get('titulo', '')} ({m.get('linhas', 0)} linhas) | {m.get('quando_usar', '')} |")
    linhas += ["", "Não incluídos (grandes e em PDF/planilha de layout): componente organizacional, "
               "componente de conteúdo e estrutura, segurança. Consulte no site da ANS."]
    (pasta / "00-INDICE.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")


def cmd_indices(a) -> None:
    saida = Path(a.saida)
    man = comum.carregar_manifest(saida)
    for nome, meta in man.get("conjuntos", {}).items():
        gerar_indice_conjunto(saida, nome, meta)
    gerar_indices_pastas(saida)
    print("índices refeitos")


# ------------------------------------------------------------------ CLI


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--saida", default=str(comum.REFERENCIAS_PADRAO), help="pasta referencias/ (padrão: a do kit)")
    sp = p.add_subparsers(dest="cmd", required=True)

    s = sp.add_parser("cmed")
    s.add_argument("--pmc", required=True); s.add_argument("--pmvg")
    s.add_argument("--tuss-registros"); s.add_argument("--edicao", required=True); s.add_argument("--data", default="")

    for nome in ("brasindice-medicamentos", "brasindice-materiais"):
        s = sp.add_parser(nome)
        s.add_argument("--principal", required=True); s.add_argument("--edicao", required=True)
        s.add_argument("--anterior", help="mesma publicação na edição anterior (para detectar descontinuados)")
        s.add_argument("--complementar", action="append", help="arquivo extra (ex.: Outros Fármacos)")
        s.add_argument("--edicao-complementar", default=""); s.add_argument("--data", default="")

    s = sp.add_parser("simpro")
    s.add_argument("--tipo", required=True, choices=["material", "medicamento", "saneante", "reagente"])
    s.add_argument("--arquivo", required=True); s.add_argument("--edicao", required=True); s.add_argument("--data", default="")
    s.add_argument("--rotulo-origem", default="", help="nome a registrar no índice no lugar do nome do arquivo bruto")

    s = sp.add_parser("tuss-historico"); s.add_argument("--arquivo", required=True); s.add_argument("--competencia", required=True)
    s = sp.add_parser("tuss-registros-anvisa"); s.add_argument("--arquivo", required=True); s.add_argument("--competencia", required=True)
    s = sp.add_parser("tuss-opme")
    s.add_argument("--nomes-tecnicos"); s.add_argument("--fabricantes"); s.add_argument("--envio-individualizado")
    s.add_argument("--competencia", required=True)
    s = sp.add_parser("cbhpm"); s.add_argument("--arquivo", required=True)
    s = sp.add_parser("tiss"); s.add_argument("--schemas", required=True); s.add_argument("--versao", default="4.03.00")
    sp.add_parser("indices")

    a = p.parse_args(argv)
    Path(a.saida).mkdir(parents=True, exist_ok=True)
    {"cmed": cmd_cmed,
     "brasindice-medicamentos": lambda x: cmd_brasindice(x, "medicamento"),
     "brasindice-materiais": lambda x: cmd_brasindice(x, "material"),
     "simpro": cmd_simpro, "tuss-historico": cmd_tuss_historico,
     "tuss-registros-anvisa": cmd_tuss_registros, "tuss-opme": cmd_tuss_opme,
     "cbhpm": cmd_cbhpm, "tiss": cmd_tiss, "indices": cmd_indices}[a.cmd](a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
