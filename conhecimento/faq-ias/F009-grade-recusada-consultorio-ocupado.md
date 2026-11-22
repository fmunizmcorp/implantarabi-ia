# F009 — Grade do profissional/equipamento recusada: consultório já ocupado no horário

- **Rotas:** POST /grades-colaborador · PUT /grades-colaborador/{id} · POST /grades-equipamento · PUT /grades-equipamento/{id}
- **Status HTTP:** 400 | 409 | 422
- **Mensagem contém:** ocupado | conflito | já possui grade | local
- **Causa:** confirmada no manual (produção desde 18/11/2026, #707) — o Rabi recusa grade num local/
  consultório que já tem outra grade ativa no mesmo dia e horário. Status e texto exatos da recusa
  **não confirmados** pela API; confira a mensagem real
- **Status:** regra de negócio do Rabi
- **Origem:** manual oficial (atualizações de novembro/2026)

## O que fazer
Mostre ao usuário as duas grades em conflito (profissional, local, dias, horário) e pergunte qual
muda: outro local, outro horário ou encerrar a grade antiga. Lembre que **inativar uma grade realoca
os agendamentos futuros** dela (#708, parte 1) — isso é operação da clínica e só com ordem escrita.

## O que NÃO fazer
Não criar um local "Consultório 1B" só para escapar da regra sem o usuário decidir. Não inativar grade
antiga por conta própria.
