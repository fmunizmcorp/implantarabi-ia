import json
from pathlib import Path

from ferramentas.implantacao import carga


class ClienteFalso:
    base = "http://falso"
    validade = None

    def __init__(self, existentes):
        self.db = list(existentes)
        self.ultima_leitura = {}
        self.chamadas = []

    def ler_tudo(self, caminho, params=None):
        self.ultima_leitura = {"lidos": len(self.db)}
        return list(self.db)

    def get(self, caminho, params=None):
        i = int(caminho.rsplit("/", 1)[1])
        return next(x for x in self.db if x["id"] == i)

    def enviar_lote(self, caminho, chave, itens, tamanho):
        self.chamadas.append(("bulk", caminho, len(itens)))
        for it in itens:
            self.db.append({**it, "id": 100 + len(self.db), "ativo": True})
        return {"enviados": len(itens), "ok": len(itens), "erros": [], "nao_processados": [],
                "resultados": [], "lotes": [], "reenviar": []}

    def put(self, caminho, corpo):
        self.chamadas.append(("put", caminho, corpo))
        i = int(caminho.rsplit("/", 1)[1])
        for n, x in enumerate(self.db):
            if x["id"] == i:
                self.db[n] = corpo
        return corpo


def test_previa_e_gravar(tmp_path, monkeypatch):
    cli = ClienteFalso([{"id": 1, "taxas": "Taxa de sala", "codigoTaxa": "T1", "valor": 10.0, "ativo": True}])
    ent = tmp_path / "taxas.csv"
    ent.write_text("taxas;codigoTaxa;valor;origem\nTaxa de sala;T1;12,50;contrato p.2\n"
                   "Taxa de material;T2;5;contrato p.2\nSem fonte;T3;1;\n", encoding="utf-8")
    plano_arq = carga.previa(cli, "taxas", ent, "codigoTaxa", "S05", tmp_path)
    plano = json.loads(plano_arq.read_text(encoding="utf-8"))
    assert len(plano["criar"]) == 1 and len(plano["alterar"]) == 1 and len(plano["sem_origem"]) == 1
    assert "SEM ORIGEM" in (plano_arq.parent / "previa.md").read_text(encoding="utf-8")
    cod = carga.gravar(cli, plano_arq, "teste", apenas_primeiro=False, incluir_alteracoes=True, lgpd_ciente=False)
    assert cod == 0
    assert ("bulk", "/taxas/bulk", 1) in cli.chamadas
    put = [c for c in cli.chamadas if c[0] == "put"][0]
    assert put[2]["valor"] == 12.5 and put[2]["ativo"] is True  # objeto completo reenviado
    assert "origem" not in put[2]
    for f in ("antes.json", "resposta.json", "depois.json", "diff.txt"):
        assert (plano_arq.parent / f).exists()


def test_pacientes_exige_lgpd(tmp_path):
    p = tmp_path / "plano.json"
    p.write_text(json.dumps({"recurso": "pacientes", "pasta": str(tmp_path), "criar": [], "alterar": []}), encoding="utf-8")
    assert carga.gravar(ClienteFalso([]), p, "x", False, False, False) == 2


def _plano_alterar(tmp_path, recurso, id_, item, difs=None):
    (tmp_path / "antes.json").write_text(json.dumps({"dados": []}), encoding="utf-8")
    p = tmp_path / "plano.json"
    if difs is None:  # a prévia aprovou todos os campos do item
        difs = [[k, None, v] for k, v in item.items() if k != "origem"]
    p.write_text(json.dumps({"recurso": recurso, "pasta": str(tmp_path), "criar": [],
                             "alterar": [{"id": id_, "item": item, "difs": difs}]}), encoding="utf-8")
    return p


def test_alterar_servico_manda_so_o_que_muda(tmp_path):
    # PUT /servicos é parcial desde 01–02/10/2026: omitido mantém — vai só o valor
    cli = ClienteFalso([{"id": 46, "nome": "Consulta", "descricao": "Consulta", "valor": 250, "ativo": True}])
    p = _plano_alterar(tmp_path, "servicos", 46, {"valor": 40.0, "origem": "tabela p.1"})
    assert carga.gravar(cli, p, "teste", False, True, False) == 0
    put = [c for c in cli.chamadas if c[0] == "put"][0][2]
    assert put == {"valor": 40.0}


def test_alterar_servico_com_nome_de_leitura_nao_grava(tmp_path):
    cli = ClienteFalso([{"id": 46, "nome": "Consulta", "descricao": "Consulta", "valor": 250, "ativo": True}])
    p = _plano_alterar(tmp_path, "servicos", 46, {"somarItens": True, "origem": "tabela p.1"})
    assert carga.gravar(cli, p, "teste", False, True, False) == 2
    assert not [c for c in cli.chamadas if c[0] == "put"]
    resp = json.loads((tmp_path / "resposta.json").read_text(encoding="utf-8"))
    assert "somarItems" in resp["alteracoes"][0]["nao_gravado"]


def test_alterar_convenio_unidades_exige_conferencia(tmp_path):
    cli = ClienteFalso([{"id": 7, "nome": "Plano X", "unidadesIds": [1], "ativo": True}])
    p = _plano_alterar(tmp_path, "convenios", 7, {"unidadesIds": [1, 2], "origem": "contrato"})
    assert carga.gravar(cli, p, "teste", False, True, False) == 2
    assert not [c for c in cli.chamadas if c[0] == "put"]
    assert carga.gravar(cli, p, "teste", False, True, False, listas_conferidas=("unidadesIds",)) == 0
    assert [c for c in cli.chamadas if c[0] == "put"][0][2] == {"unidadesIds": [1, 2]}


def test_alterar_parcial_manda_so_o_que_a_previa_mostrou(tmp_path):
    # a prévia viu "nome" igual (só caixa diferente) e "valor" diferente: só "valor" pode ir
    cli = ClienteFalso([{"id": 46, "nome": "CONSULTA", "descricao": "Consulta", "valor": 250, "ativo": True}])
    p = _plano_alterar(tmp_path, "servicos", 46, {"nome": "consulta", "valor": 40.0, "origem": "tab"},
                       difs=[["valor", 250, 40.0]])
    assert carga.gravar(cli, p, "teste", False, True, False) == 0
    assert [c for c in cli.chamadas if c[0] == "put"][0][2] == {"valor": 40.0}


def test_alterar_parcial_sem_difs_nao_grava(tmp_path):
    cli = ClienteFalso([{"id": 46, "nome": "Consulta", "descricao": "Consulta", "valor": 250, "ativo": True}])
    p = _plano_alterar(tmp_path, "servicos", 46, {"valor": 250, "origem": "tab"}, difs=[])
    assert carga.gravar(cli, p, "teste", False, True, False) == 0
    assert not [c for c in cli.chamadas if c[0] == "put"]


def test_ler_entrada_mantem_codigos_como_texto(tmp_path):
    ent = tmp_path / "e.csv"
    ent.write_text("nome;codigoEAN;cpf;valor;quantidade;origem\nX;07891234567895;01234567890;12,5;3;doc\n",
                   encoding="utf-8")
    item = carga._ler_entrada(ent)[0]
    assert item["codigoEAN"] == "07891234567895" and item["cpf"] == "01234567890"
    assert item["valor"] == 12.5 and item["quantidade"] == 3
