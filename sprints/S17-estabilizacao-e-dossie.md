# S17 — Estabilização e dossiê

> **Fonte:** plano de implantação em sprints (Sprint de estabilização e dossiê de entrega, experiência prática) + https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#go-live ("suporte intensivo nas primeiras semanas") · **Conferido em:** 2026-09-25
> **Vale para:** pós go-live (dias 9 a 30 do projeto) · **Kit:** v0.1.0

## Objetivo

Corrigir o que o uso real revelar nas primeiras semanas e deixar a clínica com
um **dossiê** que qualquer pessoa — ou qualquer sessão de IA futura — consegue
pegar e continuar, sem depender da memória de ninguém.

## Link do manual

- Go-live e acompanhamento: https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#go-live
- Diagnóstico de preço: https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#diagnostico
- Kit: [13-conferencia-e-diagnostico](../conhecimento/precos-e-conversao/13-conferencia-e-diagnostico.md)

## Depende de

S16 (clínica operando).

## Documentos a pedir

Nenhum novo. Se aparecerem glosas ou recusas: a guia e o demonstrativo da
operadora (CV-8).

## Índice de dados a coletar

| dado | campo API | obrigatório? | onde costuma estar no material do cliente | padrão sugerível | pergunta ao usuário se faltar |
|---|---|---|---|---|---|
| Problemas relatados pela equipe | — | sim | conversa, mensagens da equipe | — | "Algo travou ou saiu com valor estranho hoje?" |
| Atendimentos/orçamentos com valor zerado | leitura de orçamentos e guias | sim | Rabi | — | (a IA lê) |
| Farol vermelho/roxo no uso real | `/farol/servicos`, `/farol/itens` | sim | Rabi | — | (a IA lê) |
| Guias recusadas ou glosadas | `GET /faturamento/glosas`, retorno da operadora | sim | Rabi, demonstrativo | — | "Chegou algum demonstrativo de glosa do <convênio>?" |
| Itens cobrados fora do contrato / não cobrados | guias × régua contratual | sim | Rabi + S10a | — | — |
| Data de vencimento das chaves ativas | `X-ApiKey-Expires-At` | sim (se houver integração) | — | — | — |

## Fila de perguntas

1. Na varredura diária: só o que a IA não consegue concluir sozinha (uma
   pergunta por vez).
2. No fim da estabilização: "Posso considerar a implantação encerrada? Ficam
   estas pendências, com estes donos e prazos."

## Enriquecimento possível

- Varredura diária por script (só leitura), com resumo curto para o usuário.
- Comparação guia × régua contratual automatizada (`ferramentas/conversao/`).

## Leitura do que já existe no Rabi e regra de não perder nada

**Nos primeiros 5 dias úteis, uma varredura diária** (só leitura), levada ao
implantador em uma tela:

- orçamentos/atendimentos com valor zerado;
- serviços com Farol vermelho ou roxo que apareceram no uso real;
- guias recusadas ou glosadas;
- itens cobrados fora do contrato, e itens do contrato que não estão sendo cobrados;
- contagens R1–R6 dos convênios, comparadas à última prova (regressão por
  alteração feita na tela pela equipe).

Depois da primeira semana: varredura semanal até o dia 30.

## Gravação

Toda correção desta sprint entra em **modo Atualização** (ou modo Convênio), com
o ritual de carga completo e análise de impacto — ver
[modos de sessão](../metodologia/modos-de-sessao.md). Nada de "ajuste rápido".

## Prova

- `historico/varreduras/AAAA-MM-DD.md` (resumo de cada varredura, sem dado de
  paciente).
- Cada correção com a sua prova, como em qualquer sprint.

## O dossiê de entrega

O repo da clínica **é** o dossiê. Na S17 a IA confere que ele está completo:

| Arquivo/pasta no repo da clínica | Conteúdo |
|---|---|
| `ESTADO.md` | painel final; modo "operação"; próximo passo (ex.: próximo reajuste) |
| `INDICE.md` | índice de tudo o que existe no repo |
| `PAPEIS.md` | dono, implantador, contatos de suporte |
| `credenciais/` | todos os acessos em texto claro, por serviço e ambiente, com data e estado (repo privado) |
| `ANALISE-CONTRATOS.md` | o que cada contrato permite, o que foi cadastrado e as sugestões |
| `dados/` | dados normalizados com origem: empresa, estrutura, catálogo, convênios (`regua-contratual.md`, `precos-<slug>.csv`, `contagens.md`, `farol.md`), pessoas, parâmetros, permissões |
| `dados/dicionario-de-ids.md` | nome ↔ ID de tudo que foi criado ou reaproveitado |
| `documentos-do-cliente/` | originais + `inventario.md` + fichas de extração |
| `provas/` | antes, resposta, depois e diff de cada carga |
| `decisoes/DECISOES.md` | toda decisão, com quem decidiu e quando |
| `pendencias/` | `LACUNAS.md` e `PENDENCIAS.md` — cada uma com dono e prazo |
| `sprints/` | checklist de S00–S17 com o status final |
| `historico/` | HISTORICO, APRENDIZADOS, dailies, reviews, mensagens verbatim |
| `diretrizes-da-equipe.md` | direcionamentos da equipe para futuras sessões |

## Armadilhas desta sprint

- Corrigir no susto, sem foto antes (uma correção "óbvia" num convênio fechado
  pode desfazer trabalho aprovado).
- Pendência sem dono e sem prazo.
- Lição que serve a todas as clínicas ficar só no repo da clínica: sugira ao
  mantenedor do kit (issue **sem nenhum dado da clínica**).
- Esquecer a validade da chave da integração contínua.

## Definition of Ready / Definition of Done

**DoR:** go-live feito (S16).

**DoD:**
- [ ] 5 varreduras diárias feitas e relatadas; semanais até o dia 30;
- [ ] correções feitas com ritual e registradas;
- [ ] dossiê completo, conferido item a item;
- [ ] nenhuma pendência sem dono e sem prazo;
- [ ] lições do método sugeridas ao mantenedor do kit (sem dados da clínica);
- [ ] a clínica opera sem a IA, e a próxima sessão consegue continuar sem o humano explicar nada.

## Checklist de itens

| # | item | status | origem | prova | observação |
|---|---|---|---|---|---|
| S17-01 | Varredura dia 1 | pendente | | historico/varreduras/ | |
| S17-02 | Varredura dia 2 | pendente | | | |
| S17-03 | Varredura dia 3 | pendente | | | |
| S17-04 | Varredura dia 4 | pendente | | | |
| S17-05 | Varredura dia 5 | pendente | | | |
| S17-06 | Varreduras semanais até o dia 30 | pendente | | | |
| S17-07 | Correções registradas (modo Atualização) | pendente | | | |
| S17-08 | Dossiê conferido item a item | pendente | | | |
| S17-09 | Pendências com dono e prazo | pendente | | | |
| S17-10 | Lições sugeridas ao kit (sem dados da clínica) | pendente | | | |
| S17-11 | Aceite de encerramento do dono | pendente | | | |

## O que registrar

- `historico/HISTORICO.md`: encerramento da implantação, com a data e a versão do kit usada.
- `historico/APRENDIZADOS.md`: lições.
- `ESTADO.md`: modo "operação", próximo passo concreto (ex.: "reajuste do <convênio> em <data>").
