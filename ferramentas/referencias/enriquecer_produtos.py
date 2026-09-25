"""Sugere dados de referência para a lista de produtos da clínica (para CONFIRMAÇÃO humana).

Fonte: referencias/ (Brasíndice, SIMPRO, CMED, TUSS) · Conferido em 2026-09-25 · Kit v0.1.0
Só biblioteca padrão. NUNCA grava no Rabi: gera um CSV de candidatos que o
implantador confirma linha a linha (coluna `decisao`).

Entrada: CSV da clínica (separador ; , ou tab; UTF-8 ou latin-1) com colunas
(maiúsculas/minúsculas tanto faz):
  nome (ou produto/descricao)  — obrigatório
  apresentacao                 — opcional (ex.: "500 mg cx 30 cprs")
  fabricante                   — opcional
  codigo                       — opcional (EAN, registro ANVISA, TUSS ou código da fonte)
  tipo                         — opcional: medicamento | material

Saída: CSV UTF-8 ';' com até 3 candidatos por item, pontuação, campos
sugeridos e classificação ÓTIMO / BOM / RESSALVA / SEM MATCH.

Uso:
  python3 ferramentas/referencias/enriquecer_produtos.py dados/produtos.csv \
      --saida dados/produtos-candidatos.csv [--referencias-clinica DIR]

``--referencias-clinica`` aponta a pasta com as tabelas PRÓPRIAS da clínica
(ver config/referencias-da-clinica.md no repo dela). Elas prevalecem: entram
primeiro na busca e ganham preferência na pontuação.

Critérios (aprendidos em implantação real):
  ÓTIMO  = código exato (EAN/registro/TUSS/código da fonte) ou nome+dose batem e
           o fabricante bate (ou não foi informado);
  BOM    = nome e dose batem, fabricante diferente ou não conferível;
  RESSALVA = nome parecido mas dose/apresentação/fabricante diverge — revisar;
  SEM MATCH = nada acima de 50 pontos (candidato a cotação direta ou tabela própria).
Manipulados, vacinas e material de limpeza em geral não têm código de
Brasíndice/SIMPRO e costumam ficar sem cobrança (Utiliza desmarcado) — a
decisão é da clínica.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Dict, List, Optional

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ferramentas.referencias import comum  # noqa: E402
from ferramentas.referencias.buscar import buscar, tokens_nome  # noqa: E402
from ferramentas.referencias.comum import extrair_doses, normalizar_texto, so_digitos  # noqa: E402

COLUNAS_SAIDA = [
    "item", "nome_clinica", "apresentacao_clinica", "fabricante_clinica", "codigo_clinica",
    "candidato", "classificacao", "pontos", "motivo",
    "fonte", "edicao", "conjunto", "codigo_fonte", "tabela_fonte",
    "produto_ref", "apresentacao_ref", "laboratorio_ref", "principio_ativo", "ean",
    "registro_anvisa", "codigo_tuss", "tabela87_sugerida",
    "pf_total", "pmc_total", "pf_unit", "pmc_unit", "preco_ref", "tipo_preco", "vigencia",
    "observacao", "decisao",
]

FONTES_MED = ["brasindice/medicamentos", "cmed/medicamentos", "simpro/medicamento"]
FONTES_MAT = ["brasindice/materiais", "simpro/material", "simpro/saneante", "simpro/reagente"]

ALERTAS = [
    (("MANIPUL",), "manipulado: em geral sem código Brasíndice/SIMPRO; avaliar tabela própria ou Utiliza desmarcado"),
    (("VACINA",), "vacina: costuma ter preço próprio/particular; confirmar se o convênio cobre"),
    (("DETERGENTE", "LIMPEZA", "ALCOOL 70", "SABAO", "DESINFET"), "material de limpeza: em geral não é cobrado do convênio"),
]


def _get(reg: Dict[str, str], *nomes: str) -> str:
    for n in nomes:
        if reg.get(n):
            return reg[n].strip()
    return ""


def _fabricante_bate(fab: str, lab: str) -> Optional[bool]:
    if not fab:
        return None
    f = set(tokens_nome(normalizar_texto(fab))) - {"LTDA", "SA", "S/A", "IND", "INDUSTRIA", "FARMACEUTICA", "LABORATORIO", "COMERCIO"}
    l = set(tokens_nome(normalizar_texto(lab)))
    if not f or not l:
        return None
    return any(any(w.startswith(x) or x.startswith(w) for w in l if len(w) >= 3) for x in f if len(x) >= 3)


def classificar(pontos: float, por_codigo: bool, conflito_dose: bool, fab_ok: Optional[bool],
                dose_confirmada: bool = True) -> str:
    """ÓTIMO pede evidência: código exato, ou nome+dose com fabricante que não diverge,
    ou nome com fabricante que bate (quando a clínica não informou dose)."""
    if por_codigo:
        return "ÓTIMO"
    if pontos < 50:
        return "SEM MATCH"
    if conflito_dose:
        return "RESSALVA"
    if pontos >= 90 and fab_ok is not False and (dose_confirmada or fab_ok is True):
        return "ÓTIMO"
    if pontos >= 75:
        return "BOM"
    return "RESSALVA"


def enriquecer_item(nome: str, apresentacao: str = "", fabricante: str = "", codigo: str = "",
                    tipo: str = "", raiz: Optional[Path] = None,
                    referencias_clinica: Optional[Path] = None, top: int = 3) -> List[Dict[str, str]]:
    """Devolve até ``top`` candidatos (dicts com COLUNAS_SAIDA menos os campos do item)."""
    t = normalizar_texto(tipo)
    fontes = FONTES_MED if t.startswith("MED") else FONTES_MAT if t.startswith("MAT") else None
    if fontes is None:
        fontes = FONTES_MED + FONTES_MAT
    cands: List[Dict[str, str]] = []
    cod = so_digitos(codigo)
    if len(cod) >= 6:
        cands += buscar(cod, fontes=fontes, limite=10, raiz=raiz, referencias_clinica=referencias_clinica)
    termo = f"{nome} {apresentacao}".strip()
    cands += buscar(termo, fontes=fontes, limite=30, raiz=raiz, referencias_clinica=referencias_clinica)
    q_doses = extrair_doses(normalizar_texto(termo))
    vistos, saida = set(), []
    for c in cands:
        chave = (c.get("fonte"), c.get("codigo_fonte"), c.get("produto"), c.get("apresentacao"))
        if chave in vistos:
            continue
        vistos.add(chave)
        por_codigo = c.get("casou_por", "nome") != "nome"
        fab_ok = _fabricante_bate(fabricante, c.get("laboratorio", ""))
        pontos = float(c["pontos"])
        if not por_codigo and fab_ok is True:
            pontos = min(100.0, pontos + 5)
        elif not por_codigo and fab_ok is False:
            pontos = max(0.0, pontos - 5)
        c_doses = extrair_doses(normalizar_texto(f"{c.get('produto', '')} {c.get('apresentacao', '')}"))
        unidades_q = {u for u, _ in q_doses}
        conflito = bool(q_doses) and not (q_doses & c_doses) and any(u in unidades_q for u, _ in c_doses)
        motivo = []
        if por_codigo:
            motivo.append(f"código exato ({c.get('casou_por')})")
        else:
            motivo.append("nome+dose" if q_doses and q_doses <= c_doses else "nome")
        if conflito:
            motivo.append("dose diferente")
        if fab_ok is True:
            motivo.append("fabricante bate")
        elif fab_ok is False:
            motivo.append("fabricante diferente")
        if c.get("conjunto", "").startswith("clinica/"):
            motivo.append("tabela própria da clínica")
        obs = []
        nn = normalizar_texto(nome)
        for chaves, texto in ALERTAS:
            if any(k in nn for k in chaves):
                obs.append(texto)
        if c.get("restrito_hospitalar") == "S":
            obs.append("restrito hospitalar: PMC 0 é normal")
        if c.get("qtd_embalagem") and c.get("qtd_embalagem") not in ("1", "") and c.get("pf_unit"):
            obs.append(f"embalagem com {c['qtd_embalagem']} unidades: confira se a clínica usa por unidade (pf_unit)")
        saida.append({
            "classificacao": classificar(pontos, por_codigo, conflito, fab_ok,
                                         dose_confirmada=bool(q_doses) and q_doses <= c_doses),
            "pontos": f"{pontos:.1f}",
            "motivo": "; ".join(motivo),
            "fonte": c.get("fonte", ""), "edicao": c.get("edicao", ""), "conjunto": c.get("conjunto", ""),
            "codigo_fonte": c.get("codigo_fonte", ""), "tabela_fonte": c.get("tabela_fonte", ""),
            "produto_ref": c.get("produto", ""), "apresentacao_ref": c.get("apresentacao", ""),
            "laboratorio_ref": c.get("laboratorio", ""), "principio_ativo": c.get("principio_ativo", ""),
            "ean": c.get("ean", ""), "registro_anvisa": c.get("registro_anvisa", ""),
            "codigo_tuss": c.get("codigo_tuss", ""),
            "tabela87_sugerida": c.get("tabela87_sugerida", "") or ("20" if t.startswith("MED") else "19" if t.startswith("MAT") else ""),
            "pf_total": c.get("pf_total", ""), "pmc_total": c.get("pmc_total", ""),
            "pf_unit": c.get("pf_unit", ""), "pmc_unit": c.get("pmc_unit", ""),
            "preco_ref": c.get("preco_ref", ""), "tipo_preco": c.get("tipo_preco", ""),
            "vigencia": c.get("vigencia", ""), "observacao": "; ".join(obs), "decisao": "",
            "_ordem": (0 if por_codigo else 1, -pontos, 0 if c.get("conjunto", "").startswith("clinica/") else 1),
        })
    saida.sort(key=lambda r: r["_ordem"])
    for r in saida:
        r.pop("_ordem")
    if not saida or saida[0]["classificacao"] == "SEM MATCH":
        obs = [texto for chaves, texto in ALERTAS if any(k in normalizar_texto(nome) for k in chaves)]
        return [{"classificacao": "SEM MATCH", "pontos": saida[0]["pontos"] if saida else "0",
                 "motivo": "nenhum candidato com 50+ pontos",
                 "observacao": "; ".join(obs + ["pedir cotação/tabela própria ou buscar com outro nome"]),
                 "decisao": ""}]
    return saida[:top]


def enriquecer_arquivo(entrada: Path, saida: Path, raiz: Optional[Path] = None,
                       referencias_clinica: Optional[Path] = None, top: int = 3) -> Dict[str, int]:
    itens = comum.ler_csv_generico(entrada)
    contagem: Dict[str, int] = {}
    linhas = []
    for i, bruto in enumerate(itens, 1):
        reg = {(k or "").strip().lower(): (v or "").strip() for k, v in bruto.items()}
        nome = _get(reg, "nome", "produto", "descricao", "descrição")
        if not nome:
            continue
        apres = _get(reg, "apresentacao", "apresentação")
        fab = _get(reg, "fabricante", "laboratorio", "laboratório")
        cod = _get(reg, "codigo", "código", "ean")
        tipo = _get(reg, "tipo")
        cands = enriquecer_item(nome, apres, fab, cod, tipo, raiz=raiz,
                                referencias_clinica=referencias_clinica, top=top)
        melhor = cands[0]["classificacao"]
        contagem[melhor] = contagem.get(melhor, 0) + 1
        for j, c in enumerate(cands, 1):
            linha = {k: "" for k in COLUNAS_SAIDA}
            linha.update(c)
            linha.update(item=str(i), nome_clinica=nome, apresentacao_clinica=apres,
                         fabricante_clinica=fab, codigo_clinica=cod, candidato=str(j))
            linhas.append(linha)
    saida = Path(saida)
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS_SAIDA, delimiter=";", lineterminator="\n")
        w.writeheader()
        w.writerows(linhas)
    return contagem


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("entrada", help="CSV de produtos da clínica")
    p.add_argument("--saida", help="CSV de candidatos (padrão: <entrada>-candidatos.csv)")
    p.add_argument("--raiz", help="pasta referencias/ (padrão: a do kit)")
    p.add_argument("--referencias-clinica", help="pasta com as tabelas próprias da clínica (prevalecem)")
    p.add_argument("--top", type=int, default=3)
    a = p.parse_args(argv)
    ent = Path(a.entrada)
    sai = Path(a.saida) if a.saida else ent.with_name(ent.stem + "-candidatos.csv")
    cont = enriquecer_arquivo(ent, sai, raiz=Path(a.raiz) if a.raiz else None,
                              referencias_clinica=Path(a.referencias_clinica) if a.referencias_clinica else None,
                              top=a.top)
    print(f"gravado: {sai}")
    for k in ("ÓTIMO", "BOM", "RESSALVA", "SEM MATCH"):
        print(f"  {k}: {cont.get(k, 0)} item(ns) (melhor candidato)")
    print("Nada foi gravado no Rabi. Mostre as sugestões ao usuário e marque a coluna `decisao`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
