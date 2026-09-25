# S10a — Convênio: dados (fase 1)

> **Fonte:** https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#convenio-fase-1 · https://www.rabisistemas.com.br/manual/modulos/configuracoes.html#convenios-campos · https://www.rabisistemas.com.br/manual/precos/guia-clinica.html#aba-dados-convenio · spec `openapi-2026-09-25.json` (`POST /convenios`, `PUT /convenios/{id}`) · leitura real (GET) da API de produção em 25/09/2026 · **Conferido em:** 2026-09-25
> **Vale para:** produção · **Kit:** v0.1.0

## Objetivo

O convênio da vez existe com os dados do **contrato lido de verdade**, cláusula
por cláusula: vigência, prazos, reajuste, fator K, unidades onde vale e a
**política de preço por tipo de produto** — pronto para receber os preços na S10b.
Um arquivo destes é executado **para cada convênio**, um por vez.

## Link do manual

- Fase 1 pela API: https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#convenio-fase-1
- Campos da tela: https://www.rabisistemas.com.br/manual/modulos/configuracoes.html#convenios-campos
- Aba de dados (guia da clínica): https://www.rabisistemas.com.br/manual/precos/guia-clinica.html#aba-dados-convenio
- Política e Fator K: https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#produto-cadeia

## Depende de

S04 (operadora e planos), S01 (`empresaId` e unidades). Para a política:
tipos de produto (S03) e a fonte de preço (tabela interna da S08, ou fonte de
compra — ver abaixo).

## Documentos a pedir

CV-1 (contrato e aditivos), CV-3 (regra de materiais e medicamentos), CV-4
(dados da operadora), CV-5 (planos). O método de leitura do contrato está em
[../conhecimento/precos-e-conversao/10-do-contrato-a-configuracao.md](../conhecimento/precos-e-conversao/10-do-contrato-a-configuracao.md).

## Índice de dados a coletar

| dado | campo API | obrigatório? | onde costuma estar no material do cliente | padrão sugerível | pergunta ao usuário se faltar |
|---|---|---|---|---|---|
| Descrição (nome do convênio no Rabi) | `descricao` | sim | capa do contrato | "<Operadora> — <produto/plano>" | "Como a equipe chama este convênio no dia a dia?" |
| Data de início da vigência | `dataInicio` | sim | cláusula de vigência | — | "Desde quando vale o contrato com o <convênio>?" |
| Empresa principal | `empresaId` | sim | S01 | a matriz | — |
| Unidades onde é aceito | `unidadesIds` | sim | cláusula de abrangência | todas as unidades | "O <convênio> vale em todas as unidades da clínica?" |
| Operadora | `operadoraId` | não (recomendado) | S04 | — | — |
| CNPJ | `cnpj` | não no simples; **sim no `/bulk`** (único na clínica) | qualificação das partes | o da operadora | — |
| Registro ANS | `registroANS` (criação) / `codigoANS` (atualização) | não | capa, rodapé, carteirinha | o da operadora | — |
| Nome fantasia / razão social | `nomeFantasia`, `razaoSocial` | não | contrato | — | — |
| Fim / renovação / reajuste | `dataFim`, `dataRenovacao`, `dataReajuste`, `prazoReajuste` | não | cláusulas de vigência e reajuste | — | "O contrato tem data de reajuste? Por qual índice?" |
| Prazo de pagamento (dias) | `prazoPagamento` | não | cláusula de pagamento | — | "Em quantos dias o <convênio> paga depois de receber as guias?" |
| Prazo de retorno sem nova cobrança (dias) | `prazoRetorno` | não | cláusula de consulta/retorno | — | "Em quantos dias o retorno não é cobrado de novo?" |
| Prazo de entrega de guias (dias) | `prazoLimiteEntregaGuias` | não | cláusula de faturamento | — | — |
| Prazo de recurso de glosa / pagamento do recurso | `prazoRecursoGlosa`, `prazoPagamentoRecursoGlosa` | não | cláusula de glosa | — | "Quantos dias a clínica tem para recorrer de uma glosa?" |
| Prazo de autorização (dias) | `prazoAutorizacao` | não | cláusula de autorização | — | — |
| Fator K geral | `fatorK` (unidade e efeito **não confirmados**; o que vale no cálculo é o Fator K da política ou da linha) | não | anexo de materiais | — | "O contrato fala em fator K, inflator ou deflator? Qual o percentual?" |
| Exige token/senha do beneficiário | `exigirToken` | não | cláusula de elegibilidade | não | — |
| Faturado/pagamento | `faturadoPagamento` | não | — | — | sentido não confirmado: marcar pela tela e conferir |
| Parcelas máximas (particular) | `limiteParcelasConvenioParticular` | não | regra da clínica | — | "No particular, parcela em até quantas vezes?" |
| Contato | `pessoaDeContato`, `telefone`, `email`, `observacao` | não | preâmbulo, aditivos | — | — |
| Modelos de XML (consulta, SP/SADT) | `xmlConsultaId`, `xmlSpSadtId` | não | — | — | IDs só na tela |
| Kit de documentos padrão | `kitDocumentosPadrao.id` | não | — | — | ID só na tela (S14) |
| **Política por tipo de produto** | `politicasPorTipoProduto[]`: `tipoProdutoId`, `fatorK` (percentual, texto), `idJson` (JSON com `fontePrecoId` e `tipoPrecificacao`) | obrigatórios em cada item | CV-3 (ex.: "Brasíndice PMC + 10%", "SIMPRO PF − 5%") | uma linha para **cada** tipo de produto usado | "Os medicamentos do <convênio> são pagos por qual tabela e com qual percentual?" |

**Política por tipo de produto:** todos os tipos de produto que os produtos da
clínica usam precisam de política **em cada convênio** — inclusive subtipos
(ex.: um subtipo de medicamento herda a regra do medicamento, se o contrato não
disser outra). Sem política, o produto fica sem preço. A fonte de preço
(`fontePrecoId`) vem de `GET /tabelas-preco/precificacao`; confira a primeira
pela tela.

## Fila de perguntas

1. **As 4 perguntas que abrem tudo** (uma por vez): paga pacote fechado? conta
   aberta? preço fixo por procedimento? quais serviços são pacote e o que tem
   dentro? (as respostas vão para a S10b).
2. Confirmar a régua contratual extraída (mostrar cada prazo com a cláusula).
3. Pedir só o que faltou (uma pergunta por mensagem).
4. Política de materiais e medicamentos (tabela + percentual por tipo).
5. Unidades onde vale.

## Enriquecimento possível — a IA propõe, não só transcreve

Ao ler o contrato, a IA escreve observações em `ANALISE-CONTRATOS.md` do repo
da clínica e mostra na review:

- prazo de glosa curto → o fluxo de recurso precisa estar pronto antes do go-live;
- reajuste com data fixa → lembrete registrado (reajuste esquecido é receita perdida);
- autorização prévia obrigatória para um grupo de serviços → marcar na S10b;
- fator K do contrato × o que vai ser cadastrado;
- serviço previsto no contrato que a clínica não presta (oportunidade);
- serviço que a clínica presta e não está no contrato (risco de glosa — aditivo?);
- proposta comercial não assinada **não** é contrato.

Detalhe do método: [../conhecimento/negocio-clinica/analise-de-contratos.md](../conhecimento/negocio-clinica/analise-de-contratos.md).

## Leitura do que já existe no Rabi e regra de não perder nada

- `GET /convenios` e `GET /convenios/{id}` — casar por CNPJ e descrição.
- Existe → diagnóstico NOVO / EM ANDAMENTO / FECHADO (modo Convênio). Corrigir =
  partir do `GET /convenios/{id}` real (traz datas, prazos, `exigirToken`,
  `faturadoPagamento`, `operadoraId`), **completar** o que ele não traz
  (`unidadesIds`, `politicasPorTipoProduto`, `fatorK`) a partir de
  `dados/convenios/<slug>/regua-contratual.md` + `dados/dicionario-de-ids.md`,
  converter os nomes de leitura para os de escrita e enviar o PUT (ver armadilhas).

## Gravação

| Ordem | Rota | Permissão | Lote |
|---|---|---|---|
| 1 | `POST /convenios` | `convenio:create` | um por vez (o `/bulk`, até 50, só com ordem escrita e depois do 1º provado) |
| Correção | GET real + (unidades, políticas, fatorK) da régua + dicionário, nomes convertidos para a escrita → `PUT /convenios/{id}` | `convenio:update` | — |

Exemplo fictício: `{"descricao":"Operadora Exemplo — Empresarial","dataInicio":"2026-10-01T00:00:00.000Z","empresaId":"<id>","unidadesIds":[<id>],"operadoraId":"<id>","prazoPagamento":30,"prazoRetorno":30}`

- 409 = CNPJ já existe; 422 = empresa, operadora ou kit não encontrado.
- Guardar `convenioId` no dicionário e em `dados/convenios/<slug>/`.

## Prova

- `provas/S10/<slug>/dados/AAAAMMDD-HHMM/` com `depois.json` = `GET /convenios/{id}`
  e o print da tela de cadastro antes e depois (o GET não mostra tudo).
  Padrão de todo o convênio: `provas/S10/<slug>/{dados|<aba>-passe-N}/AAAAMMDD-HHMM/`.
- Review: tabela com cada campo gravado × cláusula de origem.

## Armadilhas desta sprint

- **`PUT /convenios/{id}` substitui o cadastro:** unidades fora da lista são
  **desativadas** no convênio; omitir `operadoraId` remove a operadora; omitir
  datas (`dataFim`, `dataReajuste`, `dataRenovacao`) as limpa; omitir `exigirToken`
  grava `false`; `politicasPorTipoProduto`, quando enviado, é a lista **completa**.
- **O `GET /convenios/{id}` real traz datas, prazos, `exigirToken` e
  `faturadoPagamento` — use-o como base; mas `unidadesIds` e
  `politicasPorTipoProduto` NÃO vêm** (nem `fatorK`). Medido em produção em
  25/09/2026: além do Swagger (que só lista o resumo), a resposta real traz
  `dataFim`, `dataReajuste`, `dataRenovacao`, `prazoAutorizacao`,
  `prazoLimiteEntregaGuias`, `prazoPagamento`, `prazoPagamentoRecursoGlosa`,
  `prazoReajuste`, `prazoRecursoGlosa`, `prazoRetorno`, `exigirToken`,
  `faturadoPagamento`, `limiteParcelasConvenios`, `email`, `telefone`,
  `pessoaDeContato`, `observacao`, `kitDocumentosId`, `xmlConsultaId`,
  `xmlSpSadtId`. Reenviar o GET sem completar **desativa todas as unidades e
  apaga as políticas**. Complete `unidadesIds` e `politicasPorTipoProduto`
  (lista completa) da régua + `dados/dicionario-de-ids.md`, e **confira os nomes
  de leitura × escrita no schema `ConvenioUpdate` antes de reenviar**:
  `empresaPrincipalId` → `empresaId`; `kitDocumentosId` → `kitDocumentosPadrao`
  e `limiteParcelasConvenios` → `limiteParcelasConvenioParticular` (provável, não
  confirmado); tire `id`, `ativo`, `createdAt`, `updatedAt`, `markup`,
  `perfilFiscalId`, `kitDeProdutosId`, `photoConvenio`. **Confira na tela antes e
  depois** (print da tela de cadastro do convênio na prova).
- Registro ANS: `registroANS` na criação, `codigoANS` na atualização.
- `empresaId` e `operadoraId` são **texto** no schema; `unidadesIds` é lista de números.
- `fatorK` do cadastro do convênio: unidade e efeito **não confirmados** (o spec
  só traz o exemplo `1.1`). O Fator K que vale no cálculo é o da política por
  tipo de produto ou o da linha, que é **percentual** ("10" = +10%).
- Política salva vazia apaga a política — nunca envie a lista incompleta.
- Datas com hora em UTC (`…T00:00:00.000Z`): confira o dia gravado.

## Definition of Ready / Definition of Done

**DoR:** operadora existe (S04); CV-1 do convênio recebido ou lacuna aceita por escrito.

**DoD:**
- [ ] convênio existe, relido; campos obrigatórios preenchidos;
- [ ] cada prazo com a cláusula anotada (`regua-contratual.md`);
- [ ] política por tipo de produto para **todos** os tipos usados;
- [ ] respostas das 4 perguntas registradas para a S10b;
- [ ] análise do contrato escrita; provas salvas.

## Checklist de itens

| # | item | status | origem | prova | observação |
|---|---|---|---|---|---|
| S10a-01 | Régua contratual montada (com cláusulas) | pendente | | | |
| S10a-02 | As 4 perguntas de cobrança respondidas | pendente | | | |
| S10a-03 | Dados obrigatórios confirmados | pendente | | | |
| S10a-04 | Prazos confirmados | pendente | | | |
| S10a-05 | Política por tipo de produto definida (todos os tipos) | pendente | | | |
| S10a-06 | Convênio gravado e conferido | pendente | | provas/S10/<slug>/dados/ | |
| S10a-07 | Análise do contrato escrita | pendente | | | |

## O que registrar

- `dados/convenios/<slug>/regua-contratual.md` e `decisoes.md`.
- `ANALISE-CONTRATOS.md` (observações e sugestões).
- `decisoes/DECISOES.md`: modelo de cobrança do convênio.
- `ESTADO.md`: próximo passo = S10b deste convênio.
