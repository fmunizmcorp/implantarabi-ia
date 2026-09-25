"""Simulador: prevê, antes de gravar, o que o Rabi vai mostrar em cada serviço.

Uso:
  python3 .kit/ferramentas/conversao/simulador.py exemplos/cenario-convenio-a.json
  python3 .kit/ferramentas/conversao/simulador.py cenario.json --csv precos-convenio-a.csv
  opções: --servico ID (repetível) · --so-ativos · --invariantes · --json

Por serviço imprime as 4 linhas da coluna Valor (🔒 casa · 🔁 combinado ·
✅ próprio · Σ total), custo, Farol (% e cor) e a árvore de itens com
"conta" ou "fora" + motivo. Fonte das regras:
https://www.rabisistemas.com.br/manual/precos/guia-ia.html#algoritmo
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict

if __package__ in (None, ""):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    __package__ = "ferramentas.conversao"

from .modelo import cenario_from_dict  # noqa: E402
from . import motor  # noqa: E402


def brl(v) -> str:
    if v is None:
        return "vazio"
    s = f"{float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"


def pct(v) -> str:
    return "—" if v is None else f"{v:.0f}%"


ROTULO_TIPO = {"produto": "produto", "taxa": "taxa", "subservico": "subserviço", "equipamento": "equipamento"}


def _linhas_item(l: motor.Linha, nivel: int, out: list):
    ind = "   " * nivel
    if l.tipo == "equipamento":
        out.append(f"{ind}· equipamento {l.id} (sem valor)")
        return
    estado = "conta" if l.conta else f"FORA ({l.motivo})"
    if l.tipo == "subservico":
        det = f"base {brl(l.base)} · subtotal {brl(l.receita)}"
    else:
        det = f"{l.quantidade:g} × {brl(l.valor_unitario)} = {brl(l.valor_efetivo)}"
    custo = f" · custo {brl(l.custo)}" if l.tem_produto else ""
    farol = f" · {l.farol}" if l.farol else ""
    sinal = "+" if l.conta else "-"
    out.append(f"{ind}{sinal} {ROTULO_TIPO.get(l.tipo, l.tipo)} {l.nome} [{l.id}]: {det}{custo}{farol} → {estado}")
    for f in l.filhos:
        _linhas_item(f, nivel + 1, out)


def formatar_servico(r: motor.ResultadoServico, cat, conv) -> str:
    q = motor.quatro_linhas(cat, conv, r.servico_id)
    t = motor.textos_servico(cat.servicos[r.servico_id], conv)
    out = [f"== [{r.servico_id}] {r.nome}  (Utiliza: {'sim' if r.utiliza else 'NÃO'} · "
           f"pacote fechado: {'sim' if r.pacote_fechado else 'não'})"]
    out.append(f"  nome/código no convênio: {t['nome']} · {t['codigo'] or '—'} · tabela 87: {t['tabela87'] or '—'}"
               f" · tipo de atendimento: {t['tipo_atendimento'] or '—'}")
    out.append(f"  🔒 casa ........ {brl(q['casa'])} {q['casa_rotulo']}".rstrip())
    out.append(f"  🔁 combinado ... {brl(q['combinado'])}")
    out.append(f"  ✅ próprio ..... {brl(q['proprio'])}" + (f"  — {q['proprio_explicacao']}"
                                                             if q["proprio_explicacao"] else ""))
    out.append(f"  Σ  total ....... {brl(q['total'])}")
    out.append(f"  custo {brl(r.custo)} · Farol {pct(r.indice)} {r.farol or '(sem farol: sem produto)'}")
    if r.arvore.filhos:
        out.append("  itens:")
        for f in r.arvore.filhos:
            _linhas_item(f, 2, out)
    for a in r.avisos:
        out.append(f"  ! {a}")
    return "\n".join(out)


def carregar(cenario_path: str, csv_path: str = None, fontes_path: str = None):
    with open(cenario_path, encoding="utf-8") as f:
        cen = json.load(f)
    cat, conv = cenario_from_dict(cen)
    achados = []
    if csv_path:
        from .montar_convenio import ler_csv, aplicar_no_convenio
        fontes = json.load(open(fontes_path, encoding="utf-8")) if fontes_path else None
        linhas, achados = ler_csv(csv_path, fontes)
        conv = aplicar_no_convenio(linhas, conv)
    return cat, conv, achados


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Prevê 🔒/🔁/✅/Σ, custo e Farol por serviço")
    ap.add_argument("cenario", help="JSON {catalogo, convenio}")
    ap.add_argument("--csv", help="precos-<slug>.csv a sobrepor à configuração do cenário")
    ap.add_argument("--fontes", help="JSON {nome da fonte: id} (para fonte_preco numérica no CSV)")
    ap.add_argument("--servico", type=int, action="append", help="só estes serviços")
    ap.add_argument("--so-ativos", action="store_true", help="ignora serviços inativos no catálogo")
    ap.add_argument("--invariantes", action="store_true", help="lista também os achados I1–I13")
    ap.add_argument("--json", action="store_true", help="saída JSON")
    a = ap.parse_args(argv)
    cat, conv, achados_csv = carregar(a.cenario, a.csv, a.fontes)
    ids = a.servico or [s for s in sorted(cat.servicos) if not (a.so_ativos and not cat.servicos[s].ativo)]
    resultados = [motor.calcular_servico(cat, conv, sid) for sid in ids]
    achados = motor.validar_invariantes(cat, conv) if a.invariantes else []
    if a.json:
        print(json.dumps({"convenio": conv.nome, "servicos": [asdict(r) for r in resultados],
                          "achados": [asdict(x) for x in achados],
                          "achados_csv": [asdict(x) for x in achados_csv]}, ensure_ascii=False, indent=1))
        return 0
    print(f"Convênio: {conv.nome} (id {conv.id}) · régua do Farol: vermelho ≤ {conv.parametro_vermelho:g}% · "
          f"amarelo ≤ {conv.parametro_amarelo:g}%")
    print("PREVISÃO do motor do kit — confirme no Rabi depois de gravar (conferir_farol.py).\n")
    for r in resultados:
        print(formatar_servico(r, cat, conv))
        print()
    for x in achados_csv:
        print(f"CSV {x.nivel}: linha {x.linha} · {x.item} · {x.mensagem}")
    for x in achados:
        print(f"{x.codigo} {x.nivel}: {x.item} · {x.mensagem}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
