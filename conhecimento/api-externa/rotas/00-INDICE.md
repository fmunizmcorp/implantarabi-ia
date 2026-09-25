# Índice das rotas da API externa

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 ferramentas/rabi_api/atualizar_spec.py` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

Um arquivo por grupo (tag) do Swagger, na ordem do roteiro de implantação do manual (https://www.rabisistemas.com.br/manual/api-externa/index.html#mapa-grupos). Leia só o grupo de que precisa. Para achar uma rota: `grep -rn "PUT /convenios/{id}/servicos" conhecimento/api-externa/rotas/`.

| # | Grupo | Operações | Arquivo(s) | Página do manual |
|---|---|---|---|---|
| 1 | Empresas | 5 | [empresas.md](empresas.md) | [referencia-cadastros.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#grupo-empresas) |
| 2 | Depósitos | 6 | [depositos.md](depositos.md) | [referencia-cadastros.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#grupo-depositos) |
| 3 | Locais | 5 | [locais.md](locais.md) | [referencia-cadastros.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#grupo-locais) |
| 4 | Auxiliares | 14 | [auxiliares.md](auxiliares.md) | [referencia-cadastros.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#grupo-auxiliares) |
| 5 | Operadoras | 6 | [operadoras.md](operadoras.md) | [referencia-cadastros.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#grupo-operadoras) |
| 6 | Fornecedores | 5 | [fornecedores.md](fornecedores.md) | [referencia-cadastros.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#grupo-fornecedores) |
| 7 | Fabricantes | 6 | [fabricantes.md](fabricantes.md) | [referencia-cadastros.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#grupo-fabricantes) |
| 8 | Taxas | 6 | [taxas.md](taxas.md) | [referencia-cadastros.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#grupo-taxas) |
| 9 | Produtos | 6 | [produtos.md](produtos.md) | [referencia-cadastros.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#grupo-produtos) |
| 10 | Equipamentos | 6 | [equipamentos.md](equipamentos.md) | [referencia-cadastros.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#grupo-equipamentos) |
| 11 | Serviços | 6 | [servicos.md](servicos.md) | [referencia-cadastros.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#grupo-servicos) |
| 12 | Colaboradores | 7 | [colaboradores.md](colaboradores.md) | [referencia-cadastros.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#grupo-colaboradores) |
| 13 | Tabelas de Preço | 8 | [tabelas-de-preco.md](tabelas-de-preco.md) | [referencia-cadastros.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#grupo-tabelas-preco) |
| 14 | Convênios | 21 | [convenios-parte-1.md](convenios-parte-1.md) · [convenios-parte-2.md](convenios-parte-2.md) | [referencia-cadastros.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#grupo-convenios) |
| 15 | Grade de Colaborador | 7 | [grade-de-colaborador.md](grade-de-colaborador.md) | [referencia-cadastros.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#grupo-grade-colaborador) |
| 16 | Grade de Equipamento | 5 | [grade-de-equipamento.md](grade-de-equipamento.md) | [referencia-cadastros.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#grupo-grade-equipamento) |
| 17 | Financeiro | 5 | [financeiro.md](financeiro.md) | [referencia-operacao.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#grupo-financeiro) |
| 18 | Estoque | 12 | [estoque.md](estoque.md) | [referencia-operacao.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#grupo-estoque) |
| 19 | Pacientes | 11 | [pacientes.md](pacientes.md) | [referencia-cadastros.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#grupo-pacientes) |
| 20 | Parâmetros | 45 | [parametros-parte-1.md](parametros-parte-1.md) · [parametros-parte-2.md](parametros-parte-2.md) | [referencia-parametros.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-parametros.html#grupo-parametros) |
| 21 | Agendamentos | 8 | [agendamentos.md](agendamentos.md) | [referencia-operacao.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#grupo-agendamentos) |
| 22 | Orçamentos | 10 | [orcamentos.md](orcamentos.md) | [referencia-operacao.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#grupo-orcamentos) |
| 23 | Atendimentos | 6 | [atendimentos.md](atendimentos.md) | [referencia-operacao.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#grupo-atendimentos) |
| 24 | Faturamento | 24 | [faturamento.md](faturamento.md) | [referencia-operacao.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#grupo-faturamento) |
| 25 | NFS-e | 28 | [nfse.md](nfse.md) | [referencia-operacao.html](https://www.rabisistemas.com.br/manual/api-externa/referencia-operacao.html#grupo-nfse) |
| | **Total** | **268** | 27 arquivos | 191 caminhos |

**Conferência:** soma das operações = **268** (esperado no Swagger de 25/09/2026: 268); caminhos = **191** (esperado: 191).
