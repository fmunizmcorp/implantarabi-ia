"""Testes das ferramentas de referências com fixtures pequenas e FICTÍCIAS.

Nenhum dado real: laboratórios "LAB EXEMPLO"/"FABRICA TESTE", códigos inventados.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from ferramentas.referencias import comum, normalizar
from ferramentas.referencias.buscar import buscar
from ferramentas.referencias.enriquecer_produtos import enriquecer_arquivo, enriquecer_item

EAN_DIP = "7890000000011"
REG_DIP = "1000000000011"
TUSS_DIP = "90000011"


def _bras23(lab, codlab, codprod, nome, codap, apres, pmc, pf, qtd, pmcu, pfu, ed, gen, ean, tiss, tuss, ggrem, reg):
    return [codlab, lab, codprod, nome, codap, apres, pmc, pf, qtd, "PMC", pmcu, "PFB", pfu, ed, "0.00", "S",
            ean, tiss, gen, tuss, ggrem, reg, "3261"]


def _grava_latin1(caminho: Path, linhas):
    with open(caminho, "w", encoding="latin-1", newline="") as f:
        csv.writer(f, quoting=csv.QUOTE_ALL).writerows(linhas)


@pytest.fixture()
def brutos(tmp_path: Path) -> Path:
    d = tmp_path / "brutos"
    d.mkdir()
    # Brasíndice "novo" (19 colunas) e "anterior"/"complementar" (23 colunas)
    novo = [
        ["900", "LAB EXEMPLO", "00001", "DIPIRONA - GENERICO", "AAAA", "500 mg cx. 30 cprs.", "30.00", "22.00", "30",
         "PMC", "1.00", "PFB", "0.73", "1100", "0.00", "N", EAN_DIP, "0000000001", TUSS_DIP],
        ["900", "LAB EXEMPLO", "00001", "DIPIRONA - GENERICO", "BBBB", "500 mg/ml sol. or. fr. x 20 ml", "12.00", "9.00",
         "1", "PMC", "12.00", "PFB", "9.00", "1100", "0.00", "N", "7890000000028", "0000000002", "90000028"],
        ["901", "FABRICA TESTE", "00002", "ANALGEX (Restrito Hosp.)", "CCCC", "1 g inj. cx. 50 amp. x 2 ml", "0.00",
         "150.00", "50", "PMC", "0.00", "PFB", "3.00", "1099", "0.00", "S", "7890000000035", "0000000003", "90000035"],
    ]
    anterior = [
        _bras23("LAB EXEMPLO", "900", "00001", "DIPIRONA - GENERICO", "AAAA", "500 mg cx. 30 cprs.", "29.00", "21.00", "30",
                "0.97", "0.70", "1094", "S", EAN_DIP, "0000000001", TUSS_DIP, "111111111111111", REG_DIP),
        _bras23("LAB EXEMPLO", "900", "00009", "PRODUTO DESCONTINUADO", "ZZZZ", "10 mg cx. 10 cprs.", "5.00", "4.00", "10",
                "0.50", "0.40", "1090", "N", "7890000000099", "0000000009", "90000099", "", ""),
    ]
    complementar = anterior + [
        _bras23("FABRICA TESTE", "901", "00003", "OUTRO FARMACO EXEMPLO", "DDDD", "2 mg/ml sol. inj. fr. 10 ml", "0.00",
                "40.00", "1", "0.00", "40.00", "1094", "N", "7890000000042", "0000000004", "90000042", "", ""),
    ]
    _grava_latin1(d / "bras_novo.txt", novo)
    _grava_latin1(d / "bras_anterior.txt", anterior)
    _grava_latin1(d / "bras_compl.txt", complementar)
    _grava_latin1(d / "bras_mat.txt", [
        _bras23("FABRICA TESTE", "901", "00100", "SERINGA DESCARTAVEL EXEMPLO", "EEEE", "10 ml s/ agulha - un.", "0.00",
                "0.80", "1", "0.00", "0.80", "1094", "N", "7890000000059", "0000000100", "", "", ""),
    ])
    # SIMPRO (pipe), com uma linha de lixo e um código repetido
    (d / "simpro_mat.csv").write_text(
        "CODIGO|DESCRICAO|TIPO|CAPITULO|GRUPO|SUBGRUPO|VIGENCIA_ATUAL|ESPECIALIDADE|EXAME_COMPLEMENTAR|BENEFICIARIO_PERICIA_FINAL|OBSERVACAO\n"
        "0000000501|SERINGA 10ML S/AG. FABRICA TESTE.|Despesa - Material||||Desde 01/02/2024 R$  0,500|Todas|||\n"
        "0000000501|SERINGA 10ML S/AG. FABRICA TESTE.|Despesa - Material||||Desde 01/03/2025 R$ 0,550|Todas|||\n"
        "0000000502|SERINGA 20ML S/AG. FABRICA TESTE.|Despesa - Material||||Desde 01/03/2025 R$ 0,700|Todas|||\n"
        "[2] [01:50:33] [LOG]\n", encoding="utf-8")
    # CMED em CSV (caminho sem openpyxl): 2 linhas de título antes do cabeçalho
    aliq = ["0", "12", "17", "18", "19", "20", "21", "22"]
    cab = (["SUBSTÂNCIA", "CNPJ", "LABORATÓRIO", "CÓDIGO GGREM", "REGISTRO", "EAN 1", "EAN 2", "EAN 3", "PRODUTO",
            "APRESENTAÇÃO", "CLASSE TERAPÊUTICA", "TIPO DE PRODUTO (STATUS DO PRODUTO)", "REGIME DE PREÇO"]
           + [("PF 0%" if a == "0" else f"PF {a} %") for a in aliq] + [f"PMC {a} %" for a in aliq]
           + ["RESTRIÇÃO HOSPITALAR"])
    lin = (["DIPIRONA MONOIDRATADA", "00.000.000/0001-00", "LAB EXEMPLO LTDA", "111111111111111", REG_DIP, EAN_DIP,
            "-", "-", "DIPIRONA", "500 MG COM CT BL AL X 30", "N2B", "Genérico", "Regulado"]
           + ["21,00"] * 8 + ["29,00"] * 8 + ["Não"])
    with open(d / "cmed.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Secretaria Executiva - CMED"])
        w.writerow(["LISTA DE PREÇOS"])
        w.writerow(cab)
        w.writerow(lin)
    (d / "tuss_reg.csv").write_text(f"Código do Termo;REGISTRO ANVISA\n{TUSS_DIP};{REG_DIP}\n", encoding="utf-8")
    (d / "cbhpm.csv").write_text("CODIGO_TUSS;CODIGO_CBHPM;DESCRICAO;PORTE;CUSTO_OPERACIONAL_UCO;PAGINA\n"
                                 "10101012;1.01.01.01-2;Consulta em consultório;2B;;23\n", encoding="utf-8")
    return d


@pytest.fixture()
def refs(brutos: Path, tmp_path: Path) -> Path:
    s = str(tmp_path / "referencias")
    normalizar.main(["--saida", s, "cmed", "--pmc", str(brutos / "cmed.csv"), "--edicao", "20260101",
                     "--tuss-registros", str(brutos / "tuss_reg.csv")])
    normalizar.main(["--saida", s, "brasindice-medicamentos", "--principal", str(brutos / "bras_novo.txt"),
                     "--edicao", "1100", "--anterior", str(brutos / "bras_anterior.txt"),
                     "--complementar", str(brutos / "bras_compl.txt"), "--edicao-complementar", "1094"])
    normalizar.main(["--saida", s, "brasindice-materiais", "--principal", str(brutos / "bras_mat.txt"), "--edicao", "1094"])
    normalizar.main(["--saida", s, "simpro", "--tipo", "material", "--arquivo", str(brutos / "simpro_mat.csv"),
                     "--edicao", "2026-04-12"])
    normalizar.main(["--saida", s, "cbhpm", "--arquivo", str(brutos / "cbhpm.csv")])
    return Path(s)


def _linhas(refs: Path, conjunto: str):
    man = comum.carregar_manifest(refs)
    out = []
    for f in man["conjuntos"][conjunto]["fatias"]:
        out += list(comum.ler_fatia(refs / conjunto / f["arquivo"]))
    return out


# ------------------------------------------------------------------ normalização

def test_manifest_e_indices(refs: Path):
    man = json.loads((refs / "manifest.json").read_text(encoding="utf-8"))
    assert {"cmed/medicamentos", "brasindice/medicamentos", "simpro/material", "cbhpm/portes"} <= set(man["conjuntos"])
    for nome, meta in man["conjuntos"].items():
        assert (refs / nome / "00-INDICE.md").exists()
        for f in meta["fatias"]:
            p = refs / nome / f["arquivo"]
            assert p.stat().st_size == f["bytes"]
            assert comum.sha256_arquivo(p) == f["sha256"]
    assert (refs / "brasindice" / "00-INDICE.md").exists()


def test_brasindice_mescla_edicoes(refs: Path):
    rows = _linhas(refs, "brasindice/medicamentos")
    nomes = {r["produto"]: r for r in rows}
    assert "PRODUTO DESCONTINUADO" not in nomes              # saiu da edição nova
    assert nomes["OUTRO FARMACO EXEMPLO"]["edicao"] == "1094"  # só no complementar
    dip = [r for r in rows if r["ean"] == EAN_DIP][0]
    assert dip["edicao"] == "1100"
    assert dip["pf_unit"] == "0.73"                          # preço da edição nova
    assert dip["registro_anvisa"] == REG_DIP                  # veio da edição anterior
    assert dip["ggrem"] == "111111111111111"
    assert dip["generico"] == "S"
    assert dip["principio_ativo"] == "DIPIRONA MONOIDRATADA"  # veio da CMED pelo EAN
    assert dip["tabela_fonte"] == "05" and dip["tabela87_sugerida"] == "20"
    rest = nomes["ANALGEX (Restrito Hosp.)"]
    assert rest["restrito_hospitalar"] == "S"


def test_simpro_separa_vigencia_e_deduplica(refs: Path):
    rows = _linhas(refs, "simpro/material")
    assert len(rows) == 2
    s10 = [r for r in rows if r["codigo_fonte"] == "0000000501"][0]
    assert s10["vigencia"] == "2025-03-01" and s10["preco_ref"] == "0.55"
    assert s10["laboratorio"] == "FABRICA TESTE" and s10["produto"] == "SERINGA 10ML S/AG"
    assert s10["tabela_fonte"] == "12"


def test_cmed_csv_sem_openpyxl(refs: Path):
    r = _linhas(refs, "cmed/medicamentos")[0]
    assert r["codigo_tuss"] == TUSS_DIP and r["pf_total"] == "21" and "PF18=21" in r["precos_extra"]


def test_fatiamento_respeita_limite(tmp_path: Path):
    linhas = [[f"{l}PRODUTO {i}", "x" * 50] for l in "AAB" for i in range(200)]
    fatias = comum.gravar_fatiado(tmp_path / "c", ["produto", "extra"], linhas,
                                  lambda l: comum.normalizar_texto(l[0]), limite=110_000)
    assert all(f["bytes"] <= 110_000 for f in fatias)
    assert sum(f["linhas"] for f in fatias) == 600
    assert {f["prefixo"] for f in fatias} >= {"A", "B"} or any("-" in f["arquivo"] for f in fatias)


# ------------------------------------------------------------------ busca

def test_busca_nome_e_dose(refs: Path):
    res = buscar("dipirona 500 mg", raiz=refs, limite=5)
    assert res and res[0]["pontos"] >= 90
    assert "500 mg cx" in res[0]["apresentacao"] or res[0]["fonte"] == "CMED"
    # a solução 500 mg/ml não pode ficar à frente do comprimido de 500 mg
    ordem = [r["apresentacao"] for r in res]
    sol = [i for i, a in enumerate(ordem) if "ml" in a.lower()]
    cpr = [i for i, a in enumerate(ordem) if "cprs" in a.lower()]
    assert cpr and (not sol or min(cpr) < min(sol))


def test_busca_por_ean(refs: Path):
    res = buscar(EAN_DIP, raiz=refs)
    assert res and all(r["pontos"] == 100 for r in res)
    assert {r["fonte"] for r in res} == {"BRASINDICE", "CMED"}


def test_busca_por_tuss(refs: Path):
    res = buscar(TUSS_DIP, raiz=refs)
    assert res and res[0]["codigo_tuss"] == TUSS_DIP


def test_busca_por_registro_anvisa(refs: Path):
    res = buscar(REG_DIP, raiz=refs)
    assert res and res[0]["registro_anvisa"] == REG_DIP


def test_busca_material_e_cbhpm(refs: Path):
    res = buscar("seringa 10 ml", raiz=refs, limite=3)
    assert res[0]["pontos"] >= 90 and "10" in (res[0]["produto"] + res[0]["apresentacao"])
    assert all("20ML" not in r["produto"] for r in res[:2])
    proc = buscar("consulta consultorio", raiz=refs, fontes=["cbhpm"])
    assert proc and proc[0]["codigo_tuss"] == "10101012"


def test_referencias_da_clinica_prevalecem(refs: Path, tmp_path: Path):
    minha = tmp_path / "minhas"
    minha.mkdir()
    (minha / "tabela-propria.csv").write_text("nome;apresentacao;preco\nDIPIRONA 500 MG;cx 30 cprs;0,90\n", encoding="utf-8")
    res = buscar("dipirona 500 mg", raiz=refs, referencias_clinica=minha)
    assert res[0]["conjunto"].startswith("clinica/")


# ------------------------------------------------------------------ enriquecimento

def test_enriquecer_classifica(refs: Path, tmp_path: Path):
    entrada = tmp_path / "produtos.csv"
    entrada.write_text("nome;apresentacao;fabricante;codigo\n"
                       "Dipirona 500mg;cx 30 comprimidos;lab exemplo;\n"
                       "Qualquer coisa;;;" + EAN_DIP + "\n"
                       "Produto que nao existe zzz;;;\n", encoding="utf-8")
    saida = tmp_path / "cand.csv"
    cont = enriquecer_arquivo(entrada, saida, raiz=refs)
    rows = list(csv.DictReader(open(saida, encoding="utf-8"), delimiter=";"))
    por_item = {}
    for r in rows:
        por_item.setdefault(r["item"], []).append(r)
    assert por_item["1"][0]["classificacao"] == "ÓTIMO"
    assert por_item["1"][0]["principio_ativo"] == "DIPIRONA MONOIDRATADA" or por_item["1"][0]["fonte"] == "CMED"
    assert len(por_item["1"]) <= 3
    assert por_item["2"][0]["classificacao"] == "ÓTIMO" and "código exato" in por_item["2"][0]["motivo"]
    assert por_item["3"][0]["classificacao"] == "SEM MATCH"
    assert all(r["decisao"] == "" for r in rows)  # nunca decide sozinho
    assert cont["SEM MATCH"] == 1


def test_enriquecer_dose_diferente_vira_ressalva(refs: Path):
    c = enriquecer_item("DIPIRONA", "1 g cx 30 cprs", raiz=refs, tipo="medicamento")
    assert all(x["classificacao"] in ("RESSALVA", "SEM MATCH") for x in c)


def test_config_md_da_clinica(refs: Path, tmp_path: Path):
    repo = tmp_path / "repo-clinica"
    (repo / "config").mkdir(parents=True)
    (repo / "dados" / "referencias").mkdir(parents=True)
    (repo / "dados" / "referencias" / "brasindice-propria.csv").write_text(
        "produto;apresentacao;laboratorio;fonte;edicao\nDIPIRONA - GENERICO;500 mg cx. 30 cprs.;LAB EXEMPLO;BRASINDICE;9999\n",
        encoding="utf-8")
    md = repo / "config" / "referencias-da-clinica.md"
    md.write_text("| Tabela | Onde está (caminho no repo ou URL) | Edição |\n|---|---|---|\n"
                  "| Brasíndice | dados/referencias/brasindice-propria.csv | 9999 |\n| SIMPRO | | |\n", encoding="utf-8")
    res = buscar("dipirona 500 mg", raiz=refs, referencias_clinica=md)
    assert res[0]["conjunto"].startswith("clinica/") and res[0]["edicao"] == "9999"
