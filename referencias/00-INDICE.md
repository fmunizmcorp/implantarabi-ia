# Referências — tabelas-base de nomenclatura e códigos

> **Fonte:** ANS (TUSS/TISS), ANVISA/CMED, Brasíndice, SIMPRO, CBHPM — detalhes em cada pasta · **Conferido em:** 2026-09-25
> **Vale para:** referência de cadastro (nome, apresentação, códigos); **preço só indicativo** · **Kit:** v0.1.0

## Para que serve

Estas tabelas ajudam a IA a **cadastrar e enriquecer produtos e serviços** no
Sistema Rabi com o nome certo, a apresentação certa e os códigos certos (EAN,
registro ANVISA, TUSS, código Brasíndice/SIMPRO, tabela 87).

- **Nomenclatura e códigos:** é para isso que elas estão aqui.
- **Preço:** só **indicativo**. As edições podem estar desatualizadas e a
  alíquota de ICMS muda por estado. Preço de convênio vem do **contrato**; preço
  de produto vem da **tabela da clínica** (tabela interna / política do convênio).
- Nada aqui é gravado no Rabi sozinho: as ferramentas geram **candidatos para
  confirmação humana**.

## Ordem de prioridade (sempre)

1. **Tabelas próprias da clínica** — apontadas no repo dela em
   `config/referencias-da-clinica.md`. Se a clínica tem edição licenciada
   própria (Brasíndice, SIMPRO, CBHPM) ou tabela de operadora, **ela prevalece**.
   Pergunte ao cliente onde ficam os arquivos atualizados dele e registre lá.
2. **Contrato e tabela do convênio** (o que o convênio paga e qual tabela exige).
3. **Estas referências do kit** — a base comum.

## O que há

| Pasta | O que tem | Edição | Linhas | Licença | Quando usar |
|---|---|---|---|---|---|
| [brasindice/](brasindice/00-INDICE.md) | Medicamentos e materiais: nome, apresentação, EAN, código TISS (tab. 05), TUSS, PF/PMC | med. 1100 (+1094), mat. 1094 | 24.713 | licenciada | nome/apresentação padrão, código 05, TUSS |
| [simpro/](simpro/00-INDICE.md) | Material, medicamento, saneante, reagente: descrição, fabricante, código (tab. 12), valor vigente | coleta 12/04/2026 | 233.197 | licenciada | material sem Brasíndice, código 12 |
| [cmed/](cmed/00-INDICE.md) | Medicamentos com preço regulado: substância, registro ANVISA, EAN, GGREM, PF/PMC/PMVG por ICMS | 08/05/2026 | 25.276 | pública | princípio ativo, registro, teto legal de preço |
| [tuss/](tuss/00-INDICE.md) | Registro ANVISA → TUSS (medicamentos), histórico da TUSS, OPME (nomes técnicos, fabricantes) | 01/2026 | 135.266 | pública | código TUSS, mudanças de código, OPME |
| [cbhpm/](cbhpm/00-INDICE.md) | Procedimentos: código TUSS/CBHPM, descrição, porte, UCO | 5ª ed. (2008) | 2.652 | licenciada | nome/código de serviço; porte se o contrato for CBHPM |
| [tiss/](tiss/00-INDICE.md) | XSD TISS 4.03.00, domínios (dm_*) e Tabela 87 | 4.03.00 | 2.093 | pública | validar códigos do XML, escolher tabela 87 |

Mapa máquina-legível (edição, data, linhas, fatias, sha256 de cada arquivo):
[manifest.json](manifest.json).

Outros documentos desta pasta:

- [LICENCAS.md](LICENCAS.md) — o que é público, o que é licenciado e por que está aqui.
- [COMO-ATUALIZAR.md](COMO-ATUALIZAR.md) — trocar por edição nova; como a clínica aponta as dela.

## Como ler (sem estourar o contexto)

- **Não abra CSV inteiro.** Use a ferramenta:
  `python3 ferramentas/referencias/buscar.py "dipirona 500 mg"` (nome + dose),
  `… buscar.py 7896006220503` (EAN), `… buscar.py 90605233` (TUSS).
- Lista inteira da clínica: `python3 ferramentas/referencias/enriquecer_produtos.py produtos.csv`
  → até 3 candidatos por item, classificados ÓTIMO / BOM / RESSALVA / SEM MATCH.
- Manual: abra o `00-INDICE.md` do conjunto, veja a fatia pela **letra inicial
  do nome** (ex.: `brasindice/medicamentos/D.csv`) e use `grep -i`.
- Formato de todos os CSV: UTF-8, separador `;`, decimal com ponto, vazio =
  sem informação. Colunas de produto iguais em Brasíndice, SIMPRO e CMED
  (descritas em cada `00-INDICE.md`).

## Tabela 87 (qual tabela acompanha o código na guia)

| Item | Código TUSS | Código da fonte |
|---|---|---|
| Medicamento | tabela **20** | Brasíndice **05** |
| Material | tabela **19** | SIMPRO **12** (ou Brasíndice 05) |
| Taxa | tabela **18** | Taxa Própria **97** / tabela própria **00** |
| Procedimento | tabela **22** | tabela própria **00** |

Qual usar em cada convênio é regra do **contrato**. Lista completa:
[tiss/tabela-87/](tiss/tabela-87/00-INDICE.md). Não confundir com a Tabela 36
(indicador de acidente).

## Aprendizados de casamento (implantação real)

- A **dose decide**: "500 mg" comprimido ≠ "500 mg/ml" solução ≠ "1 g". Dose
  diferente = não casou.
- O preço unitário (`pf_unit`) é o que importa quando a clínica usa por
  ampola/comprimido; a embalagem pode ter 30, 60, 240 unidades.
- Item **restrito hospitalar** tem PMC 0 — é normal, use o PF.
- Material que não está no Brasíndice (ex.: soluções como glicose hipertônica)
  costuma estar no SIMPRO.
- **Manipulados, vacinas e material de limpeza** em geral não têm código de
  Brasíndice/SIMPRO e costumam ficar sem cobrança (Utiliza desmarcado) ou com
  tabela própria — decisão da clínica.
- Apresentação usada muito menos que a embalagem (ex.: 1 ampola de uma caixa
  com 6): cadastre a apresentação unitária e deixe isso claro no nome.
