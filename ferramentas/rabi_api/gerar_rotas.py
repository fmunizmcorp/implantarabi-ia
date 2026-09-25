"""Gera conhecimento/api-externa/rotas/ a partir do spec OpenAPI da API externa do Rabi.

Um arquivo Markdown por grupo (tag) do Swagger, com cada operação:
método + caminho, permissão, resumo, descrição condensada, parâmetros,
campos do corpo (obrigatórios marcados, tipos, enums) e respostas.
Arquivos que passariam de 40 KB são divididos em parte-1, parte-2...

Uso (a partir da raiz do kit):
    python3 -m ferramentas.rabi_api.gerar_rotas
    python3 -m ferramentas.rabi_api.gerar_rotas --spec caminho/openapi.json --saida pasta/

Só biblioteca padrão.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
import unicodedata

METODOS = ("get", "post", "put", "patch", "delete")
LIMITE_BYTES = 38 * 1024  # margem sob o teto de 40 KB da política do kit

RAIZ_KIT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PASTA_API = os.path.join(RAIZ_KIT, "conhecimento", "api-externa")
PASTA_SPEC = os.path.join(PASTA_API, "spec")
PASTA_ROTAS = os.path.join(PASTA_API, "rotas")

URL_MANUAL = "https://www.rabisistemas.com.br/manual/api-externa/"
URL_SWAGGER = "https://api.rabisistemas.com.br/external-docs/"

# Ordem e página do manual de cada grupo (manual api-externa/index.html#mapa-grupos).
GRUPOS = [
    ("Empresas", "referencia-cadastros.html"),
    ("Depósitos", "referencia-cadastros.html"),
    ("Locais", "referencia-cadastros.html"),
    ("Auxiliares", "referencia-cadastros.html"),
    ("Operadoras", "referencia-cadastros.html"),
    ("Fornecedores", "referencia-cadastros.html"),
    ("Fabricantes", "referencia-cadastros.html"),
    ("Taxas", "referencia-cadastros.html"),
    ("Produtos", "referencia-cadastros.html"),
    ("Equipamentos", "referencia-cadastros.html"),
    ("Serviços", "referencia-cadastros.html"),
    ("Colaboradores", "referencia-cadastros.html"),
    ("Tabelas de Preço", "referencia-cadastros.html"),
    ("Convênios", "referencia-cadastros.html"),
    ("Grade de Colaborador", "referencia-cadastros.html"),
    ("Grade de Equipamento", "referencia-cadastros.html"),
    ("Financeiro", "referencia-operacao.html"),
    ("Estoque", "referencia-operacao.html"),
    ("Pacientes", "referencia-cadastros.html"),
    ("Parâmetros", "referencia-parametros.html"),
    ("Agendamentos", "referencia-operacao.html"),
    ("Orçamentos", "referencia-operacao.html"),
    ("Atendimentos", "referencia-operacao.html"),
    ("Faturamento", "referencia-operacao.html"),
    ("NFS-e", "referencia-operacao.html"),
]
PAGINA_GRUPO = dict(GRUPOS)
RESPOSTAS_GENERICAS = {"401", "403", "503"}


# --------------------------------------------------------------------------- utilidades

def slug_arquivo(texto: str) -> str:
    """'Grade de Colaborador' -> 'grade-de-colaborador'; 'NFS-e' -> 'nfse'."""
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    t = t.lower().replace("nfs-e", "nfse")
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t or "sem-grupo"


def ancora_manual(metodo: str, caminho: str) -> str:
    """Âncora usada pelo manual: op-<metodo>-<caminho com hífens>, {id} -> id, tudo minúsculo.

    Conferida contra as 268 âncoras de manualrabi/docs/api-externa/referencia-*.html.
    """
    s = re.sub(r"\{([^}]*)\}", r"\1", caminho)
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")
    return f"op-{metodo}-{s}".lower()


def url_manual(tag: str, metodo: str, caminho: str) -> str:
    pagina = PAGINA_GRUPO.get(tag, "index.html")
    return f"{URL_MANUAL}{pagina}#{ancora_manual(metodo, caminho)}"


def colapsar(texto: str | None, limite: int | None = None) -> str:
    if not texto:
        return ""
    t = re.sub(r"\s+", " ", str(texto)).strip()
    t = t.replace("|", "\\|")
    if limite and len(t) > limite:
        t = t[: limite - 1].rstrip() + "…"
    return t


def sem_permissao(desc: str) -> str:
    return re.sub(r"Permiss[aã]o exigida:\s*`[^`]+`\.?", "", desc or "").strip()


def permissoes_da_operacao(op: dict) -> list[str]:
    return re.findall(r"Permiss[aã]o exigida:\s*`([^`]+)`", op.get("description", "") or "")


def carregar_spec(caminho: str) -> dict:
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def listar_snapshots(pasta: str = PASTA_SPEC) -> list[str]:
    """openapi-AAAA-MM-DD.json e openapi-AAAA-MM-DD-N.json, em ordem cronológica."""
    def chave(c):
        m = re.search(r"openapi-(\d{4}-\d{2}-\d{2})(?:-(\d+))?\.json$", c)
        return (m.group(1), int(m.group(2) or 1)) if m else ("", 0)
    return sorted(glob.glob(os.path.join(pasta, "openapi-*.json")), key=chave)


def spec_mais_recente(pasta: str = PASTA_SPEC) -> str:
    arquivos = listar_snapshots(pasta)
    if not arquivos:
        raise FileNotFoundError(f"Nenhum openapi-*.json em {pasta}")
    return arquivos[-1]


def data_do_spec(caminho: str) -> str:
    m = re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(caminho))
    return m.group(1) if m else "desconhecida"


def versao_kit() -> str:
    try:
        with open(os.path.join(RAIZ_KIT, "VERSION"), encoding="utf-8") as f:
            return "v" + f.read().strip()
    except OSError:
        return "v?"


def operacoes(spec: dict):
    """Gera (tag, metodo, caminho, op) na ordem do spec."""
    for caminho, itens in spec.get("paths", {}).items():
        for metodo, op in itens.items():
            if metodo in METODOS and isinstance(op, dict):
                tags = op.get("tags") or ["Sem grupo"]
                yield tags[0], metodo, caminho, op


# --------------------------------------------------------------------------- schemas

class Resolvedor:
    def __init__(self, spec: dict):
        self.schemas = spec.get("components", {}).get("schemas", {})

    def resolver(self, sch: dict | None, vistos: frozenset = frozenset()):
        """Devolve (schema resolvido, nome do ref ou None, vistos)."""
        nome = None
        while isinstance(sch, dict) and "$ref" in sch:
            nome = sch["$ref"].split("/")[-1]
            if nome in vistos:
                return {"type": "object", "description": f"(recursivo: {nome})"}, nome, vistos
            vistos = vistos | {nome}
            sch = self.schemas.get(nome, {})
        if isinstance(sch, dict) and "allOf" in sch:
            junto: dict = {"type": "object", "properties": {}, "required": []}
            for parte in sch["allOf"]:
                p, _, vistos = self.resolver(parte, vistos)
                junto["properties"].update(p.get("properties", {}))
                junto["required"] += p.get("required", [])
                if p.get("description") and not junto.get("description"):
                    junto["description"] = p["description"]
            for k in ("description", "nullable"):
                if k in sch:
                    junto[k] = sch[k]
            sch = junto
        return sch or {}, nome, vistos

    def tipo(self, sch: dict) -> str:
        sch, nome, _ = self.resolver(sch)
        t = sch.get("type")
        if "oneOf" in sch or "anyOf" in sch:
            alts = sch.get("oneOf") or sch.get("anyOf")
            return " ou ".join(self.tipo(a) for a in alts)
        if t == "array":
            return "lista de " + self.tipo(sch.get("items", {}))
        base = t or ("objeto" if "properties" in sch else "?")
        if base == "object":
            base = "objeto"
        if sch.get("format"):
            base += f" ({sch['format']})"
        return base

    def detalhes(self, sch: dict) -> str:
        sch, _, _ = self.resolver(sch)
        partes = []
        if sch.get("enum"):
            vals = ", ".join(f"`{v}`" for v in sch["enum"][:15])
            if len(sch["enum"]) > 15:
                vals += ", …"
            partes.append("valores: " + vals)
        if sch.get("type") == "array" and isinstance(sch.get("items"), dict):
            it, _, _ = self.resolver(sch["items"])
            if it.get("enum"):
                partes.append("valores: " + ", ".join(f"`{v}`" for v in it["enum"][:15]))
        if sch.get("nullable"):
            partes.append("aceita null")
        for k, rot in (("minimum", "mín."), ("maximum", "máx."), ("maxItems", "máx. itens"),
                       ("minLength", "mín. caracteres")):
            if k in sch:
                partes.append(f"{rot} {sch[k]}")
        if "default" in sch:
            partes.append(f"padrão `{sch['default']}`")
        return "; ".join(partes)

    def campos(self, sch: dict, prefixo: str = "", profundidade: int = 0,
               vistos: frozenset = frozenset(), obrig_pai: bool = True):
        """Achata o schema em linhas (caminho, tipo, obrigatório, detalhe, descrição)."""
        sch, nome, vistos = self.resolver(sch, vistos)
        linhas = []
        if profundidade > 4:
            return linhas
        alts = sch.get("oneOf") or sch.get("anyOf")
        if alts and not sch.get("properties"):
            for i, alt in enumerate(alts, 1):
                a, anome, _ = self.resolver(alt, vistos)
                rotulo = f"{prefixo}(opção {i}{': ' + anome if anome else ''})"
                linhas.append((rotulo, self.tipo(alt), False, "", colapsar(a.get("description"), 140)))
                linhas += self.campos(alt, prefixo, profundidade + 1, vistos, False)
            return linhas
        if sch.get("type") == "array" and not prefixo:
            linhas.append(("(corpo é uma lista)", self.tipo(sch), True, "", colapsar(sch.get("description"), 140)))
            return linhas + self.campos(sch.get("items", {}), "[].", profundidade + 1, vistos)
        obrig = set(sch.get("required", []))
        for campo, sub in (sch.get("properties") or {}).items():
            subr, _, _ = self.resolver(sub, vistos)
            caminho = f"{prefixo}{campo}"
            linhas.append((caminho, self.tipo(sub), campo in obrig and obrig_pai,
                           self.detalhes(sub), colapsar(subr.get("description"), 160)))
            if subr.get("type") == "array":
                it, _, _ = self.resolver(subr.get("items", {}), vistos)
                if it.get("properties") or it.get("oneOf") or it.get("allOf"):
                    linhas += self.campos(subr["items"], f"{caminho}[].", profundidade + 1, vistos,
                                          campo in obrig and obrig_pai)
            elif subr.get("properties") or subr.get("allOf"):
                linhas += self.campos(sub, f"{caminho}.", profundidade + 1, vistos,
                                      campo in obrig and obrig_pai)
        return linhas

    def resumo_resposta(self, sch: dict) -> str:
        """Nomes de campos do primeiro nível (e do item em 'dados'/'data'/'items')."""
        sch, nome, _ = self.resolver(sch)
        if sch.get("type") == "array":
            it, inome, _ = self.resolver(sch.get("items", {}))
            nomes = list((it.get("properties") or {}).keys())
            return "lista crua" + (f" de `{inome}`" if inome else "") + (
                ": " + ", ".join(f"`{n}`" for n in nomes[:25]) + (" …" if len(nomes) > 25 else "") if nomes else "")
        props = sch.get("properties") or {}
        if not props:
            alts = sch.get("oneOf") or sch.get("anyOf")
            if alts:
                return "um de: " + " \\| ".join(self.resumo_resposta(a) for a in alts)
            return f"`{nome}`" if nome else (sch.get("type") or "")
        topo = list(props.keys())
        texto = "campos: " + ", ".join(f"`{n}`" for n in topo[:20]) + (" …" if len(topo) > 20 else "")
        for chave in ("dados", "data", "items", "resultados"):
            if chave in props:
                sub, _, _ = self.resolver(props[chave])
                if sub.get("type") == "array":
                    it, _, _ = self.resolver(sub.get("items", {}))
                    nomes = list((it.get("properties") or {}).keys())
                    if nomes:
                        texto += f"; item de `{chave}`: " + ", ".join(f"`{n}`" for n in nomes[:25]) + (
                            " …" if len(nomes) > 25 else "")
                break
        return texto


# --------------------------------------------------------------------------- render

def render_operacao(res: Resolvedor, tag: str, metodo: str, caminho: str, op: dict) -> str:
    perms = permissoes_da_operacao(op)
    linhas = [f"### `{metodo.upper()} {caminho}`", ""]
    linhas.append(f"- **Permissão:** {', '.join(f'`{p}`' for p in perms) or '(não declarada)'}"
                  f" · **Manual:** [{ancora_manual(metodo, caminho)}]({url_manual(tag, metodo, caminho)})")
    if op.get("summary"):
        linhas.append(f"- **Resumo:** {colapsar(op['summary'])}")
    desc = colapsar(sem_permissao(op.get("description", "")), 1400)
    if desc:
        linhas.append(f"- **Descrição:** {desc}")
    params = op.get("parameters") or []
    if params:
        linhas += ["", "| Parâmetro | Onde | Tipo | Obrig. | Observação |", "|---|---|---|---|---|"]
        for p in params:
            p, _, _ = res.resolver(p)
            sch = p.get("schema", {})
            obs = "; ".join(x for x in (res.detalhes(sch), colapsar(p.get("description"), 160)) if x)
            linhas.append(f"| `{p.get('name')}` | {p.get('in')} | {res.tipo(sch)} | "
                          f"{'**sim**' if p.get('required') else 'não'} | {obs} |")
    corpo = op.get("requestBody")
    if corpo:
        for ctype, cont in corpo.get("content", {}).items():
            campos = res.campos(cont.get("schema", {}))
            linhas += ["", f"**Corpo** (`{ctype}`{', obrigatório' if corpo.get('required') else ''}):", ""]
            if campos:
                linhas += ["| Campo | Tipo | Obrig. | Observação |", "|---|---|---|---|"]
                for cam, tip, obr, det, dsc in campos:
                    obs = "; ".join(x for x in (det, dsc) if x)
                    linhas.append(f"| `{cam}` | {tip} | {'**sim**' if obr else 'não'} | {obs} |")
            else:
                linhas.append("(sem campos documentados)")
    resp = op.get("responses") or {}
    if resp:
        linhas += ["", "**Respostas:**"]
        for cod, r in resp.items():
            if cod in RESPOSTAS_GENERICAS:
                continue
            r, _, _ = res.resolver(r)
            txt = colapsar(r.get("description"), 300)
            js = (r.get("content") or {}).get("application/json")
            if js and str(cod).startswith("2") and js.get("schema"):
                resumo = res.resumo_resposta(js["schema"])
                if resumo:
                    txt += f" — {colapsar(resumo, 900)}"
            linhas.append(f"- `{cod}` {txt}")
    linhas.append("")
    return "\n".join(linhas)


def dividir(blocos: list[str], extra: int) -> list[list[str]]:
    """Divide os blocos em n partes de tamanho parecido, cada uma abaixo de LIMITE_BYTES."""
    tam = [len(b.encode("utf-8")) + 1 for b in blocos]
    n = 1
    while True:
        alvo = sum(tam) / n
        partes: list[list[str]] = [[]]
        atual = 0
        for b, t in zip(blocos, tam):
            if partes[-1] and atual + t > alvo + 1 and len(partes) < n:
                partes.append([])
                atual = 0
            partes[-1].append(b)
            atual += t
        if all(sum(len(b.encode("utf-8")) + 1 for b in p) + extra <= LIMITE_BYTES for p in partes) or n >= len(blocos):
            return partes
        n += 1


def cabecalho(titulo: str, fonte_spec: str, data_spec: str) -> str:
    return (
        f"# {titulo}\n\n"
        f"> **Fonte:** Swagger oficial {URL_SWAGGER} (snapshot `spec/{os.path.basename(fonte_spec)}`)"
        f" · **Conferido em:** {data_spec}\n"
        f"> **Vale para:** produção (Swagger publicado em {data_spec}) · **Kit:** {versao_kit()}\n\n"
        "> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode "
        "`python3 -m ferramentas.rabi_api.atualizar_spec` para atualizar. Toda rota pode responder "
        "também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — "
        "ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).\n\n"
    )


def gerar(spec_path: str | None = None, saida: str = PASTA_ROTAS) -> dict:
    """Gera os arquivos. Devolve {'total': n, 'por_grupo': {tag: n}, 'arquivos': [...]}."""
    spec_path = spec_path or spec_mais_recente()
    spec = carregar_spec(spec_path)
    data_spec = data_do_spec(spec_path)
    res = Resolvedor(spec)
    por_tag: dict[str, list] = {}
    for tag, metodo, caminho, op in operacoes(spec):
        por_tag.setdefault(tag, []).append((metodo, caminho, op))
    ordem = [g for g, _ in GRUPOS if g in por_tag] + sorted(t for t in por_tag if t not in PAGINA_GRUPO)

    os.makedirs(saida, exist_ok=True)
    for antigo in glob.glob(os.path.join(saida, "*.md")):
        os.remove(antigo)

    indice_linhas = []
    arquivos = []
    total = 0
    for n, tag in enumerate(ordem, 1):
        ops = por_tag[tag]
        blocos = [render_operacao(res, tag, m, c, o) for m, c, o in ops]
        slug = slug_arquivo(tag)
        titulo_base = f"Rotas — {tag} ({len(ops)} operações)"
        cab = cabecalho(titulo_base, spec_path, data_spec)
        sumario = "## Operações\n\n" + "\n".join(f"- `{m.upper()} {c}`" for m, c, _ in ops) + "\n\n"
        # divide em partes equilibradas que caibam no limite
        partes = dividir(blocos, len((cab + sumario).encode("utf-8")) + 200)
        nomes = [f"{slug}.md"] if len(partes) == 1 else [f"{slug}-parte-{i}.md" for i in range(1, len(partes) + 1)]
        for i, (nome, pb) in enumerate(zip(nomes, partes), 1):
            titulo = titulo_base if len(partes) == 1 else f"{titulo_base} — parte {i} de {len(partes)}"
            conteudo = cabecalho(titulo, spec_path, data_spec)
            if len(partes) > 1:
                outras = " · ".join(f"[parte {j}]({nm})" for j, nm in enumerate(nomes, 1) if nm != nome)
                conteudo += f"Outras partes: {outras}.\n\n"
            conteudo += sumario if i == 1 else ""
            conteudo += "\n".join(pb)
            with open(os.path.join(saida, nome), "w", encoding="utf-8") as f:
                f.write(conteudo)
            arquivos.append(nome)
        total += len(ops)
        pagina = PAGINA_GRUPO.get(tag, "index.html")
        links = " · ".join(f"[{nm}]({nm})" for nm in nomes)
        indice_linhas.append(f"| {n} | {tag} | {len(ops)} | {links} | "
                             f"[{pagina}]({URL_MANUAL}{pagina}#grupo-{slug_arquivo(tag).replace('-de-', '-')}) |")

    n_caminhos = len(spec.get("paths", {}))
    indice = (
        cabecalho("Índice das rotas da API externa", spec_path, data_spec)
        + "Um arquivo por grupo (tag) do Swagger, na ordem do roteiro de implantação do manual "
          f"({URL_MANUAL}index.html#mapa-grupos). Leia só o grupo de que precisa. Para achar uma rota: "
          "`grep -rn \"PUT /convenios/{id}/servicos\" conhecimento/api-externa/rotas/`.\n\n"
        + "| # | Grupo | Operações | Arquivo(s) | Página do manual |\n|---|---|---|---|---|\n"
        + "\n".join(indice_linhas)
        + f"\n| | **Total** | **{total}** | {len(arquivos)} arquivos | {n_caminhos} caminhos |\n\n"
        + f"**Conferência:** soma das operações = **{total}** (esperado no Swagger de 25/09/2026: 268); "
          f"caminhos = **{n_caminhos}** (esperado: 191).\n"
    )
    with open(os.path.join(saida, "00-INDICE.md"), "w", encoding="utf-8") as f:
        f.write(indice)
    return {"total": total, "caminhos": n_caminhos,
            "por_grupo": {t: len(por_tag[t]) for t in ordem}, "arquivos": ["00-INDICE.md"] + arquivos}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Gera rotas/*.md a partir do spec OpenAPI.")
    ap.add_argument("--spec", help="arquivo openapi-*.json (padrão: o mais recente em spec/)")
    ap.add_argument("--saida", default=PASTA_ROTAS, help="pasta de saída (padrão: conhecimento/api-externa/rotas)")
    a = ap.parse_args(argv)
    r = gerar(a.spec, a.saida)
    for tag, n in r["por_grupo"].items():
        print(f"{tag:<22} {n:>3}")
    print(f"TOTAL de operações: {r['total']} · caminhos: {r['caminhos']} · arquivos: {len(r['arquivos'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
