# Rotas — Estoque (12 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 -m ferramentas.rabi_api.atualizar_spec` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `GET /estoque`
- `GET /estoque/saldo-produtos`
- `GET /estoque/{id}`
- `GET /estoque/historico/{id}`
- `GET /estoque/ultima-compra/{id}`
- `GET /estoque/movimentacao/{id}`
- `GET /estoque/buscar/{lote}/{produtoId}/{localizacaoId}`
- `GET /estoque/lotes-produtos/{idProduto}/{idLocalizacao}`
- `POST /estoque/entrada`
- `POST /estoque/saida`
- `POST /estoque/transferencia`
- `POST /estoque/previsao`

### `GET /estoque`

- **Permissão:** `estoque:read` · **Manual:** [op-get-estoque](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-estoque)
- **Resumo:** Listar posições de estoque
- **Descrição:** Só linhas de **entrada** (movimentações de saída/transferência não aparecem aqui — use `/estoque/historico/{id}` pra ver todo o histórico de um produto).

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |
| `produtoId` | query | integer | não |  |
| `localizacaoId` | query | integer | não |  |

**Respostas:**
- `200` Lista paginada — campos: `dados`, `page`, `pageSize`, `total`, `totalPages`; item de `dados`: `id`, `produtoId`, `localizacaoId`, `quantidade`, `lote`, `validade`, `valorCompra`, `valorMedio`, `data`, `fornecedor`, `responsavel`, `localizacao`, `produto`

### `GET /estoque/saldo-produtos`

- **Permissão:** `estoque:read` · **Manual:** [op-get-estoque-saldo-produtos](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-estoque-saldo-produtos)
- **Resumo:** Saldo atual em estoque por produto
- **Descrição:** Quantidade calculada (soma de entradas menos saídas), não um campo fixo.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |
| `search` | query | string | não |  |

**Respostas:**
- `200` Lista paginada. Cada item tem todos os campos do cadastro do produto (`Fabricante`/`TipoProduto` incluídos) mais 3 campos calculados: `unidadeTotal` (saldo restante), `valor` (custo total em reais, já convertido) e `valorUnitario` (custo médio por unidade, em reais). A lista bruta de posições usada… — campos: `dados`, `total`, `page`, `pageSize`, `totalPages`; item de `dados`: `Fabricante`, `TipoProduto`, `unidadeTotal`, `valor`, `valorUnitario`

### `GET /estoque/{id}`

- **Permissão:** `estoque:read` · **Manual:** [op-get-estoque-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-estoque-id)
- **Resumo:** Consultar posição de estoque

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |

**Respostas:**
- `200` Posição de estoque — campos: `id`, `produtoId`, `localizacaoId`, `quantidade`, `lote`, `validade`, `TipoDeMovimentacaoId`
- `404` Posição não encontrada

### `GET /estoque/historico/{id}`

- **Permissão:** `estoque:read` · **Manual:** [op-get-estoque-historico-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-estoque-historico-id)
- **Resumo:** Histórico de movimentações de um produto
- **Descrição:** **Sem paginação real** apesar do nome do parâmetro `id` — devolve o histórico completo do produto sempre (o use case aceita `skip`/`take`, mas o controller nunca os lê da query, então nunca são usados). Linhas de entrada com `valorUnitarioEntrada <= 0` são removidas; saída e outros tipos são sempre mantidos.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do produto (não é o id da posição de estoque) |

**Respostas:**
- `200` Array direto (sem envelope de paginação) com o histórico completo do produto. — lista crua: `id`, `localizacaoId`, `produtoId`, `responsavelId`, `pacienteId`, `lote`, `validade`, `quantidade`, `qntUnitaria`, `valorCompra`, `valorVenda`, `valorMedio`, `valorUnitarioEntrada`, `valorUnitarioSaida`, `TipoDeMovimentacaoId`, `TipoDeMovimentacao`, `fornecedor`, `responsavel`, `paciente`, `motivo`, `produto`, `data`, `createdAt`
- `422` Falha ao buscar histórico de movimentações

### `GET /estoque/ultima-compra/{id}`

- **Permissão:** `estoque:read` · **Manual:** [op-get-estoque-ultima-compra-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-estoque-ultima-compra-id)
- **Resumo:** Última compra de um produto
- **Descrição:** Nunca lança erro de "não encontrado" — se não houver dados, os valores vêm `0`.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do produto |

**Respostas:**
- `200` Sempre 200, mesmo sem dados (valores ficam 0 nesse caso). — campos: `ultimaCompraUnitaria`, `ultimaCompraCompraCaixa`, `padraoCalcularUltimaCompra`

### `GET /estoque/movimentacao/{id}`

- **Permissão:** `estoque:read` · **Manual:** [op-get-estoque-movimentacao-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-estoque-movimentacao-id)
- **Resumo:** Consultar movimentação por id
- **Descrição:** `id` aqui é o id da própria posição de estoque (diferente de `/estoque/historico/{id}`, onde é o id do produto). **Sem conversão de centavos** (diferente de todas as outras rotas de estoque) e sem nenhum include de nome — só os campos crus do Prisma, com FKs como id.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |

**Respostas:**
- `200` Se `id` não existir, devolve **200 com corpo `null`** (não 404). — um de: object \\| null
- `422` Falha ao buscar movimentação de estoque

### `GET /estoque/buscar/{lote}/{produtoId}/{localizacaoId}`

- **Permissão:** `estoque:read` · **Manual:** [op-get-estoque-buscar-lote-produtoid-localizacaoid](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-estoque-buscar-lote-produtoid-localizacaoid)
- **Resumo:** Buscar posição por lote/produto/depósito
- **Descrição:** Só considera entradas com saldo positivo (`quantidade > 0`, `TipoDeMovimentacaoId=1`). Mesmo formato cru do `GET /estoque/movimentacao/{id}` — **sem conversão de centavos**, sem includes de nome.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `lote` | path | string | **sim** |  |
| `produtoId` | path | integer | **sim** |  |
| `localizacaoId` | path | integer | **sim** |  |

**Respostas:**
- `200` Se não achar, devolve **200 com corpo `null`** (não 404). — um de: object \\| null
- `422` Falha ao buscar posição de estoque

### `GET /estoque/lotes-produtos/{idProduto}/{idLocalizacao}`

- **Permissão:** `estoque:read` · **Manual:** [op-get-estoque-lotes-produtos-idproduto-idlocalizacao](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-estoque-lotes-produtos-idproduto-idlocalizacao)
- **Resumo:** Listar lotes disponíveis de um produto em um depósito
- **Descrição:** Mesmo controller e mesmo shape de `GET /estoque` — só entradas (`TipoDeMovimentacaoId=1`), com valores já convertidos para reais.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `idProduto` | path | integer | **sim** |  |
| `idLocalizacao` | path | integer | **sim** |  |
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |

**Respostas:**
- `200` Lista paginada — mesmo shape de item de `GET /estoque`. — campos: `dados`, `page`, `pageSize`, `total`, `totalPages`

### `POST /estoque/entrada`

- **Permissão:** `estoque:create` · **Manual:** [op-post-estoque-entrada](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-estoque-entrada)
- **Resumo:** Registrar entrada de estoque

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `responsavelId` | integer | **sim** | ID de um colaborador já cadastrado. |
| `produtoId` | integer | **sim** |  |
| `localizacaoId` | integer | **sim** | ID do depósito |
| `fornecedorId` | integer | não | aceita null |
| `motivoId` | integer | **sim** | ID de um motivo de movimentação do tipo ENTRADA |
| `lote` | string | não | aceita null |
| `observacoes` | string | não | aceita null |
| `produtoEmCaixaQuantidade` | string | não | valores: `UNIDADES`, `CAIXAS`; padrão `CAIXAS` |
| `notaFiscal` | string | não | aceita null |
| `validade` | string (date) | não | aceita null |
| `codIndividual` | string | não | aceita null |
| `valorCompra` | number | não | aceita null; Em reais |
| `quantidade` | integer | **sim** |  |
| `data` | string (date) | não | aceita null |

**Respostas:**
- `201` Entrada registrada — campos: `id`, `produtoId`, `localizacaoId`, `quantidade`, `lote`, `validade`, `TipoDeMovimentacaoId`
- `400` responsavelId ausente/inválido, ou campo obrigatório faltando
- `422` Falha ao registrar entrada de estoque

### `POST /estoque/saida`

- **Permissão:** `estoque:create` · **Manual:** [op-post-estoque-saida](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-estoque-saida)
- **Resumo:** Registrar saída de estoque
- **Descrição:** Recusada se não houver saldo suficiente, a não ser que `permitirNegativo: true`.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `responsavelId` | integer | **sim** |  |
| `produtoId` | integer | **sim** |  |
| `localizacaoId` | integer | **sim** |  |
| `motivoId` | integer | **sim** | ID de um motivo de movimentação do tipo SAIDA |
| `quantidade` | integer | **sim** |  |
| `permitirNegativo` | boolean | não | padrão `False` |
| `valorVenda` | number | não | aceita null |
| `lote` | string | não | aceita null |
| `validade` | string (date) | não | aceita null |
| `data` | string (date) | não | aceita null |
| `produtoEmCaixaQuantidade` | string | não | valores: `UNIDADES`, `CAIXAS`; padrão `CAIXAS` |

**Respostas:**
- `201` Saída registrada — campos: `id`, `produtoId`, `localizacaoId`, `quantidade`, `lote`, `validade`, `TipoDeMovimentacaoId`
- `400` responsavelId ausente/inválido, ou campo obrigatório faltando
- `422` Estoque insuficiente, motivo inválido para saída, ou depósito inativo

### `POST /estoque/transferencia`

- **Permissão:** `estoque:create` · **Manual:** [op-post-estoque-transferencia](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-estoque-transferencia)
- **Resumo:** Transferir estoque entre depósitos

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `responsavelId` | integer | **sim** |  |
| `produtoId` | integer | **sim** |  |
| `localizacaoId` | integer | **sim** | Depósito de origem |
| `localizacaoParaId` | integer | **sim** | Depósito de destino |
| `motivoId` | integer | **sim** |  |
| `quantidade` | integer | **sim** |  |
| `lote` | string | não | aceita null |
| `validade` | string (date) | não | aceita null |
| `produtoEmCaixaQuantidade` | string | não | valores: `UNIDADES`, `CAIXAS`; padrão `CAIXAS` |

**Respostas:**
- `201` Transferência registrada — campos: `id`, `produtoId`, `localizacaoId`, `quantidade`, `lote`, `validade`, `TipoDeMovimentacaoId`
- `400` responsavelId ausente/inválido, ou campo obrigatório faltando
- `404` Este depósito não possui este produto com este lote/validade
- `422` Estoque insuficiente para transferência

### `POST /estoque/previsao`

- **Permissão:** `estoque:read` · **Manual:** [op-post-estoque-previsao](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-estoque-previsao)
- **Resumo:** Previsão de consumo de estoque
- **Descrição:** Não envolve valores monetários, só quantidades.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `localId` | integer | **sim** |  |
| `dataAgendamento` | string (date-time) | não | aceita null; Se informado, considera compromissos concorrentes no período (`comprometido`/`previsto` passam a ser calculados de verdade). |
| `agendamentoId` | integer | não |  |
| `produtos` | lista de objeto | **sim** |  |
| `produtos[].produtoId` | integer | **sim** |  |
| `produtos[].quantidade` | number | não | aceita null |

**Respostas:**
- `200` Previsão por produto. — campos: `comDataEscolhida`, `depositoId`, `itens`
- `422` localId ausente ou produtos não é um array
