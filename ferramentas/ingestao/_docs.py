"""Utilidades comuns da ingestão de documentos do cliente (só stdlib)."""
from __future__ import annotations

import hashlib
import shutil
import subprocess
from pathlib import Path

PASTA_DOCS = "documentos-do-cliente"
PASTAS_IGNORADAS = {"texto-extraido", "fichas-de-extracao", "__pycache__", ".git"}
ARQUIVOS_IGNORADOS = {"00-INDICE.md", "inventario.md", "README.md", ".gitkeep", ".DS_Store"}

TIPOS = {
    ".pdf": "PDF", ".xlsx": "Excel", ".xlsm": "Excel", ".xls": "Excel (antigo)",
    ".csv": "CSV", ".tsv": "CSV", ".txt": "Texto", ".md": "Texto",
    ".docx": "Word", ".doc": "Word (antigo)", ".odt": "Documento ODF", ".ods": "Planilha ODF",
    ".png": "Imagem", ".jpg": "Imagem", ".jpeg": "Imagem", ".tif": "Imagem", ".tiff": "Imagem",
    ".xml": "XML", ".json": "JSON", ".zip": "ZIP", ".eml": "E-mail", ".msg": "E-mail",
}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def hash_curto(p: Path) -> str:
    return sha256(p)[:16]


def tipo(p: Path) -> str:
    return TIPOS.get(p.suffix.lower(), p.suffix.lower().lstrip(".").upper() or "?")


def documentos(repo: Path):
    """Arquivos originais em documentos-do-cliente/ (sem índices, fichas e texto extraído)."""
    base = repo / PASTA_DOCS
    if not base.is_dir():
        return []
    saida = []
    for p in sorted(base.rglob("*")):
        if not p.is_file():
            continue
        partes = set(p.relative_to(base).parts[:-1])
        if partes & PASTAS_IGNORADAS or p.name in ARQUIVOS_IGNORADOS:
            continue
        if p.name.startswith("_modelo"):
            continue
        saida.append(p)
    return saida


def tem(programa: str) -> bool:
    return shutil.which(programa) is not None


def rodar(cmd: list[str], timeout: int = 300) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout
    except (OSError, subprocess.SubprocessError) as e:
        return 1, str(e)


def paginas_pdf(p: Path):
    """Nº de páginas de um PDF, se pypdf ou pdfinfo existirem; senão None."""
    try:
        import pypdf  # type: ignore

        return len(pypdf.PdfReader(str(p)).pages)
    except Exception:
        pass
    if tem("pdfinfo"):
        cod, saida = rodar(["pdfinfo", str(p)], timeout=60)
        if cod == 0:
            for linha in saida.splitlines():
                if linha.lower().startswith("pages:"):
                    try:
                        return int(linha.split(":", 1)[1])
                    except ValueError:
                        return None
    return None
