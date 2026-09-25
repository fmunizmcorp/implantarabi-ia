"""Diz qual é a PRÓXIMA pergunta/ação da sprint — uma por vez.

Uso: python3 .kit/ferramentas/implantacao/fila_perguntas.py --repo . [--sprint S03] [--todas]

Regra (metodologia/conversa-com-o-usuario.md):
- item 'coletado'   → CONFIRMAR com o usuário (mostrar o dado e a origem)
- item 'pendente'   → PEDIR (ou SUGERIR PADRÃO se a observação trouxer "padrão: ...")
- item 'confirmado' → GRAVAR (ritual de 5 passos, com prévia e aprovação)
- item 'gravado'    → CONFERIR (foto depois + diff)
- 'bloqueado'       → lembrar o bloqueio na daily; não insistir
Sem --sprint, usa a primeira sprint não concluída na ordem S00..S17.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from checklist import ler_sprints  # type: ignore
else:
    from .checklist import ler_sprints

ACAO = {"coletado": "CONFIRMAR", "pendente": "PEDIR", "confirmado": "GRAVAR", "gravado": "CONFERIR"}
ORDEM = ("gravado", "confirmado", "coletado", "pendente")  # fecha o que está adiantado antes de abrir novo


def proximas(repo: Path, sprint: str | None = None, todas: bool = False):
    sprints = ler_sprints(repo)
    if sprint:
        alvo = [s for s in sprints if s.codigo.lower().startswith(sprint.lower())]
    else:
        alvo = [next((s for s in sprints if s.situacao not in ("concluída", "sem itens")), None)]
        alvo = [s for s in alvo if s]
    saida = []
    for s in alvo:
        for st in ORDEM:
            for i in s.itens:
                if i.status == st:
                    m = re.search(r"padr[aã]o:\s*([^;|]+)", i.observacao, re.I)
                    acao = "SUGERIR PADRÃO" if st == "pendente" and m else ACAO[st]
                    saida.append((s.codigo, acao, i, m.group(1).strip() if m else ""))
    return saida if todas else saida[:1]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--sprint")
    ap.add_argument("--todas", action="store_true")
    a = ap.parse_args(argv)
    fila = proximas(Path(a.repo), a.sprint, a.todas)
    if not fila:
        print("Nada pendente nesta sprint. Próximo: review da sprint e abrir a seguinte.")
        return 0
    for cod, acao, item, padrao in fila:
        extra = f" (padrão sugerido: {padrao})" if padrao else ""
        origem = f" [origem: {item.origem}]" if item.origem else ""
        print(f"{cod} · {acao} · #{item.numero} {item.item}{extra}{origem}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
