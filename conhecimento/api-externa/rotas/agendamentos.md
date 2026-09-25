# Rotas — Agendamentos (8 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 -m ferramentas.rabi_api.atualizar_spec` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `GET /agendamentos/datas/disponiveis`
- `POST /agendamentos/horarios/disponiveis`
- `GET /agendamentos/locais/disponiveis`
- `GET /agendamentos/motivo-cancelamento`
- `GET /agendamentos`
- `POST /agendamentos`
- `GET /agendamentos/{id}`
- `PATCH /agendamentos/{id}/cancelar`

### `GET /agendamentos/datas/disponiveis`

- **Permissão:** `agendamento:read` · **Manual:** [op-get-agendamentos-datas-disponiveis](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-agendamentos-datas-disponiveis)
- **Resumo:** Datas disponíveis para agendamento

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `dataSelecionada` | query | string (date) | não |  |
| `horarioInicio` | query | string | não |  |
| `localId` | query | integer | não |  |
| `responsavelId` | query | integer | não | ID do colaborador ou equipamento |
| `tipoResponsavel` | query | string | não | valores: `COLABORADOR`, `EQUIPAMENTO` |

**Respostas:**
- `200` **`responsavelId` é obrigatório na prática** — sem ele a rota devolve `{datasDisponiveis: [], message: "Data disponível com grades encontradas"}` direto, ignorando os outros filtros. `tipoResponsavel` deve ser exatamente `COLABORADOR` ou `EQUIPAMENTO` (case-sensitive); outro valor cai no mesmo fall… — campos: `datasDisponiveis`, `message`

### `POST /agendamentos/horarios/disponiveis`

- **Permissão:** `agendamento:read` · **Manual:** [op-post-agendamentos-horarios-disponiveis](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-agendamentos-horarios-disponiveis)
- **Resumo:** Horários disponíveis numa data

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `tipo` | string | **sim** | valores: `COLABORADOR`, `EQUIPAMENTO` |
| `data` | string (date) | **sim** |  |
| `localId` | integer | **sim** |  |
| `agendamentoId` | integer | **sim** | Obrigatório mesmo pra buscar horários de um agendamento novo — usado internamente pra saber qual horário já é "do próprio" ao editar. |
| `colaboradorId` | integer | não |  |
| `isEncaixe` | boolean | não | padrão `False`; false (padrão): só retorna slots com status "Disponível" e não bloqueados, ou o slot que já é do próprio agendamentoId. true: retorna todos os slots da grade,… |

**Respostas:**
- `200` Array direto (sem envelope). — lista crua: `id`, `gradeId`, `tipoResponsavel`, `horario`
- `400` tipo/data ausente ou inválido

### `GET /agendamentos/locais/disponiveis`

- **Permissão:** `agendamento:read` · **Manual:** [op-get-agendamentos-locais-disponiveis](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-agendamentos-locais-disponiveis)
- **Resumo:** Locais disponíveis para agendamento

**Respostas:**
- `200` Envelope de lista padrão, mas `page`/`pageSize` não são paginação real — sempre devolve tudo (`page:1`, `pageSize:total`). — campos: `dados`, `page`, `pageSize`, `total`, `totalPages`; item de `dados`: `id`, `nome`, `empresaId`, `depositoPadraoSaidaId`, `ativo`, `createdAt`, `updatedAt`, `empresa`

### `GET /agendamentos/motivo-cancelamento`

- **Permissão:** `agendamento:read` · **Manual:** [op-get-agendamentos-motivo-cancelamento](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-agendamentos-motivo-cancelamento)
- **Resumo:** Listar motivos de cancelamento
- **Descrição:** Necessário para escolher `motivoCancelamentoId` ao cancelar. **Bug conhecido:** em erro de banco, o use case não lança — devolve o número `401` como "resultado", e a rota responde **200 com corpo `401`** (número cru) em vez de um erro HTTP de verdade. Reportado ao time.

**Respostas:**
- `200` Envelope de lista padrão (`page:1`, `pageSize:total`, sem paginação real). Ver bug acima sobre o corpo `401`. — um de: campos: `dados`, `page`, `pageSize`, `total`, `totalPages`; item de `dados`: `id`, `descricao` \\| integer

### `GET /agendamentos`

- **Permissão:** `agendamento:read` · **Manual:** [op-get-agendamentos](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-agendamentos)
- **Resumo:** Listar agendamentos
- **Descrição:** `data` é obrigatório — a consulta interna sempre filtra por um dia (não dá pra listar vários dias de uma vez nesta rota).

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `data` | query | string (date) | **sim** |  |
| `profissionalId` | query | integer | não |  |
| `pacienteId` | query | integer | não |  |
| `statusId` | query | integer | não |  |
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |

**Respostas:**
- `200` Lista paginada (do dia informado) — campos: `dados`, `page`, `pageSize`, `total`, `totalPages`; item de `dados`: `id`, `pacienteId`, `statusId`, `dataAgendamento`
- `400` Informe data

### `POST /agendamentos`

- **Permissão:** `agendamento:create` · **Manual:** [op-post-agendamentos](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-agendamentos)
- **Resumo:** Criar agendamento
- **Descrição:** **Sem pagamento no ato** — o campo `movimentacaoFinanceira` não é suportado por esta API (dispara emissão automática de NFS-e). Consome o limite mensal do plano (`agendamentos.mes`).

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `responsavelId` | integer | **sim** | ID de um colaborador já cadastrado. |
| `paciente` | objeto | **sim** |  |
| `paciente.id` | string | **sim** |  |
| `local` | objeto | não |  |
| `local.id` | integer | não |  |
| `idGrade` | integer | **sim** | ID da grade de colaborador/equipamento |
| `tipoAtendimento` | string | não | valores: `COLABORADOR`, `EQUIPAMENTO` |
| `data` | string (date) | **sim** |  |
| `hora` | string | não |  |
| `horaFim` | string | não | aceita null |
| `statusId` | integer | **sim** | 1=Confirmado, 3=Aguardando, 11=Pendente Autorização, etc. |
| `procedimentos` | lista de objeto | **sim** |  |
| `procedimentos[].procedimentoId` | integer | **sim** | ID do serviço |
| `procedimentos[].convenioId` | integer | **sim** |  |
| `procedimentos[].planoId` | integer | não | aceita null |
| `procedimentos[].colaboradorId` | integer | não | aceita null |
| `procedimentos[].horarioInicio` | string | não | aceita null |
| `procedimentos[].horarioFim` | string | não | aceita null |
| `contatos` | lista de objeto | não |  |
| `contatos[].email` | string | não |  |
| `contatos[].celular` | string | não |  |
| `repetir` | boolean | não | padrão `False` |
| `encaixe` | boolean | não | padrão `False` |

**Respostas:**
- `201` Agendamento criado — campos: `id`, `pacienteId`, `statusId`, `dataAgendamento`
- `400` Pagamento no ato não é suportado por esta API, ou responsavelId ausente/inválido
- `409` Conflito de horário/farol de rentabilidade bloqueando a criação

### `GET /agendamentos/{id}`

- **Permissão:** `agendamento:read` · **Manual:** [op-get-agendamentos-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-agendamentos-id)
- **Resumo:** Consultar agendamento

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do agendamento |

**Respostas:**
- `200` Agendamento — campos: `id`, `pacienteId`, `statusId`, `dataAgendamento`
- `404` Agendamento não encontrado

### `PATCH /agendamentos/{id}/cancelar`

- **Permissão:** `agendamento:delete` · **Manual:** [op-patch-agendamentos-id-cancelar](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-patch-agendamentos-id-cancelar)
- **Resumo:** Cancelar agendamento
- **Descrição:** Libera reservas de medicamento vinculadas e notifica a fila de espera, se houver.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do agendamento |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `responsavelId` | integer | **sim** |  |
| `motivoCancelamentoId` | integer | **sim** |  |
| `descricao` | string | não | aceita null |

**Respostas:**
- `200` Corpo fixo — não reflete o resultado das notificações de fila de espera, que são disparadas de forma assíncrona (fire-and-forget) e não aparecem na resposta. — campos: `message`
- `400` Motivo de cancelamento é obrigatório, ou responsavelId ausente/inválido
- `409` Este status não pode ser cancelado (ex.: já atendido, já cancelado)
