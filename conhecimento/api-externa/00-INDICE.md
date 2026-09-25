# Índice — API externa do Rabi

> **Fonte:** Swagger https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · manual https://www.rabisistemas.com.br/manual/api-externa/ · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger de 25/09/2026) · **Kit:** v0.1.0

Leia por aqui; abra só o arquivo de que precisa. Para uma rota específica, vá direto a
[rotas/00-INDICE.md](rotas/00-INDICE.md) ou use
`grep -rn "POST /servicos" conhecimento/api-externa/rotas/`.

| Arquivo | O que tem | Quando ler |
|---|---|---|
| [visao-geral.md](visao-geral.md) | o que é, URLs, Swagger, os 25 grupos com contagem, API externa × interna × tela, novidades | primeira vez; dúvida de "a API faz isso?" |
| [chave-e-token.md](chave-e-token.md) | chave `rbk_`, como configurar na clínica (`RABI_API_KEY` + `credenciais/rabi-api-externa.md`), validade, revogação, teste, kit mínimo e as 88 permissões | S00; troca de chave; 401/403/503 |
| [convencoes.md](convencoes.md) | paginação, envelope e exceções, reais × centavos, UF, `responsavelId`, PUT (upsert × sobrescrita × não declarado), DELETE, lotes 207/429/45 s, códigos de erro, idempotência | antes de qualquer leitura ou gravação nova |
| [ordem-de-carga-via-api.md](ordem-de-carga-via-api.md) | passos 0 a 14 com rotas e dependências, ligados às sprints S00–S17; checklist de fechamento | planejar a sprint; erro 422 |
| [proibidas-sem-ordem-escrita.md](proibidas-sem-ordem-escrita.md) | NFS-e, dinheiro, estoque, agenda/orçamento/atendimento, DELETE, lote sem prévia, login, LGPD, rotas internas | antes de chamar qualquer rota com efeito externo |
| [nao-coberto-e-api-interna.md](nao-coberto-e-api-interna.md) | o que a API não cobre, ids que só existem na tela, rotas que não funcionam com chave, API interna como último recurso | quando a rota não existe |
| [defeitos-conhecidos.md](defeitos-conhecidos.md) | defeitos corrigidos e abertos (25/09), como detectar em execução, contornos | resposta estranha (500 que gravou, 401 que não é chave, corpo `0`/`null`) |
| [rotas/00-INDICE.md](rotas/00-INDICE.md) | **gerado do spec**: um arquivo por grupo, cada operação com permissão, parâmetros, corpo e respostas (268 operações) | montar uma chamada |
| `spec/openapi-2026-09-25.json` | o spec OpenAPI oficial (743 KB) — **não abra inteiro**; use as rotas geradas ou `grep` | só o gerador e o atualizador leem |

Ferramentas Python (cliente, foto/diff, teste da chave, atualizador do spec):
[../../ferramentas/rabi_api/00-INDICE.md](../../ferramentas/rabi_api/00-INDICE.md).
