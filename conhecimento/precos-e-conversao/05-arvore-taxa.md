# 05 — Árvore da TAXA

> **Fonte:** https://www.rabisistemas.com.br/manual/precos/arvore-de-decisao.html#arvore-taxa · https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#taxa-niveis · https://www.rabisistemas.com.br/manual/modulos/configuracoes.html#taxas · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-5 · experiência real (generalizada) · **Conferido em:** 2026-09-25
> **Vale para:** produção desde 23–24/09/2026 · **Kit:** v0.1.0

A taxa é o item mais simples: **dois níveis, sem Fator K, sem política, sem
custo**. É receita pura. Mas é onde mais acontece cobrança em dobro e taxa
"sumida" dentro de pacote.

## 1. A árvore

```
TAXA T no convênio C
├─ há valor convertido na aba Taxas do convênio (linha 🔁)?  (0,00 conta)
│     sim → valor = esse valor
│     não → valor = Valor do cadastro da taxa
├─ sem Fator K, sem política (nível 2), sem custo
└─ entra na conta?  → árvore ENTRA/NÃO ENTRA (arquivo 06):
      Utiliza ✘ → fora
      dentro de pacote de preço fechado (pai ou ancestral) E Zerar ✔ → fora
      senão → entra (quantidade da composição × valor)
```

| Ordem | Campo | Tela | API |
|---|---|---|---|
| 1 | Valor (linha 🔁) | Convênio › aba Taxas (ou painel da taxa › "Valor Convênio") | `PUT /convenios/{id}/taxas` → `valorConvertido` (reais; `null` limpa) |
| 2 | Valor | Configurações › Taxas | `POST /taxas` → `valor` (reais) |

Textos e códigos: nome `nomeConvertido` → nome do cadastro; descrição
`descricaoConvertida` → cadastro; código `codigo` (no convênio) → código da
taxa; `tipoCodigoId` e `tabela87ANSId` → cadastro. Campos extras da aba:
`tipoTaxaId`, `codigoTabelaConversao`, `descricaoConversaoTabela`.

## 2. Cadastro (catálogo)

- Configurações › Tipos de Taxas (categorias) e › Taxas (valores).
- API: `POST /taxas` · `/taxas/bulk` (50) · obrigatórios `taxas` (o nome),
  `codigoTaxa`, `tipoTaxaId` (de `GET /auxiliares/tipos-taxa`), `valor`.
  Opcionais: `tipoCodigoId`, `tabelaANS87ID` (atenção: grafia diferente da
  aba do convênio, que usa `tabela87ANSId`). `POST /taxas` responde 200.
- Corrigir: `PUT /taxas/{id}` com a taxa **completa** (sobrescreve).
- Na implantação, **taxas vêm antes** de produtos, serviços, tabela interna e
  convênios (as abas do convênio e a composição dos serviços exigem as
  taxas).
- Toda taxa tem preço no catálogo, mesmo que num convênio ela vá a zero
  dentro de pacote: o mesmo item pode ser usado **fora** do pacote e aí
  precisa ter valor.

## 3. Situações típicas e configuração

| Situação no contrato | Configuração da taxa no convênio |
|---|---|
| paga pelo valor da casa | Utiliza ✔ · valor 🔁 vazio · Zerar ✘ |
| paga valor próprio / código próprio | Utiliza ✔ · `valorConvertido` = valor · `codigo`/`nomeConvertido` do contrato |
| incluída no preço de um pacote | Utiliza ✔ · Zerar ✔ (e o serviço com Pacote + preço) |
| cobrada à parte mesmo no pacote | Utiliza ✔ · Zerar ✘ |
| gratuita neste convênio | Utiliza ✔ · `valorConvertido` = 0 |
| o contrato não paga taxa nenhuma | Utiliza ✘ (taxa não tem custo; não afeta Farol) — **decisão escrita** |

## 4. Armadilhas da taxa

1. **Taxa em dobro.** A mesma taxa configurada no serviço raiz **e** dentro
   do subserviço (ex.: taxa de aplicação) sai duas vezes. Mantenha em **um**
   lugar só. O mesmo vale para "valor extra" do convênio: ou no valor
   convertido da raiz, ou no subserviço — nunca nos dois.
2. **Taxa dentro de subserviço zerado continua entrando.** Desde 24/09/2026
   o Zerar não desce em cascata: zerar o subserviço "Aplicação" zera **só**
   o valor dele. Se a taxa de sala de dentro também está inclusa no pacote,
   marque Zerar **na própria taxa**.
3. **Taxa que "parece serviço".** Algumas taxas (curativo, enfermagem) estão
   cadastradas como **serviço** com tabela 87 = 18. Procure nas três abas.
4. **Código de procedimento só para autorização.** Algumas operadoras exigem
   um código de procedimento apenas para autorizar (com valor 0) e pagam o
   atendimento por uma **taxa** (ex.: taxa de sala compacta). Configuração:
   serviço com Utiliza ✔ e valor convertido **0,00** (zero é zero), e a taxa
   com o valor do contrato. Honorário nesse código é glosa.
5. **Taxa uma vez por atendimento.** Taxa vinculada à aplicação é cobrada
   uma vez; confira a quantidade na composição.
6. **Documentos antigos** dizem que "a API não expõe a conversão de taxa por
   convênio" — isso era a API interna antiga. Hoje a API externa tem
   `GET/PUT /convenios/{id}/taxas`.

## 5. Farol da taxa

O Farol da aba Taxas olha **só a taxa**. Como taxa não tem custo, não fica
roxo por falta de custo; serviço ou taxa **sem nenhum produto** não vira
roxo (custo zero é esperado). Ver [08-farol.md](08-farol.md).
