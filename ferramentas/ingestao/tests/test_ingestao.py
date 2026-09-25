"""Testes simples da ingestão (inventário e extração de texto)."""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import extrair_texto as et  # noqa: E402
import inventario as inv  # noqa: E402


@pytest.fixture
def repo(tmp_path):
    docs = tmp_path / "documentos-do-cliente"
    (docs / "recebidos" / "2026-10-01").mkdir(parents=True)
    (docs / "00-INDICE.md").write_text("# índice", encoding="utf-8")
    (docs / "inventario.md").write_text(
        "# Inventário\n\n| nº | arquivo | tipo | páginas | hash | recebido em | o que contém | dados extraídos → sprint | status lote |\n"
        "|---|---|---|---|---|---|---|---|---|\n",
        encoding="utf-8",
    )
    (docs / "fichas-de-extracao").mkdir()
    (docs / "fichas-de-extracao" / "_modelo-ficha.md").write_text("modelo", encoding="utf-8")
    (docs / "recebidos" / "2026-10-01" / "tabela-convenio-a.csv").write_text(
        "codigo;descricao;valor\n10101012;Consulta em consultório;150,00\n", encoding="utf-8"
    )
    (docs / "recebidos" / "2026-10-01" / "lista.txt").write_text("Dra. Ana Exemplo\n", encoding="utf-8")
    return tmp_path


def test_inventario_acrescenta_sem_duplicar(repo):
    novas = inv.inventariar(repo)
    assert len(novas) == 2
    texto = (repo / "documentos-do-cliente" / "inventario.md").read_text(encoding="utf-8")
    assert "recebidos/2026-10-01/tabela-convenio-a.csv" in texto
    assert "| 2026-10-01 |" in texto and "| CSV |" in texto
    assert inv.inventariar(repo) == []  # segunda vez: nada novo
    # cópia com outro nome e mesmo conteúdo não duplica
    orig = repo / "documentos-do-cliente" / "recebidos" / "2026-10-01" / "lista.txt"
    (orig.parent / "lista-copia.txt").write_bytes(orig.read_bytes())
    assert inv.inventariar(repo) == []
    # arquivo novo recebe o próximo nº
    (orig.parent / "novo.md").write_text("outro", encoding="utf-8")
    novas = inv.inventariar(repo)
    assert len(novas) == 1 and novas[0].startswith("| 3 |")


def test_inventario_simular_nao_grava(repo):
    antes = (repo / "documentos-do-cliente" / "inventario.md").read_text(encoding="utf-8")
    assert len(inv.inventariar(repo, simular=True)) == 2
    assert (repo / "documentos-do-cliente" / "inventario.md").read_text(encoding="utf-8") == antes


def test_extrair_csv_txt_e_indice(repo):
    assert et.main(["--repo", str(repo)]) == 0
    saida = repo / "documentos-do-cliente" / "texto-extraido"
    txts = sorted(saida.glob("*.txt"))
    assert len(txts) == 2
    conteudo = "".join(t.read_text(encoding="utf-8") for t in txts)
    assert "Consulta em consultório" in conteudo and "# origem:" in conteudo
    assert (saida / "00-INDICE.md").exists()
    # não refaz sem --forcar
    assert et.main(["--repo", str(repo)]) == 0
    assert len(list(saida.glob("*.txt"))) == 2


def test_extrair_docx_stdlib(tmp_path):
    p = tmp_path / "contrato.docx"
    with zipfile.ZipFile(p, "w") as z:
        z.writestr("word/document.xml",
                   "<w:document><w:body><w:p><w:r><w:t>Cláusula 5 prazo 30 dias</w:t></w:r></w:p></w:body></w:document>")
    texto, metodo = et.extrair(p)
    assert "Cláusula 5 prazo 30 dias" in texto and metodo.startswith("docx")


def test_extrair_xlsx_se_openpyxl(tmp_path):
    openpyxl = pytest.importorskip("openpyxl")
    wb = openpyxl.Workbook()
    wb.active.title = "Precos"
    wb.active.append(["codigo", "valor"])
    wb.active.append(["10101012", 150])
    p = tmp_path / "t.xlsx"
    wb.save(p)
    texto, _ = et.extrair(p)
    assert "aba: Precos" in texto and "10101012;150" in texto


def test_tipo_nao_suportado_avisa(tmp_path):
    p = tmp_path / "x.bin"
    p.write_bytes(b"\x00\x01")
    with pytest.raises(et.SemFerramenta):
        et.extrair(p)


def test_fatiar_respeita_limite():
    texto = "".join(f"linha {i} " + "x" * 50 + "\n" for i in range(200))
    fatias = et.fatiar(texto, limite=1000)
    assert len(fatias) > 1
    assert all(len(f.encode("utf-8")) <= 1000 for f in fatias)
    assert "".join(fatias) == texto


def test_gravar_em_partes(tmp_path):
    texto = "abc\n" * 1000
    arqs = et.gravar(tmp_path, "x.txt", "h" * 16, texto, "teste", limite=1500)
    assert len(arqs) > 1 and arqs[0].name.endswith("-parte-001.txt")
    assert all(a.stat().st_size <= 1500 + 200 for a in arqs)
