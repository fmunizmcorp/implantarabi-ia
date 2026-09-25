# Rotas — Grade de Colaborador (7 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 ferramentas/rabi_api/atualizar_spec.py` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `GET /grades-colaborador`
- `POST /grades-colaborador`
- `GET /grades-colaborador/filter`
- `GET /grades-colaborador/{id}`
- `PUT /grades-colaborador/{id}`
- `DELETE /grades-colaborador/{id}`
- `DELETE /grades-colaborador/unique/{id}`

### `GET /grades-colaborador`

- **Permissão:** `gradeColaborador:read` · **Manual:** [op-get-grades-colaborador](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-grades-colaborador)
- **Resumo:** Listar grade de colaborador
- **Descrição:** Paginado de verdade — use `page`/`pageSize` e os filtros abaixo para não trazer a grade inteira da clínica.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |
| `colaboradorId` | query | integer | não |  |
| `localId` | query | integer | não |  |
| `vigenteEm` | query | string (date) | não | Só grades vigentes nessa data (entre `vigenteDesde` e `vigenteAte`, ou sem `vigenteAte`). |

**Respostas:**
- `200` Lista paginada — campos: `dados`, `page`, `pageSize`, `total`, `totalPages`; item de `dados`: `id`, `localId`, `colaboradorId`, `inicioAtendimento`, `fimAtendimento`, `vigenteDesde`, `vigenteAte`, `ativo`, `copiaId`, `tempoAtendimento`, `repetir`, `diasDaSemana`, `maximoEncaixePorDia`, `maximoEncaixePorHorario`, `minimoTempoEntreEncaixes`, `agendamentoOnline`, `modoConvenio`, `Colaborador`, `Local`, `ColaboradorGradeEspecialidades`

### `POST /grades-colaborador`

- **Permissão:** `gradeColaborador:create` · **Manual:** [op-post-grades-colaborador](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-grades-colaborador)
- **Resumo:** Cadastrar horário(s) de grade
- **Descrição:** Já checa conflito de horário — retorna erro se o novo horário colidir com um existente.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `colaboradorGrade` | lista de objeto | **sim** | Um ou mais horários — o corpo já aceita lista, então cria vários de uma vez. |
| `colaboradorGrade[].localId` | integer | não | aceita null |
| `colaboradorGrade[].colaboradorId` | integer | **sim** |  |
| `colaboradorGrade[].inicioAtendimento` | string (date-time) | **sim** |  |
| `colaboradorGrade[].fimAtendimento` | string (date-time) | **sim** |  |
| `colaboradorGrade[].tempoAtendimento` | integer | **sim** | Duração de cada horário, em minutos |
| `colaboradorGrade[].repetir` | string | **sim** | Ex.: NAO_REPETIR, SEMANALMENTE |
| `colaboradorGrade[].diasDaSemana` | string | **sim** | Dias em que a grade se repete |
| `colaboradorGrade[].vigenteDesde` | string (date) | não | aceita null |
| `colaboradorGrade[].vigenteAte` | string (date) | não | aceita null |
| `colaboradorGrade[].maximoEncaixePorDia` | integer | não |  |
| `colaboradorGrade[].maximoEncaixePorHorario` | integer | não |  |
| `colaboradorGrade[].minimoTempoEntreEncaixes` | integer | não |  |
| `colaboradorGrade[].convenio` | lista de objeto | não | Convênios atendidos nesta grade |
| `colaboradorGrade[].convenio[].id` | integer | não |  |
| `colaboradorGrade[].convenio[].limite` | integer | não | aceita null |
| `colaboradorGrade[].equipamento` | lista de integer | não |  |
| `colaboradorGrade[].especialidades` | lista de objeto | não |  |
| `colaboradorGrade[].especialidades[].id` | integer | não |  |
| `colaboradorGrade[].servicos` | lista de objeto | não |  |
| `colaboradorGrade[].servicos[].id` | integer | não |  |
| `colaboradorGrade[].agendamentoOnline` | boolean | não | aceita null |

**Respostas:**
- `201` Grade(s) criada(s) — **comportamento real, não o esperado**: o corpo é um array de `null`, um por item enviado (ex.: `[null, null]` para 2 horários). A resposta não devolve os registros criados nem seus ids; se precisar do id, consulte depois por `GET /grades-colaborador?colaboradorId=...`. — lista crua
- `409` Conflito de horário com uma grade já existente
- `422` Falha ao criar grade do colaborador

### `GET /grades-colaborador/filter`

- **Permissão:** `gradeColaborador:read` · **Manual:** [op-get-grades-colaborador-filter](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-grades-colaborador-filter)
- **Resumo:** Filtrar grade de colaborador

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `colaboradorId` | query | integer | não |  |
| `localId` | query | integer | não |  |

**Respostas:**
- `200` Lista filtrada — lista crua de `GradeColaborador`: `id`, `localId`, `colaboradorId`, `inicioAtendimento`, `fimAtendimento`, `tempoAtendimento`, `repetir`, `diasDaSemana`

### `GET /grades-colaborador/{id}`

- **Permissão:** `gradeColaborador:read` · **Manual:** [op-get-grades-colaborador-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-grades-colaborador-id)
- **Resumo:** Consultar horário de grade

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID da grade |

**Respostas:**
- `200` Horário de grade — campos: `id`, `localId`, `colaboradorId`, `inicioAtendimento`, `fimAtendimento`, `tempoAtendimento`, `repetir`, `diasDaSemana`
- `404` Grade não encontrada

### `PUT /grades-colaborador/{id}`

- **Permissão:** `gradeColaborador:update` · **Manual:** [op-put-grades-colaborador-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-grades-colaborador-id)
- **Resumo:** Atualizar horário de grade
- **Descrição:** **O `id` do path é ignorado** — o corpo é um array direto (não um envelope) e cada item precisa ter o próprio `id`. Erros de negócio (ex.: grade não encontrada) caem no tratamento genérico e viram **500**, não 404.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID da grade |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `(corpo é uma lista)` | lista de objeto | **sim** |  |
| `[].localId` | integer | não | aceita null |
| `[].colaboradorId` | integer | **sim** |  |
| `[].inicioAtendimento` | string (date-time) | **sim** |  |
| `[].fimAtendimento` | string (date-time) | **sim** |  |
| `[].tempoAtendimento` | integer | **sim** | Duração de cada horário, em minutos |
| `[].repetir` | string | **sim** | Ex.: NAO_REPETIR, SEMANALMENTE |
| `[].diasDaSemana` | string | **sim** | Dias em que a grade se repete |
| `[].vigenteDesde` | string (date) | não | aceita null |
| `[].vigenteAte` | string (date) | não | aceita null |
| `[].maximoEncaixePorDia` | integer | não |  |
| `[].maximoEncaixePorHorario` | integer | não |  |
| `[].minimoTempoEntreEncaixes` | integer | não |  |
| `[].convenio` | lista de objeto | não | Convênios atendidos nesta grade |
| `[].convenio[].id` | integer | não |  |
| `[].convenio[].limite` | integer | não | aceita null |
| `[].equipamento` | lista de integer | não |  |
| `[].especialidades` | lista de objeto | não |  |
| `[].especialidades[].id` | integer | não |  |
| `[].servicos` | lista de objeto | não |  |
| `[].servicos[].id` | integer | não |  |
| `[].agendamentoOnline` | boolean | não | aceita null |
| `[].id` | integer | **sim** |  |

**Respostas:**
- `202` **Status real é 202, não 200. O corpo de sucesso é o número cru `201`** (não um objeto, não a grade atualizada) — comportamento observado, não documentação de intenção. — integer

### `DELETE /grades-colaborador/{id}`

- **Permissão:** `gradeColaborador:delete` · **Manual:** [op-delete-grades-colaborador-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-delete-grades-colaborador-id)
- **Resumo:** Excluir este e os próximos horários da série
- **Descrição:** Inativação lógica (`ativo=false`).

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID da grade |

**Respostas:**
- `200` **O corpo de sucesso é o número cru `201`**, não um objeto — mesmo padrão de PUT. — integer
- `404` Grade não encontrada

### `DELETE /grades-colaborador/unique/{id}`

- **Permissão:** `gradeColaborador:delete` · **Manual:** [op-delete-grades-colaborador-unique-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-delete-grades-colaborador-unique-id)
- **Resumo:** Excluir só este horário (não a série)
- **Descrição:** Diferente do DELETE de série: este é uma **exclusão física** (`prisma.colaboradorGrade.delete`), não inativação lógica.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID da grade |

**Respostas:**
- `200` **O corpo de sucesso é o número cru `201`**, não um objeto. — integer
- `404` Grade não encontrada — inclusive em erro de integridade referencial (FK), não só "não existe"
