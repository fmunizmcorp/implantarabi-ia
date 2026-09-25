# Rotas — Orçamentos (10 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 ferramentas/rabi_api/atualizar_spec.py` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `GET /orcamentos`
- `POST /orcamentos`
- `GET /orcamentos/status`
- `GET /orcamentos/consideracoes`
- `PUT /orcamentos/{id}`
- `PUT /orcamentos/status/{idOrcamento}/{idStatus}`
- `GET /orcamentos/{id}/{isAgendamento}`
- `GET /orcamentos/anexo/listar/{orcamentoId}`
- `GET /orcamentos/anexo/listar-necessarios/{pacienteId}`
- `POST /orcamentos/anexo/vincular/{anexoId}/{orcamentoId}`

### `GET /orcamentos`

- **Permissão:** `orcamento:read` · **Manual:** [op-get-orcamentos](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-orcamentos)
- **Resumo:** Listar orçamentos
- **Descrição:** **O shape do item muda por completo conforme `pacienteId` é informado ou não na query — são dois formatos de resposta atrás do mesmo endpoint, não só um filtro a mais.**

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `pacienteId` | query | integer | não | Quando informado, ignora page/pageSize/demais filtros e muda o shape do item (ver descrição). |
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `10` |
| `id` | query | integer | não |  |
| `statusId` | query | integer | não | `statusId=8` (Vencido) é ignorado no filtro — não dá pra filtrar server-side por vencidos. |
| `pacienteNome` | query | string | não |  |
| `pacienteCpf` | query | string | não |  |
| `createdAtDe` | query | string (date) | não |  |
| `createdAtAte` | query | string (date) | não |  |

**Respostas:**
- `200` SEM `pacienteId`: paginação real, mas com uma ressalva — depois de paginar, o código ainda filtra a página em memória (remove sessões usadas > autorizadas), então `dados.length` pode vir menor que `pageSize` mesmo havendo mais resultados, e `total` pode não bater exatamente com a soma real de itens… — campos: `dados`, `page`, `pageSize`, `total`, `totalPages`

### `POST /orcamentos`

- **Permissão:** `orcamento:create` · **Manual:** [op-post-orcamentos](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-orcamentos)
- **Resumo:** Criar orçamento
- **Descrição:** Pagamento no ato (`movimentacaoFinanceira`) é permitido e pode disparar emissão automática de NFS-e. Bloqueado (422) se o farol de rentabilidade exigir aprovação e não houver token/pendência informada.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `responsavelId` | integer | **sim** | ID de um colaborador já cadastrado. |
| `paciente` | objeto | **sim** |  |
| `paciente.id` | string | **sim** |  |
| `local` | objeto | não |  |
| `local.id` | integer | não |  |
| `idGrade` | integer | **sim** |  |
| `gradeBaseId` | integer | **sim** |  |
| `responsavelBaseId` | integer | **sim** |  |
| `tipoAtendimentoConsulta` | integer | **sim** |  |
| `tipoRepeticao` | integer | **sim** |  |
| `tipoAtendimento` | string | não | valores: `COLABORADOR`, `EQUIPAMENTO` |
| `data` | string (date) | **sim** |  |
| `hora` | string | **sim** |  |
| `horaFim` | string | não | aceita null |
| `statusId` | integer | **sim** |  |
| `encaixe` | boolean | não | padrão `False` |
| `documentosSelecionados` | lista de objeto | não |  |
| `procedimentos` | lista de objeto | **sim** |  |
| `procedimentos[].procedimentoId` | integer | **sim** | ID do serviço |
| `procedimentos[].convenioId` | integer | **sim** |  |
| `procedimentos[].planoId` | integer | não | aceita null |
| `procedimentos[].colaboradorId` | integer | não | aceita null |
| `procedimentos[].horarioInicio` | string | não | aceita null |
| `procedimentos[].horarioFim` | string | não | aceita null |
| `contatos` | lista de objeto | **sim** |  |
| `contatos[].email` | string | não |  |
| `contatos[].celular` | string | não |  |
| `endereco` | objeto | não | aceita null |
| `repetir` | boolean | não | padrão `False` |
| `movimentacaoFinanceira` | objeto | não | aceita null; Sinal/entrada pago no ato. **Presente, dispara emissão automática de NFS-e** — permitido de propósito nesta API. |
| `movimentacaoFinanceira.registroFinanceiro` | lista de objeto | não |  |
| `movimentacaoFinanceira.registroFinanceiro[].quantidade` | integer | não |  |
| `movimentacaoFinanceira.registroFinanceiro[].valorUnitario` | number | não |  |
| `movimentacaoFinanceira.registroFinanceiro[].contendo` | integer | não |  |
| `movimentacaoFinanceira.registroFinanceiro[].centroDeCustoId` | integer | não |  |
| `movimentacaoFinanceira.registroFinanceiro[].tipoConta` | string | não |  |
| `movimentacaoFinanceira.registroFinanceiro[].tipoConjunto` | string | não |  |
| `movimentacaoFinanceira.registroFinanceiro[].descricao` | string | não | aceita null |
| `movimentacaoFinanceira.registroFinanceiro[].produtoId` | integer | não | aceita null |
| `movimentacaoFinanceira.registroFinanceiro[].fornecedorId` | integer | não | aceita null |
| `movimentacaoFinanceira.registroFinanceiro[].contasCaixasId` | integer | não | aceita null |
| `movimentacaoFinanceira.duplicatas` | lista de objeto | não |  |
| `movimentacaoFinanceira.duplicatas[].vencimento` | string (date) | não |  |
| `movimentacaoFinanceira.duplicatas[].observacao` | string | não | aceita null |
| `movimentacaoFinanceira.duplicatas[].valor` | number | não |  |
| `movimentacaoFinanceira.duplicatas[].aVista` | boolean | não |  |
| `movimentacaoFinanceira.duplicatas[].valorPago` | number | não | aceita null |
| `movimentacaoFinanceira.duplicatas[].pago` | boolean | não | padrão `False` |
| `movimentacaoFinanceira.duplicatas[].dataPagamento` | string (date) | não | aceita null |
| `movimentacaoFinanceira.duplicatas[].tipoDePagamentoId` | integer | não | aceita null |
| `movimentacaoFinanceira.duplicatas[].contaCaixaId` | integer | não | aceita null |
| `movimentacaoFinanceira.categoriaDePagamentoId` | integer | não |  |
| `movimentacaoFinanceira.centroDeCustoId` | integer | não |  |
| `aprovacaoFarolToken` | string | não | aceita null; Necessário se o farol de rentabilidade estiver amarelo/vermelho e os parâmetros exigirem aprovação. |
| `aprovacaoFarolPendenteId` | integer | não | aceita null |

**Respostas:**
- `201` Orçamento criado — campos: `message`, `data`
- `400` responsavelId ausente/inválido
- `422` Bloqueado pelo farol de rentabilidade — falta aprovação

### `GET /orcamentos/status`

- **Permissão:** `orcamento:read` · **Manual:** [op-get-orcamentos-status](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-orcamentos-status)
- **Resumo:** Listar status possíveis de orçamento
- **Descrição:** `findMany()` sem filtro nem ordenação — vem tudo, inclusive status com `ativo:false`, em ordem não garantida. **Não inclui o status "Vencido" (id 8)**, que é calculado em runtime em `GET /orcamentos` e não existe como registro aqui.

**Respostas:**
- `200` Array direto (sem envelope). — lista crua: `id`, `descricao`, `ativo`, `createdAt`, `updatedAt`

### `GET /orcamentos/consideracoes`

- **Permissão:** `orcamento:read` · **Manual:** [op-get-orcamentos-consideracoes](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-orcamentos-consideracoes)
- **Resumo:** Listar considerações padrão de orçamento
- **Descrição:** **Não é lista — é uma STRING crua** (o texto configurado em ParametrosOrcamento.consideracoesGerais). Se nunca configurado, devolve string vazia `""` (não `null`, não 404).

**Respostas:**
- `200` String crua com o texto configurado (ou vazia). — string

### `PUT /orcamentos/{id}`

- **Permissão:** `orcamento:update` · **Manual:** [op-put-orcamentos-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-put-orcamentos-id)
- **Resumo:** Atualizar orçamento
- **Descrição:** Orçamento já aprovado não pode ter procedimentos/valores editados (precisa criar um novo) — exceção: registrar pagamento continua funcionando.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do orçamento |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `responsavelId` | integer | **sim** | ID de um colaborador já cadastrado. |
| `paciente` | objeto | **sim** |  |
| `paciente.id` | string | **sim** |  |
| `local` | objeto | não |  |
| `local.id` | integer | não |  |
| `idGrade` | integer | **sim** |  |
| `gradeBaseId` | integer | **sim** |  |
| `responsavelBaseId` | integer | **sim** |  |
| `tipoAtendimentoConsulta` | integer | **sim** |  |
| `tipoRepeticao` | integer | **sim** |  |
| `tipoAtendimento` | string | não | valores: `COLABORADOR`, `EQUIPAMENTO` |
| `data` | string (date) | **sim** |  |
| `hora` | string | **sim** |  |
| `horaFim` | string | não | aceita null |
| `statusId` | integer | **sim** |  |
| `encaixe` | boolean | não | padrão `False` |
| `documentosSelecionados` | lista de objeto | não |  |
| `procedimentos` | lista de objeto | **sim** |  |
| `procedimentos[].procedimentoId` | integer | **sim** | ID do serviço |
| `procedimentos[].convenioId` | integer | **sim** |  |
| `procedimentos[].planoId` | integer | não | aceita null |
| `procedimentos[].colaboradorId` | integer | não | aceita null |
| `procedimentos[].horarioInicio` | string | não | aceita null |
| `procedimentos[].horarioFim` | string | não | aceita null |
| `contatos` | lista de objeto | **sim** |  |
| `contatos[].email` | string | não |  |
| `contatos[].celular` | string | não |  |
| `endereco` | objeto | não | aceita null |
| `repetir` | boolean | não | padrão `False` |
| `movimentacaoFinanceira` | objeto | não | aceita null; Sinal/entrada pago no ato. **Presente, dispara emissão automática de NFS-e** — permitido de propósito nesta API. |
| `movimentacaoFinanceira.registroFinanceiro` | lista de objeto | não |  |
| `movimentacaoFinanceira.registroFinanceiro[].quantidade` | integer | não |  |
| `movimentacaoFinanceira.registroFinanceiro[].valorUnitario` | number | não |  |
| `movimentacaoFinanceira.registroFinanceiro[].contendo` | integer | não |  |
| `movimentacaoFinanceira.registroFinanceiro[].centroDeCustoId` | integer | não |  |
| `movimentacaoFinanceira.registroFinanceiro[].tipoConta` | string | não |  |
| `movimentacaoFinanceira.registroFinanceiro[].tipoConjunto` | string | não |  |
| `movimentacaoFinanceira.registroFinanceiro[].descricao` | string | não | aceita null |
| `movimentacaoFinanceira.registroFinanceiro[].produtoId` | integer | não | aceita null |
| `movimentacaoFinanceira.registroFinanceiro[].fornecedorId` | integer | não | aceita null |
| `movimentacaoFinanceira.registroFinanceiro[].contasCaixasId` | integer | não | aceita null |
| `movimentacaoFinanceira.duplicatas` | lista de objeto | não |  |
| `movimentacaoFinanceira.duplicatas[].vencimento` | string (date) | não |  |
| `movimentacaoFinanceira.duplicatas[].observacao` | string | não | aceita null |
| `movimentacaoFinanceira.duplicatas[].valor` | number | não |  |
| `movimentacaoFinanceira.duplicatas[].aVista` | boolean | não |  |
| `movimentacaoFinanceira.duplicatas[].valorPago` | number | não | aceita null |
| `movimentacaoFinanceira.duplicatas[].pago` | boolean | não | padrão `False` |
| `movimentacaoFinanceira.duplicatas[].dataPagamento` | string (date) | não | aceita null |
| `movimentacaoFinanceira.duplicatas[].tipoDePagamentoId` | integer | não | aceita null |
| `movimentacaoFinanceira.duplicatas[].contaCaixaId` | integer | não | aceita null |
| `movimentacaoFinanceira.categoriaDePagamentoId` | integer | não |  |
| `movimentacaoFinanceira.centroDeCustoId` | integer | não |  |
| `aprovacaoFarolToken` | string | não | aceita null; Necessário se o farol de rentabilidade estiver amarelo/vermelho e os parâmetros exigirem aprovação. |
| `aprovacaoFarolPendenteId` | integer | não | aceita null |

**Respostas:**
- `201` Orçamento atualizado — campos: `message`, `data`
- `400` responsavelId ausente/inválido
- `409` Orçamento já aprovado não pode ser editado

### `PUT /orcamentos/status/{idOrcamento}/{idStatus}`

- **Permissão:** `orcamento:update` · **Manual:** [op-put-orcamentos-status-idorcamento-idstatus](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-put-orcamentos-status-idorcamento-idstatus)
- **Resumo:** Alterar status do orçamento
- **Descrição:** Ao aprovar, promove agendamentos vinculados que estavam pendentes de orçamento e sincroniza o financeiro.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `idOrcamento` | path | integer | **sim** |  |
| `idStatus` | path | integer | **sim** |  |

**Respostas:**
- `200` Efeitos colaterais que não aparecem na resposta: pode promover agendamentos vinculados para "Confirmado", disparar notificação, sincronizar MovimentacaoFinanceira/duplicatas. — campos: `message`, `data`

### `GET /orcamentos/{id}/{isAgendamento}`

- **Permissão:** `orcamento:read` · **Manual:** [op-get-orcamentos-id-isagendamento](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-orcamentos-id-isagendamento)
- **Resumo:** Consultar orçamento
- **Descrição:** `isAgendamento` indica se o `id` é de orçamento ou de agendamento vinculado (`1` ou `0`).

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do orçamento |
| `isAgendamento` | path | string | **sim** | valores: `0`, `1` |

**Respostas:**
- `200` Orçamento — campos: `id`, `statusId`, `financeiroOrcamentoId`
- `404` Orçamento não encontrado

### `GET /orcamentos/anexo/listar/{orcamentoId}`

- **Permissão:** `orcamento:read` · **Manual:** [op-get-orcamentos-anexo-listar-orcamentoid](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-orcamentos-anexo-listar-orcamentoid)
- **Resumo:** Listar anexos do orçamento
- **Descrição:** Sem URL assinada (só `link` cru — chave do storage). Se precisar da URL pra baixar, use `GET /orcamentos/anexo/listar-necessarios/{pacienteId}`.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `orcamentoId` | path | integer | **sim** |  |

**Respostas:**
- `200` Array direto (sem envelope), ordenado por `createdAt` desc. — lista crua: `createdAt`, `anexoPaciente`

### `GET /orcamentos/anexo/listar-necessarios/{pacienteId}`

- **Permissão:** `orcamento:read` · **Manual:** [op-get-orcamentos-anexo-listar-necessarios-pacienteid](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-orcamentos-anexo-listar-necessarios-pacienteid)
- **Resumo:** Listar documentos necessários para o paciente
- **Descrição:** Agrupado por tipo de anexo. Anexos do paciente sem `tipoAnexoId` são excluídos silenciosamente do resultado inteiro.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `pacienteId` | path | integer | **sim** |  |
| `orcamentoId` | query | integer | não | Se informado, marca quais anexos já estão vinculados a ESTE orçamento (`anexado`). Sem isso, todos vêm `anexado:false`. |

**Respostas:**
- `200` Array direto (sem envelope), grupos com algum anexado primeiro. — lista crua: `id`, `titulo`, `anexos`

### `POST /orcamentos/anexo/vincular/{anexoId}/{orcamentoId}`

- **Permissão:** `orcamento:update` · **Manual:** [op-post-orcamentos-anexo-vincular-anexoid-orcamentoid](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-orcamentos-anexo-vincular-anexoid-orcamentoid)
- **Resumo:** Vincular/desvincular anexo do orçamento (toggle)
- **Descrição:** **Não é idempotente — é um toggle.** Se o vínculo não existe, cria; se já existe, remove. Chamar duas vezes seguidas vincula e depois desvincula. Não é seguro re-tentar cegamente em caso de timeout/retry automático, já que a resposta vazia não informa qual dos dois estados resultou.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `anexoId` | path | integer | **sim** |  |
| `orcamentoId` | path | integer | **sim** |  |

**Respostas:**
- `204` Vínculo alternado (criado ou removido, conforme o estado anterior) — sem corpo.
- `404` Anexo não encontrado
