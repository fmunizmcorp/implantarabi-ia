# Rotas — Equipamentos (6 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 -m ferramentas.rabi_api.atualizar_spec` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `GET /equipamentos`
- `POST /equipamentos`
- `POST /equipamentos/bulk`
- `GET /equipamentos/{id}`
- `PUT /equipamentos/{id}`
- `DELETE /equipamentos/{id}`

### `GET /equipamentos`

- **Permissão:** `equipamento:read` · **Manual:** [op-get-equipamentos](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-equipamentos)
- **Resumo:** Listar equipamentos

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |
| `ativo` | query | boolean | não | Sem informar, lista ativos e inativos. |

**Respostas:**
- `200` Lista paginada — campos: `page`, `pageSize`, `total`, `totalPages`, `dados`; item de `dados`: `id`, `nome`, `ativo`, `createdAt`, `updatedAt`

### `POST /equipamentos`

- **Permissão:** `equipamento:create` · **Manual:** [op-post-equipamentos](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-equipamentos)
- **Resumo:** Cadastrar equipamento
- **Descrição:** Recusa (`409`) se já existir um equipamento ativo com o mesmo nome.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `nome` | string | **sim** |  |

**Respostas:**
- `201` Equipamento criado — campos: `id`, `nome`, `ativo`, `createdAt`, `updatedAt`
- `409` Este equipamento já foi cadastrado

### `POST /equipamentos/bulk`

- **Permissão:** `equipamento:create` · **Manual:** [op-post-equipamentos-bulk](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-equipamentos-bulk)
- **Resumo:** Cadastrar vários equipamentos de uma vez
- **Descrição:** Até 50 itens por requisição (chave `equipamentos`). `207` = falha parcial, ver `resultados`; reenvie só os itens com erro.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `equipamentos` | lista de objeto | **sim** | máx. itens 50 |
| `equipamentos[].nome` | string | **sim** |  |

**Respostas:**
- `201` Todos criados — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `207` Falha parcial — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `400` Lote vazio ou acima de 50 itens
- `429` Já existe um lote em andamento para esta clínica e recurso

### `GET /equipamentos/{id}`

- **Permissão:** `equipamento:read` · **Manual:** [op-get-equipamentos-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-equipamentos-id)
- **Resumo:** Consultar equipamento

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do equipamento |

**Respostas:**
- `200` Equipamento — campos: `id`, `nome`, `ativo`, `createdAt`, `updatedAt`
- `404` Equipamento não encontrado

### `PUT /equipamentos/{id}`

- **Permissão:** `equipamento:update` · **Manual:** [op-put-equipamentos-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-equipamentos-id)
- **Resumo:** Atualizar equipamento
- **Descrição:** Recusa (`422`) se já existir outro equipamento ativo com o mesmo nome.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do equipamento |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `nome` | string | **sim** |  |

**Respostas:**
- `202` Equipamento atualizado — campos: `id`, `nome`, `ativo`, `createdAt`, `updatedAt`
- `422` Nome já usado por outro equipamento

### `DELETE /equipamentos/{id}`

- **Permissão:** `equipamento:delete` · **Manual:** [op-delete-equipamentos-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-delete-equipamentos-id)
- **Resumo:** Desativar equipamento
- **Descrição:** É uma **desativação** (`ativo = false`), não uma exclusão física.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do equipamento |

**Respostas:**
- `200` **Corpo de sucesso é o número cru `201`**, não um objeto. — integer
- `404` Equipamento não encontrado
