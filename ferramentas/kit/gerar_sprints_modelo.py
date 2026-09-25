"""Copia o checklist de itens de cada playbook do kit (sprints/Sxx-*.md, seção
"## Checklist de itens") para o arquivo de status da clínica no modelo
(modelo-repo-clinica/sprints/Sxx.md, seção "## Checklist"), mantendo uma única fonte.

S10a e S10b entram no S10 da clínica (itens prefixados). Uso:
  python3 ferramentas/kit/gerar_sprints_modelo.py            # regrava
  python3 ferramentas/kit/gerar_sprints_modelo.py --checar   # CI: falha se estiver desatualizado
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CAB = "| # | item | status | origem | prova | observação |\n|---|---|---|---|---|---|"


def linhas_checklist(arq: Path) -> list[list[str]]:
    texto = arq.read_text(encoding="utf-8")
    m = re.search(r"^## Checklist de itens\s*$(.*?)(?=^## |\Z)", texto, re.M | re.S)
    if not m:
        return []
    saida = []
    for ln in m.group(1).splitlines():
        ln = ln.strip()
        if not ln.startswith("|") or set(ln.replace("|", "").strip()) <= set("-: "):
            continue
        cels = [c.strip() for c in ln.strip("|").split("|")]
        if cels and cels[0] == "#":
            continue
        saida.append(cels)
    return saida


def tabela_para(codigo: str) -> str:
    fontes = sorted(RAIZ.glob(f"sprints/{codigo}-*.md")) + sorted(RAIZ.glob(f"sprints/{codigo}[a-z]-*.md"))
    linhas, n = [], 0
    for arq in fontes:
        sub = re.match(r"(S\d{2}[a-z]?)", arq.name).group(1)
        for c in linhas_checklist(arq):
            n += 1
            item = c[1] if len(c) > 1 else ""
            if sub != codigo:
                item = f"[{sub}] {item}"
            obs = c[5] if len(c) > 5 else ""
            linhas.append(f"| {n} | {item} | pendente | | | {obs} |")
    return CAB + "\n" + "\n".join(linhas)


def aplicar(checar: bool) -> int:
    diferentes = []
    for alvo in sorted((RAIZ / "modelo-repo-clinica" / "sprints").glob("S[0-9][0-9].md")):
        codigo = alvo.stem
        tab = tabela_para(codigo)
        texto = alvo.read_text(encoding="utf-8")
        novo = re.sub(r"(^## Checklist\s*\n\n)(\|.*?\n)(?=\n|\Z)(?:(?!^#).)*?(?=^> |^## |\Z)",
                      lambda m: m.group(1) + tab + "\n\n", texto, count=1, flags=re.M | re.S)
        if novo == texto and tab not in texto:
            print(f"AVISO: não achei a seção '## Checklist' em {alvo}")
            continue
        if novo != texto:
            diferentes.append(alvo)
            if not checar:
                alvo.write_text(novo, encoding="utf-8")
    if checar and diferentes:
        print("FAIL: checklists do modelo desatualizados:", *[str(d.relative_to(RAIZ)) for d in diferentes], sep="\n  ")
        print("Rode: python3 ferramentas/kit/gerar_sprints_modelo.py")
        return 1
    print(("PASS" if checar else f"Atualizados: {len(diferentes)}") + " — checklists do modelo")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--checar", action="store_true")
    sys.exit(aplicar(ap.parse_args().checar))
