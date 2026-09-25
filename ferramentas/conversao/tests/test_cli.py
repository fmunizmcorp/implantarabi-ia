"""Testes das ferramentas de linha de comando com o cenário fictício de exemplos/."""
import copy
import json
import os

import pytest

from ferramentas.conversao import montar_convenio as mc, simulador, conferir_farol as cf
from ferramentas.conversao.modelo import cenario_from_dict

AQUI = os.path.dirname(__file__)
EX = os.path.join(AQUI, "..", "exemplos")
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
SPEC = os.path.join(RAIZ, "conhecimento", "api-externa", "spec", "openapi-2026-09-25.json")
CENARIO = os.path.join(EX, "cenario-convenio-a.json")
CSV_OK = os.path.join(EX, "precos-convenio-a.csv")
CSV_ERR = os.path.join(EX, "precos-com-erros.csv")


# --------------------------------------------------------------------------- simulador

def test_simulador_imprime_quatro_linhas(capsys):
    assert simulador.main([CENARIO, "--servico", "303"]) == 0
    out = capsys.readouterr().out
    assert "🔒 casa ........ R$ 150,00 (soma dos itens)" in out
    assert "✅ próprio ..... R$ 0,00" in out and "sem preço próprio" in out
    assert "Σ  total ....... R$ 176,00" in out
    assert "Farol 525% VERDE" in out


def test_simulador_mostra_item_fora_com_motivo(capsys):
    simulador.main([CENARIO, "--servico", "304"])
    out = capsys.readouterr().out
    assert "FORA (ZERADO_EM_PACOTE)" in out and "Σ  total ....... R$ 120,00" in out


def test_simulador_csv_sobrepoe_e_da_o_mesmo_resultado(capsys):
    simulador.main([CENARIO, "--csv", CSV_OK, "--json"])
    d = json.loads(capsys.readouterr().out)
    tot = {s["servico_id"]: s["total"] for s in d["servicos"]}
    assert tot == {301: 180, 302: 121, 303: 176, 304: 120, 305: 10}


# --------------------------------------------------------------------------- montar_convenio

def test_csv_ok_gera_lotes_e_previa(tmp_path):
    rc = mc.main([CSV_OK, "--convenio-id", "12", "--saida", str(tmp_path), "--catalogo", CENARIO,
                  "--atual", os.path.join(EX, "atual-convenio-a.json")])
    assert rc == 0
    man = json.loads((tmp_path / "manifesto.json").read_text(encoding="utf-8"))
    fases = [c["fase"] for c in man["chamadas"]]
    assert fases == sorted(fases)  # Utiliza → valores → textos → tipo atendimento → Pacote/Zerar
    assert fases[0] == "1-utiliza" and fases[-1] == "5-pacote-zerar"
    previa = (tmp_path / "previa.md").read_text(encoding="utf-8")
    assert "| servico 301 Consulta clínica | valorInternoConvenio | R$ 150,00 | R$ 180,00 |" in previa
    assert "| servico 304 Curativo em pacote | pacote | não | sim |" in previa
    corpo = json.loads((tmp_path / man["chamadas"][-1]["arquivo"]).read_text(encoding="utf-8"))
    assert {"servicoId": 304, "pacote": True, "zerarValor": False} in corpo["servicos"]


def test_vazio_vira_null_e_zero_vira_zero(tmp_path):
    csv = tmp_path / "p.csv"
    csv.write_text("tipo;id_rabi;valor_combinado;origem\nservico;1;;contrato\nservico;2;0,00;contrato\n"
                   "servico;3;manter;contrato\nservico;4;1.234,56;contrato\n", encoding="utf-8")
    linhas, ach = mc.ler_csv(str(csv))
    assert not [a for a in ach if a.nivel == "ERRO"]
    v = {l.id: l.campos.get("valorInternoConvenio", "OMITIDO") for l in linhas}
    assert v == {1: None, 2: 0.0, 3: "OMITIDO", 4: 1234.56}


def test_csv_com_erros_nao_gera_lote(tmp_path):
    rc = mc.main([CSV_ERR, "--convenio-id", "12", "--saida", str(tmp_path)])
    assert rc == 2
    assert not list(tmp_path.glob("*-lote-*.json"))
    previa = (tmp_path / "previa.md").read_text(encoding="utf-8")
    assert "0,01 não pode ser usado" in previa
    assert "linha sem origem" in previa
    assert "coluna pacote não existe na aba produtos" in previa
    assert "coluna fator_k não existe na aba taxas" in previa


def test_avisos_valor_combinado_e_zerar_sem_pacote(tmp_path):
    csv = tmp_path / "p.csv"
    csv.write_text("tipo;id_rabi;utiliza;valor_combinado;pacote;zerar;origem\n"
                   "servico;303;sim;266,16;não;não;contrato\nproduto;101;sim;;;sim;contrato\n", encoding="utf-8")
    linhas, ach = mc.ler_csv(str(csv))
    ach += mc.validar_linhas(linhas, json.load(open(CENARIO, encoding="utf-8")))
    textos = " ".join(a.mensagem for a in ach)
    assert "valor combinado não é pacote: serviço soma itens" in textos
    assert "ZERAR_SEM_PACOTE" in textos


def test_lotes_de_ate_200():
    linhas = [mc.LinhaPreco(i, "produto", i, "", "o", "", {"utiliza": True}) for i in range(1, 451)]
    ch = mc.gerar_lotes(linhas, 9, unico=True)
    assert [c["itens"] for c in ch] == [200, 200, 50]
    assert all(c["caminho"] == "/convenios/9/produtos" for c in ch)


# --------------------------------------------------------------------------- campos x spec

def _schema(spec, nome):
    return spec["components"]["schemas"][nome]["properties"]


TIPO_JSON = {"integer": int, "number": (int, float), "boolean": bool, "string": str}


@pytest.mark.skipif(not os.path.exists(SPEC), reason="spec da API externa ausente")
def test_todo_campo_gerado_existe_no_schema(tmp_path):
    spec = json.load(open(SPEC, encoding="utf-8"))
    schemas = {"servicos": "ConvenioServicoItem", "produtos": "ConvenioProdutoItem", "taxas": "ConvenioTaxaItem"}
    # o mapa inteiro precisa existir no spec
    for tipo, mapa in mc.MAPA.items():
        props = _schema(spec, schemas[mc.ABA[tipo]])
        for campo in list(mapa.values()) + [mc.CHAVE_ID[tipo]]:
            assert campo in props, f"{tipo}.{campo} não existe em {schemas[mc.ABA[tipo]]}"
    # e cada valor gerado respeita o tipo do schema
    csv = tmp_path / "todas.csv"
    csv.write_text(
        ";".join(c for c in mc.COLUNAS if c != "descricao_convenio") + "\n"
        "servico;1;S;NOME;C1;3;22;5;sim;10,50;sim;não;sim;não;;;;4;contrato;\n"
        "servico;2;S2;;;;;limpar;sim;;;;;;;;;;contrato;\n"
        "produto;2;P;NOMEP;C2;3;20;;sim;5,00;;sim;;;10,5;7;Preço 2;2;contrato;\n"
        "taxa;3;T;NOMET;C3;3;18;;sim;0;;sim;;;;;;;contrato;\n", encoding="utf-8")
    linhas, ach = mc.ler_csv(str(csv))
    assert not [a for a in ach if a.nivel == "ERRO"], ach
    for ch in mc.gerar_lotes(linhas, 1, unico=True):
        req = spec["paths"]["/convenios/{id}/" + ch["aba"]]["put"]["requestBody"]["content"]["application/json"]
        nome_req = req["schema"]["$ref"].split("/")[-1]
        props_req = spec["components"]["schemas"][nome_req]
        assert list(ch["corpo"]) == props_req["required"]
        assert len(ch["corpo"][ch["aba"]]) <= props_req["properties"][ch["aba"]]["maxItems"]
        props = _schema(spec, schemas[ch["aba"]])
        for item in ch["corpo"][ch["aba"]]:
            for campo, valor in item.items():
                assert campo in props, campo
                p = props[campo]
                if valor is None:
                    assert p.get("nullable"), f"{campo} não aceita null"
                    continue
                assert isinstance(valor, TIPO_JSON[p["type"]]), (campo, valor)
                if p["type"] in ("integer", "number"):
                    assert not isinstance(valor, bool)
                if "enum" in p:
                    assert valor in p["enum"]


# --------------------------------------------------------------------------- conferir_farol

def _arq(tmp_path, nome, dados):
    p = tmp_path / nome
    p.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    return str(p)


def test_conferir_sem_divergencia(capsys):
    rc = cf.main([CENARIO, "--servicos", os.path.join(EX, "farol-servicos-convenio-a.json"),
                  "--itens", os.path.join(EX, "farol-itens-convenio-a.json"),
                  "--produtos", os.path.join(EX, "farol-produtos-convenio-a.json"), "--ignorar-inativos"])
    assert rc == 0
    assert "Nenhuma divergência" in capsys.readouterr().out


def _farol(nome):
    return copy.deepcopy(json.load(open(os.path.join(EX, f"farol-{nome}-convenio-a.json"), encoding="utf-8")))


def _item(itens, raiz, iid):
    return next(i for i in itens["dados"] if i["servico_raiz_id"] == raiz and i["item_id"] == iid)


def test_exemplos_estao_no_formato_real():
    """Os exemplos usam os nomes de campo medidos na resposta REAL de produção (25/09)."""
    itens, prods, serv = _farol("itens"), _farol("produtos"), _farol("servicos")
    for k in ("page", "pageSize", "total", "totalPages", "dados"):
        assert k in itens and k in prods and k in serv
    for campo in ("conta_no_total", "motivo_exclusao", "receita_item_total", "quantidade_efetiva",
                  "receita_total_servico", "utiliza_no_convenio", "servico_pai_id", "farol_servico"):
        assert campo in itens["dados"][0], campo
    for campo in ("receita", "custo", "utiliza", "farol"):  # nomes do Swagger que a resposta real NÃO tem
        assert campo not in itens["dados"][0], campo
    for campo in ("receita_sem_zerar", "fonte_id", "fonte_nome", "fator_k", "origem_receita", "custo_status"):
        assert campo in prods["dados"][0], campo


def test_conferir_aponta_divergencias(tmp_path, capsys):
    serv, itens = _farol("servicos"), _farol("itens")
    for s in serv["dados"]:
        if s["servico_id"] == 303:
            s["receita_total"] = 121.0  # medicamento ficou fora (ex.: faltou Utiliza)
    _item(itens, 304, 104)["conta_no_total"] = True  # a API diz que o item zerado conta
    _item(itens, 304, 104)["receita_item_total"] = 12.0
    itens["dados"] = [i for i in itens["dados"] if not (i["servico_raiz_id"] == 303 and i["item_id"] == 101)]
    rc = cf.main([CENARIO, "--servicos", _arq(tmp_path, "s.json", serv), "--itens", _arq(tmp_path, "i.json", itens),
                  "--saida", str(tmp_path / "rel.md")])
    out = capsys.readouterr().out
    assert rc == 1
    assert "| [303] Medicamento Exemplo aplicado | (serviço) | receita_total | 176.0 | 121.0 |" in out
    assert "(ausente na API)" in out
    assert "| conta_no_total | False | True | motivo previsto: ZERADO_EM_PACOTE |" in out
    assert "| receita_item_total | 0.0 | 12.0 |" in out
    assert (tmp_path / "rel.md").exists()


def test_item_fora_com_preco_cheio_e_conta_no_total_nao_e_divergencia():
    cat, conv = cenario_from_dict(json.load(open(CENARIO, encoding="utf-8")))
    itens = _farol("itens")
    _item(itens, 304, 104)["receita_item_total"] = 12.0  # preço cheio (2 × 6,00), mas conta_no_total = false
    assert cf.conferir_itens(cat, conv, itens["dados"], 0.01, False) == []
    _item(itens, 304, 104)["receita_item_total"] = 9.0
    divs = cf.conferir_itens(cat, conv, itens["dados"], 0.01, False)
    assert [(d.campo, d.lido) for d in divs] == [("receita_item_total", 9.0)]


def test_itens_campos_reais_de_servico_e_quantidade():
    cat, conv = cenario_from_dict(json.load(open(CENARIO, encoding="utf-8")))
    itens = _farol("itens")
    for i in itens["dados"]:
        if i["servico_raiz_id"] == 302:
            i["receita_total_servico"] = 100.0
    _item(itens, 303, 102)["receita_unitaria"] = 1.5  # preço de casa em vez do convertido
    _item(itens, 303, 102)["quantidade_efetiva"] = 3
    _item(itens, 303, 102)["utiliza_no_convenio"] = False
    divs = {(d.servico.split("]")[0], d.campo): d for d in cf.conferir_itens(cat, conv, itens["dados"], 0.01, False)}
    assert divs[("[302", "receita_total_servico")].previsto == 121.0
    assert divs[("[303", "receita_unitaria")].previsto == 2.0
    assert "CONVERTIDO" in divs[("[303", "receita_unitaria")].nota
    assert ("[303", "quantidade_efetiva") in divs and ("[303", "utiliza_no_convenio") in divs


def test_itens_formato_antigo_do_swagger_continua_aceito():
    """Compatibilidade: receita/custo/utiliza/farol (nomes do Swagger) sem os campos reais."""
    cat, conv = cenario_from_dict(json.load(open(CENARIO, encoding="utf-8")))
    antigos = []
    for i in _farol("itens")["dados"]:
        antigos.append({"servico_raiz_id": i["servico_raiz_id"], "item_tipo": i["item_tipo"], "item_id": i["item_id"],
                        "item_nome": i["item_nome"], "receita": i["receita_item_total"],
                        "custo": i["custo_item_total"], "utiliza": i["utiliza_no_convenio"]})
    assert cf.conferir_itens(cat, conv, antigos, 0.01, False) == []
    next(a for a in antigos if a["servico_raiz_id"] == 304 and a["item_id"] == 104)["receita"] = 12.0
    divs = cf.conferir_itens(cat, conv, antigos, 0.01, False)
    assert len(divs) == 1 and "a API mostra o preço do item" in divs[0].nota


def test_produtos_campos_reais():
    cat, conv = cenario_from_dict(json.load(open(CENARIO, encoding="utf-8")))
    prods = _farol("produtos")
    assert cf.conferir_produtos(cat, conv, prods["dados"], 0.01, False) == []
    p104 = next(p for p in prods["dados"] if p["produto_id"] == 104)
    assert p104["zerar_valor"] and p104["receita"] == 0.0 and p104["receita_sem_zerar"] == 6.0
    p101 = next(p for p in prods["dados"] if p["produto_id"] == 101)
    p101["receita_sem_zerar"] = p101["receita"] = 50.0
    p101["fonte_nome"] = "PRECO FIXO CADASTRADO"
    p101["fator_k"] = 0
    divs = {d.campo: d for d in cf.conferir_produtos(cat, conv, prods["dados"], 0.01, False)}
    assert set(divs) >= {"receita", "receita_sem_zerar", "fonte_nome", "fator_k"}
    assert "origem_receita=" in divs["receita"].nota and "previsão: FONTE" in divs["receita"].nota


def test_servicos_campos_reais_por_tipo():
    cat, conv = cenario_from_dict(json.load(open(CENARIO, encoding="utf-8")))
    serv = _farol("servicos")
    s303 = next(s for s in serv["dados"] if s["servico_id"] == 303)
    assert (s303["receita_produtos"], s303["receita_servicos"], s303["receita_taxas"]) == (61.0, 80.0, 35.0)  # 80 + 61 + 35 = 176
    s303["receita_produtos"] = 0.0
    s303["somar_itens"] = False
    divs = {d.campo for d in cf.conferir_servicos(cat, conv, [s303], 0.01, False)}
    assert divs == {"receita_produtos", "somar_itens"}


def test_conferir_ignora_inativos(tmp_path):
    cat, conv = cenario_from_dict(json.load(open(CENARIO, encoding="utf-8")))
    api = [{"servico_id": 305, "servico": "Serviço antigo (inativo)", "receita_total": 999, "servico_ativo": False}]
    assert cf.conferir_servicos(cat, conv, api, 0.01, True) == []
    assert cf.conferir_servicos(cat, conv, api, 0.01, False)


# Nomes de campo das abas do convênio na resposta REAL de produção (GET medido em 25/09/2026).
LEITURA_REAL_ABAS = {
    "servicos": {"ativo", "autorizacaoPrevia", "codigo", "codigoConvenio", "codigoTuss", "descricaoConvenio", "id",
                 "kitDocumentoId", "nomeConversao", "pacote", "parcelasMaximas", "retornoServico", "servicoId",
                 "tabela87ANSId", "tipoAtendimentoId", "tipoCodigoId", "utiliza", "valorInternoConvenio", "zerarValor"},
    "produtos": {"codigo", "codigoConversao", "codigoTiss", "codigoTuss", "descricaoConversao", "fatorK",
                 "fontePrecoCompraOptionsId", "id", "nomeConversao", "parcelasMaximas", "produtoId", "tabela87ANSId",
                 "tipoCodigoId", "tipoPrecificacao", "utiliza", "valorUnitarioConversao", "zerarValor"},
    "taxas": {"codigo", "codigoTabelaConversao", "descricaoConversaoTabela", "descricaoConvertida", "id",
              "nomeConvertido", "tabela87ANSId", "taxaId", "tipoCodigoId", "tipoTaxaId", "utiliza", "valorConvertido",
              "zerarValor"},
}


def test_mapa_usa_os_nomes_da_leitura_real_das_abas():
    for tipo, mapa in mc.MAPA.items():
        reais = LEITURA_REAL_ABAS[mc.ABA[tipo]]
        for campo in list(mapa.values()) + [mc.CHAVE_ID[tipo]]:
            assert campo in reais, f"{tipo}.{campo} não aparece no GET real de /convenios/{{id}}/{mc.ABA[tipo]}"
