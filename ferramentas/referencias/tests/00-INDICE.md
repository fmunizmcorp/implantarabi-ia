# Testes das ferramentas de referências

> **Fonte:** código desta pasta · **Conferido em:** 2026-09-25
> **Vale para:** kit v0.1.0 · **Kit:** v0.1.0

| Arquivo | O que testa |
|---|---|
| [test_referencias.py](test_referencias.py) | normalização (mescla de edições do Brasíndice, SIMPRO com vigência e duplicados, CMED por CSV, fatiamento, manifest/sha256), busca (nome+dose, EAN, TUSS, registro ANVISA, material, CBHPM), tabelas da clínica prevalecendo (pasta e `config/referencias-da-clinica.md`) e enriquecimento (ÓTIMO por código, SEM MATCH, dose diferente = RESSALVA) |
| [\_\_init\_\_.py](__init__.py) | marca o pacote |

Todas as fixtures são **fictícias** ("LAB EXEMPLO", "FABRICA TESTE", códigos
inventados) e são criadas em pasta temporária pelo próprio teste.

Rodar: `python3 -m pytest ferramentas/referencias -q`
