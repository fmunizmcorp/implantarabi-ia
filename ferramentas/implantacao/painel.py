"""Regenera o painel de progresso do ESTADO.md a partir de sprints/Sxx*.md.

Uso:  python3 .kit/ferramentas/implantacao/painel.py --repo .   [--so-mostrar]

O bloco entre <!-- PAINEL:INICIO --> e <!-- PAINEL:FIM --> é substituído.
Nada fora do bloco é alterado.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from checklist import ler_sprints  # type: ignore
else:
    from .checklist import ler_sprints

INICIO, FIM = "<!-- PAINEL:INICIO -->", "<!-- PAINEL:FIM -->"


def barra(pct: int, largura: int = 10) -> str:
    cheio = round(pct * largura / 100)
    return "█" * cheio + "░" * (largura - cheio)


def montar_painel(repo: Path) -> str:
    sprints = ler_sprints(repo)
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    linhas = [INICIO, f"_Painel gerado em {agora} por `painel.py` — não edite à mão._", "",
              "| Sprint | Nome | Progresso | % | Situação | Itens (conferidos/total) | Manual |",
              "|---|---|---|---|---|---|---|"]
    total_pct = []
    for s in sprints:
        c = s.contagem()
        base = len(s.considerados)
        total_pct.append(s.percentual if base else None)
        linhas.append(f"| {s.codigo} | {s.nome} | {barra(s.percentual)} | {s.percentual}% | {s.situacao} | {c['conferido']}/{base} | {('[📖](' + s.manual_url + ')') if s.manual_url else '—'} |")
    validos = [p for p in total_pct if p is not None]
    geral = round(sum(validos) / len(validos)) if validos else 0
    linhas += ["", f"**Progresso geral:** {barra(geral, 20)} {geral}%"]
    bloqueados = [(s.codigo, i.item) for s in sprints for i in s.itens if i.status == "bloqueado"]
    if bloqueados:
        linhas += ["", "**Bloqueios:**"] + [f"- {c}: {t}" for c, t in bloqueados]
    avisos = [f"{s.codigo}: {a}" for s in sprints for a in s.avisos]
    if avisos:
        linhas += ["", "**Avisos de formato:**"] + [f"- {a}" for a in avisos]
    linhas.append(FIM)
    return "\n".join(linhas)


def atualizar_estado(repo: Path, painel: str) -> Path:
    estado = Path(repo) / "ESTADO.md"
    texto = estado.read_text(encoding="utf-8") if estado.exists() else "# ESTADO\n\n"
    if INICIO in texto and FIM in texto:
        a = texto.index(INICIO)
        b = texto.index(FIM) + len(FIM)
        texto = texto[:a] + painel + texto[b:]
    else:
        texto = texto.rstrip() + "\n\n## Painel\n\n" + painel + "\n"
    estado.write_text(texto, encoding="utf-8")
    return estado


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Atualiza o painel do ESTADO.md")
    ap.add_argument("--repo", default=".", help="raiz do repo da clínica")
    ap.add_argument("--so-mostrar", action="store_true", help="imprime sem gravar")
    a = ap.parse_args(argv)
    repo = Path(a.repo)
    if not (repo / "sprints").is_dir():
        print(f"ERRO: {repo}/sprints não existe — este é o repo da clínica?", file=sys.stderr)
        return 2
    painel = montar_painel(repo)
    print(painel)
    if not a.so_mostrar:
        print(f"\nGravado em {atualizar_estado(repo, painel)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
