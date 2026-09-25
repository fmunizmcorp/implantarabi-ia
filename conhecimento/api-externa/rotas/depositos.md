# Rotas — Depósitos (6 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 -m ferramentas.rabi_api.atualizar_spec` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `GET /depositos`
- `POST /depositos`
- `POST /depositos/bulk`
- `GET /depositos/{id}`
- `PUT /depositos/{id}`
- `DELETE /depositos/{id}`

### `GET /depositos`

- **Permissão:** `deposito:read` · **Manual:** [op-get-depositos](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-depositos)
- **Resumo:** Listar depósitos

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |
| `ativo` | query | boolean | não |  |

**Respostas:**
- `200` Lista paginada — campos: `page`, `pageSize`, `total`, `totalPages`, `dados`; item de `dados`: `id`, `descricaoDeposito`, `empresaId`, `produtoId`, `ativo`, `createdAt`, `updatedAt`

### `POST /depositos`

- **Permissão:** `deposito:create` · **Manual:** [op-post-depositos](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-depositos)
- **Resumo:** Cadastrar depósito

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `empresaId` | integer | **sim** |  |
| `descricaoDeposito` | string | **sim** |  |

**Respostas:**
- `201` Depósito criado — campos: `id`, `descricaoDeposito`, `empresaId`, `produtoId`, `ativo`, `createdAt`, `updatedAt`
- `409` Já existe um depósito com este nome nesta unidade

### `POST /depositos/bulk`

- **Permissão:** `deposito:create` · **Manual:** [op-post-depositos-bulk](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-depositos-bulk)
- **Resumo:** Cadastrar vários depósitos de uma vez
- **Descrição:** Até 50 itens por requisição (chave `depositos`). `207` = falha parcial.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `depositos` | lista de objeto | **sim** | máx. itens 50 |
| `depositos[].empresaId` | integer | **sim** |  |
| `depositos[].descricaoDeposito` | string | **sim** |  |

**Respostas:**
- `201` Todos criados — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `207` Falha parcial — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `400` Lote vazio ou acima de 50 itens
- `429` Já existe um lote em andamento para esta clínica e recurso

### `GET /depositos/{id}`

- **Permissão:** `deposito:read` · **Manual:** [op-get-depositos-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-depositos-id)
- **Resumo:** Consultar depósito

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do depósito |

**Respostas:**
- `200` Depósito — campos: `id`, `descricaoDeposito`, `empresaId`, `produtoId`, `ativo`, `createdAt`, `updatedAt`
- `404` Depósito não encontrado

### `PUT /depositos/{id}`

- **Permissão:** `deposito:update` · **Manual:** [op-put-depositos-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-depositos-id)
- **Resumo:** Atualizar depósito
- **Descrição:** Bloqueia nome duplicado ativo na mesma empresa (`409`).

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do depósito |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `empresaId` | integer | **sim** |  |
| `descricaoDeposito` | string | **sim** |  |

**Respostas:**
- `200` Row crua, sem include — confirmado batendo com o schema Deposito, com uma ressalva: o real também tem `produtoId` (integer, nullable), não documentado no schema hoje. — campos: `id`, `descricaoDeposito`, `empresaId`, `produtoId`, `ativo`, `createdAt`, `updatedAt`
- `404` Depósito não encontrado
- `409` Já existe um depósito ativo com este nome nesta empresa

### `DELETE /depositos/{id}`

- **Permissão:** `deposito:delete` · **Manual:** [op-delete-depositos-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-delete-depositos-id)
- **Resumo:** Desativar depósito
- **Descrição:** Desativação lógica, não exclusão física.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do depósito |

**Respostas:**
- `200` **Corpo de sucesso é o número cru `201`**, não um objeto. — integer
- `404` "Failed in Delete Deposito." — mensagem em inglês, inconsistente com o padrão em português do resto da API
