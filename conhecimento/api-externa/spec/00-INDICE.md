# spec/ — snapshots do Swagger (OpenAPI 3.0) da API externa

| Arquivo | O que é |
|---|---|
| `openapi-2026-09-25.json` | spec publicado em https://api.rabisistemas.com.br/external-docs/ em 25/09/2026 — 191 caminhos, 268 operações, 155 schemas, v1.0.0 |
| `openapi-2026-09-28.json` | 28/09/2026 — 192 caminhos, 269 operações (rota nova `GET /convenios/{id}/farol/itens/{servicoRaizId}`) |
| `openapi-2026-11-22.json` | **atual** — 22/11/2026: 198 caminhos, 277 operações (+ `/financeiro/contas-caixa` ×5, `pagamentos/confirmacao`, `xml-tiss`, `xml-tiss/casar-historico`); PUT parcial declarado em 13 rotas; 403 com `escopoFaltante`; descrição oficial de `rbt_`/`rbk_` |

Não leia o JSON inteiro: use `../rotas/00-INDICE.md` (gerado dele) ou `grep`.
Para atualizar: `python3 ferramentas/rabi_api/atualizar_spec.py` (baixa, compara e regenera `rotas/`).
