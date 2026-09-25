# S06 — Produtos (catálogo)

> **Fonte:** https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-6 · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-6 · https://www.rabisistemas.com.br/manual/modulos/estoque.html#produto-obrigatorios-api · spec `openapi-2026-09-25.json` (`POST /produtos`, `/produtos/bulk`) · leitura real (GET) da API de produção em 25/09/2026 · **Conferido em:** 2026-09-25
> **Vale para:** produção (ordem corrigida em 24/09/2026: produtos antes dos serviços) · **Kit:** v0.1.0

## Objetivo

Todo medicamento e material usado nos serviços existe no catálogo, uma vez só,
com fabricante, apresentação, unidade e códigos certos. **Só o cadastro do
item**: entradas de estoque, saldo e custo ficam para a S12.

## Link do manual

- Etapa 6: https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-6
- Tela: https://www.rabisistemas.com.br/manual/modulos/estoque.html#cadastrar-produto
- Obrigatórios pela API: https://www.rabisistemas.com.br/manual/modulos/estoque.html#produto-obrigatorios-api
- Como o produto vira preço: https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#produto-cadeia

## Depende de

S02 (depósito), S03 (tipo de produto, unidade de medida, tipo de código),
S04 (fabricante; fornecedor e princípio ativo, se usados).

## Documentos a pedir

FA-3 (lista de medicamentos e materiais), FA-4 (notas fiscais), FA-6 (o que vai
em cada serviço), CV-3 (regras de materiais dos convênios — ajuda a nomear e
codificar), SA-3 (cadastro do sistema anterior).

## Índice de dados a coletar

| dado | campo API | obrigatório? | onde costuma estar no material do cliente | padrão sugerível | pergunta ao usuário se faltar |
|---|---|---|---|---|---|
| Nome (com dose e forma) | `nome` | sim | lista de produtos, nota fiscal, prescrição-padrão | — | "O <produto> que vocês usam é de qual dose? (ex.: 100 mg/5 ml)" |
| Código interno | `codigoProduto` | sim | sistema anterior | sequência "PRD-0001"… | "Posso numerar os produtos como PRD-0001, PRD-0002…?" |
| Apresentação | `apresentacao` | sim | nota fiscal, bula, referências | pelas referências (ex.: "Ampola 5 ml") | "Ele vem em ampola, frasco ou comprimido?" |
| Quantidade na embalagem | `contendo` (inteiro) | sim | nota fiscal, referências | **1** | "Cada embalagem tem quantas unidades?" |
| Depósito padrão | `depositoId` | sim | S02 | o depósito mínimo da unidade | — |
| Tipo de produto | `tipoProdutoId` | sim | classificação | pelo item (Medicamento, Material Hospitalar…) | "O <produto> é medicamento ou material?" |
| Fabricante | `fabricanteId` | sim | nota fiscal, referências | pelas referências | "Qual o laboratório do <produto>?" |
| Unidade de medida | `unidadeDeMedidaId` | sim | nota fiscal | pela apresentação | — |
| Prazo de reposição (dias) | `prazoDeReposicao` (inteiro) | sim | compras | **15** (confirmar) | "Em quantos dias costuma chegar uma compra deste produto? Posso usar 15 dias para todos?" |
| Princípio ativo | `principioAtivoId` | não (recomendado em medicamento) | bula, referências | pelas referências | — |
| Fornecedores | `fornecedores` (IDs) | não | notas fiscais | os das notas | — |
| Código EAN | `codigoEAN` (inteiro) | não | nota fiscal, caixa | pelas referências | — |
| NCM | `codigoNCM` (inteiro) | não | nota fiscal | — | — |
| Tipo de código / Tabela 87 | `tipoCodigoId`, `tabelaANS87ID` | não (recomendado p/ TISS) | tabelas dos convênios | Brasíndice/SIMPRO/TUSS conforme o caso | — |
| Estoque pode ficar negativo? | `estoquePodeNegativar` | não | regra interna | não | "Se acabar no sistema, pode continuar usando (estoque negativo)?" |
| Preço da última pesquisa | `precoUltimaPesquisa`, `dataUltimaPesquisa` | não | nota fiscal | — | — |

## Fila de perguntas

1. Confirmar a **lista de produtos** (extraída; mostrar quantos e as dúvidas).
2. Para os com dose/apresentação ambígua: uma pergunta por produto.
3. Tipo de produto dos ambíguos.
4. Padrões em bloco: prazo de reposição e "pode negativar".
5. Candidatos de referência (fabricante, EAN, princípio ativo) — confirmar em
   bloco os de pontuação alta, um a um os de pontuação baixa.

## Enriquecimento possível

- **Referências do kit** (`referencias/` — Brasíndice, SIMPRO, CMED, TUSS; ou as
  tabelas próprias da clínica em `config/referencias-da-clinica.md`, que
  prevalecem). Busca por nome + dose, EAN, registro ANVISA ou código TUSS
  (`ferramentas/referencias/buscar.py`, `enriquecer_produtos.py`), com
  **candidatos para confirmação** — nunca gravação automática.
- **A dose é discriminante:** "Hidrocortisona 100 mg" ≠ "500 mg"; "80 mg" ≠
  "40 mg". Toda sugestão confere a dose por expressão numérica; divergência de
  dose = não casou.
- Preço das referências é **indicativo**: não vira preço de convênio sem regra.

## Leitura do que já existe no Rabi e regra de não perder nada

- `GET /produtos?ativo=true&nome=<termo>` e `GET /produtos` — casar por EAN,
  código interno e nome normalizado **com dose**.
- Existe → reutilizar; diferenças viram proposta.
- O campo `valorUnitario` da leitura do produto **não é preço de venda**. Não use
  para conferir preço. O preço calculado **por convênio** aparece em
  `GET /convenios/{id}/farol/produtos` (`receita`, `receita_sem_zerar`, com
  `fonte_nome` e `fator_k`) — use-o na S10b/S11.

## Gravação

| Ordem | Rota | Permissão | Lote |
|---|---|---|---|
| 1 | `POST /produtos` (o primeiro, sozinho) | `produto:create` | — |
| 2 | `POST /produtos/bulk` (chave `produtos`) | `produto:create` | até 50, depois do 1º provado |
| Correção | `GET /produtos/{id}` → `corpo_put_produto()` (`ferramentas/rabi_api/corpo_escrita.py`) → `PUT /produtos/{id}` completo | `produto:update` | — |

- Exemplo mínimo (fictício): `{"nome":"Soro fisiológico 0,9% 500 ml","codigoProduto":"PRD-0001","apresentacao":"Frasco 500 ml","contendo":1,"depositoId":<id>,"tipoProdutoId":<id>,"fabricanteId":<id>,"unidadeDeMedidaId":<id>,"prazoDeReposicao":15}`
- A leitura real (medida em 25/09/2026) traz `TipoProduto`, `Fabricante`, `deposito`,
  `UnidadeDeMedida` como objetos aninhados e `permitirEstoqueNegativo`, e **não** traz
  princípio ativo, CD, tipo de código, tabela 87, última pesquisa, fornecedores nem
  anexos (guarde-os no dicionário de IDs / no corpo enviado na prova da criação); a escrita quer `tipoProdutoId`, `fabricanteId`, `depositoId`,
  `unidadeDeMedidaId`, `estoquePodeNegativar`. O conversor faz isso e **recusa** (com a
  lista) quando o GET não traz algum campo de escrita — complete com o cadastro do repo.
- 422 = referência inválida (depósito, tipo, fabricante ou unidade inexistente).
- Guardar `produtoId` no dicionário: composição de serviços (S08), tabela interna
  (S08), aba Produtos dos convênios (S10b), estoque (S12).

## Prova

- `provas/S06/produto-<codigo>/` (primeiro item) e `provas/S06/lote-NN/` (lotes,
  com `resultados` do 207 quando houver).
- Review: contagem esperado × gravado × conferido; lista dos que ficaram de fora
  e por quê.

## Armadilhas desta sprint

- Produto sem fabricante não salva — cadastre o fabricante na S04 antes.
- Nome sem dose gera casamento errado em convênio e em referência.
- Mesmo produto duas vezes (nome da nota × nome da prescrição): unifique antes.
- Tipo de produto errado quebra a **política de preço por tipo** do convênio
  (S10a): o produto fica sem preço.
- `PUT /produtos/{id}` sem o objeto completo apaga campos.

## Definition of Ready / Definition of Done

**DoR:** S04 conferida (fabricantes); tipos e unidades com ID; FA-3 ou FA-6 recebidos.

**DoD:**
- [ ] todo produto usado em serviço existe uma vez só, lido de volta;
- [ ] dose, apresentação, tipo e fabricante confirmados;
- [ ] `produtoId` no dicionário; provas salvas.

## Checklist de itens

| # | item | status | origem | prova | observação |
|---|---|---|---|---|---|
| S06-01 | Lista de produtos extraída (com origem) | pendente | | | |
| S06-02 | Duplicatas unificadas | pendente | | | |
| S06-03 | Candidatos de referência conferidos (dose!) | pendente | | | |
| S06-04 | Padrões aprovados (prazo de reposição, negativar) | pendente | | | |
| S06-05 | 1º produto gravado e provado | pendente | | provas/S06/ | |
| S06-06 | Lotes gravados e conferidos (uma linha por lote) | pendente | | | |
| S06-07 | Dicionário de IDs (produtoId) | pendente | | | |

## O que registrar

- `dados/catalogo/produtos.csv` (campos + ORIGEM + candidato de referência aceito).
- `decisoes/DECISOES.md`: padrões aprovados.
- `ESTADO.md`: próximo passo = S07.
