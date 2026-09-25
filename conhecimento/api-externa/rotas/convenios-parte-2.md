# Rotas — Convênios (21 operações) — parte 2 de 2

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 -m ferramentas.rabi_api.atualizar_spec` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

Outras partes: [parte 1](convenios-parte-1.md).

### `PUT /convenios/{id}/servicos`

- **Permissão:** `convenio:update` · **Manual:** [op-put-convenios-id-servicos](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-convenios-id-servicos)
- **Resumo:** Definir serviços do convênio (em lote)
- **Descrição:** Equivale à aba **Serviços** do cadastro de convênio. Aceita até **200 serviços por requisição**, todos do mesmo convênio. **Comportamento (upsert)** - A chave é `servicoId`: cria o vínculo se ainda não existir, atualiza se já existir. - Campos omitidos **mantêm o valor atual**, exceto `valorInternoConvenio`: omitido mantém, `null` limpa. - Idempotente: reenviar o mesmo item não duplica. **Como interpretar a resposta** - `200`: todos os serviços foram processados. - `207`: ao menos um falhou. Confira `resultados` pelo `indice`. **Limites** - Máximo de 200 serviços por requisição (`400` acima disso). - Só uma atualização por vez por convênio: uma segunda, enquanto a primeira roda, recebe `429`. - Interrompida após 45 segundos; o restante volta como `NAO_PROCESSADO`.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `servicos` | lista de objeto | **sim** | máx. itens 200 |
| `servicos[].servicoId` | integer | **sim** | ID do serviço cadastrado no sistema (coluna **Serviço** da tela) |
| `servicos[].utiliza` | boolean | não | Coluna **Utiliza**. Omitido: mantém o valor atual (ou `false` se o vínculo for novo). |
| `servicos[].zerarValor` | boolean | não |  |
| `servicos[].pacote` | boolean | não |  |
| `servicos[].autorizacaoPrevia` | boolean | não |  |
| `servicos[].retornoServico` | boolean | não |  |
| `servicos[].ativo` | boolean | não |  |
| `servicos[].nomeConversao` | string | não |  |
| `servicos[].descricaoConvenio` | string | não |  |
| `servicos[].valorInternoConvenio` | number | não | aceita null; Em reais. `null` limpa o valor. Omitido: mantém o valor atual. |
| `servicos[].parcelasMaximas` | integer | não |  |
| `servicos[].tipoCodigoId` | integer | não |  |
| `servicos[].tipoAtendimentoId` | integer | não | aceita null |
| `servicos[].tabela87ANSId` | integer | não |  |
| `servicos[].kitDocumentoId` | integer | não |  |
| `servicos[].codigo` | string | não |  |
| `servicos[].codigoTuss` | string | não |  |
| `servicos[].codigoConvenio` | string | não |  |

**Respostas:**
- `200` Todos os serviços foram processados — campos: `total`, `criados`, `atualizados`, `falhas`, `resultados`; item de `resultados`: `indice`, `servicoId`, `status`, `id`, `erro`
- `207` Processado com falhas parciais. Veja `resultados`. — campos: `total`, `criados`, `atualizados`, `falhas`, `resultados`; item de `resultados`: `indice`, `servicoId`, `status`, `id`, `erro`
- `400` `id` inválido, lista vazia, sem a chave `servicos` ou acima de 200 itens
- `404` Convênio não encontrado
- `429` Já existe uma atualização em andamento para este convênio

### `GET /convenios/{id}/produtos`

- **Permissão:** `convenio:read` · **Manual:** [op-get-convenios-id-produtos](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-convenios-id-produtos)
- **Resumo:** Listar produtos do convênio

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |

**Respostas:**
- `200` Lista paginada — campos: `page`, `pageSize`, `total`, `totalPages`, `dados`; item de `dados`: `produtoId`, `utiliza`, `zerarValor`, `nomeConversao`, `descricaoConversao`, `valorUnitarioConversao`, `fatorK`, `parcelasMaximas`, `tipoCodigoId`, `tabela87ANSId`, `fontePrecoCompraOptionsId`, `tipoPrecificacao`, `codigo`, `codigoTuss`, `codigoTiss`, `codigoConversao`, `id`
- `400` `id` inválido
- `404` Convênio não encontrado

### `PUT /convenios/{id}/produtos`

- **Permissão:** `convenio:update` · **Manual:** [op-put-convenios-id-produtos](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-convenios-id-produtos)
- **Resumo:** Definir produtos do convênio (em lote)
- **Descrição:** Equivale à aba **Produtos** do cadastro de convênio. Aceita até **200 produtos por requisição**, todos do mesmo convênio. **Comportamento (upsert)** - A chave é `produtoId`: cria o vínculo se ainda não existir, atualiza se já existir. - Campos omitidos **mantêm o valor atual**, exceto `valorUnitarioConversao` e `fatorK`: omitido mantém, `null` limpa. - Idempotente: reenviar o mesmo item não duplica. **Como interpretar a resposta** - `200`: todos os produtos foram processados. - `207`: ao menos um falhou. Confira `resultados` pelo `indice`. **Limites** - Máximo de 200 produtos por requisição (`400` acima disso). - Só uma atualização por vez por convênio: uma segunda, enquanto a primeira roda, recebe `429`. - Interrompida após 45 segundos; o restante volta como `NAO_PROCESSADO`.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `produtos` | lista de objeto | **sim** | máx. itens 200 |
| `produtos[].produtoId` | integer | **sim** | ID do produto cadastrado no sistema (coluna **Produto** da tela) |
| `produtos[].utiliza` | boolean | não | Coluna **Utiliza**. Omitido: mantém o valor atual (ou `false` se o vínculo for novo). |
| `produtos[].zerarValor` | boolean | não | Coluna **Zerar Valor**. |
| `produtos[].nomeConversao` | string | não |  |
| `produtos[].descricaoConversao` | string | não |  |
| `produtos[].valorUnitarioConversao` | number | não | aceita null; Valor unitário em reais. `null` limpa o valor. Omitido: mantém o valor atual. |
| `produtos[].fatorK` | string | não | aceita null; Percentual do fatorK/inflator/deflator. Aceita vírgula ou ponto. `null` limpa. |
| `produtos[].parcelasMaximas` | integer | não |  |
| `produtos[].tipoCodigoId` | integer | não | aceita null |
| `produtos[].tabela87ANSId` | integer | não | aceita null |
| `produtos[].fontePrecoCompraOptionsId` | integer | não | Fonte de preço de compra usada na política de preço. |
| `produtos[].tipoPrecificacao` | string | não | valores: `PRECO_1`, `PRECO_2`, `PRECO_3` |
| `produtos[].codigo` | string | não |  |
| `produtos[].codigoTuss` | string | não |  |
| `produtos[].codigoTiss` | string | não |  |
| `produtos[].codigoConversao` | string | não |  |

**Respostas:**
- `200` Todos os produtos foram processados — campos: `total`, `criados`, `atualizados`, `falhas`, `resultados`; item de `resultados`: `indice`, `produtoId`, `status`, `id`, `erro`
- `207` Processado com falhas parciais. Veja `resultados`. — campos: `total`, `criados`, `atualizados`, `falhas`, `resultados`; item de `resultados`: `indice`, `produtoId`, `status`, `id`, `erro`
- `400` `id` inválido, lista vazia, sem a chave `produtos` ou acima de 200 itens
- `404` Convênio não encontrado
- `429` Já existe uma atualização em andamento para este convênio

### `GET /convenios/{id}/especialidades`

- **Permissão:** `convenio:read` · **Manual:** [op-get-convenios-id-especialidades](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-convenios-id-especialidades)
- **Resumo:** Listar especialidades do convênio

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |

**Respostas:**
- `200` Lista paginada — campos: `page`, `pageSize`, `total`, `totalPages`, `dados`; item de `dados`: `especialidadeId`, `utiliza`, `dataInicio`, `dataFim`, `id`
- `400` `id` inválido
- `404` Convênio não encontrado

### `PUT /convenios/{id}/especialidades`

- **Permissão:** `convenio:update` · **Manual:** [op-put-convenios-id-especialidades](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-convenios-id-especialidades)
- **Resumo:** Definir especialidades do convênio (em lote)
- **Descrição:** Equivale à aba **Especialidades** do cadastro de convênio. Aceita até **200 especialidades por requisição**, todas do mesmo convênio. **Comportamento (upsert)** - A chave é `especialidadeId`: cria o vínculo se ainda não existir, atualiza se já existir. A tabela não tem restrição única no banco (é o mesmo comportamento da tela interna); esta rota resolve isso do lado da aplicação, usando sempre a linha mais antiga quando há mais de uma. - Campos omitidos **mantêm o valor atual**. - Idempotente: reenviar o mesmo item não duplica. **Como interpretar a resposta** - `200`: todas as especialidades foram processadas. - `207`: ao menos uma falhou. Confira `resultados` pelo `indice`. **Limites** - Máximo de 200 especialidades por requisição (`400` acima disso). - Só uma atualização por vez por convênio: uma segunda, enquanto a primeira roda, recebe `429`. - Interrompida após 45 segundos; o restante volta como `NAO_PROCESSADO`.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `especialidades` | lista de objeto | **sim** | máx. itens 200 |
| `especialidades[].especialidadeId` | integer | **sim** | ID da especialidade cadastrada no sistema (coluna **Especialidade** da tela) |
| `especialidades[].utiliza` | boolean | não | Coluna **Atende**. Omitido: mantém o valor atual (ou `false` se o vínculo for novo). |
| `especialidades[].dataInicio` | string (date-time) | não | aceita null |
| `especialidades[].dataFim` | string (date-time) | não | aceita null |

**Respostas:**
- `200` Todas as especialidades foram processadas — campos: `total`, `criados`, `atualizados`, `falhas`, `resultados`; item de `resultados`: `indice`, `especialidadeId`, `status`, `id`, `erro`
- `207` Processado com falhas parciais. Veja `resultados`. — campos: `total`, `criados`, `atualizados`, `falhas`, `resultados`; item de `resultados`: `indice`, `especialidadeId`, `status`, `id`, `erro`
- `400` `id` inválido, lista vazia, sem a chave `especialidades` ou acima de 200 itens
- `404` Convênio não encontrado
- `429` Já existe uma atualização em andamento para este convênio

### `GET /convenios/{id}/planos`

- **Permissão:** `convenio:read` · **Manual:** [op-get-convenios-id-planos](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-convenios-id-planos)
- **Resumo:** Listar planos do convênio

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |

**Respostas:**
- `200` Lista paginada — campos: `page`, `pageSize`, `total`, `totalPages`, `dados`; item de `dados`: `planoId`, `utiliza`, `id`
- `400` `id` inválido
- `404` Convênio não encontrado

### `PUT /convenios/{id}/planos`

- **Permissão:** `convenio:update` · **Manual:** [op-put-convenios-id-planos](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-convenios-id-planos)
- **Resumo:** Definir planos do convênio (em lote)
- **Descrição:** Equivale à aba **Planos** do cadastro de convênio. Aceita até **200 planos por requisição**, todos do mesmo convênio. **Comportamento (upsert)** - A chave é `planoId`: cria o vínculo se ainda não existir, atualiza se já existir. A tabela não tem restrição única no banco (mesmo comportamento da tela interna); esta rota resolve isso do lado da aplicação, usando sempre a linha mais antiga quando há mais de uma. - Idempotente: reenviar o mesmo item não duplica. **Como interpretar a resposta** - `200`: todos os planos foram processados. - `207`: ao menos um falhou. Confira `resultados` pelo `indice`. **Limites** - Máximo de 200 planos por requisição (`400` acima disso). - Só uma atualização por vez por convênio: uma segunda, enquanto a primeira roda, recebe `429`. - Interrompida após 45 segundos; o restante volta como `NAO_PROCESSADO`.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `planos` | lista de objeto | **sim** | máx. itens 200 |
| `planos[].planoId` | integer | **sim** | ID do plano cadastrado no sistema (coluna **Plano** da tela) |
| `planos[].utiliza` | boolean | não | Coluna **Atende**. Omitido: mantém o valor atual (ou `false` se o vínculo for novo). |

**Respostas:**
- `200` Todos os planos foram processados — campos: `total`, `criados`, `atualizados`, `falhas`, `resultados`; item de `resultados`: `indice`, `planoId`, `status`, `id`, `erro`
- `207` Processado com falhas parciais. Veja `resultados`. — campos: `total`, `criados`, `atualizados`, `falhas`, `resultados`; item de `resultados`: `indice`, `planoId`, `status`, `id`, `erro`
- `400` `id` inválido, lista vazia, sem a chave `planos` ou acima de 200 itens
- `404` Convênio não encontrado
- `429` Já existe uma atualização em andamento para este convênio

### `GET /convenios/{id}/farol/produtos`

- **Permissão:** `convenio:read` · **Manual:** [op-get-convenios-id-farol-produtos](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-convenios-id-farol-produtos)
- **Resumo:** Farol de produtos do convênio
- **Descrição:** Espelha a tela interna Farol do Convênio.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |
| `produto` | query | string | não |  |
| `codigo` | query | string | não |  |
| `farol` | query | string | não | Lista separada por vírgula |
| `ativoNoConvenio` | query | boolean | não |  |
| `produtoAtivo` | query | boolean | não |  |
| `search` | query | string | não |  |
| `sortBy` | query | string | não |  |
| `sortOrder` | query | string | não | valores: `asc`, `desc` |

**Respostas:**
- `200` Lista paginada — campos: `page`, `pageSize`, `total`, `totalPages`, `dados`; item de `dados`: `produto_id`, `produto`, `codigo`, `custo`, `receita`, `margem_resultado_pct`, `farol`, `ativo_no_convenio`, `produto_ativo`
- `400` `id` inválido
- `404` Convênio não encontrado

### `GET /convenios/{id}/farol/servicos`

- **Permissão:** `convenio:read` · **Manual:** [op-get-convenios-id-farol-servicos](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-convenios-id-farol-servicos)
- **Resumo:** Farol de serviços do convênio
- **Descrição:** Espelha a tela interna Farol do Convênio.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |
| `servico` | query | string | não |  |
| `codigo` | query | string | não |  |
| `farol` | query | string | não | Lista separada por vírgula |
| `ativoNoConvenio` | query | boolean | não |  |
| `servicoAtivo` | query | boolean | não |  |
| `search` | query | string | não |  |
| `sortBy` | query | string | não |  |
| `sortOrder` | query | string | não | valores: `asc`, `desc` |

**Respostas:**
- `200` Lista paginada — campos: `page`, `pageSize`, `total`, `totalPages`, `dados`; item de `dados`: `servico_id`, `servico`, `codigo`, `custo_total`, `receita_total`, `receita_propria_servico`, `margem_resultado_pct`, `farol`, `ativo_no_convenio`, `servico_ativo`
- `400` `id` inválido
- `404` Convênio não encontrado

### `GET /convenios/{id}/farol/itens`

- **Permissão:** `convenio:read` · **Manual:** [op-get-convenios-id-farol-itens](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-convenios-id-farol-itens)
- **Resumo:** Árvore de composição do convênio (produtos, taxas e sub-serviços)
- **Descrição:** Espelha a tela interna Farol do Convênio, aba Itens.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `50` |
| `servicoRaizId` | query | integer | não |  |
| `itemTipo` | query | string | não |  |
| `itemNome` | query | string | não |  |
| `search` | query | string | não |  |
| `apenasAtivosNoConvenio` | query | boolean | não | Restringe aos serviços contratados pelo convênio (vínculo `utiliza`) — não confundir com `servicoAtivo`. |
| `servicoAtivo` | query | boolean | não | Filtra pelo cadastro do serviço raiz estar ativo/inativo (`servico.ativo`), igual a `produtoAtivo` em `/farol/produtos` e `servicoAtivo` em `/farol/servicos`. |

**Respostas:**
- `200` Lista paginada — campos: `page`, `pageSize`, `total`, `totalPages`, `dados`; item de `dados`: `servico_raiz_id`, `item_tipo`, `item_id`, `item_nome`, `custo`, `receita`, `farol`, `utiliza`
- `400` `id` inválido
- `404` Convênio não encontrado

### `GET /convenios/{id}`

- **Permissão:** `convenio:read` · **Manual:** [op-get-convenios-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-convenios-id)
- **Resumo:** Consultar convênio

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |

**Respostas:**
- `200` Convênio — campos: `id`, `nomeFantasia`, `razaoSocial`, `cnpj`, `descricao`, `codigoANS`, `codigo`, `dataInicio`, `empresaPrincipalId`, `operadoraId`, `ativo`, `createdAt`, `updatedAt`
- `400` `id` inválido
- `404` Convênio não encontrado

### `PUT /convenios/{id}`

- **Permissão:** `convenio:update` · **Manual:** [op-put-convenios-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-put-convenios-id)
- **Resumo:** Atualizar convênio
- **Descrição:** **Atenção — a atualização substitui o cadastro, não faz merge parcial.** Envie sempre o convênio completo: - `empresaId` e `unidadesIds` são obrigatórios. As unidades que não estiverem na lista são **desativadas** no convênio. - Omitir `operadoraId` **remove** a operadora do convênio. - Omitir `dataFim`, `dataReajuste` ou `dataRenovacao` **limpa** essas datas. - Omitir `exigirToken` grava `false`. - `politicasPorTipoProduto`, quando enviado, é a lista completa: políticas que não estiverem nela são inativadas. Se for omitido, as políticas existentes não são alteradas.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `nomeFantasia` | string | não |  |
| `razaoSocial` | string | não |  |
| `cnpj` | string | não | Único por clínica |
| `descricao` | string | **sim** |  |
| `codigo` | integer | não |  |
| `telefone` | string | não |  |
| `email` | string | não |  |
| `pessoaDeContato` | string | não |  |
| `observacao` | string | não |  |
| `dataInicio` | string (date-time) | **sim** |  |
| `dataFim` | string (date-time) | não | aceita null |
| `dataReajuste` | string (date-time) | não | aceita null |
| `dataRenovacao` | string (date-time) | não | aceita null |
| `prazoRecursoGlosa` | integer | não |  |
| `prazoPagamentoRecursoGlosa` | integer | não |  |
| `prazoReajuste` | integer | não |  |
| `prazoAutorizacao` | integer | não |  |
| `prazoPagamento` | integer | não |  |
| `prazoRetorno` | integer | não |  |
| `prazoLimiteEntregaGuias` | integer | não |  |
| `limiteParcelasConvenioParticular` | integer | não |  |
| `fatorK` | number | não |  |
| `faturadoPagamento` | boolean | não |  |
| `exigirToken` | boolean | não |  |
| `operadoraId` | string | não | ID da operadora |
| `empresaId` | string | **sim** | ID da empresa dona do convênio ("Empresa Principal" na tela do sistema). |
| `unidadesIds` | lista de integer | **sim** | IDs das filiais/unidades ("Unidades" na tela do sistema) em que esse convênio é aceito na agenda. Pode incluir o mesmo ID de empresaId. |
| `kitDocumentosPadrao` | objeto | não |  |
| `kitDocumentosPadrao.id` | integer | não |  |
| `xmlConsultaId` | integer | não |  |
| `xmlSpSadtId` | integer | não |  |
| `politicasPorTipoProduto` | lista de objeto | não |  |
| `politicasPorTipoProduto[].tipoProdutoId` | integer | não |  |
| `politicasPorTipoProduto[].fatorK` | string | não | Percentual. Aceita vírgula ou ponto. |
| `politicasPorTipoProduto[].idJson` | string | não | JSON serializado com `fontePrecoId` e `tipoPrecificacao` |
| `codigoANS` | string | não | Código/registro ANS. **Na atualização, o nome do campo é `codigoANS`.** |

**Respostas:**
- `200` Convênio atualizado — campos: `id`, `nomeFantasia`, `razaoSocial`, `cnpj`, `descricao`, `codigoANS`, `codigo`, `dataInicio`, `empresaPrincipalId`, `operadoraId`, `ativo`, `createdAt`, `updatedAt`
- `400` `id` inválido
- `404` Convênio não encontrado
- `409` CNPJ já existe no sistema

### `DELETE /convenios/{id}`

- **Permissão:** `convenio:delete` · **Manual:** [op-delete-convenios-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-delete-convenios-id)
- **Resumo:** Desativar convênio
- **Descrição:** É uma **desativação** (`ativo = false`), não uma exclusão física. Se o convênio estiver em agendamentos ativos, a resposta traz um `aviso`.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | integer | **sim** | mín. 1; ID do convênio |

**Respostas:**
- `200` Convênio desativado — campos: `status`, `message`, `aviso`
- `400` `id` inválido
