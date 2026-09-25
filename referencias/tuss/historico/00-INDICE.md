# TUSS — histórico de alterações (inclusões, alterações, inativações)

> **Fonte:** https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss · **Conferido em:** 2026-09-25
> **Vale para:** referência de nomenclatura e códigos (edição 202601); preço só indicativo · **Kit:** v0.1.0

Registro das mudanças da TUSS na competência (não é a tabela TUSS completa). Útil para saber se um código foi incluído, alterado ou inativado.

| Campo | Valor |
|---|---|
| Fonte | ANS — Padrão TISS, Histórico da TUSS |
| Edição | 202601 |
| Data da edição | 202601 |
| Linhas | 31838 |
| Fatias | 27 |
| Normalizado em | 2026-09-25 |
| Licença | pública (ANS) — ver [LICENCAS.md](../../LICENCAS.md) |

## Observações

- O kit não traz a TUSS completa de procedimentos (terminologia 22); para procedimentos use `cbhpm/portes` (código TUSS + descrição) e o contrato do convênio.

## Colunas

| Coluna | Significado |
|---|---|
| `competencia` | Mês/ano da publicação. |
| `codigo_terminologia` | Número da terminologia (19 materiais/OPME, 20 medicamentos, 64 forma de envio à ANS, 38 mensagens). |
| `terminologia` | Nome da terminologia. |
| `codigo_termo` | Código TUSS do termo. |
| `termo` | Descrição do termo. |
| `inicio_vigencia` | AAAA-MM-DD. |
| `fim_vigencia` | AAAA-MM-DD (vazio = vigente). |
| `fim_implantacao` | Prazo para operadoras/prestadores implantarem. |
| `tipo_acao` | Incluído, Alterado, Inativado… |

## Origem (arquivos brutos)

| Arquivo | Bytes | sha256 |
|---|---|---|
| Padr╞o TISS - Histórico da TUSS - 202601.txt | 4342858 | `d721e95b55e0ab7f…` |

## Fatias

Abra só a fatia da letra inicial do nome (ou use `ferramentas/referencias/buscar.py`).

| Arquivo | Prefixo | Linhas | Bytes | sha256 |
|---|---|---|---|---|
| [0-9.csv](0-9.csv) | 0-9 | 1 | 261 | `1cdabf282cecf6d4…` |
| [A.csv](A.csv) | A | 147 | 17888 | `9ee7c1bc2f35c651…` |
| [B.csv](B.csv) | B | 34 | 3869 | `95b28b6994de3ef6…` |
| [C.csv](C.csv) | C | 19169 | 2417970 | `1483fe2618175a65…` |
| [D.csv](D.csv) | D | 60 | 7214 | `3064061664b8d73f…` |
| [E.csv](E.csv) | E | 90 | 11191 | `d5eae9b46eb8a089…` |
| [F.csv](F.csv) | F | 114 | 20027 | `2224a79609217459…` |
| [G.csv](G.csv) | G | 133 | 20305 | `a19b7b839d51387a…` |
| [H.csv](H.csv) | H | 150 | 16817 | `9060ffd196ee7512…` |
| [I.csv](I.csv) | I | 606 | 77619 | `0b1e779ee08ba20c…` |
| [J.csv](J.csv) | J | 6 | 729 | `5130b96fcefe607c…` |
| [K.csv](K.csv) | K | 75 | 8703 | `7fd1f8d89aed548d…` |
| [L.csv](L.csv) | L | 112 | 15207 | `9423fad815323762…` |
| [M.csv](M.csv) | M | 187 | 21874 | `f2887684395d5b4c…` |
| [N.csv](N.csv) | N | 369 | 83885 | `d4ef94bacb99720c…` |
| [O.csv](O.csv) | O | 12 | 1419 | `34f9921159576254…` |
| [P.csv](P.csv) | P | 1014 | 166999 | `c940272e83aeb1c8…` |
| [Q.csv](Q.csv) | Q | 10 | 2040 | `4f5251ffd407daf8…` |
| [R.csv](R.csv) | R | 28 | 3417 | `0ebaac8c5d4711ff…` |
| [S.csv](S.csv) | S | 9256 | 1469688 | `07888f604dfa0d7b…` |
| [T.csv](T.csv) | T | 42 | 4804 | `284e8c4164cd77e2…` |
| [U.csv](U.csv) | U | 3 | 436 | `ef6a50c4f997a30a…` |
| [V.csv](V.csv) | V | 172 | 20852 | `468328676ea4a983…` |
| [W.csv](W.csv) | W | 3 | 403 | `f680c9cf15c2446a…` |
| [X.csv](X.csv) | X | 1 | 213 | `3cb42c8d41c4c3cb…` |
| [Y.csv](Y.csv) | Y | 5 | 594 | `c3936b2cf3697deb…` |
| [Z.csv](Z.csv) | Z | 39 | 6190 | `a31c4db2b63b3ad3…` |
