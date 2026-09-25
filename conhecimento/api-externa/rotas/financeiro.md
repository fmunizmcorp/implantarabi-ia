# Rotas — Financeiro (5 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 ferramentas/rabi_api/atualizar_spec.py` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `GET /financeiro/movimentacoes`
- `POST /financeiro/movimentacoes`
- `POST /financeiro/movimentacoes/bulk`
- `GET /financeiro/movimentacoes/{id}`
- `PUT /financeiro/movimentacoes/{id}`

### `GET /financeiro/movimentacoes`

- **Permissão:** `financeiro:read` · **Manual:** [op-get-financeiro-movimentacoes](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-financeiro-movimentacoes)
- **Resumo:** Listar movimentações financeiras

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |
| `search` | query | string | não |  |

**Respostas:**
- `200` Lista paginada — campos: `page`, `pageSize`, `total`, `totalPages`, `dados`; item de `dados`: `id`, `tipoMovimentacaoFinanceira`, `tipoFinanceiro`, `contasCaixaId`, `data`, `observacoes`, `createdAt`

### `POST /financeiro/movimentacoes`

- **Permissão:** `financeiro:create` · **Manual:** [op-post-financeiro-movimentacoes](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-financeiro-movimentacoes)
- **Resumo:** Cadastrar movimentação financeira
- **Descrição:** **Pode disparar emissão automática de NFS-e** dependendo da configuração do emitente.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `responsavelId` | integer | **sim** | ID de um colaborador já cadastrado, responsável por esta movimentação. |
| `tipoMovimentacaoFinanceira` | string | **sim** | valores: `PACIENTE`, `COLABORADOR`, `FORNECEDOR`, `CONVENIO`, `EMPRESA` |
| `tipoFinanceiro` | string | **sim** | valores: `PAGAMENTO`, `RECEBIMENTO` |
| `categoriaDePagamentoId` | integer | **sim** |  |
| `contasCaixaId` | integer | **sim** |  |
| `data` | string (date) | **sim** |  |
| `fornecedorId` | integer | não | aceita null |
| `pacienteId` | integer | não | aceita null |
| `colaboradorId` | integer | não | aceita null |
| `convenioId` | integer | não | aceita null |
| `centroDeCustoId` | integer | não | aceita null |
| `observacoes` | string | não | aceita null |
| `notaFiscal` | string | não | aceita null |
| `parcelas` | integer | **sim** |  |
| `descontoGeral` | number | não | aceita null |
| `registroFinanceiro` | lista de objeto | **sim** |  |
| `registroFinanceiro[].quantidade` | integer | **sim** |  |
| `registroFinanceiro[].valorUnitario` | number | **sim** |  |
| `registroFinanceiro[].contendo` | integer | **sim** |  |
| `registroFinanceiro[].centroDeCustoId` | integer | **sim** |  |
| `registroFinanceiro[].tipoConta` | string | **sim** |  |
| `registroFinanceiro[].tipoConjunto` | string | **sim** |  |
| `registroFinanceiro[].descricao` | string | não | aceita null |
| `registroFinanceiro[].produtoId` | integer | não | aceita null |
| `registroFinanceiro[].fornecedorId` | integer | não | aceita null |
| `registroFinanceiro[].contasCaixasId` | integer | não | aceita null |
| `duplicatas` | lista de objeto | não |  |
| `duplicatas[].vencimento` | string (date) | não |  |
| `duplicatas[].observacao` | string | não | aceita null |
| `duplicatas[].valor` | number | não |  |
| `duplicatas[].aVista` | boolean | não |  |
| `duplicatas[].valorPago` | number | não | aceita null |
| `duplicatas[].pago` | boolean | não | padrão `False` |
| `duplicatas[].dataPagamento` | string (date) | não | aceita null |
| `duplicatas[].tipoDePagamentoId` | integer | não | aceita null |
| `duplicatas[].contaCaixaId` | integer | não | aceita null |

**Respostas:**
- `201` Movimentação criada — campos: `id`, `tipoMovimentacaoFinanceira`, `tipoFinanceiro`, `contasCaixaId`, `data`, `observacoes`, `createdAt`
- `400` responsavelId ausente/inválido, ou conta caixa não encontrada

### `POST /financeiro/movimentacoes/bulk`

- **Permissão:** `financeiro:create` · **Manual:** [op-post-financeiro-movimentacoes-bulk](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-financeiro-movimentacoes-bulk)
- **Resumo:** Cadastrar várias movimentações financeiras de uma vez
- **Descrição:** Até 50 itens por requisição (chave `movimentacoes`), todos com o mesmo `responsavelId`. `207` = falha parcial.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `responsavelId` | integer | **sim** |  |
| `movimentacoes` | lista de objeto | **sim** | máx. itens 50 |
| `movimentacoes[].responsavelId` | integer | **sim** | ID de um colaborador já cadastrado, responsável por esta movimentação. |
| `movimentacoes[].tipoMovimentacaoFinanceira` | string | **sim** | valores: `PACIENTE`, `COLABORADOR`, `FORNECEDOR`, `CONVENIO`, `EMPRESA` |
| `movimentacoes[].tipoFinanceiro` | string | **sim** | valores: `PAGAMENTO`, `RECEBIMENTO` |
| `movimentacoes[].categoriaDePagamentoId` | integer | **sim** |  |
| `movimentacoes[].contasCaixaId` | integer | **sim** |  |
| `movimentacoes[].data` | string (date) | **sim** |  |
| `movimentacoes[].fornecedorId` | integer | não | aceita null |
| `movimentacoes[].pacienteId` | integer | não | aceita null |
| `movimentacoes[].colaboradorId` | integer | não | aceita null |
| `movimentacoes[].convenioId` | integer | não | aceita null |
| `movimentacoes[].centroDeCustoId` | integer | não | aceita null |
| `movimentacoes[].observacoes` | string | não | aceita null |
| `movimentacoes[].notaFiscal` | string | não | aceita null |
| `movimentacoes[].parcelas` | integer | **sim** |  |
| `movimentacoes[].descontoGeral` | number | não | aceita null |
| `movimentacoes[].registroFinanceiro` | lista de objeto | **sim** |  |
| `movimentacoes[].registroFinanceiro[].quantidade` | integer | **sim** |  |
| `movimentacoes[].registroFinanceiro[].valorUnitario` | number | **sim** |  |
| `movimentacoes[].registroFinanceiro[].contendo` | integer | **sim** |  |
| `movimentacoes[].registroFinanceiro[].centroDeCustoId` | integer | **sim** |  |
| `movimentacoes[].registroFinanceiro[].tipoConta` | string | **sim** |  |
| `movimentacoes[].registroFinanceiro[].tipoConjunto` | string | **sim** |  |
| `movimentacoes[].registroFinanceiro[].descricao` | string | não | aceita null |
| `movimentacoes[].registroFinanceiro[].produtoId` | integer | não | aceita null |
| `movimentacoes[].registroFinanceiro[].fornecedorId` | integer | não | aceita null |
| `movimentacoes[].registroFinanceiro[].contasCaixasId` | integer | não | aceita null |
| `movimentacoes[].duplicatas` | lista de objeto | não |  |
| `movimentacoes[].duplicatas[].vencimento` | string (date) | não |  |
| `movimentacoes[].duplicatas[].observacao` | string | não | aceita null |
| `movimentacoes[].duplicatas[].valor` | number | não |  |
| `movimentacoes[].duplicatas[].aVista` | boolean | não |  |
| `movimentacoes[].duplicatas[].valorPago` | number | não | aceita null |
| `movimentacoes[].duplicatas[].pago` | boolean | não | padrão `False` |
| `movimentacoes[].duplicatas[].dataPagamento` | string (date) | não | aceita null |
| `movimentacoes[].duplicatas[].tipoDePagamentoId` | integer | não | aceita null |
| `movimentacoes[].duplicatas[].contaCaixaId` | integer | não | aceita null |

**Respostas:**
- `201` Todas criadas — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `207` Falha parcial — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `400` Lote vazio ou acima de 50 itens
- `429` Já existe um lote em andamento para esta clínica e recurso

### `GET /financeiro/movimentacoes/{id}`

- **Permissão:** `financeiro:read` · **Manual:** [op-get-financeiro-movimentacoes-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-financeiro-movimentacoes-id)
- **Resumo:** Consultar movimentação financeira

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |

**Respostas:**
- `200` Movimentação — campos: `id`, `tipoMovimentacaoFinanceira`, `tipoFinanceiro`, `contasCaixaId`, `data`, `observacoes`, `createdAt`
- `404` Movimentação não encontrada

### `PUT /financeiro/movimentacoes/{id}`

- **Permissão:** `financeiro:update` · **Manual:** [op-put-financeiro-movimentacoes-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-put-financeiro-movimentacoes-id)
- **Resumo:** Atualizar movimentação financeira
- **Descrição:** **Pode disparar emissão automática de NFS-e** dependendo da configuração do emitente (fire-and-forget — falha só é logada, não afeta a resposta). **A resposta é bem mais rica que o schema `MovimentacaoFinanceira` documentado nas rotas de leitura** — o repository busca com `include: {RegistroFinanceiro: true, duplicatas: true}` e devolve tudo.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `responsavelId` | integer | **sim** | ID de um colaborador já cadastrado, responsável por esta movimentação. |
| `tipoMovimentacaoFinanceira` | string | **sim** | valores: `PACIENTE`, `COLABORADOR`, `FORNECEDOR`, `CONVENIO`, `EMPRESA` |
| `tipoFinanceiro` | string | **sim** | valores: `PAGAMENTO`, `RECEBIMENTO` |
| `categoriaDePagamentoId` | integer | **sim** |  |
| `contasCaixaId` | integer | **sim** |  |
| `data` | string (date) | **sim** |  |
| `fornecedorId` | integer | não | aceita null |
| `pacienteId` | integer | não | aceita null |
| `colaboradorId` | integer | não | aceita null |
| `convenioId` | integer | não | aceita null |
| `centroDeCustoId` | integer | não | aceita null |
| `observacoes` | string | não | aceita null |
| `notaFiscal` | string | não | aceita null |
| `parcelas` | integer | **sim** |  |
| `descontoGeral` | number | não | aceita null |
| `registroFinanceiro` | lista de objeto | **sim** |  |
| `registroFinanceiro[].quantidade` | integer | **sim** |  |
| `registroFinanceiro[].valorUnitario` | number | **sim** |  |
| `registroFinanceiro[].contendo` | integer | **sim** |  |
| `registroFinanceiro[].centroDeCustoId` | integer | **sim** |  |
| `registroFinanceiro[].tipoConta` | string | **sim** |  |
| `registroFinanceiro[].tipoConjunto` | string | **sim** |  |
| `registroFinanceiro[].descricao` | string | não | aceita null |
| `registroFinanceiro[].produtoId` | integer | não | aceita null |
| `registroFinanceiro[].fornecedorId` | integer | não | aceita null |
| `registroFinanceiro[].contasCaixasId` | integer | não | aceita null |
| `duplicatas` | lista de objeto | não |  |
| `duplicatas[].vencimento` | string (date) | não |  |
| `duplicatas[].observacao` | string | não | aceita null |
| `duplicatas[].valor` | number | não |  |
| `duplicatas[].aVista` | boolean | não |  |
| `duplicatas[].valorPago` | number | não | aceita null |
| `duplicatas[].pago` | boolean | não | padrão `False` |
| `duplicatas[].dataPagamento` | string (date) | não | aceita null |
| `duplicatas[].tipoDePagamentoId` | integer | não | aceita null |
| `duplicatas[].contaCaixaId` | integer | não | aceita null |

**Respostas:**
- `200` Todos os campos escalares de MovimentacaoFinanceira + RegistroFinanceiro[] + duplicatas[]. Todo valor monetário (valorUnitario, valor, valorPago, multa, juros, outrosAcrescimos, desconto, descontoGeral, valorPagoGlosa) é inteiro em **centavos**. — campos: `id`, `tipoMovimentacaoFinanceira`, `tipoFinanceiro`, `contasCaixaId`, `data`, `observacoes`, `createdAt`, `fornecedorId`, `pacienteId`, `colaboradorId`, `unidadeId`, `unidadeExecutaId`, `convenioId`, `categoriaDePagamentoId`, `centroDeCustoId`, `pendencias`, `notaFiscal`, `tissNumeroLote`, `updatedAt`, `parcelas` …
- `404` Movimentação não encontrada
