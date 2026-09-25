"""Confere a previsão do motor contra o que o Rabi devolve na aba Farol.

Uso:
  python3 .kit/ferramentas/conversao/conferir_farol.py cenario.json \\
      [--csv precos-<slug>.csv] --servicos farol-servicos.json --itens farol-itens.json \\
      [--produtos farol-produtos.json] [--ignorar-inativos] [--tolerancia 0.01] [--saida conferencia.md]

Arquivos lidos (GET da API externa, envelope padrão ``{"dados": [...], "page", "pageSize",
"total", "totalPages"}`` ou lista; junte todas as páginas antes). Nomes de campo = resposta
REAL de produção medida em 25/09/2026 (o Swagger de 25/09 está incompleto no Farol e, em
``/farol/itens``, traz nomes que a resposta real não usa):

  GET /convenios/{id}/farol/servicos → servico_id, servico, receita_total, receita_propria_servico,
       receita_produtos, receita_servicos, receita_taxas, custo_total, custo_produtos,
       margem_resultado_pct, farol, ativo_no_convenio, servico_ativo, somar_itens, zerar_valor
  GET /convenios/{id}/farol/itens    → servico_raiz_id, servico_pai_id, item_tipo, item_id, item_nome,
       quantidade, quantidade_efetiva, receita_unitaria, receita_item_total, custo_item_total,
       conta_no_total, motivo_exclusao, utiliza_no_convenio, zerar_valor,
       receita_total_servico, custo_total_servico, margem_servico_pct, farol_servico
       (compatível com o formato do Swagger: receita, custo, farol, utiliza)
  GET /convenios/{id}/farol/produtos → produto_id, produto, receita, receita_sem_zerar, custo,
       fator_k, fonte_id, fonte_nome, origem_receita, zerar_valor, margem_resultado_pct, farol,
       ativo_no_convenio, produto_ativo  (campos dbg_* são de diagnóstico; os *_centavos estão
       em centavos)

Margem da API = (receita − custo) ÷ receita × 100; índice do Farol = receita ÷ custo × 100.
Interpretações ainda não confirmadas pela fonte (tratadas com tolerância, nunca como erro certo):
  * ``receita_item_total`` de item FORA da conta: aceita 0 ou o preço cheio, desde que
    ``conta_no_total`` concorde com a previsão;
  * ``quantidade_efetiva``: aceita quantidade × multiplicadores dos pais, ou 0 se o item está fora;
  * ``receita`` de produto com ``zerar_valor``: aceita o preço ou 0 (``receita_sem_zerar`` = preço);
  * ``receita_servicos`` do serviço: aceita com ou sem o valor próprio do serviço.
Sai com código 1 se houver divergência.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

if __package__ in (None, ""):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    __package__ = "ferramentas.conversao"

from . import motor  # noqa: E402
from .simulador import carregar  # noqa: E402

MOTIVOS_OFICIAIS = (motor.NAO_UTILIZA, motor.ZERADO_EM_PACOTE, motor.PAI_FORA)


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


def _g(reg: dict, *nomes):
    """Primeiro campo presente e preenchido (nome real primeiro, nome do Swagger depois)."""
    for n in nomes:
        if reg.get(n) is not None:
            return reg[n]
    return None


def _tem(reg: dict, *nomes) -> bool:
    return any(n in reg for n in nomes)


def _bool(v) -> Optional[bool]:
    if v is None:
        return None
    if isinstance(v, bool):
        return v
    return str(v).strip().lower() in ("sim", "true", "1", "s")


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


def _norm_nome(v) -> str:
    s = unicodedata.normalize("NFKD", str(v or "")).encode("ascii", "ignore").decode()
    return " ".join(s.upper().split())


def margem(receita, custo) -> Optional[float]:
    if receita is None or custo is None or receita == 0:
        return None
    return (receita - custo) / receita * 100


def _dif(a, b, tol) -> bool:
    if a is None or b is None:
        return (a is None) != (b is None)
    return abs(float(a) - float(b)) > tol


def _algum_igual(lido, aceitos, tol) -> bool:
    return any(not _dif(a, lido, tol) for a in aceitos)


# --------------------------------------------------------------------------- /farol/servicos

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
        custo_prev = r.custo if r.arvore.tem_produto else 0.0
        pares = [("receita_total", r.total), ("receita_propria_servico", r.base), ("custo_total", custo_prev),
                 ("custo_produtos", custo_prev), ("receita_produtos", r.receita_por_tipo.get("produto")),
                 ("receita_taxas", r.receita_por_tipo.get("taxa"))]
        for campo, prev in pares:
            lido = reg.get(campo)
            if lido is not None and prev is not None and _dif(prev, lido, tol):
                out.append(Divergencia(nome, "(serviço)", campo, prev, lido))
        if reg.get("receita_servicos") is not None:
            com = r.receita_por_tipo.get("servico", 0.0)
            if not _algum_igual(reg["receita_servicos"], (com, com - r.base), tol):
                out.append(Divergencia(nome, "(serviço)", "receita_servicos", round(com - r.base, 2),
                                       reg["receita_servicos"], "sem o valor próprio (com ele: "
                                       f"{round(com, 2)})"))
        mg = margem(r.total, r.custo)
        if reg.get("margem_resultado_pct") is not None and mg is not None and _dif(mg, reg["margem_resultado_pct"], 0.5):
            out.append(Divergencia(nome, "(serviço)", "margem_resultado_pct", round(mg, 2), reg["margem_resultado_pct"]))
        if "farol" in reg and norm_farol(reg.get("farol")) != r.farol:
            out.append(Divergencia(nome, "(serviço)", "farol", r.farol, reg.get("farol")))
        if "ativo_no_convenio" in reg and bool(reg["ativo_no_convenio"]) != r.utiliza:
            out.append(Divergencia(nome, "(serviço)", "ativo_no_convenio", r.utiliza, reg["ativo_no_convenio"]))
        if reg.get("somar_itens") is not None and _bool(reg["somar_itens"]) != bool(s.somar_itens):
            out.append(Divergencia(nome, "(serviço)", "somar_itens", s.somar_itens, reg["somar_itens"]))
        sc = conv.servicos.get(sid)
        if reg.get("zerar_valor") is not None and _bool(reg["zerar_valor"]) != bool(sc and sc.zerar):
            out.append(Divergencia(nome, "(serviço)", "zerar_valor", bool(sc and sc.zerar), reg["zerar_valor"]))
    return out


# --------------------------------------------------------------------------- /farol/itens

def _previstas(r: motor.ResultadoServico) -> List[motor.Linha]:
    return [l for l in r.linhas if l.tipo in ("produto", "taxa", "subservico")]


def _com_multiplicador(raiz: motor.Linha) -> List[Tuple[motor.Linha, float, int]]:
    """(linha, multiplicador dos pais, id do pai). Filhos de subserviço valem por 1 unidade do pai."""
    out: List[Tuple[motor.Linha, float, int]] = []

    def andar(pai: motor.Linha, mult: float):
        for f in pai.filhos:
            if f.tipo not in ("produto", "taxa", "subservico"):
                continue
            out.append((f, mult, pai.id))
            if f.tipo == "subservico":
                andar(f, mult * f.quantidade)

    andar(raiz, 1.0)
    return out


def _conferir_totais_do_servico(nome, r, regs, tol) -> List[Divergencia]:
    """Campos do serviço raiz repetidos em cada linha de /farol/itens (resposta real)."""
    out = []
    custo_prev = r.custo if r.arvore.tem_produto else 0.0
    for campo, prev, t in (("receita_total_servico", r.total, tol), ("custo_total_servico", custo_prev, tol),
                           ("margem_servico_pct", margem(r.total, r.custo), 0.5)):
        lidos = {reg[campo] for reg in regs if reg.get(campo) is not None}
        for lido in sorted(lidos):
            if prev is not None and _dif(prev, lido, t):
                out.append(Divergencia(nome, "(serviço, em /itens)", campo,
                                       round(prev, 2) if campo.startswith("margem") else prev, lido))
    lidos = {norm_farol(reg.get("farol_servico")) for reg in regs if "farol_servico" in reg}
    for lido in lidos:
        if lido != r.farol:
            out.append(Divergencia(nome, "(serviço, em /itens)", "farol_servico", r.farol, lido))
    return out


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
        out += _conferir_totais_do_servico(nome, r, regs, tol)
        fila: Dict[tuple, list] = defaultdict(list)
        for l, mult, pai in _com_multiplicador(r.arvore):
            fila[(l.tipo, l.id)].append((l, mult, pai))
        for reg in regs:
            tipo, iid = norm_tipo(reg.get("item_tipo")), reg.get("item_id")
            item = f"{tipo} [{iid}] {reg.get('item_nome', '')}".strip()
            cands = fila.get((tipo, iid)) or []
            if tipo == "subservico" and iid == raiz and not cands:
                prev, mult = r.arvore, 1.0  # linha do próprio serviço raiz
            elif cands:
                pai_lido = reg.get("servico_pai_id")
                idx = next((i for i, c in enumerate(cands) if pai_lido is None or c[2] == pai_lido), 0)
                prev, mult, _ = cands.pop(idx)
            else:
                out.append(Divergencia(nome, item, "linha", "(não prevista)", "presente na API"))
                continue
            out += _conferir_item(nome, item, prev, mult, reg, prev is r.arvore, tol)
        for (tipo, iid), resto in fila.items():
            for l, _, _ in resto:
                out.append(Divergencia(nome, f"{tipo} [{iid}] {l.nome}", "linha", "prevista", "(ausente na API)"))
    return out


def _conferir_item(nome, item, prev: motor.Linha, mult: float, reg: dict, e_raiz: bool,
                   tol: float) -> List[Divergencia]:
    out = []
    conta_lida = _bool(reg.get("conta_no_total")) if "conta_no_total" in reg else None
    receita = _g(reg, "receita_item_total", "receita")
    campo_rec = "receita_item_total" if reg.get("receita_item_total") is not None else "receita"
    prev_rec = motor.r2(prev.receita * mult)
    if receita is not None and _dif(prev_rec, receita, tol):
        potencial = (prev.quantidade * prev.valor_unitario * mult) if prev.valor_unitario is not None else None
        cheio = potencial is not None and not _dif(potencial, receita, tol)
        if not (cheio and not prev.conta and conta_lida is False):
            nota = ""
            if cheio and not prev.conta:
                nota = (f"a API mostra o preço do item ({potencial:.2f}); a previsão diz que ele NÃO conta "
                        f"({prev.motivo}) — confira 'Conta no total' na tela")
            out.append(Divergencia(nome, item, campo_rec, prev_rec, receita, nota))
    if not e_raiz and prev.valor_unitario is not None and reg.get("receita_unitaria") is not None \
            and _dif(prev.valor_unitario, reg["receita_unitaria"], tol):
        out.append(Divergencia(nome, item, "receita_unitaria", prev.valor_unitario, reg["receita_unitaria"],
                               f"origem do preço na previsão: {prev.origem_preco}"))
    custo = _g(reg, "custo_item_total", "custo")
    custo_prev = motor.r2(prev.custo * mult) if prev.tem_produto else None
    if custo is not None and custo_prev is not None and _dif(custo_prev, custo, tol):
        out.append(Divergencia(nome, item, "custo_item_total" if reg.get("custo_item_total") is not None
                               else "custo", custo_prev, custo))
    if not e_raiz:
        if reg.get("quantidade") is not None and _dif(prev.quantidade, reg["quantidade"], 0.0001):
            out.append(Divergencia(nome, item, "quantidade", prev.quantidade, reg["quantidade"]))
        if reg.get("quantidade_efetiva") is not None:
            aceitos = [prev.quantidade * mult] + ([0.0] if not prev.conta else [])
            if not _algum_igual(reg["quantidade_efetiva"], aceitos, 0.0001):
                out.append(Divergencia(nome, item, "quantidade_efetiva", aceitos[0], reg["quantidade_efetiva"]))
        uti = _g(reg, "utiliza_no_convenio", "utiliza")
        if uti is not None and prev.utiliza is not None and _bool(uti) != prev.utiliza:
            out.append(Divergencia(nome, item, "utiliza_no_convenio" if "utiliza_no_convenio" in reg
                                   else "utiliza", prev.utiliza, uti))
        if reg.get("zerar_valor") is not None and prev.zerar is not None and _bool(reg["zerar_valor"]) != prev.zerar:
            out.append(Divergencia(nome, item, "zerar_valor", prev.zerar, reg["zerar_valor"]))
        if conta_lida is not None and conta_lida != prev.conta:
            out.append(Divergencia(nome, item, "conta_no_total", prev.conta, reg["conta_no_total"],
                                   f"motivo previsto: {prev.motivo}" if prev.motivo else ""))
    if reg.get("farol") is not None and norm_farol(reg["farol"]) != prev.farol and prev.tem_produto:
        out.append(Divergencia(nome, item, "farol", prev.farol, reg["farol"]))
    if reg.get("motivo_exclusao") and prev.motivo in MOTIVOS_OFICIAIS \
            and str(reg["motivo_exclusao"]).strip().upper() != prev.motivo:
        out.append(Divergencia(nome, item, "motivo_exclusao", prev.motivo, reg["motivo_exclusao"]))
    return out


# --------------------------------------------------------------------------- /farol/produtos

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
        pr = motor.valor_produto(p, conv)
        cp = conv.produtos.get(pid)
        zerar = _bool(reg.get("zerar_valor")) if reg.get("zerar_valor") is not None else bool(cp and cp.zerar)
        explica = (f"API: origem_receita={reg.get('origem_receita')}, fonte={reg.get('fonte_nome')}, "
                   f"fator_k={reg.get('fator_k')} · previsão: {pr.origem} ({pr.detalhe})")
        if reg.get("receita_sem_zerar") is not None and _dif(f["receita"], reg["receita_sem_zerar"], tol):
            out.append(Divergencia(nome, "(produto)", "receita_sem_zerar", f["receita"], reg["receita_sem_zerar"],
                                   explica))
        if reg.get("receita") is not None:
            aceitos = [f["receita"]] + ([0.0] if zerar else [])
            if not _algum_igual(reg["receita"], aceitos, tol):
                out.append(Divergencia(nome, "(produto)", "receita", f["receita"], reg["receita"], explica))
        if reg.get("custo") is not None and f["custo"] is not None and _dif(f["custo"], reg["custo"], tol):
            out.append(Divergencia(nome, "(produto)", "custo", f["custo"], reg["custo"]))
        if pr.fator_k is not None and "fator_k" in reg and _dif(pr.fator_k, reg.get("fator_k") or 0.0, tol):
            out.append(Divergencia(nome, "(produto)", "fator_k", pr.fator_k, reg.get("fator_k")))
        if pr.origem == "FONTE" and reg.get("fonte_nome") and _norm_nome(reg["fonte_nome"]) != _norm_nome(pr.fonte):
            out.append(Divergencia(nome, "(produto)", "fonte_nome", pr.fonte, reg["fonte_nome"]))
        if "farol" in reg and norm_farol(reg.get("farol")) != f["farol"]:
            out.append(Divergencia(nome, "(produto)", "farol", f["farol"], reg.get("farol")))
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
