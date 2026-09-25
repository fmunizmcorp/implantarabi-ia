# SIMPRO — material

> **Fonte:** coleta de portal de operadora que publica a tabela SIMPRO · **Conferido em:** 2026-09-25
> **Vale para:** referência de nomenclatura e códigos (edição 2026-04-12); preço só indicativo · **Kit:** v0.1.0

Descrição, fabricante, código SIMPRO (tabela 12) e valor vigente com data.

| Campo | Valor |
|---|---|
| Fonte | SIMPRO (publicação licenciada), via coleta de portal de operadora que publica a tabela SIMPRO |
| Edição | 2026-04-12 |
| Data da edição | 2026-04-12 (coleta) |
| Linhas | 202484 |
| Fatias | 41 |
| Normalizado em | 2026-09-25 |
| Licença | licenciada — incluída só como referência de nomenclatura/códigos — ver [LICENCAS.md](../../LICENCAS.md) |

## Observações

- `produto` e `laboratorio` foram separados no último '. ' da descrição publicada (ex.: 'SERINGA 10ML. FABRICANTE.').
- Campo bruto 'Desde dd/mm/aaaa R$ x,xxx' separado em `vigencia` (AAAA-MM-DD) e `preco_ref`.
- Código repetido: ficou a vigência mais recente. Linhas inválidas ignoradas: 1175.
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
| TST_SIMPRO_MATERIAL.csv | 27287638 | `75ba78df3cd7669f…` |

## Fatias

Abra só a fatia da letra inicial do nome (ou use `ferramentas/referencias/buscar.py`).

| Arquivo | Prefixo | Linhas | Bytes | sha256 |
|---|---|---|---|---|
| [0-9.csv](0-9.csv) | 0-9 | 3 | 672 | `c536c3cb8d03e9d9…` |
| [A.csv](A.csv) | A | 10853 | 1555477 | `64dda27aa84a7f17…` |
| [B.csv](B.csv) | B | 10624 | 1530067 | `2b9e0c9d3cd4d9e1…` |
| [CA-001.csv](CA-001.csv) | CA | 26505 | 4006747 | `0e3c745c353f651e…` |
| [CA-002.csv](CA-002.csv) | CA | 14967 | 2242248 | `fe2b97c3f5410ffe…` |
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
| [E.csv](E.csv) | E | 13152 | 1973651 | `d0514a8402051f9b…` |
| [F.csv](F.csv) | F | 17747 | 2660695 | `d6a7d67451aab403…` |
| [G.csv](G.csv) | G | 2222 | 312276 | `9aa14c0eace8e814…` |
| [H.csv](H.csv) | H | 2836 | 392063 | `c27afbd87584a170…` |
| [I.csv](I.csv) | I | 4773 | 714505 | `0229da799174e032…` |
| [J.csv](J.csv) | J | 292 | 39501 | `fc964e163560abbf…` |
| [K.csv](K.csv) | K | 9015 | 1373200 | `f3463842a5144864…` |
| [L.csv](L.csv) | L | 5813 | 837574 | `2c77504936d2d75e…` |
| [M.csv](M.csv) | M | 9007 | 1301736 | `3bc0788cf8fe53eb…` |
| [N.csv](N.csv) | N | 196 | 26399 | `36de07b4e26234b9…` |
| [O.csv](O.csv) | O | 1311 | 180538 | `d50fef75d4b751a0…` |
| [P.csv](P.csv) | P | 22768 | 3254600 | `82e543d9334d1b8b…` |
| [Q.csv](Q.csv) | Q | 16 | 2498 | `43fa563b99b302c7…` |
| [R.csv](R.csv) | R | 1519 | 216526 | `1e954e7c1a11a09f…` |
| [S.csv](S.csv) | S | 24051 | 3561540 | `f454c3cc65f64b7d…` |
| [T.csv](T.csv) | T | 7963 | 1132471 | `61a554db1493d77d…` |
| [U.csv](U.csv) | U | 277 | 41378 | `3ba87862f0e1c035…` |
| [V.csv](V.csv) | V | 984 | 142532 | `674a775f353c3455…` |
| [W.csv](W.csv) | W | 123 | 17987 | `dbaa07fcd8b2753a…` |
| [X.csv](X.csv) | X | 1 | 399 | `a52a7bee86175067…` |
| [Y.csv](Y.csv) | Y | 1 | 423 | `374714345c14abcf…` |
| [Z.csv](Z.csv) | Z | 3 | 713 | `7a9df5a82db8f97e…` |
