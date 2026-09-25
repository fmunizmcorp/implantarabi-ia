# SIMPRO — saneante

> **Fonte:** coleta de portal de operadora que publica a tabela SIMPRO · **Conferido em:** 2026-09-25
> **Vale para:** referência de nomenclatura e códigos (edição 2026-04-12); preço só indicativo · **Kit:** v0.1.0

Descrição, fabricante, código SIMPRO (tabela 12) e valor vigente com data.

| Campo | Valor |
|---|---|
| Fonte | SIMPRO (publicação licenciada), via coleta de portal de operadora que publica a tabela SIMPRO |
| Edição | 2026-04-12 |
| Data da edição | 2026-04-12 (coleta) |
| Linhas | 711 |
| Fatias | 19 |
| Normalizado em | 2026-09-25 |
| Licença | licenciada — incluída só como referência de nomenclatura/códigos — ver [LICENCAS.md](../../LICENCAS.md) |

## Observações

- `produto` e `laboratorio` foram separados no último '. ' da descrição publicada (ex.: 'SERINGA 10ML. FABRICANTE.').
- Campo bruto 'Desde dd/mm/aaaa R$ x,xxx' separado em `vigencia` (AAAA-MM-DD) e `preco_ref`.
- Código repetido: ficou a vigência mais recente. Linhas inválidas ignoradas: 14.
- Colunas sempre vazias ou constantes na coleta (capítulo, grupo, especialidade 'Todas'…) foram descartadas.

## Colunas

| Coluna | Significado |
|---|---|
| `fonte` | Tabela de origem (BRASINDICE, SIMPRO ou CMED). |
| `edicao` | Edição/competência da publicação usada. |
| `tipo_item` | medicamento, material, saneante ou reagente. |
| `codigo_fonte` | Código do item na própria tabela (Brasíndice: código TISS de 10 dígitos; SIMPRO: código de 10 dígitos; CMED: código GGREM). |
| `tabela_fonte` | Código da Tabela 87 (TISS) que acompanha `codigo_fonte` na guia: 05 Brasíndice, 12 SIMPRO; vazio na CMED. |
| `chave_fonte` | Chave interna da publicação (Brasíndice: laboratório-produto-apresentação). |
| `laboratorio` | Laboratório/fabricante. |
| `produto` | Nome comercial ou descrição curta, como publicado. |
| `apresentacao` | Apresentação (forma, concentração, embalagem), como publicada. |
| `principio_ativo` | Substância. CMED publica; no Brasíndice vem da CMED pelo EAN (ou registro). |
| `ean` | Código de barras (EAN-13). |
| `registro_anvisa` | Registro ANVISA (13 dígitos em medicamento). |
| `codigo_tuss` | Código TUSS (20 medicamentos, 19 materiais, 18 taxas). |
| `ggrem` | Código GGREM da CMED. |
| `generico` | S = genérico; N = não; vazio = não informado. |
| `restrito_hospitalar` | S = uso restrito a hospital/clínica (PMC costuma ser 0 — normal). |
| `qtd_embalagem` | Unidades por embalagem (quando a fonte informa). |
| `pf_total` | Preço Fábrica da embalagem (R$). |
| `pmc_total` | Preço Máximo ao Consumidor da embalagem (R$). |
| `pf_unit` | PF por unidade (R$). |
| `pmc_unit` | PMC por unidade (R$). |
| `preco_ref` | Preço único publicado quando não há PF/PMC (SIMPRO, em geral por unidade/fração). |
| `tipo_preco` | Código curto da base do preço: BRAS_PF_PMC = PF/PMC do Brasíndice (ICMS 17%; PMC 0 em restrito hospitalar é normal); CMED_ICMS17 = PF/PMC CMED com ICMS 17% (outras alíquotas em precos_extra); SIMPRO_VIG = valor vigente SIMPRO (em geral por unidade/fração, 3 casas). |
| `vigencia` | Data (AAAA-MM-DD) ou edição da última alteração de preço do item. |
| `tabela87_sugerida` | Tabela TUSS sugerida para o item: 20 medicamento, 19 material. Conferir com o contrato do convênio. |
| `precos_extra` | CMED: preços em outras alíquotas de ICMS (PF0, PF12, PF18…, PMC18…, PMVG17…). |

## Origem (arquivos brutos)

| Arquivo | Bytes | sha256 |
|---|---|---|
| SIMPRO_SANEANTE_coleta.csv | 85995 | `11854b3be8b8a1fb…` |

## Fatias

Abra só a fatia da letra inicial do nome (ou use `ferramentas/referencias/buscar.py`).

| Arquivo | Prefixo | Linhas | Bytes | sha256 |
|---|---|---|---|---|
| [A.csv](A.csv) | A | 173 | 23095 | `0952c4baded564a2…` |
| [B.csv](B.csv) | B | 18 | 2696 | `3113de313553f982…` |
| [C.csv](C.csv) | C | 43 | 5765 | `1da15f2a3ef18610…` |
| [D.csv](D.csv) | D | 190 | 28199 | `0ab16f1d5fd10383…` |
| [E.csv](E.csv) | E | 11 | 1664 | `9492d4ffbc3b99c1…` |
| [F.csv](F.csv) | F | 19 | 2643 | `2b943ff79b4b67f1…` |
| [G.csv](G.csv) | G | 21 | 2972 | `4d8391b16f7ab2aa…` |
| [H.csv](H.csv) | H | 46 | 5940 | `601f0cb76a3ccbfc…` |
| [I.csv](I.csv) | I | 29 | 4513 | `b1a69a516cfa6237…` |
| [K.csv](K.csv) | K | 5 | 903 | `9ef4a0e7e4adb251…` |
| [L.csv](L.csv) | L | 27 | 4078 | `26089747f8b6574a…` |
| [M.csv](M.csv) | M | 12 | 1753 | `6a5c6f20f526072b…` |
| [N.csv](N.csv) | N | 11 | 1839 | `6fd8826a200ba173…` |
| [O.csv](O.csv) | O | 11 | 1788 | `010f3b631f8de8a6…` |
| [P.csv](P.csv) | P | 24 | 3393 | `8d77f943cbb602e7…` |
| [R.csv](R.csv) | R | 29 | 4087 | `80f4a349293de7d6…` |
| [S.csv](S.csv) | S | 35 | 5077 | `e52743dcc9015fc2…` |
| [V.csv](V.csv) | V | 6 | 991 | `ae07ee0e84e5e959…` |
| [X.csv](X.csv) | X | 1 | 395 | `1a3977fcfa4f4d22…` |
