# SIMPRO — material

> **Fonte:** coleta de portal de operadora que publica a tabela SIMPRO · **Conferido em:** 2026-09-25
> **Vale para:** referência de nomenclatura e códigos (edição 2026-04-12); preço só indicativo · **Kit:** v0.1.0

Descrição, fabricante, código SIMPRO (tabela 12) e valor vigente com data.

| Campo | Valor |
|---|---|
| Fonte | SIMPRO (publicação licenciada), via coleta de portal de operadora que publica a tabela SIMPRO |
| Edição | 2026-04-12 |
| Data da edição | 2026-04-12 (coleta) |
| Linhas | 203659 |
| Fatias | 42 |
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
| SIMPRO_MATERIAL_coleta.csv | 27287638 | `75ba78df3cd7669f…` |

## Fatias

Abra só a fatia da letra inicial do nome (ou use `ferramentas/referencias/buscar.py`).

| Arquivo | Prefixo | Linhas | Bytes | sha256 |
|---|---|---|---|---|
| [0-9.csv](0-9.csv) | 0-9 | 3 | 672 | `c536c3cb8d03e9d9…` |
| [A.csv](A.csv) | A | 10850 | 1555117 | `9bf82d4d11cee1f6…` |
| [B.csv](B.csv) | B | 10646 | 1532579 | `d5fdd33d1df67985…` |
| [CA-001.csv](CA-001.csv) | CA | 25861 | 3908053 | `b8c162367d191694…` |
| [CA-002.csv](CA-002.csv) | CA | 15436 | 2314990 | `c5964366a69249d7…` |
| [CE.csv](CE.csv) | CE | 688 | 107500 | `394e396dbf26ee2e…` |
| [CG.csv](CG.csv) | CG | 8 | 1399 | `2d0cfc5ae19bc481…` |
| [CH.csv](CH.csv) | CH | 79 | 10904 | `6d48aadd517062a7…` |
| [CI.csv](CI.csv) | CI | 1099 | 157851 | `87961f5610f12567…` |
| [CK.csv](CK.csv) | CK | 7 | 1215 | `f620f8c70cd4d110…` |
| [CL.csv](CL.csv) | CL | 578 | 81456 | `046074a107343421…` |
| [CO.csv](CO.csv) | CO | 5425 | 782510 | `2c0c446bb2aa44da…` |
| [CP.csv](CP.csv) | CP | 37 | 4799 | `f108f83e0208723b…` |
| [CR.csv](CR.csv) | CR | 152 | 21153 | `25a9c07a6dcf90e6…` |
| [CS.csv](CS.csv) | CS | 1 | 398 | `f37bd719516278e2…` |
| [CU.csv](CU.csv) | CU | 3622 | 556101 | `d663789f7b97b704…` |
| [CY.csv](CY.csv) | CY | 3 | 683 | `117774301446b2a4…` |
| [C_.csv](C_.csv) | C_ | 2 | 548 | `2107b47ccff83973…` |
| [D.csv](D.csv) | D | 3761 | 540320 | `c01ec58cc276919d…` |
| [E.csv](E.csv) | E | 13197 | 1980028 | `859a8af47e002b46…` |
| [F.csv](F.csv) | F | 17676 | 2650158 | `fbdf0c76468a4b85…` |
| [G.csv](G.csv) | G | 2222 | 312276 | `9aa14c0eace8e814…` |
| [H.csv](H.csv) | H | 2840 | 392679 | `ce275136e3f005de…` |
| [I.csv](I.csv) | I | 4830 | 721755 | `9b1086d4477db0d1…` |
| [J.csv](J.csv) | J | 292 | 39501 | `fc964e163560abbf…` |
| [K.csv](K.csv) | K | 9015 | 1373200 | `f3463842a5144864…` |
| [L.csv](L.csv) | L | 5822 | 838691 | `7e2014c226b61857…` |
| [M.csv](M.csv) | M | 9008 | 1301894 | `a92ea0ccb52ae764…` |
| [N.csv](N.csv) | N | 196 | 26399 | `36de07b4e26234b9…` |
| [O.csv](O.csv) | O | 1311 | 180538 | `d50fef75d4b751a0…` |
| [P.csv](P.csv) | P | 23176 | 3305637 | `c3479b985c0a7038…` |
| [Q.csv](Q.csv) | Q | 16 | 2498 | `43fa563b99b302c7…` |
| [R.csv](R.csv) | R | 1519 | 216526 | `1e954e7c1a11a09f…` |
| [S.csv](S.csv) | S | 24132 | 3571370 | `e1bdf3b8f26f5368…` |
| [T.csv](T.csv) | T | 7979 | 1134525 | `380655bac96d72b8…` |
| [U.csv](U.csv) | U | 277 | 41378 | `3ba87862f0e1c035…` |
| [V.csv](V.csv) | V | 984 | 142532 | `674a775f353c3455…` |
| [W.csv](W.csv) | W | 123 | 17987 | `dbaa07fcd8b2753a…` |
| [X.csv](X.csv) | X | 1 | 399 | `a52a7bee86175067…` |
| [Y.csv](Y.csv) | Y | 1 | 423 | `374714345c14abcf…` |
| [Z.csv](Z.csv) | Z | 3 | 713 | `7a9df5a82db8f97e…` |
| [_.csv](_.csv) | _ | 781 | 114320 | `2b27b0f41aa03cfb…` |
