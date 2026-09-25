# SIMPRO — medicamento

> **Fonte:** coleta de portal de operadora que publica a tabela SIMPRO · **Conferido em:** 2026-09-25
> **Vale para:** referência de nomenclatura e códigos (edição 2026-04-12); preço só indicativo · **Kit:** v0.1.0

Descrição, fabricante, código SIMPRO (tabela 12) e valor vigente com data.

| Campo | Valor |
|---|---|
| Fonte | SIMPRO (publicação licenciada), via coleta de portal de operadora que publica a tabela SIMPRO |
| Edição | 2026-04-12 |
| Data da edição | 2026-04-12 (coleta) |
| Linhas | 28770 |
| Fatias | 27 |
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
| TST_SIMPRO_MEDICAMENTO.csv | 3540455 | `83454ff5e7029cbc…` |

## Fatias

Abra só a fatia da letra inicial do nome (ou use `ferramentas/referencias/buscar.py`).

| Arquivo | Prefixo | Linhas | Bytes | sha256 |
|---|---|---|---|---|
| [0-9.csv](0-9.csv) | 0-9 | 2 | 542 | `d981871f16455273…` |
| [A.csv](A.csv) | A | 3000 | 398227 | `57a65cca346a47e6…` |
| [B.csv](B.csv) | B | 1378 | 183876 | `2a35da14c2fd936a…` |
| [C.csv](C.csv) | C | 4431 | 601990 | `a233d1d34854d6b7…` |
| [D.csv](D.csv) | D | 1983 | 262286 | `f7879af03f41e4c8…` |
| [E.csv](E.csv) | E | 1020 | 134319 | `1b7e5256531d0baa…` |
| [F.csv](F.csv) | F | 1344 | 178432 | `7d2e80ea88fa9ee8…` |
| [G.csv](G.csv) | G | 743 | 96694 | `22f46fa1679f24ba…` |
| [H.csv](H.csv) | H | 674 | 92004 | `e3b4d385902d4531…` |
| [I.csv](I.csv) | I | 621 | 82851 | `ca1019a31736bd4f…` |
| [J.csv](J.csv) | J | 96 | 12718 | `69bdd6c3c4d43b3a…` |
| [K.csv](K.csv) | K | 263 | 34618 | `2eb97cad3239538c…` |
| [L.csv](L.csv) | L | 1183 | 154441 | `b799d3801af08aa0…` |
| [M.csv](M.csv) | M | 1523 | 201465 | `fc40eff51d3e83af…` |
| [N.csv](N.csv) | N | 1446 | 192159 | `6b6967b3059f33b9…` |
| [O.csv](O.csv) | O | 775 | 101961 | `53e4b45f196f7ffc…` |
| [P.csv](P.csv) | P | 1916 | 253736 | `b0e6d1a61f7dd535…` |
| [Q.csv](Q.csv) | Q | 109 | 14589 | `2ff665bb4940b7b1…` |
| [R.csv](R.csv) | R | 973 | 127134 | `f3ccb198a1d4a1eb…` |
| [S.csv](S.csv) | S | 2222 | 311108 | `66de572e100cadcb…` |
| [T.csv](T.csv) | T | 1315 | 170953 | `0d6e85124edcdbec…` |
| [U.csv](U.csv) | U | 187 | 24465 | `8aa414828be786b1…` |
| [V.csv](V.csv) | V | 1072 | 143361 | `7da2ba6cf46dfc3c…` |
| [W.csv](W.csv) | W | 35 | 4874 | `8b7cb85d5df1e6dd…` |
| [X.csv](X.csv) | X | 89 | 11931 | `b9ff75b9795c2a5e…` |
| [Y.csv](Y.csv) | Y | 14 | 2062 | `27edbec0dd2efd1b…` |
| [Z.csv](Z.csv) | Z | 356 | 45103 | `f76001b57d5dd279…` |
