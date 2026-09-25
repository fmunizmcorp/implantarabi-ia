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


def test_conferir_aponta_divergencias(tmp_path, capsys):
    serv = json.load(open(os.path.join(EX, "farol-servicos-convenio-a.json"), encoding="utf-8"))
    itens = json.load(open(os.path.join(EX, "farol-itens-convenio-a.json"), encoding="utf-8"))
    serv = copy.deepcopy(serv)
    for s in serv["dados"]:
        if s["servico_id"] == 303:
            s["receita_total"] = 121.0  # medicamento ficou fora (ex.: faltou Utiliza)
    for i in itens["dados"]:
        if i["servico_raiz_id"] == 304 and i["item_id"] == 104:
            i["receita"] = 12.0  # tela mostra o preço do item zerado
    itens["dados"] = [i for i in itens["dados"] if not (i["servico_raiz_id"] == 303 and i["item_id"] == 101)]
    rc = cf.main([CENARIO, "--servicos", _arq(tmp_path, "s.json", serv), "--itens", _arq(tmp_path, "i.json", itens),
                  "--saida", str(tmp_path / "rel.md")])
    out = capsys.readouterr().out
    assert rc == 1
    assert "| [303] Medicamento Exemplo aplicado | (serviço) | receita_total | 176.0 | 121.0 |" in out
    assert "(ausente na API)" in out
    assert "a API mostra o preço do item" in out
    assert (tmp_path / "rel.md").exists()


def test_conferir_ignora_inativos(tmp_path):
    cat, conv = cenario_from_dict(json.load(open(CENARIO, encoding="utf-8")))
    api = [{"servico_id": 305, "servico": "Serviço antigo (inativo)", "receita_total": 999, "servico_ativo": False}]
    assert cf.conferir_servicos(cat, conv, api, 0.01, True) == []
    assert cf.conferir_servicos(cat, conv, api, 0.01, False)
