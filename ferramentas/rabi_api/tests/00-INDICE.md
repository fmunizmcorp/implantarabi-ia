# Índice — testes de `ferramentas/rabi_api`

> **Fonte:** código deste kit · **Conferido em:** 2026-09-25
> **Vale para:** Kit v0.1.0 · **Kit:** v0.1.0

| Arquivo | O que testa |
|---|---|
| `test_cliente.py` | cliente contra servidor HTTP falso local: 5 formatos de envelope, paginação até `totalPages`, conferência de total, corpo vazio, 401/403/503 (sem loop), 429 com espera, lote 207 por `indice`, chave por ambiente/arquivo e máscara, 401 de rota com defeito, foto com máscara de dado pessoal, diff, `testar_chave` sem dados |
| `test_corpo_escrita.py` | conversor leitura → escrita: campos iguais aos do spec (`ServicoCreate`/`ProdutoCreate`), `somarItens`→`somarItems`, objetos aninhados/vínculos → IDs, erro listando faltantes, nome de leitura recusado em `complementos`, vínculo ambíguo |
| `test_gerar_rotas.py` | gerador de rotas: 268 operações / 191 caminhos / 25 grupos / 88 permissões, cada operação uma vez, arquivos ≤ 40 KB com cabeçalho, âncora do manual, extração do `swaggerDoc` e comparação de specs |

Rodar (da raiz do kit): `python3 -m pytest ferramentas/rabi_api -q`.
