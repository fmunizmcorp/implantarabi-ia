# Rotas — Produtos (6 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 -m ferramentas.rabi_api.atualizar_spec` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `GET /produtos`
- `POST /produtos`
- `POST /produtos/bulk`
- `GET /produtos/{id}`
- `PUT /produtos/{id}`
- `DELETE /produtos/{id}`

### `GET /produtos`

- **Permissão:** `produto:read` · **Manual:** [op-get-produtos](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-produtos)
- **Resumo:** Listar produtos

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |
| `ativo` | query | boolean | não | Sem informar, lista ativos e inativos. |
| `nome` | query | string | não | Filtro por nome (contém, sem diferenciar maiúsculas) |

**Respostas:**
- `200` Lista paginada — campos: `page`, `pageSize`, `total`, `totalPages`, `dados`; item de `dados`: `id`, `nome`, `codigoProduto`, `codigoEAN`, `codigoNCM`, `apresentacao`, `contendo`, `valorUnitario`, `permitirEstoqueNegativo`, `prazoDeReposicao`, `ativo`, `createdAt`, `updatedAt`, `TipoProduto`, `Fabricante`, `deposito`, `UnidadeDeMedida`

### `POST /produtos`

- **Permissão:** `produto:create` · **Manual:** [op-post-produtos](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-produtos)
- **Resumo:** Cadastrar produto

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `nome` | string | **sim** |  |
| `codigoProduto` | string | **sim** |  |
| `codigoEAN` | integer | não | aceita null |
| `codigoNCM` | integer | não | aceita null |
| `apresentacao` | string | **sim** |  |
| `contendo` | integer | **sim** | Quantidade na embalagem |
| `depositoId` | integer | **sim** |  |
| `tipoProdutoId` | integer | **sim** |  |
| `fabricanteId` | integer | **sim** |  |
| `principioAtivoId` | integer | não | aceita null |
| `unidadeDeMedidaId` | integer | **sim** |  |
| `cdId` | integer | não | aceita null |
| `tipoCodigoId` | integer | não | aceita null |
| `tabelaANS87ID` | integer | não | aceita null |
| `estoquePodeNegativar` | boolean | não | padrão `False` |
| `prazoDeReposicao` | integer | **sim** | Em dias |
| `precoUltimaPesquisa` | number | não | aceita null |
| `dataUltimaPesquisa` | string (date-time) | não | aceita null |
| `fornecedores` | lista de integer | não | IDs dos fornecedores |
| `anexos` | lista de objeto | não |  |
| `anexos[].nome` | string | não | aceita null |
| `anexos[].caminhoArquivo` | string | não | aceita null; Referência a um arquivo já enviado — esta API não faz upload de anexo de produto. |

**Respostas:**
- `201` Produto criado — campos: `id`, `nome`, `codigoProduto`, `codigoEAN`, `codigoNCM`, `apresentacao`, `contendo`, `valorUnitario`, `permitirEstoqueNegativo`, `prazoDeReposicao`, `ativo`, `createdAt`, `updatedAt`, `TipoProduto`, `Fabricante`, `deposito`, `UnidadeDeMedida`
- `422` Falha ao criar produto (referência inválida)

### `POST /produtos/bulk`

- **Permissão:** `produto:create` · **Manual:** [op-post-produtos-bulk](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-produtos-bulk)
- **Resumo:** Cadastrar vários produtos de uma vez
- **Descrição:** Até 50 itens por requisição (chave `produtos`). `207` = falha parcial, ver `resultados`; reenvie só os itens com erro.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `produtos` | lista de objeto | **sim** | máx. itens 50 |
| `produtos[].nome` | string | **sim** |  |
| `produtos[].codigoProduto` | string | **sim** |  |
| `produtos[].codigoEAN` | integer | não | aceita null |
| `produtos[].codigoNCM` | integer | não | aceita null |
| `produtos[].apresentacao` | string | **sim** |  |
| `produtos[].contendo` | integer | **sim** | Quantidade na embalagem |
| `produtos[].depositoId` | integer | **sim** |  |
| `produtos[].tipoProdutoId` | integer | **sim** |  |
| `produtos[].fabricanteId` | integer | **sim** |  |
| `produtos[].principioAtivoId` | integer | não | aceita null |
| `produtos[].unidadeDeMedidaId` | integer | **sim** |  |
| `produtos[].cdId` | integer | não | aceita null |
| `produtos[].tipoCodigoId` | integer | não | aceita null |
| `produtos[].tabelaANS87ID` | integer | não | aceita null |
| `produtos[].estoquePodeNegativar` | boolean | não | padrão `False` |
| `produtos[].prazoDeReposicao` | integer | **sim** | Em dias |
| `produtos[].precoUltimaPesquisa` | number | não | aceita null |
| `produtos[].dataUltimaPesquisa` | string (date-time) | não | aceita null |
| `produtos[].fornecedores` | lista de integer | não | IDs dos fornecedores |
| `produtos[].anexos` | lista de objeto | não |  |
| `produtos[].anexos[].nome` | string | não | aceita null |
| `produtos[].anexos[].caminhoArquivo` | string | não | aceita null; Referência a um arquivo já enviado — esta API não faz upload de anexo de produto. |

**Respostas:**
- `201` Todos criados — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `207` Falha parcial — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `400` Lote vazio ou acima de 50 itens
- `429` Já existe um lote em andamento para esta clínica e recurso

### `GET /produtos/{id}`

- **Permissão:** `produto:read` · **Manual:** [op-get-produtos-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-produtos-id)
- **Resumo:** Consultar produto

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do produto |

**Respostas:**
- `200` Produto — campos: `id`, `nome`, `codigoProduto`, `codigoEAN`, `codigoNCM`, `apresentacao`, `contendo`, `valorUnitario`, `permitirEstoqueNegativo`, `prazoDeReposicao`, `ativo`, `createdAt`, `updatedAt`, `TipoProduto`, `Fabricante`, `deposito`, `UnidadeDeMedida`
- `400` `id` inválido
- `404` Produto não encontrado

### `PUT /produtos/{id}`

- **Permissão:** `produto:update` · **Manual:** [op-put-produtos-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-produtos-id)
- **Resumo:** Atualizar produto
- **Descrição:** **Status HTTP real é 200, não 202.** Devolve a row crua do Prisma (`update` sem `include`) — FKs como `fabricanteId`/`tipoProdutoId`/`depositoId`/etc aparecem como inteiros, não como os objetos aninhados que o schema `Produto` usa nas rotas de leitura (aquele formato só existe nos GETs, que fazem include). `fornecedores` e `anexos` enviados no corpo são persistidos, mas não aparecem na resposta.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do produto |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `nome` | string | **sim** |  |
| `codigoProduto` | string | **sim** |  |
| `codigoEAN` | integer | não | aceita null |
| `codigoNCM` | integer | não | aceita null |
| `apresentacao` | string | **sim** |  |
| `contendo` | integer | **sim** | Quantidade na embalagem |
| `depositoId` | integer | **sim** |  |
| `tipoProdutoId` | integer | **sim** |  |
| `fabricanteId` | integer | **sim** |  |
| `principioAtivoId` | integer | não | aceita null |
| `unidadeDeMedidaId` | integer | **sim** |  |
| `cdId` | integer | não | aceita null |
| `tipoCodigoId` | integer | não | aceita null |
| `tabelaANS87ID` | integer | não | aceita null |
| `estoquePodeNegativar` | boolean | não | padrão `False` |
| `prazoDeReposicao` | integer | **sim** | Em dias |
| `precoUltimaPesquisa` | number | não | aceita null |
| `dataUltimaPesquisa` | string (date-time) | não | aceita null |
| `fornecedores` | lista de integer | não | IDs dos fornecedores |
| `anexos` | lista de objeto | não |  |
| `anexos[].nome` | string | não | aceita null |
| `anexos[].caminhoArquivo` | string | não | aceita null; Referência a um arquivo já enviado — esta API não faz upload de anexo de produto. |

**Respostas:**
- `200` Row crua de Produto, sem includes — ver descrição. — object

### `DELETE /produtos/{id}`

- **Permissão:** `produto:delete` · **Manual:** [op-delete-produtos-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-delete-produtos-id)
- **Resumo:** Desativar produto
- **Descrição:** É uma **desativação** (`ativo = false`), não uma exclusão física. Também desativa os fornecedores vinculados e remove a configuração de estoque do produto (hard delete). Se qualquer passo falhar, a mensagem de erro ("Não autorizado.") é enganosa — pode ser erro de integridade/not-found, não de permissão.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do produto |

**Respostas:**
- `200` **Corpo de sucesso é o número cru `201`**, não um objeto. — integer
