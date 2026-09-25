# 01 — Conceitos da conversão de valores

> **Fonte:** https://www.rabisistemas.com.br/manual/precos/index.html#ideia-em-uma-pagina · https://www.rabisistemas.com.br/manual/precos/arvore-de-decisao.html#visao-geral · experiência de implantação real (generalizada) · **Conferido em:** 2026-09-25
> **Vale para:** produção desde 23–24/09/2026 (regra única de preço) · **Kit:** v0.1.0

Este é o **coração financeiro** do Rabi. Tudo o que a clínica cobra — no
orçamento, na autorização, no agendamento, na guia e no XML TISS enviado à
operadora — nasce destas configurações. Bem configurado, o sistema calcula
sozinho e o Farol avisa quando a margem está ruim. Mal configurado, a clínica
cobra menos do que o contrato permite (receita perdida), cobra em dobro
(glosa) ou emite orçamento de R$ 0,00.

Leia este arquivo inteiro antes de qualquer outro da pasta.

---

## 1. Dois mundos: o catálogo e o convênio

```
MUNDO INTERNO (a clínica)                 MUNDO EXTERNO (cada convênio)
catálogo único: serviços, produtos,  ──►  a "tradução" de cada item para
taxas, equipamentos                        aquele contrato: nome, código,
(vale para todos os convênios)             tabela 87, valor, cobre/não cobre,
                                           pacote, tipo de atendimento
```

- O **catálogo** (nível 1) existe **uma vez** para a clínica inteira. Mexer
  nele afeta todos os convênios de uma vez.
- Cada **convênio** mostra o catálogo inteiro nas suas abas (Serviços,
  Produtos, Taxas, Equipamentos) para que cada item possa ser **convertido**
  ali. Ver o mesmo item em todos os convênios não é duplicação.
- Código próprio de operadora **não é item novo**: é a **conversão** (nível 3)
  de um item que já existe no catálogo. Casa-se o item da operadora com o do
  catálogo **pelo nome/natureza**, nunca pelo código.
- Vários itens do catálogo podem convergir para **um** código da operadora
  (N→1: por exemplo, 5 modelos de seringa pagos pelo mesmo código). Só se
  faz isso quando a operadora paga **um** código para a família inteira. Se
  ela paga códigos diferentes por variante, cada item fica com o seu.

## 2. Os tipos de item

| Tipo | Exemplo | Onde se cadastra (catálogo) | Onde se converte | Gera receita? |
|---|---|---|---|---|
| **Serviço** | consulta, aplicação de medicamento, sessão | Configurações › Serviços | Convênio › aba Serviços | sim |
| **Subserviço** | "Aplicação endovenosa" dentro de "Ferro aplicado EV" | Serviço pai › aba **Servicos** (sem cedilha) | Convênio › aba Serviços (é um serviço como outro) | sim |
| **Produto** | medicamento, seringa, soro, gaze | Estoque › Produtos (preço e custo na aba **Estoque**) | Convênio › aba Produtos + Política de Preço por Tipo de Produto | sim |
| **Taxa** | taxa de sala, taxa de aplicação | Configurações › Taxas | Convênio › aba Taxas | sim |
| **Equipamento** | aparelho usado no serviço | Configurações › Equipamentos | Convênio › aba Equipamentos | **não** (não tem valor, não entra na conta) |

- Um **serviço composto** contém produtos, taxas e subserviços, cada um com
  uma **quantidade** na composição.
- **Custo** só existe em **produto**. Taxa é receita pura. Serviço não tem
  custo próprio: o custo dele é a soma dos produtos da árvore.
- Um item que "parece taxa" pode estar cadastrado como **serviço** (ex.: taxa
  de curativo, taxa de enfermagem com tabela 87 = 18). Ao procurar um item,
  procure nas três abas.

## 3. Os três níveis de conversão

O sistema procura cada informação **do mais específico para o mais geral**.
Achou (campo preenchido), para. Campo **vazio**, desce um nível.

```
NÍVEL 3  item DENTRO do convênio        abas Produtos / Serviços / Taxas do convênio
   │     (linha azul 🔁 "Convertido")    → SEMPRE ganha quando preenchido
   ▼ vazio
NÍVEL 2  política geral do convênio     Dados do convênio › "Política de Preço
   │     (SÓ para o PREÇO de produto)    por Tipo de Produto"
   ▼ vazio
NÍVEL 1  cadastro do próprio item        serviço: Valor · produto: aba Estoque ·
         (linha cinza 🔒 "da casa")      taxa: coluna Valor
```

- O nível 2 **só existe para o preço de produto**. Não muda nome, código,
  tabela 87 de nada, nem o preço de serviço ou taxa.
- O que sai na guia/XML é o resultado dessa cadeia. A pergunta que julga
  tudo: *se esta guia fosse emitida hoje para este convênio, o que sairia
  (itens, código, descrição, tabela, valor)? Está de acordo com o contrato?*

## 4. Regra de ouro: vazio ≠ zero

| Você fez | O sistema entende |
|---|---|
| Deixou o campo **vazio** | "não tenho regra aqui — use o nível de baixo" |
| Digitou **0,00** | "o preço é zero mesmo" (gratuito neste convênio) — **não desce** |

- ✅ Em produção desde **23/09/2026** em **todas** as telas: Farol, linha ✅,
  agendamento, orçamento, pré-faturamento, contas a receber e XML. Antes, o
  Farol e várias telas tratavam 0,00 do serviço como vazio — por isso
  documentos antigos dizem "zero vira vazio". **Isso não vale mais.**
- Na API: `null` **limpa** (volta a vazio); `0` é zero; campo **omitido**
  mantém o valor atual (nas abas do convênio).
- Na tela: botão **Limpar valor** deixa o campo vazio.

### 4.1 Vazio × zero, atributo por atributo

| Campo | Vazio significa | Zero / marcado significa |
|---|---|---|
| Valor do serviço, valor unitário do produto, valor da taxa (linha 🔁) | sem regra → desce | 0,00 = gratuito neste convênio (não desce) |
| Fator K (produto) | desce: linha do convênio → política → cadastro | 0 = 0% de ajuste (multiplica por 1) e **não desce** |
| Nome, descrição, código, tabela 87, tipo de código, tipo de atendimento | em branco = vazio → usa o do cadastro | — |
| Utiliza | desmarcado (padrão de vínculo novo) = o convênio **não cobre** o item | marcado = cobre; preço pela cadeia do convênio |
| Pacote (só serviço, só no convênio) | desmarcado (padrão) = não é pacote | marcado = pacote; só é "de preço fechado" com preço fixo ou valor combinado (inclusive 0) |
| Zerar valor em pacotes | desmarcado = cobra à parte mesmo dentro de pacote | marcado = embutido **quando** dentro de pacote de preço fechado |

## 5. R$ 0,01 como marcador é PROIBIDO

- No passado, antes de 23/09/2026, usava-se R$ 0,01 para "marcar" uma linha
  sem valor (porque 0,00 era tratado como vazio). **Revogado.**
- 0,01 é **valor de verdade**: vai para a guia e para o Farol.
- Para "sem regra": **campo vazio** (`null` na API). Para "gratuito": **0,00**.
- Única exceção: 0,01 **intencional** como preço fechado simbólico de um
  pacote, decidido por escrito pela clínica. Registre a decisão.
- A IA **nunca** grava 0,01 e, ao encontrar um, pergunta: marcador antigo
  (limpar) ou preço simbólico intencional (manter e registrar)?

## 6. O que se converte, por item

Para cada serviço, subserviço, produto e taxa de cada convênio, o sistema
decide **separadamente**:

1. nome exibido e descrição (vão **literalmente** para a guia e o XML);
2. código e tipo de código (TUSS, próprio da operadora, SIMPRO, Brasíndice…);
3. tabela 87 (ver §7);
4. tipo de atendimento e parcelas máximas (só serviço);
5. valor unitário;
6. se o item **entra ou não na conta** (Utiliza · Pacote · Zerar);
7. o custo que vai para o Farol (só produto).

Regras práticas de texto (experiência):
- Nome e descrição convertidos são a **descrição contratual** do item naquele
  convênio. Nunca comentário, justificativa ou observação.
- Se forem iguais ao do cadastro, **deixe vazio** (herda).
- Preencha conversão (nível 3) **só no que difere** do que já sai pelo
  cadastro/política.

Detalhe completo da precedência: [02-tabela-mestra.md](02-tabela-mestra.md).

## 7. Tabela 87 da ANS (domínio TISS)

A **tabela 87** é o domínio TISS que diz **de que tabela de referência é o
código do item** ("tabela de tabelas"). Não confundir com a tabela 36, que é
indicador de acidente.

Valores citados no manual do Rabi (confira sempre a lista do sistema em
`GET /auxiliares/tabelas-ans87` — a API usa o **id** do registro, não o código):

| Código | Uso típico |
|---|---|
| 22 | procedimentos e eventos em saúde (TUSS) — serviços |
| 20 | medicamentos |
| 19 | materiais (e OPME) |
| 18 | diárias, taxas e gases medicinais |
| 05 | Brasíndice (acrescentado em set/2026) |
| 12 | SIMPRO (acrescentado em set/2026) |
| 97 | Taxa Própria (acrescentado em set/2026) |
| 00 | tabela própria (o XML agrupa "19/00" como materiais) |

No XML, os produtos saem agrupados pela tabela 87: **20/05 medicamentos ·
19/00 materiais · 18 gases**. Taxas saem na área de taxas. O serviço sai na
linha de procedimento.

> Não confirmado no kit: a lista completa de códigos aceitos pelo seu
> ambiente. Verifique com `GET /auxiliares/tabelas-ans87` antes de preencher.

## 8. Tipo de código

Tipos comuns: **TUSS** (terminologia da ANS), **CBHPM**, **código próprio /
tabela própria** (interno da operadora ou da clínica), **SIMPRO**,
**TISS/Brasíndice**. Atenção (experiência): em uma implantação real, o tipo
de código chamado "TISS" na tela guardava o **código interno Brasíndice** —
o nome engana. Leia os ids em `GET /auxiliares/tipos-codigo` e confirme o
significado com a clínica.

## 9. Glossário rápido

| Termo | Significado |
|---|---|
| Linha 🔒 / 🔁 / ✅ | cadastro (só leitura) / valor digitado no convênio / valor efetivo que vale |
| Linha Σ | total do serviço no convênio (só coluna Valor do serviço) |
| Valor combinado | valor do serviço digitado no convênio (linha 🔁). **Não é pacote** |
| Pacote | marcação do serviço **no convênio**: "este preço já inclui itens" |
| Pacote de preço fechado | Pacote marcado **e** (preço fixo **ou** valor combinado preenchido, inclusive 0) |
| Zerar valor em pacotes | marcação do item no convênio: "já está no preço do pacote" |
| Utiliza | "este convênio cobre este item" |
| Somar itens | caixinha "Definir preço do serviço pelos itens" do catálogo (API: `somarItems` na escrita, `somarItens` na leitura) |
| Base / valor próprio | valor do serviço sem os itens = linha ✅ = linha de procedimento do XML |
| Farol | receita ÷ custo × 100, com cores (verde/amarelo/vermelho/roxo) |
| Fator K | percentual de ajuste sobre a fonte de preço do produto (20 = +20%) |
| PF / PMC | Preço Fábrica / Preço Máximo ao Consumidor (Brasíndice) |

Próximo: [02-tabela-mestra.md](02-tabela-mestra.md).
