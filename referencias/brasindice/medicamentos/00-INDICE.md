# Brasíndice — medicamentos

> **Fonte:** Brasíndice — arquivo TXT da edição · **Conferido em:** 2026-09-25
> **Vale para:** referência de nomenclatura e códigos (edição 1100 (+1094 complementar)); preço só indicativo · **Kit:** v0.1.0

Nomenclatura, apresentação, EAN, código TISS (tabela 05) e TUSS, com PF/PMC indicativos.

| Campo | Valor |
|---|---|
| Fonte | Brasíndice (publicação licenciada) |
| Edição | 1100 (+1094 complementar) |
| Data da edição | não informada no arquivo |
| Linhas | 16946 |
| Fatias | 27 |
| Normalizado em | 2026-09-25 |
| Licença | licenciada — incluída só como referência de nomenclatura/códigos — ver [LICENCAS.md](../../LICENCAS.md) |

## Observações

- Base = edição 1100 (15474 itens). Da edição 1094 entraram 1472 itens que não estão na 1100 (arquivo 'Outros Fármacos', que a 1100 recebida não traz); 177 itens que saíram da 1100 ficaram fora (tratados como descontinuados). A edição de cada linha está na coluna `edicao`.
- A edição 1100 recebida tem layout reduzido (19 colunas, sem genérico/GGREM/registro): esses campos vieram da edição anterior (mesma chave) ou da CMED (mesmo EAN).
- Layout do TXT conferido cruzando EAN/GGREM/registro com a CMED: coluna 17 = código TISS Brasíndice (vai na guia com tabela 05), 18 = genérico, 19 = código TUSS, 20 = GGREM, 21 = registro ANVISA. Restrito hospitalar vem do nome '(Restrito Hosp.)' ou da CMED.
- pf_unit/pmc_unit já vêm unitários da publicação. PMC 0 em item restrito hospitalar é normal.
- A coluna `vigencia` traz a edição em que o preço do item mudou pela última vez.
- principio_ativo vem da CMED (junção por EAN; se não achar, por registro). Vazio = não achado.

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
| Brasindice_1100_Medicamentos.txt | 3094267 | `4d83d4835a711f69…` |
| Brasindice_1094_Medicamentos.txt | 3713301 | `e63424edb737e948…` |
| Brasindice_1094_MedicamentosFarmacos.txt | 3993751 | `52521c42b5a3c669…` |

## Fatias

Abra só a fatia da letra inicial do nome (ou use `ferramentas/referencias/buscar.py`).

| Arquivo | Prefixo | Linhas | Bytes | sha256 |
|---|---|---|---|---|
| [0-9.csv](0-9.csv) | 0-9 | 5 | 1107 | `43931a7ed28610ae…` |
| [A.csv](A.csv) | A | 1671 | 411010 | `bbdc17e06e353ab6…` |
| [B.csv](B.csv) | B | 861 | 212166 | `f280604f43ebc99c…` |
| [C.csv](C.csv) | C | 2204 | 570148 | `427bd7cc99d143a1…` |
| [D.csv](D.csv) | D | 1286 | 319269 | `c3f21903e785b5da…` |
| [E.csv](E.csv) | E | 772 | 189793 | `0c2c3300f8c0e3b7…` |
| [F.csv](F.csv) | F | 734 | 180197 | `d2495a2fccca1a5f…` |
| [G.csv](G.csv) | G | 396 | 97670 | `222091222bddd0b6…` |
| [H.csv](H.csv) | H | 467 | 119180 | `ab90e90b59d25b7f…` |
| [I.csv](I.csv) | I | 414 | 98291 | `485b4e8ebb95c45f…` |
| [J.csv](J.csv) | J | 60 | 14983 | `2f3dd662eae624d7…` |
| [K.csv](K.csv) | K | 191 | 47896 | `7379a932181b5c0b…` |
| [L.csv](L.csv) | L | 841 | 204676 | `6e94ff43048d9f17…` |
| [M.csv](M.csv) | M | 874 | 217465 | `1f47b148128bd92c…` |
| [N.csv](N.csv) | N | 720 | 175304 | `ed99a1ccd19369d9…` |
| [O.csv](O.csv) | O | 601 | 151226 | `2436633610cca2f6…` |
| [P.csv](P.csv) | P | 1068 | 261842 | `2958fc1aca38b080…` |
| [Q.csv](Q.csv) | Q | 68 | 16365 | `3b85f02dd02598bc…` |
| [R.csv](R.csv) | R | 704 | 170179 | `845fb49172f0d707…` |
| [S.csv](S.csv) | S | 969 | 244445 | `1b22947a524ab690…` |
| [T.csv](T.csv) | T | 795 | 198700 | `0ec108f5be14abc7…` |
| [U.csv](U.csv) | U | 119 | 28904 | `4203262e2de08895…` |
| [V.csv](V.csv) | V | 716 | 173179 | `dd25ca8265a6fb04…` |
| [W.csv](W.csv) | W | 32 | 9179 | `5125c8b3b162900c…` |
| [X.csv](X.csv) | X | 123 | 31273 | `ca3a01db9d2dec27…` |
| [Y.csv](Y.csv) | Y | 14 | 3872 | `9a9046252273744f…` |
| [Z.csv](Z.csv) | Z | 241 | 58316 | `3cac055d094f8058…` |
