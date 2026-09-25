# 10 — Do contrato à configuração: o método da IA

> **Fonte:** https://www.rabisistemas.com.br/manual/precos/guia-ia.html#arvore-de-decisao · https://www.rabisistemas.com.br/manual/precos/guia-ia.html#checklist-perguntas · https://www.rabisistemas.com.br/manual/precos/guia-ia.html#alg-api-pacote · https://www.rabisistemas.com.br/manual/precos/arvore-de-decisao.html#checklist · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#convenio-fase-1 · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#convenio-fase-2 · spec `../api-externa/spec/openapi-2026-09-25.json` (nomes de campo conferidos) · experiência real (generalizada) · **Conferido em:** 2026-09-25
> **Vale para:** produção desde 23–24/09/2026; regra "valor combinado não é pacote" vigente desde 25/09/2026 · **Kit:** v0.1.0

Este é o passo a passo que a IA segue para transformar o contrato e a tabela
de um convênio em configuração no Rabi. **Um convênio por vez**, do começo
ao fim, com prova. Nunca aplique a mesma regra a vários convênios numa
passada. Nunca compare um convênio com outro para decidir preço: cada
contrato é um contrato.

## 1. Fluxo

```
 documentos do convênio (contrato, aditivos, tabela, manual/informativos da operadora)
      │
 [1] RÉGUA CONTRATUAL ── vigência, reajuste, prazos, fator K, fontes de preço (cláusula de cada um)
      │
 [2] AS 4 PERGUNTAS ─── pacote fechado? conta aberta? preço fixo? quais serviços são pacote?
      │
 [3] FOTO ANTES ─────── GET convênio, abas, farol (paginando até o total) → provas/antes
      │
 [4] precos-<slug>.csv ─ uma linha por item, com ORIGEM (documento + página/linha)
      │
 [5] SIMULADOR ──────── prevê ✅, Σ e Farol de cada serviço; valida invariantes I1–I13
      │
 [6] PRÉVIA + APROVAÇÃO (item a item, grupos A/B/C)
      │
 [7] GRAVA em passes: política → Utiliza → valores → textos/códigos → tipo atend. → Pacote/Zerar
      │
 [8] FOTO DEPOIS + DIFF + FAROL (arquivo 13) → registra, commit, próximo convênio
```

## 2. Régua contratual

Leia o contrato **cláusula por cláusula** e monte a régua antes de olhar o
sistema. Cada linha com a **cláusula de origem**. Destino no cadastro do
convênio (`POST /convenios` na criação; `PUT /convenios/{id}` sobrescreve —
ver §8.1):

| O que está no contrato | Campo (API) | Observação |
|---|---|---|
| início da vigência | `dataInicio` (obrigatório) | cláusula de vigência |
| fim / renovação | `dataFim`, `dataRenovacao` | omitir no PUT **limpa** |
| data e periodicidade de reajuste | `dataReajuste`, `prazoReajuste` | reajuste esquecido = receita perdida em silêncio: propor lembrete |
| prazo de pagamento | `prazoPagamento` | dias |
| prazo de retorno sem nova cobrança | `prazoRetorno` | dias |
| prazo de entrega de guias | `prazoLimiteEntregaGuias` | dias |
| prazo de recurso de glosa | `prazoRecursoGlosa` | < 30 dias: avisar que o fluxo de recurso precisa estar pronto |
| prazo de pagamento do recurso | `prazoPagamentoRecursoGlosa` | |
| prazo de autorização prévia | `prazoAutorizacao` | |
| exige token do beneficiário | `exigirToken` | omitir no PUT grava `false` |
| parcelas (particular) | `limiteParcelasConvenioParticular` | |
| registro ANS | `registroANS` na criação · `codigoANS` na atualização | trocar os nomes perde o registro sem erro |
| política de material/medicamento por tipo | `politicasPorTipoProduto[]` | arquivo 04 §4 |
| "Pago no ato do atendimento" | campo de tela | **nome na API não confirmado** (o spec tem `faturadoPagamento`, semântica não documentada). Configure/confira pela tela |
| fator K do convênio | `fatorK` (numérico) | efeito no cálculo **não confirmado**; o FK que vale é o da política/linha |

### 2.1 Fonte de preço de material e medicamento — padrões de mercado

Contratos costumam dizer, por tipo de produto, **qual tabela** e **qual
percentual**. Padrões genéricos (confirme sempre no contrato daquele
convênio):

| Tipo de produto | Padrão comum de contrato | Como fica no Rabi |
|---|---|---|
| Materiais (hospitalar, perfurocortante) | **SIMPRO ± x%** | política do tipo: tabela interna com os valores SIMPRO, coluna correspondente, FK = ±x |
| Medicamentos (comuns) | **Brasíndice PMC** (às vezes ± x%) ou **PF + x%** | política: tabela, coluna PMC ou PF, FK = x |
| Medicamentos **restritos hospitalares** (sem PMC) | **Brasíndice PF + x%** | política do tipo "restrito": coluna PF, FK = x. Nunca "PMC" (item sem PMC não tem esse preço) |
| Imunobiológicos | às vezes negociado à parte (ex.: PF + x%) | política da categoria ou nível 3 do item |
| OPME / fora de tabela | **valor da nota fiscal + x%** (margem de comercialização) | nível 3 do item (valor unitário convertido) caso a caso; não há fonte "nota" automática |
| Edição congelada (ex.: "Brasíndice edição N/ano") | valores daquela edição | **outra tabela interna** e política apontando para ela |
| Preço fixo por item (anexo) | valor do anexo | nível 3 do item (valor unitário convertido) |

Nunca "complete" um percentual por dedução ou por média de outros
convênios. Sem cláusula → grupo **C** (lacuna) e pergunta à clínica.

## 3. As 4 perguntas que abrem tudo

Sem estas respostas, **não configure nada**:

1. **Este convênio paga por pacote fechado?** (um valor único que já inclui
   material, medicamento e/ou taxa)
2. **Paga conta aberta?** (cada item usado é cobrado à parte)
3. **Paga preço fixo por procedimento?** (e esse preço inclui algo?)
4. **Quais serviços são pacote** — e **o que está dentro** de cada pacote?

Pergunta modelo (uma por vez, ao usuário leigo):
> "No Convênio A, a aplicação de medicamento na veia é cobrada como um valor
> único que já inclui material e taxa (pacote), ou cada item é cobrado à
> parte (conta aberta)?"

Um convênio pode ser **misto** (alguns serviços pacote, outros conta aberta).
Registre a resposta por serviço.

## 4. Árvore de decisão: da resposta à configuração

### 4.1 Para cada serviço × convênio

```
1. O convênio atende este serviço?
     não → Utiliza = false. FIM.  (serviço sem Utiliza não pode ser agendado)
2. O preço é um valor FECHADO negociado (já inclui itens)?
     sim → valor_combinado = preço (inclusive 0 se contratado assim)
           Pacote = true  (OBRIGATÓRIO — valor combinado sozinho NÃO fecha pacote)
           para CADA item da composição, inclusive dentro de subserviços (Zerar não cascateia):
               incluso no preço → Zerar = true
               cobrado à parte  → Zerar = false
           o serviço que É o pacote: Zerar = false
     não → 3
3. O preço é "soma do que foi usado" (medicamento + aplicação…)?
     sim → catálogo: somar itens = true; valor_combinado vazio; Pacote = false;
           Utiliza = true em cada item/subserviço cobrado; preço de cada item pelos 3 níveis;
           valor extra do convênio sobre o serviço vai em UM lugar só
           (valor combinado da raiz OU no subserviço)
     não → 4
4. Preço fixo do serviço (valor próprio):
     igual ao da casa → valor_combinado vazio
     diferente        → valor_combinado = preço  (muda só a base — NÃO é pacote)
     a composição tem itens? eles ENTRAM por cima (desde 23/09/2026):
         todos cobrados à parte         → Pacote = false
         algum já incluso no preço fixo → Pacote = true + Zerar=true nos inclusos, false nos à parte
         item que o convênio não cobre  → Utiliza = false (custo sem receita) — decisão escrita
```

### 4.2 Para cada produto × convênio

```
preço específico no contrato (anexo, OPME)  → valor_combinado (valor unitário convertido) na aba Produtos
regra por tipo (tabela ± %)                  → política de nível 2 (não repetir item a item)
exceção de percentual só neste item          → fator_k da linha (e/ou fonte_preco/tipo_precificacao da linha)
nada no contrato                             → herda (política/cadastro) — confirmar com a clínica
o convênio não cobre                         → Utiliza = false
gratuito                                     → valor_combinado = 0
incluso em pacote fechado                    → Utiliza = true + Zerar = true
```

### 4.3 Para cada taxa × convênio

```
paga pelo valor da casa           → Utiliza = true; valor_combinado vazio
paga valor/código próprio         → Utiliza = true; valor_combinado; codigo/nome do contrato
inclusa em pacote fechado         → Utiliza = true; Zerar = true
o contrato não paga taxa          → Utiliza = false (decisão escrita)
```

### 4.4 Textos e códigos (todos os tipos)

- Case o item do contrato com o do catálogo **pelo nome/natureza**, nunca
  pelo código.
- Preencha nome/descrição/código/tabela 87/tipo de código **só onde difere**
  do cadastro. Nome e descrição = texto contratual (vai ao XML).
- Código próprio da operadora = conversão (nível 3), nunca item novo.
- Item que o contrato cobra e **não existe** no catálogo → lacuna (grupo C):
  cadastrar no catálogo é decisão da clínica (afeta todos os convênios).

## 5. Ordem de configuração dentro do convênio

1. **Dados do convênio** (fase 1): régua + **política por tipo de produto**.
2. **Planos** e **Especialidades** (`PUT /convenios/{id}/planos|especialidades`).
3. Nas abas **Taxas → Produtos → Serviços** (serviços por último, porque
   somam os outros), em **passes**:
   1. **Utiliza** (tudo que o convênio cobre; nada mais);
   2. **valores** (`valor_combinado`, `fator_k`, `fonte_preco`, `tipo_precificacao`);
   3. **textos e códigos** (`nome_convenio`, `descricao_convenio`, `codigo`,
      `tipo_codigo_id`, `tabela87_id`);
   4. **tipo de atendimento** (serviços), `autorizacao_previa`, `retorno`, `parcelas`;
   5. **Pacote e Zerar** por último (item por item, inclusive dentro de subserviços).
4. **Colaboradores** do convênio (fora desta pasta).
5. **Conferência pelo Farol** (arquivo 13).

Por que em passes: cada passe é verificável isoladamente (Utiliza muda a
receita; valores mudam o preço; Pacote/Zerar mudam o que entra). Um passe
pode ser **uma** chamada por aba (até 200 itens), respeitando **uma chamada
por vez por convênio**.

## 6. O arquivo `precos-<slug>.csv`

Fica no repo da clínica em `dados/convenios/<slug>/precos-<slug>.csv`. **Uma linha por item** (serviço, subserviço,
produto ou taxa) que precisa de alguma configuração neste convênio. É a fonte
da verdade que a ferramenta `ferramentas/conversao/montar_convenio.py` lê.

### 6.1 Formato

- UTF-8, **separador `;`**, 1ª linha = cabeçalho **exatamente** com os nomes
  abaixo, nesta ordem (21 colunas). Linhas começando com `#` são comentário.
- Decimal com **vírgula ou ponto**, sem separador de milhar (`1234,56` ou
  `1234.56`).
- Booleanos: `S` ou `N`. Vazio = **não enviar** (mantém o atual).
- Fichas grandes: fatiar (`precos-parte-001.csv`…) com índice.

### 6.2 Colunas

| # | Coluna | Obrig. | Vale para | Conteúdo | Vazio significa |
|---|---|---|---|---|---|
| 1 | `tipo` | sim | todos | `servico` · `produto` · `taxa` (subserviço = `servico`) | — |
| 2 | `id_rabi` | sim | todos | id do item no **catálogo** (`servicoId`/`produtoId`/`taxaId`) — nunca o id do vínculo | — |
| 3 | `nome_rabi` | sim | todos | nome no catálogo (conferência humana; a ferramenta confere com o GET e **para** se divergir) | — |
| 4 | `nome_convenio` | não | todos | nome convertido (texto contratual, vai ao XML) | não envia (mantém). `LIMPAR` = envia `""` (não confirmado se limpa) |
| 5 | `descricao_convenio` | não | todos | descrição convertida | idem |
| 6 | `codigo` | não | todos | código do item **neste convênio** | não envia |
| 7 | `tipo_codigo_id` | não | todos | id de `GET /auxiliares/tipos-codigo` | não envia |
| 8 | `tabela87_id` | não | todos | **id** do registro em `GET /auxiliares/tabelas-ans87` (não o código "20") | não envia |
| 9 | `tipo_atendimento_id` | não | servico | id de `GET /auxiliares/tipos-atendimento`; `LIMPAR` = `null` | não envia |
| 10 | `utiliza` | sim | todos | `S`/`N` — **sempre explícito** | (proibido vazio) |
| 11 | `valor_combinado` | não | todos | número (inclusive `0`): valor 🔁 do item | **envia `null`** = sem regra, desce de nível. `=` (sinal de igual) ou `manter` = não envia (mantém) |
| 12 | `pacote` | não | servico | `S`/`N` | não envia |
| 13 | `zerar` | sim* | todos | `S`/`N` (*obrigatório em vínculo novo) | não envia |
| 14 | `autorizacao_previa` | não | servico | `S`/`N` | não envia |
| 15 | `retorno` | não | servico | `S`/`N` | não envia |
| 16 | `fator_k` | não | produto | percentual (`10`, `-15`, `38,24`); `0` = sem ajuste | **envia `null`** = herda **só** quando o valor unitário convertido está vazio; com valor convertido na linha, `null` = sem ajuste (0%), **não** herda. `=` ou `manter` = não envia |
| 17 | `fonte_preco` | não | produto | id da fonte (`fontePrecoId` de `GET /tabelas-preco/precificacao`) | não envia (herda) |
| 18 | `tipo_precificacao` | não | produto | `PRECO_1` · `PRECO_2` · `PRECO_3` | não envia |
| 19 | `parcelas` | não | servico | inteiro | não envia |
| 20 | `origem` | **sim** | todos | documento + página/linha/cláusula (ex.: `contrato-convenio-a.pdf p.12 cl.7.3` ou `decisao 2026-10-02 dono`) | **linha inválida** |
| 21 | `observacao` | não | todos | texto livre (nunca vai ao Rabi) | — |

Cabeçalho exato:

```
tipo;id_rabi;nome_rabi;nome_convenio;descricao_convenio;codigo;tipo_codigo_id;tabela87_id;tipo_atendimento_id;utiliza;valor_combinado;pacote;zerar;autorizacao_previa;retorno;fator_k;fonte_preco;tipo_precificacao;parcelas;origem;observacao
```

Exemplo fictício (Convênio A):

```
servico;101;APLICACAO ENDOVENOSA;;;;;;;S;=;N;N;S;N;;;;;contrato-convenio-a.pdf p.4 cl.3.1;conta aberta
servico;205;MEDICAMENTO X APLICADO EV;;;;;;;S;;N;N;S;N;;;;;contrato-convenio-a.pdf p.4 cl.3.2;soma itens
produto;3001;MEDICAMENTO X 100MG AMP;;;;;;;S;;;N;;;;;;;contrato-convenio-a.pdf p.9 anexo II;politica medicamento PMC
taxa;40;TAXA DE SALA;TAXA DE SALA AMBULATORIAL;;60000001;3;;;S;73,99;;N;;;;;;;tabela-convenio-a.xlsx linha 14;
servico;310;CURATIVO;;;;;;;S;120;S;N;;;;;;;contrato-convenio-a.pdf p.6 cl.5;pacote: gaze, soro e taxa inclusos
produto;3100;GAZE;;;;;;;S;;;S;;;;;;;contrato-convenio-a.pdf p.6 cl.5;incluso no pacote curativo
```

### 6.3 Validações da ferramenta antes de gerar qualquer corpo

- `origem` preenchida em **toda** linha; `utiliza` explícito.
- `valor_combinado = 0,01` → **bloqueia** até decisão escrita (marcador proibido).
- `pacote` só em `servico`; `fator_k`/`fonte_preco`/`tipo_precificacao`
  só em `produto`; `tipo_atendimento_id`/`autorizacao_previa`/`retorno`/
  `parcelas` só em `servico`.
- `fator_k` entre −100 e 2000; nunca `1` sem cláusula (default suspeito).
- `id_rabi` existe, está **ativo** no catálogo e `nome_rabi` confere.
- Serviço com `pacote=S` e (`somarItens` do catálogo = true) e
  `valor_combinado` vazio → aviso: "Pacote não fecha preço (V5)".
- Invariantes I1–I13 ([12-casos-de-teste.md](12-casos-de-teste.md)) sobre o
  resultado simulado; divergência → não grava.

## 7. Mapeamento coluna → campo da API, por aba

Nomes **conferidos** no spec 25/09/2026. Cada corpo leva só os campos com
valor a enviar.

| Coluna CSV | `PUT /convenios/{id}/servicos` (`servicos[]`) | `…/produtos` (`produtos[]`) | `…/taxas` (`taxas[]`) |
|---|---|---|---|
| `id_rabi` | `servicoId` | `produtoId` | `taxaId` |
| `utiliza` | `utiliza` | `utiliza` | `utiliza` |
| `zerar` | `zerarValor` | `zerarValor` | `zerarValor` |
| `pacote` | `pacote` | — | — |
| `autorizacao_previa` | `autorizacaoPrevia` | — | — |
| `retorno` | `retornoServico` | — | — |
| `nome_convenio` | `nomeConversao` | `nomeConversao` | `nomeConvertido` |
| `descricao_convenio` | `descricaoConvenio` | `descricaoConversao` | `descricaoConvertida` |
| `valor_combinado` | `valorInternoConvenio` | `valorUnitarioConversao` | `valorConvertido` |
| `fator_k` | — | `fatorK` (**string**, ex. `"38,24"`) | — |
| `fonte_preco` | — | `fontePrecoCompraOptionsId` ¹ | — |
| `tipo_precificacao` | — | `tipoPrecificacao` | — |
| `parcelas` | `parcelasMaximas` | (`parcelasMaximas` existe; não usar) | — |
| `tipo_codigo_id` | `tipoCodigoId` | `tipoCodigoId` | `tipoCodigoId` |
| `tabela87_id` | `tabela87ANSId` | `tabela87ANSId` | `tabela87ANSId` |
| `tipo_atendimento_id` | `tipoAtendimentoId` | — | — |
| `codigo` | `codigo` ² | `codigoConversao` ² | `codigo` |

¹ Não confirmado que `fontePrecoCompraOptionsId` = `fontePrecoId` de
`/tabelas-preco/precificacao` (o spec só diz "fonte de preço de compra
usada na política de preço"; erro devolve "fontePrecoCompraOptionsId N não
encontrado"). Verifique gravando 1 item em homologação e relendo.

² Campos de código existentes e **não usados** pelo CSV v1 (só com decisão):
serviço `codigoTuss`, `codigoConvenio`; produto `codigo`, `codigoTuss`,
`codigoTiss`; taxa `codigoTabelaConversao`, `descricaoConversaoTabela`,
`tipoTaxaId`; serviço `ativo`, `kitDocumentoId`. O mapeamento de `codigo` do
produto para `codigoConversao` é o mais provável pela precedência do manual
("código de conversão no convênio") — **confirme** em homologação.

### 7.1 Regras de envio

- **GET antes** de cada aba (foto). Vínculo novo: `utiliza` omitido vira
  `false` — por isso `utiliza` é sempre enviado.
- Até **200** itens por chamada; **uma** chamada por vez por convênio
  (senão 429); 45 s de limite (o resto volta `NAO_PROCESSADO`).
- `200` = tudo processado. `207` = falha parcial: leia `resultados[]`
  (`indice` começa em 0; `status` `CRIADO`/`ATUALIZADO`/`ERRO`/`NAO_PROCESSADO`)
  e reenvie **só** os `ERRO`/`NAO_PROCESSADO` depois de corrigir.
- Reenviar o mesmo item é seguro (idempotente).
- Depois: releia a aba, faça o diff campo a campo e uma **segunda leitura
  fria** (pega o que foi aceito e não persistiu).

## 8. Como gravar PACOTE pela API

`valorInternoConvenio` sozinho **não fecha pacote**. Envie as três coisas:

```
# 1) serviço: valor combinado + pacote; subserviço incluso: zerarValor
PUT /convenios/{id}/servicos
{ "servicos": [
    { "servicoId": 47, "utiliza": true, "valorInternoConvenio": 350.00, "pacote": true, "zerarValor": false },
    { "servicoId": 46, "utiliza": true, "zerarValor": true } ] }
# 2) produtos e taxas inclusos: zerarValor true (cobrado à parte: false)
PUT /convenios/{id}/produtos  { "produtos": [ { "produtoId": 120, "utiliza": true, "zerarValor": true } ] }
PUT /convenios/{id}/taxas     { "taxas":    [ { "taxaId": 15,    "utiliza": true, "zerarValor": true } ] }
# 3) conferir
GET /convenios/{id}/farol/itens?servicoRaizId=47&apenasAtivosNoConvenio=true&pageSize=200
    → itens zerados com receita 0; linha do serviço com receita = total esperado
GET /convenios/{id}/farol/servicos?servicoAtivo=true → receita_total do 47 = Σ esperado
```

- `valorInternoConvenio: null` limpa o valor combinado (volta a vazio).
- Lembre: o subserviço zerado perde **só** a base; os produtos/taxas de
  dentro dele precisam do **próprio** `zerarValor`.
- Serviço com `somarItens = true` e `pacote = true` **sem** valor combinado
  não fecha preço (Pacote não muda nada).

### 8.1 Cuidado com `PUT /convenios/{id}` (dados do convênio)

Substitui o cadastro inteiro: omitir `operadoraId` remove a operadora;
omitir datas limpa; `unidadesIds` fora da lista são desativadas;
`politicasPorTipoProduto` enviado = lista completa (as ausentes são
inativadas). E o `GET /convenios/{id}` do spec **não devolve** todos esses
campos. Portanto: crie o convênio com tudo na fase 1; para alterar depois,
monte o objeto completo a partir da régua confirmada e confira na tela /
relatório "Validação de Configuração Por Convênio" antes e depois.

## 9. Grupos da prévia

| Grupo | O que é | Ação |
|---|---|---|
| **A** — incontroverso | alteração com cláusula/linha de tabela que sustenta | propõe na prévia |
| **B** — precisa de decisão | pré-avaliação pronta + pergunta objetiva | pergunta (uma por vez) |
| **C** — não sei tratar | falta documento/valor | registra lacuna em `pendencias/LACUNAS.md` |

Nada entra por dedução: valor sem documento é **C**, não chute.

## 10. Sugestões que a IA faz ao ler o contrato (não só transcreve)

1. prazo de glosa curto → alertar fluxo de recurso;
2. reajuste com data fixa → lembrete;
3. autorização prévia obrigatória para grupo de serviços → `autorizacao_previa = S`;
4. FK de material → conferir com o que vai ser cadastrado;
5. contrato com pacote → registrar **quais** serviços e **o que** está dentro;
6. conta aberta → registrar (nem Pacote, nem Zerar);
7. serviço previsto no contrato que a clínica não presta → oportunidade;
8. serviço que a clínica presta e o contrato não prevê → risco de glosa, sugerir aditivo.

Registre em `ANALISE-CONTRATOS.md` do repo da clínica.
