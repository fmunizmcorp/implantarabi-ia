#!/usr/bin/env python3
"""Verifica o contrato de tamanho e de índices do kit (metodologia/politicas.md §1).

- Nenhum .md passa de 40 KB.
- Nenhum outro arquivo passa de 5 MB (a spec OpenAPI em
  conhecimento/api-externa/spec/*.json também tem teto de 5 MB).
- Toda pasta com arquivos .md ou de dados tem 00-INDICE.md ou README.md
  (INDICE.md também vale). Ignora .git, .claude, __pycache__, tests, exemplos.

Saída: PASS/FAIL + lista. Código de saída 0 (pass) ou 1 (fail).
Uso: python3 ferramentas/kit/verificar_tamanhos.py [--raiz DIR]
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comum import RAIZ_KIT, arquivos, rel  # noqa: E402

LIMITE_MD = 40 * 1024
LIMITE_OUTROS = 5 * 1024 * 1024
EXT_DADOS = {".csv", ".tsv", ".json", ".jsonl", ".xlsx", ".xls", ".xml", ".txt", ".pdf", ".zip", ".gz"}
INDICES = {"00-INDICE.md", "README.md", "INDICE.md"}
IGNORAR_INDICE = {".claude", "tests", "exemplos", ".github"}


def verificar(raiz: Path) -> list[str]:
    problemas: list[str] = []
    por_pasta: dict[Path, list[Path]] = defaultdict(list)
    for p in arquivos(raiz):
        tam = p.stat().st_size
        if p.suffix == ".md" and tam > LIMITE_MD:
            problemas.append(f"MD GRANDE   {rel(p, raiz)} ({tam/1024:.1f} KB > 40 KB)")
        elif p.suffix != ".md" and tam > LIMITE_OUTROS:
            problemas.append(f"ARQ GRANDE  {rel(p, raiz)} ({tam/1048576:.2f} MB > 5 MB)")
        por_pasta[p.parent].append(p)
    for pasta, lista in sorted(por_pasta.items()):
        partes = pasta.relative_to(raiz).parts if pasta != raiz else ()
        if any(x in IGNORAR_INDICE for x in partes):
            continue
        conteudo = [p for p in lista if p.suffix == ".md" or p.suffix in EXT_DADOS]
        if not conteudo:
            continue
        if not any(p.name in INDICES for p in lista):
            problemas.append(f"SEM ÍNDICE  {rel(pasta, raiz) or '.'}/ (falta 00-INDICE.md ou README.md)")
    return problemas


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Tamanhos e índices do kit")
    ap.add_argument("--raiz", default=str(RAIZ_KIT))
    args = ap.parse_args(argv)
    raiz = Path(args.raiz).resolve()
    problemas = verificar(raiz)
    if problemas:
        print(f"FAIL: {len(problemas)} problema(s) de tamanho/índice em {raiz}")
        for linha in problemas:
            print("  -", linha)
        return 1
    print(f"PASS: tamanhos e índices ok em {raiz}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
