"""Funções comuns das ferramentas de referências (normalizar, buscar, enriquecer).

Fonte: decisão do proprietário do kit (referencias/LICENCAS.md) · Conferido em 2026-09-25
Vale para: kit v0.1.0 · Só biblioteca padrão do Python.

Formato dos dados normalizados (contrato):
  * CSV UTF-8, separador ';', cabeçalho na 1ª linha, aspas só quando o campo
    contém ';' ou aspas (csv.QUOTE_MINIMAL);
  * números com ponto decimal (ex.: 30.96), vazio = sem informação;
  * cada conjunto fica numa pasta (ex.: referencias/brasindice/medicamentos/)
    fatiado por letra inicial do nome normalizado (A.csv, B.csv…, 0-9.csv,
    _.csv); se uma letra passar de 4 MB, vira duas letras (SE.csv, SO.csv…)
    e, se ainda passar, partes numeradas (SE-001.csv…);
  * o mapa de fatias de todos os conjuntos fica em referencias/manifest.json.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import unicodedata
from datetime import date
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Sequence

KIT_VERSAO = "0.1.0"
LIMITE_FATIA = 4_000_000  # bytes (política: dados ≤ 5 MB; margem de segurança)
RAIZ_KIT = Path(__file__).resolve().parents[2]
REFERENCIAS_PADRAO = RAIZ_KIT / "referencias"

# Colunas padronizadas dos conjuntos de PRODUTOS (medicamentos e materiais),
# iguais para Brasíndice, SIMPRO e CMED. Documentadas em referencias/00-INDICE.md.
COLUNAS_PRODUTO = [
    "fonte",              # BRASINDICE | SIMPRO | CMED
    "edicao",             # edição/competência da publicação usada
    "tipo_item",          # medicamento | material | saneante | reagente
    "codigo_fonte",       # código do item na própria tabela (vai na guia com tabela_fonte)
    "tabela_fonte",       # código TISS (Tabela 87) da própria fonte: 05 Brasíndice, 12 SIMPRO, vazio CMED
    "chave_fonte",        # chave interna da publicação (ex.: lab-produto-apresentação)
    "laboratorio",        # laboratório / fabricante
    "produto",            # nome comercial / descrição curta
    "apresentacao",       # apresentação (forma, dose, embalagem)
    "principio_ativo",    # substância (CMED; Brasíndice enriquecido via EAN na CMED)
    "ean",                # código de barras
    "registro_anvisa",    # registro ANVISA (13 dígitos para medicamento)
    "codigo_tuss",        # código TUSS (terminologia 19 materiais / 20 medicamentos / 18 taxas)
    "ggrem",              # código GGREM (CMED)
    "generico",           # S | N | vazio
    "restrito_hospitalar",  # S | N | vazio
    "qtd_embalagem",      # quantidade de unidades na embalagem (quando a fonte informa)
    "pf_total",           # preço fábrica da embalagem
    "pmc_total",          # preço máximo ao consumidor da embalagem
    "pf_unit",            # PF por unidade (Brasíndice já publica)
    "pmc_unit",           # PMC por unidade
    "preco_ref",          # preço único da fonte quando não há PF/PMC (SIMPRO)
    "tipo_preco",         # explica a base do preço (ex.: "PF/PMC ICMS 17%")
    "vigencia",           # data ou edição da última alteração de preço
    "tabela87_sugerida",  # 20 medicamento | 19 material (TUSS)
    "precos_extra",       # CMED: outras alíquotas de ICMS, formato PF18=..|PMC18=..
]

_TRADUZ = str.maketrans(
    "ÁÀÂÃÄÅÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇÑÝáàâãäåéèêëíìîïóòôõöúùûüçñýÿºª",
    "AAAAAAEEEEIIIIOOOOOUUUUCNYaaaaaaeeeeiiiiooooouuuucnyyoa",
)


def normalizar_texto(texto: Optional[str]) -> str:
    """Maiúsculas, sem acento, espaços simples. Rápido (tabela de tradução)."""
    if not texto:
        return ""
    t = str(texto).translate(_TRADUZ)
    if not t.isascii():
        t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode("ascii")
    return " ".join(t.upper().split())


def so_digitos(texto: Optional[str]) -> str:
    return re.sub(r"\D", "", texto or "")


def numero(texto) -> str:
    """'1.234,56' | '1234.56' | 1234.56 -> '1234.56'; vazio/traço -> ''."""
    if texto is None:
        return ""
    if isinstance(texto, (int, float)):
        return f"{float(texto):.4f}".rstrip("0").rstrip(".")
    t = str(texto).strip().replace("R$", "").strip()
    if not t or t in {"-", "--"} or not re.search(r"\d", t):
        return ""
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
    try:
        return f"{float(t):.4f}".rstrip("0").rstrip(".")
    except ValueError:
        return ""


def prefixo_letra(nome_normalizado: str, tamanho: int = 1) -> str:
    """Prefixo de fatia: letras A-Z; dígitos -> '0-9'; outro -> '_'."""
    n = nome_normalizado.strip()
    if not n:
        return "_"
    c = n[0]
    if c.isdigit():
        return "0-9"
    if not ("A" <= c <= "Z"):
        return "_"
    if tamanho == 1:
        return c
    resto = "".join(ch if "A" <= ch <= "Z" else "_" for ch in n[1:tamanho])
    return (c + resto).ljust(tamanho, "_")


def sha256_arquivo(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def _csv_bytes(colunas: Sequence[str], linhas: Iterable[Sequence[str]]) -> bytes:
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=";", lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    w.writerow(colunas)
    for l in linhas:
        w.writerow(["" if v is None else str(v).replace("\n", " ").replace("\r", " ") for v in l])
    return buf.getvalue().encode("utf-8")


def _tamanho_linhas(linhas: List[Sequence[str]]) -> int:
    return sum(len(";".join("" if v is None else str(v) for v in l).encode("utf-8")) + 1 for l in linhas)


def gravar_fatiado(
    pasta: Path,
    colunas: Sequence[str],
    linhas: List[Sequence[str]],
    chave_nome: Callable[[Sequence[str]], str],
    limite: int = LIMITE_FATIA,
    fatiar_por_letra: bool = True,
) -> List[Dict]:
    """Grava linhas em fatias ≤ limite. Devolve a lista de fatias para o manifest.

    ``chave_nome(linha)`` devolve o texto normalizado usado para a letra.
    Com ``fatiar_por_letra=False`` grava ``dados.csv`` (ou partes numeradas).
    """
    pasta.mkdir(parents=True, exist_ok=True)
    for antigo in pasta.glob("*.csv"):
        antigo.unlink()
    linhas = sorted(linhas, key=lambda l: (chave_nome(l), [str(x) for x in l]))
    grupos: Dict[str, List] = {}
    if fatiar_por_letra:
        for l in linhas:
            grupos.setdefault(prefixo_letra(chave_nome(l), 1), []).append(l)
        # letras grandes demais viram duas letras
        for pref in list(grupos):
            if _tamanho_linhas(grupos[pref]) > limite and pref not in ("0-9", "_"):
                sub: Dict[str, List] = {}
                for l in grupos.pop(pref):
                    sub.setdefault(prefixo_letra(chave_nome(l), 2), []).append(l)
                grupos.update(sub)
    else:
        grupos["dados"] = linhas
    fatias = []
    for pref in sorted(grupos):
        partes = _partir(grupos[pref], limite)
        for i, parte in enumerate(partes, 1):
            nome = f"{pref}.csv" if len(partes) == 1 else f"{pref}-{i:03d}.csv"
            destino = pasta / nome
            destino.write_bytes(_csv_bytes(colunas, parte))
            fatias.append({
                "prefixo": "" if pref == "dados" else pref,
                "arquivo": nome,
                "linhas": len(parte),
                "bytes": destino.stat().st_size,
                "sha256": sha256_arquivo(destino),
            })
    return fatias


def _partir(linhas: List, limite: int) -> List[List]:
    partes, atual, tam = [], [], 0
    for l in linhas:
        t = len(";".join("" if v is None else str(v) for v in l).encode("utf-8")) + 1
        if atual and tam + t > limite - 100_000:
            partes.append(atual)
            atual, tam = [], 0
        atual.append(l)
        tam += t
    if atual or not partes:
        partes.append(atual)
    return partes


# ---------------------------------------------------------------- manifest

def carregar_manifest(raiz: Path) -> Dict:
    arq = Path(raiz) / "manifest.json"
    if arq.exists():
        return json.loads(arq.read_text(encoding="utf-8"))
    return {"kit": KIT_VERSAO, "descricao": "Mapa das tabelas de referência normalizadas", "conjuntos": {}}


def salvar_manifest(raiz: Path, manifest: Dict) -> None:
    manifest["kit"] = KIT_VERSAO
    manifest["atualizado_em"] = date.today().isoformat()
    manifest["conjuntos"] = dict(sorted(manifest.get("conjuntos", {}).items()))
    (Path(raiz) / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def ler_fatia(caminho: Path) -> Iterable[Dict[str, str]]:
    with open(caminho, encoding="utf-8", newline="") as f:
        yield from csv.DictReader(f, delimiter=";")


def ler_csv_generico(caminho: Path) -> List[Dict[str, str]]:
    """Lê CSV da clínica detectando separador (; , tab) e encoding (utf-8/latin-1)."""
    dados = Path(caminho).read_bytes()
    try:
        texto = dados.decode("utf-8-sig")
    except UnicodeDecodeError:
        texto = dados.decode("latin-1")
    amostra = texto[:4096]
    sep = max([";", ",", "\t", "|"], key=amostra.count)
    return list(csv.DictReader(io.StringIO(texto), delimiter=sep))


# ---------------------------------------------------------------- doses

RE_DOSE = re.compile(r"(\d+[.,]?\d*)\s*(MCG|MG|ML|G|UI|%)(?![A-Z])"
                     r"(?:\s*/\s*(?:\d+[.,]?\d*\s*)?(ML|G|L|DOSE|GOTA|GT|H)(?![A-Z]))?")
_FATOR = {"MCG": ("MG", 0.001), "MG": ("MG", 1.0), "G": ("MG", 1000.0),
          "ML": ("ML", 1.0), "UI": ("UI", 1.0), "%": ("%", 1.0)}


def extrair_doses(texto_normalizado: str) -> set:
    """Conjunto de (unidade_base, valor) — G e MCG convertidos para MG.

    Concentração ("500 MG/ML", "10 MG/G") vira unidade própria ("MG/ML"), para
    não confundir comprimido de 500 mg com solução de 500 mg/ml.
    """
    doses = set()
    for num, un, por in RE_DOSE.findall(texto_normalizado):
        try:
            v = float(num.replace(",", "."))
        except ValueError:
            continue
        base, f = _FATOR[un]
        if por:
            base = f"{base}/{por}"
        doses.add((base, round(v * f, 6)))
    return doses


def remover_doses(texto_normalizado: str) -> str:
    return RE_DOSE.sub(" ", texto_normalizado)
