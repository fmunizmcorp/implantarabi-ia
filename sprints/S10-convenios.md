# S10 — Convênios (visão da etapa), convênio "Particular" e grade horária

> **Fonte:** https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-10 · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-10 · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-10b · https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#ordem-configuracao · spec `openapi-2026-09-25.json` · **Conferido em:** 2026-09-25
> **Vale para:** produção (regras de preço por convênio em produção desde 23–24/09/2026; coluna Valor com 4 linhas desde 24/09/2026) · **Kit:** v0.1.0

## Objetivo

Todo convênio que a clínica atende — **começando pelo "Particular"** — existe
com os dados do contrato (S10a), com as abas de preço configuradas e conferidas
(S10b), com os profissionais credenciados; e cada profissional e equipamento tem
**grade horária** (a grade lista os convênios aceitos, por isso vem aqui).

Esta é a sprint que decide a receita da clínica. **Atenção redobrada.**

## Link do manual

- Etapa 10: https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-10
- Tela de convênios: https://www.rabisistemas.com.br/manual/modulos/configuracoes.html#convenios
- Ordem de configuração de preços: https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#ordem-configuracao
- Grade: https://www.rabisistemas.com.br/manual/modulos/configuracoes.html#colaboradores-grade-set-2026
- Pela API: https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-10 e #passo-10b

## Depende de

S04 (operadoras e planos), S05 (taxas), S06 (produtos), S08 (serviços e tabela
interna), S09 (colaboradores). Para a grade: S03 (locais) e S07 (equipamentos).

## Documentos a pedir

CV-1 a CV-8, PE-2 (escalas). Ver [lista única](../metodologia/lista-unica-de-documentos.md).

## Como esta sprint se divide

| Parte | Arquivo | O que faz |
|---|---|---|
| Fila de convênios + "Particular" + grade | este arquivo | organiza a etapa |
| Fase 1 — dados do convênio | [S10a-convenio-dados.md](S10a-convenio-dados.md) | contrato → cadastro (prazos, planos, política por tipo de produto) |
| Fase 2 — abas e preços | [S10b-convenio-abas-e-precos.md](S10b-convenio-abas-e-precos.md) | Planos, Especialidades, Taxas, Produtos, Serviços, Colaboradores |
| Conferência | [S11-conferencia-farol.md](S11-conferencia-farol.md) | Farol por convênio |

**Um convênio por vez**, do começo ao fim (S10a → S10b → leitura do Farol),
provado, e só então o próximo. Nunca dois em paralelo.

## Índice de dados a coletar (nível da etapa)

| dado | campo API | obrigatório? | onde costuma estar no material do cliente | padrão sugerível | pergunta ao usuário se faltar |
|---|---|---|---|---|---|
| Lista de convênios atendidos | — | sim | contratos (CV-1), faturamento (CV-8), carteirinhas | — | "Quais convênios a clínica atende hoje? Algum parou de atender?" |
| Ordem de trabalho | — | sim | volume de atendimento (CV-8) | "Particular" primeiro; depois do maior volume para o menor | "Posso começar pelo Particular e depois pelo convênio que mais atende?" |
| Modelo de cobrança de cada convênio | (define S10b) | sim | contrato, tabela | — | "No <convênio>, a aplicação é um valor único com material e taxa incluídos, ou cada item é cobrado à parte?" |

### Grade horária (depois dos convênios)

| dado | campo API | obrigatório? | onde costuma estar | padrão sugerível | pergunta se faltar |
|---|---|---|---|---|---|
| Profissional | `colaboradorGrade[].colaboradorId` | sim | PE-2 | — | — |
| Local | `localId` | não (recomendado) | PE-2 | a sala habitual | "Em qual sala <nome> atende?" |
| Início e fim | `inicioAtendimento`, `fimAtendimento` (data-hora) | sim | PE-2 | — | "Em que dias e horários <nome> atende?" |
| Duração de cada horário (min) | `tempoAtendimento` | sim | PE-2, duração do serviço (S08) | a duração da consulta | "Quanto tempo dura cada atendimento de <nome>?" |
| Repetição | `repetir` (ex.: `NAO_REPETIR`, `SEMANALMENTE`) | sim | PE-2 | `SEMANALMENTE` | — |
| Dias da semana | `diasDaSemana` (ex.: `SEG,QUA,SEX`) | sim | PE-2 | — | — |
| Convênios aceitos (e limite) | `convenio[]` (`id`, `limite`) | não | credenciamento (CV-6) | os convênios em que o profissional é credenciado | "<nome> atende por quais convênios nesse horário? Tem limite por dia?" |
| Especialidades / serviços / equipamentos | `especialidades[]`, `servicos[]`, `equipamento[]` | não | PE-2 | — | — |
| Vigência | `vigenteDesde`, `vigenteAte` | não | — | a partir do go-live | — |
| Encaixes | `maximoEncaixePorDia`, `maximoEncaixePorHorario`, `minimoTempoEntreEncaixes` | não | regra interna | em branco | "A agenda de <nome> aceita encaixe? Quantos por dia?" |
| Agendamento online | `agendamentoOnline` | não | — | desligado | — |
| Grade do equipamento | `POST /grades-equipamento` (lista sem envelope): `localId`, `equipamentoId`, `diaDaSemana`, `inicioAtendimento`, `fimAtendimento`, `gradeEmMinutos` | sim | PE-2 | horário da sala | "O <aparelho> fica disponível em que horários?" |

## Fila de perguntas (nível da etapa)

1. Confirmar a lista de convênios e a ordem (Particular primeiro).
2. Para cada convênio, **na vez dele**: as 4 perguntas do modelo de cobrança
   (pacote fechado? conta aberta? preço fixo? quais serviços são pacote e o que
   tem dentro?) — ver S10a/S10b.
3. Depois de todos (ou de cada) convênio: escala de cada profissional, **uma
   pessoa por vez**.
4. Horário dos equipamentos.

## O convênio "Particular"

- É **um convênio como os outros** (da operadora "Particular", S04), e é **dele**
  que sai o preço cobrado do paciente particular — não da tabela interna.
- No manual: "Pagamento no ato = Sim". **Não encontrei na API externa um campo
  com esse nome** (há `faturadoPagamento`, cujo sentido não está confirmado):
  marque pela tela e confira; registre a decisão.
- Também precisa de **política de preço por tipo de produto** (S10a): particular
  sem política é causa de produto sem preço e orçamento zerado.
- Pacote no Particular é comum (ex.: aplicação com materiais e taxas inclusos):
  mesmas regras da S10b.
- Consultório individual: o Particular (e, no máximo, 1 convênio) é a S10 toda.

## Enriquecimento possível

- Ordem por volume a partir do relatório de faturamento (CV-8).
- Grade a partir da agenda atual exportada do sistema anterior (SA-3), convertida
  para o formato da API.

## Leitura do que já existe no Rabi e regra de não perder nada

- `GET /convenios` (todas as páginas) — casar por CNPJ e nome. Convênio que já
  existe entra no **modo Convênio** com o diagnóstico NOVO / EM ANDAMENTO /
  FECHADO ([modos de sessão](../metodologia/modos-de-sessao.md)).
- Grades: `GET /grades-colaborador?colaboradorId=…&localId=…&vigenteEm=…` e
  `GET /grades-equipamento?equipamentoId=…&localId=…&vigenteEm=…` — **filtre**;
  sem filtro a leitura pode trazer a grade da clínica inteira.

## Gravação

| Ordem | O que | Rota | Permissão |
|---|---|---|---|
| 1 | Cada convênio, um por vez | S10a e S10b | `convenio:create`, `convenio:update` |
| 2 | Grade de cada profissional | `POST /grades-colaborador` (corpo `{"colaboradorGrade":[…]}`, vários horários de uma vez) | `gradeColaborador:create` |
| 3 | Grade de cada equipamento | `POST /grades-equipamento` (lista direta) | `gradeEquipamento:create` |
| Correção | um horário | `PUT /grades-colaborador/{id}` / `PUT /grades-equipamento/{id}` com o horário completo | `…:update` |

- Grade: 409 (colaborador) ou 422 (equipamento) = conflito com grade existente.
- **Grade de equipamento:** defeito documentado — grava e devolve **500**. Não
  repita a chamada: releia e confira.
- **Excluir horário:** `DELETE /grades-colaborador/unique/{id}` apaga **só aquele
  horário**; `DELETE /grades-colaborador/{id}` apaga **ele e os próximos da
  série**. Trocar as duas apaga a agenda do profissional. Só com ordem escrita.

## Prova

- Por convênio: as provas da S10a/S10b e o relatório do Farol (S11).
- Grade: `provas/S10/grade-<profissional>/` com a leitura filtrada depois; na
  review, a tabela dia × horário × sala × convênios, e o implantador confirma que
  os horários aparecem na agenda da tela.

## Armadilhas desta sprint

- Configurar dois convênios ao mesmo tempo.
- Grade antes dos convênios (a grade lista os aceitos).
- Esquecer o Particular ou a política de preço do Particular.
- Contar serviços "ligados" incluindo serviços inativos no catálogo.
- Todas as armadilhas de preço: ver S10b.

## Definition of Ready / Definition of Done

**DoR:** S04–S09 conferidas; lista de convênios e ordem aprovadas; CV-1 e CV-2 do
convênio da vez recebidos (ou lacuna registrada e aceita).

**DoD:**
- [ ] todo convênio da lista com S10a e S10b concluídas e Farol lido (S11);
- [ ] Particular configurado, com política de preço;
- [ ] todo profissional e equipamento com grade, visível na agenda;
- [ ] provas salvas; review aceita.

## Checklist de itens

| # | item | status | origem | prova | observação |
|---|---|---|---|---|---|
| S10-01 | Lista de convênios e ordem aprovadas | pendente | | | |
| S10-02 | Particular — S10a concluída | pendente | | | |
| S10-03 | Particular — S10b concluída | pendente | | | |
| S10-04 | Convênio <nome> — S10a concluída (uma linha por convênio) | pendente | | | |
| S10-05 | Convênio <nome> — S10b concluída (uma linha por convênio) | pendente | | | |
| S10-06 | Escalas coletadas (PE-2) | pendente | | | |
| S10-07 | Grade de <profissional> (uma linha por profissional) | pendente | | provas/S10/ | |
| S10-08 | Grade de <equipamento> (uma linha por equipamento) | pendente | | | |
| S10-09 | Agenda confirmada na tela pelo implantador | pendente | | | |

## O que registrar

- `ESTADO.md`: fila de convênios com o estado de cada um (NOVO / EM ANDAMENTO / FECHADO).
- `dados/convenios/<slug>/` por convênio (régua, precos.csv, decisões, contagens).
- `dados/agenda/grades.md`.
- `decisoes/DECISOES.md`: ordem, modelo de cobrança de cada convênio.
