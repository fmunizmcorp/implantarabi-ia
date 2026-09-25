# Rotas — Faturamento (24 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 -m ferramentas.rabi_api.atualizar_spec` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `GET /faturamento/guias`
- `GET /faturamento/guias/buscar-por-numero-guia`
- `GET /faturamento/guias/pacientes`
- `GET /faturamento/guias/info-extras/{guiaMae}/{guiaFilha}`
- `GET /faturamento/guias/valores-atualizados/{guiaMae}/{guiaFilha}`
- `GET /faturamento/guias/conversoes-convenio/{guiaMae}/{guiaFilha}/{convenioId}`
- `GET /faturamento/guias/{guiaMae}/filhas`
- `GET /faturamento/guias/servico/{guiaFilha}`
- `GET /faturamento/guias/valores-atendimento/{atendimentoId}`
- `PUT /faturamento/guias/{servicoAtendimentoId}`
- `PUT /faturamento/guias/{guiaMae}/confirmar`
- `GET /faturamento/divergencias`
- `POST /faturamento/divergencias/{numeroGuiaMae}/faturar-diferenca`
- `GET /faturamento/recebimento`
- `GET /faturamento/recebimento/opcoes`
- `POST /faturamento/recebimento/registrar`
- `POST /faturamento/recebimento/devolver`
- `GET /faturamento/glosas`
- `GET /faturamento/glosas/guia/{guiaMae}`
- `GET /faturamento/glosas/status`
- `GET /faturamento/glosas/motivos`
- `PUT /faturamento/glosas/produto`
- `PUT /faturamento/glosas/taxa`
- `PUT /faturamento/glosas/servico`

### `GET /faturamento/guias`

- **Permissão:** `faturamento:read` · **Manual:** [op-get-faturamento-guias](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-faturamento-guias)
- **Resumo:** Listar todas as guias em pré-faturamento

**Respostas:**
- `200` Lista de guias (nota: a rota interna usa `items`, normalizado pra `dados` nesta API) — campos: `dados`, `total`, `page`, `pageSize`, `totalPages`; item de `dados`: `atendimentoId`, `servicoAtendimentoId`, `dataAtendimento`, `paciente`, `colaborador`, `convenio`, `unidade`, `tipoGuia`, `preFaturado`, `guiaMae`, `guiaFilha`, `status`, `statusId`, `statusServico`, `statusServicoId`, `numeroLote`, `valor`, `glosa`

### `GET /faturamento/guias/buscar-por-numero-guia`

- **Permissão:** `faturamento:read` · **Manual:** [op-get-faturamento-guias-buscar-por-numero-guia](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-faturamento-guias-buscar-por-numero-guia)
- **Resumo:** Buscar guia pelo número
- **Descrição:** **O parâmetro de query é `numero`, não `numeroGuia`** — e é obrigatório.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `numero` | query | string | **sim** |  |

**Respostas:**
- `200` Envelope de lista padrão, mesmo sendo uma busca por número específico (pode casar mais de um registro). — campos: `dados`, `page`, `pageSize`, `total`, `totalPages`; item de `dados`: `atendimentoId`, `servicoAtendimentoId`, `dataAtendimento`, `paciente`, `colaborador`, `convenio`, `unidade`, `tipoGuia`, `preFaturado`, `guiaMae`, `guiaFilha`, `guiaFilhaDatas`, `status`, `statusId`, `statusServico`, `statusServicoId`, `numeroLote`, `valor`, `glosa`, `numeroBuscado`
- `400` Parâmetro 'numero' é obrigatório

### `GET /faturamento/guias/pacientes`

- **Permissão:** `faturamento:read` · **Manual:** [op-get-faturamento-guias-pacientes](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-faturamento-guias-pacientes)
- **Resumo:** Listar pacientes com pré-faturamento pendente
- **Descrição:** Limitado a 50 por padrão.

**Respostas:**
- `200` Lista de pacientes — campos: `dados`, `page`, `pageSize`, `total`, `totalPages`; item de `dados`: `id`, `nome`

### `GET /faturamento/guias/info-extras/{guiaMae}/{guiaFilha}`

- **Permissão:** `faturamento:read` · **Manual:** [op-get-faturamento-guias-info-extras-guiamae-guiafilha](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-faturamento-guias-info-extras-guiamae-guiafilha)
- **Resumo:** Informações extras da guia
- **Descrição:** Payload grande — dados cadastrais completos de paciente/convênio, autorização, e a composição de serviço/produtos/taxas (originais e convertidos pelo convênio). Valores monetários aqui já em reais.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `guiaMae` | path | string | **sim** |  |
| `guiaFilha` | path | string | **sim** |  |

**Respostas:**
- `200` Informações extras — campos: `id`, `Paciente`, `Convenio`, `servicoConvenio`, `produtosConvenio`, `taxasConvenio`, `Autorizacao`, `caraterAtendimento`, `dataAtendimento`

### `GET /faturamento/guias/valores-atualizados/{guiaMae}/{guiaFilha}`

- **Permissão:** `faturamento:read` · **Manual:** [op-get-faturamento-guias-valores-atualizados-guiamae-guiafilha](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-faturamento-guias-valores-atualizados-guiamae-guiafilha)
- **Resumo:** Valores atualizados da guia
- **Descrição:** `valorTotal` é só o valor resolvido do serviço, apesar do nome — não é a soma de produtos+taxas.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `guiaMae` | path | string | **sim** |  |
| `guiaFilha` | path | string | **sim** |  |

**Respostas:**
- `200` Valores atualizados (em reais) — campos: `servico`, `produtos`, `taxas`, `valorTotal`, `operadora`

### `GET /faturamento/guias/conversoes-convenio/{guiaMae}/{guiaFilha}/{convenioId}`

- **Permissão:** `faturamento:read` · **Manual:** [op-get-faturamento-guias-conversoes-convenio-guiamae-guiafilha-convenioid](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-faturamento-guias-conversoes-convenio-guiamae-guiafilha-convenioid)
- **Resumo:** Conversões de convênio disponíveis para a guia

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `guiaMae` | path | string | **sim** |  |
| `guiaFilha` | path | string | **sim** |  |
| `convenioId` | path | integer | **sim** |  |

**Respostas:**
- `200` Conversões disponíveis (em reais) — campos: `servicoConvenio`, `produtosConvenio`, `taxasConvenio`

### `GET /faturamento/guias/{guiaMae}/filhas`

- **Permissão:** `faturamento:read` · **Manual:** [op-get-faturamento-guias-guiamae-filhas](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-faturamento-guias-guiamae-filhas)
- **Resumo:** Listar guias filhas de uma guia mãe
- **Descrição:** A guia mãe (guiaFilha === guiaMae) vem primeiro na lista.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `guiaMae` | path | string | **sim** |  |

**Respostas:**
- `200` Lista de guias filhas — campos: `dados`, `page`, `pageSize`, `total`, `totalPages`; item de `dados`: `atendimentoId`, `servicoAtendimentoId`, `dataAtendimento`, `status`, `guiaMae`, `guiaFilha`, `valor`

### `GET /faturamento/guias/servico/{guiaFilha}`

- **Permissão:** `faturamento:read` · **Manual:** [op-get-faturamento-guias-servico-guiafilha](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-faturamento-guias-servico-guiafilha)
- **Resumo:** Serviço vinculado a uma guia filha
- **Descrição:** **Payload grande**: devolve as linhas cruas de `ServicoAtendimento` (toda coluna do modelo) com relações completas de colaborador, conversão de convênio, produtos/taxas/equipamentos usados — não um resumo. Valores (`valorServico`, `valorServicoConvertido`) vêm em centavos, sem conversão.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `guiaFilha` | path | string | **sim** |  |

**Respostas:**
- `200` Linhas de ServicoAtendimento (payload grande, ver descrição) — lista crua

### `GET /faturamento/guias/valores-atendimento/{atendimentoId}`

- **Permissão:** `faturamento:read` · **Manual:** [op-get-faturamento-guias-valores-atendimento-atendimentoid](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-faturamento-guias-valores-atendimento-atendimentoid)
- **Resumo:** Valores faturados de um atendimento
- **Descrição:** Um item por serviço prestado no atendimento.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `atendimentoId` | path | integer | **sim** |  |

**Respostas:**
- `200` Valores do atendimento (em reais) — lista crua: `servicoAtendimentoId`, `servico`, `produtos`, `taxas`, `totalServico`, `totalProdutos`, `totalTaxas`, `total`

### `PUT /faturamento/guias/{servicoAtendimentoId}`

- **Permissão:** `faturamento:update` · **Manual:** [op-put-faturamento-guias-servicoatendimentoid](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-put-faturamento-guias-servicoatendimentoid)
- **Resumo:** Editar a guia por completo
- **Descrição:** Edição completa: número da guia, conversão de convênio/colaborador, valores de produto/taxa/serviço. Não sensibiliza estoque (já foi baixado no consumo real do atendimento).

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `servicoAtendimentoId` | path | integer | **sim** |  |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `responsavelId` | integer | **sim** |  |
| `preFaturamento` | objeto | **sim** | Campos da guia a atualizar |

**Respostas:**
- `201` Corpo simples — não ecoa o objeto `preFaturamento` enviado. — campos: `success`, `message`, `numeroGuiaMae`
- `400` responsavelId ausente/inválido

### `PUT /faturamento/guias/{guiaMae}/confirmar`

- **Permissão:** `faturamento:update` · **Manual:** [op-put-faturamento-guias-guiamae-confirmar](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-put-faturamento-guias-guiamae-confirmar)
- **Resumo:** Confirmar pré-faturamento da guia
- **Descrição:** Valida campos TISS obrigatórios (ex.: número da guia da operadora) e marca a guia como pré-faturada.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `guiaMae` | path | string | **sim** |  |

**Respostas:**
- `201` **Corpo de sucesso é o número cru `200`** (não um objeto) — comportamento observado, o use case retorna o literal 200 e o controller devolve isso como corpo com status HTTP 201. — integer
- `400` Guia/serviço não encontrado, ou validação TISS falhou (lista de campos faltando na mensagem)

### `GET /faturamento/divergencias`

- **Permissão:** `faturamento:read` · **Manual:** [op-get-faturamento-divergencias](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-faturamento-divergencias)
- **Resumo:** Listar divergências atendido x faturado
- **Descrição:** Cache Redis de 60s (quando disponível) — dado pode estar até 60s desatualizado.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `page` | query | integer | não | mín. 1; padrão `1` |
| `pageSize` | query | integer | não | mín. 1; máx. 200; padrão `20` |

**Respostas:**
- `200` Lista paginada. — campos: `dados`, `page`, `pageSize`, `total`, `totalPages`; item de `dados`: `numeroGuiaMae`, `autorizacaoId`, `atendimentoId`, `pacienteNome`, `convenioNome`, `detectadoEm`, `motivoDivergencia`

### `POST /faturamento/divergencias/{numeroGuiaMae}/faturar-diferenca`

- **Permissão:** `faturamento:update` · **Manual:** [op-post-faturamento-divergencias-numeroguiamae-faturar-diferenca](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-faturamento-divergencias-numeroguiamae-faturar-diferenca)
- **Resumo:** Faturar a diferença de uma divergência
- **Descrição:** Para itens sub-faturados, inclui a diferença num lote. Bloqueado (409) se houver item sobre-faturado — esse caso exige correção manual.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `numeroGuiaMae` | path | string | **sim** |  |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `responsavelId` | integer | **sim** |  |

**Respostas:**
- `200` Diferença faturada — campos: `numeroGuiaMae`, `loteId`, `servicoAtendimentoIdsFaturados`
- `400` responsavelId ausente/inválido, ou não há divergência pendente para esta guia
- `409` Item sobre-faturado, ou a diferença não corresponde a nenhum registro — exige correção manual

### `GET /faturamento/recebimento`

- **Permissão:** `faturamento:read` · **Manual:** [op-get-faturamento-recebimento](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-faturamento-recebimento)
- **Resumo:** Listar recebimento físico de guias

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `page` | query | integer | não |  |
| `pageSize` | query | integer | não |  |
| `numeroGuia` | query | string | não |  |

**Respostas:**
- `200` Lista paginada — campos: `dados`, `page`, `pageSize`, `total`, `totalPages`; item de `dados`: `id`, `numeroGuia`, `statusRecebimento`, `registradoEm`, `colaborador`, `paciente`, `convenio`

### `GET /faturamento/recebimento/opcoes`

- **Permissão:** `faturamento:read` · **Manual:** [op-get-faturamento-recebimento-opcoes](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-faturamento-recebimento-opcoes)
- **Resumo:** Opções de filtro do recebimento de guia

**Respostas:**
- `200` Opções (valores distintos já cadastrados) — campos: `colaboradores`, `convenios`, `servicos`, `statusGuia`, `numeroGuias`, `pacientes`

### `POST /faturamento/recebimento/registrar`

- **Permissão:** `faturamento:create` · **Manual:** [op-post-faturamento-recebimento-registrar](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-faturamento-recebimento-registrar)
- **Resumo:** Registrar recebimento físico de guias

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `responsavelId` | integer | **sim** |  |
| `guias` | lista de objeto | **sim** |  |
| `guias[].codigoLido` | string | não |  |
| `guias[].servicoAtendimentoId` | integer | não | aceita null |

**Respostas:**
- `201` Corpo simples — não ecoa ids nem quantas guias foram processadas. — campos: `message`
- `400` Nenhuma guia informada, ou responsavelId ausente/inválido

### `POST /faturamento/recebimento/devolver`

- **Permissão:** `faturamento:update` · **Manual:** [op-post-faturamento-recebimento-devolver](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-faturamento-recebimento-devolver)
- **Resumo:** Registrar devolução de guias

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `responsavelId` | integer | **sim** |  |
| `guias` | lista de objeto | **sim** |  |
| `guias[].codigoLido` | string | não |  |
| `guias[].servicoAtendimentoId` | integer | não | aceita null |

**Respostas:**
- `200` Corpo simples — não ecoa ids nem quantas guias foram processadas. — campos: `message`
- `400` Nenhuma guia informada, ou responsavelId ausente/inválido

### `GET /faturamento/glosas`

- **Permissão:** `faturamento:read` · **Manual:** [op-get-faturamento-glosas](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-faturamento-glosas)
- **Resumo:** Listar itens em conta a receber (elegíveis a glosa)

**Respostas:**
- `200` Lista de itens — campos: `dados`, `page`, `pageSize`, `total`, `totalPages`; item de `dados`: `numeroLote`, `valorTotal`, `status`, `convenio`, `dataAtendimento`, `guiaMae`

### `GET /faturamento/glosas/guia/{guiaMae}`

- **Permissão:** `faturamento:read` · **Manual:** [op-get-faturamento-glosas-guia-guiamae](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-faturamento-glosas-guia-guiamae)
- **Resumo:** Listar serviços/produtos/taxas de uma guia mãe
- **Descrição:** Não é uma lista apesar do nome — é um único objeto agregado com três arrays internos. `valor`/`valorPagoGlosa` aqui vêm como string, em centavos brutos (diferente de `valorTotal` de `/glosas`, que é string em reais).

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `guiaMae` | path | string | **sim** |  |

**Respostas:**
- `200` Itens da guia — campos: `numeroLote`, `status`, `convenio`, `dataAtendimento`, `guiaMae`, `servicos`, `produtos`, `taxa`

### `GET /faturamento/glosas/status`

- **Permissão:** `faturamento:read` · **Manual:** [op-get-faturamento-glosas-status](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-faturamento-glosas-status)
- **Resumo:** Listar status de glosa possíveis
- **Descrição:** `id` não é numérico — é o próprio valor do enum como texto (ex.: `"GLOSADO"`).

**Respostas:**
- `200` Lista de status — campos: `dados`, `page`, `pageSize`, `total`, `totalPages`; item de `dados`: `id`, `descricao`

### `GET /faturamento/glosas/motivos`

- **Permissão:** `faturamento:read` · **Manual:** [op-get-faturamento-glosas-motivos](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-faturamento-glosas-motivos)
- **Resumo:** Listar motivos de glosa

**Respostas:**
- `200` Lista de motivos — campos: `dados`, `page`, `pageSize`, `total`, `totalPages`; item de `dados`: `id`, `nome`

### `PUT /faturamento/glosas/produto`

- **Permissão:** `faturamento:update` · **Manual:** [op-put-faturamento-glosas-produto](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-put-faturamento-glosas-produto)
- **Resumo:** Registrar glosa de produto
- **Descrição:** Só grava o resultado da glosa no item (não gera lançamento financeiro). **Nomes de campo reais do body (confirmados no código, diferentes do que o nome sugere):** `ProdutoAtendimentoId` — apesar do nome, é o id de `produtoConvercao` (a linha de conversão pelo convênio), não o id de `ProdutoAtendimento`. `valorPagoGlosa` precisa ser enviado em **centavos** (padrão diferente de outras rotas de faturamento, que usam reais). Erro de `motivoGlosado` (id) não encontrado em `term_mensagens` devolve **401**, não 400/422 — comportamento observado, não é sobre autenticação.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `ProdutoAtendimentoId` | integer | não | Id de produtoConvercao, apesar do nome |
| `motivoGlosado` | integer | não | Id em term_mensagens |
| `statusGlosado` | string | não |  |
| `valorPagoGlosa` | integer | não | Centavos, não reais |

**Respostas:**
- `200` Nenhum eco do registro atualizado. — campos: `message`, `success`

### `PUT /faturamento/glosas/taxa`

- **Permissão:** `faturamento:update` · **Manual:** [op-put-faturamento-glosas-taxa](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-put-faturamento-glosas-taxa)
- **Resumo:** Registrar glosa de taxa
- **Descrição:** Mesmas ressalvas de `PUT /faturamento/glosas/produto` (id é de `taxaConvercao`, `valorPagoGlosa` em centavos, erro de motivo devolve 401).

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `TaxaDocumentoId` | integer | não | Id de taxaConvercao, apesar do nome |
| `motivoGlosado` | integer | não |  |
| `statusGlosado` | string | não |  |
| `valorPagoGlosa` | integer | não | Centavos, não reais |

**Respostas:**
- `200` Nenhum eco do registro atualizado. — campos: `message`, `success`

### `PUT /faturamento/glosas/servico`

- **Permissão:** `faturamento:update` · **Manual:** [op-put-faturamento-glosas-servico](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-put-faturamento-glosas-servico)
- **Resumo:** Registrar glosa de serviço
- **Descrição:** Mesmas ressalvas de `PUT /faturamento/glosas/produto` (id é de `servicoConversao`, `valorPagoGlosa` em centavos, erro de motivo devolve 401).

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `ServicoAtendimentoId` | integer | não | Id de servicoConversao, apesar do nome |
| `motivoGlosado` | integer | não |  |
| `statusGlosado` | string | não |  |
| `valorPagoGlosa` | integer | não | Centavos, não reais |

**Respostas:**
- `200` Nenhum eco do registro atualizado. — campos: `message`, `success`
