"""Confere a previsão do motor contra o que o Rabi devolve na aba Farol.

Uso:
  python3 -m ferramentas.conversao.conferir_farol cenario.json \\
      [--csv precos.csv] --servicos farol-servicos.json --itens farol-itens.json \\
      [--produtos farol-produtos.json] [--ignorar-inativos] [--tolerancia 0.01] [--saida conferencia.md]

Arquivos lidos (GET da API externa, envelope ``{"dados": [...]}`` ou lista;
junte todas as páginas antes):
  GET /convenios/{id}/farol/servicos  → servico_id, servico, custo_total, receita_total,
       receita_propria_servico, margem_resultado_pct, farol, ativo_no_convenio, servico_ativo
  GET /convenios/{id}/farol/itens     → servico_raiz_id, item_tipo, item_id, item_nome, custo,
       receita, farol, utiliza  (campos do spec 2026-09-25; se vierem também conta_no_total /
       motivo_exclusao, eles são conferidos)
  GET /convenios/{id}/farol/produtos  → produto_id, custo, receita, margem_resultado_pct, farol,
       ativo_no_convenio, produto_ativo

Margem da API = (receita − custo) ÷ receita × 100; índice do Farol = receita ÷ custo × 100.
Sai com código 1 se houver divergência.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional

if __package__ in (None, ""):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    __package__ = "ferramentas.conversao"

from . import motor  # noqa: E402
from .simulador import carregar  # noqa: E402


@dataclass
class Divergencia:
    servico: str
    item: str
    campo: str
    previsto: object
    lido: object
    nota: str = ""


def _lista(obj) -> list:
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        for k in ("dados", "data", "items", "itens"):
            if isinstance(obj.get(k), list):
                return obj[k]
    return []


def ler(caminho: Optional[str]) -> list:
    if not caminho:
        return []
    with open(caminho, encoding="utf-8") as f:
        return _lista(json.load(f))


def norm_farol(v) -> Optional[str]:
    if v is None:
        return None
    s = str(v).strip().upper()
    if s in ("", "SEM_FAROL", "NONE", "NULL"):
        return None
    if s in ("SEM_CUSTO", "ROXO", "SEM CUSTO"):
        return motor.ROXO
    return s


def norm_tipo(v) -> str:
    s = str(v or "").lower().replace("-", "").replace("_", "").replace("ç", "c").replace(" ", "")
    return "subservico" if s in ("servico", "subservico") else s


def margem(receita, custo) -> Optional[float]:
    if receita is None or custo is None or receita == 0:
        return None
    return (receita - custo) / receita * 100


def _dif(a, b, tol) -> bool:
    if a is None or b is None:
        return (a is None) != (b is None)
    return abs(float(a) - float(b)) > tol


def conferir_servicos(cat, conv, api: list, tol: float, ignorar_inativos: bool) -> List[Divergencia]:
    out = []
    for reg in api:
        sid = reg.get("servico_id")
        s = cat.servicos.get(sid)
        nome = f"[{sid}] {reg.get('servico') or (s.nome if s else '?')}"
        if ignorar_inativos and (reg.get("servico_ativo") is False or (s is not None and not s.ativo)):
            continue
        if s is None:
            out.append(Divergencia(nome, "—", "servico_id", "(fora do catálogo do cenário)", sid))
            continue
        r = motor.calcular_servico(cat, conv, sid)
        pares = [("receita_total", r.total, reg.get("receita_total")),
                 ("receita_propria_servico", r.base, reg.get("receita_propria_servico")),
                 ("custo_total", r.custo if r.arvore.tem_produto else 0.0, reg.get("custo_total"))]
        for campo, prev, lido in pares:
            if lido is not None and _dif(prev, lido, tol):
                out.append(Divergencia(nome, "(serviço)", campo, prev, lido))
        mg = margem(r.total, r.custo)
        if reg.get("margem_resultado_pct") is not None and mg is not None and _dif(mg, reg["margem_resultado_pct"], 0.5):
            out.append(Divergencia(nome, "(serviço)", "margem_resultado_pct", round(mg, 2), reg["margem_resultado_pct"]))
        if "farol" in reg and norm_farol(reg.get("farol")) != r.farol:
            out.append(Divergencia(nome, "(serviço)", "farol", r.farol, reg.get("farol")))
        if "ativo_no_convenio" in reg and bool(reg["ativo_no_convenio"]) != r.utiliza:
            out.append(Divergencia(nome, "(serviço)", "ativo_no_convenio", r.utiliza, reg["ativo_no_convenio"]))
    return out


def _previstas(r: motor.ResultadoServico) -> List[motor.Linha]:
    return [l for l in r.linhas if l.tipo in ("produto", "taxa", "subservico")]


def conferir_itens(cat, conv, api: list, tol: float, ignorar_inativos: bool) -> List[Divergencia]:
    out = []
    por_raiz: Dict[int, list] = defaultdict(list)
    for reg in api:
        por_raiz[reg.get("servico_raiz_id")].append(reg)
    for raiz, regs in sorted(por_raiz.items(), key=lambda x: (x[0] is None, x[0])):
        s = cat.servicos.get(raiz)
        nome = f"[{raiz}] {s.nome if s else '?'}"
        if s is None:
            out.append(Divergencia(nome, "—", "servico_raiz_id", "(fora do catálogo do cenário)", raiz))
            continue
        if ignorar_inativos and not s.ativo:
            continue
        r = motor.calcular_servico(cat, conv, raiz)
        fila: Dict[tuple, list] = defaultdict(list)
        for l in _previstas(r):
            fila[(l.tipo, l.id)].append(l)
        for reg in regs:
            tipo, iid = norm_tipo(reg.get("item_tipo")), reg.get("item_id")
            item = f"{tipo} [{iid}] {reg.get('item_nome', '')}".strip()
            if tipo == "subservico" and iid == raiz and not fila.get((tipo, iid)):
                prev = r.arvore  # linha do próprio serviço raiz
            elif fila.get((tipo, iid)):
                prev = fila[(tipo, iid)].pop(0)
            else:
                out.append(Divergencia(nome, item, "linha", "(não prevista)", "presente na API"))
                continue
            if reg.get("receita") is not None and _dif(prev.receita, reg["receita"], tol):
                potencial = (prev.quantidade * prev.valor_unitario) if prev.valor_unitario is not None else None
                nota = ""
                if potencial is not None and not prev.conta and not _dif(potencial, reg["receita"], tol):
                    nota = (f"a API mostra o preço do item ({potencial:.2f}); a previsão diz que ele NÃO conta "
                            f"({prev.motivo}) — confira 'Conta no total' na tela")
                out.append(Divergencia(nome, item, "receita", prev.receita, reg["receita"], nota))
            custo_prev = prev.custo if prev.tem_produto else None
            if reg.get("custo") is not None and custo_prev is not None and _dif(custo_prev, reg["custo"], tol):
                out.append(Divergencia(nome, item, "custo", custo_prev, reg["custo"]))
            if "utiliza" in reg and prev is not r.arvore and prev.utiliza is not None \
                    and bool(reg["utiliza"]) != prev.utiliza:
                out.append(Divergencia(nome, item, "utiliza", prev.utiliza, reg["utiliza"]))
            if reg.get("farol") is not None and norm_farol(reg["farol"]) != prev.farol and prev.tem_produto:
                out.append(Divergencia(nome, item, "farol", prev.farol, reg["farol"]))
            if "conta_no_total" in reg and prev is not r.arvore:
                lido = reg["conta_no_total"]
                lido_b = lido if isinstance(lido, bool) else str(lido).strip().lower() in ("sim", "true", "1")
                if lido_b != prev.conta:
                    out.append(Divergencia(nome, item, "conta_no_total", prev.conta, lido))
            if reg.get("motivo_exclusao") and prev.motivo and reg["motivo_exclusao"] != prev.motivo:
                out.append(Divergencia(nome, item, "motivo_exclusao", prev.motivo, reg["motivo_exclusao"]))
        for (tipo, iid), resto in fila.items():
            for l in resto:
                out.append(Divergencia(nome, f"{tipo} [{iid}] {l.nome}", "linha", "prevista", "(ausente na API)"))
    return out


def conferir_produtos(cat, conv, api: list, tol: float, ignorar_inativos: bool) -> List[Divergencia]:
    out = []
    for reg in api:
        pid = reg.get("produto_id")
        p = cat.produtos.get(pid)
        nome = f"produto [{pid}] {reg.get('produto', '')}".strip()
        if ignorar_inativos and (reg.get("produto_ativo") is False or (p is not None and not p.ativo)):
            continue
        if p is None:
            out.append(Divergencia(nome, "—", "produto_id", "(fora do catálogo do cenário)", pid))
            continue
        f = motor.farol_produto(cat, conv, pid)
        if reg.get("receita") is not None and _dif(f["receita"], reg["receita"], tol):
            out.append(Divergencia(nome, "(produto)", "receita", f["receita"], reg["receita"]))
        if reg.get("custo") is not None and f["custo"] is not None and _dif(f["custo"], reg["custo"], tol):
            out.append(Divergencia(nome, "(produto)", "custo", f["custo"], reg["custo"]))
        if "farol" in reg and norm_farol(reg.get("farol")) != f["farol"]:
            out.append(Divergencia(nome, "(produto)", "farol", f["farol"], reg.get("farol")))
        cp = conv.produtos.get(pid)
        if "ativo_no_convenio" in reg and bool(reg["ativo_no_convenio"]) != bool(cp and cp.utiliza):
            out.append(Divergencia(nome, "(produto)", "ativo_no_convenio", bool(cp and cp.utiliza),
                                   reg["ativo_no_convenio"]))
    return out


def relatorio(divs: List[Divergencia], cont: Dict[str, int]) -> str:
    out = ["# Conferência do Farol — previsto (motor do kit) × lido (API)", ""]
    out.append(" · ".join(f"{k}: {v} linha(s) lidas" for k, v in cont.items()))
    out.append("")
    if not divs:
        out.append("**Nenhuma divergência.** Previsão e Rabi concordam.")
        return "\n".join(out) + "\n"
    out.append(f"**{len(divs)} divergência(s).** Investigue cada uma antes de dizer que o convênio está pronto.")
    out += ["", "| Serviço | Item | Campo | Previsto | Lido | Nota |", "|---|---|---|---|---|---|"]
    for d in divs:
        out.append(f"| {d.servico} | {d.item} | {d.campo} | {d.previsto} | {d.lido} | {d.nota} |")
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Previsão do motor × /convenios/{id}/farol/*")
    ap.add_argument("cenario")
    ap.add_argument("--csv")
    ap.add_argument("--fontes")
    ap.add_argument("--servicos", help="JSON do GET /farol/servicos")
    ap.add_argument("--itens", help="JSON do GET /farol/itens")
    ap.add_argument("--produtos", help="JSON do GET /farol/produtos")
    ap.add_argument("--ignorar-inativos", action="store_true")
    ap.add_argument("--tolerancia", type=float, default=0.01)
    ap.add_argument("--saida", help="grava o relatório .md aqui")
    a = ap.parse_args(argv)
    cat, conv, _ = carregar(a.cenario, a.csv, a.fontes)
    serv, itens, prods = ler(a.servicos), ler(a.itens), ler(a.produtos)
    divs = (conferir_servicos(cat, conv, serv, a.tolerancia, a.ignorar_inativos)
            + conferir_itens(cat, conv, itens, a.tolerancia, a.ignorar_inativos)
            + conferir_produtos(cat, conv, prods, a.tolerancia, a.ignorar_inativos))
    rel = relatorio(divs, {"servicos": len(serv), "itens": len(itens), "produtos": len(prods)})
    if a.saida:
        with open(a.saida, "w", encoding="utf-8") as f:
            f.write(rel)
    print(rel)
    return 1 if divs else 0


if __name__ == "__main__":
    sys.exit(main())
