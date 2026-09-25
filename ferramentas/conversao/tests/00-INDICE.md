# Índice — testes do motor de conversão

> **Fonte:** https://www.rabisistemas.com.br/manual/precos/guia-ia.html#casos-de-teste e #invariantes · **Conferido em:** 2026-09-25
> **Vale para:** produção desde 23–25/09/2026 · **Kit:** v0.1.0

Rodar: `python3 -m pytest ferramentas/conversao -q` (na raiz do kit).

| Arquivo | O que testa |
|---|---|
| `test_casos_manual.py` | T1–T26 (um teste por caso, ids "T1".."T26"), exemplos 4.1/4.2/subserviço 540, herança de produto e Fator K, invariantes I1–I13, Zerar sem pacote, circularidade |
| `test_cli.py` | simulador, montar_convenio (fases, vazio × zero, erros, lotes ≤ 200, **todo campo gerado existe no schema do spec**), conferir_farol |
| `conftest.py` | Põe a raiz do kit no caminho de importação |
