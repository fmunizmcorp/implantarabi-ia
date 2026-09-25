"""Baixa o Swagger publicado da API externa, salva um snapshot datado, compara com o anterior
e regenera conhecimento/api-externa/rotas/.

Uso (a partir da raiz do kit — só o MANTENEDOR do kit roda isto; sessões de clínica só leem):
    python3 ferramentas/rabi_api/atualizar_spec.py
    python3 ferramentas/rabi_api/atualizar_spec.py --arquivo-js swagger-ui-init.js   # offline
    python3 ferramentas/rabi_api/atualizar_spec.py --sem-rotas --relatorio mudancas.md

O spec fica embutido em https://api.rabisistemas.com.br/external-docs/swagger-ui-init.js, no
objeto "swaggerDoc". Não precisa de chave.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
import urllib.request

import os as _os
import sys as _sys

if __package__ in (None, ""):
    _sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(__file__), "..", "..")))
    __package__ = "ferramentas.rabi_api"

from . import gerar_rotas  # noqa: E402
from .cliente import _abridor  # noqa: E402

URL_JS = "https://api.rabisistemas.com.br/external-docs/swagger-ui-init.js"


def extrair_swaggerdoc(js: str) -> dict:
    pos = js.find('"swaggerDoc"')
    if pos < 0:
        raise ValueError('Não achei "swaggerDoc" no swagger-ui-init.js')
    inicio = js.find("{", pos)
    spec, _ = json.JSONDecoder().raw_decode(js[inicio:])
    if "paths" not in spec:
        raise ValueError("Objeto swaggerDoc sem 'paths'")
    return spec


def baixar_js(url: str = URL_JS, timeout: float = 60) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "implantarabi-ia/atualizar_spec"})
    with _abridor(url).open(req, timeout=timeout) as r:
        return r.read().decode("utf-8")


def _ops(spec: dict) -> dict:
    return {f"{m.upper()} {p}": o for t, m, p, o in gerar_rotas.operacoes(spec)}


def comparar(anterior: dict, novo: dict) -> dict:
    a, n = _ops(anterior), _ops(novo)
    alteradas = []
    for k in sorted(set(a) & set(n)):
        if json.dumps(a[k], sort_keys=True) != json.dumps(n[k], sort_keys=True):
            partes = sorted(x for x in set(a[k]) | set(n[k])
                            if json.dumps(a[k].get(x), sort_keys=True) != json.dumps(n[k].get(x), sort_keys=True))
            alteradas.append((k, partes))
    sa = anterior.get("components", {}).get("schemas", {})
    sn = novo.get("components", {}).get("schemas", {})
    return {
        "adicionadas": sorted(set(n) - set(a)),
        "removidas": sorted(set(a) - set(n)),
        "alteradas": alteradas,
        "schemas_adicionados": sorted(set(sn) - set(sa)),
        "schemas_removidos": sorted(set(sa) - set(sn)),
        "schemas_alterados": sorted(k for k in set(sa) & set(sn)
                                    if json.dumps(sa[k], sort_keys=True) != json.dumps(sn[k], sort_keys=True)),
        "info_alterada": anterior.get("info") != novo.get("info"),
        "total_anterior": len(a), "total_novo": len(n),
    }


def relatorio(c: dict, arq_ant: str | None, arq_novo: str) -> str:
    linhas = [f"# Mudanças no Swagger da API externa — {_dt.date.today().isoformat()}", "",
              f"- Anterior: `{os.path.basename(arq_ant) if arq_ant else '(nenhum)'}` · operações: {c['total_anterior']}",
              f"- Novo: `{os.path.basename(arq_novo)}` · operações: {c['total_novo']}",
              f"- Texto geral (info/convenções) mudou: {'sim' if c['info_alterada'] else 'não'}", ""]
    for titulo, chave in (("Operações adicionadas", "adicionadas"), ("Operações removidas", "removidas")):
        linhas.append(f"## {titulo} ({len(c[chave])})")
        linhas += [f"- `{x}`" for x in c[chave]] or ["- nenhuma"]
        linhas.append("")
    linhas.append(f"## Operações alteradas ({len(c['alteradas'])})")
    linhas += [f"- `{k}` — mudou: {', '.join(p)}" for k, p in c["alteradas"]] or ["- nenhuma"]
    linhas += ["", f"## Schemas: +{len(c['schemas_adicionados'])} · -{len(c['schemas_removidos'])} · "
                   f"~{len(c['schemas_alterados'])}"]
    for rot, chave in (("+", "schemas_adicionados"), ("-", "schemas_removidos"), ("~", "schemas_alterados")):
        linhas += [f"- {rot} `{x}`" for x in c[chave]]
    linhas += ["", "Depois de atualizar: revise convencoes.md, defeitos-conhecidos.md e "
                   "proibidas-sem-ordem-escrita.md se alguma mudança afetar regras."]
    return "\n".join(linhas) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python3 ferramentas/rabi_api/atualizar_spec.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", default=URL_JS)
    ap.add_argument("--arquivo-js", help="usar um swagger-ui-init.js já baixado")
    ap.add_argument("--destino", default=gerar_rotas.PASTA_SPEC, help="pasta dos snapshots openapi-*.json")
    ap.add_argument("--rotas", default=gerar_rotas.PASTA_ROTAS, help="pasta de saída das rotas")
    ap.add_argument("--sem-rotas", action="store_true", help="não regenerar rotas/")
    ap.add_argument("--relatorio", help="gravar o relatório de mudanças neste arquivo .md")
    a = ap.parse_args(argv)

    if a.arquivo_js:
        with open(a.arquivo_js, encoding="utf-8") as f:
            js = f.read()
    else:
        js = baixar_js(a.url)
    novo = extrair_swaggerdoc(js)

    os.makedirs(a.destino, exist_ok=True)
    anteriores = gerar_rotas.listar_snapshots(a.destino)
    arq_ant = anteriores[-1] if anteriores else None
    anterior = json.load(open(arq_ant, encoding="utf-8")) if arq_ant else {"paths": {}}

    hoje = _dt.date.today().isoformat()
    arq_novo = os.path.join(a.destino, f"openapi-{hoje}.json")
    if anterior == novo and arq_ant:
        print(f"Swagger igual ao snapshot {os.path.basename(arq_ant)} — nada novo.")
        arq_novo = arq_ant
    else:
        n = 2
        while os.path.exists(arq_novo):
            arq_novo = os.path.join(a.destino, f"openapi-{hoje}-{n}.json")
            n += 1
        with open(arq_novo, "w", encoding="utf-8") as f:
            json.dump(novo, f, ensure_ascii=False, indent=1)
        print(f"Snapshot salvo: {arq_novo}")

    c = comparar(anterior, novo)
    rel = relatorio(c, arq_ant, arq_novo)
    print(rel)
    if a.relatorio:
        with open(a.relatorio, "w", encoding="utf-8") as f:
            f.write(rel)
    if not a.sem_rotas:
        r = gerar_rotas.gerar(arq_novo, a.rotas)
        print(f"Rotas regeneradas em {a.rotas}: {r['total']} operações, {r['caminhos']} caminhos, "
              f"{len(r['arquivos'])} arquivos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
