# S15 — Testes de validação (10 cenários)

> **Fonte:** https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-15 · https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#como-conferir · spec `openapi-2026-09-25.json` (leituras de agenda, orçamento, faturamento, financeiro, NFS-e, Farol) · **Conferido em:** 2026-09-25
> **Vale para:** produção (10 cenários do guia de 25/09/2026; cenários 7, 8 e 10 marcados "Novo — set/2026") · **Kit:** v0.1.0

## Objetivo

Provar, **antes** de a clínica depender do sistema, que ele funciona do
agendamento ao recebimento: os 10 cenários do manual passam, com as checagens
extras da IA, e os dados de teste são cancelados ou inativados (nunca apagados).

## Link do manual

- Etapa 15: https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-15
- Conferência de preços: https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#como-conferir
- Rotinas do dia a dia (para montar os roteiros): https://www.rabisistemas.com.br/manual/rotinas/index.html

## Depende de

S01–S14 concluídas (S12 NFS-e só para o cenário 7).

## Documentos a pedir

Nenhum novo. Usa CV-2/CV-7 (preços esperados), CV-8 (guias reais para comparar).

## Índice de dados a coletar

| dado | campo API | obrigatório? | onde costuma estar no material do cliente | padrão sugerível | pergunta ao usuário se faltar |
|---|---|---|---|---|---|
| Paciente de teste | `POST /pacientes` | sim | — | nome "TESTE IMPLANTACAO 01", CPF de teste (dígito válido, gerado para teste), dados fictícios | "Posso criar um paciente de teste com nome 'TESTE IMPLANTACAO 01'? Ele será inativado depois." |
| Convênio e serviços dos testes | — | sim | S10 | Particular + o convênio de maior volume; um serviço simples, um com medicamento, um com pacote | "Para o teste por convênio, posso usar o <convênio de maior volume>?" |
| Quem executa na tela | — | sim | PE-3 | recepção + profissional + faturamento reais | "Quem da equipe pode fazer os testes comigo? Leva cerca de 1 hora." |
| Valores esperados de cada teste | — | sim | CV-2, CV-7, simulador | — | — |

## Os 10 cenários do manual + checagens da IA

A tela é operada pela equipe (a API externa não cobre check-in, atendimento ao
vivo, bloqueio de agenda, fila de espera nem fechamento de lote/XML); a IA
**prepara o roteiro, lê o resultado pela API e compara com o esperado**.

| # | Cenário (manual) | O que se faz na tela | O que a IA confere além disso (leitura) |
|---|---|---|---|
| 1 | Agendamento Particular | cadastrar paciente → agendar → confirmar → check-in → atender → verificar lançamento financeiro | valor lançado = o do convênio **Particular** (não da tabela interna); **orçamento de medicamento não sai R$ 0,00**; `GET /agendamentos?data=<dia>`, `GET /financeiro/movimentacoes` |
| 2 | Agendamento por Convênio | paciente com carteirinha → agendar com convênio → check-in → atender → verificar guia | preço = contrato; **código** certo na guia; autorização prévia exigida onde o contrato manda; `GET /faturamento/guias`, `GET /faturamento/guias/valores-atendimento/{atendimentoId}` |
| 3 | Faturamento | pré-faturamento → fechar lote → gerar contas a receber → ver no financeiro | nenhum item fora da tabela; **XML valida** (o arquivo baixado da tela é conferido contra o padrão TISS, quando o esquema estiver disponível); valores de faturamento lidos conforme a descrição da rota (algumas em centavos/texto) |
| 4 | Bloqueio de Agenda | criar bloqueio → horário some da agenda | bloqueio respeita local, sala e equipamento; `POST /agendamentos/horarios/disponiveis` não oferece o horário bloqueado |
| 5 | Relatórios | agenda e fluxo de caixa com os dados dos testes | relatório bate item a item com o que foi lançado |
| 6 | Permissões | logar com cada perfil | recepção não vê Configurações; profissional não vê Financeiro; cada perfil conforme a matriz da S14 |
| 7 | Emissão de NFS-e (módulo ativo) | recebimento particular → NFS-e no ato → retorno/autorização | código de serviço e alíquota = configuração fiscal; `GET /nfse/notas` — **só com o módulo contratado**; sem módulo = `n/a` (escopo não contratado), não reprovado |
| 8 | Fila de Espera | paciente na fila com horário cheio → cancelar um agendamento → sugestão do próximo e botão "Agendar" | a sugestão respeita profissional e serviço |
| 9 | Aprovação por alçada | desconto acima do limite (ou farol consolidado vermelho) → pendência na Central de Notificações → aprovar com usuário de alçada | limite = o definido na S14; quem aprova = quem tem o nível |
| 10 | Orçamento com serviço composto | orçar serviço com medicamento e taxa | produtos e taxas com Utiliza entram na conta; farol consolidado bate com a S11; `GET /orcamentos/{id}/0` |

### Checagens extras da IA (valem para todos os convênios)

- **3 serviços por convênio** (simples, com medicamento, com pacote) conferidos
  contra o contrato — já feito na S10b; aqui se refaz para o Particular e o
  convênio do cenário 2 **pelo orçamento real**.
- **Orçamento de medicamento não sai R$ 0,00** em nenhum convênio que o cobra.
- Nenhum Farol vermelho sem causa decidida; nenhum roxo aberto.
- Credenciamento: o profissional do cenário 2 aparece para o convênio na agenda.
- Todos os perfis testados em login real (S14).
- Validade da chave (`X-ApiKey-Expires-At`) ainda cobre o go-live e a S17.

## Fila de perguntas

1. Quem executa e quando (uma sessão de ~1 h com a equipe).
2. Aprovação do paciente de teste e dos convênios/serviços usados.
3. Para cada cenário, "feito?" e, se algo diferir do esperado, "o que apareceu na
   tela?" (a IA explica a causa e propõe a correção).

## Enriquecimento possível

- Roteiro de cada cenário pronto para imprimir, com o valor esperado já calculado
  pelo simulador.

## Leitura do que já existe no Rabi e regra de não perder nada

- Os testes criam registros reais: tudo o que for de teste leva "TESTE" no nome
  ou na observação e entra numa lista em `provas/S15/dados-de-teste.md` (IDs).
- `GET /agendamentos` **exige `data`** (um dia por chamada).

## Gravação

| O que | Como |
|---|---|
| Paciente de teste | `POST /pacientes` (ritual normal) |
| Orçamento de teste (cenário 10, se feito pela API) | `POST /orcamentos` **sem pagamento no ato** (pagamento no ato pode emitir NFS-e) |
| Demais cenários | na tela, pela equipe |
| Limpeza | cancelar agendamentos (`PATCH /agendamentos/{id}/cancelar` com `motivoCancelamentoId`), inativar paciente de teste (`DELETE /pacientes/{id}` = inativação), cancelar orçamentos — **com ordem escrita**; nota fiscal emitida em teste: cancelamento só com ordem escrita e conforme a regra da prefeitura |

Nada é apagado de verdade: tudo fica cancelado ou inativo e listado.

## Prova

- `provas/S15/cenario-NN.md` para cada um: roteiro, esperado, encontrado,
  resultado (passou / não passou / `n/a` com motivo), IDs envolvidos (sem dado
  pessoal — o paciente de teste é fictício).
- `provas/S15/dados-de-teste.md`: lista dos registros de teste e o estado final
  (cancelado/inativo).

## Armadilhas desta sprint

- Testar o particular com a tabela interna em mente: o preço vem do convênio
  "Particular".
- Emitir NFS-e de teste sem saber que é real (o cenário 7 gera nota de verdade):
  combine com o dono e o contador antes.
- Registrar movimentação financeira pela API (pode emitir NFS-e).
- Apagar dados de teste em vez de cancelar/inativar.
- Go-live com cenário reprovado.

## Definition of Ready / Definition of Done

**DoR:** S01–S14 concluídas; equipe disponível; valores esperados calculados.

**DoD:**
- [ ] os 10 cenários passaram (ou `n/a` com motivo — ex.: 7 sem módulo fiscal);
- [ ] checagens extras da IA sem pendência;
- [ ] dados de teste cancelados/inativados e listados;
- [ ] relatório da sprint no repo.

## Checklist de itens

| # | item | status | origem | prova | observação |
|---|---|---|---|---|---|
| S15-01 | Roteiros e valores esperados prontos | pendente | | | |
| S15-02 | Paciente de teste criado | pendente | | | |
| S15-03 | Cenário 1 — Agendamento Particular | pendente | | provas/S15/ | |
| S15-04 | Cenário 2 — Agendamento por Convênio | pendente | | | |
| S15-05 | Cenário 3 — Faturamento (+ XML) | pendente | | | |
| S15-06 | Cenário 4 — Bloqueio de Agenda | pendente | | | |
| S15-07 | Cenário 5 — Relatórios | pendente | | | |
| S15-08 | Cenário 6 — Permissões | pendente | | | |
| S15-09 | Cenário 7 — NFS-e | pendente | | | n/a se sem módulo |
| S15-10 | Cenário 8 — Fila de Espera | pendente | | | |
| S15-11 | Cenário 9 — Aprovação por alçada | pendente | | | |
| S15-12 | Cenário 10 — Orçamento com serviço composto | pendente | | | |
| S15-13 | Orçamento de medicamento ≠ R$ 0,00 (todos os convênios) | pendente | | | |
| S15-14 | Dados de teste cancelados/inativados | pendente | | | |

## O que registrar

- `historico/reviews/S15-<data>.md` com o placar dos cenários.
- `decisoes/DECISOES.md`: cenários `n/a` e por quê.
- `ESTADO.md`: próximo passo = S16 (data de go-live).
