# Índice — ferramentas/conversao

> **Fonte:** manual https://www.rabisistemas.com.br/manual/precos/guia-ia.html#algoritmo + spec `openapi-2026-09-25.json` · **Conferido em:** 2026-09-25
> **Vale para:** produção desde 23–25/09/2026 · **Kit:** v0.1.0

| Arquivo | O que tem | Quando ler/usar |
|---|---|---|
| [README.md](README.md) | Fluxo completo, formato do CSV, mapa coluna → API, interpretações e limitações | Antes de configurar um convênio |
| `modelo.py` | Classes de dados e leitura do cenário JSON | Ao montar o cenário |
| `motor.py` | Árvores do manual: valor, custo, Farol, orçamento, 4 linhas, invariantes | Ao investigar um número |
| `montar_cenario.py` | CLI: fotos da API + políticas da régua → `cenario.json` do simulador, com a lista de lacunas | Antes de simular um convênio real |
| `simulador.py` | CLI de previsão por serviço (🔒 🔁 ✅ Σ, custo, Farol, itens) | Antes de gravar |
| `montar_convenio.py` | CLI: CSV com origem → lotes dos PUT + `previa.md` | Para a prévia e a gravação |
| `conferir_farol.py` | CLI: previsão × GET `/farol/servicos`, `/itens`, `/produtos` | Depois de gravar |
| [exemplos/00-INDICE.md](exemplos/00-INDICE.md) | Cenário fictício "Convênio A" | Para aprender o formato |
| [tests/00-INDICE.md](tests/00-INDICE.md) | T1–T26, invariantes, CLIs, campos × spec | Para conferir o motor |
