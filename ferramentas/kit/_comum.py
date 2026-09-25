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


# ---------------------------------------------------------------------------
# Placeholders do modelo do repo da clínica (usados por novo_repo_clinica.py,
# personalizar_clinica.py e exportar_modelo.py).
# ---------------------------------------------------------------------------
import datetime as _dt
import re as _re
import unicodedata as _ud

MODELO = RAIZ_KIT / "modelo-repo-clinica"

PORTES = {
    "consultorio": "Consultório individual",
    "pequena-media": "Clínica pequena/média",
    "rede": "Rede / policlínica",
}

# Marcadores que o modelo carrega até a clínica ser personalizada.
PH_NOME = "<NOME_DA_CLINICA>"
PH_SLUG = "<SLUG_DA_CLINICA>"
PH_PORTE = "<PORTE>"
PH_VERSAO = "<VERSAO_DO_KIT>"
PH_DATA = "<DATA_CRIACAO>"
PLACEHOLDERS = (PH_NOME, PH_SLUG, PH_PORTE, PH_VERSAO, PH_DATA)

TEXTO = {".md", ".sh", ".json", ".csv", ".txt", ".gitignore", ".yml", ".yaml"}


def slugificar(nome: str) -> str:
    s = _ud.normalize("NFKD", nome).encode("ascii", "ignore").decode()
    s = _re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "clinica"


def hoje() -> str:
    """Data de hoje em America/Sao_Paulo (AAAA-MM-DD)."""
    try:
        from zoneinfo import ZoneInfo

        return _dt.datetime.now(ZoneInfo("America/Sao_Paulo")).date().isoformat()
    except Exception:  # pragma: no cover - sem tzdata
        return _dt.date.today().isoformat()


def ler_versao(raiz: Path = RAIZ_KIT) -> str:
    try:
        return (raiz / "VERSION").read_text(encoding="utf-8").strip() or "?"
    except OSError:
        return "?"


def eh_texto(p: Path) -> bool:
    return p.suffix in TEXTO or p.name in TEXTO


def substituir(texto: str, valores: dict[str, str]) -> str:
    for chave, valor in valores.items():
        texto = texto.replace(chave, valor)
    return texto


def valores_clinica(nome: str, porte: str, versao: str, data: str, slug: str | None = None) -> dict[str, str]:
    """Mapa placeholder → valor para uma clínica. `porte` é a chave de PORTES."""
    return {
        PH_NOME: nome,
        PH_SLUG: slug or f"rabi-implantacao-{slugificar(nome)}",
        PH_PORTE: PORTES[porte],
        PH_VERSAO: versao,
        PH_DATA: data,
    }
