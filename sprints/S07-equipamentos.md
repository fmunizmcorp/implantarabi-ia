# S07 — Equipamentos

> **Fonte:** https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-7 · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-7 · spec `openapi-2026-09-25.json` (`POST /equipamentos`, `/equipamentos/bulk`) · **Conferido em:** 2026-09-25
> **Vale para:** produção · **Kit:** v0.1.0

## Objetivo

Os aparelhos que a agenda precisa reservar (ultrassom, eletrocardiógrafo,
cadeira de infusão…) existem, para entrar na composição dos serviços (S08) e
ganhar grade (S10). Clínica sem aparelho reservável: sprint `n/a`, com motivo.

## Link do manual

- Etapa 7: https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-7
- Tela: https://www.rabisistemas.com.br/manual/modulos/configuracoes.html#equipamentos
- Pela API: https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-7

## Depende de

S03 (locais — a grade do equipamento vai apontar para um local).

## Documentos a pedir

FA-5 (equipamentos), PE-2 (horários dos equipamentos, usado na S10).

## Índice de dados a coletar

| dado | campo API | obrigatório? | onde costuma estar no material do cliente | padrão sugerível | pergunta ao usuário se faltar |
|---|---|---|---|---|---|
| Nome do equipamento | `nome` | sim (único entre os ativos) | lista de equipamentos, contrato de manutenção, agenda atual | "<Aparelho> — <Sala>" (ex.: "Ultrassom — Sala 2") | "Quais aparelhos precisam ser reservados na agenda, e em que sala ficam?" |
| Sala onde fica | (grade, S10) | para a grade | escala | o local da S03 | "O <aparelho> fica em qual sala?" |
| Horário de uso | (grade, S10) | para a grade | escala | o horário da sala | — |

## Fila de perguntas

1. "A clínica tem aparelho que precisa ser reservado na agenda?" (se não:
   sprint `n/a`).
2. Confirmar a lista e a sala de cada um.
3. Sugerir o padrão de nome.

## Enriquecimento possível

Nenhum relevante.

## Leitura do que já existe no Rabi e regra de não perder nada

- `GET /equipamentos?ativo=true` e `GET /equipamentos` — casar por nome
  normalizado. Existe → reutilizar.

## Gravação

| Ordem | Rota | Permissão | Lote |
|---|---|---|---|
| 1 | `POST /equipamentos` (o primeiro) | `equipamento:create` | — |
| 2 | `POST /equipamentos/bulk` (chave `equipamentos`) | `equipamento:create` | até 50 |
| Correção | `GET /equipamentos/{id}` → `PUT /equipamentos/{id}` completo | `equipamento:update` | — |

- Corpo mínimo: `{"nome":"Ultrassom — Sala 2"}`.
- 409 = já existe equipamento **ativo** com o mesmo nome → reutilizar.
- Guardar `equipamentoId`: composição do serviço (`equipamentoIds`, S08) e grade
  do equipamento (S10).

## Prova

- `provas/S07/equipamento-<slug>/`. Review: nome, sala prevista, ativo.

## Armadilhas desta sprint

- A **grade** do equipamento não é aqui: vem depois dos convênios (S10).
- `POST|PUT|DELETE /grades-equipamento` tem defeito documentado: grava e devolve
  500. Na S10, confira pela leitura em vez de repetir a chamada.
- Dois aparelhos iguais em salas diferentes precisam de nomes diferentes.

## Definition of Ready / Definition of Done

**DoR:** locais existentes (S03); FA-5 ou lista confirmada.

**DoD:**
- [ ] todo equipamento reservável existe, lido de volta (ou sprint `n/a` com motivo);
- [ ] `equipamentoId` no dicionário; provas salvas.

## Checklist de itens

| # | item | status | origem | prova | observação |
|---|---|---|---|---|---|
| S07-01 | Clínica tem equipamento reservável? | pendente | | | se não, demais itens `n/a` |
| S07-02 | Lista de equipamentos e salas confirmada | pendente | | | |
| S07-03 | Equipamento <nome> (uma linha por equipamento) | pendente | | provas/S07/ | |
| S07-04 | Dicionário de IDs (equipamentoId) | pendente | | | |

## O que registrar

- `dados/estrutura/equipamentos.md` (nome, sala, horário previsto, ID).
- `ESTADO.md`: próximo passo = S08.
