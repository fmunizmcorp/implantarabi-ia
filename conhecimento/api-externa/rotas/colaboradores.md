# Rotas — Colaboradores (7 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 -m ferramentas.rabi_api.atualizar_spec` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `GET /colaboradores`
- `POST /colaboradores`
- `POST /colaboradores/bulk`
- `GET /colaboradores/{id}`
- `PUT /colaboradores/{id}`
- `DELETE /colaboradores/{id}`
- `POST /colaboradores/{id}/usuario`

### `GET /colaboradores`

- **Permissão:** `colaborador:read` · **Manual:** [op-get-colaboradores](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-colaboradores)
- **Resumo:** Listar colaboradores

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |
| `ativo` | query | boolean | não | Sem informar, lista ativos e inativos. |

**Respostas:**
- `200` Lista paginada — campos: `page`, `pageSize`, `total`, `totalPages`, `dados`; item de `dados`: `id`, `nome`, `cpf`, `dataDeNascimento`, `sexoId`, `ativo`, `isParceiro`, `telefone`, `telefone2`, `celular`, `celular2`, `email`, `email2`, `corNaAgenda`, `createdAt`, `updatedAt`, `endereco`, `colaboradorEspecialidades`, `colaboradorEmpresas`

### `POST /colaboradores`

- **Permissão:** `colaborador:create` · **Manual:** [op-post-colaboradores](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-colaboradores)
- **Resumo:** Cadastrar colaborador
- **Descrição:** Não cria acesso de login ao sistema — só o cadastro.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `nome` | string | **sim** |  |
| `cpf` | string | **sim** |  |
| `dataDeNascimento` | string (date) | **sim** |  |
| `sexoId` | integer | **sim** |  |
| `telefone` | string | **sim** |  |
| `telefone2` | string | não | aceita null |
| `celular` | string | **sim** |  |
| `celular2` | string | não | aceita null |
| `email` | string | **sim** |  |
| `email2` | string | não | aceita null |
| `mensagem` | string | não | aceita null |
| `corNaAgenda` | string | não | aceita null |
| `empresas` | lista de integer | não | IDs das empresas/unidades onde o colaborador atua |
| `endereco` | objeto | **sim** |  |
| `endereco.cep` | string | **sim** |  |
| `endereco.endereco` | string | **sim** |  |
| `endereco.numero` | string | **sim** |  |
| `endereco.complemento` | string | não | aceita null |
| `endereco.bairro` | string | **sim** |  |
| `endereco.cidade` | string | **sim** |  |
| `endereco.unidadeFederativa` | string | **sim** | Nome por extenso da UF, não a sigla |
| `conselho` | lista de objeto | não |  |
| `conselho[].uf` | integer | não | ID da Unidade Federativa |
| `conselho[].descricao` | string | não |  |
| `conselho[].registroConselho` | string | não |  |
| `especialidades` | lista de objeto | não |  |
| `especialidades[].rqe` | string | não | aceita null |
| `especialidades[].uf` | integer | não | ID da Unidade Federativa |
| `especialidades[].numeroConselho` | string | não |  |
| `especialidades[].especialidadeId` | string | não |  |
| `especialidades[].idadeMinimaAtendimento` | integer | não | aceita null |
| `especialidades[].idadeMaximaAtendimento` | integer | não | aceita null |
| `especialidades[].anamnesePadrao` | string | não | aceita null |
| `especialidades[].evolucaoPadrao` | string | não | aceita null |
| `especialidades[].observacoes` | string | não | aceita null |
| `especialidades[].conselhoProfissionalId` | integer | não |  |
| `vinculoRepasse` | objeto | não | Regras de comissão/repasse do colaborador. |
| `vinculoRepasse.tipoVinculo` | string | não |  |
| `vinculoRepasse.produtos` | lista de objeto | não |  |
| `vinculoRepasse.produtos[].valorPercentual` | number | não |  |
| `vinculoRepasse.produtos[].valorMonetario` | number | não |  |
| `vinculoRepasse.produtos[].tipoCalculo` | string | não |  |
| `vinculoRepasse.produtos[].tipoProduto` | integer | não |  |
| `vinculoRepasse.produtos[].material` | integer | não |  |
| `vinculoRepasse.produtos[].produto` | integer | não |  |
| `vinculoRepasse.servicos` | lista de objeto | não |  |
| `vinculoRepasse.servicos[].valorPercentual` | number | não |  |
| `vinculoRepasse.servicos[].valorMonetario` | number | não |  |
| `vinculoRepasse.servicos[].tipoCalculo` | string | não |  |
| `vinculoRepasse.servicos[].servico` | integer | não |  |
| `vinculoRepasse.taxas` | lista de objeto | não |  |
| `vinculoRepasse.taxas[].valorPercentual` | number | não |  |
| `vinculoRepasse.taxas[].valorMonetario` | number | não |  |
| `vinculoRepasse.taxas[].tipoCalculo` | string | não |  |
| `vinculoRepasse.taxas[].taxa` | integer | não |  |

**Respostas:**
- `201` Colaborador criado — campos: `id`, `nome`, `cpf`, `dataDeNascimento`, `sexoId`, `ativo`, `isParceiro`, `telefone`, `telefone2`, `celular`, `celular2`, `email`, `email2`, `corNaAgenda`, `createdAt`, `updatedAt`, `endereco`, `colaboradorEspecialidades`, `colaboradorEmpresas`

### `POST /colaboradores/bulk`

- **Permissão:** `colaborador:create` · **Manual:** [op-post-colaboradores-bulk](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-colaboradores-bulk)
- **Resumo:** Cadastrar vários colaboradores de uma vez
- **Descrição:** Até 50 itens por requisição (chave `colaboradores`). `207` = falha parcial, ver `resultados`; reenvie só os itens com erro. Não cria acesso de login.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `colaboradores` | lista de objeto | **sim** | máx. itens 50 |
| `colaboradores[].nome` | string | **sim** |  |
| `colaboradores[].cpf` | string | **sim** |  |
| `colaboradores[].dataDeNascimento` | string (date) | **sim** |  |
| `colaboradores[].sexoId` | integer | **sim** |  |
| `colaboradores[].telefone` | string | **sim** |  |
| `colaboradores[].telefone2` | string | não | aceita null |
| `colaboradores[].celular` | string | **sim** |  |
| `colaboradores[].celular2` | string | não | aceita null |
| `colaboradores[].email` | string | **sim** |  |
| `colaboradores[].email2` | string | não | aceita null |
| `colaboradores[].mensagem` | string | não | aceita null |
| `colaboradores[].corNaAgenda` | string | não | aceita null |
| `colaboradores[].empresas` | lista de integer | não | IDs das empresas/unidades onde o colaborador atua |
| `colaboradores[].endereco` | objeto | **sim** |  |
| `colaboradores[].endereco.cep` | string | **sim** |  |
| `colaboradores[].endereco.endereco` | string | **sim** |  |
| `colaboradores[].endereco.numero` | string | **sim** |  |
| `colaboradores[].endereco.complemento` | string | não | aceita null |
| `colaboradores[].endereco.bairro` | string | **sim** |  |
| `colaboradores[].endereco.cidade` | string | **sim** |  |
| `colaboradores[].endereco.unidadeFederativa` | string | **sim** | Nome por extenso da UF, não a sigla |
| `colaboradores[].conselho` | lista de objeto | não |  |
| `colaboradores[].conselho[].uf` | integer | não | ID da Unidade Federativa |
| `colaboradores[].conselho[].descricao` | string | não |  |
| `colaboradores[].conselho[].registroConselho` | string | não |  |
| `colaboradores[].especialidades` | lista de objeto | não |  |
| `colaboradores[].especialidades[].rqe` | string | não | aceita null |
| `colaboradores[].especialidades[].uf` | integer | não | ID da Unidade Federativa |
| `colaboradores[].especialidades[].numeroConselho` | string | não |  |
| `colaboradores[].especialidades[].especialidadeId` | string | não |  |
| `colaboradores[].especialidades[].idadeMinimaAtendimento` | integer | não | aceita null |
| `colaboradores[].especialidades[].idadeMaximaAtendimento` | integer | não | aceita null |
| `colaboradores[].especialidades[].anamnesePadrao` | string | não | aceita null |
| `colaboradores[].especialidades[].evolucaoPadrao` | string | não | aceita null |
| `colaboradores[].especialidades[].observacoes` | string | não | aceita null |
| `colaboradores[].especialidades[].conselhoProfissionalId` | integer | não |  |
| `colaboradores[].vinculoRepasse` | objeto | não | Regras de comissão/repasse do colaborador. |
| `colaboradores[].vinculoRepasse.tipoVinculo` | string | não |  |
| `colaboradores[].vinculoRepasse.produtos` | lista de objeto | não |  |
| `colaboradores[].vinculoRepasse.produtos[].valorPercentual` | number | não |  |
| `colaboradores[].vinculoRepasse.produtos[].valorMonetario` | number | não |  |
| `colaboradores[].vinculoRepasse.produtos[].tipoCalculo` | string | não |  |
| `colaboradores[].vinculoRepasse.produtos[].tipoProduto` | integer | não |  |
| `colaboradores[].vinculoRepasse.produtos[].material` | integer | não |  |
| `colaboradores[].vinculoRepasse.produtos[].produto` | integer | não |  |
| `colaboradores[].vinculoRepasse.servicos` | lista de objeto | não |  |
| `colaboradores[].vinculoRepasse.servicos[].valorPercentual` | number | não |  |
| `colaboradores[].vinculoRepasse.servicos[].valorMonetario` | number | não |  |
| `colaboradores[].vinculoRepasse.servicos[].tipoCalculo` | string | não |  |
| `colaboradores[].vinculoRepasse.servicos[].servico` | integer | não |  |
| `colaboradores[].vinculoRepasse.taxas` | lista de objeto | não |  |
| `colaboradores[].vinculoRepasse.taxas[].valorPercentual` | number | não |  |
| `colaboradores[].vinculoRepasse.taxas[].valorMonetario` | number | não |  |
| `colaboradores[].vinculoRepasse.taxas[].tipoCalculo` | string | não |  |
| `colaboradores[].vinculoRepasse.taxas[].taxa` | integer | não |  |

**Respostas:**
- `201` Todos criados — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `207` Falha parcial — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `400` Lote vazio ou acima de 50 itens
- `429` Já existe um lote em andamento para esta clínica e recurso

### `GET /colaboradores/{id}`

- **Permissão:** `colaborador:read` · **Manual:** [op-get-colaboradores-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-colaboradores-id)
- **Resumo:** Consultar colaborador

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do colaborador |

**Respostas:**
- `200` Colaborador — campos: `id`, `nome`, `cpf`, `dataDeNascimento`, `sexoId`, `ativo`, `isParceiro`, `telefone`, `telefone2`, `celular`, `celular2`, `email`, `email2`, `corNaAgenda`, `createdAt`, `updatedAt`, `endereco`, `colaboradorEspecialidades`, `colaboradorEmpresas`
- `400` `id` inválido
- `404` Colaborador não encontrado

### `PUT /colaboradores/{id}`

- **Permissão:** `colaborador:update` · **Manual:** [op-put-colaboradores-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-colaboradores-id)
- **Resumo:** Atualizar colaborador
- **Descrição:** **Não devolve o colaborador atualizado — o corpo de sucesso é o número cru `201`.** É a exceção real dentro do padrão "PUT devolve o recurso" usado no resto da API.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do colaborador |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `nome` | string | **sim** |  |
| `cpf` | string | **sim** |  |
| `dataDeNascimento` | string (date) | **sim** |  |
| `sexoId` | integer | **sim** |  |
| `telefone` | string | **sim** |  |
| `telefone2` | string | não | aceita null |
| `celular` | string | **sim** |  |
| `celular2` | string | não | aceita null |
| `email` | string | **sim** |  |
| `email2` | string | não | aceita null |
| `mensagem` | string | não | aceita null |
| `corNaAgenda` | string | não | aceita null |
| `empresas` | lista de integer | não | IDs das empresas/unidades onde o colaborador atua |
| `endereco` | objeto | **sim** |  |
| `endereco.cep` | string | **sim** |  |
| `endereco.endereco` | string | **sim** |  |
| `endereco.numero` | string | **sim** |  |
| `endereco.complemento` | string | não | aceita null |
| `endereco.bairro` | string | **sim** |  |
| `endereco.cidade` | string | **sim** |  |
| `endereco.unidadeFederativa` | string | **sim** | Nome por extenso da UF, não a sigla |
| `conselho` | lista de objeto | não |  |
| `conselho[].uf` | integer | não | ID da Unidade Federativa |
| `conselho[].descricao` | string | não |  |
| `conselho[].registroConselho` | string | não |  |
| `especialidades` | lista de objeto | não |  |
| `especialidades[].rqe` | string | não | aceita null |
| `especialidades[].uf` | integer | não | ID da Unidade Federativa |
| `especialidades[].numeroConselho` | string | não |  |
| `especialidades[].especialidadeId` | string | não |  |
| `especialidades[].idadeMinimaAtendimento` | integer | não | aceita null |
| `especialidades[].idadeMaximaAtendimento` | integer | não | aceita null |
| `especialidades[].anamnesePadrao` | string | não | aceita null |
| `especialidades[].evolucaoPadrao` | string | não | aceita null |
| `especialidades[].observacoes` | string | não | aceita null |
| `especialidades[].conselhoProfissionalId` | integer | não |  |
| `vinculoRepasse` | objeto | não | Regras de comissão/repasse do colaborador. |
| `vinculoRepasse.tipoVinculo` | string | não |  |
| `vinculoRepasse.produtos` | lista de objeto | não |  |
| `vinculoRepasse.produtos[].valorPercentual` | number | não |  |
| `vinculoRepasse.produtos[].valorMonetario` | number | não |  |
| `vinculoRepasse.produtos[].tipoCalculo` | string | não |  |
| `vinculoRepasse.produtos[].tipoProduto` | integer | não |  |
| `vinculoRepasse.produtos[].material` | integer | não |  |
| `vinculoRepasse.produtos[].produto` | integer | não |  |
| `vinculoRepasse.servicos` | lista de objeto | não |  |
| `vinculoRepasse.servicos[].valorPercentual` | number | não |  |
| `vinculoRepasse.servicos[].valorMonetario` | number | não |  |
| `vinculoRepasse.servicos[].tipoCalculo` | string | não |  |
| `vinculoRepasse.servicos[].servico` | integer | não |  |
| `vinculoRepasse.taxas` | lista de objeto | não |  |
| `vinculoRepasse.taxas[].valorPercentual` | number | não |  |
| `vinculoRepasse.taxas[].valorMonetario` | number | não |  |
| `vinculoRepasse.taxas[].tipoCalculo` | string | não |  |
| `vinculoRepasse.taxas[].taxa` | integer | não |  |

**Respostas:**
- `202` Corpo de sucesso é o número cru `201`, não o objeto Colaborador. — integer

### `DELETE /colaboradores/{id}`

- **Permissão:** `colaborador:delete` · **Manual:** [op-delete-colaboradores-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-delete-colaboradores-id)
- **Resumo:** Desativar colaborador
- **Descrição:** É uma **desativação** (`ativo = false`), não uma exclusão física. Desativa também as grades, especialidades e vínculos de empresa do colaborador. Avisa (mas não bloqueia) se houver agendamento futuro.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do colaborador |

**Respostas:**
- `200` Segue o padrão canônico (igual convênio). — campos: `status`, `message`, `aviso`
- `404` Colaborador não encontrado

### `POST /colaboradores/{id}/usuario`

- **Permissão:** `colaborador:update` · **Manual:** [op-post-colaboradores-id-usuario](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-colaboradores-id-usuario)
- **Resumo:** Criar login (Keycloak) para o colaborador
- **Descrição:** Cria um acesso de login de verdade ao sistema para este colaborador (email + senha) — diferente do `POST /colaboradores`/`PUT /colaboradores/{id}`, que só cadastram dados e nunca criam acesso. Falha se o colaborador já tiver login.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do colaborador |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `email` | string (email) | **sim** |  |
| `senha` | string | **sim** | mín. caracteres 8 |
| `primeiroNome` | string | não | aceita null; Sem informar, usa a primeira palavra do nome cadastrado. |
| `sobrenome` | string | não | aceita null; Sem informar, usa o restante do nome cadastrado. |

**Respostas:**
- `201` Login criado — campos: `colaboradorId`, `email`, `criado`
- `400` Email ausente, ou senha com menos de 8 caracteres
- `404` Colaborador não encontrado
- `409` Este colaborador já tem login
