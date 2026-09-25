"""Busca nas tabelas de referência normalizadas (Brasíndice, SIMPRO, CMED, TUSS, CBHPM).

Fonte: referencias/manifest.json · Conferido em 2026-09-25 · Kit v0.1.0
Só biblioteca padrão. Lê SÓ as fatias necessárias (pela letra inicial dos
termos); se achar pouco, amplia para as demais fatias do conjunto, sempre
linha a linha (nunca carrega a tabela inteira na memória).

Uso:
  python3 ferramentas/referencias/buscar.py "dipirona 500 mg"
  python3 ferramentas/referencias/buscar.py "seringa 10 ml" --fontes simpro/material,brasindice/materiais
  python3 ferramentas/referencias/buscar.py 7896006220503          # EAN
  python3 ferramentas/referencias/buscar.py 1049715390080          # registro ANVISA
  python3 ferramentas/referencias/buscar.py 90605233               # código TUSS
  python3 ferramentas/referencias/buscar.py "dipirona" --referencias-clinica ../minhas-tabelas

Em Python:
  from ferramentas.referencias.buscar import buscar
  for r in buscar("dipirona 500 mg", limite=5): print(r["pontos"], r["produto"])

Pontuação 0–100: nome (tokens) + dose/concentração; código exato (EAN,
registro ANVISA, TUSS, código da fonte) = 100. É uma SUGESTÃO para
confirmação humana — nunca grava nada.
"""
from __future__ import annotations

import argparse
import csv as _csv
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ferramentas.referencias import comum  # noqa: E402
from ferramentas.referencias.comum import extrair_doses, normalizar_texto, remover_doses, so_digitos  # noqa: E402

FONTES_PRODUTO = ["brasindice/medicamentos", "brasindice/materiais", "cmed/medicamentos",
                  "simpro/medicamento", "simpro/material", "simpro/saneante", "simpro/reagente"]

# Campos de texto usados na busca por conjunto (conjuntos que não são de produto).
CAMPOS_TEXTO = {
    "tuss/historico": ["termo", "terminologia"],
    "tuss/opme-nomes-tecnicos": ["termo", "modelo", "fabricante"],
    "tuss/opme-fabricantes": ["fabricante_nacional", "fabricante_internacional"],
    "tuss/opme-envio-individualizado": ["nome_tecnico"],
    "cbhpm/portes": ["descricao"],
    "tiss/dominios": ["dominio", "descricao"],
    "tiss/tabela-87": ["descricao"],
}
CAMPOS_CODIGO = ["ean", "registro_anvisa", "codigo_tuss", "codigo_fonte", "ggrem", "codigo_termo",
                 "codigo_cbhpm", "codigo"]

PALAVRAS_VAZIAS = {"DE", "DA", "DO", "DAS", "DOS", "E", "C", "X", "P", "PARA", "EM", "A", "O",
                   "CX", "UN", "UND", "UNID", "CT", "UNIDADE", "UNIDADES", "SEM", "S", "EMB", "EMBALAGEM"}

# Formas/embalagens: abreviações das fontes viram uma forma canônica e pesam
# metade na pontuação (o nome do produto é o que mais importa).
FORMAS = {
    "CPR": {"COMPRIMIDO", "COMPRIMIDOS", "CPR", "CPRS", "COMP", "COMPR", "CP", "COM"},
    "CAP": {"CAPSULA", "CAPSULAS", "CAP", "CAPS"},
    "AMP": {"AMPOLA", "AMPOLAS", "AMP", "AMPS"},
    "FA": {"FA", "FRASCO-AMPOLA"},
    "FR": {"FRASCO", "FRASCOS", "FR", "FRS"},
    "SOL": {"SOLUCAO", "SOL"},
    "INJ": {"INJETAVEL", "INJ", "INJET"},
    "SUS": {"SUSPENSAO", "SUSP", "SUS"},
    "GTS": {"GOTAS", "GOTA", "GOT", "GTS"},
    "XPE": {"XAROPE", "XPE"},
    "CREM": {"CREME", "CREM"},
    "POM": {"POMADA", "POM"},
    "SER": {"SERINGA", "SERINGAS", "SER"},
    "AG": {"AGULHA", "AGULHAS", "AG"},
    "OR": {"ORAL", "OR"},
    "BL": {"BLISTER", "BL"},
}
_CANON = {v: k for k, vs in FORMAS.items() for v in vs}


def tokens_nome(texto_normalizado: str) -> List[str]:
    t = remover_doses(texto_normalizado)
    out = []
    for tok in "".join(ch if ch.isalnum() else " " for ch in t).split():
        tok = _CANON.get(tok, tok)
        if tok in PALAVRAS_VAZIAS or tok.isdigit() or len(tok) < 2:
            continue
        out.append(tok)
    return out


def _eh_codigo(termo: str) -> bool:
    d = so_digitos(termo)
    return len(d) >= 6 and len(d) >= len(termo.replace(" ", "").replace(".", "").replace("-", "")) - 1


def _fatias_de(raiz: Path, conjunto: str, man: Dict) -> List[Dict]:
    meta = man.get("conjuntos", {}).get(conjunto)
    return list(meta.get("fatias", [])) if meta else []


def _prefixo_casa(prefixo: str, tokens: Sequence[str]) -> bool:
    if not prefixo:
        return True
    for t in tokens:
        p = comum.prefixo_letra(t, len(prefixo) if prefixo not in ("0-9", "_") else 1)
        if p == prefixo or (len(prefixo) == 1 and t[:1] == prefixo):
            return True
    return False


def _pontuar(q_tokens: List[str], q_doses: set, reg: Dict[str, str], campos: Sequence[str]) -> float:
    if not q_tokens and not q_doses:
        return 0.0
    principal = normalizar_texto(reg.get(campos[0], ""))
    secundario = normalizar_texto(" ".join(reg.get(c, "") for c in campos[1:]))
    w_princ = set(tokens_nome(principal))
    w_ativo = set(tokens_nome(normalizar_texto(reg.get("principio_ativo", ""))))
    w_sec = set(tokens_nome(secundario))
    todos = w_princ | w_sec | w_ativo
    nome = 0.0
    peso_total = 0.0
    for t in q_tokens:
        peso = 0.5 if t in FORMAS else 1.0
        peso_total += peso
        if t in w_princ:
            nome += peso * 1.0
        elif t in w_ativo:
            nome += peso * 0.9
        elif t in w_sec:
            nome += peso * (1.0 if t in FORMAS else 0.7)
        elif len(t) >= 4 and any(w.startswith(t) for w in todos):
            nome += peso * 0.6
        elif any(len(w) >= 4 and t.startswith(w) for w in todos):
            nome += peso * 0.4
    nome = nome / peso_total if peso_total else 1.0
    if q_tokens and principal.startswith(q_tokens[0]):
        nome = min(1.0, nome + 0.05)
    # pequena preferência por nomes "enxutos" (menos palavras sobrando)
    prod_tokens = tokens_nome(normalizar_texto(reg.get(campos[0], "")))
    if prod_tokens:
        sobra = sum(1 for w in prod_tokens if w not in q_tokens and not any(w.startswith(t) for t in q_tokens))
        nome -= min(0.1, 0.02 * sobra)
    if not q_doses:
        return max(0.0, round(100 * nome, 1))
    c_doses = extrair_doses(normalizar_texto(" ".join(reg.get(c, "") for c in campos)))
    if q_doses <= c_doses:
        unidades_q = {u for u, _ in q_doses}
        extras = [d for d in c_doses - q_doses if d[0] in unidades_q]
        dose = 1.0 if not extras else 0.85  # associação (ex.: 500 MG + 65 MG)
    elif q_doses & c_doses:
        dose = 0.6
    elif any(u in {x[0] for x in c_doses} for u, _ in q_doses):
        dose = -0.4  # mesma unidade, valor diferente: conflito de dose
    else:
        dose = 0.2  # candidato não informa dose
    return max(0.0, round(100 * (0.7 * nome + 0.3 * dose), 1))


def _campos(conjunto: str) -> List[str]:
    if conjunto in CAMPOS_TEXTO:
        return CAMPOS_TEXTO[conjunto]
    return ["produto", "apresentacao", "laboratorio"]


def _ler_clinica(dir_clinica: Path) -> Iterable[tuple]:
    """(conjunto, registro) de cada CSV da clínica (prevalece sobre o kit)."""
    for arq in sorted(Path(dir_clinica).rglob("*.csv")):
        for r in comum.ler_csv_generico(arq):
            r = {(k or "").strip().lower(): (v or "").strip() for k, v in r.items()}
            if "produto" not in r:
                r["produto"] = r.get("nome", "") or r.get("descricao", "")
            r.setdefault("fonte", f"CLINICA:{arq.name}")
            r.setdefault("edicao", r.get("edicao", ""))
            yield f"clinica/{arq.stem}", r


def buscar(termo: str, fontes: Optional[Sequence[str]] = None, limite: int = 10,
           raiz: Optional[Path] = None, referencias_clinica: Optional[Path] = None,
           amplo: bool = False, minimo: float = 30.0) -> List[Dict[str, str]]:
    """Devolve até ``limite`` registros (dicts) com ``pontos``, ``conjunto`` e campos da fonte.

    ``fontes``: lista de conjuntos (ex.: ["brasindice/medicamentos"]) ou prefixos
    (ex.: ["simpro"]). Padrão: todos os conjuntos de produto.
    ``referencias_clinica``: pasta com CSVs próprios da clínica; entram primeiro
    e ganham +5 pontos de preferência.
    """
    raiz = Path(raiz or comum.REFERENCIAS_PADRAO)
    man = comum.carregar_manifest(raiz)
    todos = list(man.get("conjuntos", {}))
    if fontes:
        conjuntos = [c for c in todos if any(c == f or c.startswith(f.rstrip("/") + "/") for f in fontes)]
    else:
        conjuntos = [c for c in FONTES_PRODUTO if c in todos]
    q = normalizar_texto(termo)
    codigo = so_digitos(q) if _eh_codigo(q) else ""
    q_tokens = tokens_nome(q)
    q_doses = extrair_doses(q)
    filtro = [t for t in q_tokens if len(t) >= 3] or q_tokens
    resultados: List[Dict[str, str]] = []

    def avaliar(conjunto: str, reg: Dict[str, str], bonus: float = 0.0) -> None:
        if codigo:
            for c in CAMPOS_CODIGO:
                v = so_digitos(reg.get(c, ""))
                if v and (v == codigo or v.lstrip("0") == codigo.lstrip("0")):
                    r = dict(reg); r["pontos"] = 100.0; r["conjunto"] = conjunto; r["casou_por"] = c
                    resultados.append(r)
                    return
            return
        p = _pontuar(q_tokens, q_doses, reg, _campos(conjunto)) + bonus
        if p >= minimo:
            r = dict(reg); r["pontos"] = min(100.0, round(p, 1)); r["conjunto"] = conjunto; r["casou_por"] = "nome"
            resultados.append(r)

    if referencias_clinica:
        for conj, reg in _ler_clinica(Path(referencias_clinica)):
            avaliar(conj, reg, bonus=5.0)

    def varrer(fatias_por_conj: Dict[str, List[Dict]]) -> None:
        for conj, fatias in fatias_por_conj.items():
            for f in fatias:
                caminho = raiz / conj / f["arquivo"]
                with open(caminho, encoding="utf-8", newline="") as fh:
                    cab = fh.readline()
                    nomes = next(_csv.reader([cab], delimiter=";"))
                    for linha in fh:
                        up = linha.translate(comum._TRADUZ).upper()
                        if codigo:
                            if codigo.lstrip("0") not in up:
                                continue
                        elif filtro and not any(t in up for t in filtro):
                            continue
                        vals = next(_csv.reader([linha.rstrip("\n")], delimiter=";"))
                        avaliar(conj, dict(zip(nomes, vals)))

    lidas: Dict[str, set] = {}
    primeira: Dict[str, List[Dict]] = {}
    for conj in conjuntos:
        fatias = _fatias_de(raiz, conj, man)
        if codigo or amplo or not q_tokens:
            escolhidas = fatias
        else:
            escolhidas = [f for f in fatias if _prefixo_casa(f["prefixo"], q_tokens)]
        primeira[conj] = escolhidas
        lidas[conj] = {f["arquivo"] for f in escolhidas}
    varrer(primeira)
    bons = [r for r in resultados if r["pontos"] >= 60]
    if not codigo and not amplo and len(bons) < limite:
        resto = {c: [f for f in _fatias_de(raiz, c, man) if f["arquivo"] not in lidas[c]] for c in conjuntos}
        varrer(resto)
    resultados.sort(key=lambda r: (-r["pontos"], not r["conjunto"].startswith("clinica/"),
                                   r.get("produto", r.get("termo", r.get("descricao", "")))))
    return resultados[:limite]


def formatar(resultados: List[Dict[str, str]]) -> str:
    if not resultados:
        return "(nenhum resultado)"
    linhas = ["| pts | fonte/edição | código | nome | apresentação | laboratório | EAN | TUSS | preço ref. |",
              "|---|---|---|---|---|---|---|---|---|"]
    for r in resultados:
        nome = r.get("produto") or r.get("termo") or r.get("descricao") or r.get("nome_tecnico") or r.get("dominio", "")
        cod = r.get("codigo_fonte") or r.get("codigo_termo") or r.get("codigo_tuss") or r.get("codigo", "")
        if r.get("tabela_fonte"):
            cod = f"{cod} (tab {r['tabela_fonte']})"
        preco = ""
        if r.get("pf_unit") or r.get("pf_total"):
            preco = f"PF un {r.get('pf_unit') or '-'} / PF {r.get('pf_total') or '-'} / PMC {r.get('pmc_total') or '-'}"
        elif r.get("preco_ref"):
            preco = f"{r['preco_ref']} ({r.get('vigencia', '')})"
        linhas.append("| {} | {} {} | {} | {} | {} | {} | {} | {} | {} |".format(
            r["pontos"], r.get("fonte", r["conjunto"]), r.get("edicao", ""), cod, nome,
            r.get("apresentacao", ""), r.get("laboratorio", r.get("fabricante", "")), r.get("ean", ""),
            r.get("codigo_tuss", ""), preco).replace("\n", " "))
    return "\n".join(linhas)


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("termo", help="nome (com dose), EAN, registro ANVISA ou código TUSS")
    p.add_argument("--fontes", help="conjuntos separados por vírgula (ex.: brasindice,cmed/medicamentos,tuss/historico)")
    p.add_argument("--limite", type=int, default=10)
    p.add_argument("--raiz", help="pasta referencias/ (padrão: a do kit)")
    p.add_argument("--referencias-clinica", help="pasta com CSVs próprios da clínica (prevalecem)")
    p.add_argument("--amplo", action="store_true", help="ler todas as fatias (mais lento)")
    a = p.parse_args(argv)
    fontes = [f.strip() for f in a.fontes.split(",")] if a.fontes else None
    res = buscar(a.termo, fontes=fontes, limite=a.limite, raiz=Path(a.raiz) if a.raiz else None,
                 referencias_clinica=Path(a.referencias_clinica) if a.referencias_clinica else None, amplo=a.amplo)
    print(formatar(res))
    print("\nPreço é só indicativo (edição da fonte). Confirme com a tabela da clínica/contrato do convênio.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
