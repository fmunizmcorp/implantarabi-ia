"""Toda ferramenta com CLI roda por CAMINHO a partir do repo da clínica.

Simula o repo da clínica: pasta temporária com `.kit/` apontando para o kit e
roda `python3 .kit/ferramentas/<area>/<x>.py --help` com cwd nessa pasta
(sem PYTHONPATH). Tem de sair com código 0 (sem ImportError de import relativo).
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ_KIT = Path(__file__).resolve().parents[3]
FERR = RAIZ_KIT / "ferramentas"


def _clis():
    for p in sorted(FERR.rglob("*.py")):
        if "tests" in p.parts or "__pycache__" in p.parts or p.name.startswith("_"):
            continue
        if '__name__ == "__main__"' in p.read_text(encoding="utf-8"):
            yield p.relative_to(RAIZ_KIT).as_posix()


CLIS = list(_clis())


def test_ha_clis():
    assert len(CLIS) >= 15
    for esperado in ("ferramentas/rabi_api/testar_chave.py", "ferramentas/rabi_api/foto.py",
                     "ferramentas/rabi_api/atualizar_spec.py", "ferramentas/rabi_api/gerar_rotas.py",
                     "ferramentas/conversao/simulador.py"):
        assert esperado in CLIS


@pytest.mark.parametrize("rel", CLIS)
def test_help_por_caminho_no_repo_da_clinica(rel, tmp_path):
    (tmp_path / ".kit").symlink_to(RAIZ_KIT, target_is_directory=True)
    amb = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    r = subprocess.run([sys.executable, f".kit/{rel}", "--help"], cwd=tmp_path, env=amb,
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, f"{rel}: código {r.returncode}\n{r.stderr[-800:]}"
    assert "Traceback" not in r.stderr
