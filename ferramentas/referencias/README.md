# Ferramentas de referências

> **Fonte:** tabelas em [`referencias/`](../../referencias/00-INDICE.md) · **Conferido em:** 2026-09-25
> **Vale para:** kit v0.1.0 · **Kit:** v0.1.0

Três ferramentas em Python (só biblioteca padrão; `openpyxl` é opcional e só
serve para o normalizador ler `.xlsx`).

| Ferramenta | Faz | Quem usa |
|---|---|---|
| `normalizar.py` | Converte os arquivos brutos (Brasíndice TXT, SIMPRO, CMED, TUSS, CBHPM, XSD TISS) em CSV UTF-8 `;` fatiado ≤ 4 MB por letra, com `00-INDICE.md` e `manifest.json` | mantenedor do kit; clínica que queira normalizar a própria edição |
| `buscar.py` | Busca por nome + dose, EAN, registro ANVISA ou código TUSS, lendo só as fatias necessárias, com pontuação 0–100 | IA implantadora (S06, convênios) |
| `enriquecer_produtos.py` | Para cada produto da lista da clínica, até 3 candidatos com códigos sugeridos e classificação ÓTIMO / BOM / RESSALVA / SEM MATCH | IA implantadora (S06), sempre para **confirmação humana** |

## Exemplos

```bash
python3 ferramentas/referencias/buscar.py "dipirona 500 mg"
python3 ferramentas/referencias/buscar.py "seringa 10 ml" --fontes simpro/material,brasindice/materiais
python3 ferramentas/referencias/buscar.py 7896006220503            # EAN
python3 ferramentas/referencias/buscar.py 90605233                 # TUSS
python3 ferramentas/referencias/buscar.py "consulta consultorio" --fontes cbhpm
python3 ferramentas/referencias/enriquecer_produtos.py produtos.csv --saida produtos-candidatos.csv \
    --referencias-clinica config/referencias-da-clinica.md
```

Em Python:

```python
from ferramentas.referencias.buscar import buscar
for r in buscar("dipirona 500 mg", limite=5):
    print(r["pontos"], r["fonte"], r["edicao"], r["produto"], r["apresentacao"])
```

## Como a pontuação funciona

- **Código exato** (EAN, registro ANVISA, TUSS, código da fonte, GGREM) = 100.
- **Nome**: palavras da busca achadas no nome do produto (peso 1), no princípio
  ativo (0,9) ou na apresentação/laboratório (0,7); palavras de forma
  (comprimido, ampola, frasco…) são reconhecidas pelas abreviações das fontes
  (`cprs`, `amp`, `fr`…) e pesam metade.
- **Dose** (`500 mg`, `10 ml`, `5 mg/ml`, `1 g` = `1000 mg`): dose igual soma;
  **dose diferente derruba** (conflito); concentração (`mg/ml`) é diferente de
  dose (`mg`); associação (`500 mg + 65 mg`) pesa um pouco menos.
- Tabelas da clínica ganham +5 e vêm primeiro no empate.

Classificação do `enriquecer_produtos.py`:

| Classe | Quando |
|---|---|
| **ÓTIMO** | código exato; ou ≥ 90 pontos com dose confirmada e fabricante que não diverge; ou ≥ 90 com fabricante que bate |
| **BOM** | ≥ 75 pontos sem conflito de dose |
| **RESSALVA** | 50–75 pontos, ou dose diferente, ou fabricante diferente — revisar |
| **SEM MATCH** | nada com 50+ pontos — cotação, tabela própria ou outro nome |

A coluna `decisao` do CSV de saída fica **vazia**: quem decide é o humano.

## Formato normalizado

Colunas de produto (iguais em Brasíndice, SIMPRO e CMED) estão em
[`comum.py`](comum.py) (`COLUNAS_PRODUTO`) e descritas em cada
`referencias/<fonte>/<conjunto>/00-INDICE.md`.

## Testes

```bash
python3 -m pytest ferramentas/referencias -q
```

Fixtures são **fictícias** e geradas no próprio teste (ver [tests/](tests/00-INDICE.md)).
