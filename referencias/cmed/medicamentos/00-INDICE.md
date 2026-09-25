# CMED — lista de preços de medicamentos (PF/PMC/PMVG)

> **Fonte:** https://www.gov.br/anvisa/pt-br/assuntos/medicamentos/cmed/precos · **Conferido em:** 2026-09-25
> **Vale para:** referência de nomenclatura e códigos (edição 20260508); preço só indicativo · **Kit:** v0.1.0

Preços regulados (teto) de medicamentos com substância, registro ANVISA, EAN e GGREM. Serve para achar o princípio ativo, o registro e o teto legal de preço.

| Campo | Valor |
|---|---|
| Fonte | CMED/ANVISA — Lista de preços de medicamentos |
| Edição | 20260508 |
| Data da edição | 2026-05-09 |
| Linhas | 25276 |
| Fatias | 26 |
| Normalizado em | 2026-09-25 |
| Licença | pública (ANVISA/CMED) — ver [LICENCAS.md](../../LICENCAS.md) |

## Observações

- pf_total/pmc_total = alíquota de ICMS 17% (a mesma base que o Brasíndice usa). Outras alíquotas em `precos_extra`; use a do estado da clínica.
- codigo_tuss preenchido pelo arquivo oficial 'Registros ANVISA na TUSS de medicamentos' (junção por registro).
- Quantidade por embalagem não é publicada de forma estruturada: pf_unit/pmc_unit ficam vazios.

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
| CMED_PMC_20260508.xlsx | 12201070 | `1b0845ff704af163…` |
| CMED_PMVG_PF_20260508.xlsx | 12901684 | `cbd02c251f803730…` |
| REGISTROS ANVISA NA TUSS DE MEDICAMENTOS VERS╟O 202601.xlsx | 1030047 | `569960541cfa0393…` |

## Fatias

Abra só a fatia da letra inicial do nome (ou use `ferramentas/referencias/buscar.py`).

| Arquivo | Prefixo | Linhas | Bytes | sha256 |
|---|---|---|---|---|
| [A.csv](A.csv) | A | 2387 | 1058022 | `16b4c072af86eeeb…` |
| [B.csv](B.csv) | B | 1189 | 523134 | `90ae79c2e5164cc9…` |
| [C.csv](C.csv) | C | 3638 | 1603795 | `e7b867468ccc9f7e…` |
| [D.csv](D.csv) | D | 1788 | 793398 | `6e3525d90028c782…` |
| [E.csv](E.csv) | E | 1190 | 523654 | `f1444cfe2caa8bcd…` |
| [F.csv](F.csv) | F | 1076 | 448676 | `6c1b63409db69a44…` |
| [G.csv](G.csv) | G | 613 | 263279 | `98fae612179a89ae…` |
| [H.csv](H.csv) | H | 833 | 369707 | `b841cce98471a65b…` |
| [I.csv](I.csv) | I | 622 | 271864 | `ec818d4827b92a49…` |
| [J.csv](J.csv) | J | 78 | 34790 | `5e8ee2ffc0cf7de7…` |
| [K.csv](K.csv) | K | 245 | 110189 | `b64e7809c2260468…` |
| [L.csv](L.csv) | L | 1364 | 596169 | `64866da49edda1f2…` |
| [M.csv](M.csv) | M | 1351 | 582211 | `c62060fc5edb96c2…` |
| [N.csv](N.csv) | N | 933 | 427245 | `93d1d70252bfcaad…` |
| [O.csv](O.csv) | O | 936 | 411158 | `8a2d0bc33283d129…` |
| [P.csv](P.csv) | P | 1427 | 637635 | `50070253422d2146…` |
| [Q.csv](Q.csv) | Q | 101 | 47313 | `a818c4a7db2e9942…` |
| [R.csv](R.csv) | R | 1060 | 467438 | `44268a80b1626b8a…` |
| [S.csv](S.csv) | S | 1396 | 621274 | `3c9caed380bef5e1…` |
| [T.csv](T.csv) | T | 1319 | 578383 | `f448bd6756d92bd5…` |
| [U.csv](U.csv) | U | 131 | 57253 | `cc9581521243be10…` |
| [V.csv](V.csv) | V | 1042 | 475353 | `2be5923299c3f9ac…` |
| [W.csv](W.csv) | W | 45 | 21018 | `eca3cf3b39331245…` |
| [X.csv](X.csv) | X | 165 | 72868 | `3c3f1856594e45f0…` |
| [Y.csv](Y.csv) | Y | 20 | 9859 | `1c3ef4269a105424…` |
| [Z.csv](Z.csv) | Z | 327 | 141384 | `3d27cc010cc7d9d3…` |
