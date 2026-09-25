# TUSS — registros ANVISA dos medicamentos (terminologia 20)

> **Fonte:** https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss · **Conferido em:** 2026-09-25
> **Vale para:** referência de nomenclatura e códigos (edição 202601); preço só indicativo · **Kit:** v0.1.0

Liga o registro ANVISA (13 dígitos) ao código TUSS do medicamento.

| Campo | Valor |
|---|---|
| Fonte | ANS — arquivo auxiliar 'Registros ANVISA na TUSS de medicamentos' |
| Edição | 202601 |
| Data da edição | 202601 |
| Linhas | 42936 |
| Fatias | 1 |
| Normalizado em | 2026-09-25 |
| Licença | pública (ANS) — ver [LICENCAS.md](../../LICENCAS.md) |

## Colunas

| Coluna | Significado |
|---|---|
| `codigo_tuss` | Código do termo na terminologia 20. |
| `registro_anvisa` | Registro ANVISA (só dígitos). |

## Origem (arquivos brutos)

| Arquivo | Bytes | sha256 |
|---|---|---|
| REGISTROS ANVISA NA TUSS DE MEDICAMENTOS VERS╟O 202601.xlsx | 1030047 | `569960541cfa0393…` |

## Fatias

Abra só a fatia da letra inicial do nome (ou use `ferramentas/referencias/buscar.py`).

| Arquivo | Prefixo | Linhas | Bytes | sha256 |
|---|---|---|---|---|
| [dados.csv](dados.csv) | — | 42936 | 987538 | `d4739077593e54e8…` |
