#!/usr/bin/env python3
"""Copia agents/, skills/ e commands/ do .claude/ do KIT para
modelo-repo-clinica/.claude/, reescrevendo caminhos do kit para `.kit/…`.

A fonte da verdade é o .claude/ do kit. Rode depois de alterar um agente,
skill ou comando:

    python3 ferramentas/kit/sincronizar_claude_modelo.py          # grava
    python3 ferramentas/kit/sincronizar_claude_modelo.py --checar # só confere (CI)

Só stdlib.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PASTAS = ("agents", "skills", "commands")

# Caminhos que pertencem ao KIT (no repo da clínica ficam sob .kit/).
# `sprints/` só é do kit quando é playbook (Sxx-nome.md ou Sxx-<nome>.md);
# `sprints/Sxx.md` é o status da clínica.
_PADRAO = re.compile(
    r"(?<![\w./-])"
    r"(conhecimento/|metodologia/|ferramentas/|prompts/|referencias/|"
    r"sprints/S(?:\d\d[a-z]?|xx)-|BOOTSTRAP\.md|INDICE\.md(?!\S*\w))"
)


def reescrever(texto: str) -> str:
    """Prefixa com `.kit/` os caminhos que apontam para o kit."""
    return _PADRAO.sub(lambda m: ".kit/" + m.group(1), texto)


def gerar(raiz: Path = RAIZ) -> dict[Path, str]:
    """Devolve {destino: conteúdo} para todos os arquivos a sincronizar."""
    origem = raiz / ".claude"
    destino = raiz / "modelo-repo-clinica" / ".claude"
    saida: dict[Path, str] = {}
    for pasta in PASTAS:
        for arq in sorted((origem / pasta).rglob("*.md")):
            rel = arq.relative_to(origem)
            saida[destino / rel] = reescrever(arq.read_text(encoding="utf-8"))
    return saida


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--checar", action="store_true", help="não grava; falha se o modelo estiver desatualizado")
    args = ap.parse_args(argv)
    arquivos = gerar()
    divergentes = []
    for destino, conteudo in arquivos.items():
        atual = destino.read_text(encoding="utf-8") if destino.exists() else None
        if atual != conteudo:
            divergentes.append(destino)
            if not args.checar:
                destino.parent.mkdir(parents=True, exist_ok=True)
                destino.write_text(conteudo, encoding="utf-8")
    if args.checar:
        if divergentes:
            print("FAIL: modelo-repo-clinica/.claude desatualizado em relação ao .claude do kit:")
            for d in divergentes:
                print("  -", d.relative_to(RAIZ))
            print("Rode: python3 ferramentas/kit/sincronizar_claude_modelo.py")
            return 1
        print(f"PASS: {len(arquivos)} arquivos de .claude sincronizados com o modelo")
        return 0
    print(f"Sincronizados {len(arquivos)} arquivos ({len(divergentes)} alterados).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
