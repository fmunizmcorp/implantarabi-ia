#!/usr/bin/env python3
"""Personaliza o repositório da clínica criado pelo repositório-modelo.

Roda DENTRO do repo da clínica, na primeira sessão ("Vamos implantar <nome>"):

    python3 .kit/ferramentas/kit/personalizar_clinica.py --clinica "Clínica Exemplo" \
        --porte consultorio|pequena-media|rede [--repo .] [--slug NOME-DO-REPO]

- Troca os marcadores do modelo (nome, slug, porte, versão do kit, data) em
  todos os .md/.json/.yml/.yaml/.sh/.csv/.txt do repo, exceto `.kit/` e `.git/`.
- Versão do kit: lida de `.kit/VERSION`. Data: hoje em America/Sao_Paulo.
- Slug: `--slug`, senão o nome do repositório no `origin`, senão
  `rabi-implantacao-<nome>`.
- Troca o README do repositório-modelo pelo README da clínica (do kit).
- Idempotente: rodar de novo com o MESMO nome só completa o que faltar
  (código 0). Com OUTRO nome, recusa com código 3:
  "este repositório é da clínica X".

Códigos: 0 ok · 2 erro de uso · 3 repositório de outra clínica.
Só stdlib.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comum import (  # noqa: E402
    MODELO, PH_NOME, PH_SLUG, PORTES, RAIZ_KIT, eh_texto, hoje, ler_versao, slugificar, substituir,
    valores_clinica,
)

PULAR = {".kit", ".git", "__pycache__", "node_modules"}
SUFIXOS = {".md", ".json", ".yml", ".yaml", ".sh", ".csv", ".txt"}
MARCA_README = "<!-- implantarabi:repo-modelo -->"
LINHA_CLINICA = re.compile(r"^- \*\*Clínica:\*\*\s*(.+?)\s*$", re.M)


def arquivos_do_repo(repo: Path):
    pilha = [repo]
    while pilha:
        atual = pilha.pop()
        for p in sorted(atual.iterdir()):
            if p.is_symlink():
                continue
            if p.is_dir():
                if p.name not in PULAR:
                    pilha.append(p)
            elif p.suffix in SUFIXOS or eh_texto(p):
                yield p


def clinica_atual(repo: Path) -> str | None:
    """Nome registrado no ESTADO.md; None se ainda é o modelo (ou não há ESTADO)."""
    estado = repo / "ESTADO.md"
    if not estado.is_file():
        return None
    m = LINHA_CLINICA.search(estado.read_text(encoding="utf-8", errors="replace"))
    if not m or PH_NOME in m.group(1):
        return None
    return m.group(1).strip()


def mesma_clinica(a: str, b: str) -> bool:
    return slugificar(a) == slugificar(b)


def slug_do_origin(repo: Path) -> str | None:
    try:
        url = subprocess.run(["git", "-C", str(repo), "remote", "get-url", "origin"],
                             capture_output=True, text=True, timeout=10).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None
    if not url:
        return None
    nome = re.sub(r"\.git$", "", url.rstrip("/")).rsplit("/", 1)[-1].rsplit(":", 1)[-1]
    return nome or None


def raiz_do_kit(repo: Path) -> Path:
    kit = repo / ".kit"
    return kit if (kit / "VERSION").is_file() else RAIZ_KIT


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Personaliza o repo da clínica (troca os marcadores do modelo).")
    ap.add_argument("--clinica", required=True, help='nome da clínica, ex.: "Clínica Exemplo"')
    ap.add_argument("--porte", choices=sorted(PORTES),
                    help="consultorio · pequena-media · rede (obrigatório na primeira vez)")
    ap.add_argument("--repo", default=".", help="raiz do repo da clínica (padrão: pasta atual)")
    ap.add_argument("--slug", help="nome do repositório (padrão: o do origin)")
    args = ap.parse_args(argv)

    repo = Path(args.repo).resolve()
    nome = args.clinica.strip()
    if not nome or "<" in nome or ">" in nome:
        print("ERRO: informe o nome real da clínica em --clinica.", file=sys.stderr)
        return 2
    if not (repo / "ESTADO.md").is_file():
        print(f"ERRO: {repo} não parece o repo da clínica (falta ESTADO.md).", file=sys.stderr)
        return 2
    if repo == RAIZ_KIT or RAIZ_KIT in repo.parents:
        print("ERRO: não rode no kit; rode na raiz do repo da clínica.", file=sys.stderr)
        return 2

    atual = clinica_atual(repo)
    if atual and not mesma_clinica(atual, nome):
        print(f"RECUSADO: este repositório é da clínica {atual}. "
              f"Não misturo com \"{nome}\": crie outro repositório pelo modelo para ela.",
              file=sys.stderr)
        return 3

    kit = raiz_do_kit(repo)
    versao, data = ler_versao(kit), hoje()
    porte = args.porte or "pequena-media"
    if not atual and not args.porte:
        print("ERRO: primeira personalização: informe --porte (consultorio, pequena-media ou rede).",
              file=sys.stderr)
        return 2
    nome_final = atual or nome
    valores = valores_clinica(nome_final, porte, versao, data,
                              args.slug or slug_do_origin(repo))
    if atual and not args.porte:
        valores.pop("<PORTE>")  # já personalizado: não inventa porte para marcadores soltos

    alterados = []
    readme = repo / "README.md"
    modelo_readme = kit / "modelo-repo-clinica" / "README.md"
    if not modelo_readme.is_file():
        modelo_readme = MODELO / "README.md"
    if readme.is_file() and MARCA_README in readme.read_text(encoding="utf-8", errors="replace") \
            and modelo_readme.is_file():
        readme.write_text(modelo_readme.read_text(encoding="utf-8"), encoding="utf-8")
        alterados.append(readme)

    for p in arquivos_do_repo(repo):
        try:
            texto = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        novo = substituir(texto, valores)
        if novo != texto:
            p.write_text(novo, encoding="utf-8")
            if p not in alterados:
                alterados.append(p)

    restantes = [p for p in arquivos_do_repo(repo)
                 if PH_NOME in p.read_text(encoding="utf-8", errors="ignore")]
    if atual:
        print(f"Já personalizado para {atual}: {len(alterados)} arquivo(s) completado(s) agora.")
    else:
        print(f"Repositório personalizado: {nome_final} · porte {PORTES[porte]} · "
              f"repo {valores[PH_SLUG]} · kit {versao} · {data}")
        print(f"  arquivos alterados: {len(alterados)}")
    if restantes:
        print(f"  AVISO: {len(restantes)} arquivo(s) ainda com o marcador do nome:")
        for p in restantes[:10]:
            print("   -", p.relative_to(repo))
    print("Próximo: commit + push (\"S00: repositório personalizado para a clínica\").")
    return 0


if __name__ == "__main__":
    sys.exit(main())
