# SIMPRO — reagente

> **Fonte:** coleta de portal de operadora que publica a tabela SIMPRO · **Conferido em:** 2026-09-25
> **Vale para:** referência de nomenclatura e códigos (edição 2026-04-12); preço só indicativo · **Kit:** v0.1.0

Descrição, fabricante, código SIMPRO (tabela 12) e valor vigente com data.

| Campo | Valor |
|---|---|
| Fonte | SIMPRO (publicação licenciada), via coleta de portal de operadora que publica a tabela SIMPRO |
| Edição | 2026-04-12 |
| Data da edição | 2026-04-12 (coleta) |
| Linhas | 57 |
| Fatias | 13 |
| Normalizado em | 2026-09-25 |
| Licença | licenciada — incluída só como referência de nomenclatura/códigos — ver [LICENCAS.md](../../LICENCAS.md) |

## Observações

- `produto` e `laboratorio` foram separados no último '. ' da descrição publicada (ex.: 'SERINGA 10ML. FABRICANTE.').
- Campo bruto 'Desde dd/mm/aaaa R$ x,xxx' separado em `vigencia` (AAAA-MM-DD) e `preco_ref`.
- Código repetido: ficou a vigência mais recente. Linhas inválidas ignoradas: 0.
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
| TST_SIMPRO_REAGENTE.csv | 5912 | `8dc44be6aecea1c9…` |

## Fatias

Abra só a fatia da letra inicial do nome (ou use `ferramentas/referencias/buscar.py`).

| Arquivo | Prefixo | Linhas | Bytes | sha256 |
|---|---|---|---|---|
| [A.csv](A.csv) | A | 23 | 3000 | `294f2a675c8dd261…` |
| [B.csv](B.csv) | B | 2 | 519 | `9c43787a290a6362…` |
| [C.csv](C.csv) | C | 8 | 1259 | `3640286b53aed1fc…` |
| [E.csv](E.csv) | E | 3 | 632 | `c945e859ac2df1b9…` |
| [F.csv](F.csv) | F | 3 | 609 | `42b6a0e90a3195aa…` |
| [G.csv](G.csv) | G | 5 | 843 | `57212fe9c86b5a10…` |
| [H.csv](H.csv) | H | 2 | 533 | `6545f87e0d2fd482…` |
| [I.csv](I.csv) | I | 2 | 524 | `c02635eedbc1b67c…` |
| [M.csv](M.csv) | M | 3 | 638 | `424cefe5c7f8efc0…` |
| [O.csv](O.csv) | O | 2 | 512 | `6056332ec9842d65…` |
| [P.csv](P.csv) | P | 1 | 415 | `5b45b5b916892cf2…` |
| [S.csv](S.csv) | S | 2 | 531 | `160650aa02600b80…` |
| [X.csv](X.csv) | X | 1 | 394 | `f2ad03ccdc4298f2…` |
