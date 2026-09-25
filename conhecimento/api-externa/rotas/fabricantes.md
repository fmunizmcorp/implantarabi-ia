# Rotas — Fabricantes (6 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 -m ferramentas.rabi_api.atualizar_spec` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `GET /fabricantes`
- `POST /fabricantes`
- `POST /fabricantes/bulk`
- `GET /fabricantes/{id}`
- `PUT /fabricantes/{id}`
- `DELETE /fabricantes/{id}`

### `GET /fabricantes`

- **Permissão:** `fabricante:read` · **Manual:** [op-get-fabricantes](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-fabricantes)
- **Resumo:** Listar fabricantes

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |
| `ativo` | query | boolean | não | Sem informar, lista ativos e inativos. |

**Respostas:**
- `200` Lista paginada — campos: `page`, `pageSize`, `total`, `totalPages`, `dados`; item de `dados`: `id`, `nome`, `ativo`, `createdAt`, `updatedAt`

### `POST /fabricantes`

- **Permissão:** `fabricante:create` · **Manual:** [op-post-fabricantes](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-fabricantes)
- **Resumo:** Cadastrar fabricante

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `nome` | string | **sim** |  |
| `anexos` | lista de objeto | não |  |
| `anexos[].nome` | string | não |  |
| `anexos[].caminhoArquivo` | string | não |  |

**Respostas:**
- `201` Fabricante criado — campos: `id`, `nome`, `ativo`, `createdAt`, `updatedAt`
- `422` Falha ao criar fabricante

### `POST /fabricantes/bulk`

- **Permissão:** `fabricante:create` · **Manual:** [op-post-fabricantes-bulk](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-fabricantes-bulk)
- **Resumo:** Cadastrar vários fabricantes de uma vez
- **Descrição:** Até 50 itens por requisição (chave `fabricantes`). `207` = falha parcial, ver `resultados`; reenvie só os itens com erro.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `fabricantes` | lista de objeto | **sim** | máx. itens 50 |
| `fabricantes[].nome` | string | **sim** |  |
| `fabricantes[].anexos` | lista de objeto | não |  |
| `fabricantes[].anexos[].nome` | string | não |  |
| `fabricantes[].anexos[].caminhoArquivo` | string | não |  |

**Respostas:**
- `201` Todos criados — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `207` Falha parcial — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `400` Lote vazio ou acima de 50 itens
- `429` Já existe um lote em andamento para esta clínica e recurso

### `GET /fabricantes/{id}`

- **Permissão:** `fabricante:read` · **Manual:** [op-get-fabricantes-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-fabricantes-id)
- **Resumo:** Consultar fabricante

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do fabricante |

**Respostas:**
- `200` Fabricante — campos: `id`, `nome`, `ativo`, `createdAt`, `updatedAt`
- `400` `id` inválido
- `404` Fabricante não encontrado

### `PUT /fabricantes/{id}`

- **Permissão:** `fabricante:update` · **Manual:** [op-put-fabricantes-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-fabricantes-id)
- **Resumo:** Atualizar fabricante
- **Descrição:** `anexos` enviados no corpo vão pra uma tabela separada e não aparecem na resposta.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do fabricante |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `nome` | string | **sim** |  |
| `anexos` | lista de objeto | não |  |
| `anexos[].nome` | string | não |  |
| `anexos[].caminhoArquivo` | string | não |  |

**Respostas:**
- `202` Fabricante atualizado — row completa, confirmado batendo com o schema Fabricante. — campos: `id`, `nome`, `ativo`, `createdAt`, `updatedAt`
- `404` "Failed in Update Fabricante." — mensagem em inglês, inconsistente com o padrão em português do resto da API

### `DELETE /fabricantes/{id}`

- **Permissão:** `fabricante:delete` · **Manual:** [op-delete-fabricantes-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-delete-fabricantes-id)
- **Resumo:** Desativar fabricante
- **Descrição:** É uma **desativação** lógica, não uma exclusão física.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do fabricante |

**Respostas:**
- `200` **Corpo de sucesso é o número cru `201`**, não um objeto. — integer
- `404` "Failed in Delete Grupo Fabricante." — mensagem parece copy-paste de outro contexto ("Grupo Fabricante" não existe aqui)
