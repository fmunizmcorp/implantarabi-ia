# 07 — As linhas 🔒 🔁 ✅ Σ da coluna Valor

> **Fonte:** https://www.rabisistemas.com.br/manual/precos/index.html#quatro-linhas-servico · https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#quatro-linhas · https://www.rabisistemas.com.br/manual/precos/guia-ia.html#alg-quatro-linhas · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#convenio-fase-2 · spec 25/09 · **Conferido em:** 2026-09-25
> **Vale para:** 3 linhas em produção desde 23/09/2026; 4ª linha (Σ) em produção desde 24/09/2026 · **Kit:** v0.1.0

## 1. Três linhas em todo item; quatro na coluna Valor do serviço

| Linha | Serviço (coluna Valor) | Produto, taxa, coluna Tipo de Atendimento |
|---|---|---|
| 🔒 cinza (só leitura) | preço da casa; em serviço que soma itens: **soma dos itens a preço de casa**, com a etiqueta "(soma dos itens)" | valor/tipo de origem (cadastro; no produto, níveis 1/2) |
| 🔁 azul ("Convertido") | **valor combinado** com este convênio — digita-se aqui; sozinho **não** fecha pacote | o que se digita para este convênio (nível 3) |
| ✅ verde | **valor próprio** do serviço = linha de procedimento do XML. Soma itens sem combinado → "0,00 (sem preço próprio: itens cobrados à parte)" — **não é erro** | valor/tipo **efetivo** — como sai na guia |
| **Σ** (só coluna Valor do serviço) | **total do serviço neste convênio** = serviço + produtos, taxas e subserviços que entram = **o que o convênio paga** = receita do Farol | — |

Passando o mouse, cada linha mostra uma dica. Hoje a explicação do 0,00
aparece só no tooltip da linha ✅; um texto visível na própria linha está
anunciado para o próximo ajuste.

## 2. Em termos do algoritmo (guia-ia 2.11)

```
coluna Valor do SERVIÇO S no convênio C (aba Serviços):
  🔒 = S.somar_itens ? Σ itens a preço de CASA ("(soma dos itens)") : Valor do cadastro de S
  🔁 = valor_convertido(S, C)                 (vazio = não digitado)
  ✅ = base(S, C)                              (linha de procedimento do XML)
       se S.somar_itens E valor_convertido vazio → 0   # não é erro
  Σ  = valor(S, C)                             (arquivo 06 §5)
     = receita total do Farol do serviço = o que o convênio paga
produtos, taxas e coluna Tipo de Atendimento: 3 linhas (🔒/🔁/✅)
o mesmo total aparece no Farol (bolinha), em Farol › Itens (linha do serviço)
e no botão "Expandir serviço"
```

## 3. Por que ✅ e Σ são diferentes (e os dois estão certos)

- **✅** responde: *quanto sai na linha do procedimento da guia?* Produtos e
  taxas saem nas **áreas deles** do XML, cada um com a própria conversão.
- **Σ** responde: *quanto o convênio paga no total por este serviço?*
- Caso motivador (manual): um "medicamento de ferro aplicado" no convênio
  Particular, com "somar itens" marcado: ✅ = R$ 0,00 (parecia erro); Σ = medicamento + aplicação.
- Caso real do manual (exemplo 4.3 da árvore de decisão): pacote com
  combinado 0,01 (preço simbólico intencional) → ✅ = 0,01 (antes da
  correção de 23/09 mostrava 16,03, a soma); Σ ≥ 90,02.

## 4. Como conferir cada linha

| Linha | O que conferir |
|---|---|
| 🔒 | referência; se "(soma dos itens)" parecer estranho, o catálogo está com preços da casa faltando |
| 🔁 | o valor do contrato está onde deveria? vazio onde não há regra? nada de 0,01 marcador? |
| ✅ | é o valor que deve sair no **procedimento** (não a soma)? |
| Σ | é o **total contratado**? (pacote fechado bate com o valor combinado + itens não zerados?) |

## 5. O que existe na API externa

| Informação | Onde na API externa | Status |
|---|---|---|
| 🔁 valor combinado do serviço | `GET /convenios/{id}/servicos` → `valorInternoConvenio` | ✅ spec |
| 🔁 produto / taxa | `…/produtos` → `valorUnitarioConversao` (+ `fatorK`) · `…/taxas` → `valorConvertido` | ✅ spec |
| "somar itens" do serviço | `GET /servicos/{id}` → `somarItens` (leitura); na escrita `somarItems` | ✅ spec |
| 🔒 valor do cadastro do serviço/taxa | `GET /servicos/{id}` → `valor` · `GET /taxas` → `valor` | ✅ spec |
| ✅ valor próprio do serviço | **não** vem pronto. Calcule: `valorInternoConvenio` se não-nulo (inclusive 0) → senão 0 se `somarItens` → senão `valor` do cadastro. Também em `GET /convenios/{id}/farol/servicos` → `receita_propria_servico` | ✅ spec (campo do farol) |
| Σ total do serviço no convênio | `GET /convenios/{id}/farol/servicos` → **`receita_total`** | ✅ spec |
| Σ por linha da árvore | `GET /convenios/{id}/farol/itens?servicoRaizId=` → `receita` da linha do serviço | ✅ spec |
| `efetivo.totalConvenio` | **não exposto** na API externa (existe só na API interna usada pela tela) | ❌ não use |
| valor efetivo (✅) do produto | não vem pronto; use `GET /convenios/{id}/farol/produtos` → `receita` | ✅ spec |

> **I13:** linha Σ = `valor(S, C)` = receita do Farol do serviço =
> `receita_total` de `/farol/servicos`. Se divergir do simulador, pare.

## 6. Tipo de Atendimento (3 linhas)

🔒 o do cadastro do serviço · 🔁 o escolhido para o convênio · ✅ o que vale.
O ✅ vai para o atendimento, o pré-faturamento e o campo `tipoAtendimento` do
XML. Ver [09-tipo-de-atendimento-e-xml.md](09-tipo-de-atendimento-e-xml.md).

## 7. Cor da linha

Desde 23/09/2026 a **1ª linha** das abas Serviços, Produtos, Taxas e
Equipamentos recebe a **cor do Farol** do item; sem Farol calculado fica
cinza claro.
