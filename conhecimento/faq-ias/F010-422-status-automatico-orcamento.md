# F010 — 422/409 ao mudar status de orçamento

- **Rotas:** PUT /orcamentos/status/{idOrcamento}/{idStatus}
- **Status HTTP:** 422 | 409
- **Mensagem contém:** automático | ORCAMENTO_CANCELAR | motivo
- **Causa:** confirmada (Swagger 22/11) — os status **automáticos** (8 Vencido, 10 Pago, 11 Agendado,
  12 Concluído, 13 Renegociado; campo `automatico: true` em `GET /orcamentos/status`) só o sistema grava
  → **422**. Com o status automático ativo na clínica só valem as trocas permitidas (ex.: Vencido → só
  Cancelado); cancelar exige `motivo` e, havendo agendamento futuro ou pagamento, responde **409**
  `ORCAMENTO_CANCELAR_CONFI…` pedindo confirmação
- **Status:** regra de negócio
- **Origem:** Swagger de 22/11/2026

## O que fazer
Orçamento é operação da clínica: **só com ordem escrita**. Mostre ao dono o motivo da recusa e o que
o Rabi exige (motivo, confirmação). Na implantação, não há razão para mexer em status de orçamento real.

## O que NÃO fazer
Não tentar gravar status automático. Não confirmar cancelamento com agendamento/pagamento sem ordem.
