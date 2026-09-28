#!/usr/bin/env python3
"""Leva as novidades do kit para o repo da clínica (sem tocar em nenhum dado dela).

Roda DENTRO do repo da clínica (o kit em `.kit/` é atualizado pelo hook a cada sessão):

    python3 .kit/ferramentas/kit/atualizar_repo_clinica.py --novidades     # o que mudou no kit desde a última vez
    python3 .kit/ferramentas/kit/atualizar_repo_clinica.py --checar        # a estrutura do repo está defasada?
    python3 .kit/ferramentas/kit/atualizar_repo_clinica.py --aplicar       # atualiza a estrutura
    python3 .kit/ferramentas/kit/atualizar_repo_clinica.py --marcar-visto  # registra que as novidades foram tratadas

Estrutura (atualizada a partir de `.kit/modelo-repo-clinica/`, com o nome da
clínica reaplicado): CLAUDE.md, INDICE.md, README.md, scripts/, .claude/,
.github/, .gitignore — sem perder o que é da clínica:
- `.gitignore`: linhas da clínica são mantidas (união);
- `.claude/settings.json`: permissões em união, chaves extras da clínica mantidas;
- CLAUDE.md/README.md/INDICE.md: o bloco `<!-- REGRAS-LOCAIS:INICIO -->…FIM` da
  clínica é preservado;
- antes de sobrescrever, a versão anterior vai para
  `historico/estrutura-anterior/AAAA-MM-DD/`.
Fora da estrutura, um arquivo do modelo só é CRIADO se a PASTA dele ainda não
existe na clínica (pasta nova do kit). Arquivo apagado de propósito numa pasta
existente não volta. NUNCA sobrescreve: ESTADO.md, dados/, provas/,
credenciais/, historico/, decisoes/, pendencias/, documentos-do-cliente/,
contribuicoes-kit/, sprints/, diretrizes-da-equipe.md, PAPEIS.md, config/.

Estado em `.modelo-kit.json` (raiz do repo): `versao_do_kit` da estrutura e
`kit_visto` (última versão cujas novidades foram tratadas).

Códigos: 0 ok/em dia · 1 defasado (--checar) · 2 erro de uso.
Só stdlib.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comum import MODELO, PORTES, RAIZ_KIT, eh_texto, hoje, ler_versao, substituir, valores_clinica  # noqa: E402
from personalizar_clinica import clinica_atual, slug_do_origin  # noqa: E402

MARCADOR = ".modelo-kit.json"
ESTRUTURA_ARQ = {"CLAUDE.md", "INDICE.md", "README.md", ".gitignore"}
ESTRUTURA_PASTAS = {"scripts", ".claude", ".github"}
NUNCA = {"ESTADO.md", "diretrizes-da-equipe.md", "PAPEIS.md", MARCADOR}
NUNCA_PASTAS = {"dados", "provas", "credenciais", "historico", "decisoes", "pendencias",
                "documentos-do-cliente", "contribuicoes-kit", "sprints", "config"}
CAB_VERSAO = re.compile(r"^## v(\d+(?:\.\d+)*)\b.*$", re.M)
BLOCO_LOCAL = re.compile(r"<!-- REGRAS-LOCAIS:INICIO -->.*?<!-- REGRAS-LOCAIS:FIM -->", re.S)


def mesclar(rel: Path, novo: str, atual: str) -> str:
    """Conteúdo final de um arquivo de estrutura, sem perder o que é da clínica."""
    if rel.as_posix() == ".gitignore":
        linhas_novo = novo.splitlines()
        conhecidas = {l.strip() for l in linhas_novo}
        locais = [l for l in atual.splitlines() if l.strip() and l.strip() not in conhecidas
                  and l.strip() != "# linhas locais da clínica (mantidas pelo atualizador)"]
        if locais:
            linhas_novo += ["", "# linhas locais da clínica (mantidas pelo atualizador)"] + locais
        return "\n".join(linhas_novo).rstrip("\n") + "\n"
    if rel.as_posix() == ".claude/settings.json":
        try:
            n, a = json.loads(novo), json.loads(atual)
            original = json.loads(novo)
        except json.JSONDecodeError:
            return novo
        for chave, valor in a.items():
            if chave not in n:
                n[chave] = valor
        perm_n, perm_a = n.get("permissions", {}), a.get("permissions", {})
        for lista in ("allow", "deny", "ask"):
            juntos = list(perm_n.get(lista, []))
            juntos += [x for x in perm_a.get(lista, []) if x not in juntos]
            if juntos:
                perm_n[lista] = juntos
        if perm_n:
            n["permissions"] = perm_n
        if n == a:
            return atual  # nada mudou de verdade: não reformata o arquivo
        if n == original:
            return novo
        return json.dumps(n, ensure_ascii=False, indent=2) + "\n"
    m_atual = BLOCO_LOCAL.search(atual)
    if m_atual and BLOCO_LOCAL.search(novo):
        return BLOCO_LOCAL.sub(lambda _: m_atual.group(0), novo, count=1)
    if m_atual:  # modelo sem o bloco: não perde o da clínica
        return novo.rstrip("\n") + "\n\n" + m_atual.group(0) + "\n"
    return novo


def _versao(v: str) -> tuple[int, ...]:
    try:
        return tuple(int(x) for x in v.strip().lstrip("v").split("."))
    except ValueError:
        return (0,)


def ler_marcador(repo: Path) -> dict:
    try:
        return json.loads((repo / MARCADOR).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def gravar_marcador(repo: Path, **campos) -> None:
    dados = ler_marcador(repo)
    dados.setdefault("kit", "fmunizmcorp/implantarabi-ia")
    dados.update(campos)
    (repo / MARCADOR).write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def porte_da_clinica(repo: Path) -> str:
    try:
        texto = (repo / "ESTADO.md").read_text(encoding="utf-8")
    except OSError:
        return "pequena-media"
    m = re.search(r"^- \*\*Porte:\*\*\s*(.+?)\s*$", texto, re.M)
    rotulo = m.group(1) if m else ""
    for chave, nome in PORTES.items():
        if nome == rotulo:
            return chave
    return "pequena-media"


def eh_estrutura(rel: Path) -> bool:
    return (len(rel.parts) == 1 and rel.name in ESTRUTURA_ARQ) or rel.parts[0] in ESTRUTURA_PASTAS


def protegido(rel: Path) -> bool:
    return rel.as_posix() in NUNCA or rel.parts[0] in NUNCA_PASTAS


def planejar(repo: Path, modelo: Path = MODELO) -> list[tuple[str, Path, bytes, Path]]:
    """Lista (ação, caminho relativo, conteúdo novo, origem) — ação ∈ {atualizar, criar}."""
    nome = clinica_atual(repo)
    valores = valores_clinica(nome, porte_da_clinica(repo), ler_versao(modelo.parent), hoje(),
                              slug_do_origin(repo))
    plano = []
    for origem in sorted(modelo.rglob("*")):
        if origem.is_dir() or "__pycache__" in origem.parts:
            continue
        rel = origem.relative_to(modelo)
        alvo = repo / rel
        if eh_texto(origem):
            texto = substituir(origem.read_text(encoding="utf-8"), valores)
            if alvo.is_file() and eh_estrutura(rel):
                texto = mesclar(rel, texto, alvo.read_text(encoding="utf-8", errors="replace"))
            novo = texto.encode("utf-8")
        else:
            novo = origem.read_bytes()
        if not alvo.exists():
            if rel.as_posix() in NUNCA:
                continue
            # fora da estrutura, só cria em pasta NOVA (não ressuscita o que a clínica apagou)
            if eh_estrutura(rel) or (len(rel.parts) > 1 and not alvo.parent.exists()):
                plano.append(("criar", rel, novo, origem))
        elif eh_estrutura(rel) and not protegido(rel) and alvo.read_bytes() != novo:
            plano.append(("atualizar", rel, novo, origem))
    return plano


def novidades(repo: Path, kit: Path) -> tuple[list[str], str, str]:
    """Entradas do CHANGELOG do kit mais novas que `kit_visto` (título + 'Ação nas clínicas')."""
    atual = ler_versao(kit)
    marc = ler_marcador(repo)
    visto = marc.get("kit_visto") or marc.get("versao_do_kit") or ""
    try:
        changelog = (kit / "CHANGELOG.md").read_text(encoding="utf-8")
    except OSError:
        return [], visto, atual
    blocos = CAB_VERSAO.split(changelog)
    # split com grupo: [pré, v1, corpo1, v2, corpo2, ...]
    linhas: list[str] = []
    for i in range(1, len(blocos) - 1, 2):
        ver, corpo = blocos[i], blocos[i + 1]
        if visto and _versao(ver) <= _versao(visto):
            continue
        if not visto and linhas:
            break  # sem registro: mostra só a última versão
        titulo = next((l.strip("- ").strip() for l in corpo.splitlines() if l.strip().startswith("-")), "")
        linhas.append(f"v{ver}: {titulo[:140]}")
        for l in corpo.splitlines():
            if "Ação nas clínicas:" in l:
                linhas.append("   → " + l.split("Ação nas clínicas:", 1)[1].strip())
    return linhas, visto, atual


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Atualiza a estrutura do repo da clínica a partir do kit.")
    ap.add_argument("--repo", default=".", help="raiz do repo da clínica (padrão: pasta atual)")
    modo = ap.add_mutually_exclusive_group(required=True)
    modo.add_argument("--novidades", action="store_true")
    modo.add_argument("--checar", action="store_true")
    modo.add_argument("--aplicar", action="store_true")
    modo.add_argument("--marcar-visto", action="store_true")
    ap.add_argument("--curto", action="store_true", help="saída resumida (para o hook)")
    args = ap.parse_args(argv)

    repo = Path(args.repo).resolve()
    kit = MODELO.parent
    if repo == RAIZ_KIT or RAIZ_KIT in repo.parents:
        print("ERRO: rode na raiz do repo da clínica, não no kit.", file=sys.stderr)
        return 2
    if not (repo / "ESTADO.md").is_file():
        print(f"ERRO: {repo} não parece o repo da clínica (falta ESTADO.md).", file=sys.stderr)
        return 2
    if not clinica_atual(repo):
        print("Repo ainda não personalizado (primeira vez): nada a atualizar antes de personalizar.")
        return 0 if args.novidades or args.checar else 2

    if args.novidades:
        linhas, visto, atual = novidades(repo, kit)
        if not linhas:
            print(f"Novidades do kit: nenhuma (kit {atual}, já visto).")
        else:
            print(f"Novidades do kit desde {visto or '(sem registro)'} → {atual}:")
            for l in linhas[: 12 if args.curto else None]:
                print("  " + l)
            if args.curto and len(linhas) > 12:
                print(f"  … (+{len(linhas) - 12} linhas: .kit/CHANGELOG.md)")
        return 0

    if args.marcar_visto:
        gravar_marcador(repo, kit_visto=ler_versao(kit))
        print(f"Novidades marcadas como vistas até o kit {ler_versao(kit)}.")
        return 0

    plano = planejar(repo)
    if args.checar:
        if not plano:
            print(f"Estrutura do repo: em dia com o kit {ler_versao(kit)}.")
            return 0
        n_at = sum(1 for a, *_ in plano if a == "atualizar")
        n_cr = len(plano) - n_at
        print(f"Estrutura do repo: DEFASADA ({n_at} a atualizar, {n_cr} a criar). "
              "Rode: python3 .kit/ferramentas/kit/atualizar_repo_clinica.py --aplicar")
        if not args.curto:
            for acao, rel, *_ in plano:
                print(f"  {acao:9s} {rel.as_posix()}")
        return 1

    marc = ler_marcador(repo)
    if "kit_visto" not in marc and marc.get("versao_do_kit"):
        # guarda o "visto" ANTES de mudar a versão da estrutura: as novidades não se perdem
        gravar_marcador(repo, kit_visto=marc["versao_do_kit"])
    copia = repo / "historico" / "estrutura-anterior" / hoje()
    for acao, rel, novo, origem in plano:
        alvo = repo / rel
        if acao == "atualizar":
            destino = copia / rel
            destino.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(alvo, destino)
        alvo.parent.mkdir(parents=True, exist_ok=True)
        alvo.write_bytes(novo)
        shutil.copymode(origem, alvo)
        print(f"  {acao:9s} {rel.as_posix()}")
    gravar_marcador(repo, versao_do_kit=ler_versao(kit), estrutura_atualizada_em=hoje())
    print(f"Estrutura atualizada com o kit {ler_versao(kit)}: {len(plano)} arquivo(s). "
          "Nenhum dado da clínica foi tocado. Próximo: commit + push.")
    if any(a == "atualizar" for a, *_ in plano):
        print(f"  cópia das versões anteriores: {copia.relative_to(repo)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
