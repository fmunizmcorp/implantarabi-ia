# ferramentas/kit — manutenção do kit e criação de repo de clínica

> **Fonte:** este kit · **Conferido em:** 2026-09-25
> **Vale para:** kit v0.1.0 · **Kit:** v0.1.0

Python 3 só com biblioteca padrão. Todos devolvem código 0 (pass) ou 1 (fail).

> **Só do kit:** `verificar_tamanhos.py`, `verificar_links.py`,
> `verificar_vazamento.py`, `sincronizar_claude_modelo.py` e
> `gerar_sprints_modelo.py` são do **mantenedor do kit**. **Não rode no repo da
> clínica**: lá há credenciais e dados de propósito, e as regras de
> tamanho/índice são as do kit. Na clínica só se usam `personalizar_clinica.py`
> (primeira sessão) e `novo_repo_clinica.py --atualizar-claude`.

| Arquivo | O que faz | Quando usar |
|---|---|---|
| `novo_repo_clinica.py` | (caminho antigo / plano B) gera o repo de uma clínica a partir de `modelo-repo-clinica/` (placeholders, versão do kit no `ESTADO.md`; não sobrescreve sem `--forcar`; `--atualizar-claude` traz agentes novos) | ao começar uma clínica; quando o hook avisar que os agentes mudaram |
| `personalizar_clinica.py` | roda **dentro do repo da clínica** criado pelo repositório-modelo: troca os marcadores (nome, porte, slug, versão do kit de `.kit/VERSION`, data em America/Sao_Paulo) em todos os `.md/.json/.yml/.sh` (fora `.kit/` e `.git/`) e troca o README do modelo pelo da clínica; idempotente; recusa com código 3 se o repo já é de **outra** clínica | primeira sessão ("Vamos implantar <clínica>"); ver `modelo-repo-clinica/CLAUDE.md` |
| `exportar_modelo.py` | `--destino DIR` copia `modelo-repo-clinica/` **com os marcadores** (inclui `.github/`, `.claude/`, `scripts/`, `.gitignore`), grava o README do repositório-modelo e `.modelo-kit.json`, remove o que saiu do modelo (nunca `.git/`); `--checar DIR` sai 1 se defasado | publicar o repositório-modelo (manual ou pelo workflow `publicar-modelo.yml`) |
| `sincronizar_claude_modelo.py` | copia `.claude/{agents,skills,commands}` do kit para o modelo, reescrevendo caminhos para `.kit/` (`--checar` para a CI) | depois de alterar agente, skill ou comando do kit |
| `verificar_tamanhos.py` | `.md` ≤ 40 KB, demais ≤ 5 MB, toda pasta com `.md`/dados tem `00-INDICE.md` ou `README.md` | antes de todo commit do kit (CI) |
| `verificar_links.py` | links relativos dos `.md` existem (ignora http, âncoras, placeholders e `.kit/`) | antes de todo commit do kit (CI) |
| `verificar_vazamento.py` | chave `rbk_`, CPF real, nome de clínica real, `senha:` com valor (fora do modelo) | antes de todo commit do kit (CI) |
| `gerar_sprints_modelo.py` | copia o "Checklist de itens" de cada playbook `sprints/Sxx-*.md` para `modelo-repo-clinica/sprints/Sxx.md` (fonte única); `--checar` na CI | depois de editar qualquer playbook |
| `_comum.py` | utilidades compartilhadas pelos verificadores | — |
| `tests/` | testes pytest (`python3 -m pytest ferramentas/kit -q`) | CI |

## Exemplos

```bash
# dentro do repo da clínica (primeira sessão)
python3 .kit/ferramentas/kit/personalizar_clinica.py --clinica "Clínica Exemplo" --porte pequena-media
# no kit: exportar o repositório-modelo
python3 ferramentas/kit/exportar_modelo.py --destino ../implantarabi-modelo-clinica
python3 ferramentas/kit/verificar_tamanhos.py && python3 ferramentas/kit/verificar_links.py \
    && python3 ferramentas/kit/verificar_vazamento.py
```

## Repositório-modelo (GitHub Template) e o secret `MODELO_PUSH_TOKEN`

As clínicas criam o repo pelo botão **Use this template** do repositório
público `fmunizmcorp/implantarabi-modelo-clinica`
(https://github.com/fmunizmcorp/implantarabi-modelo-clinica/generate). O
conteúdo dele sai de `modelo-repo-clinica/` por `exportar_modelo.py`.

**Publicação automática** — workflow `.github/workflows/publicar-modelo.yml`
(roda a cada push na `main` que mexa em `modelo-repo-clinica/**`,
`exportar_modelo.py`, `_comum.py` ou `VERSION`, e sob demanda). Ele precisa do
secret do kit:

| Campo | Valor |
|---|---|
| Nome do secret | `MODELO_PUSH_TOKEN` (em *Settings → Secrets and variables → Actions* do repo do kit) |
| Tipo | token **fine-grained** (GitHub → *Settings → Developer settings → Personal access tokens → Fine-grained tokens*) |
| Acesso a repositórios | **Only select repositories** → só `implantarabi-modelo-clinica` |
| Permissões | **Contents: Read and write** e **Workflows: Read and write** (o modelo leva `.github/workflows/automerge.yml`; sem "Workflows" o GitHub recusa o push desse arquivo). Metadata: read (automático) |
| Validade | a que o dono escolher; ao vencer, o workflow falha no `git clone`/`push` — gere outro e troque o secret |

Sem o secret, o job imprime um aviso e termina **verde** (não bloqueia o kit).
Passo a passo para o mantenedor: [../../manual/06-mantenedor.md](../../manual/06-mantenedor.md).

**Publicação manual** (sessão do kit com acesso ao repositório-modelo):

```bash
git clone https://github.com/fmunizmcorp/implantarabi-modelo-clinica /tmp/modelo
python3 ferramentas/kit/exportar_modelo.py --destino /tmp/modelo
python3 ferramentas/kit/exportar_modelo.py --checar /tmp/modelo
cd /tmp/modelo && git add -A && git commit -m "modelo: kit $(cat VERSION)" && git push
```
