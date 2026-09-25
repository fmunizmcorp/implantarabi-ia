# Rotas — Serviços (6 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 -m ferramentas.rabi_api.atualizar_spec` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `GET /servicos`
- `POST /servicos`
- `POST /servicos/bulk`
- `GET /servicos/{id}`
- `PUT /servicos/{id}`
- `DELETE /servicos/{id}`

### `GET /servicos`

- **Permissão:** `servico:read` · **Manual:** [op-get-servicos](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-servicos)
- **Resumo:** Listar serviços

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |
| `ativo` | query | boolean | não | Sem informar, lista ativos e inativos. |
| `nome` | query | string | não | Filtro por nome (contém, sem diferenciar maiúsculas) |

**Respostas:**
- `200` Lista paginada (versão resumida de cada serviço) — campos: `page`, `pageSize`, `total`, `totalPages`, `dados`; item de `dados`: `id`, `nome`, `valor`, `tempoServico`, `ativo`, `tipoServico`

### `POST /servicos`

- **Permissão:** `servico:create` · **Manual:** [op-post-servicos](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-servicos)
- **Resumo:** Cadastrar serviço

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `nome` | string | **sim** |  |
| `descricao` | string | **sim** |  |
| `codigo` | string | não | aceita null |
| `codigoTUSS` | string | não | aceita null |
| `valor` | number | não | Em reais (não em centavos). |
| `tempoServico` | number | não | aceita null; Duração em minutos |
| `somarItems` | boolean | não | padrão `False`; Se true, o valor é calculado somando os itens vinculados em vez do `valor` informado. |
| `linkAuxiliar` | string | não | aceita null |
| `preparamentos` | string | não | aceita null |
| `preparo` | string | não | aceita null |
| `tipoServicoId` | integer | não | aceita null |
| `tipoCodigoId` | integer | não | aceita null |
| `tipoGuiaId` | integer | não | aceita null |
| `tabelaANS87ID` | integer | não | aceita null |
| `regimeDeAtendimentoId` | integer | não | aceita null |
| `tipoAtendimento` | integer | não | aceita null; ID do tipo de atendimento |
| `taxaServicoId` | integer | não | aceita null |
| `valorTaxaServico` | number | não | aceita null |
| `especialidadesId` | lista de integer | não |  |
| `produtoIds` | lista de integer | não |  |
| `equipamentoIds` | lista de integer | não |  |
| `servicosRelacionados` | lista de integer | não | IDs de serviços que compõem este serviço |
| `habilitarAgendamentoOnline` | boolean | não | padrão `False` |
| `apenasComColaboradorDesignado` | boolean | não | padrão `False` |

**Respostas:**
- `201` Serviço criado — campos: `id`, `nome`, `descricao`, `codigo`, `codigoTUSS`, `valor`, `tempoServico`, `somarItens`, `ativo`, `createdAt`, `updatedAt`

### `POST /servicos/bulk`

- **Permissão:** `servico:create` · **Manual:** [op-post-servicos-bulk](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-post-servicos-bulk)
- **Resumo:** Cadastrar vários serviços de uma vez
- **Descrição:** Até 50 itens por requisição (chave `servicos`). `207` = falha parcial, ver `resultados`; reenvie só os itens com erro.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `servicos` | lista de objeto | **sim** | máx. itens 50 |
| `servicos[].nome` | string | **sim** |  |
| `servicos[].descricao` | string | **sim** |  |
| `servicos[].codigo` | string | não | aceita null |
| `servicos[].codigoTUSS` | string | não | aceita null |
| `servicos[].valor` | number | não | Em reais (não em centavos). |
| `servicos[].tempoServico` | number | não | aceita null; Duração em minutos |
| `servicos[].somarItems` | boolean | não | padrão `False`; Se true, o valor é calculado somando os itens vinculados em vez do `valor` informado. |
| `servicos[].linkAuxiliar` | string | não | aceita null |
| `servicos[].preparamentos` | string | não | aceita null |
| `servicos[].preparo` | string | não | aceita null |
| `servicos[].tipoServicoId` | integer | não | aceita null |
| `servicos[].tipoCodigoId` | integer | não | aceita null |
| `servicos[].tipoGuiaId` | integer | não | aceita null |
| `servicos[].tabelaANS87ID` | integer | não | aceita null |
| `servicos[].regimeDeAtendimentoId` | integer | não | aceita null |
| `servicos[].tipoAtendimento` | integer | não | aceita null; ID do tipo de atendimento |
| `servicos[].taxaServicoId` | integer | não | aceita null |
| `servicos[].valorTaxaServico` | number | não | aceita null |
| `servicos[].especialidadesId` | lista de integer | não |  |
| `servicos[].produtoIds` | lista de integer | não |  |
| `servicos[].equipamentoIds` | lista de integer | não |  |
| `servicos[].servicosRelacionados` | lista de integer | não | IDs de serviços que compõem este serviço |
| `servicos[].habilitarAgendamentoOnline` | boolean | não | padrão `False` |
| `servicos[].apenasComColaboradorDesignado` | boolean | não | padrão `False` |

**Respostas:**
- `201` Todos criados — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `207` Falha parcial — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `400` Lote vazio ou acima de 50 itens
- `429` Já existe um lote em andamento para esta clínica e recurso

### `GET /servicos/{id}`

- **Permissão:** `servico:read` · **Manual:** [op-get-servicos-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-servicos-id)
- **Resumo:** Consultar serviço
- **Descrição:** Traz o serviço completo, incluindo serviços relacionados (composição).

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do serviço |

**Respostas:**
- `200` Serviço — campos: `id`, `nome`, `descricao`, `codigo`, `codigoTUSS`, `valor`, `tempoServico`, `somarItens`, `ativo`, `createdAt`, `updatedAt`
- `404` Serviço não encontrado

### `PUT /servicos/{id}`

- **Permissão:** `servico:update` · **Manual:** [op-put-servicos-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-servicos-id)
- **Resumo:** Atualizar serviço
- **Descrição:** Sobrescreve os dados — envie o objeto completo, campos omitidos não são preservados.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do serviço |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `nome` | string | **sim** |  |
| `descricao` | string | **sim** |  |
| `codigo` | string | não | aceita null |
| `codigoTUSS` | string | não | aceita null |
| `valor` | number | não | Em reais (não em centavos). |
| `tempoServico` | number | não | aceita null; Duração em minutos |
| `somarItems` | boolean | não | padrão `False`; Se true, o valor é calculado somando os itens vinculados em vez do `valor` informado. |
| `linkAuxiliar` | string | não | aceita null |
| `preparamentos` | string | não | aceita null |
| `preparo` | string | não | aceita null |
| `tipoServicoId` | integer | não | aceita null |
| `tipoCodigoId` | integer | não | aceita null |
| `tipoGuiaId` | integer | não | aceita null |
| `tabelaANS87ID` | integer | não | aceita null |
| `regimeDeAtendimentoId` | integer | não | aceita null |
| `tipoAtendimento` | integer | não | aceita null; ID do tipo de atendimento |
| `taxaServicoId` | integer | não | aceita null |
| `valorTaxaServico` | number | não | aceita null |
| `especialidadesId` | lista de integer | não |  |
| `produtoIds` | lista de integer | não |  |
| `equipamentoIds` | lista de integer | não |  |
| `servicosRelacionados` | lista de integer | não | IDs de serviços que compõem este serviço |
| `habilitarAgendamentoOnline` | boolean | não | padrão `False` |
| `apenasComColaboradorDesignado` | boolean | não | padrão `False` |

**Respostas:**
- `202` Serviço atualizado — campos: `id`, `nome`, `descricao`, `codigo`, `codigoTUSS`, `valor`, `tempoServico`, `somarItens`, `ativo`, `createdAt`, `updatedAt`

### `DELETE /servicos/{id}`

- **Permissão:** `servico:delete` · **Manual:** [op-delete-servicos-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-delete-servicos-id)
- **Resumo:** Desativar serviço
- **Descrição:** É uma **desativação** (`ativo = false`), não uma exclusão física.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do serviço |

**Respostas:**
- `200` **Corpo de sucesso é o número cru `201`**, não um objeto. — integer
- `404` Serviço não encontrado
