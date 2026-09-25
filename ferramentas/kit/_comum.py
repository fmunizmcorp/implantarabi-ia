"""Utilidades comuns dos verificadores do kit (só stdlib)."""
from __future__ import annotations

from pathlib import Path

RAIZ_KIT = Path(__file__).resolve().parents[2]

# Pastas nunca varridas pelos verificadores.
IGNORAR_SEMPRE = {".git", "__pycache__", ".pytest_cache", "node_modules", ".venv", ".kit"}


def arquivos(raiz: Path, ignorar: set[str] = frozenset()):
    """Percorre `raiz` devolvendo arquivos, pulando pastas ignoradas."""
    pular = IGNORAR_SEMPRE | set(ignorar)
    pilha = [raiz]
    while pilha:
        atual = pilha.pop()
        try:
            itens = sorted(atual.iterdir())
        except OSError:
            continue
        for p in itens:
            if p.is_dir():
                if p.name not in pular:
                    pilha.append(p)
            elif p.is_file():
                yield p


def rel(p: Path, raiz: Path) -> str:
    try:
        return str(p.relative_to(raiz))
    except ValueError:
        return str(p)
