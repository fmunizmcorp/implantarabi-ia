# Brasíndice — materiais e insumos

> **Fonte:** Brasíndice — arquivo TXT da edição · **Conferido em:** 2026-09-25
> **Vale para:** referência de nomenclatura e códigos (edição 1094); preço só indicativo · **Kit:** v0.1.0

Nomenclatura, apresentação, EAN, código TISS (tabela 05) e TUSS, com PF/PMC indicativos.

| Campo | Valor |
|---|---|
| Fonte | Brasíndice (publicação licenciada) |
| Edição | 1094 |
| Data da edição | não informada no arquivo |
| Linhas | 7767 |
| Fatias | 27 |
| Normalizado em | 2026-09-25 |
| Licença | licenciada — incluída só como referência de nomenclatura/códigos — ver [LICENCAS.md](../../LICENCAS.md) |

## Observações

- Layout do TXT conferido cruzando EAN/GGREM/registro com a CMED: coluna 17 = código TISS Brasíndice (vai na guia com tabela 05), 18 = genérico, 19 = código TUSS, 20 = GGREM, 21 = registro ANVISA. Restrito hospitalar vem do nome '(Restrito Hosp.)' ou da CMED.
- pf_unit/pmc_unit já vêm unitários da publicação. PMC 0 em item restrito hospitalar é normal.
- A coluna `vigencia` traz a edição em que o preço do item mudou pela última vez.

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
| Brasindice_1094_Materiais.txt | 1772868 | `7c78793921850998…` |

## Fatias

Abra só a fatia da letra inicial do nome (ou use `ferramentas/referencias/buscar.py`).

| Arquivo | Prefixo | Linhas | Bytes | sha256 |
|---|---|---|---|---|
| [0-9.csv](0-9.csv) | 0-9 | 11 | 2263 | `9f0727f3c8aee25d…` |
| [A.csv](A.csv) | A | 578 | 116675 | `5c677c066ae49046…` |
| [B.csv](B.csv) | B | 390 | 72770 | `007ece0cb3f7fc5d…` |
| [C.csv](C.csv) | C | 505 | 98851 | `10e4195fd9a7d13f…` |
| [D.csv](D.csv) | D | 302 | 56184 | `53fd6b4c97e0c341…` |
| [E.csv](E.csv) | E | 341 | 67563 | `012427ed32b11c3d…` |
| [F.csv](F.csv) | F | 279 | 52122 | `de1dcbeb063190db…` |
| [G.csv](G.csv) | G | 70 | 12443 | `a274a1d804717f75…` |
| [H.csv](H.csv) | H | 338 | 66430 | `0f1e1761950c9504…` |
| [I.csv](I.csv) | I | 267 | 49014 | `4963a122b2641457…` |
| [J.csv](J.csv) | J | 17 | 3120 | `ccda9bcbcc218a59…` |
| [K.csv](K.csv) | K | 198 | 40872 | `0f6ab2ee014362b5…` |
| [L.csv](L.csv) | L | 530 | 107833 | `010dc8f9f0b664d2…` |
| [M.csv](M.csv) | M | 450 | 81149 | `f43a0d2aac22053a…` |
| [N.csv](N.csv) | N | 853 | 165924 | `339a7a0b6d27468a…` |
| [O.csv](O.csv) | O | 303 | 67107 | `1a99af37e0094f33…` |
| [P.csv](P.csv) | P | 774 | 165401 | `f75ff799ea451368…` |
| [Q.csv](Q.csv) | Q | 14 | 2429 | `028813c8d0b7fe61…` |
| [R.csv](R.csv) | R | 150 | 28833 | `38c8506414c5ecab…` |
| [S.csv](S.csv) | S | 718 | 142220 | `5785e6cb8d1931cd…` |
| [T.csv](T.csv) | T | 361 | 71087 | `e0ac2275d697c422…` |
| [U.csv](U.csv) | U | 43 | 8941 | `67eb04110e8411f1…` |
| [V.csv](V.csv) | V | 214 | 38595 | `faf800d0e7a48703…` |
| [W.csv](W.csv) | W | 1 | 465 | `ac97d055ab39780a…` |
| [X.csv](X.csv) | X | 6 | 1346 | `f2caa1ab067fcd0e…` |
| [Y.csv](Y.csv) | Y | 6 | 1290 | `2ce886cc4cbec9ee…` |
| [Z.csv](Z.csv) | Z | 48 | 8992 | `f9a48031cfc80f8c…` |
