# Rotas — Serviços (6 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-11-22.json`) · **Conferido em:** 2026-11-22
> **Vale para:** produção (Swagger publicado em 2026-11-22) · **Kit:** v0.3.3

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 ferramentas/rabi_api/atualizar_spec.py` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

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
| `especialidadesId` | lista de integer | não |  |
| `documentos` | lista de objeto | não | Documentos obrigatórios do serviço (ex.: PRESCRIÇÃO MÉDICA) — exigidos no agendamento, acolhimento, autorização e pela IA. No PUT, lista enviada substitui; omi… |
| `documentos[].id` | integer | não | ID do documento |
| `perfilFiscalId` | string | não | aceita null; Perfil fiscal (NFS-e) do serviço. `null` desvincula; omitido mantém (no PUT). |
| `produtoIds` | lista de integer ou objeto | não | ID do produto (quantidade 1) ou objeto com quantidade/valor. |
| `produtoIds[].(opção 1)` | integer | não |  |
| `produtoIds[].(opção 2)` | objeto | não |  |
| `produtoIds[].id` | integer | não |  |
| `produtoIds[].quantidade` | number | não | padrão `1` |
| `produtoIds[].valorUnitario` | number | não | Em reais. |
| `equipamentoIds` | lista de integer ou objeto | não |  |
| `equipamentoIds[].(opção 1)` | integer | não |  |
| `equipamentoIds[].(opção 2)` | objeto | não |  |
| `equipamentoIds[].id` | integer | não |  |
| `servicosRelacionados` | lista de integer ou objeto | não | Serviços que compõem este serviço: ID (quantidade 1) ou objeto com quantidade. |
| `servicosRelacionados[].(opção 1)` | integer | não |  |
| `servicosRelacionados[].(opção 2)` | objeto | não |  |
| `servicosRelacionados[].servicoId` | integer | não |  |
| `servicosRelacionados[].quantidade` | number | não | padrão `1` |
| `servicoTaxa` | lista de objeto | não | Taxas vinculadas ao serviço. |
| `servicoTaxa[].taxaId` | integer | não |  |
| `servicoTaxa[].quantidade` | number | não | padrão `1` |
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
| `servicos[].especialidadesId` | lista de integer | não |  |
| `servicos[].documentos` | lista de objeto | não | Documentos obrigatórios do serviço (ex.: PRESCRIÇÃO MÉDICA) — exigidos no agendamento, acolhimento, autorização e pela IA. No PUT, lista enviada substitui; omi… |
| `servicos[].documentos[].id` | integer | não | ID do documento |
| `servicos[].perfilFiscalId` | string | não | aceita null; Perfil fiscal (NFS-e) do serviço. `null` desvincula; omitido mantém (no PUT). |
| `servicos[].produtoIds` | lista de integer ou objeto | não | ID do produto (quantidade 1) ou objeto com quantidade/valor. |
| `servicos[].produtoIds[].(opção 1)` | integer | não |  |
| `servicos[].produtoIds[].(opção 2)` | objeto | não |  |
| `servicos[].produtoIds[].id` | integer | não |  |
| `servicos[].produtoIds[].quantidade` | number | não | padrão `1` |
| `servicos[].produtoIds[].valorUnitario` | number | não | Em reais. |
| `servicos[].equipamentoIds` | lista de integer ou objeto | não |  |
| `servicos[].equipamentoIds[].(opção 1)` | integer | não |  |
| `servicos[].equipamentoIds[].(opção 2)` | objeto | não |  |
| `servicos[].equipamentoIds[].id` | integer | não |  |
| `servicos[].servicosRelacionados` | lista de integer ou objeto | não | Serviços que compõem este serviço: ID (quantidade 1) ou objeto com quantidade. |
| `servicos[].servicosRelacionados[].(opção 1)` | integer | não |  |
| `servicos[].servicosRelacionados[].(opção 2)` | objeto | não |  |
| `servicos[].servicosRelacionados[].servicoId` | integer | não |  |
| `servicos[].servicosRelacionados[].quantidade` | number | não | padrão `1` |
| `servicos[].servicoTaxa` | lista de objeto | não | Taxas vinculadas ao serviço. |
| `servicos[].servicoTaxa[].taxaId` | integer | não |  |
| `servicos[].servicoTaxa[].quantidade` | number | não | padrão `1` |
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
- **Descrição:** Traz o serviço completo, incluindo composição (`servicosRelacionados`), especialidades (`especialidadesId`), documentos obrigatórios (`documentos`), produtos (`produtoIds`, valor em reais), equipamentos (`equipamentoIds`) e taxas (`servicoTaxa`) — com os mesmos nomes que o `PUT` aceita (também `somarItems`, `procedimentos`, `tipoAtendimento`, `perfilFiscalId`). Ler e reenviar sem alterar não muda nada.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do serviço |

**Respostas:**
- `200` Serviço — campos: `id`, `nome`, `descricao`, `codigo`, `codigoTUSS`, `valor`, `tempoServico`, `somarItens`, `ativo`, `createdAt`, `updatedAt`
- `404` Serviço não encontrado

### `PUT /servicos/{id}`

- **Permissão:** `servico:update` · **Manual:** [op-put-servicos-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-servicos-id)
- **Resumo:** Atualizar serviço
- **Descrição:** **Atualização parcial**: envie só o que quer mudar — todos os campos são opcionais. - Campo omitido: mantém o valor atual. - `null`: limpa o campo (ex.: `linkAuxiliar: null`, `perfilFiscalId: null`; `valor: null` vira 0). - Lista omitida (`documentos`, `produtoIds`, `equipamentoIds`, `servicoTaxa`, `especialidadesId`, `servicosRelacionados`): mantém os vínculos atuais. - Lista enviada: **substitui** os vínculos por exatamente o que veio. Para remover todos, envie `[]`. Ex.: `{ "nome": "X" }` só renomeia; `{ "documentos": [{ "id": 3 }] }` deixa só o documento 3.

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
| `especialidadesId` | lista de integer | não |  |
| `documentos` | lista de objeto | não | Documentos obrigatórios do serviço (ex.: PRESCRIÇÃO MÉDICA) — exigidos no agendamento, acolhimento, autorização e pela IA. No PUT, lista enviada substitui; omi… |
| `documentos[].id` | integer | não | ID do documento |
| `perfilFiscalId` | string | não | aceita null; Perfil fiscal (NFS-e) do serviço. `null` desvincula; omitido mantém (no PUT). |
| `produtoIds` | lista de integer ou objeto | não | ID do produto (quantidade 1) ou objeto com quantidade/valor. |
| `produtoIds[].(opção 1)` | integer | não |  |
| `produtoIds[].(opção 2)` | objeto | não |  |
| `produtoIds[].id` | integer | não |  |
| `produtoIds[].quantidade` | number | não | padrão `1` |
| `produtoIds[].valorUnitario` | number | não | Em reais. |
| `equipamentoIds` | lista de integer ou objeto | não |  |
| `equipamentoIds[].(opção 1)` | integer | não |  |
| `equipamentoIds[].(opção 2)` | objeto | não |  |
| `equipamentoIds[].id` | integer | não |  |
| `servicosRelacionados` | lista de integer ou objeto | não | Serviços que compõem este serviço: ID (quantidade 1) ou objeto com quantidade. |
| `servicosRelacionados[].(opção 1)` | integer | não |  |
| `servicosRelacionados[].(opção 2)` | objeto | não |  |
| `servicosRelacionados[].servicoId` | integer | não |  |
| `servicosRelacionados[].quantidade` | number | não | padrão `1` |
| `servicoTaxa` | lista de objeto | não | Taxas vinculadas ao serviço. |
| `servicoTaxa[].taxaId` | integer | não |  |
| `servicoTaxa[].quantidade` | number | não | padrão `1` |
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
