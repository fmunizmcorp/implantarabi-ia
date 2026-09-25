#!/usr/bin/env python3
"""Inventaria os documentos do cliente: acrescenta ao inventario.md uma linha por
documento novo (hash sha256), sem duplicar.

Uso (na raiz do repo da clínica):
    python3 .kit/ferramentas/ingestao/inventario.py [--repo .] [--simular]

Colunas: nº | arquivo | tipo | páginas | hash | recebido em | o que contém |
dados extraídos → sprint | status lote. A sessão completa "o que contém" e
"dados extraídos → sprint" depois de ler o documento.
Páginas de PDF: usa pypdf ou pdfinfo se existirem (opcional).
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _docs import PASTA_DOCS, documentos, hash_curto, paginas_pdf, tipo  # noqa: E402

CABECALHO = [
    "# Inventário de documentos recebidos",
    "",
    "| nº | arquivo | tipo | páginas | hash | recebido em | o que contém | dados extraídos → sprint | status lote |",
    "|---|---|---|---|---|---|---|---|---|",
]
DATA_PASTA = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def ler_existentes(inv: Path) -> tuple[set[str], int]:
    """Hashes já inventariados e o maior nº usado."""
    hashes, maior = set(), 0
    if not inv.exists():
        return hashes, maior
    for linha in inv.read_text(encoding="utf-8").splitlines():
        cel = [c.strip() for c in linha.strip().strip("|").split("|")]
        if len(cel) >= 5 and cel[0].isdigit():
            maior = max(maior, int(cel[0]))
            hashes.add(cel[4].strip("`"))
    return hashes, maior


def recebido_em(p: Path) -> str:
    for parte in reversed(p.parts[:-1]):
        if DATA_PASTA.match(parte):
            return parte
    return dt.date.fromtimestamp(p.stat().st_mtime).isoformat()


def paginas(p: Path) -> str:
    if p.suffix.lower() == ".pdf":
        n = paginas_pdf(p)
        return str(n) if n is not None else "?"
    if p.suffix.lower() in {".xlsx", ".xlsm"}:
        try:
            import openpyxl  # type: ignore

            wb = openpyxl.load_workbook(p, read_only=True)
            n = len(wb.sheetnames)
            wb.close()
            return f"{n} aba(s)"
        except Exception:
            return "?"
    return "—"


def celula(t: str) -> str:
    return t.replace("|", "\\|").replace("\n", " ")


def inventariar(repo: Path, simular: bool = False) -> list[str]:
    base = repo / PASTA_DOCS
    inv = base / "inventario.md"
    hashes, n = ler_existentes(inv)
    novas = []
    for p in documentos(repo):
        h = hash_curto(p)
        if h in hashes:
            continue
        hashes.add(h)
        n += 1
        rel = p.relative_to(base).as_posix()
        novas.append(
            f"| {n} | {celula(rel)} | {tipo(p)} | {paginas(p)} | `{h}` | {recebido_em(p)} "
            f"| (a preencher) | (a preencher) | recebido |"
        )
    if novas and not simular:
        base.mkdir(parents=True, exist_ok=True)
        texto = inv.read_text(encoding="utf-8") if inv.exists() else "\n".join(CABECALHO) + "\n"
        if "| nº |" not in texto:
            texto = texto.rstrip("\n") + "\n\n" + "\n".join(CABECALHO[2:]) + "\n"
        inv.write_text(texto.rstrip("\n") + "\n" + "\n".join(novas) + "\n", encoding="utf-8")
    return novas


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Inventário de documentos do cliente")
    ap.add_argument("--repo", default=".", help="raiz do repo da clínica")
    ap.add_argument("--simular", action="store_true", help="mostra sem gravar")
    args = ap.parse_args(argv)
    repo = Path(args.repo).resolve()
    if not (repo / PASTA_DOCS).is_dir():
        print(f"ERRO: {repo / PASTA_DOCS} não existe.", file=sys.stderr)
        return 2
    novas = inventariar(repo, args.simular)
    acao = "seriam acrescentados" if args.simular else "acrescentados"
    print(f"{len(novas)} documento(s) novo(s) {acao} ao inventário.")
    for linha in novas:
        print("  " + linha)
    return 0


if __name__ == "__main__":
    sys.exit(main())
