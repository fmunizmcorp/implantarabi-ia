---
name: enriquecer-produtos
description: Enriquece a lista de produtos (medicamentos, materiais) da clínica com códigos e dados de referência (TUSS, Brasíndice, SIMPRO, CMED, registro ANVISA) usando as tabelas do kit ou as tabelas próprias da clínica, mostrando candidatos para o usuário confirmar. Use na sprint S06 (catálogo de produtos) e quando um convênio pedir código de material/medicamento.
---

# Skill: enriquecer produtos

Playbook: `sprints/S06-produtos-catalogo.md`. Ferramentas:
`ferramentas/referencias/buscar.py` e `ferramentas/referencias/enriquecer_produtos.py`.

## Qual tabela usar
1. Se `config/referencias-da-clinica.md` (repo da clínica) aponta tabelas
   próprias, **elas prevalecem**.
2. Senão, use `referencias/` do kit (edição mais recente; preço é só **indicativo**).

## Passos
1. Lista de produtos da clínica em `dados/produtos/produtos.csv` (com coluna ORIGEM).
2. Rode `python3 ferramentas/referencias/enriquecer_produtos.py` → candidatos
   por produto (nome + dose, EAN, registro ANVISA, TUSS) com pontuação.
3. Mostre ao usuário **um produto por vez** (ou um bloco pequeno, se ele pedir),
   com os 3 melhores candidatos: "É este? (1, 2, 3 ou nenhum)".
4. Grave a escolha no CSV (coluna `referencia_escolhida` + fonte + edição).
   Candidato não confirmado **não entra**.
5. Só então o catálogo vai ao Rabi pela skill `ritual-de-carga`.

## Regras
- Nunca escolher sozinho quando a pontuação empata ou a dose difere.
- Preço de referência não é preço da clínica: preço vem do contrato/convênio
  ou da tabela interna (preço de produto).
