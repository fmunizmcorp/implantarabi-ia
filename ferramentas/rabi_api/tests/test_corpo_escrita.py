"""Conversor leitura → escrita de /servicos e /produtos (PUT sobrescreve: nada pode sumir em silêncio)."""
import json
import os

import pytest

from .. import gerar_rotas
from ..corpo_escrita import (CAMPOS_PRODUTO, CAMPOS_SERVICO, OBRIGATORIOS_PRODUTO,
                             OBRIGATORIOS_SERVICO, CampoDeEscritaAusente,
                             corpo_put_produto, corpo_put_servico)

SPEC = os.path.join(gerar_rotas.PASTA_SPEC, "openapi-2026-09-25.json")


def _schema(nome):
    with open(SPEC, encoding="utf-8") as f:
        return json.load(f)["components"]["schemas"][nome]


def test_campos_batem_com_o_spec():
    s = _schema("ServicoCreate")
    assert set(CAMPOS_SERVICO) == set(s["properties"])
    assert set(OBRIGATORIOS_SERVICO) == set(s["required"])
    p = _schema("ProdutoCreate")
    assert set(CAMPOS_PRODUTO) == set(p["properties"])
    assert set(OBRIGATORIOS_PRODUTO) == set(p["required"])


def _leitura_servico():
    return {
        "id": 46, "nome": "Aplicação endovenosa", "descricao": "Aplicação endovenosa",
        "codigo": "A1", "codigoTUSS": "20104090", "valor": 600.0, "tempoServico": 30,
        "somarItens": False, "linkAuxiliar": None, "preparamentos": None, "preparo": None,
        "tipoServico": {"id": 3, "nome": "Procedimento"}, "tipoCodigo": {"id": 22, "nome": "TUSS"},
        "tipoGuiaId": 2, "tabelaANS87": None, "regimeDeAtendimento": {"id": 1},
        "tipoAtendimento": 5, "taxaServico": {"id": 9, "nome": "Taxa de sala"},
        "valorTaxaServico": 15.0,
        "ServicoEspecialidade": [{"id": 700, "servicoId": 46, "especialidadeId": 12}],
        "produtos": [{"id": 77, "servicoId": 46, "produto": {"id": 501, "nome": "Soro"}}],
        "equipamentos": [{"id": 31, "nome": "Poltrona"}],
        "servicosRelacionados": [{"servicoRelacionadoId": 47}],
        "habilitarAgendamentoOnline": False, "apenasComColaboradorDesignado": False,
        "ativo": True, "createdAt": "x", "updatedAt": "y",
    }


def test_servico_mapeia_nomes_e_aninhados():
    corpo = corpo_put_servico({"dados": _leitura_servico()}, complementos={"valor": 40.0})
    assert set(corpo) == set(CAMPOS_SERVICO)
    assert "somarItens" not in corpo and corpo["somarItems"] is False
    assert corpo["valor"] == 40.0  # mudança aplicada
    assert corpo["tipoServicoId"] == 3 and corpo["tipoCodigoId"] == 22 and corpo["tabelaANS87ID"] is None
    assert corpo["regimeDeAtendimentoId"] == 1 and corpo["taxaServicoId"] == 9
    assert corpo["especialidadesId"] == [12]
    assert corpo["produtoIds"] == [501]
    assert corpo["equipamentoIds"] == [31]
    assert corpo["servicosRelacionados"] == [47]
    for k in ("id", "ativo", "createdAt", "updatedAt"):
        assert k not in corpo


def test_servico_forma_minima_do_spec_levanta_erro_listando_faltantes():
    # o schema Servico (leitura) do spec só tem estes campos: não dá para montar o PUT com segurança
    leitura = {"id": 45, "nome": "Consulta", "descricao": "Consulta", "codigo": "1001",
               "codigoTUSS": "10101012", "valor": 250, "tempoServico": 30, "somarItens": False,
               "ativo": True}
    with pytest.raises(CampoDeEscritaAusente) as e:
        corpo_put_servico(leitura)
    for campo in ("especialidadesId", "produtoIds", "servicosRelacionados", "taxaServicoId", "tipoServicoId"):
        assert campo in e.value.faltam and campo in str(e.value)
    assert "somarItems" not in e.value.faltam and "valor" not in e.value.faltam


def test_servico_complementos_resolvem_faltantes():
    leitura = {"nome": "Consulta", "descricao": "Consulta", "valor": 250, "somarItens": False}
    faltam = [c for c in CAMPOS_SERVICO if c not in ("nome", "descricao", "valor", "somarItems")]
    comp = {c: None for c in faltam}
    comp.update(especialidadesId=[1], produtoIds=[], equipamentoIds=[], servicosRelacionados=[])
    corpo = corpo_put_servico(leitura, complementos=comp)
    assert corpo["especialidadesId"] == [1] and corpo["valor"] == 250


def test_complemento_com_nome_de_leitura_e_recusado():
    with pytest.raises(CampoDeEscritaAusente, match="somarItens"):
        corpo_put_servico(_leitura_servico(), complementos={"somarItens": True})


def test_vinculo_ambiguo_e_recusado():
    leitura = _leitura_servico()
    leitura["ServicoEspecialidade"] = [{"id": 700, "servicoId": 46}]  # sem especialidadeId
    with pytest.raises(CampoDeEscritaAusente, match="ambíguo"):
        corpo_put_servico(leitura)


def test_obrigatorio_vazio_e_recusado():
    leitura = _leitura_servico()
    leitura["descricao"] = None
    with pytest.raises(CampoDeEscritaAusente, match="descricao"):
        corpo_put_servico(leitura)


def _leitura_produto():
    return {
        "id": 120, "nome": "Soro fisiológico 0,9% 250 ml", "codigoProduto": "P1", "codigoEAN": None,
        "codigoNCM": None, "apresentacao": "Bolsa", "contendo": 1, "valorUnitario": None,
        "permitirEstoqueNegativo": True, "prazoDeReposicao": 7, "ativo": True,
        "TipoProduto": {"id": 4, "nome": "Medicamento"}, "Fabricante": {"id": 8, "nome": "Fab"},
        "deposito": {"id": 2, "descricaoDeposito": "Central"},
        "UnidadeDeMedida": {"id": 6, "descricao": "Bolsa", "termo": "BOL"},
    }


def test_produto_forma_do_spec_mapeia_aninhados_e_exige_o_resto():
    with pytest.raises(CampoDeEscritaAusente) as e:
        corpo_put_produto(_leitura_produto())
    assert set(e.value.faltam) == {"principioAtivoId", "cdId", "tipoCodigoId", "tabelaANS87ID",
                                   "precoUltimaPesquisa", "dataUltimaPesquisa", "fornecedores", "anexos"}


def test_produto_com_complementos():
    comp = {"principioAtivoId": 3, "cdId": None, "tipoCodigoId": 20, "tabelaANS87ID": None,
            "precoUltimaPesquisa": None, "dataUltimaPesquisa": None, "fornecedores": [5], "anexos": []}
    corpo = corpo_put_produto(_leitura_produto(), complementos=comp)
    assert set(corpo) == set(CAMPOS_PRODUTO)
    assert corpo["tipoProdutoId"] == 4 and corpo["fabricanteId"] == 8
    assert corpo["depositoId"] == 2 and corpo["unidadeDeMedidaId"] == 6
    assert corpo["estoquePodeNegativar"] is True and "permitirEstoqueNegativo" not in corpo


def test_produto_fornecedores_de_linhas_de_vinculo():
    leitura = _leitura_produto()
    leitura.update(principioAtivo={"id": 3}, cdId=None, tipoCodigoId=20, tabelaANS87ID=None,
                   precoUltimaPesquisa=None, dataUltimaPesquisa=None, anexos=[],
                   ProdutoFornecedor=[{"id": 1, "produtoId": 120, "fornecedorId": 5}])
    corpo = corpo_put_produto(leitura)
    assert corpo["fornecedores"] == [5] and corpo["principioAtivoId"] == 3
