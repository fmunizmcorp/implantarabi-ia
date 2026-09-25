#!/usr/bin/env python3
"""Gera o repositório de uma clínica a partir de `modelo-repo-clinica/`.

Uso:
    python3 ferramentas/kit/novo_repo_clinica.py --destino DIR --clinica "Clínica Exemplo" \
        [--porte consultorio|pequena-media|rede] [--forcar]
    python3 .kit/ferramentas/kit/novo_repo_clinica.py --destino . --atualizar-claude

- Copia o modelo, substituindo os placeholders <NOME_DA_CLINICA>,
  <SLUG_DA_CLINICA>, <PORTE>, <VERSAO_DO_KIT>, <DATA_CRIACAO>.
- Grava a versão do kit em ESTADO.md.
- Não sobrescreve arquivo existente sem --forcar (relata o que pulou).
- --atualizar-claude: só reescreve .claude/agents|skills|commands (sem
  placeholders da clínica), para trazer a versão nova dos agentes do kit.

Só stdlib. Datas em America/Sao_Paulo quando disponível.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comum import (  # noqa: E402
    MODELO, PORTES, RAIZ_KIT, eh_texto, hoje, ler_versao, slugificar, substituir, valores_clinica,
)

PASTAS_CLAUDE = ("agents", "skills", "commands")
__all__ = ["slugificar", "hoje", "versao_kit", "substituir", "eh_texto", "PORTES", "RAIZ_KIT", "MODELO"]


def versao_kit() -> str:
    return ler_versao(RAIZ_KIT)


def copiar_modelo(destino: Path, valores: dict[str, str], forcar: bool,
                  so_claude: bool = False) -> tuple[list[Path], list[Path]]:
    criados, pulados = [], []
    for origem in sorted(MODELO.rglob("*")):
        if origem.is_dir() or "__pycache__" in origem.parts:
            continue
        rel = origem.relative_to(MODELO)
        if so_claude and not (len(rel.parts) > 2 and rel.parts[0] == ".claude"
                              and rel.parts[1] in PASTAS_CLAUDE):
            continue
        alvo = destino / rel
        if alvo.exists() and not (forcar or so_claude):
            pulados.append(rel)
            continue
        alvo.parent.mkdir(parents=True, exist_ok=True)
        if eh_texto(origem):
            alvo.write_text(substituir(origem.read_text(encoding="utf-8"), valores), encoding="utf-8")
            shutil.copymode(origem, alvo)
        else:
            shutil.copy2(origem, alvo)
        criados.append(rel)
    return criados, pulados


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Gera o repo de uma clínica a partir do modelo do kit.")
    ap.add_argument("--destino", required=True, help="pasta do repo da clínica (criada se não existir)")
    ap.add_argument("--clinica", help='nome da clínica, ex.: "Clínica Exemplo"')
    ap.add_argument("--porte", choices=sorted(PORTES), default="pequena-media")
    ap.add_argument("--slug", help="slug do repo (padrão: rabi-implantacao-<nome>)")
    ap.add_argument("--forcar", action="store_true", help="sobrescreve arquivos existentes")
    ap.add_argument("--atualizar-claude", action="store_true",
                    help="só atualiza .claude/agents|skills|commands a partir do kit")
    args = ap.parse_args(argv)

    if not MODELO.is_dir():
        print(f"ERRO: modelo não encontrado em {MODELO}", file=sys.stderr)
        return 2
    destino = Path(args.destino).resolve()
    if destino == RAIZ_KIT or RAIZ_KIT in destino.parents:
        print("ERRO: o destino não pode ser dentro do kit (o kit é só leitura).", file=sys.stderr)
        return 2
    if not args.atualizar_claude and not args.clinica:
        print("ERRO: informe --clinica \"Nome da clínica\".", file=sys.stderr)
        return 2

    versao, data = versao_kit(), hoje()
    if args.atualizar_claude:
        criados, _ = copiar_modelo(destino, {}, forcar=True, so_claude=True)
        print(f"Atualizados {len(criados)} arquivos de .claude/ a partir do kit {versao}.")
        return 0

    valores = valores_clinica(args.clinica, args.porte, versao, data, args.slug)
    slug = valores["<SLUG_DA_CLINICA>"]
    destino.mkdir(parents=True, exist_ok=True)
    criados, pulados = copiar_modelo(destino, valores, args.forcar)

    print(f"Repo da clínica gerado em {destino}")
    print(f"  clínica: {args.clinica} · slug: {slug} · porte: {PORTES[args.porte]} · kit: {versao} · data: {data}")
    print(f"  arquivos criados/atualizados: {len(criados)}")
    if pulados:
        print(f"  arquivos já existentes (NÃO sobrescritos; use --forcar): {len(pulados)}")
        for p in pulados[:20]:
            print(f"    - {p}")
    restantes = [p for p in destino.rglob("*.md")
                 if ".kit" not in p.parts and "<NOME_DA_CLINICA>" in p.read_text(encoding="utf-8", errors="ignore")]
    if restantes:
        print(f"  AVISO: {len(restantes)} arquivo(s) ainda com <NOME_DA_CLINICA> (existiam antes).")
    print("Próximos passos: git init/commit/push no repo PRIVADO; configurar RABI_API_KEY; abrir a sessão.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
