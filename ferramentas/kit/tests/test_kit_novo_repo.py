"""Testes do gerador de repo de clínica."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import novo_repo_clinica as nrc  # noqa: E402


def test_slugificar():
    assert nrc.slugificar("Clínica São João & Cia") == "clinica-sao-joao-cia"
    assert nrc.slugificar("!!!") == "clinica"


def test_gera_repo_com_placeholders_substituidos(tmp_path):
    destino = tmp_path / "clinica"
    assert nrc.main(["--destino", str(destino), "--clinica", "Clínica Exemplo", "--porte", "consultorio"]) == 0
    estado = (destino / "ESTADO.md").read_text(encoding="utf-8")
    assert "Clínica Exemplo" in estado
    assert "Consultório individual" in estado
    assert nrc.versao_kit() in estado
    assert "rabi-implantacao-clinica-exemplo" in estado
    for p in destino.rglob("*"):
        if p.is_file() and p.suffix in {".md", ".json", ".sh"}:
            t = p.read_text(encoding="utf-8")
            for ph in ("<NOME_DA_CLINICA>", "<SLUG_DA_CLINICA>", "<PORTE>", "<VERSAO_DO_KIT>", "<DATA_CRIACAO>"):
                assert ph not in t, f"{ph} ficou em {p}"
    for obrig in ["CLAUDE.md", ".gitignore", ".claude/settings.json", "scripts/sessao-inicio.sh",
                  "sprints/S00.md", "sprints/S17.md", "credenciais/rabi-api-externa.md",
                  "dados/convenios/_modelo-convenio/precos-SLUG.csv", ".claude/agents/conferente-precos.md"]:
        assert (destino / obrig).exists(), obrig
    import os
    assert os.access(destino / "scripts" / "sessao-inicio.sh", os.X_OK)


def test_nao_sobrescreve_sem_forcar(tmp_path):
    destino = tmp_path / "c"
    nrc.main(["--destino", str(destino), "--clinica", "A"])
    (destino / "ESTADO.md").write_text("editado pela clínica", encoding="utf-8")
    nrc.main(["--destino", str(destino), "--clinica", "A"])
    assert (destino / "ESTADO.md").read_text(encoding="utf-8") == "editado pela clínica"
    nrc.main(["--destino", str(destino), "--clinica", "A", "--forcar"])
    assert "editado pela clínica" not in (destino / "ESTADO.md").read_text(encoding="utf-8")


def test_atualizar_claude_so_mexe_no_claude(tmp_path):
    destino = tmp_path / "c"
    nrc.main(["--destino", str(destino), "--clinica", "A"])
    (destino / "ESTADO.md").write_text("meu estado", encoding="utf-8")
    agente = destino / ".claude" / "agents" / "consolidador.md"
    agente.write_text("velho", encoding="utf-8")
    assert nrc.main(["--destino", str(destino), "--atualizar-claude"]) == 0
    assert agente.read_text(encoding="utf-8") != "velho"
    assert (destino / "ESTADO.md").read_text(encoding="utf-8") == "meu estado"


def test_exige_nome_da_clinica(tmp_path):
    assert nrc.main(["--destino", str(tmp_path / "x")]) == 2


def test_recusa_destino_dentro_do_kit():
    assert nrc.main(["--destino", str(nrc.RAIZ_KIT / "tmp-teste"), "--clinica", "A"]) == 2
