# Modelo de pasta de convênio

Copie esta pasta para `dados/convenios/<slug>/` e renomeie
`precos-SLUG.csv` para `precos-<slug>.csv`.

| Arquivo | O que tem |
|---|---|
| [regua-contratual.md](regua-contratual.md) | prazos, reajuste, fator K, modelo de cobrança — cada um com cláusula/página |
| [precos-SLUG.csv](precos-SLUG.csv) | uma linha por item (serviço/produto/taxa) com ORIGEM; entrada do `simulador.py` e do `montar_convenio.py` |
| [decisoes.md](decisoes.md) | decisões específicas deste convênio |

Colunas do CSV: confira as aceitas em `.kit/ferramentas/conversao/montar_convenio.py`
(o cabeçalho abaixo é o do modelo; se a ferramenta pedir outra coluna, siga a ferramenta).
