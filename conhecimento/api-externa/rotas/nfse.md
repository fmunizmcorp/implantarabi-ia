# Rotas — NFS-e (28 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 ferramentas/rabi_api/atualizar_spec.py` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `GET /nfse/emitentes`
- `GET /nfse/emitentes/{id}`
- `GET /nfse/perfis-fiscais`
- `GET /nfse/perfis-fiscais/{id}`
- `GET /nfse/tomadores`
- `POST /nfse/tomadores`
- `POST /nfse/tomadores/bulk`
- `GET /nfse/tomadores/{id}`
- `PUT /nfse/tomadores/{id}`
- `POST /nfse/tomadores/{id}/completar`
- `POST /nfse/tomadores/sincronizar-paciente/{pacienteId}`
- `GET /nfse/notas`
- `POST /nfse/notas`
- `GET /nfse/notas/{id}`
- `POST /nfse/notas/{id}/emitir`
- `POST /nfse/notas/{id}/consultar-protocolo`
- `POST /nfse/notas/{id}/emitir-contingencia`
- `POST /nfse/notas/{id}/transmitir-contingencia`
- `PUT /nfse/notas/{id}/tomador`
- `POST /nfse/notas/{id}/desistir`
- `POST /nfse/notas/{id}/cancelar`
- `POST /nfse/notas/{id}/substituir`
- `POST /nfse/notas/{id}/analise-fiscal`
- `GET /nfse/notas/{id}/xml`
- `GET /nfse/notas/{id}/links`
- `GET /nfse/notas/{id}/danfse.html`
- `GET /nfse/notas/{id}/danfse.pdf`
- `GET /nfse/notas/{id}/tentativas`

### `GET /nfse/emitentes`

- **Permissão:** `nfse:read` · **Manual:** [op-get-nfse-emitentes](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-nfse-emitentes)
- **Resumo:** Listar emitentes
- **Descrição:** Necessário para escolher `emitenteId` ao calcular uma nota. Sem certificado digital nem configuração de infraestrutura — isso não é exposto por esta API.

**Respostas:**
- `200` Lista — lista crua de `NfseEmitente`: `id`, `nome`, `razaoSocial`, `cnpj`, `ambiente`, `padrao`, `ativo`

### `GET /nfse/emitentes/{id}`

- **Permissão:** `nfse:read` · **Manual:** [op-get-nfse-emitentes-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-nfse-emitentes-id)
- **Resumo:** Consultar emitente

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | string | **sim** |  |

**Respostas:**
- `200` Emitente — campos: `id`, `nome`, `razaoSocial`, `cnpj`, `ambiente`, `padrao`, `ativo`
- `404` Emitente não encontrado

### `GET /nfse/perfis-fiscais`

- **Permissão:** `nfse:read` · **Manual:** [op-get-nfse-perfis-fiscais](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-nfse-perfis-fiscais)
- **Resumo:** Listar perfis fiscais
- **Descrição:** Necessário para escolher `perfilId` ao calcular uma nota.

**Respostas:**
- `200` Lista — lista crua de `NfsePerfilFiscal`: `id`, `nome`, `ativo`

### `GET /nfse/perfis-fiscais/{id}`

- **Permissão:** `nfse:read` · **Manual:** [op-get-nfse-perfis-fiscais-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-nfse-perfis-fiscais-id)
- **Resumo:** Consultar perfil fiscal

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | string | **sim** |  |

**Respostas:**
- `200` Perfil fiscal — campos: `id`, `nome`, `ativo`
- `404` Perfil não encontrado

### `GET /nfse/tomadores`

- **Permissão:** `nfse:read` · **Manual:** [op-get-nfse-tomadores](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-nfse-tomadores)
- **Resumo:** Listar tomadores

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `q` | query | string | não | Busca por nome/documento |
| `tipoPessoa` | query | string | não | valores: `PF`, `PJ` |
| `ativos` | query | string | não | valores: `1` |

**Respostas:**
- `200` Lista (até 20 resultados) — lista crua de `NfseTomador`: `id`, `nome`, `razaoSocial`, `tipo`, `tipoPessoa`, `doc`, `docFormatado`, `ativo`, `avisos`

### `POST /nfse/tomadores`

- **Permissão:** `nfse:create` · **Manual:** [op-post-nfse-tomadores](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-nfse-tomadores)
- **Resumo:** Cadastrar tomador

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `nome` | string | **sim** |  |
| `tipo` | string | **sim** | valores: `operadora`, `empresa`, `particular` |
| `cnpj` | string | não | aceita null; 14 dígitos — obrigatório se não informar cpf |
| `cpf` | string | não | aceita null; 11 dígitos — obrigatório se não informar cnpj |
| `razaoSocial` | string | não | aceita null |
| `nomeFantasia` | string | não | aceita null |
| `im` | string | não | aceita null |
| `logradouro` | string | não | aceita null |
| `numero` | string | não | aceita null |
| `complemento` | string | não | aceita null |
| `bairro` | string | não | aceita null |
| `cidade` | string | não | aceita null |
| `uf` | string | não | aceita null |
| `cep` | string | não | aceita null |
| `codigoMunicipio` | string | não | aceita null |

**Respostas:**
- `201` Tomador criado — campos: `id`, `nome`, `razaoSocial`, `tipo`, `tipoPessoa`, `doc`, `docFormatado`, `ativo`, `avisos`
- `400` Informe nome e tipo, e cnpj (14 dígitos) ou cpf (11 dígitos)

### `POST /nfse/tomadores/bulk`

- **Permissão:** `nfse:create` · **Manual:** [op-post-nfse-tomadores-bulk](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-nfse-tomadores-bulk)
- **Resumo:** Cadastrar vários tomadores de uma vez
- **Descrição:** Até 100 itens por requisição (chave `tomadores`). `207` = falha parcial.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `tomadores` | lista de objeto | **sim** | máx. itens 100 |
| `tomadores[].nome` | string | **sim** |  |
| `tomadores[].tipo` | string | **sim** | valores: `operadora`, `empresa`, `particular` |
| `tomadores[].cnpj` | string | não | aceita null; 14 dígitos — obrigatório se não informar cpf |
| `tomadores[].cpf` | string | não | aceita null; 11 dígitos — obrigatório se não informar cnpj |
| `tomadores[].razaoSocial` | string | não | aceita null |
| `tomadores[].nomeFantasia` | string | não | aceita null |
| `tomadores[].im` | string | não | aceita null |
| `tomadores[].logradouro` | string | não | aceita null |
| `tomadores[].numero` | string | não | aceita null |
| `tomadores[].complemento` | string | não | aceita null |
| `tomadores[].bairro` | string | não | aceita null |
| `tomadores[].cidade` | string | não | aceita null |
| `tomadores[].uf` | string | não | aceita null |
| `tomadores[].cep` | string | não | aceita null |
| `tomadores[].codigoMunicipio` | string | não | aceita null |

**Respostas:**
- `201` Todos criados — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `207` Falha parcial — campos: `total`, `criados`, `falhas`, `resultados`; item de `resultados`: `indice`, `status`, `id`, `identificador`, `erro`
- `400` Lote vazio ou acima de 100 itens
- `429` Já existe um lote em andamento para esta clínica e recurso

### `GET /nfse/tomadores/{id}`

- **Permissão:** `nfse:read` · **Manual:** [op-get-nfse-tomadores-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-nfse-tomadores-id)
- **Resumo:** Consultar tomador

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | string | **sim** |  |

**Respostas:**
- `200` Tomador — campos: `id`, `nome`, `razaoSocial`, `tipo`, `tipoPessoa`, `doc`, `docFormatado`, `ativo`, `avisos`
- `404` Tomador não encontrado

### `PUT /nfse/tomadores/{id}`

- **Permissão:** `nfse:update` · **Manual:** [op-put-nfse-tomadores-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-put-nfse-tomadores-id)
- **Resumo:** Atualizar tomador

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | string | **sim** |  |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `nome` | string | **sim** |  |
| `tipo` | string | **sim** | valores: `operadora`, `empresa`, `particular` |
| `cnpj` | string | não | aceita null; 14 dígitos — obrigatório se não informar cpf |
| `cpf` | string | não | aceita null; 11 dígitos — obrigatório se não informar cnpj |
| `razaoSocial` | string | não | aceita null |
| `nomeFantasia` | string | não | aceita null |
| `im` | string | não | aceita null |
| `logradouro` | string | não | aceita null |
| `numero` | string | não | aceita null |
| `complemento` | string | não | aceita null |
| `bairro` | string | não | aceita null |
| `cidade` | string | não | aceita null |
| `uf` | string | não | aceita null |
| `cep` | string | não | aceita null |
| `codigoMunicipio` | string | não | aceita null |

**Respostas:**
- `200` Tomador atualizado — campos: `id`, `nome`, `razaoSocial`, `tipo`, `tipoPessoa`, `doc`, `docFormatado`, `ativo`, `avisos`
- `404` Tomador não encontrado

### `POST /nfse/tomadores/{id}/completar`

- **Permissão:** `nfse:update` · **Manual:** [op-post-nfse-tomadores-id-completar](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-nfse-tomadores-id-completar)
- **Resumo:** Completar cadastro do tomador
- **Descrição:** Preenche campos vazios a partir do histórico de notas e/ou consulta à Receita Federal (PJ). Só preenche o que já não estiver preenchido.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | string | **sim** |  |

**Corpo** (`application/json`):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `consultarReceita` | boolean | não | padrão `True` |

**Respostas:**
- `200` Campos preenchidos. **Efeito colateral**: já grava os campos preenchidos no tomador (`prisma.nfseTomador.update`) — a resposta é o diff aplicado, não o tomador inteiro atualizado. — campos: `preenchidos`, `fontes`, `dadosCnpj`, `nomeCombina`, `avisos`
- `404` Tomador não encontrado

### `POST /nfse/tomadores/sincronizar-paciente/{pacienteId}`

- **Permissão:** `nfse:read` · **Manual:** [op-post-nfse-tomadores-sincronizar-paciente-pacienteid](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-nfse-tomadores-sincronizar-paciente-pacienteid)
- **Resumo:** Sincronizar tomador a partir de um paciente
- **Descrição:** Cria/garante um tomador clonando o perfil fiscal padrão de pessoa física, sem precisar configurar fiscal por paciente. Idempotente (find-or-create por paciente).

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `pacienteId` | path | integer | **sim** |  |

**Respostas:**
- `200` Tomador sincronizado — campos: `tomadorId`, `nome`
- `404` Paciente não encontrado

### `GET /nfse/notas`

- **Permissão:** `nfse:read` · **Manual:** [op-get-nfse-notas](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-nfse-notas)
- **Resumo:** Listar notas

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `emitenteId` | query | string | não |  |
| `tomadorId` | query | string | não |  |
| `status` | query | string | não |  |
| `referenciaExterna` | query | string | não |  |
| `dataInicial` | query | string (date) | não |  |
| `dataFinal` | query | string (date) | não |  |
| `limite` | query | integer | não | máx. 500; padrão `100` |
| `pular` | query | integer | não | padrão `0` |

**Respostas:**
- `200` Lista — campos: `total`, `itens`

### `POST /nfse/notas`

- **Permissão:** `nfse:create` · **Manual:** [op-post-nfse-notas](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-nfse-notas)
- **Resumo:** Calcular nota (não emite)
- **Descrição:** Calcula e confere os valores, sem enviar nada à prefeitura ainda — use `POST /nfse/notas/{id}/emitir` para efetivar. Idempotente via header `Idempotency-Key` ou campo `chaveIdempotencia`.

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `emitenteId` | string | **sim** |  |
| `tomadorId` | string | **sim** |  |
| `perfilId` | string | **sim** |  |
| `valorServicos` | number | **sim** |  |
| `dataCompetencia` | string (date) | **sim** |  |
| `referencia` | string | não | aceita null |
| `referenciaExterna` | string | não | aceita null; ID livre para correlacionar com o sistema de origem |
| `dataPagamento` | string (date) | não | aceita null |
| `detalhamentoAdicional` | string | não | aceita null |
| `descontoCondicionado` | number | não | aceita null |
| `descontoIncondicionado` | number | não | aceita null |
| `deducoesBaseISSQN` | number | não | aceita null |
| `notaSubstituidaId` | string | não | aceita null; Preencher para calcular uma nota que substitui uma já emitida |
| `tomadorDocConfirmado` | string | não | aceita null |

**Respostas:**
- `201` Nota calculada — campos: `id`, `status`, `valorServicos`, `dataCompetencia`, `nfse`, `erroUltimo`, `criadoEm`
- `400` emitenteId/tomadorId/perfilId inválido ou inativo, ou valorServicos/dataCompetencia inválido
- `409` Guarda de tomador falhou (ex.: documento não confirmado)

### `GET /nfse/notas/{id}`

- **Permissão:** `nfse:read` · **Manual:** [op-get-nfse-notas-id](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-nfse-notas-id)
- **Resumo:** Consultar nota

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | string | **sim** |  |

**Respostas:**
- `200` Nota — campos: `id`, `status`, `valorServicos`, `dataCompetencia`, `nfse`, `erroUltimo`, `criadoEm`
- `404` Nota não encontrada

### `POST /nfse/notas/{id}/emitir`

- **Permissão:** `nfse:create` · **Manual:** [op-post-nfse-notas-id-emitir](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-nfse-notas-id-emitir)
- **Resumo:** Emitir nota — EFEITO FISCAL
- **Descrição:** Envia a nota de verdade à prefeitura. Consome o limite mensal do plano (`nfse.notas.mes`). Campo `forcar: true` no corpo emite mesmo se a conferência automática não estiver apta (assume o risco). `modo: "assincrono"` só vale para o padrão nacional.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | string | **sim** |  |

**Corpo** (`application/json`):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `forcar` | boolean | não | padrão `False` |
| `modo` | string | não | valores: `sincrono`, `assincrono`; padrão `sincrono` |

**Respostas:**
- `200` Nota emitida — campos: `id`, `status`, `valorServicos`, `dataCompetencia`, `nfse`, `erroUltimo`, `criadoEm`
- `409` Nota já emitida, ou não apta para emissão
- `502` Falha na comunicação com a prefeitura

### `POST /nfse/notas/{id}/consultar-protocolo`

- **Permissão:** `nfse:create` · **Manual:** [op-post-nfse-notas-id-consultar-protocolo](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-nfse-notas-id-consultar-protocolo)
- **Resumo:** Consultar protocolo de emissão assíncrona
- **Descrição:** Só para notas emitidas no `modo: "assincrono"` — verifica se a prefeitura já processou e, se sim, grava o resultado (mesmo desfecho de emitir síncrono).

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | string | **sim** |  |

**Respostas:**
- `200` Nota atualizada (ainda processando ou já emitida) — campos: `id`, `status`, `valorServicos`, `dataCompetencia`, `nfse`, `erroUltimo`, `criadoEm`
- `409` Esta nota não está aguardando protocolo assíncrono

### `POST /nfse/notas/{id}/emitir-contingencia`

- **Permissão:** `nfse:create` · **Manual:** [op-post-nfse-notas-id-emitir-contingencia](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-nfse-notas-id-emitir-contingencia)
- **Resumo:** Emitir em contingência — EFEITO FISCAL
- **Descrição:** Gera a nota localmente, sem contato com a prefeitura (para quando o webservice está fora do ar). Precisa ser transmitida depois via `transmitir-contingencia`, dentro do prazo municipal.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | string | **sim** |  |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `justificativa` | string | **sim** | mín. caracteres 15 |

**Respostas:**
- `200` Nota emitida em contingência — campos: `id`, `status`, `valorServicos`, `dataCompetencia`, `nfse`, `erroUltimo`, `criadoEm`
- `400` Justificativa com menos de 15 caracteres

### `POST /nfse/notas/{id}/transmitir-contingencia`

- **Permissão:** `nfse:create` · **Manual:** [op-post-nfse-notas-id-transmitir-contingencia](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-nfse-notas-id-transmitir-contingencia)
- **Resumo:** Transmitir nota emitida em contingência — EFEITO FISCAL

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | string | **sim** |  |

**Respostas:**
- `200` Nota transmitida — campos: `id`, `status`, `valorServicos`, `dataCompetencia`, `nfse`, `erroUltimo`, `criadoEm`
- `409` Esta nota não está aguardando transmissão de contingência
- `502` Falha na comunicação com a prefeitura

### `PUT /nfse/notas/{id}/tomador`

- **Permissão:** `nfse:update` · **Manual:** [op-put-nfse-notas-id-tomador](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-put-nfse-notas-id-tomador)
- **Resumo:** Trocar tomador da nota
- **Descrição:** Só antes de enviar à prefeitura (status calculada/conferida/erro). Usado para um pagador avulso (CPF/nome informados na hora).

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | string | **sim** |  |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `cpf` | string | **sim** |  |
| `nome` | string | **sim** |  |
| `email` | string | não | aceita null |
| `fone` | string | não | aceita null |

**Respostas:**
- `200` Tomador trocado — campos: `id`, `status`, `valorServicos`, `dataCompetencia`, `nfse`, `erroUltimo`, `criadoEm`
- `409` Nota já enviada à prefeitura — não pode mais trocar o tomador

### `POST /nfse/notas/{id}/desistir`

- **Permissão:** `nfse:delete` · **Manual:** [op-post-nfse-notas-id-desistir](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-nfse-notas-id-desistir)
- **Resumo:** Desistir da nota (antes de emitir)
- **Descrição:** Só para nota ainda não emitida — nota já emitida se cancela, não se desiste.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | string | **sim** |  |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `motivo` | string | **sim** |  |

**Respostas:**
- `200` Nota marcada como desistida — campos: `id`, `status`, `valorServicos`, `dataCompetencia`, `nfse`, `erroUltimo`, `criadoEm`
- `409` Nota já emitida ou em outro status incompatível

### `POST /nfse/notas/{id}/cancelar`

- **Permissão:** `nfse:delete` · **Manual:** [op-post-nfse-notas-id-cancelar](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-nfse-notas-id-cancelar)
- **Resumo:** Cancelar nota emitida — EFEITO FISCAL
- **Descrição:** Cancelamento de verdade na prefeitura (padrão nacional com fallback ABRASF).

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | string | **sim** |  |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `motivo` | string | **sim** | mín. caracteres 15 |
| `codigo` | string | não | valores: `1`, `2`, `9`; padrão `1` |

**Respostas:**
- `200` Nota cancelada — campos: `id`, `status`, `valorServicos`, `dataCompetencia`, `nfse`, `erroUltimo`, `criadoEm`
- `400` Motivo com menos de 15 caracteres
- `409` Só nota emitida pode ser cancelada
- `502` Falha na comunicação com a prefeitura

### `POST /nfse/notas/{id}/substituir`

- **Permissão:** `nfse:create` · **Manual:** [op-post-nfse-notas-id-substituir](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-nfse-notas-id-substituir)
- **Resumo:** Calcular nota substituindo uma já emitida
- **Descrição:** Calcula uma nota nova reaproveitando os dados da antiga (só sobrescreve o que for enviado no corpo). A antiga só é cancelada de verdade quando a nova emitir com sucesso.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | string | **sim** | ID da nota a ser substituída |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `motivo` | string | **sim** | mín. caracteres 15; Motivo da substituição |

**Respostas:**
- `201` Nova nota calculada — campos: `id`, `status`, `valorServicos`, `dataCompetencia`, `nfse`, `erroUltimo`, `criadoEm`
- `409` Só nota emitida pode ser substituída, ou já tem substituta em andamento

### `POST /nfse/notas/{id}/analise-fiscal`

- **Permissão:** `nfse:delete` · **Manual:** [op-post-nfse-notas-id-analise-fiscal](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-post-nfse-notas-id-analise-fiscal)
- **Resumo:** Solicitar análise fiscal de cancelamento fora do prazo
- **Descrição:** Só padrão nacional. O desfecho é assíncrono — a nota fica em `analise_fiscal_pendente` até a prefeitura decidir.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | string | **sim** |  |

**Corpo** (`application/json`, obrigatório):

| Campo | Tipo | Obrig. | Observação |
|---|---|---|---|
| `motivo` | string | **sim** | mín. caracteres 15 |
| `codigo` | string | não | valores: `1`, `2`, `9`; padrão `1` |

**Respostas:**
- `200` Pedido enviado — campos: `id`, `status`, `valorServicos`, `dataCompetencia`, `nfse`, `erroUltimo`, `criadoEm`
- `409` Só nota emitida no padrão nacional pode solicitar análise fiscal

### `GET /nfse/notas/{id}/xml`

- **Permissão:** `nfse:read` · **Manual:** [op-get-nfse-notas-id-xml](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-nfse-notas-id-xml)
- **Resumo:** Baixar XML da NFS-e
- **Descrição:** **Não é JSON** — `Content-Type: application/xml`, com `Content-Disposition: attachment; filename="NFSe_00001234.xml"`. Corpo é o XML já assinado, cru.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | string | **sim** |  |

**Respostas:**
- `200` Arquivo XML
- `404` Nota sem XML (não foi emitida)

### `GET /nfse/notas/{id}/links`

- **Permissão:** `nfse:read` · **Manual:** [op-get-nfse-notas-id-links](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-nfse-notas-id-links)
- **Resumo:** Links oficiais de visualização/autenticidade
- **Descrição:** Sem `?atualizar=1`, devolve o que já está gravado (se existir); com `?atualizar=1`, reconsulta a prefeitura.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | string | **sim** |  |
| `atualizar` | query | string | não | valores: `1` |

**Respostas:**
- `200` Links — campos: `numero`, `visualizacao`, `autenticidade`, `origem`
- `404` Nota não encontrada, ou prefeitura não devolveu links
- `409` Nota ainda não foi emitida

### `GET /nfse/notas/{id}/danfse.html`

- **Permissão:** `nfse:read` · **Manual:** [op-get-nfse-notas-id-danfse-html](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-nfse-notas-id-danfse-html)
- **Resumo:** Visualizar DANFSe (HTML)
- **Descrição:** **Não é JSON** — `Content-Type: text/html`, sem `Content-Disposition` (renderizável inline, não é anexo).

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | string | **sim** |  |

**Respostas:**
- `200` HTML do DANFSe
- `404` Nota sem XML (não foi emitida)

### `GET /nfse/notas/{id}/danfse.pdf`

- **Permissão:** `nfse:read` · **Manual:** [op-get-nfse-notas-id-danfse-pdf](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-nfse-notas-id-danfse-pdf)
- **Resumo:** Baixar DANFSe (PDF)
- **Descrição:** **Não é JSON, é binário** — `Content-Type: application/pdf`, `Content-Disposition: attachment; filename="NFSe_00001234.pdf"`.

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | string | **sim** |  |

**Respostas:**
- `200` Arquivo PDF
- `404` Nota sem XML (não foi emitida)
- `500` PDF indisponível — a mensagem indica o motivo e recomenda usar danfse.html + "salvar como PDF"

### `GET /nfse/notas/{id}/tentativas`

- **Permissão:** `nfse:read` · **Manual:** [op-get-nfse-notas-id-tentativas](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#op-get-nfse-notas-id-tentativas)
- **Resumo:** Histórico de tentativas de comunicação com a prefeitura
- **Descrição:** `?xml=1` inclui requisição/resposta bruta trocada com a prefeitura (pode ser grande e sensível).

| Parâmetro | Onde | Tipo | Obrig. | Observação |
|---|---|---|---|---|
| `id` | path | string | **sim** |  |
| `xml` | query | string | não | valores: `1`; 1 para incluir requisição/resposta bruta |

**Respostas:**
- `200` Array direto, sem envelope de paginação. — lista crua: `id`, `operacao`, `padrao`, `ambiente`, `httpStatus`, `sucesso`, `mensagens`, `duracaoMs`, `criadoEm`, `requisicao`, `resposta`
- `404` Nota não encontrada
