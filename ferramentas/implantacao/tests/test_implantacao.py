from pathlib import Path

from ferramentas.implantacao import checklist, painel, fila_perguntas, importar_planilha as imp

SPRINT = """# S05 — Taxas

| # | item | status | origem | prova | observação |
|---|---|---|---|---|---|
| 1 | Taxa de sala | conferido | contrato p.3 | provas/S05/x | |
| 2 | Taxa de material | coletado | tabela A l.12 | | |
| 3 | Tipo de taxa | pendente | | | padrão: Taxa Própria |
| 4 | Taxa antiga | n/a | | | |
"""


def _repo(tmp: Path) -> Path:
    (tmp / "sprints").mkdir()
    (tmp / "sprints" / "S05-taxas.md").write_text(SPRINT, encoding="utf-8")
    (tmp / "ESTADO.md").write_text("# ESTADO\n\n<!-- PAINEL:INICIO -->\nvelho\n<!-- PAINEL:FIM -->\nfim\n", encoding="utf-8")
    return tmp


def test_percentual_e_situacao(tmp_path):
    s = checklist.ler_sprints(_repo(tmp_path))[0]
    assert s.codigo == "S05" and len(s.itens) == 4
    assert s.percentual == round(100 * (1 + 0.25 + 0) / 3)
    assert s.situacao == "em andamento"


def test_painel_substitui_so_o_bloco(tmp_path):
    repo = _repo(tmp_path)
    painel.main(["--repo", str(repo)])
    txt = (repo / "ESTADO.md").read_text(encoding="utf-8")
    assert "velho" not in txt and txt.endswith("fim\n") and "S05" in txt


def test_fila_prioriza_confirmar_e_sugere_padrao(tmp_path):
    repo = _repo(tmp_path)
    fila = fila_perguntas.proximas(repo, "S05", todas=True)
    assert fila[0][1] == "CONFIRMAR"
    assert fila[1][1] == "SUGERIR PADRÃO" and fila[1][3] == "Taxa Própria"


def test_validadores():
    assert imp.cpf_valido("529.982.247-25")
    assert not imp.cpf_valido("111.111.111-11")
    assert imp.cnpj_valido("11.222.333/0001-81")
    assert imp.normalizar_valor("valor", "R$ 1.234,56") == ("1234.56", "")
    assert imp.normalizar_valor("dataDeNascimento", "05/03/1980")[0] == "1980-03-05"


def test_importar_planilha(tmp_path):
    ent = tmp_path / "antigo.csv"
    ent.write_text("Nome;CPF;Celular;CRM\nAna Exemplo;529.982.247-25;(11) 91234-5678;12345\nAna Exemplo;52998224725;;\n", encoding="utf-8")
    cab, _ = imp.ler_tabela(ent)
    mapa = imp.sugerir_mapa(cab, "colaboradores")
    assert mapa["CPF"] == "cpf" and mapa["Celular"] == "celular" and mapa["CRM"] == "numeroConselho"
    sai = tmp_path / "out.csv"
    r = imp.aplicar(ent, mapa, "colaboradores", sai)
    assert r["linhas"] == 2 and r["duplicados"] == 1
    assert "antigo.csv:linha 2" in sai.read_text(encoding="utf-8")
