# Rotas — Parâmetros (45 operações) — parte 1 de 2

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 ferramentas/rabi_api/atualizar_spec.py` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

Outras partes: [parte 2](parametros-parte-2.md).

## Operações

- `GET /parametros/desconto`
- `PUT /parametros/desconto`
- `GET /parametros/desconto/colaboradores/{nivel}`
- `GET /parametros/desconto/colaborador/{id}`
- `POST /parametros/desconto/colaborador/{id}`
- `GET /parametros/alcada-compra/colaborador/{id}`
- `POST /parametros/alcada-compra/colaborador/{id}`
- `GET /parametros/financeiro`
- `PUT /parametros/financeiro`
- `GET /parametros/orcamento`
- `PUT /parametros/orcamento`
- `GET /parametros/estoque`
- `PUT /parametros/estoque`
- `GET /parametros/avisos`
- `GET /parametros/avisos/{chave}`
- `PUT /parametros/avisos/{chave}`
- `GET /parametros/acolhimento`
- `PUT /parametros/acolhimento`
- `GET /parametros/acolhimento/validar/{pacienteId}`
- `POST /parametros/acolhimento/atualizar-validacoes/{pacienteId}`
- `GET /parametros/acolhimento/historico-confirmacoes/{pacienteId}`
- `GET /parametros/servicos-online`
- `GET /parametros/servicos-online/link`
- `PATCH /parametros/servicos-online/habilitar`
- `PATCH /parametros/servicos-online/agendamento/habilitar`
- `PATCH /parametros/servicos-online/agendamento/mudanca-colaborador/habilitar`
- `PATCH /parametros/servicos-online/confirmacao/habilitar`
- `PATCH /parametros/servicos-online/prontuario/habilitar`
- `PATCH /parametros/servicos-online/lista-medico-convenio/habilitar`
- `PATCH /parametros/servicos-online/textos-informativos`
- `GET /parametros/servicos-online/agendamento/perguntas`
- `POST /parametros/servicos-online/agendamento/perguntas`
- `GET /parametros/servicos-online/agendamento/perguntas/por-especialidade`
- `PUT /parametros/servicos-online/agendamento/perguntas/{id}`
- `DELETE /parametros/servicos-online/agendamento/perguntas/{id}`
- `GET /parametros/servicos-online/agendamento/perguntas/colaborador/{colaboradorId}`
- `POST /parametros/servicos-online/agendamento/perguntas/{perguntaId}/colaborador/{colaboradorId}`
- `GET /parametros/termo`
- `PUT /parametros/termo`
- `GET /parametros/dashboard-permissoes/graficos`
- `PUT /parametros/dashboard-permissoes/graficos`
- `GET /parametros/dashboard-permissoes/dashboards`
- `PUT /parametros/dashboard-permissoes/dashboards`
- `GET /parametros/dashboard-atribuicao`
- `PUT /parametros/dashboard-atribuicao`

### `GET /parametros/desconto`

- **Permissão:** `parametro:read` · **Manual:** [op-get-parametros-desconto](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-get-parametros-desconto)
- **Resumo:** Consultar parâmetros de desconto
- **Descrição:** 404 se nunca configurado.

**Respostas:**
- `200` Parâmetros de desconto — campos: `id`, `descontoNivel1`, `descontoNivel2`, `descontoNivel3`, `limiteParcelasDesconto`, `ativo`
- `404` Parâmetros de desconto não configurados

### `PUT /parametros/desconto`

- **Permissão:** `parametro:update` · **Manual:** [op-put-parametros-desconto](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-put-parametros-desconto)
- **Resumo:** Atualizar parâmetros de desconto
- **Descrição:** Busca a linha a atualizar com `findFirst()` sem filtro (pega a primeira que existir, sem checar ativo/deleted). Campo omitido não altera o valor já salvo.

**Corpo** (`application/json`):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `descontoNivel1` | number | não | mín. 0; máx. 100 |
| `descontoNivel2` | number | não | mín. 0; máx. 100 |
| `descontoNivel3` | number | não | mín. 0; máx. 100 |
| `limiteParcelasDesconto` | integer | não | mín. 0 |

**Respostas:**
- `200` Row completa (inclui `deleted`, que não aparece no GET desta mesma rota). — campos: `id`, `descontoNivel1`, `descontoNivel2`, `descontoNivel3`, `limiteParcelasDesconto`, `ativo`, `createdAt`, `updatedAt`, `deleted`

### `GET /parametros/desconto/colaboradores/{nivel}`

- **Permissão:** `parametro:read` · **Manual:** [op-get-parametros-desconto-colaboradores-nivel](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-get-parametros-desconto-colaboradores-nivel)
- **Resumo:** Colaboradores com permissão de um nível de desconto
- **Descrição:** `nivel`: 1, 2 ou 3 — qualquer outro valor (inclusive não numérico) é tratado como nível 0.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `nivel` | path | string | **sim** |  |

**Respostas:**
- `200` Lista de colaboradores com esse nível (só quem já tem login no sistema) — lista crua: `nivelAlcada`, `colaborador`

### `GET /parametros/desconto/colaborador/{id}`

- **Permissão:** `parametro:read` · **Manual:** [op-get-parametros-desconto-colaborador-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-get-parametros-desconto-colaborador-id)
- **Resumo:** Nível de alçada de desconto de um colaborador
- **Descrição:** Sem `DescontoColaborador` cadastrado, devolve 200 com `nivelAlcada: "NIVEL0"` e `percentual: 0` — não é 404.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do colaborador |

**Respostas:**
- `200` Nível de alçada — campos: `nivelAlcada`, `percentual`, `colaborador`
- `404` Colaborador não encontrado

### `POST /parametros/desconto/colaborador/{id}`

- **Permissão:** `parametro:create` · **Manual:** [op-post-parametros-desconto-colaborador-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-post-parametros-desconto-colaborador-id)
- **Resumo:** Conceder nível de desconto a um colaborador
- **Descrição:** **Hoje sempre falha por chave de API: o controller chama o use case com `isAdmin` fixo em `false`, e o use case exige `isAdmin=true` — toda chamada autenticada recebe 401, mesmo com o scope certo.** `nivel` vai por **query string**, não pelo corpo, apesar de ser POST. Reportado ao time; documentado aqui pra não gerar confusão a mais em cima de um 401 que também é usado (em outras rotas) pra chave inválida.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do colaborador |
| `nivel` | query | integer | **sim** |  |

**Respostas:**
- `200` Nunca observado hoje via chave de API — ver descrição. Se um dia for liberado, o corpo é vazio (0 bytes, sem JSON).

### `GET /parametros/alcada-compra/colaborador/{id}`

- **Permissão:** `parametro:read` · **Manual:** [op-get-parametros-alcada-compra-colaborador-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-get-parametros-alcada-compra-colaborador-id)
- **Resumo:** Alçada de compra de um colaborador

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do colaborador |

**Respostas:**
- `200` Alçada de compra — null se nunca configurada. Não existe NIVEL_1 (esse nível aprova sozinho, sem aprovador atribuível). — campos: `nivelAlcadaCompra`
- `404` Colaborador não encontrado

### `POST /parametros/alcada-compra/colaborador/{id}`

- **Permissão:** `parametro:create` · **Manual:** [op-post-parametros-alcada-compra-colaborador-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-post-parametros-alcada-compra-colaborador-id)
- **Resumo:** Conceder alçada de compra a um colaborador
- **Descrição:** **Hoje sempre falha por chave de API — mesmo bug de `isAdmin` fixo em `false` da rota de nível de desconto.** `nivel` vai por **query string**, não pelo corpo.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do colaborador |
| `nivel` | query | string | não | valores: `NIVEL_2`, `NIVEL_3`, `NIVEL_4`, ``; Vazio remove a alçada |

**Respostas:**
- `200` Nunca observado hoje via chave de API — ver descrição. Se um dia for liberado, o corpo é o DTO abaixo. — campos: `nivelAlcadaCompra`
- `400` nivel inválido
- `404` Colaborador não encontrado

### `GET /parametros/financeiro`

- **Permissão:** `parametro:read` · **Manual:** [op-get-parametros-financeiro](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-get-parametros-financeiro)
- **Resumo:** Consultar parâmetros financeiros
- **Descrição:** Sem configuração salva, devolve um objeto reduzido só com os 3 campos numéricos (sem `id`).

**Respostas:**
- `200` Parâmetros financeiros — campos: `id`, `limiteMaximoRecebimento`, `limiteMaximoPagamento`, `valorMinimoParcela`, `ativo`

### `PUT /parametros/financeiro`

- **Permissão:** `parametro:update` · **Manual:** [op-put-parametros-financeiro](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-put-parametros-financeiro)
- **Resumo:** Atualizar parâmetros financeiros
- **Descrição:** `findFirst()` sem filtro (pega a primeira linha que existir). **Cuidado com `categoriaPagamentoId`/`centroDeCustoId`**: omitir, mandar `0`, `""` ou `false` força esses dois campos para `null`, mesmo em cima de um registro que já tinha esses vínculos — diferente dos 3 campos numéricos, que ficam inalterados se omitidos.

**Corpo** (`application/json`):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `limiteMaximoRecebimento` | number | não | aceita null |
| `limiteMaximoPagamento` | number | não | aceita null |
| `valorMinimoParcela` | number | não | aceita null |
| `categoriaPagamentoId` | integer | não | aceita null; Falsy (0/""/false/omitido) vira null |
| `centroDeCustoId` | integer | não | aceita null; Falsy (0/""/false/omitido) vira null |

**Respostas:**
- `200` Row completa. — campos: `id`, `limiteMaximoRecebimento`, `limiteMaximoPagamento`, `valorMinimoParcela`, `categoriaPagamentoId`, `centroDeCustoId`, `ativo`, `createdAt`, `updatedAt`, `deleted`

### `GET /parametros/orcamento`

- **Permissão:** `parametro:read` · **Manual:** [op-get-parametros-orcamento](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-get-parametros-orcamento)
- **Resumo:** Consultar parâmetros de orçamento
- **Descrição:** **Atenção**: sem configuração salva, esta rota devolve o número `0` cru como corpo da resposta (não um objeto, não 404) — comportamento real, não documentação errada.

**Respostas:**
- `200` Parâmetros de orçamento, ou `0` se nunca configurado — um de: integer \\| campos: `id`, `diasValidos`, `consideracoesGerais`, `parametroVermelho`, `parametroAmarelo`, `requerAutorizacaoNivel2Amarelo`, `requerAutorizacaoNivel3Vermelho`, `requerAutorizacaoNivel3Roxo`, `desabilitarBloqueioFarol`, `ativo`

### `PUT /parametros/orcamento`

- **Permissão:** `parametro:update` · **Manual:** [op-put-parametros-orcamento](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-put-parametros-orcamento)
- **Resumo:** Atualizar parâmetros de orçamento
- **Descrição:** Inclui, entre outros, a chave que liga/desliga o bloqueio de criação pelo farol de rentabilidade (`desabilitarBloqueioFarol`). `findFirst({where:{ativo:true}})` — diferente de desconto/financeiro, que não filtram. **Nomes de campo do corpo divergem dos nomes na resposta**: envie `diasVencimento` (não `diasValidos`) e `consideracoes` (não `consideracoesGerais`) — os demais batem 1:1. Sempre cria a linha se não existir (nunca devolve `0` no PUT, diferente do GET).

**Corpo** (`application/json`):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `diasVencimento` | integer | não | aceita null; Vira `diasValidos` na resposta |
| `consideracoes` | string | não | aceita null; Vira `consideracoesGerais` na resposta |
| `parametroVermelho` | number | não | aceita null |
| `parametroAmarelo` | number | não | aceita null |
| `requerAutorizacaoNivel2Amarelo` | boolean | não |  |
| `requerAutorizacaoNivel3Vermelho` | boolean | não |  |
| `requerAutorizacaoNivel3Roxo` | boolean | não |  |
| `desabilitarBloqueioFarol` | boolean | não |  |

**Respostas:**
- `200` Row completa. — campos: `id`, `diasValidos`, `consideracoesGerais`, `parametroVermelho`, `parametroAmarelo`, `requerAutorizacaoNivel2Amarelo`, `requerAutorizacaoNivel3Vermelho`, `requerAutorizacaoNivel3Roxo`, `desabilitarBloqueioFarol`, `ativo`, `createdAt`, `updatedAt`, `deleted`

### `GET /parametros/estoque`

- **Permissão:** `parametro:read` · **Manual:** [op-get-parametros-estoque](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-get-parametros-estoque)
- **Resumo:** Consultar parâmetros de estoque
- **Descrição:** Sem configuração salva, devolve `{ reservaMedicamentoAtiva: false }` sem `id`.

**Respostas:**
- `200` Parâmetros de estoque — campos: `id`, `reservaMedicamentoAtiva`, `ativo`

### `PUT /parametros/estoque`

- **Permissão:** `parametro:update` · **Manual:** [op-put-parametros-estoque](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-put-parametros-estoque)
- **Resumo:** Atualizar parâmetros de estoque
- **Descrição:** Inclui, entre outros, se a reserva de medicamento por paciente está ativa. **Este modelo não tem campo `deleted`** (diferente de desconto/financeiro/orçamento/termo).

**Corpo** (`application/json`):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `reservaMedicamentoAtiva` | boolean | não |  |

**Respostas:**
- `200` Row completa. — campos: `id`, `reservaMedicamentoAtiva`, `ativo`, `createdAt`, `updatedAt`

### `GET /parametros/avisos`

- **Permissão:** `parametro:read` · **Manual:** [op-get-parametros-avisos](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-get-parametros-avisos)
- **Resumo:** Listar avisos parametrizados
- **Descrição:** Catálogo fixo (hoje 3 chaves: `AUTORIZACAO_VENCENDO`, `GRADE_PENDENTE_GUIA`, `GRADE_AUTORIZACAO_VENCENDO`).

**Respostas:**
- `200` Lista de avisos — campos: `dados`, `page`, `pageSize`, `total`, `totalPages`; item de `dados`: `chave`, `label`, `descricao`, `temLimiar`, `unidadeLimiar`, `habilitado`, `limiar`

### `GET /parametros/avisos/{chave}`

- **Permissão:** `parametro:read` · **Manual:** [op-get-parametros-avisos-chave](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-get-parametros-avisos-chave)
- **Resumo:** Consultar aviso por chave

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `chave` | path | string | **sim** |  |

**Respostas:**
- `200` Aviso — campos: `chave`, `label`, `descricao`, `temLimiar`, `habilitado`, `limiar`
- `404` Aviso não encontrado

### `PUT /parametros/avisos/{chave}`

- **Permissão:** `parametro:update` · **Manual:** [op-put-parametros-avisos-chave](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-put-parametros-avisos-chave)
- **Resumo:** Atualizar aviso
- **Descrição:** `chave` precisa ser uma das 3 do catálogo fixo (`AUTORIZACAO_VENCENDO`, `GRADE_PENDENTE_GUIA`, `GRADE_AUTORIZACAO_VENCENDO`) — outra chave dá 404. Se o aviso não suporta limiar (`temLimiar:false`), `limiar` enviado é descartado silenciosamente (fica `null`). Efeito colateral sem impacto na resposta: invalida cache Redis para `GRADE_PENDENTE_GUIA`/`GRADE_AUTORIZACAO_VENCENDO`.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `chave` | path | string | **sim** | valores: `AUTORIZACAO_VENCENDO`, `GRADE_PENDENTE_GUIA`, `GRADE_AUTORIZACAO_VENCENDO` |

**Corpo** (`application/json`):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `habilitado` | boolean | não |  |
| `limiar` | integer | não | aceita null |

**Respostas:**
- `200` Mesmo shape do GET — nunca inclui id/createdAt/updatedAt (o aviso não é exposto como row de banco, é reconstruído a partir de um catálogo fixo no código + o que está persistido). — campos: `chave`, `label`, `descricao`, `temLimiar`, `unidadeLimiar`, `habilitado`, `limiar`
- `404` Aviso não existe

### `GET /parametros/acolhimento`

- **Permissão:** `parametro:read` · **Manual:** [op-get-parametros-acolhimento](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-get-parametros-acolhimento)
- **Resumo:** Consultar parâmetros de acolhimento
- **Descrição:** Devolve `null` (200) se nunca configurado.

**Respostas:**
- `200` Parâmetros de acolhimento, ou null — campos: `id`, `validadeCPFDias`, `validadeContatoDias`, `validadeEnderecoDias`, `validadeRgDias`, `validadeDocumentosDias`

### `PUT /parametros/acolhimento`

- **Permissão:** `parametro:update` · **Manual:** [op-put-parametros-acolhimento](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-put-parametros-acolhimento)
- **Resumo:** Atualizar parâmetros de acolhimento

**Corpo** (`application/json`):

(sem campos documentados)

**Respostas:**
- `200` Envelope diferente da leitura — campos: `parametros`

### `GET /parametros/acolhimento/validar/{pacienteId}`

- **Permissão:** `parametro:read` · **Manual:** [op-get-parametros-acolhimento-validar-pacienteid](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-get-parametros-acolhimento-validar-pacienteid)
- **Resumo:** Validar dados de acolhimento de um paciente

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `pacienteId` | path | integer | **sim** |  |
| `dataAgendamento` | query | string (date-time) | não | ISO 8601 — sem informar, usa agora |
| `servicoIds` | query | string | não | IDs de serviço separados por vírgula |

**Respostas:**
- `200` Resultado da validação — campos: `cpfValido`, `rgValido`, `enderecoValido`, `contatoValido`, `documentos`, `convenios`
- `404` Paciente não encontrado

### `POST /parametros/acolhimento/atualizar-validacoes/{pacienteId}`

- **Permissão:** `parametro:update` · **Manual:** [op-post-parametros-acolhimento-atualizar-validacoes-pacienteid](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-post-parametros-acolhimento-atualizar-validacoes-pacienteid)
- **Resumo:** Atualizar validações de acolhimento de um paciente
- **Descrição:** **Hoje sempre falha por chave de API: o controller exige `req.colaborador?.id`, que a autenticação por chave de API nunca popula — toda chamada recebe 401.** Reportado ao time. Efeitos (não retornados, hipoteticamente se liberado): grava `cpfValidadoEm`/`rgValidadoEm`/`enderecoValidadoEm`/`contatoValidadoEm` no paciente e `convenioValidadoEm` nos vínculos em `conveniosConfirmados`, cria linhas em histórico de confirmação.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `pacienteId` | path | integer | **sim** |  |

**Corpo** (`application/json`):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `conveniosConfirmados` | lista de integer | não | IDs de vínculo paciente-convênio a marcar como validado |

**Respostas:**
- `200` Nunca observado hoje via chave de API — ver descrição. — campos: `ok`
- `400` pacienteId inválido

### `GET /parametros/acolhimento/historico-confirmacoes/{pacienteId}`

- **Permissão:** `parametro:read` · **Manual:** [op-get-parametros-acolhimento-historico-confirmacoes-pacienteid](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-get-parametros-acolhimento-historico-confirmacoes-pacienteid)
- **Resumo:** Histórico de confirmações de acolhimento

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `pacienteId` | path | integer | **sim** |  |

**Respostas:**
- `200` Histórico, mais recente primeiro — lista crua: `id`, `tipo`, `confirmadoEm`, `colaborador`, `agendamento`, `pacienteConvenioPlano`

### `GET /parametros/servicos-online`

- **Permissão:** `parametro:read` · **Manual:** [op-get-parametros-servicos-online](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-get-parametros-servicos-online)
- **Resumo:** Consultar parâmetros de agendamento online
- **Descrição:** Devolve `null` (200) se nunca configurado.

**Respostas:**
- `200` Parâmetros, ou null — campos: `id`, `habilitarAgendamentoOnline`, `habilitarEtapaAgendamento`, `permitirMudancaColaborador`, `habilitarEtapaConfirmacao`, `habilitarEtapaProntuario`, `habilitarListaMedicoConvenio`, `textoEtapaConvenio`, `textoEtapaEspecialidade`, `textoEtapaServico`, `textoEtapaDocumentos`, `textoEtapaProfissional`, `textoEtapaData`, `textoEtapaConfirmacao`

### `GET /parametros/servicos-online/link`

- **Permissão:** `parametro:read` · **Manual:** [op-get-parametros-servicos-online-link](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-get-parametros-servicos-online-link)
- **Resumo:** Gerar link público de agendamento online

**Respostas:**
- `200` Link gerado — campos: `link`
- `500` Serviço de agendamento online não configurado no ambiente
