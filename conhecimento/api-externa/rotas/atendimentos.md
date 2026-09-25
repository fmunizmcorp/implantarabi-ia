# Rotas — Atendimentos (6 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 -m ferramentas.rabi_api.atualizar_spec` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `POST /atendimentos`
- `PUT /atendimentos/{id}`
- `GET /atendimentos/{id}`
- `POST /atendimentos/prontuario`
- `POST /atendimentos/novo-prontuario`
- `GET /atendimentos/historico`

### `POST /atendimentos`

- **Permissão:** `atendimento:create` · **Manual:** [op-post-atendimentos](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-atendimentos)
- **Resumo:** Criar atendimento
- **Descrição:** Voltado a migração de histórico — cria por trás um Agendamento sintético e um prontuário vazio. `horarioInicioAtendimento` sempre grava "agora"; use `PUT /{id}` com `horarioInicio` para corrigir com a data real.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `pacienteId` | integer | **sim** |  |
| `colaboradorId` | integer | **sim** |  |
| `empresaId` | integer | **sim** |  |
| `servicoId` | integer | **sim** |  |
| `convenioId` | integer | **sim** |  |
| `dataAtendimento` | string (date-time) | não | aceita null; Usada só no Agendamento sintético criado por trás. O Atendimento em si sempre grava a data/hora de agora — use PUT /{id} com `horarioInicio` para corrigir com… |

**Respostas:**
- `201` Atendimento criado — campos: `atendimentoId`, `agendamentoId`, `prontuarioId`
- `400` Campo obrigatório faltando ou inválido

### `PUT /atendimentos/{id}`

- **Permissão:** `atendimento:update` · **Manual:** [op-put-atendimentos-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-put-atendimentos-id)
- **Resumo:** Atualizar atendimento
- **Descrição:** Principal uso: corrigir `horarioInicio` com a data real de um atendimento migrado.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do atendimento |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `responsavelId` | integer | **sim** | ID de um colaborador já cadastrado. |
| `pacienteId` | integer | não | aceita null |
| `empresaId` | integer | não | aceita null |
| `tempoDoAtendimento` | integer | não | aceita null; Em minutos |
| `horarioInicio` | string (date-time) | não | aceita null; Corrige a data/hora real do atendimento — usado em migração. |
| `DocumentosAtendimentos` | lista de objeto | não | Conteúdo de DocumentoAtendimento (documento administrativo, diferente do prontuário). |
| `version` | integer | não | aceita null; Trava otimista — envie a versão atual do registro. |

**Respostas:**
- `202` Devolve o registro cru de `Atendimento` (sem includes de paciente/documentos). Se `DocumentosAtendimentos` foi enviado no corpo, é processado à parte e não aparece na resposta. — campos: `id`, `ativo`, `deleted`, `createdAt`, `updatedAt`, `pacienteId`, `empresaId`, `agendamentoId`, `horarioInicioAtendimento`, `horarioFimAtendimento`, `tempoDoAtendimento`, `colaboradorId`, `colaboradorCriadorId`, `updatedByColaboradorId`, `deletedAt`, `deletedByColaboradorId`, `motivoExclusao`, `version`, `origemPreFaturamento`
- `400` responsavelId ausente/inválido
- `409` Versão desatualizada (conflito de edição concorrente) — recarregue e tente de novo

### `GET /atendimentos/{id}`

- **Permissão:** `atendimento:read` · **Manual:** [op-get-atendimentos-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-atendimentos-id)
- **Resumo:** Consultar atendimento
- **Descrição:** Todos os segmentos são opcionais: `/atendimentos/{id}`, `/atendimentos/{id}/{pacienteId}` ou filtre só por paciente/agendamento. **Se `id` não existir, devolve 200 com corpo `[]` (array vazio), não 404.**

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | não | mín. 1; ID do atendimento |

**Respostas:**
- `200` Objeto do atendimento (com paciente e agendamento incluídos, agendamento inclui status e convênios do paciente) quando encontrado — **ou array vazio `[]` se o id não existir**. — um de: object \\| lista crua

### `POST /atendimentos/prontuario`

- **Permissão:** `atendimento:update` · **Manual:** [op-post-atendimentos-prontuario](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-atendimentos-prontuario)
- **Resumo:** Editar prontuário
- **Descrição:** **Sobrescreve o texto no lugar — não guarda a versão anterior.**

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `prontuarioId` | integer | **sim** |  |
| `conteudo` | string | **sim** | Texto clínico livre. **Sobrescreve o valor atual, sem guardar a versão anterior.** |

**Respostas:**
- `202` Devolve o registro cru de ProntuarioAtendimento. — campos: `id`, `conteudoProntuario`, `createdAt`, `updatedAt`, `atendimentoId`, `TipoDocumentoAtendimentoId`

### `POST /atendimentos/novo-prontuario`

- **Permissão:** `atendimento:create` · **Manual:** [op-post-atendimentos-novo-prontuario](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-atendimentos-novo-prontuario)
- **Resumo:** Criar um novo prontuário no atendimento
- **Descrição:** Cria uma linha nova (o atendimento pode ter mais de um prontuário) — não edita o existente.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `AgendamentoId` | integer | não | aceita null; Informe este ou atendimentoId |
| `atendimentoId` | integer | não | aceita null |

**Respostas:**
- `200` **Corpo de sucesso é um inteiro cru — o id do prontuário recém-criado**, não um objeto. — integer
- `400` agendamentoId ou atendimentoId são obrigatórios
- `404` Agendamento ou atendimento não encontrado

### `GET /atendimentos/historico`

- **Permissão:** `atendimento:read` · **Manual:** [op-get-atendimentos-historico](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-atendimentos-historico)
- **Resumo:** Histórico do paciente (linha do tempo)
- **Descrição:** Leitura ao vivo — reflete qualquer edição de prontuário na hora. `pacienteId` é obrigatório nesta API (a rota interna aceita omitir, mas sem filtro ela varre o histórico inteiro do tenant e pode travar/estourar tempo). **Sem paginação real** — sempre devolve o histórico completo que casar com os filtros, um item por atendimento encontrado.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `pacienteId` | query | integer | **sim** |  |
| `medico` | query | integer | não | ID do colaborador |
| `servico` | query | integer | não |  |
| `dataAtendimento` | query | string (date) | não | Filtra por createdAt do atendimento, não pela data do agendamento vinculado |

**Respostas:**
- `200` Array direto (sem envelope de paginação). — lista crua: `conteudoProntuario`, `atendimento`, `tipoDocumentoAtendimento`, `servicoAtendimento`, `taxaDocumento`
- `400` Informe pacienteId
