"""Testa a chave da API externa do Rabi: uma leitura por grupo (25 áreas) + validade.

Só faz GET. Não imprime dado de nenhum registro — só status e contagem (total).
Nunca imprime a chave (mostra mascarada).

Uso (a partir da raiz do repo da clínica ou do kit):
    python3 -m ferramentas.rabi_api.testar_chave
    python3 -m ferramentas.rabi_api.testar_chave --saida provas/S00/teste-chave-2026-10-01.md
    RABI_API_BASE=https://api.hmg.rabisistemas.dev/api/v1/integrations python3 -m ferramentas.rabi_api.testar_chave

Leitura do resultado:
    OK            a chave lê esta área (a coluna "total" mostra quantos registros existem)
    OK (validação) a rota respondeu erro de validação (400/404/422) → a permissão existe
    SEM PERMISSÃO 403 → falta a permissão indicada; peça ao time Rabi
    CHAVE         401/503 → problema com a chave; o teste para na hora (sem repetir)
"""
from __future__ import annotations

import argparse
import datetime as _dt
import sys

from .cliente import ClienteRabi, ErroRabi, normalizar_envelope

# (grupo, rota de leitura sem dado pessoal, params, permissão)
SONDAS = [
    ("Empresas", "/empresas", {}, "empresa:read"),
    ("Depósitos", "/depositos", {"page": 1, "pageSize": 1}, "deposito:read"),
    ("Locais", "/locais", {}, "local:read"),
    ("Auxiliares", "/auxiliares/sexos", {}, "auxiliar:read"),
    ("Operadoras", "/operadoras", {"page": 1, "pageSize": 1}, "operadora:read"),
    ("Fornecedores", "/fornecedores", {"page": 1, "pageSize": 1}, "fornecedor:read"),
    ("Fabricantes", "/fabricantes", {"page": 1, "pageSize": 1}, "fabricante:read"),
    ("Taxas", "/taxas", {"page": 1, "pageSize": 1}, "taxa:read"),
    ("Produtos", "/produtos", {"page": 1, "pageSize": 1}, "produto:read"),
    ("Equipamentos", "/equipamentos", {"page": 1, "pageSize": 1}, "equipamento:read"),
    ("Serviços", "/servicos", {"page": 1, "pageSize": 1}, "servico:read"),
    ("Colaboradores", "/colaboradores", {"page": 1, "pageSize": 1}, "colaborador:read"),
    ("Tabelas de Preço", "/tabelas-preco", {}, "tabelaPreco:read"),
    ("Convênios", "/convenios", {"page": 1, "pageSize": 1}, "convenio:read"),
    ("Grade de Colaborador", "/grades-colaborador", {"page": 1, "pageSize": 1}, "gradeColaborador:read"),
    ("Grade de Equipamento", "/grades-equipamento", {"page": 1, "pageSize": 1}, "gradeEquipamento:read"),
    ("Financeiro", "/financeiro/movimentacoes", {"page": 1, "pageSize": 1}, "financeiro:read"),
    ("Estoque", "/estoque/saldo-produtos", {"page": 1, "pageSize": 1}, "estoque:read"),
    ("Pacientes", "/pacientes", {"page": 1, "pageSize": 1}, "paciente:read"),
    ("Parâmetros", "/parametros/avisos", {}, "parametro:read"),
    ("Agendamentos", "/agendamentos/motivo-cancelamento", {}, "agendamento:read"),
    ("Orçamentos", "/orcamentos/status", {}, "orcamento:read"),
    # sem pacienteId a rota responde 400 "Informe pacienteId" se a permissão existir (nenhum dado volta)
    ("Atendimentos", "/atendimentos/historico", {}, "atendimento:read"),
    ("Faturamento", "/faturamento/glosas/status", {}, "faturamento:read"),
    ("NFS-e", "/nfse/emitentes", {}, "nfse:read"),
]


def _total(texto: str):
    import json
    try:
        corpo = json.loads(texto)
    except ValueError:
        return "?"
    try:
        env = normalizar_envelope(corpo)
        return env["total"] if env["total"] is not None else len(env["itens"])
    except ErroRabi:
        return "objeto" if isinstance(corpo, dict) else ("null" if corpo is None else "?")


def testar(cliente: ClienteRabi) -> dict:
    linhas = []
    parou = None
    for grupo, rota, params, perm in SONDAS:
        try:
            r = cliente.requisicao("GET", rota, params or None, levantar=False)
        except ErroRabi as e:
            linhas.append((grupo, rota, perm, "ERRO", "-", str(e)[:80]))
            continue
        if 200 <= r.status < 300:
            linhas.append((grupo, rota, perm, "OK", _total(r.texto), str(r.status)))
        elif r.status == 403:
            linhas.append((grupo, rota, perm, "SEM PERMISSÃO", "-", "403"))
        elif r.status in (400, 404, 422):
            linhas.append((grupo, rota, perm, "OK (validação)", "-", str(r.status)))
        elif r.status in (401, 503):
            linhas.append((grupo, rota, perm, "CHAVE", "-", str(r.status)))
            parou = r.status
            break
        else:
            linhas.append((grupo, rota, perm, "ERRO", "-", str(r.status)))
    return {"linhas": linhas, "parou": parou, "validade": cliente.validade,
            "dias": cliente.dias_restantes(), "base": cliente.base, "chave": cliente.chave_mascarada,
            "origem": cliente.origem_chave}


def relatorio_md(res: dict) -> str:
    agora = _dt.datetime.now().astimezone().strftime("%d/%m/%Y %H:%M")
    ok = sum(1 for l in res["linhas"] if l[3].startswith("OK"))
    out = [f"# Teste da chave da API externa — {agora}", "",
           f"- **Base:** {res['base']}",
           f"- **Chave:** {res['chave']} (origem: {res['origem']})",
           f"- **Validade (X-ApiKey-Expires-At):** {res['validade'] or 'não informada'}"
           + (f" · **faltam {res['dias']} dias**" if res["dias"] is not None else ""),
           f"- **Áreas alcançadas:** {ok} de {len(SONDAS)}", ""]
    if res["dias"] is not None and res["dias"] < 15:
        out += [f"> ⚠️ **A chave vence em {res['dias']} dias.** Peça a chave nova ao time Rabi agora "
                "(não há renovação automática nem autoatendimento).", ""]
    if res["parou"]:
        out += [f"> ⛔ **O teste parou com {res['parou']}:** a API não aceitou a chave. Não repita em loop. "
                "Confira a chave (ver conhecimento/api-externa/chave-e-token.md) e, se estiver certa, "
                "avise o time Rabi.", ""]
    out += ["| Área | Rota testada | Permissão | Resultado | Total | HTTP |", "|---|---|---|---|---|---|"]
    for g, r, p, s, t, h in res["linhas"]:
        out.append(f"| {g} | `{r}` | `{p}` | {s} | {t} | {h} |")
    faltam = [l[2] for l in res["linhas"] if l[3] == "SEM PERMISSÃO"]
    if faltam:
        out += ["", "**Permissões que faltam:** " + ", ".join(f"`{p}`" for p in faltam)]
    out += ["", "_Só leitura. Nenhum dado de registro foi exibido ou gravado; a chave não aparece neste arquivo._"]
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python3 -m ferramentas.rabi_api.testar_chave",
                                 description="Testa a chave da API externa do Rabi (25 áreas + validade).")
    ap.add_argument("--base", help="URL base (padrão: RABI_API_BASE ou produção)")
    ap.add_argument("--saida", help="grava o resumo Markdown neste arquivo")
    a = ap.parse_args(argv)
    try:
        c = ClienteRabi(base=a.base, esperas_503=())
    except ErroRabi as e:
        print(f"⛔ {e}")
        return 2
    res = testar(c)
    md = relatorio_md(res)
    print(md)
    if a.saida:
        with open(a.saida, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"Resumo gravado em {a.saida}")
    return 1 if res["parou"] else 0


if __name__ == "__main__":
    sys.exit(main())
