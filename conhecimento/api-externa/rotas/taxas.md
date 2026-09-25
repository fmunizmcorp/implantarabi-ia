# Rotas — Taxas (6 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 -m ferramentas.rabi_api.atualizar_spec` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `GET /taxas`
- `POST /taxas`
- `POST /taxas/bulk`
- `GET /taxas/{id}`
- `PUT /taxas/{id}`
- `DELETE /taxas/{id}`

### `GET /taxas`

- **Permissão:** `taxa:read` · **Manual:** [op-get-taxas](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-taxas)
- **Resumo:** Listar taxas

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |
| `ativo` | query | boolean | não | Sem informar, lista ativas e inativas. |

**Respostas:**
- `200` Lista paginada — campos: `page`, `pageSize`, `total`, `totalPages`, `dados`; item de `dados`: `id`, `taxas`, `descricao`, `codigoTaxa`, `valor`, `ativo`, `createdAt`, `updatedAt`, `tipoTaxa`

### `POST /taxas`

- **Permissão:** `taxa:create` · **Manual:** [op-post-taxas](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-taxas)
- **Resumo:** Cadastrar taxa

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `taxas` | string | **sim** |  |
| `descricao` | string | não | aceita null |
| `codigoTaxa` | string | **sim** |  |
| `tipoTaxaId` | integer | **sim** |  |
| `tipoCodigoId` | integer | não | aceita null |
| `tabelaANS87ID` | integer | não | aceita null |
| `valor` | number | **sim** | Em reais (não em centavos) |

**Respostas:**
- `200` Taxa criada — campos: `id`, `taxas`, `descricao`, `codigoTaxa`, `valor`, `ativo`, `createdAt`, `updatedAt`, `tipoTaxa`
- `422` Erro ao criar taxa (referência inválida)

### `POST /taxas/bulk`

- **Permissão:** `taxa:create` · **Manual:** [op-post-taxas-bulk](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-taxas-bulk)
- **Resumo:** Cadastrar várias taxas de uma vez
- **Descrição:** Até 50 itens por requisição (chave `taxas`). `207` = falha parcial, ver `resultados`; reenvie só os itens com erro.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `taxas` | lista de objeto | **sim** | máx. itens 50 |
| `taxas[].taxas` | string | **sim** |  |
| `taxas[].descricao` | string | não | aceita null |
| `taxas[].codigoTaxa` | string | **sim** |  |
| `taxas[].tipoTaxaId` | integer | **sim** |  |
| `taxas[].tipoCodigoId` | integer | não | aceita null |
| `taxas[].tabelaANS87ID` | integer | não | aceita null |
| `taxas[].valor` | number | **sim** | Em reais (não em centavos) |

**Respostas:**
- `201` Todas criadas — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `207` Falha parcial — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `400` Lote vazio ou acima de 50 itens
- `429` Já existe um lote em andamento para esta clínica e recurso

### `GET /taxas/{id}`

- **Permissão:** `taxa:read` · **Manual:** [op-get-taxas-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-taxas-id)
- **Resumo:** Consultar taxa

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID da taxa |

**Respostas:**
- `200` Taxa — campos: `id`, `taxas`, `descricao`, `codigoTaxa`, `valor`, `ativo`, `createdAt`, `updatedAt`, `tipoTaxa`
- `400` `id` inválido
- `404` Taxa não encontrada

### `PUT /taxas/{id}`

- **Permissão:** `taxa:update` · **Manual:** [op-put-taxas-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-taxas-id)
- **Resumo:** Atualizar taxa

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID da taxa |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `taxas` | string | **sim** |  |
| `descricao` | string | não | aceita null |
| `codigoTaxa` | string | **sim** |  |
| `tipoTaxaId` | integer | **sim** |  |
| `tipoCodigoId` | integer | não | aceita null |
| `tabelaANS87ID` | integer | não | aceita null |
| `valor` | number | **sim** | Em reais (não em centavos) |

**Respostas:**
- `200` Taxa atualizada — campos: `id`, `taxas`, `descricao`, `codigoTaxa`, `valor`, `ativo`, `createdAt`, `updatedAt`, `tipoTaxa`
- `422` Erro ao atualizar taxa (referência inválida)

### `DELETE /taxas/{id}`

- **Permissão:** `taxa:delete` · **Manual:** [op-delete-taxas-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-delete-taxas-id)
- **Resumo:** Desativar taxa
- **Descrição:** É uma **desativação** lógica — mas diferente dos outros cadastros, o model `Taxas` não tem campo `ativo`; usa `delete: true` (mapeado pra coluna `deleted`), é o único recurso desta lista que funciona assim.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID da taxa |

**Respostas:**
- `200` **Corpo de sucesso é o número cru `201`**, não um objeto. — integer
- `422` Erro ao excluir taxa
