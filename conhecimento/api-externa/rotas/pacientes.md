# Rotas — Pacientes (11 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 ferramentas/rabi_api/atualizar_spec.py` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `GET /pacientes`
- `POST /pacientes`
- `POST /pacientes/bulk`
- `GET /pacientes/{id}`
- `PUT /pacientes/{id}`
- `DELETE /pacientes/{id}`
- `GET /pacientes/{id}/convenios`
- `POST /pacientes/{id}/convenios`
- `PUT /pacientes/{id}/convenios/{vinculoId}`
- `GET /pacientes/{id}/anexos`
- `POST /pacientes/{id}/anexos`

### `GET /pacientes`

- **Permissão:** `paciente:read` · **Manual:** [op-get-pacientes](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-pacientes)
- **Resumo:** Listar pacientes

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |
| `ativo` | query | boolean | não | Sem informar, lista ativos e inativos. |

**Respostas:**
- `200` Lista paginada — campos: `page`, `pageSize`, `total`, `totalPages`, `dados`; item de `dados`: `id`, `nome`, `cpf`, `rg`, `numeroDocumento`, `orgaoEmissor`, `ufRg`, `dataDeNascimento`, `estrangeiro`, `estadoCivil`, `profissao`, `atendimentoRN`, `sexoId`, `ativo`, `createdAt`, `updatedAt`, `contatos`, `endereco`

### `POST /pacientes`

- **Permissão:** `paciente:create` · **Manual:** [op-post-pacientes](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-pacientes)
- **Resumo:** Cadastrar paciente

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `nome` | string | **sim** |  |
| `rg` | string | não | aceita null |
| `cpf` | string | não | Obrigatório, salvo para recém-nascido sem CPF (usar `cpfMae`) |
| `orgaoEmissor` | string | não | aceita null |
| `ufRg` | string | não | aceita null |
| `dataDeNascimento` | string (date) | não |  |
| `sexoId` | integer | **sim** |  |
| `estrangeiro` | boolean | não | padrão `False` |
| `estadoCivil` | string | não | aceita null |
| `profissao` | string | não | aceita null |
| `atendimentoRn` | boolean | não | padrão `False`; Atendimento de recém-nascido — dispensa CPF próprio se `cpfMae` for informado |
| `cpfMae` | string | não | aceita null |
| `contato` | lista de objeto | **sim** |  |
| `contato[].pessoaDeContato` | string | não | aceita null |
| `contato[].email` | string | **sim** |  |
| `contato[].celular` | string | **sim** |  |
| `contato[].telefone` | string | não | aceita null |
| `endereco` | objeto | **sim** |  |
| `endereco.cep` | string | não |  |
| `endereco.endereco` | string | não |  |
| `endereco.numero` | string | não |  |
| `endereco.complemento` | string | não | aceita null |
| `endereco.bairro` | string | não |  |
| `endereco.cidade` | string | não |  |
| `endereco.unidadeFederativaId` | integer | não | aceita null |
| `convenioPlano` | lista de objeto | não |  |
| `convenioPlano[].convenioId` | integer | não |  |
| `convenioPlano[].planoId` | integer | não | aceita null |
| `convenioPlano[].numeroDaCarterinha` | string | não | aceita null |
| `convenioPlano[].validade` | string (date) | não | aceita null |
| `convenioPlano[].ativo` | boolean | não | padrão `True` |

**Respostas:**
- `201` Paciente criado — campos: `id`, `nome`, `cpf`, `rg`, `numeroDocumento`, `orgaoEmissor`, `ufRg`, `dataDeNascimento`, `estrangeiro`, `estadoCivil`, `profissao`, `atendimentoRN`, `sexoId`, `ativo`, `createdAt`, `updatedAt`, `contatos`, `endereco`
- `400` CPF inválido, contato obrigatório ausente ou dado inconsistente
- `409` CPF já cadastrado nesta clínica

### `POST /pacientes/bulk`

- **Permissão:** `paciente:create` · **Manual:** [op-post-pacientes-bulk](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-pacientes-bulk)
- **Resumo:** Cadastrar vários pacientes de uma vez
- **Descrição:** Até 50 itens por requisição (chave `pacientes`). `207` = falha parcial, ver `resultados`; reenvie só os itens com erro.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `pacientes` | lista de objeto | **sim** | máx. itens 50 |
| `pacientes[].nome` | string | **sim** |  |
| `pacientes[].rg` | string | não | aceita null |
| `pacientes[].cpf` | string | não | Obrigatório, salvo para recém-nascido sem CPF (usar `cpfMae`) |
| `pacientes[].orgaoEmissor` | string | não | aceita null |
| `pacientes[].ufRg` | string | não | aceita null |
| `pacientes[].dataDeNascimento` | string (date) | não |  |
| `pacientes[].sexoId` | integer | **sim** |  |
| `pacientes[].estrangeiro` | boolean | não | padrão `False` |
| `pacientes[].estadoCivil` | string | não | aceita null |
| `pacientes[].profissao` | string | não | aceita null |
| `pacientes[].atendimentoRn` | boolean | não | padrão `False`; Atendimento de recém-nascido — dispensa CPF próprio se `cpfMae` for informado |
| `pacientes[].cpfMae` | string | não | aceita null |
| `pacientes[].contato` | lista de objeto | **sim** |  |
| `pacientes[].contato[].pessoaDeContato` | string | não | aceita null |
| `pacientes[].contato[].email` | string | **sim** |  |
| `pacientes[].contato[].celular` | string | **sim** |  |
| `pacientes[].contato[].telefone` | string | não | aceita null |
| `pacientes[].endereco` | objeto | **sim** |  |
| `pacientes[].endereco.cep` | string | não |  |
| `pacientes[].endereco.endereco` | string | não |  |
| `pacientes[].endereco.numero` | string | não |  |
| `pacientes[].endereco.complemento` | string | não | aceita null |
| `pacientes[].endereco.bairro` | string | não |  |
| `pacientes[].endereco.cidade` | string | não |  |
| `pacientes[].endereco.unidadeFederativaId` | integer | não | aceita null |
| `pacientes[].convenioPlano` | lista de objeto | não |  |
| `pacientes[].convenioPlano[].convenioId` | integer | não |  |
| `pacientes[].convenioPlano[].planoId` | integer | não | aceita null |
| `pacientes[].convenioPlano[].numeroDaCarterinha` | string | não | aceita null |
| `pacientes[].convenioPlano[].validade` | string (date) | não | aceita null |
| `pacientes[].convenioPlano[].ativo` | boolean | não | padrão `True` |

**Respostas:**
- `201` Todos criados — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `207` Falha parcial — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `400` Lote vazio ou acima de 50 itens
- `429` Já existe um lote em andamento para esta clínica e recurso

### `GET /pacientes/{id}`

- **Permissão:** `paciente:read` · **Manual:** [op-get-pacientes-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-pacientes-id)
- **Resumo:** Consultar paciente

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do paciente |

**Respostas:**
- `200` Paciente — campos: `id`, `nome`, `cpf`, `rg`, `numeroDocumento`, `orgaoEmissor`, `ufRg`, `dataDeNascimento`, `estrangeiro`, `estadoCivil`, `profissao`, `atendimentoRN`, `sexoId`, `ativo`, `createdAt`, `updatedAt`, `contatos`, `endereco`
- `400` `id` inválido
- `404` Paciente não encontrado

### `PUT /pacientes/{id}`

- **Permissão:** `paciente:update` · **Manual:** [op-put-pacientes-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-pacientes-id)
- **Resumo:** Atualizar paciente
- **Descrição:** Sobrescreve os dados cadastrais — envie o objeto completo, campos omitidos não são preservados.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do paciente |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `nome` | string | **sim** |  |
| `rg` | string | não | aceita null |
| `cpf` | string | não | Obrigatório, salvo para recém-nascido sem CPF (usar `cpfMae`) |
| `orgaoEmissor` | string | não | aceita null |
| `ufRg` | string | não | aceita null |
| `dataDeNascimento` | string (date) | não |  |
| `sexoId` | integer | **sim** |  |
| `estrangeiro` | boolean | não | padrão `False` |
| `estadoCivil` | string | não | aceita null |
| `profissao` | string | não | aceita null |
| `atendimentoRn` | boolean | não | padrão `False`; Atendimento de recém-nascido — dispensa CPF próprio se `cpfMae` for informado |
| `cpfMae` | string | não | aceita null |
| `contato` | lista de objeto | **sim** |  |
| `contato[].pessoaDeContato` | string | não | aceita null |
| `contato[].email` | string | **sim** |  |
| `contato[].celular` | string | **sim** |  |
| `contato[].telefone` | string | não | aceita null |
| `endereco` | objeto | **sim** |  |
| `endereco.cep` | string | não |  |
| `endereco.endereco` | string | não |  |
| `endereco.numero` | string | não |  |
| `endereco.complemento` | string | não | aceita null |
| `endereco.bairro` | string | não |  |
| `endereco.cidade` | string | não |  |
| `endereco.unidadeFederativaId` | integer | não | aceita null |
| `convenioPlano` | lista de objeto | não |  |
| `convenioPlano[].convenioId` | integer | não |  |
| `convenioPlano[].planoId` | integer | não | aceita null |
| `convenioPlano[].numeroDaCarterinha` | string | não | aceita null |
| `convenioPlano[].validade` | string (date) | não | aceita null |
| `convenioPlano[].ativo` | boolean | não | padrão `True` |

**Respostas:**
- `200` Paciente atualizado — campos: `id`, `nome`, `cpf`, `rg`, `numeroDocumento`, `orgaoEmissor`, `ufRg`, `dataDeNascimento`, `estrangeiro`, `estadoCivil`, `profissao`, `atendimentoRN`, `sexoId`, `ativo`, `createdAt`, `updatedAt`, `contatos`, `endereco`
- `400` CPF inválido ou dado inconsistente
- `404` Paciente não encontrado

### `DELETE /pacientes/{id}`

- **Permissão:** `paciente:delete` · **Manual:** [op-delete-pacientes-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-delete-pacientes-id)
- **Resumo:** Desativar paciente
- **Descrição:** É uma **desativação** (`ativo = false`), não uma exclusão física.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do paciente |

**Respostas:**
- `200` **Corpo de sucesso é o número cru `201`**, não um objeto — comportamento observado, não intenção de design. — integer

### `GET /pacientes/{id}/convenios`

- **Permissão:** `paciente:read` · **Manual:** [op-get-pacientes-id-convenios](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-pacientes-id-convenios)
- **Resumo:** Listar convênios/planos vinculados ao paciente

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do paciente |
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |

**Respostas:**
- `200` Lista paginada — campos: `page`, `pageSize`, `total`, `totalPages`, `dados`; item de `dados`: `id`, `pacienteId`, `convenioId`, `planoId`, `numeroDaCarterinha`, `validade`, `ativo`, `convenio`, `plano`
- `400` `id` inválido
- `404` Paciente não encontrado

### `POST /pacientes/{id}/convenios`

- **Permissão:** `paciente:update` · **Manual:** [op-post-pacientes-id-convenios](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-pacientes-id-convenios)
- **Resumo:** Vincular convênio(s)/plano(s) ao paciente
- **Descrição:** Sempre cria um novo vínculo — não atualiza um existente (use `PUT /pacientes/{id}/convenios/{vinculoId}` para isso).

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do paciente |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `convenioPlano` | lista de objeto | **sim** |  |
| `convenioPlano[].convenioId` | integer | **sim** |  |
| `convenioPlano[].planoId` | integer | não | aceita null |
| `convenioPlano[].numeroDaCarterinha` | string | não | aceita null |
| `convenioPlano[].validade` | string (date) | não | aceita null |
| `convenioPlano[].ativo` | boolean | não | padrão `True` |

**Respostas:**
- `201` **Corpo de sucesso é o número cru `201`**, não os vínculos criados — internamente o use case monta o registro completo (com convênio/plano/paciente incluídos) mas descarta esse resultado antes de retornar. Se precisar dos ids, consulte depois com `GET /pacientes/{id}/convenios`. — integer
- `400` Convênio/plano não encontrado ou número de carteirinha já em uso
- `404` Paciente não encontrado

### `PUT /pacientes/{id}/convenios/{vinculoId}`

- **Permissão:** `paciente:update` · **Manual:** [op-put-pacientes-id-convenios-vinculoid](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-pacientes-id-convenios-vinculoid)
- **Resumo:** Atualizar um vínculo de convênio do paciente
- **Descrição:** `vinculoId` é o `id` retornado por `GET /pacientes/{id}/convenios`, não o id do convênio.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do paciente |
| `vinculoId` | path | integer | **sim** | mín. 1; ID do vínculo paciente-convênio (não é o ID do convênio nem do paciente) |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `convenioId` | integer | **sim** |  |
| `planoId` | integer | não | aceita null |
| `numeroDaCarterinha` | string | não | aceita null |
| `validade` | string (date) | não | aceita null |

**Respostas:**
- `200` Vínculo atualizado — campos: `id`, `pacienteId`, `convenioId`, `planoId`, `numeroDaCarterinha`, `validade`, `ativo`, `convenio`, `plano`
- `400` Convênio/plano não encontrado ou número de carteirinha já em uso
- `404` Vínculo não encontrado para este paciente

### `GET /pacientes/{id}/anexos`

- **Permissão:** `paciente:read` · **Manual:** [op-get-pacientes-id-anexos](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-pacientes-id-anexos)
- **Resumo:** Listar anexos do paciente
- **Descrição:** Cada anexo traz uma `url` assinada, válida por 1 hora.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do paciente |

**Respostas:**
- `200` Lista de anexos — campos: `dados`; item de `dados`: `id`, `pacienteId`, `tipoAnexoId`, `descricao`, `ativo`, `createdAt`, `url`
- `400` `id` inválido
- `404` Paciente não encontrado

### `POST /pacientes/{id}/anexos`

- **Permissão:** `paciente:update` · **Manual:** [op-post-pacientes-id-anexos](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-pacientes-id-anexos)
- **Resumo:** Enviar anexo(s) do paciente
- **Descrição:** `multipart/form-data`, campo `file` (até 10 arquivos por requisição). Formatos aceitos: JPG, PNG e PDF, até 10MB cada. Campo opcional `tipoAnexoId` no corpo classifica o tipo de documento. Não há rota de exclusão de anexo nesta API — é uma operação restrita à tela do sistema.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do paciente |

**Corpo** (`multipart/form-data`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `file` | lista de string (binary) | **sim** |  |
| `tipoAnexoId` | integer | não | aceita null |

**Respostas:**
- `200` Anexo(s) enviado(s). Se `tipoAnexoId` for informado, anexos antigos do mesmo tipo são desativados (`ativo:false`) antes de criar os novos — não aparece no corpo. — campos: `message`, `anexos`, `paths`
- `400` Nenhum arquivo enviado, formato não permitido ou acima de 10MB
- `404` Paciente não encontrado
