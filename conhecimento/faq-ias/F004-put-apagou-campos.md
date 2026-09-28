# F004 — Depois de um PUT, campos que não mandei ficaram vazios

- **Rotas:** PUT /servicos/{id} · PUT /pacientes/{id} · PUT /convenios/{id} · outros PUT
- **Status HTTP:** 200
- **Mensagem contém:** —
- **Causa:** confirmada — PUT sobrescreve o registro inteiro (campo omitido = apagado)
- **Status:** comportamento do Rabi (documentado)
- **Origem:** implantação real anterior

## O que fazer
GET antes → alterar só o necessário → PUT com o objeto **completo** (serviço/produto
convertidos por `ferramentas/rabi_api/corpo_escrita.py`). Se já apagou: restaure a partir
da foto antes. Detalhe: [../api-externa/convencoes.md](../api-externa/convencoes.md) §4 e
lições da API em [../licoes-aprendidas/api.md](../licoes-aprendidas/api.md).
