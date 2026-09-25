#!/usr/bin/env python3
"""Procura vazamento de segredo ou de dado real no kit (metodologia/politicas.md §3).

Padrões:
- chave da API: rbk_ seguido de 8+ caracteres alfanuméricos;
- CPF formatado (000.000.000-00), exceto CPFs de teste conhecidos;
- o nome da clínica de origem da experiência (proibido no kit);
- `senha: <valor>` com cara de senha real, fora de modelo-repo-clinica/.

Ignora: .git, referencias/ (tabelas de referência), conhecimento/api-externa/spec/,
arquivos binários. Uma linha com o marcador `vazamento-ok` é pulada (use só com
justificativa ao lado).

Nunca imprime o valor inteiro encontrado. Código 0 (pass) / 1 (fail).
Uso: python3 ferramentas/kit/verificar_vazamento.py [--raiz DIR]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comum import RAIZ_KIT, arquivos, rel  # noqa: E402

CHAVE = re.compile(r"rbk_[A-Za-z0-9]{8,}")
CPF = re.compile(r"(?<!\d)\d{3}\.\d{3}\.\d{3}-\d{2}(?!\d)")
NOME_PROIBIDO = re.compile("clin" + "fec", re.IGNORECASE)  # montado para não casar consigo mesmo
SENHA = re.compile(r"\bsenha\s*:\s*[`\"']?([^\s`\"'|]+)", re.IGNORECASE)

# CPFs de teste conhecidos (fictícios / exemplos públicos de validação).
CPFS_TESTE = {f"{d*3}.{d*3}.{d*3}-{d*2}" for d in "0123456789"} | {
    "123.456.789-09",
    "529.982.247-25",
    "111.444.777-35",
}
EXT_TEXTO = {".md", ".py", ".sh", ".json", ".yml", ".yaml", ".csv", ".txt", ".toml", ".cfg", ".ini", ".html", ""}
MARCADOR = "vazamento-ok"


def _ignorado(relativo: str) -> bool:
    return relativo.startswith("referencias/") or relativo.startswith("conhecimento/api-externa/spec/")


def _parece_senha(valor: str) -> bool:
    if valor.startswith(("<", "…", "...", "(", "[")) or len(valor) < 6:
        return False
    return bool(re.search(r"[\d!@#$%^&*_\-+=]", valor))


def _mascara(v: str) -> str:
    return v[:6] + "…" if len(v) > 6 else "…"


def verificar(raiz: Path) -> list[str]:
    achados = []
    for p in arquivos(raiz):
        r = rel(p, raiz).replace("\\", "/")
        if _ignorado(r) or (p.suffix not in EXT_TEXTO and p.name != ".gitignore"):
            continue
        try:
            texto = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        no_modelo = r.startswith("modelo-repo-clinica/")
        for n, linha in enumerate(texto.splitlines(), 1):
            if MARCADOR in linha:
                continue
            for m in CHAVE.finditer(linha):
                achados.append(f"{r}:{n} CHAVE rbk_ ({_mascara(m.group(0))})")
            for m in CPF.finditer(linha):
                if m.group(0) not in CPFS_TESTE:
                    achados.append(f"{r}:{n} CPF ({m.group(0)[:4]}…)")
            if NOME_PROIBIDO.search(linha):
                achados.append(f"{r}:{n} NOME DE CLÍNICA REAL")
            if not no_modelo:
                for m in SENHA.finditer(linha):
                    if _parece_senha(m.group(1)):
                        achados.append(f"{r}:{n} SENHA ({_mascara(m.group(1))})")
    return achados


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Vazamento de segredo/dado real")
    ap.add_argument("--raiz", default=str(RAIZ_KIT))
    args = ap.parse_args(argv)
    raiz = Path(args.raiz).resolve()
    achados = verificar(raiz)
    if achados:
        print(f"FAIL: {len(achados)} possível(is) vazamento(s) em {raiz}")
        for linha in achados:
            print("  -", linha)
        return 1
    print(f"PASS: nenhum vazamento encontrado em {raiz}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
