# Tabela 87 — tabela de tabelas (referência do código do item)

> **Fonte:** https://www.rabisistemas.com.br/manual/modulos/configuracoes.html · **Conferido em:** 2026-09-25
> **Vale para:** referência de nomenclatura e códigos (edição 4.03.00); preço só indicativo · **Kit:** v0.1.0

Diz de qual tabela é o código do item na guia: 20 medicamento TUSS, 19 material TUSS, 05 Brasíndice, 12 SIMPRO…

| Campo | Valor |
|---|---|
| Fonte | ANS (XSD TISS dm_tabela/dm_tabelaGeral) + manual do Sistema Rabi (domínio do convênio) |
| Edição | 4.03.00 |
| Data da edição |  |
| Linhas | 10 |
| Fatias | 1 |
| Normalizado em | 2026-09-25 |
| Licença | pública (ANS) — ver [LICENCAS.md](../../LICENCAS.md) |

## Observações

- Não confundir: Tabela 36 = indicador de acidente; Tabela 87 = tabela de tabelas.
- Qual tabela usar no convênio (TUSS 20/19 ou 05/12) é definido pelo contrato do convênio.

## Colunas

| Coluna | Significado |
|---|---|
| `codigo` | Código da tabela. |
| `descricao` | Descrição. |
| `base` | De onde veio a descrição. |

## Origem (arquivos brutos)

| Arquivo | Bytes | sha256 |
|---|---|---|

## Fatias

Abra só a fatia da letra inicial do nome (ou use `ferramentas/referencias/buscar.py`).

| Arquivo | Prefixo | Linhas | Bytes | sha256 |
|---|---|---|---|---|
| [dados.csv](dados.csv) | — | 10 | 862 | `67b2d7601be45910…` |
