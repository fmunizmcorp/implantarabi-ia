# ferramentas/ — automações Python (só biblioteca padrão; openpyxl opcional)

| Pasta | Para quê | Principais |
|---|---|---|
| [rabi_api/](rabi_api/00-INDICE.md) | falar com a API externa com segurança | `cliente.py` (paginação, envelopes, lotes 207/429, erros de chave), `foto.py` (antes/depois/diff), `testar_chave.py` (25 áreas + validade), `atualizar_spec.py` |
| [conversao/](conversao/00-INDICE.md) | **montar e conferir preços por convênio** | `motor.py` (árvores do manual; T1–T26), `simulador.py` (prévia de valores e Farol), `montar_convenio.py` (CSV com origem → corpos dos PUT das abas), `conferir_farol.py` |
| [implantacao/](implantacao/00-INDICE.md) | dia a dia da sessão implantadora | `painel.py`, `fila_perguntas.py` (uma pergunta por vez), `carga.py` (ritual de 5 passos), `importar_planilha.py` (sistema anterior → CSV com origem) |
| [referencias/](referencias/00-INDICE.md) | nomenclatura e códigos de produtos | `buscar.py`, `enriquecer_produtos.py`, `normalizar.py` |
| [ingestao/](ingestao/README.md) | documentos do cliente | `inventario.py` (hash, tipo, páginas), `extrair_texto.py` (PDF/OCR/Excel/Word → texto fatiado) |
| [kit/](kit/00-INDICE.md) | manutenção do kit e criação de repo de clínica | `novo_repo_clinica.py`, verificadores de tamanho/links/vazamento, sincronizadores do modelo |

Rodar tudo: `python3 -m pytest ferramentas -q`
