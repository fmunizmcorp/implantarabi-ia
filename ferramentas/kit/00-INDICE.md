# ferramentas/kit — manutenção do kit e criação de repo de clínica

> **Fonte:** este kit · **Conferido em:** 2026-09-25
> **Vale para:** kit v0.1.0 · **Kit:** v0.1.0

Python 3 só com biblioteca padrão. Todos devolvem código 0 (pass) ou 1 (fail).

> **Só do kit:** `verificar_tamanhos.py`, `verificar_links.py`,
> `verificar_vazamento.py`, `sincronizar_claude_modelo.py` e
> `gerar_sprints_modelo.py` são do **mantenedor do kit**. **Não rode no repo da
> clínica**: lá há credenciais e dados de propósito, e as regras de
> tamanho/índice são as do kit. Na clínica só se usa `novo_repo_clinica.py`.

| Arquivo | O que faz | Quando usar |
|---|---|---|
| `novo_repo_clinica.py` | gera o repo de uma clínica a partir de `modelo-repo-clinica/` (placeholders, versão do kit no `ESTADO.md`; não sobrescreve sem `--forcar`; `--atualizar-claude` traz agentes novos) | ao começar uma clínica; quando o hook avisar que os agentes mudaram |
| `sincronizar_claude_modelo.py` | copia `.claude/{agents,skills,commands}` do kit para o modelo, reescrevendo caminhos para `.kit/` (`--checar` para a CI) | depois de alterar agente, skill ou comando do kit |
| `verificar_tamanhos.py` | `.md` ≤ 40 KB, demais ≤ 5 MB, toda pasta com `.md`/dados tem `00-INDICE.md` ou `README.md` | antes de todo commit do kit (CI) |
| `verificar_links.py` | links relativos dos `.md` existem (ignora http, âncoras, placeholders e `.kit/`) | antes de todo commit do kit (CI) |
| `verificar_vazamento.py` | chave `rbk_`, CPF real, nome de clínica real, `senha:` com valor (fora do modelo) | antes de todo commit do kit (CI) |
| `gerar_sprints_modelo.py` | copia o "Checklist de itens" de cada playbook `sprints/Sxx-*.md` para `modelo-repo-clinica/sprints/Sxx.md` (fonte única); `--checar` na CI | depois de editar qualquer playbook |
| `_comum.py` | utilidades compartilhadas pelos verificadores | — |
| `tests/` | testes pytest (`python3 -m pytest ferramentas/kit -q`) | CI |

## Exemplos

```bash
python3 ferramentas/kit/novo_repo_clinica.py --destino ../rabi-implantacao-clinica-exemplo \
    --clinica "Clínica Exemplo" --porte pequena-media
python3 ferramentas/kit/verificar_tamanhos.py && python3 ferramentas/kit/verificar_links.py \
    && python3 ferramentas/kit/verificar_vazamento.py
```
