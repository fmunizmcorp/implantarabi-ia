import json
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


def test_uf_do_conselho_ganha_de_uf_e_sigla_preenche_conselho(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "dados").mkdir()
    ent = tmp_path / "dados" / "equipe.csv"
    ent.write_text("Nome;UF CRM;UF;CRM;E-mail\nAna Exemplo;sp;RJ;12345;ana@exemplo.com.br\n"
                   "Bia Exemplo;SP;SP;999;bia-sem-arroba\n", encoding="utf-8")
    cab, _ = imp.ler_tabela(ent)
    mapa, notas = imp.sugerir_mapa_detalhado(cab, "colaboradores")
    assert mapa["UF CRM"] == "ufConselho" and mapa["UF"] == "uf" and mapa["CRM"] == "numeroConselho"
    assert notas["UF CRM"] == 1.0
    sai = tmp_path / "out.csv"
    imp.aplicar(ent, mapa, "colaboradores", sai)
    import csv
    linhas = list(csv.DictReader(sai.open(encoding="utf-8"), delimiter=";"))
    assert linhas[0]["conselho"] == "CRM" and linhas[0]["numeroConselho"] == "12345"
    assert linhas[0]["ufConselho"] == "sp" and linhas[0]["uf"] == "RJ"
    assert linhas[0]["origem"] == "dados/equipe.csv:linha 2"   # caminho relativo ao cwd
    assert "e-mail em formato inválido" in linhas[1]["avisos"]
    assert linhas[0]["avisos"] == ""


def test_sigla_de_outros_conselhos_e_uf_do_conselho():
    for cab, sigla in (("CRO", "CRO"), ("Nº COREN", "COREN"), ("crefito", "CREFITO"), ("CRN", "CRN"), ("CRP", "CRP")):
        assert imp.sigla_conselho(cab) == sigla
        assert imp.sugerir_mapa([cab], "colaboradores")[cab] == "numeroConselho"
    assert imp.sigla_conselho("UF CRM") is None
    for cab in ("uf conselho", "UF do Conselho", "UF do CRM"):
        assert imp.sugerir_mapa([cab, "UF"], "colaboradores")[cab] == "ufConselho"


def test_mapa_novo_com_incerto_e_mapa_antigo(tmp_path, capsys):
    ent = tmp_path / "x.csv"
    ent.write_text("Nome;Registro prof;CPF\nAna Exemplo;123;529.982.247-25\n", encoding="utf-8")
    mapa_json = tmp_path / "mapa.json"
    assert imp.main(["sugerir", "--entrada", str(ent), "--alvo", "colaboradores", "--mapa", str(mapa_json)]) == 0
    doc = json.loads(mapa_json.read_text(encoding="utf-8"))
    assert "incertos" in doc and isinstance(doc["incertos"], list)
    # formato novo {"campo":..,"incerto":true} também é aceito em aplicar
    novo = {"alvo": "colaboradores", "mapa": {"Nome": "nome", "Registro prof": {"campo": "numeroConselho", "incerto": True},
                                              "CPF": {"campo": "cpf"}}}
    mapa_json.write_text(json.dumps(novo), encoding="utf-8")
    sai = tmp_path / "o.csv"
    assert imp.main(["aplicar", "--entrada", str(ent), "--mapa", str(mapa_json), "--saida", str(sai)]) == 0
    texto = sai.read_text(encoding="utf-8")
    assert "123" in texto and "52998224725" in texto
    assert "x.csv:linha 2" in texto   # fora do cwd: cai para o nome do arquivo


def test_sugerir_marca_incerto_com_interrogacao(tmp_path, capsys):
    ent = tmp_path / "y.csv"
    ent.write_text("Nome;Nascim\nAna Exemplo;01/02/1980\n", encoding="utf-8")
    mapa, notas = imp.sugerir_mapa_detalhado(["Nome", "Nascim"], "colaboradores")
    assert mapa["Nascim"] == "dataDeNascimento" and notas["Nascim"] < imp.NOTA_CERTA
    mj = tmp_path / "m.json"
    imp.main(["sugerir", "--entrada", str(ent), "--alvo", "colaboradores", "--mapa", str(mj)])
    saida = capsys.readouterr().out
    assert "dataDeNascimento ?" in saida and "Confirme com o usuário" in saida
    assert json.loads(mj.read_text(encoding="utf-8"))["incertos"] == ["Nascim"]
