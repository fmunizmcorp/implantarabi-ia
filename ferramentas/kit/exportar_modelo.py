#!/usr/bin/env python3
"""Exporta `modelo-repo-clinica/` para o repositório-modelo público do GitHub.

O repositório-modelo (`fmunizmcorp/implantarabi-modelo-clinica`, marcado como
*Template repository*) é o que a clínica copia pelo botão "Use this template".
Ele carrega os marcadores do modelo SEM substituir (nome, porte, slug, versão
do kit, data): quem troca é `personalizar_clinica.py`, já dentro do repo da
clínica, na primeira sessão ("Vamos implantar <nome>").

Uso:
    python3 ferramentas/kit/exportar_modelo.py --destino DIR   # grava
    python3 ferramentas/kit/exportar_modelo.py --checar DIR    # só confere (sai 1 se defasado)

- Copia tudo do modelo (inclui .github/, .claude/, scripts/, .gitignore),
  preservando permissões (os .sh continuam executáveis).
- Troca o README.md pelo README do repositório-modelo (explica o "Use this
  template"); o README da clínica volta na personalização.
- Grava `.modelo-kit.json` com a versão do kit exportada.
- Remove de DIR o que não existe mais no modelo (nunca mexe em `.git/`).
  Por segurança, recusa (código 2) uma pasta com outros arquivos que não
  pareça o repositório-modelo (sem `.modelo-kit.json`).

Só stdlib.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comum import MODELO, RAIZ_KIT, ler_versao  # noqa: E402

REPO_MODELO = "fmunizmcorp/implantarabi-modelo-clinica"
REPO_KIT = "fmunizmcorp/implantarabi-ia"
MARCA_README = "<!-- implantarabi:repo-modelo -->"
MARCADOR = ".modelo-kit.json"
# Arquivos que o dono pode ter criado à mão no repo-modelo e que não atrapalham.
TOLERADOS = {"README.md", "LICENSE", "LICENSE.md", ".gitattributes"}


def readme_modelo(versao: str) -> str:
    return f"""{MARCA_README}
# Modelo do repositório de implantação do Sistema Rabi

> **Isto é um MODELO.** Não trabalhe aqui. Crie o repositório da sua clínica a
> partir dele (leva 1 minuto).

## Como usar

1. Clique em **Use this template → Create a new repository**
   (ou abra https://github.com/{REPO_MODELO}/generate).
2. **Owner:** a conta da clínica. **Nome:** `rabi-implantacao-<nome-da-clinica>`
   (minúsculas, sem acento, com hífen).
3. Marque **Private**. É obrigatório: o repositório da clínica vai guardar a
   chave da API e senhas.
4. Clique em **Create repository**.
5. Abra o Claude Code na web (https://claude.ai/code) no repositório novo e
   escreva só isto:

   ```
   Vamos implantar <Nome da Clínica>
   ```

   A IA baixa o kit, personaliza o repositório com o nome da clínica, confere
   se ele é privado e se a chave da API está configurada, e mostra o plano.

Passo a passo completo, clique a clique (contas, chave da API, ambiente do
Claude, problemas comuns):
https://github.com/{REPO_KIT}/blob/main/MANUAL-PASSO-A-PASSO.md

## Já é o repositório da sua clínica?

Então ainda não foi personalizado. Abra o Claude Code na web aqui e escreva
`Vamos implantar <Nome da Clínica>`: a IA troca este texto pelo README da
clínica.

---
Gerado automaticamente a partir do kit `{REPO_KIT}` (versão {versao}) por
`ferramentas/kit/exportar_modelo.py`. Não edite à mão: a próxima exportação
sobrescreve.
"""


def esperado() -> dict[str, tuple[bytes, bool]]:
    """{caminho relativo: (conteúdo, executável)} do repositório-modelo."""
    versao = ler_versao(RAIZ_KIT)
    saida: dict[str, tuple[bytes, bool]] = {}
    for origem in sorted(MODELO.rglob("*")):
        if origem.is_dir() or "__pycache__" in origem.parts or origem.suffix == ".pyc":
            continue
        rel = origem.relative_to(MODELO).as_posix()
        saida[rel] = (origem.read_bytes(), os.access(origem, os.X_OK))
    saida["README.md"] = (readme_modelo(versao).encode("utf-8"), False)
    marcador = {"kit": REPO_KIT, "versao_do_kit": versao,
                "gerado_por": "ferramentas/kit/exportar_modelo.py",
                "aviso": "repositório-modelo: os marcadores são trocados por personalizar_clinica.py"}
    saida[MARCADOR] = ((json.dumps(marcador, ensure_ascii=False, indent=2) + "\n").encode("utf-8"), False)
    return saida


def existentes(destino: Path) -> set[str]:
    achados = set()
    for p in destino.rglob("*"):
        rel = p.relative_to(destino)
        if rel.parts and rel.parts[0] == ".git":
            continue
        if p.is_file() or p.is_symlink():
            achados.add(rel.as_posix())
    return achados


def comparar(destino: Path) -> list[str]:
    """Lista de diferenças entre DIR e o que a exportação geraria."""
    exp = esperado()
    tem = existentes(destino) if destino.is_dir() else set()
    difs = []
    for rel, (conteudo, exe) in exp.items():
        alvo = destino / rel
        if rel not in tem:
            difs.append(f"falta: {rel}")
        elif alvo.read_bytes() != conteudo:
            difs.append(f"diferente: {rel}")
        elif exe and not os.access(alvo, os.X_OK):
            difs.append(f"sem permissão de execução: {rel}")
    for rel in sorted(tem - set(exp)):
        difs.append(f"sobrando: {rel}")
    return difs


def exportar(destino: Path) -> tuple[int, int]:
    exp = esperado()
    destino.mkdir(parents=True, exist_ok=True)
    tem = existentes(destino)
    gravados = 0
    for rel, (conteudo, exe) in exp.items():
        alvo = destino / rel
        if rel in tem and alvo.read_bytes() == conteudo and (not exe or os.access(alvo, os.X_OK)):
            continue
        alvo.parent.mkdir(parents=True, exist_ok=True)
        alvo.write_bytes(conteudo)
        alvo.chmod(0o755 if exe else 0o644)
        gravados += 1
    removidos = 0
    for rel in sorted(tem - set(exp)):
        (destino / rel).unlink()
        removidos += 1
    # pastas que ficaram vazias (fora de .git)
    for p in sorted(destino.rglob("*"), key=lambda x: len(x.parts), reverse=True):
        rel = p.relative_to(destino)
        if p.is_dir() and rel.parts[0] != ".git" and not any(p.iterdir()):
            p.rmdir()
    return gravados, removidos


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Exporta o modelo do repo da clínica para o repositório-modelo (Template).")
    grupo = ap.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--destino", help="pasta do clone do repositório-modelo (criada se não existir)")
    grupo.add_argument("--checar", metavar="DIR", help="não grava; sai 1 se DIR estiver defasado")
    args = ap.parse_args(argv)

    if not MODELO.is_dir():
        print(f"ERRO: modelo não encontrado em {MODELO}", file=sys.stderr)
        return 2
    alvo = Path(args.destino or args.checar).resolve()
    if alvo == RAIZ_KIT or RAIZ_KIT in alvo.parents:
        print("ERRO: o destino não pode ser dentro do kit.", file=sys.stderr)
        return 2

    if args.checar:
        difs = comparar(alvo)
        if difs:
            print(f"FAIL: {alvo} está defasado em relação ao modelo do kit ({len(difs)} diferença(s)):")
            for d in difs[:50]:
                print("  -", d)
            print("Rode: python3 ferramentas/kit/exportar_modelo.py --destino", alvo)
            return 1
        print(f"PASS: {alvo} igual ao modelo do kit {ler_versao(RAIZ_KIT)} ({len(esperado())} arquivos)")
        return 0

    if alvo.exists() and not (alvo / MARCADOR).exists():
        estranhos = sorted(r for r in existentes(alvo) if r not in TOLERADOS)
        if estranhos:
            print(f"ERRO: {alvo} tem arquivos e não parece o repositório-modelo (falta {MARCADOR}).",
                  file=sys.stderr)
            for r in estranhos[:10]:
                print("  -", r, file=sys.stderr)
            return 2
    gravados, removidos = exportar(alvo)
    print(f"Modelo exportado para {alvo} (kit {ler_versao(RAIZ_KIT)}): "
          f"{len(esperado())} arquivos, {gravados} gravado(s), {removidos} removido(s).")
    print("Marcadores preservados (a clínica personaliza com personalizar_clinica.py).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
