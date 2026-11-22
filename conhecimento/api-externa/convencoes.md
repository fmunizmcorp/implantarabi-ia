# Convenções da API externa (paginação, envelope, valores, PUT, DELETE, lotes, erros)

> **Fonte:** https://www.rabisistemas.com.br/manual/api-externa/index.html#convencoes (#paginacao, #valores, #put, #delete, #lotes, #codigos) · https://www.rabisistemas.com.br/manual/api-externa/erros-e-boas-praticas.html#armadilhas · Swagger (seção "Convenções gerais", snapshot `spec/openapi-2026-11-22.json`) · experiência de implantação real (24/09/2026) · leitura real (só GET) da API de produção em 25/09/2026 ~12h · **Conferido em:** 2026-11-22 (PUT parcial e limites conferidos no código `deploy_prd`)
> **Vale para:** produção (Swagger de 22/11/2026) · **Kit:** v0.4.0

O `ferramentas/rabi_api/cliente.py` já aplica quase tudo isto. Este arquivo explica o
porquê, para você não errar quando precisar sair do caminho feliz.

## 1. Paginação

| Regra | Valor |
|---|---|
| `page` | começa em **1**. `page=0` → **400** (`"Too small: expected number to be >0"`) |
| `pageSize` | padrão **50**, máximo **200** — desde out/2026 a API externa **reduz em silêncio** para 200 o que vier acima (`tetoPaginacao`): leia sempre o `pageSize` devolvido |
| Como percorrer | loop de `page=1` até `page = totalPages` — **não** pare porque a página veio menor que `pageSize` |
| Conferência | ao final, **itens lidos = `total`**. Se não bater, a leitura **falhou** (leia de novo) |

- Leituras que **não paginam de fato** (ex.: `GET /empresas`, `GET /locais`,
  `/auxiliares/*`, `/parametros/avisos`) usam o mesmo envelope com `page` = 1 e
  `pageSize`/`total` = tamanho da lista inteira.
- `GET /orcamentos` sem `pacienteId` **filtra depois de paginar**: `dados` pode vir menor que
  `pageSize` havendo mais páginas. Percorra por `totalPages`; a conferência de total pode
  não bater — use `ler_tudo(..., conferir_total=False)` só aqui, e diga isso na prova.
- `GET /agendamentos` **exige `data`** (um dia por chamada) e pagina de verdade
  (filtros `pacienteId`, `profissionalId`, `statusId`).
- `GET /grades-colaborador` e `GET /grades-equipamento` paginam de verdade; filtre por
  `colaboradorId`/`equipamentoId`, `localId`, `vigenteEm`.
- `GET /estoque` pagina e filtra por `produtoId` e `localizacaoId`.
- Filtro `ativo`: sem informar, a listagem traz **ativos e inativos**. Para conferir o que
  vale, use `?ativo=true`.
- **API interna é diferente:** lá a paginação começa em `page=0`. Não misture.

Uma lição de implantação real: **ler menos que o total e concluir** gerou quatro
conclusões erradas seguidas. Por isso o cliente confere o total e trata corpo vazio como
falha.

## 2. Envelope das listagens (e as exceções)

**Padrão (o Swagger de 25/09/2026 afirma que é único em toda listagem — e a leitura real de
25/09 ~12h confirmou nas rotas que eram exceção):**

```json
{ "dados": [ ... ], "page": 1, "pageSize": 50, "total": 123, "totalPages": 3 }
```

**Exceções corrigidas em produção — medido em 25/09/2026 ~12h:** `GET /tabelas-preco`,
`/orcamentos`, `/financeiro/movimentacoes`, `/estoque/saldo-produtos` e `/grades-colaborador`
devolvem o envelope padrão acima. As abas `GET /convenios/{id}/servicos|produtos|taxas` e o
Farol `GET /convenios/{id}/farol/itens|servicos|produtos` também usam o envelope padrão,
paginado. **Formatos antigos que o cliente ainda aceita** (medidos em 24/09; ficam só por
segurança, caso algum ambiente volte ao formato antigo):

| Formato | Rota onde foi visto | Como o cliente lê |
|---|---|---|
| lista crua `[ ... ]` | `GET /tabelas-preco` (antes de 25/09) | itens = a lista; uma página só |
| `{ message, data: [...] }` | `GET /orcamentos` (antes de 25/09) | itens = `data` |
| `{ data: [...], meta: { total, totalPages } }` | `GET /financeiro/movimentacoes` (antes de 25/09) | itens = `data`; total/páginas de `meta` |
| `{ items: [...], total, page, pageSize, totalPages }` | `GET /estoque/saldo-produtos` (antes de 25/09) | itens = `items` |

**Leituras que são "array direto" por desenho** (o Swagger diz na resposta; não são
listagens paginadas): `GET /atendimentos/historico`, `GET /estoque/historico/{id}`,
`GET /tabelas-preco/precificacao`, `GET /orcamentos/status`,
`GET /orcamentos/anexo/listar/{orcamentoId}`,
`GET /orcamentos/anexo/listar-necessarios/{pacienteId}`,
`GET /nfse/notas/{id}/tentativas`, `POST /agendamentos/horarios/disponiveis`.

**Respostas "estranhas" que não são erro** (documentadas no Swagger):

| Rota | Sem configuração salva devolve |
|---|---|
| `GET /parametros/orcamento` | o número `0` cru |
| `GET /parametros/acolhimento`, `/parametros/servicos-online`, `/parametros/termo` | `null` com 200 |
| `GET /parametros/desconto` | **404** |
| `GET /parametros/desconto/colaborador/{id}` | 200 com `nivelAlcada: "NIVEL0"`, `percentual: 0` |
| `GET /parametros/financeiro`, `/parametros/estoque` | objeto reduzido, sem `id` |
| `GET /faturamento/glosas/guia/{guiaMae}` | **um objeto** com três listas (não é lista) |
| `GET /faturamento/glosas/status` | `id` em texto (`"GLOSADO"`), não número |

Como conferir no spec atual quais rotas ainda são exceção:
`grep -rn "Array direto" conhecimento/api-externa/rotas/`.

## 3. Valores, datas, ids

- **Valores monetários em reais** na maioria das rotas (`50` = R$ 50,00).
- **Exceções em centavos ou texto** (ditas na descrição da rota — leia antes de somar):

| Rota | Campo | Unidade |
|---|---|---|
| `GET /faturamento/guias/servico/{guiaFilha}` | `valorServico`, `valorServicoConvertido` | **centavos** |
| `GET /faturamento/glosas/guia/{guiaMae}` | `valor`, `valorPagoGlosa` | **texto em centavos** (já `valorTotal` de `/glosas` é texto em reais) |
| `PUT /faturamento/glosas/produto` · `/taxa` · `/servico` | `valorPagoGlosa` (envio) | **centavos** |
| `GET /estoque/movimentacao/{id}`, `GET /estoque/buscar/{lote}/{produtoId}/{localizacaoId}` | valores crus | **centavos** (as outras rotas de estoque já convertem para reais) |
| `PUT /financeiro/movimentacoes/{id}` (resposta 200) | `valorUnitario`, `valor`, `valorPago`, multa, juros… | **centavos** |
| `GET /orcamentos` | itens de serviço/produto do orçamento | **centavos** |
| `GET /faturamento/guias/valores-atualizados/{guiaMae}/{guiaFilha}` | `valorTotal` | reais, mas **só o serviço** (não soma produtos e taxas) |

Para ver todas: `grep -rn -i "centavos" conhecimento/api-externa/rotas/`.

- **Vazio ≠ zero:** onde o campo aceita, `null` **limpa** (volta a vazio → o valor desce
  de nível), `0` é **zero de verdade**, omitido é diferente dos dois. **Nunca use 0,01**
  como "sem valor" (é cobrado como R$ 0,01).
- **Datas** em ISO 8601: `2026-01-01T00:00:00.000Z` (date-time) ou `2026-09-24` (date).
- **CNPJ** aceito com ou sem máscara em vários cadastros.
- **UF em três formatos:**

| Cadastro | Como mandar a UF |
|---|---|
| Empresa | id **ou** sigla (`"DF"`) |
| Operadora, colaborador | **nome por extenso** (`"Distrito Federal"`) — sigla dá 404 "Unidade Federativa não encontrada" |
| Paciente | `unidadeFederativaId` (id de `GET /auxiliares/unidades-federativas`) |

- **Nomes de campo que mudam:** convênio usa `registroANS` na criação e `codigoANS` na
  atualização; serviço envia `somarItems` e a leitura devolve `somarItens`.
- **Tipos inesperados:** no convênio `empresaId` e `operadoraId` são **texto**;
  `unidadesIds` é lista de inteiros. No colaborador, `especialidades[].especialidadeId` é
  texto.
- **`responsavelId`** (id de um colaborador já cadastrado, registrado como responsável) é
  exigido em: `POST/PUT /financeiro/movimentacoes` (+ `/bulk`), `POST /estoque/entrada`,
  `/saida`, `/transferencia`, `POST /agendamentos`, `PATCH /agendamentos/{id}/cancelar`,
  `GET /agendamentos/datas/disponiveis` (parâmetro), `POST /orcamentos`, `PUT /orcamentos/{id}`,
  `PUT /faturamento/guias/{servicoAtendimentoId}`,
  `POST /faturamento/divergencias/{numeroGuiaMae}/faturar-diferenca`,
  `POST /faturamento/recebimento/registrar`, `POST /faturamento/recebimento/devolver`,
  `PUT /atendimentos/{id}`. O quadro de permissões diz que `POST /atendimentos` também
  exige, mas o schema não traz o campo — se recusar, inclua.
- **Rótulo trocado:** em algumas rotas (financeiro, tabelas de preço, estoque, perguntas do
  agendamento online) o `{id}` aparece descrito como "ID do convênio" — é o id do
  registro daquela rota.
- **Sucesso não é só 200/201:** `POST /taxas` responde 200 ao criar; vários `PUT`
  respondem 202. Trate 2xx como sucesso.

## 4. PUT e PATCH — parcial onde o Rabi declara; no resto, objeto completo

**Mudou em 01–02/10/2026** (rabi-api `7d16cd50` e `49362b61`, em produção; Swagger de 22/11).
Até 30/09 a regra era "PUT sobrescreve: campo omitido é apagado". Agora há **três grupos**:

**Regra da API para as rotas parciais:** campo **omitido mantém** o valor atual · **`null` limpa** ·
**lista omitida mantém** os vínculos · **lista enviada substitui** os vínculos por exatamente o que
veio (**`[]` apaga todos**). A leitura (`GET`) devolve os nomes que o `PUT` aceita, e o PUT aceita
também os nomes de leitura conhecidos (contatos, endereço com maiúsculas, `limiteParcelasConvenios`,
`kitDocumentosId`).

**Regra do kit, valendo para os três grupos:** foto antes → mande **só o que muda** (nas rotas
parciais) ou o **objeto completo** (nas demais) → foto depois + diff. Toda **lista** que for no corpo
precisa estar **completa** (o que ficar fora é desvinculado) e aparece na prévia. Corpo gerado por
`ferramentas/rabi_api/corpo_escrita.py` (`corpo_parcial()` nas rotas parciais; `corpo_put_produto()` no produto).

**4.1 Parciais — 12 rotas** (11 declaradas na descrição da rota no Swagger de 22/11 e confirmadas no código `deploy_prd`; `PUT /financeiro/contas-caixa/{id}` declara "grava só os campos enviados" no **resumo** da rota, rota criada em 18/11 com o commit `03a8199c`)

| Rota | Atenção específica |
|---|---|
| `PUT /servicos/{id}` | listas `documentos`, `produtoIds`, `equipamentoIds`, `servicoTaxa`, `especialidadesId`, `servicosRelacionados`: omitida mantém, enviada substitui; `valor: null` vira 0. Produto da composição enviado **sem** `valorUnitario` mantém o valor que já tinha (`f8c7f474`) |
| `PUT /convenios/{id}` | `empresaId`/`unidadesIds` omitidos mantêm; **`unidadesIds` enviado é a lista completa** (unidade fora dela é desativada no convênio); `operadoraId`, `dataFim`, `dataReajuste`, `dataRenovacao`, `exigirToken`, `prazoLimiteEntregaGuias` omitidos mantêm, `null` limpa; `politicasPorTipoProduto`, se enviado, é a lista completa. O manual ainda recomendava (05/11, pendência C11) mandar o objeto completo por cautela (#698); o **código** de `deploy_prd` é parcial — **conferido pelo mantenedor em 22/11** em `src/modules/convenio/controllers/updateConvenio/updateConvenioController.ts` ("#640 prática 2 — grava só o que veio (tela e API externa): omitido mantém, null limpa"). O kit segue o código, mas **nunca** manda `unidadesIds`/`politicasPorTipoProduto` sem ter lido e conferido contra a régua. A leitura traz `empresaPrincipalId` (escrita: `empresaId`) |
| `PUT /convenios/{id}/servicos` · `/taxas` · `/produtos` | upsert por id do item; omitido mantém; `null` ou `""` limpa código, Tabela 87, fonte de preço, `valorInternoConvenio`/`valorConvertido`/`valorUnitarioConversao`/`fatorK`. Utiliza em serviço de especialidade **não atendida** pelo convênio é recusado como problema do item (trava #628) — grave a aba Especialidades antes |
| `PUT /pacientes/{id}` | `contato` e `convenioPlano` enviados substituem (contato/carteira com `id` que não veio é **inativado**); CPF só revalidado quando vem |
| `PUT /pacientes/{id}/convenios/{vinculoId}` | `convenioId`, `planoId`, `numeroDaCarterinha`, `validade` omitidos mantêm; `null`/`""` limpa |
| `PUT /colaboradores/{id}` | não reativa colaborador desativado; `vinculoRepasse` (`produtos`/`servicos`/`taxas`) trocado só quando enviado; item de repasse vazio = **linha geral** do tipo (#643); `perguntasIds` omitido mantém; o GET traz `perguntasIds`, `vinculoRepasse` e `mensagem` no formato do PUT |
| `PUT /grades-colaborador/{id}` | `agendamentoOnline`, `modoConvenio` (`INCLUIR`/`EXCLUIR` — trocar inverte o sentido da lista) e `limitesConvenio` só mudam quando enviados. Segue: corpo é **lista direta**, cada item com o próprio `id`; o `{id}` do caminho é ignorado (defeito aberto) |
| `PUT /grades-equipamento/{id}` | `profissionais` (aceita `colaboradores`), `convenios`, `servicos`: omitidas mantêm, enviadas substituem |
| `PUT /orcamentos/{id}` | `procedimentos` enviado substitui, reconhecendo o serviço existente por `orcamentoServicoId`; **leitura em centavos** (÷100 antes de reenviar). Operação da clínica — ordem escrita |
| `PUT /financeiro/movimentacoes/{id}` | `registroFinanceiro`/`duplicatas`: item com `id` atualizado no lugar, sem `id` criado, que não veio **removido**; leitura em centavos. Dinheiro — ordem escrita |
| `PUT /faturamento/guias/{servicoAtendimentoId}` | produtos/taxas que não vieram **não** são removidos. Ordem escrita |
| `PUT /financeiro/contas-caixa/{id}` | grava só os campos enviados; `ativo: false` desativa (não há DELETE) |

Também mantêm o omitido (já antes de 01/10): `PUT /convenios/{id}/colaboradores` (listas de
especialidades **aditivas** — remover só pela tela), `PUT /convenios/{id}/especialidades` (upsert por
`especialidadeId`; sem "Atende" no corpo mantém o valor), `PUT /parametros/desconto`,
`PATCH /parametros/servicos-online/textos-informativos`. `PUT /parametros/financeiro` é **misto**:
omitir (ou mandar `0`, `""`, `false`) em `categoriaPagamentoId`/`centroDeCustoId` **grava null** —
mande sempre os dois. `PUT /convenios/{id}/planos`: mande o item completo, com `utiliza`.

**4.2 Sobrescrevem / sincronizam (declarado)**

| Rota | O que acontece |
|---|---|
| `PUT /empresas/{id}` | substitui o cadastro inteiro. (O Swagger de 22/11 ainda diz "mesmo comportamento do `PUT /convenios/{id}`", mas o de convênio passou a ser parcial — texto incoerente; o kit trata empresa como **objeto completo**, defeitos-conhecidos.md) |
| `PUT /operadoras/{id}` | listas `plano` e `contato` sincronizadas: o que não vier é **removido** |
| `POST /atendimentos/prontuario` | sobrescreve o texto sem guardar versão anterior |

**4.3 Não declaram → objeto completo (GET → altera → reenvia tudo)**

`PUT /locais/{id}` · `PUT /produtos/{id}` · `PUT /equipamentos/{id}` · `PUT /taxas/{id}` ·
`PUT /fornecedores/{id}` · `PUT /fabricantes/{id}` · `PUT /depositos/{id}` · `PUT /tabelas-preco/{id}` ·
`PUT /nfse/tomadores/{id}` · `PUT /nfse/notas/{id}/tomador` · `PATCH /agendamentos/{id}/cancelar` ·
`PUT /orcamentos/status/{idOrcamento}/{idStatus}` · `PUT /faturamento/guias/{guiaMae}/confirmar` ·
`PUT /faturamento/glosas/produto` · `/taxa` · `/servico` · `PUT /atendimentos/{id}` ·
`PUT /parametros/orcamento` · `/estoque` · `/avisos/{chave}` · `/acolhimento` · `/termo` ·
`/dashboard-permissoes/graficos` · `/dashboard-permissoes/dashboards` · `/dashboard-atribuicao` ·
`PUT /parametros/servicos-online/agendamento/perguntas/{id}` · os `PATCH .../habilitar` de
servicos-online. Para `/produtos` use `corpo_escrita.corpo_put_produto` (modo completo).
`PUT /produtos/{id}` com `ativo: false` também é recusado com **409** se o produto estiver em serviço
ativo (FAQ F007).

**4.4 Controle de versão (409 de conflito)** — desde 01–02/10 as tabelas de configuração do
convênio (e outras) têm `version`. O PUT **só confere** a versão se o corpo trouxer `version`; sem
ela, grava como antes. Com versão velha → **409** (alguém mudou na tela depois do seu GET): releia,
refaça a prévia, não force. Não documentado no Swagger externo (`ff78db95`, `e8c3364f`). As gravações
da API ficam na auditoria com origem `API_EXTERNA`.

**Gravações antigas:** serviço, paciente ou convênio gravado por PUT **antes de 01/10/2026** seguiu a
regra antiga (omitido apagava) — conferência única na [FAQ F006](../faq-ias/F006-conferir-gravacoes-anteriores-a-28-09.md).

## 5. DELETE = inativação lógica

`DELETE` **nunca apaga**: grava `ativo = false`. Mesmo assim, **só com ordem escrita**
([proibidas-sem-ordem-escrita.md](proibidas-sem-ordem-escrita.md)).

| Recurso | Particularidade |
|---|---|
| Operadora | recusa (400) se houver convênio ativo vinculado |
| Empresa | recusa (400) com atendimentos, colaboradores, convênios, depósitos, locais ou movimentações ativas |
| Local | recusa (409) com agendamentos, orçamentos, grades ou vínculos de serviço |
| Colaborador | desativa também grades, especialidades e vínculos de empresa; **avisa** (não bloqueia) se houver agendamento futuro |
| Convênio | se estiver em agendamentos ativos, a resposta traz um aviso |
| Produto | desativa também os fornecedores vinculados |
| Grades | `DELETE /grades-colaborador/{id}` = a série a partir do horário; `/unique/{id}` = só aquele horário |
| Sem rota de exclusão | fornecedor, anexo de paciente, prontuário, movimentação financeira |

## 6. Lotes (`/bulk` e abas do convênio)

| Rota | Máx. por chamada | Chave do corpo |
|---|---|---|
| `POST /convenios/bulk`, `/pacientes/bulk`, `/operadoras/bulk`, `/servicos/bulk`, `/colaboradores/bulk`, `/produtos/bulk`, `/equipamentos/bulk`, `/taxas/bulk`, `/fornecedores/bulk`, `/fabricantes/bulk`, `/depositos/bulk` | **50** | o plural do recurso |
| `POST /financeiro/movimentacoes/bulk` | **50** | `movimentacoes` + `responsavelId` único |
| `POST /nfse/tomadores/bulk` | **100** | `tomadores` |
| `POST /tabelas-preco/produtos/bulk` | **200** | `precos` |
| `PUT /convenios/{id}/colaboradores` | **100** | `colaboradores` |
| `PUT /convenios/{id}/taxas` · `/servicos` · `/produtos` · `/especialidades` · `/planos` | **200** | `taxas`, `servicos`, `produtos`, `especialidades`, `planos` |

- **201** = todos criados (abas do convênio: **200** = todos processados).
- **207 Multi-Status = falha parcial.** Leia `resultados` item a item pelo `indice`
  (posição no array enviado, **começa em 0**). Status: `CRIADO`, `ATUALIZADO`, `ERRO`
  (com `erro`), `NAO_PROCESSADO`. Cada item é gravado em transação própria — nunca pela
  metade. Guarde os ids dos `CRIADO`.
- **Reenvie só `ERRO` (corrigido) e `NAO_PROCESSADO`**, nunca o lote inteiro.
  (Reenviar tudo só é seguro nas abas do convênio e em `/tabelas-preco/produtos(/bulk)`,
  que são upsert.)
- **429** = já existe um lote em andamento para a clínica e o recurso (nas abas: um por
  convênio). **Um lote por vez**, em sequência. O cliente espera e tenta até 3 vezes.
- **Corte de 45 s:** o que sobrar volta como `NAO_PROCESSADO`.
- **400** = lote vazio, sem a chave esperada ou acima do limite.
- 50 é o **teto**, não a meta: lotes menores facilitam a prévia e a prova.
- `enviar_lote()` do cliente faz tudo isso e devolve a lista `reenviar`.

## 7. Códigos de resposta

| Código | Significado | Repetir resolve? | O que fazer |
|---|---|---|---|
| 200/201/202 | sucesso | — | guarde o id devolvido |
| 207 | lote com falha parcial | — | seção 6 |
| 400 | dado inválido (a resposta traz a mensagem; às vezes `issues[]` com `path`/`message`) — ou DELETE com vínculos | não | corrigir o corpo |
| 401 | chave/token rejeitado (`rbt_`: "Token de integração inválido, revogado ou expirado."; `rbk_`: "Chave de API inválida ou expirada.") ou sem cabeçalho ("Token não fornecido.") — **medido 22/11/2026**. **Exceto** nas rotas com defeito ([defeitos-conhecidos.md](defeitos-conhecidos.md)) | não | parar; [FAQ F003](../faq-ias/F003-chave-recusada.md) |
| 403 | sem a permissão da rota (em `escopoFaltante`); ou `COLABORADOR_INATIVO` | não | liberar só a permissão necessária — [FAQ F008](../faq-ias/F008-403-escopo-faltante.md) |
| 404 | id não existe nesta clínica/ambiente | não | conferir o id (homologação ≠ produção) |
| 409 | já existe (CNPJ, CPF, nome de local/depósito/equipamento, login, conta com o mesmo número, conflito de grade); `ITEM_EM_USO_EM_SERVICOS` (produto/taxa em serviço ativo — F007); `version` velha (§4.4); `ORCAMENTO_CANCELAR_CONFIRMAR` (F010) | não | buscar pelo GET e **reutilizar** o id; nos outros, ver a FAQ |
| 422 | referência inválida/inativa (quase sempre ordem de implantação; depósito inativo recusa movimento de estoque); status automático de orçamento (F010) | não | criar/ativar o pré-requisito — [ordem-de-carga-via-api.md](ordem-de-carga-via-api.md) |
| 429 | lote em andamento; ou limite do token `rbt_` (**300 requisições/min**, "Limite de requisições do token excedido") ou do IP (1.200/min) — limites lidos no código `deploy_prd` em 22/11 (`rateLimitTokenIntegracao.ts`, commit `d20d4be2`); **não** documentados no Swagger | sim, depois de esperar | um lote por vez; não paralelizar leituras em massa |
| 500 | erro do servidor — desde 10/10/2026 a mensagem técnica vira "Ocorreu um erro inesperado… (código xxx)" | às vezes | reler para ver se gravou; buscar na FAQ pela **rota e status** (o texto técnico não chega mais); guardar o código |
| 503 | serviço do Rabi indisponível (falha real da validação/rede). **Até 25/09/2026** era a resposta para chave não aceita; medido em 22/11: já é 401 | uma vez | depois parar e avisar; não é a chave |

Corpo de erro: `{ "error": "mensagem" }`.

## 7b. Mudanças de 28/09/2026 (correção geral da API externa, em produção às 17:43 de Brasília)
Fonte: commit `4a79cab7` (antes citado como `c73e84de`; a história do `deploy_prd` foi reescrita) do rabi-api ("campos opcionais omitidos pela API externa quebravam ou
gravavam dados errados"), no `deploy_prd` de 28/09 20:43 UTC, + Swagger de 28/09 (snapshot
`spec/openapi-2026-09-28.json`, 269 operações).
- **Campo opcional omitido não derruba mais a rota** (antes: 500 `TypeError` ou 400 genérico) em
  serviço, produto, taxa, equipamento, colaborador (e login), grades, convênio, empresa, local,
  depósito, operadora, parâmetros, paciente, agendamento, orçamento, atendimento,
  pré-faturamento, fornecedor e fabricante. Continue mandando o corpo completo (ritual).
- **Serviço:** `produtoIds`, `equipamentoIds` e `servicosRelacionados` aceitam **ID puro ou objeto**
  (`{id, quantidade, valorUnitario}` · `{id}` · `{servicoId, quantidade}`); taxas vão em
  **`servicoTaxa: [{taxaId, quantidade}]`** (saíram `taxaServicoId`/`valorTaxaServico`).
- **Estoque:** saída e transferência exigem **`lote`** (mande `null` para produto sem lote); antes, sem
  lote, o Rabi usava um lote qualquer.
- **Leituras mais completas:** `GET /servicos/{id}` traz `especialidadesId` e subserviços;
  `GET /convenios/{id}` traz `unidadesIds` e `politicasPorTipoProduto` (confira contra a régua).
- **Farol:** o Swagger agora descreve os campos reais; rota nova
  `GET /convenios/{id}/farol/itens/{servicoRaizId}` (árvore de **um** serviço, sem paginação).
- **401 só é chave:** o Rabi parou de transformar em 401 qualquer erro com a palavra "token"
  (ex.: token obrigatório do convênio).
- **Gravações que antes saíam erradas sem aviso — confira o que foi gravado ANTES dessa hora:**
  ver [FAQ F006](../faq-ias/F006-conferir-gravacoes-anteriores-a-28-09.md).

## 7c. Mudanças de 01/10 a 22/11/2026 (resumo)

PUT parcial (§4), 401 para chave rejeitada (§7), 403 com `escopoFaltante`, 409 de produto/taxa em
serviço, controle de versão opcional (§4.4), limite de 300 req/min por token `rbt_`, `pageSize` > 200
reduzido em silêncio, mensagem de 500 genérica com código, `GET /servicos/{id}` completo (produtos,
equipamentos, taxas, documentos), EAN/NCM/código do produto como texto, rotas novas de financeiro.
Visão completa e o que mudou nas telas: [../sistema-rabi/novidades-out-nov-2026.md](../sistema-rabi/novidades-out-nov-2026.md).

## 8. Idempotência

- **Antes de criar, procure** (GET com filtro por nome/CNPJ/CPF/código) e reutilize.
- Mantenha no repo da clínica um mapa **"id de origem → id Rabi"**, atualizado a cada
  `201`/`CRIADO` — é o que torna a carga retomável.
- `POST /nfse/notas` é idempotente pelo cabeçalho `Idempotency-Key` (ou campo
  `chaveIdempotencia`).
- `PUT /atendimentos/{id}` aceita `version` (trava otimista).
- Efeitos externos **não se desfazem por reenvio**: emitir NFS-e, criar agendamento
  (consome o limite do plano), movimentação financeira (pode emitir NFS-e), criar login.
