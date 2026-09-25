"""Testes do cliente com um servidor HTTP falso local (http.server em thread). Sem rede externa."""
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import pytest

from ..cliente import (ChaveAusente, ChaveInvalida, ClienteRabi, ErroRabi, LeituraIncompleta,
                       SemPermissao, ler_chave_do_arquivo, mascarar, normalizar_envelope)
from ..foto import diff, foto
from .. import testar_chave

CHAVE = "rbk_" + "teste" * 6
ITENS = [{"id": i, "nome": f"Item {i}"} for i in range(1, 8)]  # 7 itens


def _pagina(page, size):
    ini = (page - 1) * size
    return ITENS[ini:ini + size]


class Estado:
    contagem = {}
    lotes = []


class Falso(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _enviar(self, status, corpo, headers=None):
        dados = b"" if corpo is None else (corpo if isinstance(corpo, bytes) else json.dumps(corpo).encode())
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("X-ApiKey-Expires-At", "2099-12-31T23:59:59.000Z")
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def _conta(self, rota):
        Estado.contagem[rota] = Estado.contagem.get(rota, 0) + 1
        return Estado.contagem[rota]

    def do_GET(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        rota = u.path.replace("/api/v1/integrations", "")
        page, size = int(q.get("page", 1)), int(q.get("pageSize", 50))
        if self.headers.get("Authorization") != f"Bearer {CHAVE}":
            return self._enviar(401, {"error": "Token não fornecido."})
        tp = -(-len(ITENS) // size)
        if rota == "/env/dados":
            return self._enviar(200, {"dados": _pagina(page, size), "page": page, "pageSize": size,
                                      "total": len(ITENS), "totalPages": tp})
        if rota == "/env/data-meta":
            return self._enviar(200, {"data": _pagina(page, size), "meta": {"total": len(ITENS), "totalPages": tp}})
        if rota == "/env/message-data":
            return self._enviar(200, {"message": "ok", "data": _pagina(page, size), "total": len(ITENS),
                                      "totalPages": tp})
        if rota == "/env/items":
            return self._enviar(200, {"items": _pagina(page, size), "total": len(ITENS), "page": page,
                                      "pageSize": size, "totalPages": tp})
        if rota == "/env/crua":
            return self._enviar(200, ITENS)
        if rota == "/env/mentirosa":  # anuncia total maior do que entrega
            return self._enviar(200, {"dados": _pagina(page, size), "page": page, "pageSize": size,
                                      "total": 99, "totalPages": tp})
        if rota == "/vazio":
            return self._enviar(200, None)
        if rota == "/proibido":
            return self._enviar(403, {"error": "Chave de API sem permissão para 'paciente:read'."})
        if rota == "/indisponivel":
            self._conta(rota)
            return self._enviar(503, {"error": "Não foi possível validar a chave de API."})
        if rota == "/ocupado":
            n = self._conta(rota)
            if n < 3:
                return self._enviar(429, {"error": "lote em andamento"})
            return self._enviar(200, {"dados": [], "page": 1, "pageSize": 50, "total": 0, "totalPages": 1})
        if rota == "/sempre-ocupado":
            self._conta(rota)
            return self._enviar(429, {"error": "lote em andamento"})
        if rota == "/agendamentos/motivo-cancelamento":
            return self._enviar(200, 401)
        if rota == "/atendimentos/historico":
            return self._enviar(400, {"error": "Informe pacienteId."})
        if rota == "/pacientes":
            return self._enviar(200, {"dados": [{"id": 1, "nome": "Paciente Ficticio", "cpf": "000"}],
                                      "page": 1, "pageSize": 1, "total": 1, "totalPages": 1})
        if rota.startswith("/"):
            return self._enviar(200, {"dados": [], "page": 1, "pageSize": 1, "total": 0, "totalPages": 1})

    def do_POST(self):
        tam = int(self.headers.get("Content-Length", 0))
        corpo = json.loads(self.rfile.read(tam) or b"{}")
        rota = urlparse(self.path).path.replace("/api/v1/integrations", "")
        Estado.lotes.append(corpo)
        if rota == "/produtos/bulk":
            res = []
            for i, it in enumerate(corpo["produtos"]):
                if it.get("nome") == "ruim":
                    res.append({"indice": i, "status": "ERRO", "erro": "fabricanteId 99 não encontrado"})
                elif it.get("nome") == "lento":
                    res.append({"indice": i, "status": "NAO_PROCESSADO"})
                else:
                    res.append({"indice": i, "status": "CRIADO", "id": 500 + i})
            falhas = sum(1 for r in res if r["status"] != "CRIADO")
            return self._enviar(207 if falhas else 201, {"total": len(res), "criados": len(res) - falhas,
                                                        "falhas": falhas, "resultados": res})
        if rota == "/parametros/desconto/colaborador/7":
            return self._enviar(401, {"error": "Não autorizado"})
        if rota == "/grande/bulk":
            return self._enviar(400, {"error": "Lote acima do limite"})
        return self._enviar(201, {"id": 1})


@pytest.fixture(scope="module")
def servidor():
    srv = ThreadingHTTPServer(("127.0.0.1", 0), Falso)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    yield f"http://127.0.0.1:{srv.server_address[1]}/api/v1/integrations"
    srv.shutdown()


@pytest.fixture
def cli(servidor):
    Estado.contagem.clear()
    Estado.lotes.clear()
    return ClienteRabi(servidor, CHAVE, esperas_429=(0, 0, 0), esperas_503=(0,))


# ------------------------------------------------------------------ envelopes e paginação

@pytest.mark.parametrize("rota,formato", [
    ("/env/dados", "dados"), ("/env/data-meta", "data+meta"), ("/env/message-data", "message+data"),
    ("/env/items", "items"), ("/env/crua", "lista crua")])
def test_ler_tudo_normaliza_envelopes_e_pagina(cli, rota, formato):
    itens = cli.ler_tudo(rota, page_size=3)
    assert [x["id"] for x in itens] == list(range(1, 8))
    assert cli.ultima_leitura["formato"] == formato
    assert cli.ultima_leitura["lidos"] == 7


def test_paginacao_percorre_ate_total_pages(cli):
    cli.ler_tudo("/env/dados", page_size=2)
    assert cli.ultima_leitura["paginas"] == 4


def test_total_divergente_gera_leitura_incompleta(cli):
    with pytest.raises(LeituraIncompleta):
        cli.ler_tudo("/env/mentirosa", page_size=50)
    assert len(cli.ler_tudo("/env/mentirosa", page_size=50, conferir_total=False)) == 7


def test_normalizar_envelope_formato_desconhecido():
    with pytest.raises(ErroRabi):
        normalizar_envelope({"qualquer": 1})


# ------------------------------------------------------------------ erros

def test_corpo_vazio_e_leitura_falha(cli):
    with pytest.raises(ErroRabi, match="vazia"):
        cli.get("/vazio")


def test_401_chave_invalida_sem_repetir(servidor):
    c = ClienteRabi(servidor, "rbk_" + "errada" * 5, esperas_503=(0,))
    with pytest.raises(ChaveInvalida) as e:
        c.get("/env/dados")
    assert e.value.status == 401
    assert "errada" * 5 not in str(e.value)  # nunca vaza a chave


def test_403_sem_permissao_indica_permissao(cli):
    with pytest.raises(SemPermissao, match="paciente:read"):
        cli.get("/proibido")


def test_503_uma_nova_tentativa_e_depois_chave_invalida(cli):
    with pytest.raises(ChaveInvalida) as e:
        cli.get("/indisponivel")
    assert e.value.status == 503
    assert Estado.contagem["/indisponivel"] == 2  # 1 chamada + 1 nova tentativa, sem loop


def test_429_espera_e_tenta_de_novo(cli):
    assert cli.ler_tudo("/ocupado") == []
    assert Estado.contagem["/ocupado"] == 3


def test_429_desiste_depois_de_3_tentativas(cli):
    with pytest.raises(ErroRabi) as e:
        cli.get("/sempre-ocupado")
    assert e.value.status == 429
    assert Estado.contagem["/sempre-ocupado"] == 4  # 1 + 3 novas tentativas


def test_guarda_validade_da_chave(cli):
    cli.get("/env/dados")
    assert cli.validade.startswith("2099-12-31")
    assert cli.dias_restantes() > 15


# ------------------------------------------------------------------ lotes 207

def test_enviar_lote_trata_207_por_indice(cli):
    itens = [{"nome": f"p{i}"} for i in range(5)] + [{"nome": "ruim"}, {"nome": "p6"}, {"nome": "lento"}]
    rel = cli.enviar_lote("/produtos/bulk", "produtos", itens, tamanho=3)
    assert [len(l["produtos"]) for l in Estado.lotes] == [3, 3, 2]
    assert rel["enviados"] == 8 and rel["ok"] == 6
    assert [e["indice_global"] for e in rel["erros"]] == [5]
    assert [e["indice_global"] for e in rel["nao_processados"]] == [7]
    assert rel["reenviar"] == [{"nome": "ruim"}, {"nome": "lento"}]
    assert [l["status"] for l in rel["lotes"]] == [201, 207, 207]


def test_enviar_lote_4xx_levanta_com_relatorio(cli):
    with pytest.raises(ErroRabi) as e:
        cli.enviar_lote("/grande/bulk", "itens", [{"a": 1}], tamanho=50)
    assert e.value.relatorio["lotes"][0]["status"] == 400


# ------------------------------------------------------------------ chave

def test_chave_do_arquivo_e_mascara(tmp_path, monkeypatch):
    monkeypatch.delenv("RABI_API_KEY", raising=False)
    (tmp_path / "credenciais").mkdir()
    (tmp_path / "credenciais" / "rabi-api-externa.md").write_text(
        f"# Chave\n\n- base: https://exemplo\n- api_key: {CHAVE}\n", encoding="utf-8")
    chave, arq = ler_chave_do_arquivo(str(tmp_path))
    assert chave == CHAVE and arq.endswith("rabi-api-externa.md")
    c = ClienteRabi("http://127.0.0.1:1", raiz=str(tmp_path))
    assert CHAVE not in repr(c) and mascarar(CHAVE) in repr(c)


def test_env_tem_prioridade_sobre_arquivo(tmp_path, monkeypatch):
    monkeypatch.setenv("RABI_API_KEY", "rbk_" + "doambiente" * 3)
    (tmp_path / "credenciais").mkdir()
    (tmp_path / "credenciais" / "rabi-api-externa.md").write_text(f"api_key: {CHAVE}\n", encoding="utf-8")
    c = ClienteRabi("http://127.0.0.1:1", raiz=str(tmp_path))
    assert c.origem_chave.startswith("variável de ambiente")


def test_sem_chave_erro_claro(tmp_path, monkeypatch):
    monkeypatch.delenv("RABI_API_KEY", raising=False)
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ChaveAusente, match="RABI_API_KEY"):
        ClienteRabi("http://127.0.0.1:1", raiz=str(tmp_path))


# ------------------------------------------------------------------ foto, diff, testar_chave

def test_foto_mascara_pii_e_diff(cli, tmp_path):
    arq = foto(cli, "/pacientes", str(tmp_path), "antes")
    dados = json.load(open(arq, encoding="utf-8"))
    assert dados["dados"][0]["cpf"] == "***" and dados["dados"][0]["nome"] == "***"
    assert CHAVE not in open(arq, encoding="utf-8").read()
    antes = {"dados": [{"id": 1, "valor": None, "utiliza": False}, {"id": 2, "valor": 10}]}
    depois = {"dados": [{"id": 1, "valor": 0, "utiliza": True}, {"id": 3, "valor": 5}]}
    txt = diff(antes, depois)
    assert "~ [id=1].valor: null → 0" in txt
    assert "~ [id=1].utiliza: false → true" in txt
    assert "- [id=2] (sumiu)" in txt and "+ [id=3] (novo)" in txt


def test_testar_chave_tabela_sem_dados(cli):
    res = testar_chave.testar(cli)
    assert len(res["linhas"]) == 25
    md = testar_chave.relatorio_md(res)
    assert "Paciente Ficticio" not in md and CHAVE not in md
    linha_atend = [l for l in res["linhas"] if l[0] == "Atendimentos"][0]
    assert linha_atend[3] == "OK (validação)"


def test_401_de_rota_com_defeito_nao_e_chave(cli):
    with pytest.raises(ErroRabi) as e:
        cli.post("/parametros/desconto/colaborador/7", params={"nivel": "NIVEL1"})
    assert not isinstance(e.value, ChaveInvalida)
    assert "defeito conhecido" in str(e.value)


def test_corpo_401_disfarcado_em_200(cli):
    with pytest.raises(ErroRabi, match="disfarçado"):
        cli.get("/agendamentos/motivo-cancelamento")


def _porta_livre():
    import socket
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def test_testar_chave_para_no_primeiro_erro_de_conexao():
    base = f"http://127.0.0.1:{_porta_livre()}/api/v1/integrations"  # ninguém escuta: conexão recusada
    c = ClienteRabi(base, CHAVE, esperas_429=(), esperas_503=(), timeout=5)
    res = testar_chave.testar(c)
    assert res["parou"] == "conexão"
    assert len(res["linhas"]) == 1 and res["linhas"][0][3] == "SEM CONEXÃO"
    assert "sem conexão com a API" in testar_chave.relatorio_md(res)


def test_testar_chave_codigo_de_saida(monkeypatch, servidor):
    base = f"http://127.0.0.1:{_porta_livre()}/api/v1/integrations"
    monkeypatch.setenv("RABI_API_KEY", CHAVE)
    assert testar_chave.main(["--base", base]) == 1          # sem conexão: 0 de 25 áreas
    Estado.contagem.clear()
    assert testar_chave.main(["--base", servidor]) == 0      # servidor falso: áreas OK
    monkeypatch.setenv("RABI_API_KEY", "rbk_" + "errada" * 5)
    assert testar_chave.main(["--base", servidor]) == 1      # 401: parou na chave
