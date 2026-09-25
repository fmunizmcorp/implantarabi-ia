# ferramentas/ingestao — documentos do cliente → texto para a IA

> **Fonte:** este kit · **Conferido em:** 2026-09-25
> **Vale para:** kit v0.1.0 · **Kit:** v0.1.0
> Método completo: [metodologia/ingestao-de-documentos.md](../../metodologia/ingestao-de-documentos.md).

Rodam **na raiz do repo da clínica** (o kit fica em `.kit/`). Python 3, só
biblioteca padrão; ferramentas externas são **opcionais** e usadas se existirem.

| Arquivo | O que faz |
|---|---|
| `inventario.py` | varre `documentos-do-cliente/`, calcula o sha256 (16 primeiros caracteres), tipo, nº de páginas de PDF (pypdf ou `pdfinfo`, se houver) e **acrescenta** linhas novas ao `inventario.md` sem duplicar (mesmo conteúdo com outro nome não entra de novo) |
| `extrair_texto.py` | extrai o texto para `documentos-do-cliente/texto-extraido/<hash>.txt`, fatiado ≤ 1 MB, com cabeçalho de origem, e atualiza o `00-INDICE.md` da pasta |
| `_docs.py` | utilidades comuns (hash, tipo, lista de documentos, páginas de PDF) |
| `tests/` | `python3 -m pytest ferramentas/ingestao -q` |

## Uso

```bash
# 1) guarde o original em documentos-do-cliente/recebidos/AAAA-MM-DD/
python3 .kit/ferramentas/ingestao/inventario.py            # linhas novas no inventário
python3 .kit/ferramentas/ingestao/extrair_texto.py          # texto de todos os ainda não extraídos
python3 .kit/ferramentas/ingestao/extrair_texto.py documentos-do-cliente/recebidos/2026-10-01/contrato.pdf --forcar
```

Depois, o agente `extrator-documentos` lê o texto e gera a ficha em
`documentos-do-cliente/fichas-de-extracao/`.

## Ferramentas opcionais

| Para | Precisa | Sem ela |
|---|---|---|
| PDF com texto | `pdftotext` (pacote poppler-utils) | aviso; o PDF fica sem texto |
| PDF digitalizado (OCR) | `pdftoppm` + `tesseract` com idioma `por` (300 dpi) | aviso "OCR indisponível" |
| Imagem (foto de tabela) | `tesseract -l por` | aviso |
| Excel `.xlsx` | `openpyxl` (`pip install openpyxl`) | aviso |
| Nº de páginas | `pypdf` ou `pdfinfo` | coluna "páginas" = `?` |
| Word `.docx` | nada (stdlib) | — |

Em sessão Claude web sem essas ferramentas, a sessão pode instalar
(`apt-get install -y poppler-utils tesseract-ocr tesseract-ocr-por`, `pip install openpyxl`)
se o ambiente permitir; senão, pede o documento em outro formato (PDF com texto, XLSX, CSV).

## LGPD
Documento com lista de pacientes **não** vai para o git. O `.gitignore` do repo
da clínica bloqueia padrões comuns (`*pacientes*.csv`, `extrato-*`); confira
antes do commit.
