#!/usr/bin/env python3
"""Extrai o texto dos documentos do cliente para leitura pela IA, em fatias ≤ 1 MB.

Uso (na raiz do repo da clínica):
    python3 .kit/ferramentas/ingestao/extrair_texto.py [--repo .] [arquivo ...] [--forcar] [--sem-ocr]

Saída: documentos-do-cliente/texto-extraido/<hash>.txt (ou <hash>-parte-001.txt, …)
e um 00-INDICE.md da pasta. Cada fatia começa com um cabeçalho de origem.

Métodos (o que estiver disponível; nada é obrigatório):
- PDF com texto: `pdftotext -layout` (poppler). Sem texto e com `pdftoppm` +
  `tesseract`: OCR em português a 300 dpi (`tesseract -l por`).
- Imagem: `tesseract -l por`.
- Excel (.xlsx/.xlsm): openpyxl, se instalado (uma seção por aba, células separadas por `;`).
- Word (.docx): leitura direta do XML (stdlib).
- CSV/TXT/MD/TSV/XML/JSON: leitura direta (UTF-8; se falhar, Latin-1).
Se faltar a ferramenta, avisa e segue para o próximo arquivo.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _docs import PASTA_DOCS, documentos, hash_curto, rodar, tem  # noqa: E402

LIMITE = 1024 * 1024  # 1 MB por fatia
MIN_CHARS_PAGINA = 40  # abaixo disso o PDF é tratado como digitalizado (tenta OCR)
TEXTO_DIRETO = {".csv", ".tsv", ".txt", ".md", ".xml", ".json"}
IMAGENS = {".png", ".jpg", ".jpeg", ".tif", ".tiff"}


class SemFerramenta(Exception):
    pass


def ler_texto(p: Path) -> str:
    dados = p.read_bytes()
    try:
        return dados.decode("utf-8-sig")
    except UnicodeDecodeError:
        return dados.decode("latin-1")


def ocr_imagem(p: Path) -> str:
    if not tem("tesseract"):
        raise SemFerramenta("tesseract não instalado (OCR indisponível)")
    cod, saida = rodar(["tesseract", str(p), "stdout", "-l", "por"], timeout=600)
    if cod != 0:
        raise SemFerramenta(f"tesseract falhou em {p.name}")
    return saida


def pdf(p: Path, usar_ocr: bool) -> tuple[str, str]:
    texto = ""
    if tem("pdftotext"):
        cod, texto = rodar(["pdftotext", "-layout", str(p), "-"], timeout=600)
        if cod != 0:
            texto = ""
    paginas = max(texto.count("\f"), 1)
    if len(texto.strip()) >= MIN_CHARS_PAGINA * paginas:
        return texto, "pdftotext"
    if usar_ocr and tem("pdftoppm") and tem("tesseract"):
        with tempfile.TemporaryDirectory() as tmp:
            cod, _ = rodar(["pdftoppm", "-r", "300", "-png", str(p), f"{tmp}/p"], timeout=1800)
            if cod != 0:
                raise SemFerramenta("pdftoppm falhou")
            partes = []
            for i, img in enumerate(sorted(Path(tmp).glob("p*.png")), 1):
                partes.append(f"\n===== página {i} (OCR) =====\n" + ocr_imagem(img))
            return "".join(partes), "ocr tesseract por 300dpi"
    if texto.strip():
        return texto, "pdftotext (pouco texto; OCR indisponível)"
    if not tem("pdftotext"):
        raise SemFerramenta("pdftotext (poppler-utils) não instalado")
    raise SemFerramenta("PDF sem texto e OCR indisponível (instale tesseract-ocr-por e poppler-utils)")


def excel(p: Path) -> str:
    try:
        import openpyxl  # type: ignore
    except ImportError as e:
        raise SemFerramenta("openpyxl não instalado (pip install openpyxl)") from e
    wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
    partes = []
    for aba in wb.worksheets:
        partes.append(f"\n===== aba: {aba.title} =====")
        for n, linha in enumerate(aba.iter_rows(values_only=True), 1):
            valores = ["" if v is None else str(v) for v in linha]
            if any(valores):
                partes.append(f"L{n}: " + ";".join(valores).rstrip(";"))
    wb.close()
    return "\n".join(partes)


def docx(p: Path) -> str:
    with zipfile.ZipFile(p) as z:
        xml = z.read("word/document.xml").decode("utf-8", errors="replace")
    xml = re.sub(r"</w:p>", "\n", xml)
    xml = re.sub(r"<w:tab/>", "\t", xml)
    return re.sub(r"<[^>]+>", "", xml)


def extrair(p: Path, usar_ocr: bool = True) -> tuple[str, str]:
    ext = p.suffix.lower()
    if ext == ".pdf":
        return pdf(p, usar_ocr)
    if ext in {".xlsx", ".xlsm"}:
        return excel(p), "openpyxl"
    if ext == ".docx":
        return docx(p), "docx (xml)"
    if ext in TEXTO_DIRETO:
        return ler_texto(p), "leitura direta"
    if ext in IMAGENS:
        if not usar_ocr:
            raise SemFerramenta("OCR desligado (--sem-ocr)")
        return ocr_imagem(p), "ocr tesseract por"
    raise SemFerramenta(f"tipo {ext or '(sem extensão)'} não suportado; converta para PDF/XLSX/CSV")


def fatiar(texto: str, limite: int = LIMITE) -> list[str]:
    """Quebra em fatias de até `limite` bytes UTF-8, preferindo quebra de linha."""
    fatias, atual, tam = [], [], 0
    for linha in texto.splitlines(keepends=True):
        b = len(linha.encode("utf-8"))
        while b > limite:  # linha gigante: corta em pedaços
            corte = linha[: max(1, limite // 4)]
            if atual:
                fatias.append("".join(atual)); atual, tam = [], 0
            fatias.append(corte)
            linha = linha[len(corte):]
            b = len(linha.encode("utf-8"))
        if tam + b > limite and atual:
            fatias.append("".join(atual)); atual, tam = [], 0
        atual.append(linha); tam += b
    if atual or not fatias:
        fatias.append("".join(atual))
    return fatias


def gravar(saida: Path, origem_rel: str, h: str, texto: str, metodo: str, limite: int = LIMITE) -> list[Path]:
    saida.mkdir(parents=True, exist_ok=True)
    data = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    reservado = 400  # espaço do cabeçalho
    fatias = fatiar(texto, limite - reservado)
    arquivos = []
    for i, f in enumerate(fatias, 1):
        nome = f"{h}.txt" if len(fatias) == 1 else f"{h}-parte-{i:03d}.txt"
        cab = f"# origem: {origem_rel} · hash: {h} · parte {i}/{len(fatias)} · método: {metodo} · extraído em: {data}\n\n"
        (saida / nome).write_text(cab + f, encoding="utf-8")
        arquivos.append(saida / nome)
    return arquivos


def atualizar_indice(saida: Path) -> None:
    linhas = [
        "# texto-extraido",
        "",
        "> Texto extraído dos documentos do cliente (gerado por `extrair_texto.py`).",
        "> Fatias ≤ 1 MB. Leia pela linha do documento; o original está em `documentos-do-cliente/`.",
        "",
        "| Arquivo | Origem | Parte | Método |",
        "|---|---|---|---|",
    ]
    for p in sorted(saida.glob("*.txt")):
        cab = p.open(encoding="utf-8").readline()
        m = re.match(r"# origem: (.*?) · hash: .*? · parte (\S+) · método: (.*?) · extraído", cab)
        origem, parte, metodo = (m.group(1), m.group(2), m.group(3)) if m else ("?", "?", "?")
        linhas.append(f"| {p.name} | {origem.replace('|', '/')} | {parte} | {metodo} |")
    (saida / "00-INDICE.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Extrai texto dos documentos do cliente")
    ap.add_argument("arquivos", nargs="*", help="arquivos específicos (padrão: todos de documentos-do-cliente/)")
    ap.add_argument("--repo", default=".", help="raiz do repo da clínica")
    ap.add_argument("--forcar", action="store_true", help="refaz mesmo se já extraído")
    ap.add_argument("--sem-ocr", action="store_true", help="não tenta OCR")
    args = ap.parse_args(argv)
    repo = Path(args.repo).resolve()
    base = repo / PASTA_DOCS
    saida = base / "texto-extraido"
    alvos = [Path(a).resolve() for a in args.arquivos] if args.arquivos else documentos(repo)
    if not alvos:
        print("Nenhum documento encontrado.")
        return 0
    ok, avisos = 0, 0
    for p in alvos:
        h = hash_curto(p)
        if not args.forcar and (list(saida.glob(f"{h}.txt")) or list(saida.glob(f"{h}-parte-*.txt"))):
            print(f"= {p.name}: já extraído ({h})")
            continue
        try:
            texto, metodo = extrair(p, usar_ocr=not args.sem_ocr)
        except SemFerramenta as e:
            print(f"! {p.name}: AVISO — {e}")
            avisos += 1
            continue
        try:
            origem_rel = p.relative_to(base).as_posix()
        except ValueError:
            origem_rel = p.name
        feitos = gravar(saida, origem_rel, h, texto, metodo)
        ok += 1
        print(f"+ {p.name}: {len(feitos)} fatia(s) · {metodo} · {len(texto)} caracteres")
    if saida.is_dir():
        atualizar_indice(saida)
    print(f"Concluído: {ok} extraído(s), {avisos} aviso(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
