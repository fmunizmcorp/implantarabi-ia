#!/usr/bin/env python3
"""Busca no FAQ das IAs (`conhecimento/faq-ias/`) pelo sintoma de um erro do Rabi.

    python3 .kit/ferramentas/kit/buscar_faq.py "Cannot read properties of undefined (reading 'filter')"
    python3 .kit/ferramentas/kit/buscar_faq.py "Erro ao processar a operação" --status 400 --rota "GET /servicos/1"

Cada entrada `Fxxx-*.md` declara no cabeçalho `Rotas`, `Status HTTP` e `Mensagem contém`
(alternativas separadas por `|`). A busca pontua: trecho da mensagem (peso maior), status e
rota (método + prefixo). Imprime as entradas com pontuação > 0, da melhor para a pior.

Também usada por `ferramentas/rabi_api/cliente.py` (`sugerir`) para pôr "possível FAQ: Fxxx"
na mensagem de erro. Só stdlib. Código 0 achou · 1 nada encontrado.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

PASTA = Path(__file__).resolve().parents[2] / "conhecimento" / "faq-ias"


def _norm(s: str) -> str:
    return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()


def _campo(texto: str, rotulo: str) -> list[str]:
    m = re.search(rf"^- \*\*{rotulo}:\*\*\s*(.+)$", texto, re.M)
    if not m:
        return []
    return [p.strip() for p in m.group(1).split("|") if p.strip() and p.strip() != "—"]


def carregar(pasta: Path = PASTA) -> list[dict]:
    entradas = []
    for arq in sorted(pasta.glob("F[0-9][0-9][0-9]-*.md")):
        texto = arq.read_text(encoding="utf-8")
        titulo = re.search(r"^# (.+)$", texto, re.M)
        rotas = []
        for bloco in _campo(texto, "Rotas"):
            rotas += [r.strip() for r in bloco.split("·") if r.strip()]
        status = []
        for s in _campo(texto, "Status HTTP"):
            status += [int(x) for x in re.findall(r"\d{3}", s)]
        entradas.append({
            "id": arq.name.split("-", 1)[0], "arquivo": arq, "titulo": titulo.group(1) if titulo else arq.stem,
            "rotas": rotas, "status": status, "mensagens": [_norm(m) for m in _campo(texto, "Mensagem contém")],
        })
    return entradas


def _rota_casa(rota_erro: str, rota_faq: str) -> bool:
    if not rota_erro or not rota_faq or rota_faq.lower().startswith("qualquer"):
        return False
    m_e = rota_erro.strip().split(" ", 1)
    m_f = rota_faq.strip().split(" ", 1)
    metodo_e, caminho_e = (m_e[0].upper(), m_e[1]) if len(m_e) == 2 else ("", m_e[0])
    metodo_f, caminho_f = (m_f[0].upper(), m_f[1]) if len(m_f) == 2 else ("", m_f[0])
    if metodo_f and metodo_e and metodo_f != metodo_e:
        return False
    prefixo = re.split(r"\{", caminho_f)[0].rstrip("/")
    caminho_e = caminho_e.split("?")[0]
    return bool(prefixo) and (caminho_e == prefixo or caminho_e.startswith(prefixo + "/"))


def buscar(mensagem: str = "", status: int | None = None, rota: str = "",
           pasta: Path = PASTA) -> list[tuple[int, dict]]:
    msg = _norm(mensagem)
    achados = []
    for e in carregar(pasta):
        pontos = 0
        if msg and any(m and m in msg for m in e["mensagens"]):
            pontos += 5
        if status and status in e["status"]:
            pontos += 1
        if rota and any(_rota_casa(rota, r) for r in e["rotas"]):
            pontos += 2
        if pontos >= 3 or (pontos and not msg):
            achados.append((pontos, e))
    return sorted(achados, key=lambda x: (-x[0], x[1]["id"]))


def sugerir(mensagem: str = "", status: int | None = None, rota: str = "") -> str:
    """Texto curto para anexar a uma mensagem de erro ('' se nada)."""
    try:
        achados = buscar(mensagem, status, rota)
    except OSError:
        return ""
    if not achados:
        return ""
    ids = ", ".join(e["id"] for _, e in achados[:3])
    return f" Possível FAQ: {ids} (.kit/conhecimento/faq-ias/ ou buscar_faq.py)."


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Busca no FAQ das IAs pelo sintoma do erro.")
    ap.add_argument("mensagem", nargs="?", default="", help="trecho da mensagem de erro")
    ap.add_argument("--status", type=int, help="código HTTP (ex.: 400)")
    ap.add_argument("--rota", default="", help='ex.: "POST /servicos"')
    args = ap.parse_args(argv)
    achados = buscar(args.mensagem, args.status, args.rota)
    if not achados:
        print("Nada no FAQ para esse sintoma. Resolva com cuidado (sem repetir às cegas) e registre o caso "
              "como aprendizado tipo 'api' (.kit/prompts/08-contribuir-com-o-kit.md).")
        return 1
    for pontos, e in achados:
        print(f"{e['id']} (pontos {pontos}): {e['titulo']}")
        print(f"   → {e['arquivo'].relative_to(PASTA.parents[1])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
