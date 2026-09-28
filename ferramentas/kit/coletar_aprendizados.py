#!/usr/bin/env python3
"""Coleta as issues de aprendizado das clínicas e monta a caixa de entrada do kit.

Uso (mantenedor ou workflow `.github/workflows/aprendizados.yml`):

    python3 ferramentas/kit/coletar_aprendizados.py \
        [--saida conhecimento/aprendizados-das-clinicas/caixa-de-entrada.md] \
        [--sinalizar sinal.txt] [--entrada issues.json]

- Lê as issues do kit com a label `aprendizado-clinica` (ou título que começa
  com "[aprendizado]") pela API pública do GitHub. Usa `GITHUB_TOKEN` se houver.
- Refaz o filtro de privacidade (`filtrar_aprendizado.filtrar_texto`) no texto
  recebido — 2ª trava. Issue com suspeita: o título sai mascarado na caixa e o
  número vai para `--sinalizar` (o workflow comenta e põe `revisar-privacidade`).
- `--entrada`: JSON já baixado (lista de issues), para teste sem rede.

Só stdlib. Código 0 ok · 2 erro de rede/uso.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comum import RAIZ_KIT, hoje  # noqa: E402
from filtrar_aprendizado import REPO_KIT, filtrar_texto  # noqa: E402

LABEL = "aprendizado-clinica"
SAIDA_PADRAO = RAIZ_KIT / "conhecimento" / "aprendizados-das-clinicas" / "caixa-de-entrada.md"


def baixar_issues(repo: str = REPO_KIT) -> list[dict]:
    todas: list[dict] = []
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    for pagina in range(1, 11):
        url = f"https://api.github.com/repos/{repo}/issues?state=all&per_page=100&page={pagina}"
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                                   "User-Agent": "implantarabi-kit"})
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(req, timeout=30) as r:
            lote = json.load(r)
        todas.extend(lote)
        if len(lote) < 100:
            break
    return todas


def eh_aprendizado(issue: dict) -> bool:
    if "pull_request" in issue:
        return False
    nomes = {(l.get("name") if isinstance(l, dict) else str(l)) for l in issue.get("labels", [])}
    return LABEL in nomes or (issue.get("title") or "").lower().startswith("[aprendizado]")


def campos_do_formulario(corpo: str) -> dict[str, str]:
    """Issue form → {rótulo: valor} (seções '### Rótulo')."""
    campos: dict[str, str] = {}
    for parte in re.split(r"^### ", corpo or "", flags=re.M)[1:]:
        cab, _, valor = parte.partition("\n")
        valor = valor.strip()
        campos[cab.strip()] = "" if valor == "_No response_" else valor
    return campos


def _celula(s: str, n: int = 70) -> str:
    s = re.sub(r"\s+", " ", s or "").replace("|", "/").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def montar_caixa(issues: list[dict]) -> tuple[str, list[int]]:
    abertas, fechadas, sinalizadas = [], [], []
    for i in sorted((x for x in issues if eh_aprendizado(x)), key=lambda x: x.get("number", 0)):
        campos = campos_do_formulario(i.get("body") or "")
        problemas = filtrar_texto((i.get("title") or "") + "\n" + (i.get("body") or ""))
        titulo = re.sub(r"^\[aprendizado\]\s*", "", i.get("title") or "", flags=re.I)
        if problemas:
            sinalizadas.append(i["number"])
            titulo = "(título ocultado: revisar privacidade)"
        linha = (f"| [#{i['number']}]({i.get('html_url', '')}) | {_celula(titulo)} | "
                 f"{_celula(campos.get('Tipo', ''), 30)} | {_celula(campos.get('Arquivo do kit afetado', ''), 45)} | "
                 f"{(i.get('created_at') or '')[:10]} | {'⚠ revisar' if problemas else 'ok'} |")
        (abertas if i.get("state") == "open" else fechadas).append(linha)
    cab = ("| Issue | Título | Tipo | Arquivo do kit | Aberta em | Privacidade |\n"
           "|---|---|---|---|---|---|\n")
    texto = (
        "# Caixa de entrada — aprendizados das clínicas\n\n"
        f"> Gerado por `ferramentas/kit/coletar_aprendizados.py` em {hoje()}. Não edite à mão.\n"
        f"> Fonte: issues do kit com a label `{LABEL}`. Como consolidar: "
        "`prompts/09-consolidar-aprendizados.md`.\n\n"
        f"## Abertas (a consolidar): {len(abertas)}\n\n"
        + (cab + "\n".join(abertas) + "\n" if abertas else "Nenhuma.\n")
        + f"\n## Fechadas (já tratadas; decisão em consolidados.md): {len(fechadas)}\n\n"
        + (cab + "\n".join(fechadas) + "\n" if fechadas else "Nenhuma.\n")
    )
    return texto, sinalizadas


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Monta a caixa de entrada dos aprendizados das clínicas.")
    ap.add_argument("--saida", default=str(SAIDA_PADRAO))
    ap.add_argument("--sinalizar", help="arquivo para listar issues com suspeita de dado sensível")
    ap.add_argument("--entrada", help="JSON de issues já baixado (teste sem rede)")
    args = ap.parse_args(argv)
    try:
        issues = (json.loads(Path(args.entrada).read_text(encoding="utf-8")) if args.entrada
                  else baixar_issues())
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as e:
        print(f"ERRO: não consegui ler as issues ({e.__class__.__name__}).", file=sys.stderr)
        return 2
    texto, sinalizadas = montar_caixa(issues)
    saida = Path(args.saida)
    saida.parent.mkdir(parents=True, exist_ok=True)
    antigo = saida.read_text(encoding="utf-8") if saida.is_file() else ""
    # Não reescreve só por causa da data (evita commit vazio no workflow).
    if re.sub(r"em \d{4}-\d{2}-\d{2}\.", "", antigo) != re.sub(r"em \d{4}-\d{2}-\d{2}\.", "", texto):
        saida.write_text(texto, encoding="utf-8")
        print(f"Caixa de entrada atualizada: {saida}")
    else:
        print("Caixa de entrada sem mudança.")
    if args.sinalizar:
        Path(args.sinalizar).write_text("".join(f"{n}\n" for n in sinalizadas), encoding="utf-8")
    if sinalizadas:
        print(f"ATENÇÃO: {len(sinalizadas)} issue(s) com suspeita de dado sensível: "
              + ", ".join(f"#{n}" for n in sinalizadas))
    return 0


if __name__ == "__main__":
    sys.exit(main())
