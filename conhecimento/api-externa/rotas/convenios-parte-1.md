# Rotas — Convênios (21 operações) — parte 1 de 2

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 ferramentas/rabi_api/atualizar_spec.py` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

Outras partes: [parte 2](convenios-parte-2.md).

## Operações

- `GET /convenios`
- `POST /convenios`
- `POST /convenios/bulk`
- `GET /convenios/{id}/colaboradores`
- `PUT /convenios/{id}/colaboradores`
- `GET /convenios/{id}/taxas`
- `PUT /convenios/{id}/taxas`
- `GET /convenios/{id}/servicos`
- `PUT /convenios/{id}/servicos`
- `GET /convenios/{id}/produtos`
- `PUT /convenios/{id}/produtos`
- `GET /convenios/{id}/especialidades`
- `PUT /convenios/{id}/especialidades`
- `GET /convenios/{id}/planos`
- `PUT /convenios/{id}/planos`
- `GET /convenios/{id}/farol/produtos`
- `GET /convenios/{id}/farol/servicos`
- `GET /convenios/{id}/farol/itens`
- `GET /convenios/{id}`
- `PUT /convenios/{id}`
- `DELETE /convenios/{id}`

### `GET /convenios`

- **Permissão:** `convenio:read` · **Manual:** [op-get-convenios](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-convenios)
- **Resumo:** Listar convênios

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |
| `ativo` | query | boolean | não | Sem informar, lista ativos e inativos. |

**Respostas:**
- `200` Lista paginada — campos: `page`, `pageSize`, `total`, `totalPages`, `dados`; item de `dados`: `id`, `nomeFantasia`, `razaoSocial`, `cnpj`, `descricao`, `codigoANS`, `codigo`, `dataInicio`, `empresaPrincipalId`, `operadoraId`, `ativo`, `createdAt`, `updatedAt`

### `POST /convenios`

- **Permissão:** `convenio:create` · **Manual:** [op-post-convenios](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-convenios)
- **Resumo:** Cadastrar convênio

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `nomeFantasia` | string | não |  |
| `razaoSocial` | string | não |  |
| `cnpj` | string | não | Único por clínica |
| `descricao` | string | **sim** |  |
| `codigo` | integer | não |  |
| `telefone` | string | não |  |
| `email` | string | não |  |
| `pessoaDeContato` | string | não |  |
| `observacao` | string | não |  |
| `dataInicio` | string (date-time) | **sim** |  |
| `dataFim` | string (date-time) | não | aceita null |
| `dataReajuste` | string (date-time) | não | aceita null |
| `dataRenovacao` | string (date-time) | não | aceita null |
| `prazoRecursoGlosa` | integer | não |  |
| `prazoPagamentoRecursoGlosa` | integer | não |  |
| `prazoReajuste` | integer | não |  |
| `prazoAutorizacao` | integer | não |  |
| `prazoPagamento` | integer | não |  |
| `prazoRetorno` | integer | não |  |
| `prazoLimiteEntregaGuias` | integer | não |  |
| `limiteParcelasConvenioParticular` | integer | não |  |
| `fatorK` | number | não |  |
| `faturadoPagamento` | boolean | não |  |
| `exigirToken` | boolean | não |  |
| `operadoraId` | string | não | ID da operadora |
| `empresaId` | string | **sim** | ID da empresa dona do convênio ("Empresa Principal" na tela do sistema). |
| `unidadesIds` | lista de integer | **sim** | IDs das filiais/unidades ("Unidades" na tela do sistema) em que esse convênio é aceito na agenda. Pode incluir o mesmo ID de empresaId. |
| `kitDocumentosPadrao` | objeto | não |  |
| `kitDocumentosPadrao.id` | integer | não |  |
| `xmlConsultaId` | integer | não |  |
| `xmlSpSadtId` | integer | não |  |
| `politicasPorTipoProduto` | lista de objeto | não |  |
| `politicasPorTipoProduto[].tipoProdutoId` | integer | não |  |
| `politicasPorTipoProduto[].fatorK` | string | não | Percentual. Aceita vírgula ou ponto. |
| `politicasPorTipoProduto[].idJson` | string | não | JSON serializado com `fontePrecoId` e `tipoPrecificacao` |
| `registroANS` | string | não | Registro ANS do convênio. **Na criação, é este campo que é gravado como código ANS** — `codigoANS` é ignorado. |

**Respostas:**
- `201` Convênio criado — campos: `id`, `nomeFantasia`, `razaoSocial`, `cnpj`, `descricao`, `codigoANS`, `codigo`, `dataInicio`, `empresaPrincipalId`, `operadoraId`, `ativo`, `createdAt`, `updatedAt`
- `409` CNPJ já existe no sistema
- `422` Referência inválida (empresa, operadora ou kit não encontrado)

### `POST /convenios/bulk`

- **Permissão:** `convenio:create` · **Manual:** [op-post-convenios-bulk](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-convenios-bulk)
- **Resumo:** Cadastrar vários convênios de uma vez
- **Descrição:** Cria até **50 convênios** por requisição. Cada convênio é validado e gravado de forma independente: **um item com erro não impede os demais**, e um convênio nunca fica gravado pela metade (cada um é gravado em uma transação própria). **Validações feitas antes de gravar** - Formato de cada item (campos obrigatórios, tipos, datas, CNPJ com 14 dígitos). - `empresaId`, `unidadesIds` e `operadoraId` existem na clínica. - CNPJ já cadastrado na clínica (com ou sem máscara) ou repetido dentro do próprio lote. Nesse caso, apenas a primeira ocorrência é criada. **Como interpretar a resposta** - `201`: todos os convênios foram criados. - `207`: ao menos um item falhou. Confira `resultados`, item a item, pelo `indice`. Os itens `CRIADO` já foram gravados. - Para tentar de novo, reenvie **apenas** os itens com `ERRO` ou `NAO_PROCESSADO`. Reenviar o lote inteiro é seguro: os já criados serão recusados por CNPJ duplicado. **Limites** - Máximo de 50 convênios por requisição (`400` acima disso). - Só um lote por vez por clínica: um segundo lote enquanto o primeiro roda recebe `429`. - O processamento é interrompido após 45 segundos. Os itens restantes voltam como `NAO_PROCESSADO`.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `convenios` | lista de objeto | **sim** | máx. itens 50 |
| `convenios[].nomeFantasia` | string | não |  |
| `convenios[].razaoSocial` | string | não |  |
| `convenios[].cnpj` | string | **sim** | **Obrigatório no lote.** Aceita com ou sem máscara (14 dígitos). É a chave usada para recusar convênios já cadastrados ou repetidos no lote. |
| `convenios[].descricao` | string | **sim** |  |
| `convenios[].codigo` | integer | não |  |
| `convenios[].telefone` | string | não |  |
| `convenios[].email` | string | não |  |
| `convenios[].pessoaDeContato` | string | não |  |
| `convenios[].observacao` | string | não |  |
| `convenios[].dataInicio` | string (date-time) | **sim** |  |
| `convenios[].dataFim` | string (date-time) | não | aceita null |
| `convenios[].dataReajuste` | string (date-time) | não | aceita null |
| `convenios[].dataRenovacao` | string (date-time) | não | aceita null |
| `convenios[].prazoRecursoGlosa` | integer | não |  |
| `convenios[].prazoPagamentoRecursoGlosa` | integer | não |  |
| `convenios[].prazoReajuste` | integer | não |  |
| `convenios[].prazoAutorizacao` | integer | não |  |
| `convenios[].prazoPagamento` | integer | não |  |
| `convenios[].prazoRetorno` | integer | não |  |
| `convenios[].prazoLimiteEntregaGuias` | integer | não |  |
| `convenios[].limiteParcelasConvenioParticular` | integer | não |  |
| `convenios[].fatorK` | number | não |  |
| `convenios[].faturadoPagamento` | boolean | não |  |
| `convenios[].exigirToken` | boolean | não |  |
| `convenios[].operadoraId` | string | não | ID da operadora |
| `convenios[].empresaId` | string | **sim** | ID da empresa dona do convênio ("Empresa Principal" na tela do sistema). |
| `convenios[].unidadesIds` | lista de integer | **sim** | IDs das filiais/unidades ("Unidades" na tela do sistema) em que esse convênio é aceito na agenda. Pode incluir o mesmo ID de empresaId. |
| `convenios[].kitDocumentosPadrao` | objeto | não |  |
| `convenios[].kitDocumentosPadrao.id` | integer | não |  |
| `convenios[].xmlConsultaId` | integer | não |  |
| `convenios[].xmlSpSadtId` | integer | não |  |
| `convenios[].politicasPorTipoProduto` | lista de objeto | não |  |
| `convenios[].politicasPorTipoProduto[].tipoProdutoId` | integer | não |  |
| `convenios[].politicasPorTipoProduto[].fatorK` | string | não | Percentual. Aceita vírgula ou ponto. |
| `convenios[].politicasPorTipoProduto[].idJson` | string | não | JSON serializado com `fontePrecoId` e `tipoPrecificacao` |
| `convenios[].registroANS` | string | não | Registro ANS do convênio. **Na criação, é este campo que é gravado como código ANS** — `codigoANS` é ignorado. |

**Respostas:**
- `201` Todos os convênios foram criados — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `cnpj`, `status`, `id`, `erro`
- `207` Lote processado com falhas parciais. Veja `resultados`. — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `cnpj`, `status`, `id`, `erro`
- `400` Lote vazio, sem a chave `convenios` ou acima de 50 itens
- `429` Já existe um lote em andamento para esta clínica

### `GET /convenios/{id}/colaboradores`

- **Permissão:** `convenio:read` · **Manual:** [op-get-convenios-id-colaboradores](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-convenios-id-colaboradores)
- **Resumo:** Listar colaboradores do convênio

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |

**Respostas:**
- `200` Lista paginada — campos: `page`, `pageSize`, `total`, `totalPages`, `dados`; item de `dados`: `colaboradorId`, `credenciado`, `atende`, `colaboradorConvertidoId`, `especialidadesIds`, `especialidadesConvertidasIds`, `id`
- `400` `id` inválido
- `404` Convênio não encontrado

### `PUT /convenios/{id}/colaboradores`

- **Permissão:** `convenio:update` · **Manual:** [op-put-convenios-id-colaboradores](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-convenios-id-colaboradores)
- **Resumo:** Definir colaboradores do convênio (em lote)
- **Descrição:** Equivale à aba **Colaboradores** do cadastro de convênio: para cada colaborador define se é credenciado, se atende o convênio, a conversão e as especialidades (próprias e convertidas). Aceita até **100 colaboradores por requisição**, todos do mesmo convênio. **Comportamento (upsert)** - Se o colaborador ainda não tem vínculo com o convênio, ele é **criado**. Se já tem, é **atualizado** — a linha nunca é duplicada. - Campos omitidos **mantêm o valor atual**. Diferente do `PUT /convenios/{id}`, aqui não há sobrescrita por omissão. - As listas de especialidades são **aditivas**: só acrescentam. Esta rota **nunca remove** especialidade nem conversão. Para remover, use a tela. - É idempotente: reenviar a mesma requisição não gera duplicidade. **Regras (as mesmas da tela)** - `atende` só pode ser `true` se o colaborador for credenciado ou tiver conversão. - `especialidadesIds` devem ser especialidades ativas do próprio colaborador. - `especialidadesConvertidasIds` devem ser especialidades do colaborador convertido. - O colaborador não pode ser convertido para ele mesmo, nem ter uma conversão existente trocada por outra. - `colaboradorId` não pode se repetir na mesma requisição. **Como interpretar a resposta** - `200`: todos os colaboradores foram processados. - `207`: ao menos um falhou. Confira `resultados` pelo `indice`. Os itens `CRIADO` e `ATUALIZADO` já foram gravados, e cada c…

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `colaboradores` | lista de objeto | **sim** | máx. itens 100 |
| `colaboradores[].colaboradorId` | integer | **sim** | ID do colaborador |
| `colaboradores[].credenciado` | boolean | não | Coluna **Credenciado** da tela. Omitido: mantém o valor atual (ou `false` se o vínculo for novo). |
| `colaboradores[].atende` | boolean | não | Coluna **Atende** da tela. Só pode ser `true` se o colaborador for credenciado ou tiver conversão. Omitido: mantém o valor atual. |
| `colaboradores[].colaboradorConvertidoId` | integer | não | Coluna **Conversão** da tela: colaborador que atende no lugar deste para o convênio. |
| `colaboradores[].especialidadesIds` | lista de integer | não | máx. itens 50; Coluna **Especialidade** da tela: IDs de especialidades cadastradas **neste colaborador** (`colaborador_especialidade`, ativas). |
| `colaboradores[].especialidadesConvertidasIds` | lista de integer | não | máx. itens 50; Coluna **Especialidade Conversão** da tela: IDs de especialidades do **colaborador convertido**. Exige `colaboradorConvertidoId` (enviado agora ou já existente… |

**Respostas:**
- `200` Todos os colaboradores foram processados — campos: `total`, `criados`, `atualizados`, `falhas`, `resultados`; item de `resultados`: `indice`, `colaboradorId`, `status`, `id`, `erro`
- `207` Processado com falhas parciais. Veja `resultados`. — campos: `total`, `criados`, `atualizados`, `falhas`, `resultados`; item de `resultados`: `indice`, `colaboradorId`, `status`, `id`, `erro`
- `400` `id` inválido, lista vazia, sem a chave `colaboradores` ou acima de 100 itens
- `404` Convênio não encontrado
- `429` Já existe uma atualização em andamento para este convênio

### `GET /convenios/{id}/taxas`

- **Permissão:** `convenio:read` · **Manual:** [op-get-convenios-id-taxas](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-convenios-id-taxas)
- **Resumo:** Listar taxas do convênio

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |

**Respostas:**
- `200` Lista paginada — campos: `page`, `pageSize`, `total`, `totalPages`, `dados`; item de `dados`: `taxaId`, `utiliza`, `zerarValor`, `nomeConvertido`, `descricaoConvertida`, `valorConvertido`, `tipoCodigoId`, `tipoTaxaId`, `tabela87ANSId`, `codigo`, `codigoTabelaConversao`, `descricaoConversaoTabela`, `id`
- `400` `id` inválido
- `404` Convênio não encontrado

### `PUT /convenios/{id}/taxas`

- **Permissão:** `convenio:update` · **Manual:** [op-put-convenios-id-taxas](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-convenios-id-taxas)
- **Resumo:** Definir taxas do convênio (em lote)
- **Descrição:** Equivale à aba **Taxas** do cadastro de convênio. Aceita até **200 taxas por requisição**, todas do mesmo convênio. **Comportamento (upsert)** - A chave é `taxaId`: se o convênio ainda não usa essa taxa, o vínculo é **criado**; se já usa, é **atualizado**. - Campos omitidos **mantêm o valor atual**, exceto `valorConvertido`: omitido mantém, mas `null` explicitamente limpa o valor. - É idempotente: reenviar o mesmo item não duplica. **Como interpretar a resposta** - `200`: todas as taxas foram processadas. - `207`: ao menos uma falhou. Confira `resultados` pelo `indice`. **Limites** - Máximo de 200 taxas por requisição (`400` acima disso). - Só uma atualização por vez por convênio: uma segunda, enquanto a primeira roda, recebe `429`. - Interrompida após 45 segundos; o restante volta como `NAO_PROCESSADO`.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `taxas` | lista de objeto | **sim** | máx. itens 200 |
| `taxas[].taxaId` | integer | **sim** | ID da taxa cadastrada no sistema (coluna **Taxa** da tela) |
| `taxas[].utiliza` | boolean | não | Coluna **Utiliza**. Omitido: mantém o valor atual (ou `false` se o vínculo for novo). |
| `taxas[].zerarValor` | boolean | não | Coluna **Zerar Valor**. Omitido: mantém o valor atual. |
| `taxas[].nomeConvertido` | string | não |  |
| `taxas[].descricaoConvertida` | string | não |  |
| `taxas[].valorConvertido` | number | não | aceita null; Em reais (ex.: 50 = R$ 50,00). `null` limpa o valor convertido. Omitido: mantém o valor atual. |
| `taxas[].tipoCodigoId` | integer | não |  |
| `taxas[].tipoTaxaId` | integer | não |  |
| `taxas[].tabela87ANSId` | integer | não |  |
| `taxas[].codigo` | string | não |  |
| `taxas[].codigoTabelaConversao` | string | não |  |
| `taxas[].descricaoConversaoTabela` | string | não |  |

**Respostas:**
- `200` Todas as taxas foram processadas — campos: `total`, `criados`, `atualizados`, `falhas`, `resultados`; item de `resultados`: `indice`, `taxaId`, `status`, `id`, `erro`
- `207` Processado com falhas parciais. Veja `resultados`. — campos: `total`, `criados`, `atualizados`, `falhas`, `resultados`; item de `resultados`: `indice`, `taxaId`, `status`, `id`, `erro`
- `400` `id` inválido, lista vazia, sem a chave `taxas` ou acima de 200 itens
- `404` Convênio não encontrado
- `429` Já existe uma atualização em andamento para este convênio

### `GET /convenios/{id}/servicos`

- **Permissão:** `convenio:read` · **Manual:** [op-get-convenios-id-servicos](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-convenios-id-servicos)
- **Resumo:** Listar serviços do convênio

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |

**Respostas:**
- `200` Lista paginada — campos: `page`, `pageSize`, `total`, `totalPages`, `dados`; item de `dados`: `servicoId`, `utiliza`, `zerarValor`, `pacote`, `autorizacaoPrevia`, `retornoServico`, `ativo`, `nomeConversao`, `descricaoConvenio`, `valorInternoConvenio`, `parcelasMaximas`, `tipoCodigoId`, `tipoAtendimentoId`, `tabela87ANSId`, `kitDocumentoId`, `codigo`, `codigoTuss`, `codigoConvenio`, `id`
- `400` `id` inválido
- `404` Convênio não encontrado
