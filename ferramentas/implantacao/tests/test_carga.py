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
