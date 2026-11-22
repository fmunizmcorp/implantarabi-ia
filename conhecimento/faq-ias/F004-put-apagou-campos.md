# F004 — Depois de um PUT, campos ou vínculos que eu não queria mudar sumiram

- **Rotas:** PUT /servicos/{id} · PUT /pacientes/{id} · PUT /convenios/{id} · PUT /colaboradores/{id} · PUT /produtos/{id} · outros PUT
- **Status HTTP:** 200 | 202
- **Mensagem contém:** —
- **Causa:** confirmada — depende da rota (rabi-api `7d16cd50`/`49362b61`, produção desde 01–02/10/2026):
  - nas **rotas parciais** (serviço, convênio, paciente e carteira, colaborador, grades, orçamento,
    movimentação, guia, conta/caixa) campo **omitido mantém**. Se algo sumiu, foi porque o corpo levou
    **`null`** naquele campo ou uma **lista** incompleta/`[]` — lista enviada **substitui** os vínculos;
  - nas rotas que **não declaram** (produto, taxa, equipamento, local, depósito, fornecedor, fabricante,
    tabela de preço, parâmetros…) e em `PUT /empresas` o PUT **sobrescreve**: campo omitido = apagado;
  - antes de **01/10/2026** todo PUT de serviço/paciente/convênio também sobrescrevia (gravações antigas: F006)
- **Status:** comportamento do Rabi (documentado)
- **Origem:** implantação real anterior + código do Rabi + Swagger de 22/11/2026

## O que fazer
1. Compare a foto antes com a foto depois e o **corpo enviado** (guardado nas provas): qual campo foi
   com `null`? qual lista foi enviada?
2. Restaure a partir da foto antes: nas rotas parciais, mande **só** o campo/lista a restaurar
   (lista **completa**); nas demais, o objeto completo.
3. Daí em diante gere o corpo com `ferramentas/rabi_api/corpo_escrita.py` — `modo="parcial"` manda só o
   que mudou e recusa lista vazia sem confirmação explícita. Regra por rota:
   [../api-externa/convencoes.md](../api-externa/convencoes.md) §4.

## O que NÃO fazer
Não mandar o GET de volta "como veio" sem conferir: em convênio, `unidadesIds` e
`politicasPorTipoProduto` incompletos **desativam unidades / apagam políticas**. Não mandar `[]` para
"limpar" sem prévia aprovada.
