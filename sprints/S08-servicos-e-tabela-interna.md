# S08 — Serviços (subserviços antes) e tabela de preço interna

> **Fonte:** https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-8 · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-8 · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-9b · https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#servico-niveis · spec `openapi-2026-09-25.json` (`POST /servicos`, `PUT /servicos/{id}`, `POST /tabelas-preco`, `/tabelas-preco/produtos/bulk`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (regra única do serviço composto em produção desde 23–24/09/2026) · **Kit:** v0.1.0

## Objetivo

O catálogo de serviços existe uma vez só, com código, tipo, duração, valor da
casa e a **composição** (subserviços, produtos, taxa, equipamentos) certa; e a
tabela de preço interna (que é **preço de produto**) está montada antes dos
convênios.

## Link do manual

- Etapa 8: https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-8
- Tela de serviços: https://www.rabisistemas.com.br/manual/modulos/configuracoes.html#servicos
- Tela da tabela interna: https://www.rabisistemas.com.br/manual/modulos/configuracoes.html#tabela-precos
- Serviço composto: https://www.rabisistemas.com.br/manual/precos/index.html#servico-composto
- Pela API: https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-8 e #passo-9b

## Depende de

S03 (tipos), S05 (taxas), S06 (produtos), S07 (equipamentos). Especialidades
(catálogo) só existem na tela: anotar os IDs antes (S00 — IDs só na tela).

## Documentos a pedir

FA-1 (serviços), FA-6 (composição e preço fechado), CV-7 (preços do particular —
só como informação; o preço cobrado do particular sai do convênio "Particular",
S10), CV-2 (códigos TUSS usados pelos convênios), SA-3.

## Índice de dados a coletar

### Serviço

| dado | campo API | obrigatório? | onde costuma estar no material do cliente | padrão sugerível | pergunta ao usuário se faltar |
|---|---|---|---|---|---|
| Nome | `nome` | sim | lista de serviços, tabelas | — | — |
| Descrição | `descricao` | sim | idem | igual ao nome | — |
| Código interno | `codigo` | não | sistema anterior | — | — |
| Código TUSS | `codigoTUSS` | não (recomendado p/ convênio) | tabelas dos convênios, guias | pelas referências TUSS | "Qual o código TUSS da <consulta>? Se não souber, eu procuro e te mostro." |
| Tipo de serviço | `tipoServicoId` | não (recomendado) | classificação | pelo nome | — |
| Tipo de código / Tabela 87 | `tipoCodigoId`, `tabelaANS87ID` | não | tabelas | TUSS | — |
| Tipo de guia / Regime | `tipoGuiaId`, `regimeDeAtendimentoId` | não | guias TISS | consulta → guia de consulta; demais → SP/SADT (confirmar) | — |
| Tipo de atendimento | `tipoAtendimento` (ID) | não | — | — | — |
| Duração (min) | `tempoServico` | não (recomendado) | escala, agenda | consulta **30**, retorno **15** (confirmar) | "Quanto tempo dura uma <consulta> na agenda?" |
| Valor da casa (R$) | `valor` | não | lista de serviços | nenhum | "Qual o valor de referência da <consulta> no cadastro?" |
| Definir preço pelos itens | `somarItems` (na leitura: `somarItens`) | não | FA-6 | ligado em serviço de medicamento que soma aplicação + medicamento | "O preço deste serviço é a soma do que vai dentro dele?" |
| Especialidades | `especialidadesId` (IDs) | não | lista de profissionais | — | — |
| Subserviços | `servicosRelacionados` (IDs já criados) | não | FA-6 | — | "O que acontece dentro do <serviço>? (ex.: aplicação + medicamento)" |
| Produtos | `produtoIds` | não | FA-6 | — | — |
| Taxa do serviço | `taxaServicoId` + `valorTaxaServico` | não | FA-6 | — | — |
| Equipamentos | `equipamentoIds` | não | FA-5 | — | — |
| Agendamento online | `habilitarAgendamentoOnline`, `apenasComColaboradorDesignado` | não | — | desligado | — |
| Preparo | `preparo`, `preparamentos`, `linkAuxiliar` | não | orientações ao paciente | — | — |

### Tabela de preço interna (preço de **produto**)

| dado | campo API | obrigatório? | onde costuma estar | padrão sugerível | pergunta se faltar |
|---|---|---|---|---|---|
| Nome da tabela | `name` | sim | — | "Tabela Interna" | — |
| Nome do Preço 1 | `priceType1` | sim | — | "Preço de venda" | — |
| Nomes dos Preços 2 e 3 | `priceType2`, `priceType3` | não | — | — | — |
| Preço do produto | `precos[]`: `purchasePriceSourceId` (ID da tabela), `productId`, `priceType1..3` | sim (ID da tabela e produto) | lista de preços, notas + margem da clínica | nenhum | "A clínica tem uma tabela própria de preço dos medicamentos? Ou os convênios usam Brasíndice/SIMPRO?" |

A tabela interna **não** define o preço da consulta particular: esse sai do
convênio "Particular" (S10). Se a tabela não tiver o produto, vale o "Preço de
venda tabela".

## Fila de perguntas

1. Confirmar a lista de serviços (em bloco; dúvidas uma a uma).
2. Quais serviços têm **coisas dentro** (composição)? Para cada um: o quê.
3. Quais são **preço fechado** em algum convênio? (anotar para a S10b — pacote
   é marcado no convênio, não aqui).
4. Duração padrão (sugerir) e valor da casa (pedir; nunca sugerir).
5. A clínica usa tabela interna de produtos? Se não: tabela interna `n/a`.

## Enriquecimento possível

- **Código TUSS** pelas referências do kit (`referencias/tuss/`) e pelas tabelas
  dos convênios; mostrar candidatos.
- Montagem automática da árvore de composição a partir de FA-6 (subserviços
  identificados primeiro).
- Simulação do valor antes de gravar: `ferramentas/conversao/simulador.py`
  (prevê o valor do serviço composto com as regras vigentes).

## Leitura do que já existe no Rabi e regra de não perder nada

- `GET /servicos` (resumida) e `GET /servicos/{id}` (composição completa) —
  casar por código TUSS, código interno e nome normalizado.
- Serviço existente: **GET completo antes de qualquer mudança**; o PUT sobrescreve.
- Serviços duplicados (mesma consulta cadastrada duas vezes) são sintoma de
  cadastro repetido: resolver com o dono **antes** dos convênios.

## Gravação

| Ordem | Rota | Permissão | Lote |
|---|---|---|---|
| 1 | Subserviços (ex.: "Aplicação endovenosa"): `POST /servicos` | `servico:create` | um por um até o 1º provado; depois `/servicos/bulk` (50) |
| 2 | Serviços simples (consultas, exames) | idem | idem |
| 3 | Serviços pais/compostos, com `servicosRelacionados`, `produtoIds`, `taxaServicoId` | idem | um por um no começo |
| 4 | `POST /tabelas-preco` (`name`, `priceType1`) | `tabelaPreco:create` | — |
| 5 | `POST /tabelas-preco/produtos/bulk` (chave `precos`) | `tabelaPreco:update` | até 200; é upsert |
| Correção | `GET /servicos/{id}` → alterar → `PUT /servicos/{id}` **objeto completo** | `servico:update` | — |

Exemplo fictício de composto (subserviço 46 e produto 120 já criados):
`{"nome":"Medicamento X aplicado EV","descricao":"Medicamento X aplicado EV","somarItems":true,"produtoIds":[120],"servicosRelacionados":[46]}`

**O que `somarItems` decide (regra vigente):** só o **valor próprio** do serviço
(zero quando marcado). Ele **não** decide se os itens entram: taxas, produtos e
subserviços com Utiliza no convênio **sempre** entram na conta do serviço, cada
um com a sua conversão. Detalhes em `conhecimento/precos-e-conversao/` do kit e
em https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#regra-unica.

## Prova

- `provas/S08/servico-<codigo>/` com `depois.json` = `GET /servicos/{id}`
  (mostra a composição completa e `somarItens`).
- Review: árvore de cada composto (pai → subserviços → produtos/taxas), com
  nomes; contagem esperado × gravado.
- Tabela interna: `GET /tabelas-preco`, `GET /tabelas-preco/produtos?id=<id>`,
  `GET /tabelas-preco/precificacao`.

## Armadilhas desta sprint

- **Pai antes do filho:** não dá para apontar ID que não existe; corrigir depois
  exige PUT completo.
- **PUT /servicos/{id} sobrescreve tudo.** Numa implantação real, um serviço
  perdeu valor e especialidade por um PUT parcial.
- **Nome de escrita ≠ nome de leitura:** escreve-se `somarItems` e
  `especialidadesId`; a leitura devolve `somarItens` (e as especialidades em
  outra estrutura). Nome errado apaga o campo em silêncio.
- **Pacote não existe no cadastro do serviço:** é marcado por convênio (S10b).
- **Serviço de aplicação × serviço de medicamento:** a aplicação costuma ter
  valor fixo (sem somar itens); o serviço "medicamento X aplicado" soma a
  aplicação (subserviço) + o medicamento. Confirme o modelo com o dono.
- Tabela interna **não** é preço de consulta particular.
- `GET /tabelas-preco` já devolveu lista sem o envelope padrão: não presuma o formato.

## Definition of Ready / Definition of Done

**DoR:** S05 e S06 conferidas; IDs de especialidades anotados; FA-1 recebido.

**DoD:**
- [ ] todo serviço existe uma vez só; compostos com a árvore certa (GET completo);
- [ ] subserviços criados antes dos pais;
- [ ] tabela interna montada (ou `n/a` com motivo);
- [ ] modelo de cobrança de cada composto anotado para a S10b;
- [ ] IDs no dicionário; provas salvas.

## Checklist de itens

| # | item | status | origem | prova | observação |
|---|---|---|---|---|---|
| S08-01 | Lista de serviços extraída (com origem) | pendente | | | |
| S08-02 | Duplicatas resolvidas | pendente | | | |
| S08-03 | Composições levantadas (FA-6) | pendente | | | |
| S08-04 | Subserviços gravados e conferidos | pendente | | provas/S08/ | |
| S08-05 | Serviços simples gravados e conferidos | pendente | | | |
| S08-06 | Serviços compostos gravados e conferidos (árvore) | pendente | | | |
| S08-07 | Tabela interna criada (ou n/a) | pendente | | | |
| S08-08 | Preços de produto na tabela interna | pendente | | | |
| S08-09 | Serviços de preço fechado anotados para a S10b | pendente | | | |
| S08-10 | Dicionário de IDs (servicoId, tabela interna) | pendente | | | |

## O que registrar

- `dados/catalogo/servicos.csv` e `dados/catalogo/composicao.md` (árvores).
- `decisoes/DECISOES.md`: modelo de cobrança de aplicações e medicamentos.
- `ESTADO.md`: próximo passo = S09.
