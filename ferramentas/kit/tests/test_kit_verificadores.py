"""Testes dos verificadores do kit (tamanhos, links, vazamento) e do sincronizador."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import sincronizar_claude_modelo as sinc  # noqa: E402
import verificar_links as vl  # noqa: E402
import verificar_tamanhos as vt  # noqa: E402
import verificar_vazamento as vv  # noqa: E402


def escrever(p: Path, texto: str = "x") -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texto, encoding="utf-8")
    return p


# ---------- tamanhos e índices ----------
def test_tamanhos_passa_com_indice(tmp_path):
    escrever(tmp_path / "a" / "00-INDICE.md", "# a")
    escrever(tmp_path / "a" / "b.md", "texto")
    escrever(tmp_path / "INDICE.md", "# raiz")
    assert vt.verificar(tmp_path) == []


def test_tamanhos_md_grande_e_sem_indice(tmp_path):
    escrever(tmp_path / "INDICE.md")
    escrever(tmp_path / "pasta" / "grande.md", "x" * (41 * 1024))
    probs = vt.verificar(tmp_path)
    assert any("MD GRANDE" in p for p in probs)
    assert any("SEM ÍNDICE" in p and "pasta" in p for p in probs)


def test_tamanhos_readme_vale_como_indice_e_tests_ignorado(tmp_path):
    escrever(tmp_path / "README.md")
    escrever(tmp_path / "d" / "README.md")
    escrever(tmp_path / "d" / "dados.csv", "a;b")
    escrever(tmp_path / "x" / "tests" / "nota.md")
    assert vt.verificar(tmp_path) == []


def test_tamanhos_arquivo_de_dados_acima_de_5mb(tmp_path):
    escrever(tmp_path / "README.md")
    grande = tmp_path / "big.csv"
    with open(grande, "wb") as f:
        f.seek(5 * 1024 * 1024 + 10)
        f.write(b"x")
    assert any("ARQ GRANDE" in p for p in vt.verificar(tmp_path))


def test_tamanhos_pasta_so_com_python_nao_exige_indice(tmp_path):
    escrever(tmp_path / "README.md")
    escrever(tmp_path / "ferr" / "a.py", "print(1)")
    assert vt.verificar(tmp_path) == []


# ---------- links ----------
def test_links_ok_quebrado_e_ignorados(tmp_path):
    escrever(tmp_path / "b.md", "# b")
    escrever(tmp_path / "pasta" / "c.md", "# c")
    escrever(
        tmp_path / "a.md",
        "\n".join([
            "[ok](b.md) [ok2](pasta/c.md#secao) [pasta](pasta/)",
            "[quebrado](nao-existe.md)",
            "[web](https://exemplo.com) [ancora](#topo) [mail](mailto:a@b.c)",
            "[kit](.kit/BOOTSTRAP.md) [kit2](../.kit/sprints/S01-x.md)",
            "[placeholder](sprints/<arquivo>.md)",
            "`[em codigo](nao-existe-2.md)`",
            "```",
            "[em bloco](nao-existe-3.md)",
            "```",
        ]),
    )
    probs = vl.verificar(tmp_path)
    assert len(probs) == 1 and "nao-existe.md" in probs[0]


# ---------- vazamento ----------
def test_vazamento_detecta_padroes(tmp_path):
    chave = "rbk_" + "Abcdef123456789"
    cpf_real = "987" + ".654.321-" + "00"
    nome = "Clin" + "fec"
    escrever(tmp_path / "doc.md", f"chave {chave}\ncpf {cpf_real}\n{nome} aqui\nsenha: Abc@12345\n")
    achados = vv.verificar(tmp_path)
    tipos = " ".join(achados)
    assert "CHAVE" in tipos and "CPF" in tipos and "NOME" in tipos and "SENHA" in tipos
    assert chave not in tipos  # nunca imprime a chave inteira


def test_vazamento_ignora_teste_placeholder_modelo_e_referencias(tmp_path):
    escrever(tmp_path / "doc.md", "cpf de teste 529.982.247-25 e 111.111.111-11\nsenha: <defina>\nsenha: mínimo\n")
    escrever(tmp_path / "modelo-repo-clinica" / "c.md", "sen" + "ha: Troca@123\n")
    escrever(tmp_path / "referencias" / "t.csv", "rbk_" + "Abcdef123456789\n")
    escrever(tmp_path / "conhecimento" / "api-externa" / "spec" / "s.json", '{"x":"' + "rbk_" + 'Abcdef12345678"}')
    escrever(tmp_path / "ok.md", "rbk_" + "Abcdef123456789  <!-- vazamento-ok: exemplo -->\n")
    assert vv.verificar(tmp_path) == []


def test_vazamento_rbk_curto_ou_placeholder_nao_acusa(tmp_path):
    escrever(tmp_path / "doc.md", "Authorization: Bearer rbk_...\napi_key: <cole aqui>\n")
    assert vv.verificar(tmp_path) == []


# ---------- sincronização .claude → modelo ----------
def test_reescrever_caminhos_do_kit():
    t = "Leia `conhecimento/x.md`, rode `python3 ferramentas/conversao/motor.py`, playbook `sprints/S10-convenios.md` e `sprints/S10b-convenio-abas-e-precos.md`."
    r = sinc.reescrever(t)
    assert "`.kit/conhecimento/x.md`" in r
    assert "python3 .kit/ferramentas/conversao/motor.py" in r
    assert "`.kit/sprints/S10-convenios.md`" in r and "`.kit/sprints/S10b-convenio-abas-e-precos.md`" in r


def test_reescrever_preserva_caminhos_da_clinica():
    t = "`sprints/S10.md` · `dados/convenios/a/precos-a.csv` · `config/referencias-da-clinica.md` · `00-INDICE.md` · `.kit/prompts/x.md`"
    assert sinc.reescrever(t) == t


def test_modelo_claude_esta_sincronizado():
    assert sinc.main(["--checar"]) == 0
