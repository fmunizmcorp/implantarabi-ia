# Rotas — Fornecedores (5 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 ferramentas/rabi_api/atualizar_spec.py` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `GET /fornecedores`
- `POST /fornecedores`
- `POST /fornecedores/bulk`
- `GET /fornecedores/{id}`
- `PUT /fornecedores/{id}`

### `GET /fornecedores`

- **Permissão:** `fornecedor:read` · **Manual:** [op-get-fornecedores](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-fornecedores)
- **Resumo:** Listar fornecedores

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |
| `search` | query | string | não | Busca por nome ou CNPJ |

**Respostas:**
- `200` Lista paginada — campos: `page`, `pageSize`, `total`, `totalPages`, `dados`; item de `dados`: `id`, `nome`, `cnpj`, `inscricao`, `telefoneFornecedor`, `enderecoId`, `ativo`, `tipoPrestadorDeServico`, `createdAt`, `updatedAt`

### `POST /fornecedores`

- **Permissão:** `fornecedor:create` · **Manual:** [op-post-fornecedores](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-fornecedores)
- **Resumo:** Cadastrar fornecedor

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `nome` | string | **sim** |  |
| `cnpj` | string | **sim** | Com ou sem máscara |
| `inscricao` | string | **sim** |  |
| `telefoneFornecedor` | string | **sim** |  |
| `enderecoId` | integer | não | aceita null |
| `ativo` | boolean | não | padrão `True` |
| `tipoPrestadorDeServico` | string | não | aceita null |

**Respostas:**
- `201` Fornecedor criado — campos: `id`, `nome`, `cnpj`, `inscricao`, `telefoneFornecedor`, `enderecoId`, `ativo`, `tipoPrestadorDeServico`, `createdAt`, `updatedAt`
- `400` Dados inválidos

### `POST /fornecedores/bulk`

- **Permissão:** `fornecedor:create` · **Manual:** [op-post-fornecedores-bulk](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-fornecedores-bulk)
- **Resumo:** Cadastrar vários fornecedores de uma vez
- **Descrição:** Até 50 itens por requisição (chave `fornecedores`). `207` = falha parcial, ver `resultados`; reenvie só os itens com erro.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `fornecedores` | lista de objeto | **sim** | máx. itens 50 |
| `fornecedores[].nome` | string | **sim** |  |
| `fornecedores[].cnpj` | string | **sim** | Com ou sem máscara |
| `fornecedores[].inscricao` | string | **sim** |  |
| `fornecedores[].telefoneFornecedor` | string | **sim** |  |
| `fornecedores[].enderecoId` | integer | não | aceita null |
| `fornecedores[].ativo` | boolean | não | padrão `True` |
| `fornecedores[].tipoPrestadorDeServico` | string | não | aceita null |

**Respostas:**
- `201` Todos criados — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `207` Falha parcial — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `400` Lote vazio ou acima de 50 itens
- `429` Já existe um lote em andamento para esta clínica e recurso

### `GET /fornecedores/{id}`

- **Permissão:** `fornecedor:read` · **Manual:** [op-get-fornecedores-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-fornecedores-id)
- **Resumo:** Consultar fornecedor
- **Descrição:** Inclui endereço e contatos.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do fornecedor |

**Respostas:**
- `200` Fornecedor — campos: `id`, `nome`, `cnpj`, `inscricao`, `telefoneFornecedor`, `enderecoId`, `ativo`, `tipoPrestadorDeServico`, `createdAt`, `updatedAt`
- `404` Fornecedor não encontrado

### `PUT /fornecedores/{id}`

- **Permissão:** `fornecedor:update` · **Manual:** [op-put-fornecedores-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-fornecedores-id)
- **Resumo:** Atualizar fornecedor

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do fornecedor |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `nome` | string | **sim** |  |
| `cnpj` | string | **sim** | Com ou sem máscara |
| `inscricao` | string | **sim** |  |
| `telefoneFornecedor` | string | **sim** |  |
| `enderecoId` | integer | não | aceita null |
| `ativo` | boolean | não | padrão `True` |
| `tipoPrestadorDeServico` | string | não | aceita null |

**Respostas:**
- `200` Fornecedor atualizado — campos: `id`, `nome`, `cnpj`, `inscricao`, `telefoneFornecedor`, `enderecoId`, `ativo`, `tipoPrestadorDeServico`, `createdAt`, `updatedAt`
- `400` Dados inválidos
