# Rotas — Financeiro (13 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-11-22.json`) · **Conferido em:** 2026-11-22
> **Vale para:** produção (Swagger publicado em 2026-11-22) · **Kit:** v0.3.3

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 ferramentas/rabi_api/atualizar_spec.py` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `POST /financeiro/pagamentos/confirmacao`
- `GET /financeiro/movimentacoes`
- `POST /financeiro/movimentacoes`
- `POST /financeiro/movimentacoes/bulk`
- `POST /financeiro/xml-tiss`
- `POST /financeiro/xml-tiss/casar-historico`
- `GET /financeiro/contas-caixa`
- `POST /financeiro/contas-caixa`
- `GET /financeiro/contas-caixa/tipos`
- `GET /financeiro/contas-caixa/{id}`
- `PUT /financeiro/contas-caixa/{id}`
- `GET /financeiro/movimentacoes/{id}`
- `PUT /financeiro/movimentacoes/{id}`

### `POST /financeiro/pagamentos/confirmacao`

- **Permissão:** `financeiro:update` · **Manual:** [op-post-financeiro-pagamentos-confirmacao](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-financeiro-pagamentos-confirmacao)
- **Resumo:** Confirma pagamento (Pix ou link) e dá baixa automática na parcela
- **Descrição:** Para o provedor de pagamento (#409) avisar que a cobrança foi paga. Identifique a parcela por `duplicataId` ou por `identificadorCobranca` (o txid/id da cobrança gravado no campo `transacao` da parcela). A parcela fica paga com `identificadorPagamento` (endToEndId do Pix ou id da transação do link), o que já a comprova. Idempotente: repetir a mesma confirmação devolve `jaConfirmado: true` (200) sem pagar de novo. Valor menor que o da parcela → 409.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `duplicataId` | integer | não |  |
| `identificadorCobranca` | string | não |  |
| `valor` | number | **sim** | Em reais |
| `dataPagamento` | string (date-time) | não |  |
| `identificadorPagamento` | string | **sim** |  |
| `meio` | string | **sim** | valores: `PIX`, `LINK` |

**Respostas:**
- `200` Pagamento já confirmado antes (idempotente)
- `201` Parcela paga
- `404` Parcela da cobrança não encontrada
- `409` Parcela paga por outro pagamento ou valor menor que o da parcela

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

### `POST /financeiro/xml-tiss`

- **Permissão:** `financeiro:create` · **Manual:** [op-post-financeiro-xml-tiss](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-financeiro-xml-tiss)
- **Resumo:** Importar XML TISS de faturamento de convênio
- **Descrição:** O XML vai no JSON: `xmlBase64` (bytes do arquivo, preferível) ou `xml` (texto). - Com `movimentacaoId`, ou quando já existe título ativo do `convenioId` com o lote do XML: **registra o XML nesse título** (modo `REGISTRADO_EM_TITULO_EXISTENTE`). As guias entram na Conciliação XML Externo, casam com o atendimento pelos mesmos critérios da importação da tela, o 1º item de cada guia no título recebe o `servicoAtendimentoId` e a guia do atendimento sai do Fechar lotes. Não cria outro contas a receber. Os itens são achados pelo `numeroGuiaOrigemXml`. - Sem título do lote: importação completa igual à tela (modo `IMPORTADO`, cria o título; exige `contaCaixaId`). **Como a guia do XML acha o atendimento (nos dois modos, nesta ordem):** 1) item do título já ligado pelo integrador (`servicoAtendimentoId`); 2) nº da guia (prestador/operadora), senha e valor; 3) **paciente + dia**: a carteirinha (`numeroCarteira` do XML) ou o CPF do beneficiário acha o paciente no convênio (também em convênio cadastrado com o mesmo nome) e casa com a guia dele no mesmo dia do atendimento (fuso de Brasília): guia migrada (999999) ou guia de número diferente ainda aberta no pré-faturamento com o mesmo TUSS; só quando é 1 guia do XML para 1 guia do Rabi; 4) atendimento sem guia do mesmo paciente/dia. O nome do paciente não é usado (o XML não traz). Para casar pelo paciente, a carteirinha do XML precisa estar c…

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `responsavelId` | integer | **sim** |  |
| `xmlBase64` | string | não | Arquivo XML em base64 (use este ou `xml`) |
| `xml` | string | não | Conteúdo do XML em texto (use este ou `xmlBase64`) |
| `nomeArquivo` | string | não |  |
| `movimentacaoId` | integer | não | Título já criado pela API onde registrar o XML |
| `convenioId` | integer | não |  |
| `contaCaixaId` | integer | não | Só na importação completa (sem título) |
| `protocoloEnvio` | string | não | aceita null |
| `dataEnvio` | string | não | aceita null; AAAA-MM-DD ou DD/MM/AAAA |
| `statusEnvio` | string | não | valores: `ENVIADO`, `SEM_ENVIO`, `A_CONFERIR` |

**Respostas:**
- `201` XML registrado no título ou importado
- `400` Corpo inválido ou falta contaCaixaId na importação completa
- `422` XML inválido, arquivo/lote já importado ou título incompatível

### `POST /financeiro/xml-tiss/casar-historico`

- **Permissão:** `financeiro:update` · **Manual:** [op-post-financeiro-xml-tiss-casar-historico](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-financeiro-xml-tiss-casar-historico)
- **Resumo:** Vincular guias pendentes de XML já importado pelo paciente (carteirinha/CPF) + dia
- **Descrição:** Mesmo efeito do botão "Casar histórico" da Conciliação XML Externo: as guias de XML **já importadas** que ficaram PENDENTES procuram a guia do atendimento do mesmo paciente no mesmo dia. **Não reenvie o XML para revincular** — o mesmo arquivo ou o mesmo nº de lote é recusado, e um lote com outro número cria outro contas a receber (cobrança em dobro). Paciente: pela carteirinha do XML (em qualquer convênio onde ela esteja cadastrada no paciente) ou, sem carteirinha cadastrada, pelo CPF do beneficiário. O nome não é usado. Dia no fuso de Brasília. Convênio aceito: o da importação, outro cadastro com o mesmo nome, ou onde a carteirinha está cadastrada. Guia do Rabi aceita: migrada (nº 999999), sem faturamento, sem financeiro e sem outra guia de XML; com `incluirNumeroDiferente`, também guia de número próprio ainda aberta no pré-faturamento e com o mesmo TUSS. Só casa 1 guia do XML ↔ 1 guia do Rabi; 2+ candidatas no dia desempatam pelo TUSS, senão ficam pendentes (`ambiguas`/`disputadas`) para o Vincular manual na tela. Uso: chame primeiro com `simular: true` (padrão, não grava) e confira `casaveis`; depois `simular: false` com `responsavelId`. Cada chamada grava até 1.500 guias — se `restantes` > 0, chame de novo. Guia com carteirinha fora do cadastro do paciente não casa: cadastre a carteirinha (PUT /pacientes/{id}/convenios/{vinculoId}) e chame de novo.

**Corpo** (`application/json`):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `responsavelId` | integer | não | Obrigatório quando `simular` é false |
| `convenioId` | integer | não | Só guias de importações deste convênio (omitido = todos) |
| `importacaoId` | integer | não | Só guias desta importação (o `importacaoId` devolvido por POST /financeiro/xml-tiss) |
| `simular` | boolean | não | padrão `True`; true = só conta, não grava |
| `incluirNumeroDiferente` | boolean | não | padrão `False` |
| `incluirConvenioTeste` | boolean | não | padrão `False`; Aceita guia do Rabi no convênio "teste" da migração ou sem convênio |

**Respostas:**
- `200` Resumo do casamento
- `400` Corpo inválido ou responsavelId ausente/inválido ao gravar

### `GET /financeiro/contas-caixa`

- **Permissão:** `financeiro:read` · **Manual:** [op-get-financeiro-contas-caixa](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-financeiro-contas-caixa)
- **Resumo:** Listar contas e caixas (o contaCaixaId da importação de XML e das movimentações)
- **Descrição:** `numero` acha a conta pelo número com ou sem pontuação ("110944-8" = "1109448"), inclusive em cadastros antigos que têm o número só no nome. `busca` procura no nome/descrição. `ativo=true\|false` filtra.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `numero` | query | string | não |  |
| `busca` | query | string | não |  |
| `ativo` | query | string | não | valores: `true`, `false` |

**Respostas:**
- `200` Contas — lista crua: `id`, `conta`, `descricao`, `agencia`, `numeroConta`, `tipoDeContaId`, `tipoDeConta`, `contaDaEmpresa`, `ativo`

### `POST /financeiro/contas-caixa`

- **Permissão:** `financeiro:create` · **Manual:** [op-post-financeiro-contas-caixa](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-financeiro-contas-caixa)
- **Resumo:** Cadastrar conta
- **Descrição:** Sem `tipoDeContaId` usa o tipo "Conta Corrente" (ver `GET /financeiro/contas-caixa/tipos`). Se já existir conta com o mesmo número, responde 409 com o id dela (complete os dados com o PUT).

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `conta` | string | **sim** |  |
| `descricao` | string | não |  |
| `agencia` | string | não |  |
| `numeroConta` | string | não |  |
| `tipoDeContaId` | integer | não |  |
| `contaDaEmpresa` | boolean | não | padrão `True` |

**Respostas:**
- `201` Conta criada — campos: `id`, `conta`, `descricao`, `agencia`, `numeroConta`, `tipoDeContaId`, `tipoDeConta`, `contaDaEmpresa`, `ativo`
- `400` Corpo inválido ou tipoDeContaId inexistente
- `409` Já existe conta com esse número

### `GET /financeiro/contas-caixa/tipos`

- **Permissão:** `financeiro:read` · **Manual:** [op-get-financeiro-contas-caixa-tipos](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-financeiro-contas-caixa-tipos)
- **Resumo:** Tipos de conta (valores de tipoDeContaId)

**Respostas:**
- `200` Tipos [{ id, nome }]

### `GET /financeiro/contas-caixa/{id}`

- **Permissão:** `financeiro:read` · **Manual:** [op-get-financeiro-contas-caixa-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-financeiro-contas-caixa-id)
- **Resumo:** Buscar conta

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** |  |

**Respostas:**
- `200` Conta
- `404` Conta não encontrada

### `PUT /financeiro/contas-caixa/{id}`

- **Permissão:** `financeiro:update` · **Manual:** [op-put-financeiro-contas-caixa-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-put-financeiro-contas-caixa-id)
- **Resumo:** Alterar conta (grava só os campos enviados)
- **Descrição:** Uso típico: completar `agencia` e `numeroConta` das contas antigas. `ativo: false` desativa (não há DELETE).

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** |  |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `conta` | string | não |  |
| `descricao` | string | não | aceita null |
| `agencia` | string | não | aceita null |
| `numeroConta` | string | não | aceita null |
| `tipoDeContaId` | integer | não |  |
| `contaDaEmpresa` | boolean | não |  |
| `ativo` | boolean | não |  |

**Respostas:**
- `200` Conta alterada
- `400` Corpo vazio/inválido
- `404` Conta não encontrada
- `409` Número já usado em outra conta

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
- **Descrição:** **Pode disparar emissão automática de NFS-e** dependendo da configuração do emitente (fire-and-forget — falha só é logada, não afeta a resposta). **A resposta é bem mais rica que o schema `MovimentacaoFinanceira` documentado nas rotas de leitura** — o repository busca com `include: {RegistroFinanceiro: true, duplicatas: true}` e devolve tudo. **Atualização parcial**: campo omitido mantém o valor atual; `null` limpa; lista omitida mantém; lista enviada substitui (`[]` apaga). Nenhum campo é obrigatório. - `registroFinanceiro` e `duplicatas` omitidos: lançamentos e parcelas não mudam. - Lista enviada: item com `id` é atualizado no lugar e só nos campos enviados — o lançamento mantém vínculos (atendimento, guia do XML, glosa, orçamento, estoque) e a parcela mantém conciliação e anexo. Item sem `id` é criado (precisa vir completo). Item que não veio é removido. `id` de outra movimentação responde 400. - Valores em **reais**. A leitura (`GET`) devolve em **centavos** — divida por 100 antes de reenviar.

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
