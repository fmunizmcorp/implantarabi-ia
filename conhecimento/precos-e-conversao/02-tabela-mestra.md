# 02 — Tabela-mestra: atributo × tipo de item × precedência

> **Fonte:** https://www.rabisistemas.com.br/manual/precos/arvore-de-decisao.html#tabela-mestra · https://www.rabisistemas.com.br/manual/precos/guia-ia.html#alg-textos · https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#textos-codigos · spec `../api-externa/spec/openapi-2026-09-25.json` · **Conferido em:** 2026-09-25
> **Vale para:** produção desde 23–24/09/2026 (textos e valores finais convertidos desde 24/09) · **Kit:** v0.1.0

Leia cada célula **da esquerda para a direita**: o sistema usa o **primeiro
preenchido**. "Conv." = nível 3 (item no convênio, linha 🔁). "Pol." =
nível 2 (política do convênio — só preço de produto). "Cad." = catálogo
(nível 1, linha 🔒). Texto em branco = vazio (desce). Número 0 = zero (não
desce).

## 1. A tabela

| Atributo | Serviço / subserviço | Produto | Taxa |
|---|---|---|---|
| **Nome exibido** | nome de conversão (Conv.) → nome do Cad. | nome convertido (Conv.) → nome do Cad. | nome convertido (Conv.) → nome do Cad. |
| **Descrição** | descrição no convênio → descrição do Cad. | descrição convertida → descrição do Cad. | descrição convertida → descrição do Cad. |
| **Código** | código no convênio → código do convênio → código do Cad. → código TUSS do Cad. | código de conversão (Conv.) → código da tabela da fonte de preço → código do produto | código no convênio → código da taxa |
| **Tipo de código** | Conv. → Cad. | Conv. → Cad. | Conv. → Cad. |
| **Tabela 87** | Conv. → Cad. | Conv. → Cad. | Conv. → Cad. |
| **Tipo de atendimento** | Conv. (coluna Tipo de Atendimento, linha 🔁) → Cad. do serviço | não se aplica | não se aplica |
| **Parcelas máximas** | serviço no convênio → limite de parcelas do convênio | — | — |
| **Valor unitário** | **valor próprio**: valor convertido (inclusive 0) → senão 0 se "somar itens" marcado → senão Valor do Cad. Sem nível 2, sem Fator K | valor unitário convertido × (1 + FK **da mesma linha**/100) → senão fonte, tipo de preço e FK herdados **campo a campo**: linha do convênio → Pol. (se ativa) → aba Estoque. Sem fonte → 0 | valor convertido (inclusive 0) → Valor do Cad. Sem Fator K, sem política |
| **Entra na conta?** | raiz: sempre (a tela só oferece serviços que o convênio utiliza). Subserviço: sem Utiliza → fora **com tudo dentro**; zerado em pacote fechado → só a linha dele fora | sem Utiliza → fora · zerado em pacote de preço fechado → fora · senão entra | sem Utiliza → fora · zerado em pacote de preço fechado → fora · senão entra |
| **Custo (Farol)** | não tem custo próprio; custo do serviço = soma dos custos de **todos** os produtos da árvore | aba Estoque: "Padrão Calcular" marcado → última entrada (senão o informado); desmarcado → "Última Compra (Unidade)" (senão última entrada). Nenhum → sem custo (roxo) | não tem custo |

Pseudocódigo oficial dos textos (guia-ia 2.9):

```
serviço  nome      = nome_conversao(S,C) ?? nome(S)
         descrição = descricao_convenio(S,C) ?? descricao(S)
         código    = codigo(S,C) ?? codigo_convenio(S,C) ?? codigo(S) ?? codigo_tuss(S)
         tabela 87 = tabela87(S,C) ?? tabela87(S)          (idem tipo de código)
         parcelas  = parcelas(S,C) ?? limite_parcelas(C)
produto  nome/descr = convertido(P,C) ?? cadastro(P)
         código    = codigo_conversao(P,C) ?? código da tabela da fonte de preço ?? codigo(P)
         tabela 87 = tabela87(P,C) ?? tabela87(P)
taxa     nome/descr = convertido(T,C) ?? cadastro(T)
         código    = codigo(T,C) ?? codigo(T)
         tabela 87 = tabela87(T,C) ?? tabela87(T)
("??" = só vazio desce; texto '' conta como vazio; 0 é zero)
```

## 2. De atributo para campo da API externa (abas do convênio)

Nomes **confirmados** no spec de 25/09/2026 (schemas `ConvenioServicoItem`,
`ConvenioProdutoItem`, `ConvenioTaxaItem`; os mesmos nomes voltam na leitura
`GET /convenios/{id}/servicos|produtos|taxas`, que acrescenta `id` = id do
vínculo).

| Atributo | Serviço (`PUT /convenios/{id}/servicos`) | Produto (`…/produtos`) | Taxa (`…/taxas`) |
|---|---|---|---|
| chave | `servicoId` | `produtoId` | `taxaId` |
| Utiliza | `utiliza` | `utiliza` | `utiliza` |
| Zerar valor em pacotes | `zerarValor` | `zerarValor` | `zerarValor` |
| Pacote | `pacote` | — | — |
| Autorização prévia | `autorizacaoPrevia` | — | — |
| Retorno | `retornoServico` | — | — |
| Nome convertido | `nomeConversao` | `nomeConversao` | `nomeConvertido` |
| Descrição convertida | `descricaoConvenio` | `descricaoConversao` | `descricaoConvertida` |
| Valor (linha 🔁) | `valorInternoConvenio` (reais; `null` limpa) | `valorUnitarioConversao` (reais; `null` limpa) | `valorConvertido` (reais; `null` limpa) |
| Fator K da linha | — | `fatorK` (**texto**, "10,5" ou "10.5"; `null` limpa) | — |
| Fonte de preço da linha | — | `fontePrecoCompraOptionsId` | — |
| Tipo de preço da linha | — | `tipoPrecificacao` (`PRECO_1`/`PRECO_2`/`PRECO_3`) | — |
| Tipo de código | `tipoCodigoId` | `tipoCodigoId` | `tipoCodigoId` |
| Tabela 87 | `tabela87ANSId` (id do domínio) | `tabela87ANSId` | `tabela87ANSId` |
| Tipo de atendimento | `tipoAtendimentoId` (aceita `null`) | — | — |
| Parcelas | `parcelasMaximas` | `parcelasMaximas` | — |
| Códigos | `codigo`, `codigoTuss`, `codigoConvenio` | `codigo`, `codigoTuss`, `codigoTiss`, `codigoConversao` | `codigo`, `codigoTabelaConversao`, `descricaoConversaoTabela` |
| Outros | `ativo`, `kitDocumentoId` | — | `tipoTaxaId` |

Semântica comum das três rotas (descrição oficial do spec):
- **upsert** pela chave; campo **omitido mantém** o valor atual (vínculo
  novo: `utiliza` omitido = `false`);
- `null` **limpa** apenas nos campos de valor (`valorInternoConvenio`,
  `valorUnitarioConversao`, `fatorK`, `valorConvertido`);
- até 200 itens por chamada; **uma chamada por vez por convênio** (a segunda
  simultânea recebe 429); interrompida em 45 s (o resto volta
  `NAO_PROCESSADO`); `207` = falha parcial → ler `resultados[]` pelo `indice`.

> **Não confirmado:** qual dos campos de código de produto alimenta o
> "código de conversão" da tela (`codigoConversao` é o candidato; `codigo`
> costuma vir igual ao código do catálogo). E se enviar texto vazio `""`
> limpa um texto convertido. **Como verificar:** grave em homologação um
> item de teste, releia `GET /convenios/{id}/produtos` e confira na tela a
> linha ✅ do código/nome.

## 3. Onde cada nível aparece na tela

| Linha | Serviço | Produto | Taxa |
|---|---|---|---|
| 🔒 cinza | preço da casa; se soma itens: soma dos itens a preço de casa "(soma dos itens)" | preço/fonte do cadastro (níveis 1/2) | valor do cadastro |
| 🔁 azul | valor combinado (digita-se aqui) | valor unitário convertido | valor convertido |
| ✅ verde | **valor próprio** (linha de procedimento do XML) | valor efetivo do produto | valor efetivo da taxa |
| Σ (só coluna Valor do serviço) | **total do serviço no convênio** = receita do Farol | — | — |

Colunas **Tipo de Atendimento** (serviço) seguem com 3 linhas. Detalhe das 4
linhas: [07-quatro-linhas-do-valor.md](07-quatro-linhas-do-valor.md).

## 4. Consequências práticas

1. **Nível 3 preenchido vence tudo** — inclusive a política de produto. Um
   produto com valor unitário convertido **não** recebe o FK da política.
2. **O nível 2 só mexe em preço de produto.** Para mudar nome/código de
   produto por convênio, use o nível 3.
3. **Tratar um produto diferente num convênio**: não mude a categoria do
   produto no catálogo; use o `fatorK` ou o `valorUnitarioConversao` da
   linha dele **naquele** convênio.
4. **Serviço e taxa não têm Fator K nem política.** Reajuste percentual de
   serviço/taxa = recalcular e gravar o valor convertido item a item.
5. **Equipamento** não tem valor: não entra em receita.

Árvores passo a passo: [03-arvore-servico.md](03-arvore-servico.md) ·
[04-arvore-produto-politica-fatork.md](04-arvore-produto-politica-fatork.md) ·
[05-arvore-taxa.md](05-arvore-taxa.md) ·
[06-arvore-subservico-e-entra-sai.md](06-arvore-subservico-e-entra-sai.md).
