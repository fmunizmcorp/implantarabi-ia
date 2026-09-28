"""Testes do canal de aprendizados (clínica → kit) e das novidades (kit → clínica)."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import atualizar_repo_clinica as arc  # noqa: E402
import coletar_aprendizados as col  # noqa: E402
import filtrar_aprendizado as fa  # noqa: E402
import novo_repo_clinica as nrc  # noqa: E402

LIMPO = """# Fator K negativo reduz o preço do produto
- **Tipo:** Cálculo / conversão de valores
- **Arquivo do kit afetado:** conhecimento/precos-e-conversao/05-produtos.md
- **Versão do kit:** 0.3.0
- **Status:** rascunho

## O que o kit diz
Fator K sempre aumenta o preço.

## O que acontece de verdade
Um convênio com Fator K de -10% (exemplo) reduz o valor: R$ 100,00 (exemplo) vira R$ 90,00 (exemplo).

## Regra proposta
Aceitar Fator K negativo no motor.

## Como detectar
Farol mostra receita menor que a tabela de referência.

## Evidência (só o tipo, nunca o conteúdo)
foto antes/depois relida; Farol conferido em 3 serviços.
"""


def _clinica(tmp_path: Path) -> Path:
    repo = tmp_path / "rabi-implantacao-clinica-sol-nascente"
    assert nrc.main(["--destino", str(repo), "--clinica", "Clínica Sol Nascente", "--porte", "consultorio"]) == 0
    return repo


# --- filtro -------------------------------------------------------------------
def test_filtro_limpo_passa():
    assert fa.filtrar_texto(LIMPO) == []


def test_filtro_bloqueia_cada_padrao():
    casos = {
        "chave": "use " + "rbk" + "_abcDEF123456 aqui",
        "cpf": "paciente 123.456.789-09",
        "cnpj": "empresa 12.345.678/0001-90",
        "email": "falar com fulano@clinica.com.br",
        "telefone": "ligar (61) 99132-6151",
        "cep": "fica no 70000-000",
        "id": "convênio id: 212 com erro",
        "rota": "GET /convenios/212/servicos",
        "valor": "o contrato paga R$ 150,00",
        "link": "ver https://github.com/clinica-x/rabi-implantacao-x",
        "senha": "sen" + "ha: segredo123",  # vazamento-ok (caso de teste)
    }
    for nome, texto in casos.items():
        assert fa.filtrar_texto(texto), f"não bloqueou: {nome}"


def test_filtro_nunca_imprime_valor_inteiro():
    problemas = fa.filtrar_texto("" + "rbk" + "_abcDEF123456789")
    assert problemas and "" + "rbk" + "_abcDEF123456789" not in " ".join(problemas)


def test_filtro_bloqueia_nome_da_clinica_e_pessoas_de_dados(tmp_path):
    repo = _clinica(tmp_path)
    (repo / "dados" / "colaboradores" / "colab.csv").write_text("nome,crm\nMaria Aparecida Souza,123\n", encoding="utf-8")
    termos = fa.termos_da_clinica(repo)
    assert fa.filtrar_texto("na Clínica Sol Nascente o Farol", termos)
    assert fa.filtrar_texto("a Dra. maria aparecida souza pediu", termos)
    assert fa.filtrar_texto("repo rabi-implantacao-clinica-sol-nascente", termos)
    assert fa.filtrar_texto("o Farol ficou roxo no serviço composto", termos) == []


def test_furos_apontados_pela_validacao_cruzada(tmp_path):
    repo = _clinica(tmp_path)
    (repo / "dados" / "colaboradores" / "colab.csv").write_text(
        "nome;conselho\nAna Rocha;CRM 1\n", encoding="utf-8")  # CSV do kit usa ';'
    (repo / "PAPEIS.md").write_text("| Papel | Quem |\n|---|---|\n| Dono | Carlos Menezes |\n", encoding="utf-8")
    termos = fa.termos_da_clinica(repo)
    bloqueia = [
        "a Dra. Ana Rocha aprovou", "a Rocha pediu", "o Carlos Menezes decidiu",
        '"servicoId": 4521', "convenioId=77", "paga 187,43 por consulta", "fator K 12,5%",
        "R$ 150,00 no contrato; o exemplo é outro", "ver www.site-da-clinica.com.br",
        "token ghp_abcdefghijklmnop1234", "rbk" + "_abc",
    ]
    for texto in bloqueia:
        assert fa.filtrar_texto(texto, termos), f"deixou passar: {texto}"
    passa = [
        "serviço de cardiologia com Farol roxo", "paciente com idade 45 anos",
        "paga 187,43 (exemplo) por consulta", "Fator K 12,5% (exemplo)",
        "veja https://www.rabisistemas.com.br/manual/precos/index.html",
    ]
    for texto in passa:
        assert fa.filtrar_texto(texto, termos) == [], f"falso positivo: {texto}"


def test_links_publicos_permitidos():
    ok = "ver https://www.rabisistemas.com.br/manual/precos/index.html e https://github.com/fmunizmcorp/implantarabi-ia"
    assert fa.filtrar_texto(ok) == []


# --- fila e link --------------------------------------------------------------
def test_novo_filtrar_enviado_e_indice(tmp_path, capsys):
    repo = _clinica(tmp_path)
    assert fa.main(["--repo", str(repo), "novo", "--titulo", "Fator K negativo", "--tipo", "calculo"]) == 0
    arq = next((repo / "contribuicoes-kit").glob("[0-9]*.md"))
    # incompleto → bloqueia
    assert fa.main(["--repo", str(repo), "filtrar", str(arq)]) == 1
    arq.write_text(LIMPO.replace("Fator K negativo reduz o preço do produto", "Fator K negativo"), encoding="utf-8")
    capsys.readouterr()
    assert fa.main(["--repo", str(repo), "filtrar", str(arq)]) == 0
    saida = capsys.readouterr().out
    link = next(l for l in saida.splitlines() if l.startswith("https://github.com/"))
    q = parse_qs(urlparse(link).query)
    assert q["template"] == ["aprendizado-clinica.yml"]
    assert q["title"] == ["[aprendizado] Fator K negativo"]
    assert "Aceitar Fator K negativo" in q["regra"][0]
    assert len(link) < fa.LIMITE_URL
    assert "filtrado" in fa.ler_aprendizado(arq)["status"]
    assert fa.pendentes(repo) == 1
    assert fa.main(["--repo", str(repo), "enviado", str(arq), "--issue", "7"]) == 0
    d = fa.ler_aprendizado(arq)
    assert d["status"].startswith("enviado #7") and d["issue"].endswith("/issues/7")
    assert fa.pendentes(repo) == 0
    assert "enviado #7" in (repo / "contribuicoes-kit" / "00-INDICE.md").read_text(encoding="utf-8")


def test_filtrar_bloqueia_dado_no_arquivo(tmp_path):
    repo = _clinica(tmp_path)
    arq = repo / "contribuicoes-kit" / "2026-09-25-01-x.md"
    arq.write_text(LIMPO.replace("Farol mostra", "Na Clínica Sol Nascente o Farol mostra"), encoding="utf-8")
    assert fa.main(["--repo", str(repo), "filtrar", str(arq)]) == 1
    assert fa.ler_aprendizado(arq)["status"] == "rascunho"


# --- coletor do kit -----------------------------------------------------------
def test_coletor_monta_caixa_e_sinaliza(tmp_path):
    issues = [
        {"number": 3, "state": "open", "title": "[aprendizado] Fator K negativo", "html_url": "u3",
         "created_at": "2026-09-26T10:00:00Z", "labels": [{"name": "aprendizado-clinica"}],
         "body": "### Tipo\n\nCálculo\n\n### Arquivo do kit afetado\n\nmotor.py\n\n### Regra proposta\n\n_No response_"},
        {"number": 4, "state": "open", "title": "[aprendizado] CPF 123.456.789-09 no texto", "html_url": "u4",
         "created_at": "2026-09-26T11:00:00Z", "labels": [], "body": ""},
        {"number": 5, "state": "closed", "title": "outra coisa", "labels": [], "body": ""},
        {"number": 6, "state": "open", "title": "[aprendizado] PR", "labels": [], "pull_request": {}},
    ]
    entrada = tmp_path / "i.json"
    entrada.write_text(json.dumps(issues), encoding="utf-8")
    saida, sinal = tmp_path / "caixa.md", tmp_path / "sinal.txt"
    assert col.main(["--entrada", str(entrada), "--saida", str(saida), "--sinalizar", str(sinal)]) == 0
    caixa = saida.read_text(encoding="utf-8")
    assert "#3" in caixa and "Fator K negativo" in caixa and "Cálculo" in caixa
    assert "123.456" not in caixa and "título ocultado" in caixa
    assert "#5" not in caixa and "#6" not in caixa
    assert sinal.read_text(encoding="utf-8").split() == ["4"]


# --- novidades e estrutura ----------------------------------------------------
def test_atualizar_nunca_toca_dados_e_reaplica_nome(tmp_path):
    repo = _clinica(tmp_path)
    estado_antes = (repo / "ESTADO.md").read_text(encoding="utf-8")
    (repo / "dados" / "empresa" / "empresa.md").write_text("dado real", encoding="utf-8")
    (repo / "CLAUDE.md").write_text("versão velha", encoding="utf-8")
    (repo / "dados" / "00-INDICE.md").write_text("índice editado pela clínica", encoding="utf-8")
    import shutil
    shutil.rmtree(repo / "contribuicoes-kit")
    assert arc.main(["--repo", str(repo), "--checar"]) == 1
    assert arc.main(["--repo", str(repo), "--aplicar"]) == 0
    claude = (repo / "CLAUDE.md").read_text(encoding="utf-8")
    assert "Clínica Sol Nascente" in claude and "<NOME_DA_CLINICA>" not in claude
    assert (repo / "contribuicoes-kit" / "00-INDICE.md").is_file()
    assert (repo / "ESTADO.md").read_text(encoding="utf-8") == estado_antes
    assert (repo / "dados" / "empresa" / "empresa.md").read_text(encoding="utf-8") == "dado real"
    assert (repo / "dados" / "00-INDICE.md").read_text(encoding="utf-8") == "índice editado pela clínica"
    assert arc.main(["--repo", str(repo), "--checar"]) == 0  # idempotente
    marc = json.loads((repo / ".modelo-kit.json").read_text(encoding="utf-8"))
    assert marc["versao_do_kit"] == nrc.versao_kit()


def test_atualizar_recusa_repo_nao_personalizado(tmp_path):
    repo = tmp_path / "modelo"
    shutil_copy = __import__("shutil").copytree
    shutil_copy(nrc.MODELO, repo)
    assert arc.main(["--repo", str(repo), "--aplicar"]) == 2
    assert arc.main(["--repo", str(repo), "--checar"]) == 0


def test_novidades_lista_desde_o_visto(tmp_path, capsys):
    repo = _clinica(tmp_path)
    kit = tmp_path / "kit"
    kit.mkdir()
    (kit / "VERSION").write_text("0.4.0\n", encoding="utf-8")
    (kit / "CHANGELOG.md").write_text(
        "# CHANGELOG\n\n## v0.4.0 — x\n- Regra nova de pacote.\n- Ação nas clínicas: rodar diagnóstico dos pacotes.\n\n"
        "## v0.3.0 — y\n- Canal de aprendizados.\n\n## v0.2.0 — z\n- Antiga.\n", encoding="utf-8")
    arc.gravar_marcador(repo, kit_visto="0.2.0")
    linhas, visto, atual = arc.novidades(repo, kit)
    assert visto == "0.2.0" and atual == "0.4.0"
    assert linhas[0].startswith("v0.4.0") and "rodar diagnóstico dos pacotes" in linhas[1]
    assert any(l.startswith("v0.3.0") for l in linhas) and not any("0.2.0" in l for l in linhas)
    arc.gravar_marcador(repo, kit_visto="0.4.0")
    assert arc.novidades(repo, kit)[0] == []


# --- achados da validação cruzada no atualizador --------------------------------
def test_atualizar_preserva_configuracao_local_e_nao_ressuscita(tmp_path):
    repo = _clinica(tmp_path)
    (repo / ".gitignore").write_text((repo / ".gitignore").read_text(encoding="utf-8") + "*.pdf\n", encoding="utf-8")
    cfg = json.loads((repo / ".claude" / "settings.json").read_text(encoding="utf-8"))
    cfg.setdefault("permissions", {}).setdefault("allow", []).append("Bash(meu-comando-local:*)")
    cfg["chaveDaClinica"] = True
    (repo / ".claude" / "settings.json").write_text(json.dumps(cfg), encoding="utf-8")
    claude = (repo / "CLAUDE.md").read_text(encoding="utf-8")
    claude = claude.replace("(nenhuma regra local por enquanto)", "Nunca agendar aos sábados.")
    (repo / "CLAUDE.md").write_text(claude.replace("## FRASES DE DISPARO", "## FRASES DE DISPARO (velho)"), encoding="utf-8")
    for apagado in ("credenciais/rabi-api-externa.md", "historico/HISTORICO.md", "sprints/S03.md", "ANALISE-CONTRATOS.md"):
        (repo / apagado).unlink()
    assert arc.main(["--repo", str(repo), "--aplicar"]) == 0
    assert "*.pdf" in (repo / ".gitignore").read_text(encoding="utf-8")
    cfg2 = json.loads((repo / ".claude" / "settings.json").read_text(encoding="utf-8"))
    assert "Bash(meu-comando-local:*)" in cfg2["permissions"]["allow"] and cfg2["chaveDaClinica"] is True
    claude2 = (repo / "CLAUDE.md").read_text(encoding="utf-8")
    assert "Nunca agendar aos sábados." in claude2 and "(velho)" not in claude2
    for apagado in ("credenciais/rabi-api-externa.md", "historico/HISTORICO.md", "sprints/S03.md", "ANALISE-CONTRATOS.md"):
        assert not (repo / apagado).exists(), f"ressuscitou {apagado}"
    copias = list((repo / "historico" / "estrutura-anterior").rglob("CLAUDE.md"))
    assert copias and "(velho)" in copias[0].read_text(encoding="utf-8")
    assert arc.main(["--repo", str(repo), "--checar"]) == 0  # idempotente com a mescla


def test_novidade_nao_se_perde_depois_de_aplicar(tmp_path):
    repo = _clinica(tmp_path)
    arc.gravar_marcador(repo, versao_do_kit="0.0.1")  # clínica antiga, sem kit_visto
    (repo / "CLAUDE.md").write_text("velho", encoding="utf-8")
    assert arc.main(["--repo", str(repo), "--aplicar"]) == 0
    linhas, visto, _ = arc.novidades(repo, arc.MODELO.parent)
    assert visto == "0.0.1" and linhas  # ainda mostra as novidades até --marcar-visto


def test_repo_recem_personalizado_esta_em_dia(tmp_path):
    repo = _clinica(tmp_path)
    assert arc.main(["--repo", str(repo), "--checar"]) == 0
