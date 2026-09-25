# Rotas — Operadoras (6 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 ferramentas/rabi_api/atualizar_spec.py` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `GET /operadoras`
- `POST /operadoras`
- `POST /operadoras/bulk`
- `GET /operadoras/{id}`
- `PUT /operadoras/{id}`
- `DELETE /operadoras/{id}`

### `GET /operadoras`

- **Permissão:** `operadora:read` · **Manual:** [op-get-operadoras](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-operadoras)
- **Resumo:** Listar operadoras

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |
| `ativo` | query | boolean | não | Sem informar, lista ativas e inativas. |

**Respostas:**
- `200` Lista paginada — campos: `page`, `pageSize`, `total`, `totalPages`, `dados`; item de `dados`: `id`, `nome`, `descricao`, `registroANS`, `cnpj`, `razaoSocial`, `codigoCNES`, `codigoOperadora`, `im`, `identificacaoPrestadorXML`, `ativo`, `createdAt`, `updatedAt`, `endereco`, `contato`, `plano`

### `POST /operadoras`

- **Permissão:** `operadora:create` · **Manual:** [op-post-operadoras](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-operadoras)
- **Resumo:** Cadastrar operadora

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `nome` | string | **sim** |  |
| `descricao` | string | **sim** |  |
| `registroANS` | string | **sim** |  |
| `cnpj` | string | **sim** |  |
| `razaoSocial` | string | não | aceita null |
| `codigoCNES` | string | **sim** |  |
| `codigoOperadora` | string | não | aceita null |
| `im` | string | não | aceita null |
| `identificacaoPrestadorXML` | string | não | valores: `CNPJ`, `CODIGO_NA_OPERADORA`; padrão `CNPJ`; Como identificar o prestador no XML TISS — o XSD só aceita um dos dois. |
| `endereco` | objeto | **sim** |  |
| `endereco.cep` | string | **sim** |  |
| `endereco.endereco` | string | **sim** |  |
| `endereco.numero` | string | **sim** |  |
| `endereco.complemento` | string | não | aceita null |
| `endereco.bairro` | string | **sim** |  |
| `endereco.cidade` | string | **sim** |  |
| `endereco.unidadeFederativa` | string | **sim** | Nome por extenso da UF (não a sigla), precisa bater com um cadastro existente |
| `contato` | lista de objeto | não |  |
| `contato[].pessoaDeContato` | string | não | aceita null |
| `contato[].email` | string | não |  |
| `contato[].telefone` | string | não |  |
| `contato[].celular` | string | não |  |
| `plano` | lista de objeto | não |  |
| `plano[].nome` | string | não |  |

**Respostas:**
- `201` Operadora criada — campos: `id`, `nome`, `descricao`, `registroANS`, `cnpj`, `razaoSocial`, `codigoCNES`, `codigoOperadora`, `im`, `identificacaoPrestadorXML`, `ativo`, `createdAt`, `updatedAt`, `endereco`, `contato`, `plano`
- `404` Unidade Federativa não encontrada

### `POST /operadoras/bulk`

- **Permissão:** `operadora:create` · **Manual:** [op-post-operadoras-bulk](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-operadoras-bulk)
- **Resumo:** Cadastrar várias operadoras de uma vez
- **Descrição:** Até 50 itens por requisição (chave `operadoras`). `207` = falha parcial, ver `resultados`; reenvie só os itens com erro.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `operadoras` | lista de objeto | **sim** | máx. itens 50 |
| `operadoras[].nome` | string | **sim** |  |
| `operadoras[].descricao` | string | **sim** |  |
| `operadoras[].registroANS` | string | **sim** |  |
| `operadoras[].cnpj` | string | **sim** |  |
| `operadoras[].razaoSocial` | string | não | aceita null |
| `operadoras[].codigoCNES` | string | **sim** |  |
| `operadoras[].codigoOperadora` | string | não | aceita null |
| `operadoras[].im` | string | não | aceita null |
| `operadoras[].identificacaoPrestadorXML` | string | não | valores: `CNPJ`, `CODIGO_NA_OPERADORA`; padrão `CNPJ`; Como identificar o prestador no XML TISS — o XSD só aceita um dos dois. |
| `operadoras[].endereco` | objeto | **sim** |  |
| `operadoras[].endereco.cep` | string | **sim** |  |
| `operadoras[].endereco.endereco` | string | **sim** |  |
| `operadoras[].endereco.numero` | string | **sim** |  |
| `operadoras[].endereco.complemento` | string | não | aceita null |
| `operadoras[].endereco.bairro` | string | **sim** |  |
| `operadoras[].endereco.cidade` | string | **sim** |  |
| `operadoras[].endereco.unidadeFederativa` | string | **sim** | Nome por extenso da UF (não a sigla), precisa bater com um cadastro existente |
| `operadoras[].contato` | lista de objeto | não |  |
| `operadoras[].contato[].pessoaDeContato` | string | não | aceita null |
| `operadoras[].contato[].email` | string | não |  |
| `operadoras[].contato[].telefone` | string | não |  |
| `operadoras[].contato[].celular` | string | não |  |
| `operadoras[].plano` | lista de objeto | não |  |
| `operadoras[].plano[].nome` | string | não |  |

**Respostas:**
- `201` Todas criadas — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `207` Falha parcial — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `400` Lote vazio ou acima de 50 itens
- `429` Já existe um lote em andamento para esta clínica e recurso

### `GET /operadoras/{id}`

- **Permissão:** `operadora:read` · **Manual:** [op-get-operadoras-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-operadoras-id)
- **Resumo:** Consultar operadora

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID da operadora |

**Respostas:**
- `200` Operadora — campos: `id`, `nome`, `descricao`, `registroANS`, `cnpj`, `razaoSocial`, `codigoCNES`, `codigoOperadora`, `im`, `identificacaoPrestadorXML`, `ativo`, `createdAt`, `updatedAt`, `endereco`, `contato`, `plano`
- `400` `id` inválido
- `404` Operadora não encontrada

### `PUT /operadoras/{id}`

- **Permissão:** `operadora:update` · **Manual:** [op-put-operadoras-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-operadoras-id)
- **Resumo:** Atualizar operadora
- **Descrição:** Envie as listas completas de `plano` e `contato` — o servidor compara com o estado atual e cria, atualiza ou remove pra bater com o que foi enviado.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID da operadora |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `nome` | string | **sim** |  |
| `descricao` | string | **sim** |  |
| `registroANS` | string | **sim** |  |
| `cnpj` | string | **sim** |  |
| `razaoSocial` | string | não | aceita null |
| `codigoCNES` | string | **sim** |  |
| `codigoOperadora` | string | não | aceita null |
| `im` | string | não | aceita null |
| `identificacaoPrestadorXML` | string | não | valores: `CNPJ`, `CODIGO_NA_OPERADORA`; padrão `CNPJ`; Como identificar o prestador no XML TISS — o XSD só aceita um dos dois. |
| `endereco` | objeto | **sim** |  |
| `endereco.cep` | string | **sim** |  |
| `endereco.endereco` | string | **sim** |  |
| `endereco.numero` | string | **sim** |  |
| `endereco.complemento` | string | não | aceita null |
| `endereco.bairro` | string | **sim** |  |
| `endereco.cidade` | string | **sim** |  |
| `endereco.unidadeFederativa` | string | **sim** | Nome por extenso da UF (não a sigla), precisa bater com um cadastro existente |
| `contato` | lista de objeto | não |  |
| `contato[].pessoaDeContato` | string | não | aceita null |
| `contato[].email` | string | não |  |
| `contato[].telefone` | string | não |  |
| `contato[].celular` | string | não |  |
| `plano` | lista de objeto | não |  |
| `plano[].nome` | string | não |  |

**Respostas:**
- `202` Operadora atualizada — campos: `id`, `nome`, `descricao`, `registroANS`, `cnpj`, `razaoSocial`, `codigoCNES`, `codigoOperadora`, `im`, `identificacaoPrestadorXML`, `ativo`, `createdAt`, `updatedAt`, `endereco`, `contato`, `plano`
- `404` Operadora ou Unidade Federativa não encontrada

### `DELETE /operadoras/{id}`

- **Permissão:** `operadora:delete` · **Manual:** [op-delete-operadoras-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-delete-operadoras-id)
- **Resumo:** Desativar operadora
- **Descrição:** É uma **desativação** (`ativo = false`), não uma exclusão física. Recusa (`400`) se houver convênio ativo vinculado a esta operadora.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID da operadora |

**Respostas:**
- `200` Diferente do padrão de outros cadastros (sem `status`/`aviso`). — campos: `message`
- `400` Existem convênios ativos vinculados a esta operadora — a mensagem inclui o nome da operadora e a contagem
