# S10b — Convênio: abas e preços (fase 2) — atenção redobrada

> **Fonte:** https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#convenio-fase-2 · https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#ordem-configuracao · https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#tabela-verdade · https://www.rabisistemas.com.br/manual/precos/arvore-de-decisao.html#tabela-mestra · spec `openapi-2026-09-25.json` (`PUT /convenios/{id}/planos|especialidades|taxas|produtos|servicos|colaboradores`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (regras de preço vigentes desde 23–24/09/2026; coluna Valor com 4 linhas desde 24/09/2026; "valor combinado não é pacote" vigente em 25/09/2026) · **Kit:** v0.1.0

## Objetivo

Cada item que o convênio cobra — serviço, subserviço, produto, taxa — está com
**Utiliza** marcado, o valor e o código do contrato, e o modo certo (conta aberta
ou pacote fechado); nada que o convênio não cobra está ligado; e o resultado
previsto pelo simulador **bate** com o Farol relido. Um convênio por vez.

> Cobra-se o que precisa ser cobrado, pelo valor de contrato, em todos os
> convênios — nem menos (receita perdida), nem de forma abusiva.

## Link do manual

- Fase 2 pela API: https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#convenio-fase-2
- Ordem tela a tela: https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#ordem-configuracao
- Tabela-verdade do pacote: https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#tabela-verdade
- Valor combinado não é pacote: https://www.rabisistemas.com.br/manual/precos/index.html#valor-combinado-nao-e-pacote
- 4 linhas da coluna Valor: https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#quatro-linhas
- Receitas: https://www.rabisistemas.com.br/manual/precos/guia-clinica.html#parte-4-receitas

**Leitura obrigatória no kit antes de gravar a primeira aba:**
[00-INDICE de preços](../conhecimento/precos-e-conversao/00-INDICE.md) →
[01-conceitos](../conhecimento/precos-e-conversao/01-conceitos.md) ·
[06-entra-sai](../conhecimento/precos-e-conversao/06-arvore-subservico-e-entra-sai.md) ·
[07-quatro-linhas](../conhecimento/precos-e-conversao/07-quatro-linhas-do-valor.md) ·
[10-do-contrato-a-configuracao](../conhecimento/precos-e-conversao/10-do-contrato-a-configuracao.md) ·
[11-receitas](../conhecimento/precos-e-conversao/11-receitas.md) ·
[14-armadilhas-vividas](../conhecimento/precos-e-conversao/14-armadilhas-vividas.md) ·
[15-conflitos-resolvidos](../conhecimento/precos-e-conversao/15-conflitos-resolvidos.md).

## Depende de

S10a do mesmo convênio (dados, política, respostas das 4 perguntas); catálogo
completo (S05, S06, S08); colaboradores (S09).

## Documentos a pedir

CV-2 (tabela de preços), CV-3 (materiais e medicamentos), CV-6
(credenciamento), CV-8 (faturamento real — ajuda a conferir), FA-6 (composição).

## As regras que não se negociam

1. **Vazio ≠ zero.** Vazio (`null`) = "sem regra aqui": o valor **desce** de
   nível (convênio → política por tipo → cadastro). `0` = **zero de verdade**.
2. **0,01 como marcador é proibido.** Linha com 0,01 trava até decisão escrita.
3. **Utiliza = o convênio cobre o item.** Vem desmarcado por padrão. Sem Utiliza,
   o item é custo sem receita (fora da receita do Farol; no orçamento entra a
   R$ 0). Marque Utiliza em **tudo** que o convênio cobre — e só nisso.
4. **Itens com Utiliza sempre entram** na conta do serviço (taxas, produtos,
   subserviços), cada um com a sua conversão. `somarItens` decide só o valor
   próprio do serviço.
5. **Valor combinado não é pacote.** O valor digitado na linha 🔁 muda só o preço
   do próprio serviço; os itens continuam somando por cima.
6. **Preço fechado = valor combinado + Pacote + Zerar nos inclusos.** Pacote é
   marcado na linha do serviço **no convênio** (não existe no cadastro). Sem
   Pacote, o Zerar nem é consultado.
7. **Zerar é por item e não desce em cascata.** Dentro de um serviço com Pacote,
   o item **incluso** no preço fechado recebe Zerar — inclusive medicamento, se
   o contrato diz que está incluso. O **serviço raiz não é zerado** (senão o
   pacote sai zero). Conta aberta = **sem Pacote e sem Zerar**.
8. **Subserviço:** Zerar tira só o valor próprio dele; os itens dentro seguem o
   próprio Zerar. Só a falta de Utiliza no subserviço tira tudo o que está nele.

## Índice de dados a coletar

Toda linha vai para `dados/convenios/<slug>/precos.csv` (formato de 21 colunas
em [10-do-contrato-a-configuracao](../conhecimento/precos-e-conversao/10-do-contrato-a-configuracao.md),
com **ORIGEM obrigatória**). Campos por aba:

### Aba Planos — `PUT /convenios/{id}/planos` (chave `planoId`, até 200)

| dado | campo API | obrigatório? | onde costuma estar | padrão sugerível | pergunta se faltar |
|---|---|---|---|---|---|
| Plano atendido | `planoId`, `utiliza` (coluna "Atende") | `planoId` | CV-5 | todos os planos da operadora | "A clínica atende todos os planos do <convênio>?" |

### Aba Especialidades — `PUT /convenios/{id}/especialidades` (chave `especialidadeId`, até 200)

| dado | campo API | obrigatório? | onde costuma estar | padrão sugerível | pergunta se faltar |
|---|---|---|---|---|---|
| Especialidade coberta | `especialidadeId`, `utiliza`, `dataInicio`, `dataFim` | `especialidadeId` | anexo de especialidades do contrato | — | "Quais especialidades o contrato do <convênio> cobre?" |

Faturamento real prova uso, **não** prova contrato: especialidade faturada que
não está no anexo assinado é bandeira para confirmar.

### Aba Taxas — `PUT /convenios/{id}/taxas` (chave `taxaId`, até 200)

| dado | campo API | obrigatório? | onde costuma estar | padrão sugerível | pergunta se faltar |
|---|---|---|---|---|---|
| Cobre? | `utiliza` | explícito sempre | CV-2 | — | "O <convênio> paga a <taxa>?" |
| Valor do convênio | `valorConvertido` (`null` = sem regra) | não | CV-2 | vazio | "Quanto o <convênio> paga pela <taxa>?" |
| Incluso em pacote? | `zerarValor` | não | contrato (o que está dentro do pacote) | não | — |
| Nome/descrição no convênio | `nomeConvertido`, `descricaoConvertida` | não | CV-2 | — | — |
| Códigos | `codigo`, `tipoCodigoId`, `tipoTaxaId`, `tabela87ANSId`, `codigoTabelaConversao`, `descricaoConversaoTabela` | não | CV-2 | — | — |

### Aba Produtos — `PUT /convenios/{id}/produtos` (chave `produtoId`, até 200)

| dado | campo API | obrigatório? | onde costuma estar | padrão sugerível | pergunta se faltar |
|---|---|---|---|---|---|
| Cobre? | `utiliza` | explícito sempre | CV-3 | — | "O <convênio> paga o <produto> à parte?" |
| Valor unitário do convênio | `valorUnitarioConversao` (`null` = herda) | não | tabela própria do contrato | vazio (usa a política) | — |
| Fator K da linha | `fatorK` (percentual; `null` = herda) | não | CV-3 | vazio | — |
| Fonte e tipo de preço | `fontePrecoCompraOptionsId`, `tipoPrecificacao` (`PRECO_1..3`) | não | CV-3 | herdar da política (S10a) | — |
| Incluso em pacote? | `zerarValor` | não | contrato | não | — |
| Textos e códigos | `nomeConversao`, `descricaoConversao`, `codigo`, `codigoTuss`, `codigoTiss`, `codigoConversao`, `tipoCodigoId`, `tabela87ANSId`, `parcelasMaximas` | não | CV-3 | — | — |

### Aba Serviços — `PUT /convenios/{id}/servicos` (chave `servicoId`, até 200)

| dado | campo API | obrigatório? | onde costuma estar | padrão sugerível | pergunta se faltar |
|---|---|---|---|---|---|
| Cobre? | `utiliza` | explícito sempre | CV-2 | — | "O <convênio> cobre o <serviço>?" |
| Valor combinado (🔁) | `valorInternoConvenio` (`null` = limpa, volta a vazio) | não | CV-2 | vazio | "Qual o valor do <serviço> no <convênio>?" |
| Preço fechado? | `pacote` | não | contrato / 4 perguntas | não | "O <serviço> no <convênio> é um valor único com tudo incluso?" |
| Zerar (serviço dentro de pacote de outro) | `zerarValor` | não | contrato | não | — |
| Tipo de atendimento | `tipoAtendimentoId` | não | contrato, guias | — | — |
| Autorização prévia | `autorizacaoPrevia` | não | cláusula de autorização | — | "O <convênio> exige autorização antes do <serviço>?" |
| Retorno | `retornoServico` | não | cláusula de retorno | — | — |
| Textos e códigos | `nomeConversao`, `descricaoConvenio`, `codigo`, `codigoTuss`, `codigoConvenio`, `tipoCodigoId`, `tabela87ANSId`, `kitDocumentoId`, `parcelasMaximas`, `ativo` | não | CV-2 | — | "Qual o código que o <convênio> usa para o <serviço>? Sem o código certo a guia é glosada." |

### Aba Colaboradores — `PUT /convenios/{id}/colaboradores` (chave `colaboradorId`, até 100)

| dado | campo API | obrigatório? | onde costuma estar | padrão sugerível | pergunta se faltar |
|---|---|---|---|---|---|
| Credenciado | `credenciado` | não | CV-6 | — | "<nome> é credenciado no <convênio>? Se não for, os atendimentos dele glosam." |
| Atende | `atende` (só `true` se credenciado ou com conversão) | não | CV-6 | — | — |
| Colaborador convertido | `colaboradorConvertidoId` | não | contrato (atende em nome de outro) | — | — |
| Especialidades | `especialidadesIds`, `especialidadesConvertidasIds` (aditivo, até 50) | não | CV-6 | — | — |

## Fila de perguntas

1. Confirmar as respostas das 4 perguntas (vindas da S10a) **por serviço**:
   pacote fechado / conta aberta / preço fixo, e o que está dentro de cada pacote.
2. Confirmar em bloco as linhas A (incontroversas, com origem) do `precos.csv`.
3. Perguntar uma a uma as linhas B (precisam de decisão).
4. Listar as linhas C (sem documento) como lacunas — nada de chute.
5. Credenciamento, profissional por profissional.

## Enriquecimento possível

- Casamento automático nome/código da tabela do convênio × catálogo do Rabi
  (código TUSS primeiro, depois nome normalizado **com dose**); o que não casar
  vai para confirmação.
- **Simulação antes de gravar:** `ferramentas/conversao/simulador.py` prevê a
  linha ✅, a Σ e o Farol de cada serviço com as regras vigentes.
- **Montagem dos corpos:** `ferramentas/conversao/montar_convenio.py` lê o
  `precos.csv`, valida (origem, 0,01, invariantes) e gera os corpos das abas na
  ordem certa.

## Leitura do que já existe no Rabi e regra de não perder nada

Foto antes do convênio inteiro, **todas as páginas** (`linhas lidas = total`):
`GET /convenios/{id}`, `/planos`, `/especialidades`, `/taxas`, `/produtos`,
`/servicos`, `/colaboradores`, e `/farol/itens`, `/farol/servicos`,
`/farol/produtos`.

- Antes de mexer em cada linha: **ativo ou inativo** no catálogo, e o **nome**.
- Convênio já trabalhado: 6 contagens de regressão (R1–R6) antes de tudo — ver
  [modos de sessão](../metodologia/modos-de-sessao.md).
- Nunca reaproveitar o ID de vínculo de um convênio em outro: o CSV usa sempre o
  ID do **catálogo** (`servicoId`, `produtoId`, `taxaId`).

## Gravação

As abas são **upsert**: campo omitido **mantém**; `null` **limpa** (volta a
vazio); `0` é zero de verdade. Mande **só** o que foi aprovado.
Permissão `convenio:update`. **Uma chamada por vez por convênio** (a segunda
simultânea recebe 429). Resposta 200 = tudo processado; **207** = conferir
`resultados[]` (`CRIADO`/`ATUALIZADO`/`ERRO`/`NAO_PROCESSADO`) e reenviar só os
com erro. Reenviar é seguro (idempotente).

**Ordem das abas:** 1 Planos → 2 Especialidades → 3 Taxas → 4 Produtos →
5 Serviços (por último, porque soma os de cima) → 6 Colaboradores.

**Passes dentro de Taxas, Produtos e Serviços** (cada passe verificável sozinho):
1. **Utiliza** (tudo que o convênio cobre; nada mais);
2. **valores** (valor combinado, fator K, fonte, tipo de precificação);
3. **textos e códigos**;
4. **tipo de atendimento**, autorização prévia, retorno, parcelas (serviços);
5. **Pacote e Zerar** por último, item por item.

**Primeiro item de cada passe sozinho, provado; depois o resto da aba.**

Exemplo fictício de preço fechado (serviço 47 com o produto 120 e a taxa 15
inclusos):

```
PUT /convenios/12/servicos  {"servicos":[{"servicoId":47,"utiliza":true,"valorInternoConvenio":350.00,"pacote":true}]}
PUT /convenios/12/produtos  {"produtos":[{"produtoId":120,"utiliza":true,"zerarValor":true}]}
PUT /convenios/12/taxas     {"taxas":[{"taxaId":15,"utiliza":true,"zerarValor":true}]}
```

Conta aberta (o mesmo serviço, cobrando cada item): `pacote` falso, nenhum
`zerarValor`, itens com Utiliza e o seu valor.

## Prova

- `provas/S10b/<slug>/<aba>-passe-N/` (antes, resposta, depois, diff) para cada
  passe de cada aba; **segunda leitura fria** ao fim de cada aba.
- **Conferência obrigatória de pelo menos 3 serviços por convênio:** um
  **simples**, um **com medicamento**, um **com pacote** (se houver) —
  `GET /convenios/{id}/farol/itens?servicoRaizId=<id>` e `/farol/servicos`
  comparados com o previsto pelo simulador (`ferramentas/conversao/conferir_farol.py`).
  No pacote, os itens zerados devem vir com receita 0; o total do serviço é a
  `receita_total` de `/farol/servicos` (a Σ da tela; `efetivo.totalConvenio` não
  existe na API externa).
- Validação cruzada: subagente `conferente-precos` (contexto limpo) confere a
  régua × `precos.csv` × Farol relido. Quem gravou não valida sozinho.
- Contagens R1–R6 **depois**, gravadas em `dados/convenios/<slug>/contagens.md`.

## As 4 linhas da coluna Valor do serviço (tela, em produção desde 24/09)

🔒 cadastro (ou "soma dos itens") · 🔁 combinado · ✅ valor próprio que vai na
guia · Σ total do serviço no convênio (= receita do Farol). Em serviço que soma
itens sem valor combinado, a ✅ mostra "0,00 (sem preço próprio: itens cobrados
à parte)" — **não é erro**; confira a Σ. Produtos e taxas seguem com 3 linhas.
Detalhe: [07-quatro-linhas](../conhecimento/precos-e-conversao/07-quatro-linhas-do-valor.md).

## Armadilhas desta sprint

- **Orçamento de medicamento saindo R$ 0,00:** numa implantação real, a
  aplicação (subserviço) estava com Zerar dentro do serviço de medicamento em
  conta aberta, e o medicamento também — tudo foi a zero. Correção: em conta
  aberta, sem Pacote e sem Zerar; em pacote, Zerar só nos inclusos, nunca no
  serviço raiz.
- **"Digitei um valor e os itens continuaram somando"** → falta marcar Pacote.
- **0 gravado onde devia ficar vazio:** o item deixa de herdar e sai a R$ 0.
- **Utiliza desmarcado** é a causa nº 1 de "o valor veio menor".
- **Contar "ligados" pela API sem cruzar com `ativo`** do catálogo: o Farol e as
  abas listam serviços desativados.
- **Serviço desligado não pode ser agendado:** nunca desligue serviço que a
  clínica presta; e nunca desligue o serviço deixando o produto ligado.
- Duas abas ao mesmo tempo no mesmo convênio → 429.
- Rotas de massa da tela (copiar convênio, ligar todos, importar Excel) não
  entram na implantação por IA sem ordem escrita.
- Detalhes vividos: [14-armadilhas-vividas](../conhecimento/precos-e-conversao/14-armadilhas-vividas.md).

## Definition of Ready / Definition of Done

**DoR:** S10a concluída; respostas das 4 perguntas por serviço; `precos.csv`
com origem em todas as linhas; simulação feita e mostrada.

**DoD:**
- [ ] as 6 abas gravadas e relidas, com segunda leitura fria;
- [ ] todo item cobrado com Utiliza; nada ligado que o convênio não cobra;
- [ ] nenhuma linha com 0,01; vazio onde não há regra;
- [ ] pacotes: valor combinado + Pacote + Zerar nos inclusos; serviço raiz sem Zerar;
- [ ] 3 serviços conferidos (simples, medicamento, pacote) previsto × Farol;
- [ ] contagens R1–R6 registradas; provas salvas; conferente-precos sem divergência aberta.

## Checklist de itens

| # | item | status | origem | prova | observação |
|---|---|---|---|---|---|
| S10b-01 | Foto antes do convênio inteiro (abas + Farol) | pendente | | provas/S10b/ | |
| S10b-02 | precos.csv montado com ORIGEM em todas as linhas | pendente | | | |
| S10b-03 | Linhas A confirmadas; B decididas; C como lacunas | pendente | | | |
| S10b-04 | Simulação mostrada ao usuário | pendente | | | |
| S10b-05 | Aba Planos | pendente | | | |
| S10b-06 | Aba Especialidades | pendente | | | |
| S10b-07 | Aba Taxas (passes 1–5) | pendente | | | |
| S10b-08 | Aba Produtos (passes 1–5) | pendente | | | |
| S10b-09 | Aba Serviços (passes 1–5) | pendente | | | |
| S10b-10 | Aba Colaboradores (credenciamento) | pendente | | | |
| S10b-11 | Segunda leitura fria de todas as abas | pendente | | | |
| S10b-12 | 3 serviços conferidos (simples, medicamento, pacote) | pendente | | | |
| S10b-13 | Conferente-precos sem divergência aberta | pendente | | | |
| S10b-14 | Contagens R1–R6 registradas | pendente | | | |

## O que registrar

- `dados/convenios/<slug>/precos.csv`, `contagens.md`, `decisoes.md`.
- `decisoes/DECISOES.md`: cada decisão B com quem decidiu.
- `pendencias/LACUNAS.md`: linhas C.
- `ESTADO.md`: estado do convênio (FECHADO quando o DoD estiver completo) e
  próximo convênio da fila.
