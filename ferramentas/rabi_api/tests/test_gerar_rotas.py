"""O gerador de rotas cobre as 268 operações do Swagger de 25/09/2026, sem arquivo acima de 40 KB."""
import glob
import json
import os
import re

import pytest

from .. import gerar_rotas
from ..atualizar_spec import comparar, extrair_swaggerdoc

SPEC = os.path.join(gerar_rotas.PASTA_SPEC, "openapi-2026-09-25.json")


@pytest.fixture(scope="module")
def gerado(tmp_path_factory):
    saida = tmp_path_factory.mktemp("rotas")
    r = gerar_rotas.gerar(SPEC, str(saida))
    return r, saida


def test_268_operacoes_191_caminhos_25_grupos(gerado):
    r, _ = gerado
    assert r["total"] == 268
    assert r["caminhos"] == 191
    assert len(r["por_grupo"]) == 25
    assert sum(r["por_grupo"].values()) == 268


def test_cada_operacao_aparece_uma_vez(gerado):
    _, saida = gerado
    titulos = []
    for arq in glob.glob(os.path.join(saida, "*.md")):
        if arq.endswith("00-INDICE.md"):
            continue
        titulos += re.findall(r"^### `(\w+ \S+)`", open(arq, encoding="utf-8").read(), re.M)
    spec = json.load(open(SPEC, encoding="utf-8"))
    esperado = {f"{m.upper()} {p}" for _, m, p, _ in gerar_rotas.operacoes(spec)}
    assert len(titulos) == 268
    assert set(titulos) == esperado


def test_arquivos_abaixo_de_40kb_e_com_cabecalho(gerado):
    _, saida = gerado
    for arq in glob.glob(os.path.join(saida, "*.md")):
        txt = open(arq, encoding="utf-8").read()
        assert os.path.getsize(arq) <= 40 * 1024, arq
        assert "**Fonte:**" in txt and "**Conferido em:**" in txt and "**Vale para:**" in txt


def test_ancora_do_manual():
    assert gerar_rotas.ancora_manual("put", "/convenios/{id}/servicos") == "op-put-convenios-id-servicos"
    assert (gerar_rotas.ancora_manual("get", "/estoque/buscar/{lote}/{produtoId}/{localizacaoId}")
            == "op-get-estoque-buscar-lote-produtoid-localizacaoid")


def test_88_permissoes(gerado):
    spec = json.load(open(SPEC, encoding="utf-8"))
    perms = {p for _, _, _, o in gerar_rotas.operacoes(spec) for p in gerar_rotas.permissoes_da_operacao(o)}
    assert len(perms) == 88


def test_extrair_swaggerdoc_e_comparar():
    spec = json.load(open(SPEC, encoding="utf-8"))
    js = 'window.onload = function() { var options = { "swaggerDoc": ' + json.dumps(spec) + ', "x": 1 }; };'
    assert extrair_swaggerdoc(js) == spec
    menor = json.loads(json.dumps(spec))
    del menor["paths"]["/empresas"]["post"]
    menor["paths"]["/empresas"]["get"]["summary"] = "mudou"
    c = comparar(menor, spec)
    assert c["adicionadas"] == ["POST /empresas"]
    assert c["alteradas"] == [("GET /empresas", ["summary"])]
