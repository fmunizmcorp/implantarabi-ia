# Rotas — Empresas (5 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 ferramentas/rabi_api/atualizar_spec.py` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `GET /empresas`
- `POST /empresas`
- `GET /empresas/{id}`
- `PUT /empresas/{id}`
- `DELETE /empresas/{id}`

### `GET /empresas`

- **Permissão:** `empresa:read` · **Manual:** [op-get-empresas](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-empresas)
- **Resumo:** Listar empresas/unidades
- **Descrição:** Sem paginação — devolve todas as empresas cadastradas na clínica, ativas e inativas.

**Respostas:**
- `200` Lista de empresas — lista crua de `Empresa`: `id`, `razaoSocial`, `nomeFantasia`, `cnpj`, `ativo`, `cnes`, `telefone`, `telefone2`, `celular`, `celular2`, `email`, `email2`, `dataInicioVigencia`, `dataFimVigencia`, `dataRenovacao`, `createdAt`, `updatedAt`, `endereco`

### `POST /empresas`

- **Permissão:** `empresa:create` · **Manual:** [op-post-empresas](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-empresas)
- **Resumo:** Cadastrar empresa/unidade

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `razaoSocial` | string | **sim** |  |
| `nomeFantasia` | string | **sim** |  |
| `cnpj` | string | **sim** | Único no sistema. Aceita com ou sem máscara. |
| `ativo` | boolean | não |  |
| `cnes` | string | não |  |
| `tipoContratoId` | integer | não |  |
| `dataInicioVigencia` | string (date-time) | não |  |
| `dataFimVigencia` | string (date-time) | não |  |
| `dataRenovacao` | string (date-time) | não |  |
| `telefone` | string | não |  |
| `telefone2` | string | não |  |
| `celular` | string | não |  |
| `celular2` | string | não |  |
| `email` | string | não |  |
| `email2` | string | não |  |
| `endereco` | objeto | **sim** |  |
| `endereco.Cep` | string | não |  |
| `endereco.Endereco` | string | não |  |
| `endereco.Numero` | string | não |  |
| `endereco.Complemento` | string | não |  |
| `endereco.Bairro` | string | não |  |
| `endereco.Cidade` | string | não |  |
| `endereco.unidadeFederativaId` | integer ou string | não | Aceita o ID da unidade federativa ou a sigla (ex.: "DF"). |

**Respostas:**
- `201` Empresa criada — campos: `id`, `razaoSocial`, `nomeFantasia`, `cnpj`, `ativo`, `cnes`, `telefone`, `telefone2`, `celular`, `celular2`, `email`, `email2`, `dataInicioVigencia`, `dataFimVigencia`, `dataRenovacao`, `createdAt`, `updatedAt`, `endereco`
- `409` CNPJ já cadastrado (para outra empresa ativa ou desativada)

### `GET /empresas/{id}`

- **Permissão:** `empresa:read` · **Manual:** [op-get-empresas-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-empresas-id)
- **Resumo:** Consultar empresa/unidade

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID da empresa/unidade |

**Respostas:**
- `200` Empresa — campos: `id`, `razaoSocial`, `nomeFantasia`, `cnpj`, `ativo`, `cnes`, `telefone`, `telefone2`, `celular`, `celular2`, `email`, `email2`, `dataInicioVigencia`, `dataFimVigencia`, `dataRenovacao`, `createdAt`, `updatedAt`, `endereco`
- `404` Empresa não encontrada

### `PUT /empresas/{id}`

- **Permissão:** `empresa:update` · **Manual:** [op-put-empresas-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-empresas-id)
- **Resumo:** Atualizar empresa/unidade
- **Descrição:** Substitui o cadastro por completo (mesmo comportamento do `PUT /convenios/{id}`), não faz merge parcial — envie a empresa inteira.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID da empresa/unidade |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `razaoSocial` | string | **sim** |  |
| `nomeFantasia` | string | **sim** |  |
| `cnpj` | string | **sim** | Único no sistema. Aceita com ou sem máscara. |
| `ativo` | boolean | não |  |
| `cnes` | string | não |  |
| `tipoContratoId` | integer | não |  |
| `dataInicioVigencia` | string (date-time) | não |  |
| `dataFimVigencia` | string (date-time) | não |  |
| `dataRenovacao` | string (date-time) | não |  |
| `telefone` | string | não |  |
| `telefone2` | string | não |  |
| `celular` | string | não |  |
| `celular2` | string | não |  |
| `email` | string | não |  |
| `email2` | string | não |  |
| `endereco` | objeto | **sim** |  |
| `endereco.Cep` | string | não |  |
| `endereco.Endereco` | string | não |  |
| `endereco.Numero` | string | não |  |
| `endereco.Complemento` | string | não |  |
| `endereco.Bairro` | string | não |  |
| `endereco.Cidade` | string | não |  |
| `endereco.unidadeFederativaId` | integer ou string | não | Aceita o ID da unidade federativa ou a sigla (ex.: "DF"). |

**Respostas:**
- `200` Empresa atualizada — campos: `id`, `razaoSocial`, `nomeFantasia`, `cnpj`, `ativo`, `cnes`, `telefone`, `telefone2`, `celular`, `celular2`, `email`, `email2`, `dataInicioVigencia`, `dataFimVigencia`, `dataRenovacao`, `createdAt`, `updatedAt`, `endereco`
- `404` Empresa não encontrada
- `409` CNPJ já cadastrado (para outra empresa ativa ou desativada)

### `DELETE /empresas/{id}`

- **Permissão:** `empresa:delete` · **Manual:** [op-delete-empresas-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-delete-empresas-id)
- **Resumo:** Desativar empresa/unidade
- **Descrição:** É uma **desativação** (`ativo = false`), não uma exclusão física. Recusa (`400`) se a empresa tiver atendimentos, colaboradores, convênios, depósitos, locais ou movimentações financeiras ativas vinculadas.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID da empresa/unidade |

**Respostas:**
- `200` Empresa desativada — campos: `message`
- `400` Empresa possui relações ativas vinculadas
- `404` Empresa não encontrada
