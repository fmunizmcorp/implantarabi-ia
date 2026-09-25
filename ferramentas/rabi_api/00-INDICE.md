# Índice — `ferramentas/rabi_api` (cliente da API externa do Rabi)

> **Fonte:** código deste kit · Swagger https://api.rabisistemas.com.br/external-docs/ · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger de 25/09/2026) · **Kit:** v0.1.0

Python 3.11, **só biblioteca padrão** (urllib, json). Rode tudo da raiz do repo, pelo
caminho: na clínica `python3 .kit/ferramentas/rabi_api/<modulo>.py`; no kit (mantenedor)
`python3 ferramentas/rabi_api/<modulo>.py`.

| Arquivo | O que faz | Quando usar |
|---|---|---|
| [README.md](README.md) | guia curto de uso com exemplos | primeira vez |
| `cliente.py` | `ClienteRabi`: chave (env → arquivo), base, get/post/put/patch/delete, `ler_tudo` (paginação + envelopes + total), `enviar_lote` (fatias + 207), 401/403/503/429, validade | toda chamada à API |
| `corpo_escrita.py` | converte o GET de `/servicos/{id}` e `/produtos/{id}` no corpo do PUT (nomes e IDs de escrita); recusa com a lista do que falta — nunca omite em silêncio | antes de todo PUT de serviço ou produto |
| `foto.py` | foto antes/depois (JSON, dado pessoal mascarado) e `diff` campo a campo; CLI `antes|depois|diff` | ritual de toda gravação |
| `testar_chave.py` | uma leitura por grupo (25 áreas), validade e dias restantes, resumo Markdown sem a chave | S00, troca de chave, início de sessão |
| `atualizar_spec.py` | baixa o Swagger, salva `spec/openapi-AAAA-MM-DD.json`, compara com o anterior, regenera `rotas/` | mantenedor do kit, quando a Rabi publica mudança |
| `gerar_rotas.py` | gera `conhecimento/api-externa/rotas/` a partir do spec (268 operações) | chamado pelo atualizador; ou à mão |
| `__init__.py` | marca o pacote | — |
| [tests/00-INDICE.md](tests/00-INDICE.md) | testes pytest (servidor HTTP falso local, sem rede) | antes de alterar qualquer arquivo daqui |

Conhecimento correspondente: [../../conhecimento/api-externa/00-INDICE.md](../../conhecimento/api-externa/00-INDICE.md).
