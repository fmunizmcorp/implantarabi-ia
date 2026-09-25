# spec/ — snapshots do Swagger (OpenAPI 3.0) da API externa

| Arquivo | O que é |
|---|---|
| `openapi-2026-09-25.json` | spec publicado em https://api.rabisistemas.com.br/external-docs/ em 25/09/2026 — 191 caminhos, 268 operações, 155 schemas, v1.0.0 |

Não leia o JSON inteiro: use `../rotas/00-INDICE.md` (gerado dele) ou `grep`.
Para atualizar: `python3 -m ferramentas.rabi_api.atualizar_spec` (baixa, compara e regenera `rotas/`).
