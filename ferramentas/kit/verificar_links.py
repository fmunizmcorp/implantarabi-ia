#!/usr/bin/env python3
"""Verifica se os links relativos dos .md apontam para arquivos/pastas existentes.

- Ignora http(s)://, mailto:, âncoras puras (#…), links com placeholder (<…>, {…}).
- Ignora links para `.kit/` (usados no modelo-repo-clinica: o kit só existe no repo da clínica).
- Ignora o que está dentro de blocos de código (``` … ```) e de `código inline`.

Saída: PASS/FAIL + lista (arquivo:linha → alvo). Código 0/1.
Uso: python3 ferramentas/kit/verificar_links.py [--raiz DIR]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comum import RAIZ_KIT, arquivos, rel  # noqa: E402

LINK = re.compile(r"!?\[[^\]]*\]\(\s*([^)\s]+)(?:\s+\"[^\"]*\")?\s*\)")
CODIGO_INLINE = re.compile(r"`[^`]*`")


def alvos(texto: str):
    """Gera (nº da linha, alvo) dos links fora de código."""
    em_bloco = False
    for n, linha in enumerate(texto.splitlines(), 1):
        if linha.lstrip().startswith(("```", "~~~")):
            em_bloco = not em_bloco
            continue
        if em_bloco:
            continue
        for m in LINK.finditer(CODIGO_INLINE.sub("", linha)):
            yield n, m.group(1)


def ignorar(alvo: str) -> bool:
    a = alvo.strip("<>")
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", a):  # http:, https:, mailto:, etc.
        return True
    if a.startswith("#") or not a:
        return True
    if any(c in alvo for c in "<>{}"):
        return True
    if ".kit/" in a or a == ".kit":
        return True
    return False


def verificar(raiz: Path) -> list[str]:
    problemas = []
    for p in arquivos(raiz):
        if p.suffix != ".md":
            continue
        texto = p.read_text(encoding="utf-8", errors="replace")
        for n, alvo in alvos(texto):
            if ignorar(alvo):
                continue
            caminho = unquote(alvo.split("#", 1)[0].split("?", 1)[0])
            if not caminho:
                continue
            destino = (raiz / caminho.lstrip("/")) if caminho.startswith("/") else (p.parent / caminho)
            if not destino.exists():
                problemas.append(f"{rel(p, raiz)}:{n} → {alvo}")
    return problemas


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Links relativos dos .md")
    ap.add_argument("--raiz", default=str(RAIZ_KIT))
    args = ap.parse_args(argv)
    raiz = Path(args.raiz).resolve()
    problemas = verificar(raiz)
    if problemas:
        print(f"FAIL: {len(problemas)} link(s) quebrado(s) em {raiz}")
        for linha in problemas:
            print("  -", linha)
        return 1
    print(f"PASS: links relativos ok em {raiz}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
