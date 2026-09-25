# Rotas — Locais (5 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 ferramentas/rabi_api/atualizar_spec.py` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `GET /locais`
- `POST /locais`
- `GET /locais/{id}`
- `PUT /locais/{id}`
- `DELETE /locais/{id}`

### `GET /locais`

- **Permissão:** `local:read` · **Manual:** [op-get-locais](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-locais)
- **Resumo:** Listar locais
- **Descrição:** Sem paginação — devolve todos os locais cadastrados na clínica.

**Respostas:**
- `200` Lista de locais — lista crua de `Local`: `id`, `nome`, `empresaId`, `depositoPadraoSaidaId`, `ativo`, `createdAt`, `updatedAt`

### `POST /locais`

- **Permissão:** `local:create` · **Manual:** [op-post-locais](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-locais)
- **Resumo:** Cadastrar local

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `nome` | string | **sim** |  |
| `empresaId` | integer | **sim** | ID da empresa dona do local. |
| `depositoPadraoSaidaId` | integer | **sim** | ID do depósito usado como padrão de saída de estoque nesse local. Precisa estar ativo. |

**Respostas:**
- `201` Local criado — campos: `id`, `nome`, `empresaId`, `depositoPadraoSaidaId`, `ativo`, `createdAt`, `updatedAt`
- `409` Já existe um local com esse nome nessa empresa
- `422` O depósito padrão de saída selecionado está inativo ou não existe

### `GET /locais/{id}`

- **Permissão:** `local:read` · **Manual:** [op-get-locais-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-locais-id)
- **Resumo:** Consultar local

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do local |

**Respostas:**
- `200` Local — campos: `id`, `nome`, `empresaId`, `depositoPadraoSaidaId`, `ativo`, `createdAt`, `updatedAt`
- `404` Local não encontrado

### `PUT /locais/{id}`

- **Permissão:** `local:update` · **Manual:** [op-put-locais-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-locais-id)
- **Resumo:** Atualizar local

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do local |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `nome` | string | **sim** |  |
| `empresaId` | integer | **sim** | ID da empresa dona do local. |
| `depositoPadraoSaidaId` | integer | **sim** | ID do depósito usado como padrão de saída de estoque nesse local. Precisa estar ativo. |

**Respostas:**
- `200` Local atualizado — campos: `message`
- `404` Local não encontrado
- `422` O depósito padrão de saída selecionado está inativo ou não existe

### `DELETE /locais/{id}`

- **Permissão:** `local:delete` · **Manual:** [op-delete-locais-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-delete-locais-id)
- **Resumo:** Desativar local
- **Descrição:** É uma **desativação** (`ativo = false`), não uma exclusão física. Recusa (`409`) se houver agendamentos, orçamentos, grades de colaborador/equipamento ou vínculos de serviço no local.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do local |

**Respostas:**
- `200` Local desativado — campos: `message`
- `404` Local não encontrado
- `409` Existem registros vinculados a este local
