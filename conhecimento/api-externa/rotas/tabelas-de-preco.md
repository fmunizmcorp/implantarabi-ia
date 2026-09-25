# Rotas — Tabelas de Preço (8 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 -m ferramentas.rabi_api.atualizar_spec` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `GET /tabelas-preco`
- `POST /tabelas-preco`
- `GET /tabelas-preco/{id}`
- `PUT /tabelas-preco/{id}`
- `GET /tabelas-preco/precificacao`
- `GET /tabelas-preco/produtos`
- `POST /tabelas-preco/produtos`
- `POST /tabelas-preco/produtos/bulk`

### `GET /tabelas-preco`

- **Permissão:** `tabelaPreco:read` · **Manual:** [op-get-tabelas-preco](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-tabelas-preco)
- **Resumo:** Listar tabelas de preço

**Respostas:**
- `200` Lista — lista crua de `TabelaPreco`: `id`, `nome`, `descricao`, `immutable`, `tipoPrecificacao1`, `tipoPrecificacao2`, `tipoPrecificacao3`, `ativo`, `createdAt`, `updatedAt`, `deleted`

### `POST /tabelas-preco`

- **Permissão:** `tabelaPreco:create` · **Manual:** [op-post-tabelas-preco](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-tabelas-preco)
- **Resumo:** Cadastrar tabela de preço

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `name` | string | **sim** |  |
| `description` | string | não | aceita null |
| `priceType1` | string | **sim** |  |
| `priceType2` | string | não | aceita null |
| `priceType3` | string | não | aceita null |

**Respostas:**
- `201` Tabela criada — campos: `id`, `nome`, `descricao`, `immutable`, `tipoPrecificacao1`, `tipoPrecificacao2`, `tipoPrecificacao3`, `ativo`, `createdAt`, `updatedAt`, `deleted`

### `GET /tabelas-preco/{id}`

- **Permissão:** `tabelaPreco:read` · **Manual:** [op-get-tabelas-preco-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-tabelas-preco-id)
- **Resumo:** Consultar tabela de preço

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |

**Respostas:**
- `200` Tabela de preço — campos: `id`, `nome`, `descricao`, `immutable`, `tipoPrecificacao1`, `tipoPrecificacao2`, `tipoPrecificacao3`, `ativo`, `createdAt`, `updatedAt`, `deleted`
- `404` Tabela não encontrada

### `PUT /tabelas-preco/{id}`

- **Permissão:** `tabelaPreco:update` · **Manual:** [op-put-tabelas-preco-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-tabelas-preco-id)
- **Resumo:** Atualizar tabela de preço
- **Descrição:** **`nome` é forçado para MAIÚSCULAS no servidor**, mesmo enviando minúsculas/misto.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `name` | string | **sim** |  |
| `description` | string | não | aceita null |
| `priceType1` | string | **sim** |  |
| `priceType2` | string | não | aceita null |
| `priceType3` | string | não | aceita null |

**Respostas:**
- `200` Row completa, sem include. — campos: `id`, `nome`, `descricao`, `immutable`, `tipoPrecificacao1`, `tipoPrecificacao2`, `tipoPrecificacao3`, `ativo`, `createdAt`, `updatedAt`, `deleted`
- `404` Tabela não encontrada

### `GET /tabelas-preco/precificacao`

- **Permissão:** `tabelaPreco:read` · **Manual:** [op-get-tabelas-preco-precificacao](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-tabelas-preco-precificacao)
- **Resumo:** Listar tabelas com sua precificação
- **Descrição:** Não é a lista de tabelas em si — é a lista de **opções de precificação selecionáveis** (uma tabela pode gerar até 3 opções, uma por `tipoPrecificacao1/2/3` configurado, ou 1 opção sem tipo se a tabela for `immutable` e não tiver nenhum tipo configurado). Sem envelope de paginação.

**Respostas:**
- `200` Array direto. — lista crua: `id`, `idJson`, `fontePrecoId`, `nome`, `tipoPrecificacao`

### `GET /tabelas-preco/produtos`

- **Permissão:** `tabelaPreco:read` · **Manual:** [op-get-tabelas-preco-produtos](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-tabelas-preco-produtos)
- **Resumo:** Listar preço de produtos dentro de uma tabela
- **Descrição:** **Não usa o envelope padrão `{dados, page, pageSize, total, totalPages}`** desta API — devolve `{data, meta}` cru do use case interno.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | query | integer | não | ID da tabela de preço |
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |

**Respostas:**
- `200` Lista paginada — shape próprio, fora do padrão. — campos: `data`, `meta`; item de `data`: `nome`, `id`, `tabelaPrecoInterna`

### `POST /tabelas-preco/produtos`

- **Permissão:** `tabelaPreco:update` · **Manual:** [op-post-tabelas-preco-produtos](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-tabelas-preco-produtos)
- **Resumo:** Cadastrar/atualizar preço de um produto na tabela
- **Descrição:** É upsert — chamar de novo com o mesmo `productId`/`purchasePriceSourceId` atualiza o preço em vez de duplicar. **Bug conhecido: a resposta não espera a gravação terminar** (`execute()` chama o repository sem `await` nem `return`) — o corpo devolvido é vazio (`undefined`), e a chamada pode responder sucesso antes mesmo do preço estar de fato salvo. Reportado ao time; para confirmar a gravação, faça um `GET /tabelas-preco/produtos` logo em seguida.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `purchasePriceSourceId` | integer | **sim** | ID da tabela de preço |
| `productId` | integer | **sim** |  |
| `parcelas_maximas` | integer | não | aceita null |
| `productCode` | string | não | aceita null |
| `productCodeTypeId` | integer | não | aceita null |
| `priceType1` | number | não | aceita null |
| `priceType2` | number | não | aceita null |
| `priceType3` | number | não | aceita null |

**Respostas:**
- `200` Corpo vazio — ver descrição sobre o bug de gravação não aguardada.

### `POST /tabelas-preco/produtos/bulk`

- **Permissão:** `tabelaPreco:update` · **Manual:** [op-post-tabelas-preco-produtos-bulk](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-tabelas-preco-produtos-bulk)
- **Resumo:** Cadastrar/atualizar preço de vários produtos de uma vez
- **Descrição:** Até 200 itens por requisição (chave `precos`). `207` = falha parcial.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `precos` | lista de objeto | **sim** | máx. itens 200 |
| `precos[].purchasePriceSourceId` | integer | **sim** | ID da tabela de preço |
| `precos[].productId` | integer | **sim** |  |
| `precos[].parcelas_maximas` | integer | não | aceita null |
| `precos[].productCode` | string | não | aceita null |
| `precos[].productCodeTypeId` | integer | não | aceita null |
| `precos[].priceType1` | number | não | aceita null |
| `precos[].priceType2` | number | não | aceita null |
| `precos[].priceType3` | number | não | aceita null |

**Respostas:**
- `201` Todos processados — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `207` Falha parcial — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `400` Lote vazio ou acima de 200 itens
- `429` Já existe um lote em andamento para esta clínica e recurso
