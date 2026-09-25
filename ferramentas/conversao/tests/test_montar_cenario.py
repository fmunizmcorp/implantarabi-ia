"""montar_cenario: fotos da API (formato do spec 25/09) → cenario.json que o simulador lê.

Round-trip com o exemplo fictício: as fotos são geradas a partir de exemplos/cenario-convenio-a.json
no formato da API; o cenário montado tem de dar os MESMOS números no motor.
"""
import json
from pathlib import Path

import pytest

from ferramentas.conversao import motor
from ferramentas.conversao import montar_cenario as mc
from ferramentas.conversao.modelo import cenario_from_dict

EX = Path(__file__).resolve().parents[1] / "exemplos" / "cenario-convenio-a.json"
TIPOS = {"MEDICAMENTO": 1, "MATERIAL": 2}
FONTES = {"PRECO FIXO CADASTRADO": 90, "Tabela Interna Exemplo": 91}


def _env(itens):
    return {"page": 1, "pageSize": 200, "total": len(itens), "totalPages": 1, "dados": itens}


def _fotos(cen):
    cat, conv = cen["catalogo"], cen["convenio"]
    servicos = []
    for s in cat["servicos"]:
        g = {"id": s["id"], "nome": s["nome"], "descricao": s["nome"], "valor": s.get("valor_cadastro", 0),
             "somarItens": s.get("somar_itens", False), "ativo": s.get("ativo", True),
             "codigoTUSS": s.get("codigo_tuss"), "tipoAtendimento": s.get("tipo_atendimento"),
             "ServicoProduto": [], "servicosRelacionados": [], "taxaServico": None}
        for it in s.get("itens", []):
            if it["tipo"] == "produto":
                g["ServicoProduto"].append({"id": 900 + it["id"], "servicoId": s["id"],
                                            "produto": {"id": it["id"]}, "quantidade": it["quantidade"]})
            elif it["tipo"] == "subservico":
                g["servicosRelacionados"].append({"servicoRelacionadoId": it["id"]})
            elif it["tipo"] == "taxa":
                g["taxaServico"] = {"id": it["id"], "taxas": "x"}
        servicos.append(g)
    produtos = [{"id": p["id"], "nome": p["nome"], "ativo": True, "codigoProduto": f"P{p['id']}",
                 "TipoProduto": {"id": TIPOS[p["tipo_produto"]], "nome": p["tipo_produto"]}}
                for p in cat["produtos"]]
    complemento = {str(p["id"]): {"custo": p["custo"], "preco_venda_tabela": p["preco_venda_tabela"],
                                  "fonte_preco": FONTES[p["fonte_preco"]]} for p in cat["produtos"]}
    tabelas = [{"tabela": "Tabela Interna Exemplo", "resposta": {"data": [
        {"id": p["id"], "nome": p["nome"], "tabelaPrecoInterna": {
            "precificacao1": v.get("PRECO_1"), "precificacao2": v.get("PRECO_2"), "precificacao3": None}}
        for p in cat["produtos"] for t, v in (p.get("precos_tabela") or {}).items()], "meta": {}}}]
    taxas = [{"id": t["id"], "taxas": t["nome"], "codigoTaxa": t.get("codigo"), "valor": t["valor_cadastro"],
              "ativo": True} for t in cat["taxas"]]
    cs = [{"id": 1, "servicoId": x["id"], "utiliza": x.get("utiliza", False), "pacote": x.get("pacote", False),
           "zerarValor": x.get("zerar", False), "valorInternoConvenio": x.get("valor_convertido"),
           "nomeConversao": x.get("nome"), "tipoAtendimentoId": x.get("tipo_atendimento")}
          for x in conv["servicos"]]
    cp = [{"id": 2, "produtoId": x["id"], "utiliza": x.get("utiliza", False), "zerarValor": x.get("zerar", False),
           "valorUnitarioConversao": x.get("valor_convertido"), "fatorK": None} for x in conv["produtos"]]
    ct = [{"id": 3, "taxaId": x["id"], "utiliza": x.get("utiliza", False), "zerarValor": x.get("zerar", False),
           "valorConvertido": x.get("valor_convertido")} for x in conv["taxas"]]
    fotos = {"servicos": servicos, "produtos": _env(produtos), "taxas": _env(taxas),
             "conv_servicos": _env(cs), "conv_produtos": _env(cp), "conv_taxas": _env(ct),
             "tabelas_preco": tabelas,
             "precificacao": [{"id": 1, "fontePrecoId": v, "nome": k, "tipoPrecificacao": None}
                              for k, v in FONTES.items()],
             "parametros": {"id": 1, "parametroVermelho": 100, "parametroAmarelo": 120}}
    politicas = [{"tipoProdutoId": TIPOS[p["tipo_produto"]], "fonte_preco": FONTES[p["fonte_preco"]],
                  "tipo_precificacao": p["tipo_precificacao"], "fator_k": p["fator_k"]} for p in conv["politicas"]]
    return fotos, politicas, complemento


def test_round_trip_exemplo_mesmos_numeros():
    cen = json.loads(EX.read_text(encoding="utf-8"))
    fotos, pols, comp = _fotos(cen)
    novo, lacunas = mc.montar_cenario(fotos, pols, convenio_id=12, nome="Convênio A", complemento_produtos=comp)
    cat0, c0 = cenario_from_dict(cen)
    cat1, c1 = cenario_from_dict(novo)
    for sid in cat0.servicos:
        a, b = motor.calcular_servico(cat0, c0, sid), motor.calcular_servico(cat1, c1, sid)
        assert (a.base, a.total, a.custo, a.farol, a.casa) == (b.base, b.total, b.custo, b.farol, b.casa), sid
    assert c1.politicas["MEDICAMENTO"].fonte_preco == "Tabela Interna Exemplo"
    assert cat1.servicos[304].itens[0].quantidade == 2
    assert any("NÃO confirmado" in x for x in lacunas)  # fontePrecoCompraOptionsId
    assert not any("composição" in x for x in lacunas)


def test_lacunas_quando_a_api_nao_traz():
    fotos = {"servicos": [{"id": 1, "nome": "Consulta", "valor": 200, "somarItens": False, "ativo": True}],
             "produtos": [{"id": 5, "nome": "Soro", "TipoProduto": {"id": 2, "nome": "MATERIAL"}}],
             "taxas": [], "conv_servicos": [], "conv_produtos": [], "conv_taxas": []}
    cen, lac = mc.montar_cenario(fotos, [])
    texto = " | ".join(lac)
    assert "composição" in texto and "politicasPorTipoProduto" in texto
    assert "produto 5" in texto and "custo" in texto
    assert "limites do Farol" in texto
    assert cen["convenio"]["parametro_vermelho"] == 100
    # --composicao resolve a composição
    cen2, lac2 = mc.montar_cenario(fotos, [], composicao={"1": [{"tipo": "produto", "id": 5, "quantidade": 1}]})
    assert cen2["catalogo"]["servicos"][0]["itens"][0]["id"] == 5
    assert not any("serviço 1" in x for x in lac2)


def test_cli_grava_cenario_lido_pelo_simulador(tmp_path, capsys):
    cen = json.loads(EX.read_text(encoding="utf-8"))
    fotos, pols, comp = _fotos(cen)
    args = ["--convenio-id", "12", "--nome", "Convênio A", "--saida", str(tmp_path / "cenario.json")]
    for k, v in (("servicos", fotos["servicos"]), ("produtos", fotos["produtos"]), ("taxas", fotos["taxas"]),
                 ("conv-servicos", fotos["conv_servicos"]), ("conv-produtos", fotos["conv_produtos"]),
                 ("conv-taxas", fotos["conv_taxas"]), ("politicas", pols), ("tabelas-preco", fotos["tabelas_preco"]),
                 ("precificacao", fotos["precificacao"]), ("parametros", fotos["parametros"]),
                 ("complemento-produtos", comp)):
        p = tmp_path / f"{k}.json"
        p.write_text(json.dumps(v, ensure_ascii=False), encoding="utf-8")
        args += [f"--{k}", str(p)]
    assert mc.main(args) == 0
    from ferramentas.conversao import simulador
    assert simulador.main([str(tmp_path / "cenario.json")]) == 0
    assert "Convênio A" in capsys.readouterr().out
