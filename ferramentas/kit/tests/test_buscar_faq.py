"""Testes do FAQ das IAs (busca por sintoma) e da dica no erro do cliente."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "rabi_api"))

import buscar_faq as bf  # noqa: E402
import cliente  # noqa: E402


def _ids(achados):
    return [e["id"] for _, e in achados]


def test_filter_500_leva_a_f001():
    a = bf.buscar("Cannot read properties of undefined (reading 'filter')", 500, "POST /servicos")
    assert _ids(a)[0] == "F001"


def test_400_generico_leva_a_f002():
    a = bf.buscar("Erro ao processar a operação. Tente novamente em instantes.", 400, "GET /servicos/1")
    assert "F002" in _ids(a)


def test_chave_503_leva_a_f003():
    assert _ids(bf.buscar("Não foi possível validar a chave de API.", 503))[0] == "F003"


def test_sem_sintoma_conhecido_nao_inventa():
    assert bf.buscar("mensagem que ninguém viu", 418, "GET /xyz") == []
    assert bf.main(["mensagem que ninguém viu", "--status", "418"]) == 1


def test_toda_entrada_tem_cabecalho_de_busca_e_esta_no_indice():
    indice = (bf.PASTA / "00-INDICE.md").read_text(encoding="utf-8")
    entradas = bf.carregar()
    assert entradas
    for e in entradas:
        assert e["status"] or e["mensagens"], e["id"]
        assert e["arquivo"].name in indice, f"{e['id']} fora do índice"


def test_erro_do_cliente_sugere_o_faq():
    dica = cliente._dica_faq("Cannot read properties of undefined (reading 'filter')", 500, "POST /servicos")
    assert "F001" in dica
    assert cliente._dica_faq("nada", 418, "GET /x") == ""
