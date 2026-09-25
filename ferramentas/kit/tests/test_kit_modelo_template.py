"""Testes do repositório-modelo (exportar_modelo.py) e da personalização (personalizar_clinica.py)."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import exportar_modelo as em  # noqa: E402
import personalizar_clinica as pc  # noqa: E402
from _comum import PLACEHOLDERS, RAIZ_KIT, ler_versao  # noqa: E402

SCRIPT_INICIO = "scripts/sessao-inicio.sh"


def _repo_da_clinica(tmp_path: Path) -> Path:
    """Simula 'Use this template': exporta o modelo e liga .kit/ ao kit."""
    repo = tmp_path / "rabi-implantacao-teste"
    assert em.main(["--destino", str(repo)]) == 0
    (repo / ".kit").symlink_to(RAIZ_KIT, target_is_directory=True)
    return repo


# ---------- exportar_modelo ----------
def test_exporta_preservando_marcadores(tmp_path):
    destino = tmp_path / "modelo"
    assert em.main(["--destino", str(destino)]) == 0
    estado = (destino / "ESTADO.md").read_text(encoding="utf-8")
    assert "<NOME_DA_CLINICA>" in estado and "<VERSAO_DO_KIT>" in estado and "<PORTE>" in estado
    for obrig in [".github/workflows/automerge.yml", ".claude/settings.json", ".gitignore",
                  SCRIPT_INICIO, "sprints/S17.md", ".modelo-kit.json"]:
        assert (destino / obrig).exists(), obrig
    assert os.access(destino / SCRIPT_INICIO, os.X_OK)
    readme = (destino / "README.md").read_text(encoding="utf-8")
    assert em.MARCA_README in readme
    assert "Use this template" in readme and "Private" in readme
    assert "Vamos implantar" in readme and "MANUAL-PASSO-A-PASSO.md" in readme


def test_checar_passa_depois_de_exportar_e_falha_se_defasado(tmp_path):
    destino = tmp_path / "modelo"
    em.main(["--destino", str(destino)])
    assert em.main(["--checar", str(destino)]) == 0
    (destino / "ESTADO.md").write_text("mudou", encoding="utf-8")
    (destino / "sobra.md").write_text("x", encoding="utf-8")
    assert em.main(["--checar", str(destino)]) == 1
    difs = em.comparar(destino)
    assert "diferente: ESTADO.md" in difs and "sobrando: sobra.md" in difs
    # reexportar conserta e remove o que sobra, sem mexer em .git/
    (destino / ".git").mkdir()
    (destino / ".git" / "HEAD").write_text("ref", encoding="utf-8")
    assert em.main(["--destino", str(destino)]) == 0
    assert em.main(["--checar", str(destino)]) == 0
    assert not (destino / "sobra.md").exists()
    assert (destino / ".git" / "HEAD").exists()


def test_checar_pasta_inexistente_falha(tmp_path):
    assert em.main(["--checar", str(tmp_path / "nao-existe")]) == 1


def test_recusa_pasta_estranha_e_aceita_repo_so_com_readme(tmp_path):
    estranha = tmp_path / "estranha"
    (estranha / "src").mkdir(parents=True)
    (estranha / "src" / "app.py").write_text("x", encoding="utf-8")
    assert em.main(["--destino", str(estranha)]) == 2
    assert (estranha / "src" / "app.py").exists()
    novo = tmp_path / "novo"
    novo.mkdir()
    (novo / "README.md").write_text("# criado à mão", encoding="utf-8")
    assert em.main(["--destino", str(novo)]) == 0
    assert em.MARCA_README in (novo / "README.md").read_text(encoding="utf-8")


def test_exportar_recusa_destino_dentro_do_kit():
    assert em.main(["--destino", str(RAIZ_KIT / "tmp-modelo")]) == 2


# ---------- personalizar_clinica ----------
def test_personaliza_todos_os_marcadores(tmp_path):
    repo = _repo_da_clinica(tmp_path)
    assert pc.main(["--clinica", "Clínica Teste", "--porte", "consultorio", "--repo", str(repo)]) == 0
    estado = (repo / "ESTADO.md").read_text(encoding="utf-8")
    assert "- **Clínica:** Clínica Teste" in estado
    assert "Consultório individual" in estado
    assert ler_versao(RAIZ_KIT) in estado
    assert "rabi-implantacao-clinica-teste" in estado
    for p in repo.rglob("*"):
        if ".kit" in p.relative_to(repo).parts or not p.is_file():
            continue
        if p.suffix in {".md", ".json", ".yml", ".sh"}:
            t = p.read_text(encoding="utf-8")
            for ph in PLACEHOLDERS:
                assert ph not in t, f"{ph} ficou em {p}"
    readme = (repo / "README.md").read_text(encoding="utf-8")
    assert em.MARCA_README not in readme and "Clínica Teste" in readme


def test_personalizar_usa_nome_do_origin_como_slug(tmp_path):
    repo = _repo_da_clinica(tmp_path)
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "remote", "add", "origin",
                    "https://github.com/exemplo/rabi-implantacao-exemplo-ok.git"], check=True)
    assert pc.main(["--clinica", "Clínica Teste", "--porte", "rede", "--repo", str(repo)]) == 0
    assert "rabi-implantacao-exemplo-ok" in (repo / "ESTADO.md").read_text(encoding="utf-8")


def test_personalizar_idempotente_e_recusa_outro_nome(tmp_path, capsys):
    repo = _repo_da_clinica(tmp_path)
    assert pc.main(["--clinica", "Clínica Teste", "--porte", "pequena-media", "--repo", str(repo)]) == 0
    antes = (repo / "ESTADO.md").read_text(encoding="utf-8")
    # mesma clínica (sem porte, grafia diferente): ok, nada muda
    assert pc.main(["--clinica", "clinica teste", "--repo", str(repo)]) == 0
    assert (repo / "ESTADO.md").read_text(encoding="utf-8") == antes
    # arquivo novo com marcador (veio de uma atualização) é completado
    (repo / "novo.md").write_text("# <NOME_DA_CLINICA>", encoding="utf-8")
    assert pc.main(["--clinica", "Clínica Teste", "--repo", str(repo)]) == 0
    assert (repo / "novo.md").read_text(encoding="utf-8") == "# Clínica Teste"
    # outra clínica: recusa com código 3
    capsys.readouterr()
    assert pc.main(["--clinica", "Outra Clínica", "--porte", "rede", "--repo", str(repo)]) == 3
    assert "este repositório é da clínica Clínica Teste" in capsys.readouterr().err
    assert (repo / "ESTADO.md").read_text(encoding="utf-8") == antes


def test_personalizar_primeira_vez_exige_porte(tmp_path):
    repo = _repo_da_clinica(tmp_path)
    assert pc.main(["--clinica", "Clínica Teste", "--repo", str(repo)]) == 2
    assert "<NOME_DA_CLINICA>" in (repo / "ESTADO.md").read_text(encoding="utf-8")


def test_personalizar_nao_mexe_no_kit(tmp_path):
    repo = _repo_da_clinica(tmp_path)
    kit_estado = (RAIZ_KIT / "modelo-repo-clinica" / "ESTADO.md").read_text(encoding="utf-8")
    pc.main(["--clinica", "Clínica Teste", "--porte", "rede", "--repo", str(repo)])
    assert (RAIZ_KIT / "modelo-repo-clinica" / "ESTADO.md").read_text(encoding="utf-8") == kit_estado


def test_personalizar_recusa_pasta_sem_estado(tmp_path):
    assert pc.main(["--clinica", "X", "--porte", "rede", "--repo", str(tmp_path)]) == 2


# ---------- sessao-inicio.sh: resumo de retomada ----------
def _rodar_inicio(repo: Path, **extra) -> str:
    amb = {k: v for k, v in os.environ.items() if k != "RABI_API_KEY"}
    amb.update({"CLAUDE_PROJECT_DIR": str(repo), "KIT_URL": str(RAIZ_KIT)})
    amb.update(extra)
    r = subprocess.run(["bash", str(repo / SCRIPT_INICIO)], cwd=repo, env=amb,
                       capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr
    return r.stdout


def test_resumo_primeira_vez_e_retomada(tmp_path):
    repo = _repo_da_clinica(tmp_path)
    saida = _rodar_inicio(repo)
    assert "RESUMO DE RETOMADA" in saida
    assert "ainda não personalizado — primeira vez" in saida
    assert "RABI_API_KEY: NÃO definida" in saida

    pc.main(["--clinica", "Clínica Teste", "--porte", "pequena-media", "--repo", str(repo)])
    (repo / "pendencias" / "LACUNAS.md").write_text(
        "| # | Sprint | O que falta | Pergunta | Efeito | Status |\n|---|---|---|---|---|---|\n"
        "| 1 | S01 | CNES | ? | x | aberta |\n| 2 | S01 | CEP | ? | x | respondida |\n"
        "| 3 | S03 | salas | ? | x | pendente |\n", encoding="utf-8")
    daily = repo / "historico" / "daily"
    (daily / "2026-09-24.md").write_text("velha", encoding="utf-8")
    (daily / "2026-09-25.md").write_text("nova", encoding="utf-8")
    receb = repo / "documentos-do-cliente" / "recebidos" / "2026-09-25"
    receb.mkdir(parents=True)
    (receb / "contrato convenio a.pdf").write_bytes(b"%PDF")
    (repo / "credenciais" / "rabi-api-externa.md").write_text(
        "api_key: rbk_fic_arquivo\n| Validade (`X-ApiKey-Expires-At`) | 2099-01-01T00:00:00.000Z |\n",
        encoding="utf-8")
    saida = _rodar_inicio(repo, RABI_API_KEY="rbk_teste_ficticio")
    assert "Clínica: Clínica Teste" in saida
    assert "Lacunas abertas: 2" in saida
    assert "2026-09-25.md" in saida
    assert "Documentos novos (fora do inventário): 1" in saida
    assert "contrato convenio a.pdf" in saida
    assert "2099-01-01" in saida
    assert "RABI_API_KEY: definida" in saida
    assert "rbk_teste_ficticio" not in saida and "rbk_fic_arquivo" not in saida
