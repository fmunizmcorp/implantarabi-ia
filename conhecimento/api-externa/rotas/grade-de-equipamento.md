# Rotas — Grade de Equipamento (5 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 ferramentas/rabi_api/atualizar_spec.py` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `GET /grades-equipamento`
- `POST /grades-equipamento`
- `GET /grades-equipamento/{id}`
- `PUT /grades-equipamento/{id}`
- `DELETE /grades-equipamento/{id}`

### `GET /grades-equipamento`

- **Permissão:** `gradeEquipamento:read` · **Manual:** [op-get-grades-equipamento](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-grades-equipamento)
- **Resumo:** Listar grade de equipamento
- **Descrição:** Paginado de verdade — use `page`/`pageSize` e os filtros abaixo para não trazer a grade inteira da clínica.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |
| `equipamentoId` | query | integer | não |  |
| `localId` | query | integer | não |  |
| `vigenteEm` | query | string (date) | não | Só grades vigentes nessa data (entre `vigenteDesde` e `vigenteAte`, ou sem `vigenteAte`). |

**Respostas:**
- `200` Lista paginada — campos: `dados`, `page`, `pageSize`, `total`, `totalPages`; item de `dados`: `id`, `localId`, `equipamentoId`, `convenioId`, `profissionalId`, `diaDaSemana`, `inicioAtendimento`, `fimAtendimento`, `gradeEmMinutos`, `vigenteDesde`, `vigenteAte`, `ativo`, `exibirNoAgendamento`, `repetir`, `createdAt`, `updatedAt`, `copiaId`, `equipamento`, `local`, `colaborador`

### `POST /grades-equipamento`

- **Permissão:** `gradeEquipamento:create` · **Manual:** [op-post-grades-equipamento](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-grades-equipamento)
- **Resumo:** Cadastrar horário(s) de grade
- **Descrição:** O corpo é a lista direto (sem envelope). Já checa conflito de horário. **Bug conhecido:** essa rota (e o PUT/DELETE de `/grades-equipamento/{id}`) chama `redis.deleteByPattern(...)` sem checar se `redis` existe — como a autenticação por chave de API nunca popula isso, a chamada quebra **depois** que a escrita no banco já foi commitada. Na prática, hoje, criar/atualizar/excluir grade de equipamento por API key grava certo mas devolve **500** em vez do sucesso esperado. Reportado ao time; use com cautela até ser corrigido.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `(corpo é uma lista)` | lista de objeto | **sim** | O corpo é a lista de horários direto (sem envelope) — cria vários de uma vez. |
| `[].localId` | integer | **sim** |  |
| `[].equipamentoId` | integer | **sim** |  |
| `[].repetir` | boolean | não | padrão `True` |
| `[].diaDaSemana` | string | **sim** |  |
| `[].inicioAtendimento` | string (date-time) | **sim** |  |
| `[].fimAtendimento` | string (date-time) | **sim** |  |
| `[].gradeEmMinutos` | integer | **sim** |  |
| `[].vigenteDesde` | string (date) | não | aceita null |

**Respostas:**
- `201` Sujeito ao bug de `redis` acima. Quando não bate no bug, o corpo de sucesso é o número cru `201`, não um objeto. — integer
- `422` Falha ao criar grade de equipamento (conflito de horário, entre outros)
- `500` Bug conhecido de `redis` undefined — ver descrição acima. A escrita pode ter sido efetivada mesmo com esse erro.

### `GET /grades-equipamento/{id}`

- **Permissão:** `gradeEquipamento:read` · **Manual:** [op-get-grades-equipamento-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-grades-equipamento-id)
- **Resumo:** Consultar horário de grade

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID da grade |

**Respostas:**
- `200` Horário de grade — campos: `id`, `localId`, `equipamentoId`, `diaDaSemana`, `inicioAtendimento`, `fimAtendimento`, `gradeEmMinutos`
- `404` Grade não encontrada

### `PUT /grades-equipamento/{id}`

- **Permissão:** `gradeEquipamento:update` · **Manual:** [op-put-grades-equipamento-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-grades-equipamento-id)
- **Resumo:** Atualizar horário de grade
- **Descrição:** Mesmo bug de `redis` undefined do POST — ver descrição de `POST /grades-equipamento`.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID da grade |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `localId` | integer | **sim** |  |
| `equipamentoId` | integer | **sim** |  |
| `repetir` | boolean | não | padrão `True` |
| `diaDaSemana` | string | **sim** |  |
| `inicioAtendimento` | string (date-time) | **sim** |  |
| `fimAtendimento` | string (date-time) | **sim** |  |
| `gradeEmMinutos` | integer | **sim** |  |
| `vigenteDesde` | string (date) | não | aceita null |

**Respostas:**
- `202` **Status real 202, não 200.** Sujeito ao bug de `redis` (500). Corpo de sucesso, quando não bate no bug: número cru `201`. — integer
- `404` Grade não encontrada
- `500` Bug conhecido de `redis` undefined — ver descrição de POST /grades-equipamento.

### `DELETE /grades-equipamento/{id}`

- **Permissão:** `gradeEquipamento:delete` · **Manual:** [op-delete-grades-equipamento-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-delete-grades-equipamento-id)
- **Resumo:** Excluir horário de grade
- **Descrição:** Inativação lógica (`ativo=false`). Mesmo bug de `redis` undefined do POST.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID da grade |

**Respostas:**
- `200` Sujeito ao bug de `redis` (500). Corpo de sucesso, quando não bate no bug: número cru `201`. — integer
- `404` Grade não encontrada
- `500` Bug conhecido de `redis` undefined — ver descrição de POST /grades-equipamento.
