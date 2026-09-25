# Rotas — Parâmetros (45 operações) — parte 2 de 2

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 -m ferramentas.rabi_api.atualizar_spec` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

Outras partes: [parte 1](parametros-parte-1.md).

### `PATCH /parametros/servicos-online/habilitar`

- **Permissão:** `parametro:update` · **Manual:** [op-patch-parametros-servicos-online-habilitar](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-patch-parametros-servicos-online-habilitar)
- **Resumo:** Habilitar/desabilitar agendamento online
- **Descrição:** **O campo do corpo é `habilitar`, não `habilitado`** (a spec já documentou o nome errado antes — corrigido aqui). Coerção é `Boolean(habilitar)` (truthy JS: qualquer string não vazia vira `true`; só `false`/`0`/`""`/`null`/`undefined` viram `false`). Todas as 6 rotas `*/habilitar` mexem em UM único registro singleton (`AgendamentoOnline`, id fixo 1) e a resposta é sempre a **linha inteira**, não só o campo alterado — na primeira chamada de qualquer uma delas, os campos ainda não tocados assumem o default do schema (`habilitarEtapaAgendamento` começa `true`; os demais começam `false`), o que pode surpreender.

**Corpo** (`application/json`):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `habilitar` | boolean | não |  |

**Respostas:**
- `200` Linha completa do singleton AgendamentoOnline (afeta `habilitarAgendamentoOnline`). — campos: `id`, `habilitarAgendamentoOnline`, `habilitarEtapaAgendamento`, `permitirMudancaColaborador`, `habilitarEtapaConfirmacao`, `habilitarEtapaProntuario`, `habilitarListaMedicoConvenio`, `textoEtapaConvenio`, `textoEtapaEspecialidade`, `textoEtapaServico`, `textoEtapaDocumentos`, `textoEtapaProfissional`, `textoEtapaData`, `textoEtapaConfirmacao`, `createdAt`, `updatedAt`

### `PATCH /parametros/servicos-online/agendamento/habilitar`

- **Permissão:** `parametro:update` · **Manual:** [op-patch-parametros-servicos-online-agendamento-habilitar](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-patch-parametros-servicos-online-agendamento-habilitar)
- **Resumo:** Habilitar/desabilitar etapa de agendamento online
- **Descrição:** **Campo do corpo é `habilitar`, não `habilitado`** — ver detalhes em `PATCH /parametros/servicos-online/habilitar`. Afeta `habilitarEtapaAgendamento`.

**Corpo** (`application/json`):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `habilitar` | boolean | não |  |

**Respostas:**
- `200` Linha completa do singleton AgendamentoOnline. — campos: `id`, `habilitarAgendamentoOnline`, `habilitarEtapaAgendamento`, `permitirMudancaColaborador`, `habilitarEtapaConfirmacao`, `habilitarEtapaProntuario`, `habilitarListaMedicoConvenio`, `textoEtapaConvenio`, `textoEtapaEspecialidade`, `textoEtapaServico`, `textoEtapaDocumentos`, `textoEtapaProfissional`, `textoEtapaData`, `textoEtapaConfirmacao`, `createdAt`, `updatedAt`

### `PATCH /parametros/servicos-online/agendamento/mudanca-colaborador/habilitar`

- **Permissão:** `parametro:update` · **Manual:** [op-patch-parametros-servicos-online-agendamento-mudanca-colaborador-habilitar](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-patch-parametros-servicos-online-agendamento-mudanca-colaborador-habilitar)
- **Resumo:** Habilitar/desabilitar troca de colaborador no agendamento online
- **Descrição:** **Campo do corpo é `habilitar`, não `habilitado`** — ver detalhes em `PATCH /parametros/servicos-online/habilitar`. Afeta `permitirMudancaColaborador`.

**Corpo** (`application/json`):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `habilitar` | boolean | não |  |

**Respostas:**
- `200` Linha completa do singleton AgendamentoOnline. — campos: `id`, `habilitarAgendamentoOnline`, `habilitarEtapaAgendamento`, `permitirMudancaColaborador`, `habilitarEtapaConfirmacao`, `habilitarEtapaProntuario`, `habilitarListaMedicoConvenio`, `textoEtapaConvenio`, `textoEtapaEspecialidade`, `textoEtapaServico`, `textoEtapaDocumentos`, `textoEtapaProfissional`, `textoEtapaData`, `textoEtapaConfirmacao`, `createdAt`, `updatedAt`

### `PATCH /parametros/servicos-online/confirmacao/habilitar`

- **Permissão:** `parametro:update` · **Manual:** [op-patch-parametros-servicos-online-confirmacao-habilitar](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-patch-parametros-servicos-online-confirmacao-habilitar)
- **Resumo:** Habilitar/desabilitar etapa de confirmação no agendamento online
- **Descrição:** **Campo do corpo é `habilitar`, não `habilitado`** — ver detalhes em `PATCH /parametros/servicos-online/habilitar`. Afeta `habilitarEtapaConfirmacao`.

**Corpo** (`application/json`):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `habilitar` | boolean | não |  |

**Respostas:**
- `200` Linha completa do singleton AgendamentoOnline. — campos: `id`, `habilitarAgendamentoOnline`, `habilitarEtapaAgendamento`, `permitirMudancaColaborador`, `habilitarEtapaConfirmacao`, `habilitarEtapaProntuario`, `habilitarListaMedicoConvenio`, `textoEtapaConvenio`, `textoEtapaEspecialidade`, `textoEtapaServico`, `textoEtapaDocumentos`, `textoEtapaProfissional`, `textoEtapaData`, `textoEtapaConfirmacao`, `createdAt`, `updatedAt`

### `PATCH /parametros/servicos-online/prontuario/habilitar`

- **Permissão:** `parametro:update` · **Manual:** [op-patch-parametros-servicos-online-prontuario-habilitar](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-patch-parametros-servicos-online-prontuario-habilitar)
- **Resumo:** Habilitar/desabilitar etapa de prontuário no agendamento online
- **Descrição:** **Campo do corpo é `habilitar`, não `habilitado`** — ver detalhes em `PATCH /parametros/servicos-online/habilitar`. Afeta `habilitarEtapaProntuario`.

**Corpo** (`application/json`):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `habilitar` | boolean | não |  |

**Respostas:**
- `200` Linha completa do singleton AgendamentoOnline. — campos: `id`, `habilitarAgendamentoOnline`, `habilitarEtapaAgendamento`, `permitirMudancaColaborador`, `habilitarEtapaConfirmacao`, `habilitarEtapaProntuario`, `habilitarListaMedicoConvenio`, `textoEtapaConvenio`, `textoEtapaEspecialidade`, `textoEtapaServico`, `textoEtapaDocumentos`, `textoEtapaProfissional`, `textoEtapaData`, `textoEtapaConfirmacao`, `createdAt`, `updatedAt`

### `PATCH /parametros/servicos-online/lista-medico-convenio/habilitar`

- **Permissão:** `parametro:update` · **Manual:** [op-patch-parametros-servicos-online-lista-medico-convenio-habilitar](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-patch-parametros-servicos-online-lista-medico-convenio-habilitar)
- **Resumo:** Habilitar/desabilitar lista de médico por convênio no agendamento online
- **Descrição:** **Campo do corpo é `habilitar`, não `habilitado`** — ver detalhes em `PATCH /parametros/servicos-online/habilitar`. Afeta `habilitarListaMedicoConvenio`.

**Corpo** (`application/json`):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `habilitar` | boolean | não |  |

**Respostas:**
- `200` Linha completa do singleton AgendamentoOnline. — campos: `id`, `habilitarAgendamentoOnline`, `habilitarEtapaAgendamento`, `permitirMudancaColaborador`, `habilitarEtapaConfirmacao`, `habilitarEtapaProntuario`, `habilitarListaMedicoConvenio`, `textoEtapaConvenio`, `textoEtapaEspecialidade`, `textoEtapaServico`, `textoEtapaDocumentos`, `textoEtapaProfissional`, `textoEtapaData`, `textoEtapaConfirmacao`, `createdAt`, `updatedAt`

### `PATCH /parametros/servicos-online/textos-informativos`

- **Permissão:** `parametro:update` · **Manual:** [op-patch-parametros-servicos-online-textos-informativos](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-patch-parametros-servicos-online-textos-informativos)
- **Resumo:** Atualizar textos informativos do agendamento online
- **Descrição:** Mesmo singleton `AgendamentoOnline` das rotas `*/habilitar` — campo omitido fica inalterado (Prisma ignora `undefined`); na primeira criação, vira `null`.

**Corpo** (`application/json`):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `textoEtapaConvenio` | string | não | aceita null |
| `textoEtapaEspecialidade` | string | não | aceita null |
| `textoEtapaServico` | string | não | aceita null |
| `textoEtapaDocumentos` | string | não | aceita null |
| `textoEtapaProfissional` | string | não | aceita null |
| `textoEtapaData` | string | não | aceita null |
| `textoEtapaConfirmacao` | string | não | aceita null |

**Respostas:**
- `200` Linha completa do singleton AgendamentoOnline — inclui os 6 booleans de habilitação também, não só os textos. — campos: `id`, `habilitarAgendamentoOnline`, `habilitarEtapaAgendamento`, `permitirMudancaColaborador`, `habilitarEtapaConfirmacao`, `habilitarEtapaProntuario`, `habilitarListaMedicoConvenio`, `textoEtapaConvenio`, `textoEtapaEspecialidade`, `textoEtapaServico`, `textoEtapaDocumentos`, `textoEtapaProfissional`, `textoEtapaData`, `textoEtapaConfirmacao`, `createdAt`, `updatedAt`

### `GET /parametros/servicos-online/agendamento/perguntas`

- **Permissão:** `parametro:read` · **Manual:** [op-get-parametros-servicos-online-agendamento-perguntas](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-get-parametros-servicos-online-agendamento-perguntas)
- **Resumo:** Listar perguntas do agendamento online

**Respostas:**
- `200` Lista de perguntas — lista crua de `PerguntaAgendamentoOnline`: `id`, `pergunta`, `createdAt`, `especialidades`

### `POST /parametros/servicos-online/agendamento/perguntas`

- **Permissão:** `parametro:create` · **Manual:** [op-post-parametros-servicos-online-agendamento-perguntas](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-post-parametros-servicos-online-agendamento-perguntas)
- **Resumo:** Criar pergunta do agendamento online

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `pergunta` | string | **sim** |  |
| `especialidadeIds` | lista de integer | não | Vazio/omitido = pergunta global, sem restrição de especialidade |

**Respostas:**
- `201` Pergunta criada — campos: `id`, `pergunta`, `createdAt`, `especialidades`

### `GET /parametros/servicos-online/agendamento/perguntas/por-especialidade`

- **Permissão:** `parametro:read` · **Manual:** [op-get-parametros-servicos-online-agendamento-perguntas-por-especialidade](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-get-parametros-servicos-online-agendamento-perguntas-por-especialidade)
- **Resumo:** Listar perguntas por especialidade
- **Descrição:** Sem `especialidadeIds`, só devolve as perguntas globais (sem restrição).

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `especialidadeIds` | query | string | não | IDs separados por vírgula |

**Respostas:**
- `200` Lista de perguntas — lista crua de `PerguntaAgendamentoOnline`: `id`, `pergunta`, `createdAt`, `especialidades`

### `PUT /parametros/servicos-online/agendamento/perguntas/{id}`

- **Permissão:** `parametro:update` · **Manual:** [op-put-parametros-servicos-online-agendamento-perguntas-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-put-parametros-servicos-online-agendamento-perguntas-id)
- **Resumo:** Atualizar pergunta do agendamento online

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |

**Corpo** (`application/json`):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `pergunta` | string | não |  |
| `especialidadeIds` | lista de integer | não |  |

**Respostas:**
- `200` Pergunta atualizada — campos: `id`, `pergunta`, `createdAt`, `especialidades`

### `DELETE /parametros/servicos-online/agendamento/perguntas/{id}`

- **Permissão:** `parametro:delete` · **Manual:** [op-delete-parametros-servicos-online-agendamento-perguntas-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-delete-parametros-servicos-online-agendamento-perguntas-id)
- **Resumo:** Excluir pergunta do agendamento online
- **Descrição:** Exclusão lógica (`deleted = true`).

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |

**Respostas:**
- `204` Pergunta excluída — sem corpo de resposta

### `GET /parametros/servicos-online/agendamento/perguntas/colaborador/{colaboradorId}`

- **Permissão:** `parametro:read` · **Manual:** [op-get-parametros-servicos-online-agendamento-perguntas-colaborador-colaboradorid](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-get-parametros-servicos-online-agendamento-perguntas-colaborador-colaboradorid)
- **Resumo:** Listar perguntas vinculadas a um colaborador

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `colaboradorId` | path | integer | **sim** |  |

**Respostas:**
- `200` Lista de perguntas — lista crua de `PerguntaAgendamentoOnline`: `id`, `pergunta`, `createdAt`, `especialidades`

### `POST /parametros/servicos-online/agendamento/perguntas/{perguntaId}/colaborador/{colaboradorId}`

- **Permissão:** `parametro:update` · **Manual:** [op-post-parametros-servicos-online-agendamento-perguntas-perguntaid-colaborador-colaboradorid](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-post-parametros-servicos-online-agendamento-perguntas-perguntaid-colaborador-colaboradorid)
- **Resumo:** Vincular pergunta a um colaborador
- **Descrição:** Idempotente (`upsert` numa chave composta, sem PK própria e sem timestamps). Não valida antecipadamente se `perguntaId`/`colaboradorId` existem — se algum não existir, a violação de FK do Postgres tende a virar um erro não tratado (500), diferente de outras rotas do módulo que checam antes com `AppError`.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `perguntaId` | path | integer | **sim** |  |
| `colaboradorId` | path | integer | **sim** |  |

**Respostas:**
- `200` Só as duas colunas da chave composta — note que o campo é `perguntaAgendamentoId`, não `perguntaId` como no path. — campos: `colaboradorId`, `perguntaAgendamentoId`

### `GET /parametros/termo`

- **Permissão:** `parametro:read` · **Manual:** [op-get-parametros-termo](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-get-parametros-termo)
- **Resumo:** Consultar parâmetros de termo de consentimento
- **Descrição:** Devolve `null` (200) se nunca configurado.

**Respostas:**
- `200` Parâmetros de termo, ou null — campos: `id`, `conteudo`, `ativo`

### `PUT /parametros/termo`

- **Permissão:** `parametro:update` · **Manual:** [op-put-parametros-termo](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-put-parametros-termo)
- **Resumo:** Atualizar parâmetros de termo de consentimento
- **Descrição:** Único PUT deste grupo que valida de verdade: `conteudo` é obrigatório. `findFirst({where:{ativo:true, deleted:false}})`.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `conteudo` | string | **sim** |  |

**Respostas:**
- `200` Row completa — inclui `createdAt`/`updatedAt`/`deleted`, que o GET desta mesma rota não lista hoje. — campos: `id`, `conteudo`, `ativo`, `createdAt`, `updatedAt`, `deleted`
- `400` O conteúdo do termo é obrigatório

### `GET /parametros/dashboard-permissoes/graficos`

- **Permissão:** `parametro:read` · **Manual:** [op-get-parametros-dashboard-permissoes-graficos](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-get-parametros-dashboard-permissoes-graficos)
- **Resumo:** Consultar permissão de gráficos de dashboard
- **Descrição:** Controle de acesso a telas, não parâmetro de negócio. `perfilPermissaoId` é obrigatório na query.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `perfilPermissaoId` | query | integer | **sim** |  |

**Respostas:**
- `200` Permissões — campos: `perfilPermissaoId`, `permissoes`
- `400` perfilPermissaoId ausente/inválido

### `PUT /parametros/dashboard-permissoes/graficos`

- **Permissão:** `parametro:update` · **Manual:** [op-put-parametros-dashboard-permissoes-graficos](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-put-parametros-dashboard-permissoes-graficos)
- **Resumo:** Atualizar permissão de gráficos de dashboard
- **Descrição:** **Controle de acesso**: define quem vê quais gráficos.

**Corpo** (`application/json`):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `perfilPermissaoId` | integer | **sim** |  |
| `permissoes` | lista de objeto | **sim** |  |
| `permissoes[].id` | string | não |  |
| `permissoes[].habilitado` | boolean | não |  |

**Respostas:**
- `200` Confirmação, sem devolver os dados salvos — campos: `message`

### `GET /parametros/dashboard-permissoes/dashboards`

- **Permissão:** `parametro:read` · **Manual:** [op-get-parametros-dashboard-permissoes-dashboards](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-get-parametros-dashboard-permissoes-dashboards)
- **Resumo:** Consultar permissão de dashboards
- **Descrição:** Controle de acesso a telas, não parâmetro de negócio. `perfilPermissaoId` é obrigatório na query.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `perfilPermissaoId` | query | integer | **sim** |  |

**Respostas:**
- `200` Permissões — campos: `perfilPermissaoId`, `permissoes`
- `400` perfilPermissaoId ausente/inválido

### `PUT /parametros/dashboard-permissoes/dashboards`

- **Permissão:** `parametro:update` · **Manual:** [op-put-parametros-dashboard-permissoes-dashboards](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-put-parametros-dashboard-permissoes-dashboards)
- **Resumo:** Atualizar permissão de dashboards
- **Descrição:** **Controle de acesso**: define quem vê quais painéis.

**Corpo** (`application/json`):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `perfilPermissaoId` | integer | **sim** |  |
| `permissoes` | lista de objeto | **sim** |  |
| `permissoes[].id` | string | não |  |
| `permissoes[].habilitado` | boolean | não |  |

**Respostas:**
- `200` Confirmação, sem devolver os dados salvos — campos: `message`

### `GET /parametros/dashboard-atribuicao`

- **Permissão:** `parametro:read` · **Manual:** [op-get-parametros-dashboard-atribuicao](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-get-parametros-dashboard-atribuicao)
- **Resumo:** Consultar atribuição de dashboard
- **Descrição:** `perfilPermissaoId` é obrigatório na query — diferente das duas rotas de permissão acima, esta não ecoa o valor de volta na resposta.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `perfilPermissaoId` | query | integer | **sim** |  |

**Respostas:**
- `200` Atribuições — campos: `dashboardIds`, `homeDashboardId`
- `400` perfilPermissaoId ausente

### `PUT /parametros/dashboard-atribuicao`

- **Permissão:** `parametro:update` · **Manual:** [op-put-parametros-dashboard-atribuicao](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#op-put-parametros-dashboard-atribuicao)
- **Resumo:** Atualizar atribuição de dashboard
- **Descrição:** **Controle de acesso**: define qual dashboard cada colaborador/grupo enxerga.

**Corpo** (`application/json`):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `perfilPermissaoId` | integer | **sim** |  |
| `dashboardIds` | lista de string | **sim** |  |
| `homeDashboardId` | string | não | aceita null |

**Respostas:**
- `200` Confirmação, sem devolver os dados salvos — campos: `message`
