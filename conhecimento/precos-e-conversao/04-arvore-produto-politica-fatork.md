# 04 — Árvore do PRODUTO: cadeia de preço, política, tabela interna e Fator K

> **Fonte:** https://www.rabisistemas.com.br/manual/precos/arvore-de-decisao.html#arvore-produto · https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#produto-cadeia · https://www.rabisistemas.com.br/manual/precos/guia-ia.html#alg-produto · https://www.rabisistemas.com.br/manual/modulos/configuracoes.html#tabela-precos · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-9b · spec 25/09 · experiência real (generalizada) · **Conferido em:** 2026-09-25
> **Vale para:** produção desde 23–24/09/2026 · **Kit:** v0.1.0

O produto tem a cadeia de preço mais longa do Rabi. É onde mora a maior parte
do dinheiro de medicamento e material — e onde erros de unidade (Fator K,
embalagem) multiplicam o preço por 100 ou dividem por 50 sem ninguém ver.

## 1. A árvore

```
PRODUTO P no convênio C
│
├─ Há "Valor Unitário" convertido na aba Produtos do convênio (linha 🔁)?  (0,00 conta)
│     sim → valor = Valor Unitário × (1 + FK DA MESMA LINHA / 100)
│           (FK vazio na linha = sem ajuste; NÃO herda FK da política nem do cadastro)
│     não ↓
│
├─ Monta a regra CAMPO A CAMPO (cada campo desce sozinho, só quando vazio):
│     fonte de preço = linha do convênio → política do convênio p/ o Tipo de Produto (se ativa) → aba Estoque
│     tipo de preço  = linha do convênio → política → aba Estoque   (Preço 1 / 2 / 3 da tabela)
│     Fator K        = linha do convênio → política → aba Estoque → 0
│
├─ Qual é a fonte?
│     nenhuma                    → valor = 0
│     PRECO FIXO CADASTRADO      → Preço de venda tabela (aba Estoque)        SEM Fator K
│     PRECO DA ULTIMA COMPRA     → última compra unitária × (1 + FK/100)
│     PRECO DA ULTIMA PESQUISA   → preço da última pesquisa × (1 + FK/100)
│     PRECO MEDIO DE COMPRA      → preço médio por unidade × (1 + FK/100)
│     tabela de preços interna   → (valor do produto na tabela, no Preço 1/2/3 escolhido
│                                   || Preço de venda tabela || 0) × (1 + FK/100)
│
└─ "Zerar valor em pacotes" NUNCA muda este valor avulso — ele só decide,
   dentro de um pacote de preço fechado, se o produto entra na conta (arquivo 06)
```

Pseudocódigo oficial (guia-ia 2.1):

```
se cp.ValorUnitario preenchido:
    return cp.ValorUnitario * (1 + (cp.FatorK ou 0)/100)     # FK só da própria linha
fonte  = cp.fonte  ?? pol.fonte  ?? cfg.fonte                # ?? = só vazio desce
tipo   = cp.tipo   ?? pol.tipo   ?? cfg.tipo
fatorK = cp.fatorK ?? pol.fatorK ?? cfg.fatorK ?? 0
se fonte vazia: return 0
...(tabela acima)
```

(`cp` = linha do produto no convênio; `pol` = política ativa do convênio para
o tipo do produto; `cfg` = aba Estoque do cadastro.)

## 2. As cinco fontes de preço

| Fonte | De onde vem o valor | Aplica FK? |
|---|---|---|
| PRECO FIXO CADASTRADO | "Preço de venda tabela" (aba Estoque) | **não** |
| PRECO DA ULTIMA COMPRA | última compra registrada no estoque | sim |
| PRECO MEDIO DE COMPRA | média das entradas | sim |
| PRECO DA ULTIMA PESQUISA | preço da última pesquisa (aba Dados do Produto) | sim |
| Tabela de preços interna (Preço 1/2/3) | valor do produto naquela tabela; sem valor (0/vazio) → Preço de venda tabela | sim |

As quatro primeiras são fontes "imutáveis" calculadas pelo sistema. Cada
tabela interna aparece na lista de fontes **uma vez por coluna configurada**
(ex.: "TABELA X - PF" e "TABELA X - PMC" são duas opções da mesma tabela).

## 3. Tabela de preços interna (preço de PRODUTO)

- É uma tabela de **produtos** com até **3 colunas de preço** de nome livre
  (Nome Preço 1/2/3). Em uma implantação real, as colunas foram nomeadas
  **PF** (Preço Fábrica) e **PMC** (Preço Máximo ao Consumidor) para receber
  a Brasíndice/SIMPRO; `PRECO_1` = 1ª coluna, `PRECO_2` = 2ª, `PRECO_3` = 3ª.
- ⚠️ **Não define preço de atendimento particular.** O particular vem do
  convênio "Particular" (Pago no ato = Sim), como qualquer convênio. (O
  `mapa-funcional` do manual ainda diz o contrário — está desatualizado.)
- Valores são **unitários** (menor unidade usada — §6).
- Pode conter valores de origem Brasíndice e SIMPRO na mesma tabela
  (materiais costumam vir da SIMPRO). Isso não é "tabela faltando".
- **Edições congeladas por contrato** (ex.: operadora que exige uma edição
  antiga da Brasíndice/SIMPRO): crie **outra** tabela interna com aqueles
  valores e aponte a política **daquele** convênio para ela. Não se resolve
  item a item e não se altera a tabela padrão.
- API: `POST /tabelas-preco` (`name`, `priceType1` obrigatórios;
  `priceType2/3` opcionais) · `POST /tabelas-preco/produtos/bulk` (até 200,
  chave `precos`, cada item `purchasePriceSourceId` + `productId` +
  `priceType1..3`; **upsert**) · conferir `GET /tabelas-preco/produtos?id=` e
  `GET /tabelas-preco/precificacao` (lista as **opções** selecionáveis:
  `id`, `idJson` = `{"fontePrecoId":N,"tipoPrecificacao":"PRECO_1"|…|null}`,
  `fontePrecoId`, `nome`, `tipoPrecificacao`; sem envelope).
- Ordem: depois de taxas, produtos e serviços; antes dos convênios.

## 4. Política de Preço por Tipo de Produto (nível 2)

- Tela: Convênio › Dados do convênio › "Política de Preço por Tipo de
  Produto": colunas **Tipo de Produto**, **Fonte do Preço de Venda**, **Fator
  K/inflator/deflator %**.
- Vale para **todos** os produtos daquele tipo no convênio, exceto os que têm
  valor unitário convertido na aba Produtos.
- Categorias observadas com política em uma implantação real (5):
  **Medicamento · Medicamento Restrito Hospitalar · Medicamento
  Imunobiológico · Material Hospitalar · Material Hospitalar
  Perfurocortante.** Outros tipos (ex.: vacinas, imunoestimulantes, material
  de limpeza) ficaram **sem** política e caíam no nível 1.
  > Não confirmado se a lista de 5 é fixa do sistema. Verifique na tela e em
  > `GET /auxiliares/tipos-produto`. Identifique a categoria sempre pelo
  > **id** (`tipoProdutoId`), **nunca pela ordem na tela** — uma leitura por
  > ordem já inverteu duas categorias inteiras.
- Nem todo convênio precisa de política: se os itens seguem pelo nível 3,
  ela pode não ser necessária. Mas **convênio sem política e sem nível 3
  cai no preço da casa** — no Particular, isso já deixou materiais a R$ 0,00
  (catálogo sem preço).
- API (dentro do cadastro do convênio): `politicasPorTipoProduto[]` com
  `tipoProdutoId` (int), `fatorK` (**texto**, vírgula ou ponto) e `idJson`
  (texto JSON com `fontePrecoId` e `tipoPrecificacao` — use o `idJson` que
  `GET /tabelas-preco/precificacao` devolve).
- ⚠️ `PUT /convenios/{id}` **substitui o cadastro**. Quando
  `politicasPorTipoProduto` é enviado, é a **lista completa**: as que não
  estiverem nela são **inativadas**. Omitido = não altera. Enviar lista vazia
  **apaga a política**. (Na tela também: salvar a política vazia já apagou as
  5 linhas de um convênio.)
- ⚠️ O Swagger de leitura `GET /convenios/{id}` **não traz** a política nem os
  prazos. Não é possível "ler, alterar e reenviar" com segurança só pela API
  externa. Monte o objeto completo a partir da régua contratual confirmada
  (arquivo 10) e confira depois na tela / relatório "Validação de
  Configuração Por Convênio".

## 5. Fator K

- É **percentual**: `0` = sem ajuste · `20` = +20% · `-10` = −10%. Aceita de
  **−100 a 2000**. Nunca é multiplicador.
- Tela e API: percentual (`"20"`, `"38,24"`). **Planilha Excel do convênio:
  decimal** (`0.20` = +20%) — errar a unidade erra o preço em 100×.
- ⚠️ Linha nova pode nascer com FK **1** por padrão (na planilha, 1 = +100%).
  Nunca aceite o padrão: grave explicitamente `0` ou o percentual do
  contrato.
- FK da **linha** só vale sobre o valor unitário convertido da própria linha,
  ou como 1º degrau da herança campo a campo. FK vazio na linha com valor
  unitário = sem ajuste.
- Exibição: digitado "38,24" a tela pode mostrar "38.24" depois de
  recarregar — é só exibição.
- O cadastro do convênio também tem um campo `fatorK` (numérico, exemplo do
  spec `1.1`). **Não confirmado** o efeito dele no cálculo — o algoritmo
  oficial usa o FK da linha/política/produto. Não o use como substituto da
  política; se o contrato tem FK, grave-o na política por tipo de produto.

## 6. Valor unitário = valor da embalagem ÷ quantidade

O preço gravado é o da **menor unidade** usada, não o da caixa.

| Tabela oficial | Apresentação | No Rabi |
|---|---|---|
| caixa com 5 ampolas a R$ 72,78 | 5 | R$ 14,56 por ampola |
| caixa de 50 unidades a R$ 51,00 | 50 | R$ 1,02 por unidade |
| 10 frascos a R$ 2.832,08 | 10 | R$ 283,21 por frasco |

Cobrar a caixa por unidade = glosa por valor apresentado a maior. Dividir
demais = subfaturamento. O campo `contendo` do produto (quantidade na
embalagem) ajuda a conferir.

## 7. PF, PMC e restrito hospitalar (mercado)

- **Medicamento sem PMC é restrito hospitalar** (não é vendido ao
  consumidor). Numa edição da Brasíndice verificada, 100% dos itens
  rotulados "Restrito Hosp." tinham PMC = 0.
- A classificação é por **apresentação**, não por molécula (a mesma
  substância pode ser restrita na forma IV e ter PMC na caneta SC).
- PMC ÷ PF ≈ 1,34 a 1,38 (faixas de ICMS). Para item **com** PMC, "PF +38%"
  ≈ PMC. Para item **sem** PMC, política "PMC" dá o **fallback** (§1:
  Preço de venda tabela × FK) — que **não é** preço de contrato. Por isso,
  restrito hospitalar costuma ter política **PF + x%**.
  > Conflito com a experiência: em 12/09/2026 observou-se item restrito
  > saindo **R$ 0,00** com política PMC. O manual de 25/09 descreve o
  > fallback para o Preço de venda tabela. Prevalece o manual; confira o
  > resultado real em `GET /convenios/{id}/farol/produtos` (receita).
- Imunobiológico que também é restrito: as duas categorias são defensáveis;
  a decisão é **econômica e por convênio**. Não mude a categoria no catálogo
  por causa de um convênio — use o nível 3 daquele convênio.

## 8. Custo do produto (para o Farol)

- Aba Estoque › Última Compra. **Padrão Calcular** marcado → última entrada
  de estoque (senão o valor informado); desmarcado → o valor digitado em
  **Última Compra (Unidade)** (senão a última entrada).
- Sem custo → Farol **roxo** (sempre bloqueia). Logo após a implantação,
  roxo em produto costuma ser falta de entrada de estoque (etapa de
  Financeiro/Estoque): confira de novo depois delas.
- O custo é **o mesmo em todo convênio**. O que muda é a receita.
- ⚠️ Leitura: em uma implantação real o campo `valorUnitario` de uma leitura
  interna de produto era **saldo de estoque** (negativo), não preço. O preço
  por convênio se lê em `GET /convenios/{id}/farol/produtos` (`receita`) ou
  na tela. A API externa **não expõe** o preço de venda calculado do
  catálogo.

## 9. Receita típica "medicamentos pela tabela + %"

Convênio Gama: medicamentos pela tabela de referência + 15%.
1. Convênio › Dados do convênio › Política › Adicionar: Tipo = Medicamento ·
   Fonte = a tabela/coluna desejada · FK = 15.
2. Todos os medicamentos do Gama seguem, exceto os com valor unitário
   convertido próprio na aba Produtos.

Exemplo numérico (T22): produto sem valor unitário no convênio; política:
tabela interna Preço 1 = 50, FK 10; cadastro fixo 60 → **55,00** (o nível 2
vale só para preço de produto e ganha do cadastro).

## 10. Checklist do produto por convênio

- [ ] política por tipo de produto conforme o contrato (fonte, coluna PF/PMC, FK) — cláusula anotada;
- [ ] exceções com valor unitário convertido só onde o contrato manda;
- [ ] FK só na linha que tem valor unitário, se o contrato mandar;
- [ ] nenhum FK = 1 herdado de linha nova;
- [ ] valores unitários por menor unidade;
- [ ] todo produto usado com custo (senão roxo);
- [ ] Utiliza marcado em tudo que o convênio cobre; Zerar só nos inclusos em pacote.
