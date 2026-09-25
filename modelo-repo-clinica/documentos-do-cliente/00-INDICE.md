# documentos-do-cliente · <NOME_DA_CLINICA>

> **Originais intocados** de tudo o que o cliente entregou (contratos, tabelas,
> planilhas, listas, extratos do sistema anterior sem PII). Método:
> `.kit/metodologia/ingestao-de-documentos.md`.

| Caminho | O que tem |
|---|---|
| [inventario.md](inventario.md) | uma linha por documento recebido (hash, tipo, páginas, o que contém, para qual sprint) |
| [fichas-de-extracao/](fichas-de-extracao/00-INDICE.md) | uma ficha por documento lido, com página/linha de cada dado |
| `texto-extraido/` | texto de PDFs/planilhas (gerado por `.kit/ferramentas/ingestao/extrair_texto.py`), fatiado ≤ 1 MB |
| `recebidos/AAAA-MM-DD/` | os originais, organizados pela data de recebimento |

Fluxo: arquivo chega → `recebidos/AAAA-MM-DD/` → `python3 .kit/ferramentas/ingestao/inventario.py`
→ `python3 .kit/ferramentas/ingestao/extrair_texto.py` → agente `extrator-documentos` →
ficha → dados em `dados/` com ORIGEM → confirmar com o usuário.

⚠️ Documento com lista de pacientes: **não** entra no git. Registre no inventário
só "contém dados de pacientes" e guarde fora do repo.
