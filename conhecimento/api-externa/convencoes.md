# Convenções da API externa (paginação, envelope, valores, PUT, DELETE, lotes, erros)

> **Fonte:** https://www.rabisistemas.com.br/manual/api-externa/index.html#convencoes (#paginacao, #valores, #put, #delete, #lotes, #codigos) · https://www.rabisistemas.com.br/manual/api-externa/erros-e-boas-praticas.html#armadilhas · Swagger (seção "Convenções gerais", snapshot `spec/openapi-2026-09-25.json`) · experiência de implantação real (24/09/2026) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger de 25/09/2026) · **Kit:** v0.1.0

O `ferramentas/rabi_api/cliente.py` já aplica quase tudo isto. Este arquivo explica o
porquê, para você não errar quando precisar sair do caminho feliz.

## 1. Paginação

| Regra | Valor |
|---|---|
| `page` | começa em **1**. `page=0` → **400** (`"Too small: expected number to be >0"`) |
| `pageSize` | padrão **50**, máximo **200** (acima → 400) nas rotas que declaram limite |
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

**Padrão (o Swagger de 25/09/2026 afirma que é único em toda listagem):**

```json
{ "dados": [ ... ], "page": 1, "pageSize": 50, "total": 123, "totalPages": 3 }
```

**Formatos antigos que o cliente ainda aceita** (medidos em produção em 24/09; o manual diz
que as 4 rotas foram normalizadas em 25/09/2026 — o cliente continua aceitando os dois,
por segurança):

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

## 4. PUT e PATCH — na dúvida, é sobrescrita

Regra do Swagger (25/09/2026): "o comportamento só está confirmado nos recursos cuja
descrição diz isso explicitamente; para qualquer outro PUT, trate como se sobrescrevesse
tudo". Regra do kit: **GET antes → altere só o que muda → reenvie o objeto COMPLETO**,
salvo nas rotas marcadas como upsert abaixo. Atenção: a **leitura nem sempre traz o que
a escrita exige** (nomes diferentes, objetos aninhados em vez de IDs, campos ausentes).
Para `/servicos` e `/produtos` use o conversor `ferramentas/rabi_api/corpo_escrita.py`;
para `/convenios/{id}` veja a linha da tabela 4.2. São 53 rotas PUT/PATCH (classificação feita
lendo a descrição de cada uma no spec atual).

**4.1 Declaram upsert / "omitido mantém" (7)**

| Rota | Comportamento |
|---|---|
| `PUT /convenios/{id}/servicos` | upsert por `servicoId`; omitido mantém; `valorInternoConvenio: null` limpa |
| `PUT /convenios/{id}/taxas` | upsert por `taxaId`; omitido mantém; `valorConvertido: null` limpa |
| `PUT /convenios/{id}/produtos` | upsert por `produtoId`; omitido mantém; `valorUnitarioConversao`/`fatorK: null` limpam |
| `PUT /convenios/{id}/colaboradores` | upsert; omitido mantém; listas de especialidades **aditivas** (nunca remove — remover só pela tela) |
| `PUT /convenios/{id}/especialidades` | upsert por `especialidadeId`; omitido mantém |
| `PUT /parametros/desconto` | campo omitido não altera |
| `PATCH /parametros/servicos-online/textos-informativos` | omitido fica inalterado |

`PUT /convenios/{id}/planos` fica **fora** deste grupo: o spec só diz "upsert por
`planoId`, idempotente" e não fala de campo omitido. Mande o item completo, com
`utiliza` sempre.

`PUT /parametros/financeiro` é **misto**: os 3 campos numéricos omitidos ficam como estão,
mas omitir (ou mandar `0`, `""`, `false`) em `categoriaPagamentoId`/`centroDeCustoId`
**grava null**. Mande sempre os dois.

**4.2 Declaram sobrescrita / substituição (6)**

| Rota | O que acontece |
|---|---|
| `PUT /servicos/{id}` | sobrescreve — omitido **não é preservado** (inclusive composição, especialidades, valor) |
| `PUT /pacientes/{id}` | sobrescreve os dados cadastrais |
| `PUT /convenios/{id}` | substitui: `empresaId` e `unidadesIds` obrigatórios (unidade fora da lista é desativada); omitir `operadoraId` **remove** a operadora; omitir `dataFim`/`dataReajuste`/`dataRenovacao` **limpa**; omitir `exigirToken` grava `false`; `politicasPorTipoProduto`, se enviado, é a lista completa. **O `GET /convenios/{id}` não devolve esses campos** (só `id`, nomes, `cnpj`, `descricao`, `codigoANS`, `codigo`, `dataInicio`, `empresaPrincipalId`, `operadoraId`, `ativo`, datas de registro): monte o objeto completo a partir da régua contratual e do dicionário de IDs do repo da clínica e confira na tela antes e depois |
| `PUT /empresas/{id}` | substitui o cadastro inteiro |
| `PUT /operadoras/{id}` | as listas `plano` e `contato` são sincronizadas: o que não vier é **removido** |
| `POST /atendimentos/prontuario` | sobrescreve o texto sem guardar versão anterior |

**4.3 Não declaram → trate como sobrescrita (39)**

`PUT /locais/{id}` · `PUT /pacientes/{id}/convenios/{vinculoId}` · `PUT /colaboradores/{id}` ·
`PUT /produtos/{id}` · `PUT /equipamentos/{id}` · `PUT /taxas/{id}` · `PUT /fornecedores/{id}` ·
`PUT /fabricantes/{id}` · `PUT /depositos/{id}` · `PUT /grades-colaborador/{id}` (corpo é
**lista direta**; o `{id}` do caminho é ignorado — cada item leva o seu `id`) ·
`PUT /grades-equipamento/{id}` · `PUT /financeiro/movimentacoes/{id}` · `PUT /tabelas-preco/{id}` ·
`PUT /nfse/tomadores/{id}` · `PUT /nfse/notas/{id}/tomador` · `PATCH /agendamentos/{id}/cancelar` ·
`PUT /orcamentos/{id}` · `PUT /orcamentos/status/{idOrcamento}/{idStatus}` ·
`PUT /faturamento/guias/{servicoAtendimentoId}` · `PUT /faturamento/guias/{guiaMae}/confirmar` ·
`PUT /faturamento/glosas/produto` · `PUT /faturamento/glosas/taxa` · `PUT /faturamento/glosas/servico` ·
`PUT /atendimentos/{id}` · `PUT /parametros/orcamento` · `PUT /parametros/estoque` ·
`PUT /parametros/avisos/{chave}` · `PUT /parametros/acolhimento` ·
`PATCH /parametros/servicos-online/habilitar` · `PATCH /parametros/servicos-online/agendamento/habilitar` ·
`PATCH /parametros/servicos-online/agendamento/mudanca-colaborador/habilitar` ·
`PATCH /parametros/servicos-online/confirmacao/habilitar` · `PATCH /parametros/servicos-online/prontuario/habilitar` ·
`PATCH /parametros/servicos-online/lista-medico-convenio/habilitar` ·
`PUT /parametros/servicos-online/agendamento/perguntas/{id}` · `PUT /parametros/termo` ·
`PUT /parametros/dashboard-permissoes/graficos` · `PUT /parametros/dashboard-permissoes/dashboards` ·
`PUT /parametros/dashboard-atribuicao`.

Lição de implantação real: um PUT parcial em `/servicos/{id}` apagou o valor e a
especialidade de um serviço. Por isso o ritual sempre tem foto antes e depois.

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
| 401 | chave rejeitada (ausente, errada, vencida, revogada) — **exceto** nas rotas com defeito ([defeitos-conhecidos.md](defeitos-conhecidos.md)) | não | parar; ver [chave-e-token.md](chave-e-token.md) |
| 403 | chave sem a permissão da rota | não | pedir a permissão |
| 404 | id não existe nesta clínica/ambiente | não | conferir o id (homologação ≠ produção) |
| 409 | já existe (CNPJ, CPF, nome de local/depósito/equipamento, login, conflito de grade) | não | buscar pelo GET e **reutilizar** o id |
| 422 | referência inválida/inativa (quase sempre ordem de implantação) | não | criar/ativar o pré-requisito — [ordem-de-carga-via-api.md](ordem-de-carga-via-api.md) |
| 429 | lote em andamento | sim, depois de esperar | um lote por vez |
| 500 | erro do servidor | às vezes | reler para ver se gravou (há rotas que gravam e devolvem 500) |
| 503 | falha ao validar a chave — e, medido em 25/09/2026, **ainda a resposta para chave inexistente** (medição única em 25/09, reconfirmar) | uma vez | depois parar e tratar como problema de chave |

Corpo de erro: `{ "error": "mensagem" }`.

## 8. Idempotência

- **Antes de criar, procure** (GET com filtro por nome/CNPJ/CPF/código) e reutilize.
- Mantenha no repo da clínica um mapa **"id de origem → id Rabi"**, atualizado a cada
  `201`/`CRIADO` — é o que torna a carga retomável.
- `POST /nfse/notas` é idempotente pelo cabeçalho `Idempotency-Key` (ou campo
  `chaveIdempotencia`).
- `PUT /atendimentos/{id}` aceita `version` (trava otimista).
- Efeitos externos **não se desfazem por reenvio**: emitir NFS-e, criar agendamento
  (consome o limite do plano), movimentação financeira (pode emitir NFS-e), criar login.
