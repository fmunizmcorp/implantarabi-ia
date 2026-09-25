# 06 — Subserviço e "entra ou não entra na conta" (Utiliza · Pacote · Zerar · somarItens)

> **Fonte:** https://www.rabisistemas.com.br/manual/precos/arvore-de-decisao.html#arvore-subservico · https://www.rabisistemas.com.br/manual/precos/arvore-de-decisao.html#arvore-entra · https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#regras-subservico · https://www.rabisistemas.com.br/manual/precos/guia-ia.html#alg-orcamento · **Conferido em:** 2026-09-25
> **Vale para:** produção desde 23–24/09/2026 (Zerar sem cascata desde 24/09) · **Kit:** v0.1.0

## 1. Só dois motivos tiram um item da conta

1. **Falta de Utiliza** no item (o convênio não o cobre). Em subserviço, leva
   **tudo** que está dentro dele — é o **único corte que desce em cascata**.
2. **Zerar** marcado no item **e** existe um **pacote de preço fechado acima**
   (o serviço pai ou qualquer ancestral).

"Somar itens" **não** aparece nesta decisão: desde 23/09/2026 ele decide só a
base do serviço.

## 2. Árvore ENTRA / NÃO ENTRA

```
1. O convênio Utiliza o item?
     não → FORA  (Conta no total = Não · motivo NAO_UTILIZA_NO_CONVENIO)
           subserviço: tudo dentro dele também fora (motivo PAI_FORA_DO_TOTAL)
           orçamento: a linha sai a R$ 0,00 · o custo continua no Farol
2. Há pacote de preço fechado acima (o serviço pai ou um ancestral)?
     não → ENTRA ("Zerar" nem é lido — inclusive em serviço que só soma itens)
3. O PRÓPRIO item tem "Zerar valor em pacotes"?
     não → ENTRA (cobrado à parte do pacote, quantidade inteira)
4. É subserviço?
     não → FORA (motivo ZERADO_EM_PACOTE) · orçamento: a quantidade da composição
           sai a R$ 0 e só o EXCEDENTE (o que passar do previsto) é cobrado
     sim → só a linha do subserviço (a base dele) vale 0;
           cada item de dentro volta ao passo 1
```

## 3. Tabela-verdade do item (6 linhas)

| # | Utiliza | Pacote fechado acima? | Zerar do item | Tipo | Resultado | Motivo (tela) |
|---|---|---|---|---|---|---|
| E1 | ✘ | qualquer | qualquer | qualquer | **fora**; subserviço leva a subárvore; custo conta | `NAO_UTILIZA_NO_CONVENIO` (filhos: `PAI_FORA_DO_TOTAL`) |
| E2 | ✔ | não | ✘ | qualquer | **entra** | — |
| E3 | ✔ | não | ✔ | qualquer | **entra** (Zerar não é lido) | — |
| E4 | ✔ | sim | ✘ | qualquer | **entra**, cobrado à parte, quantidade inteira | — |
| E5 | ✔ | sim | ✔ | produto / taxa | **fora**; orçamento: qtd da composição a R$ 0, excedente cobrado | `ZERADO_EM_PACOTE` |
| E6 | ✔ | sim | ✔ | subserviço | **só a base dele** fora; itens de dentro reavaliados um a um (voltam a E1…E6) | `ZERADO_EM_PACOTE` (só a linha dele) |

A tabela-verdade do **serviço** (somar × Pacote × valor convertido) está em
[03-arvore-servico.md §4](03-arvore-servico.md).

## 4. Árvore do SUBSERVIÇO

```
SUBSERVIÇO U dentro do serviço S, no convênio C
├─ 1. O convênio Utiliza U?
│     não → U e TUDO dentro dele ficam fora (custo conta, receita não). ÚNICO corte em cascata.
├─ 2. Calcula U com a árvore do serviço (arquivo 03): base(U) + itens de U (recursivo)
│     · o "contexto de pacote de preço fechado" de S (ou de qualquer ancestral) DESCE:
│       produto/taxa de U com Zerar fica fora mesmo que U não esteja zerado
│     · se U também é pacote de preço fechado, os itens dele com Zerar ficam fora
├─ 3. U tem Zerar e está dentro de pacote de preço fechado?
│     sim → U perde SÓ a própria base (a linha dele vale 0);
│           produtos/taxas de dentro seguem cada um o PRÓPRIO Zerar (desde 24/09/2026)
│     não → U contribui base(U) + itens de U
└─ Subserviço de preço fixo SEM Pacote: contribui valor dele + itens de dentro (desde 23/09/2026)
```

Exemplo: pacote fechado de 500,00 contendo o subserviço "Aplicação" (80,00,
Zerar ✔), que contém taxa 40,00 (Zerar ✘) e material 10,00 (Zerar ✔):
**500 + 0 (Aplicação zerada) + 40 (taxa entra) + 0 (material zerado) = 540,00.**

## 5. Algoritmo recursivo oficial (guia-ia 2.4)

```
func pacote_fechado(S, C):
    return sc(S,C).pacote AND (NOT S.somar_itens OR valor_convertido(S,C) preenchido)
    # "preenchido" inclui 0; pacote existe só em sc (serviço × convênio)

func valor(S, C, zeraCtx = false):
    base  = base(S, C)                       # arquivo 03 §2 A
    zera  = zeraCtx OR pacote_fechado(S, C)  # o contexto desce para todos os níveis
    total = base
    para cada item i de S (produto, taxa, subserviço) com quantidade q:
        se NOT utiliza(i, C): continue       # NAO_UTILIZA (subserviço: subárvore toda fora)
        zerado = zera AND zerar(i, C)        # ZERADO_EM_PACOTE (só a linha de i)
        se i é subserviço:
            v = valor(i, C, zera)            # itens de i avaliados um a um
            se zerado: v = v - base(i, C)    # perde SÓ a base (não cascateia)
            total += q * v
        senão:
            se zerado: continue
            total += q * valor_unitario(i, C) # arquivos 04 / 05
    return total

custo(S) = Σ de TODOS os produtos da árvore (sem filtro de Utiliza/Pacote/Zerar)
```

Observações do algoritmo:
- Ciclos são cortados pelo caminho visitado.
- O Zerar do serviço **raiz** não zera a própria base.
- Zerar **nunca** altera o valor do item vendido sozinho (avulso).
- `zera` só fica verdadeiro com `pacote = true` no próprio serviço ou num
  ancestral. Com valor combinado e `pacote = false`: `valor = convertido +
  Σ itens com Utiliza`.

## 6. Regra transacional do ORÇAMENTO (guia-ia 2.5)

```
embute = composicao_qtd > 0 AND ( absorvido_por_pacote_acima OR (zera AND zerar(item)) )
se embute: cobra 0 pela qtd da composição e preço cheio só pelo EXCEDENTE
senão:     cobra preço cheio pela quantidade inteira
preço cheio = cadeia de conversão do convênio (nível 3 → política → cadastro),
              nunca o preço da casa avulso
item sem Utiliza (produto, taxa, ou subserviço + subárvore): entra a R$ 0,00 (tem custo, sem receita)
linha do serviço = base(S,C)  (0 se o subserviço está zerado dentro de pacote fechado;
                               os itens dele não zerados continuam cobrados)
```

- Orçamento existe só para convênio **"Pago no ato do atendimento"**.
- O serviço raiz do orçamento não é zerado por Utiliza (a tela só oferece
  serviços que o convênio utiliza).
- Desde 23/09/2026 serviço de preço fixo **sem** Pacote **não** embute mais:
  cobra os itens na quantidade inteira.

## 7. Utiliza: o que significa e o que NÃO significa

- **Utiliza = "este convênio cobre este item".** Com Utiliza, o preço vem
  pela cadeia do convênio (combinado → política → cadastro), nunca pelo
  "preço da casa" avulso.
- **Padrão de vínculo novo: desmarcado** (na API, `utiliza` omitido em
  vínculo novo = `false`). É a **causa nº 1 de "o valor veio menor"**.
- Serviço sem Utiliza no convênio **não pode ser oferecido/agendado** naquele
  convênio. Nunca desmarque um serviço que a clínica presta.
- **"Desligar" ≠ "não cobrar".** Para um item que está **incluso** num
  pacote, o certo é **Utiliza ✔ + Zerar ✔** (e, se o item nunca tem preço
  próprio nesse convênio, valor 🔁 0,00). Desmarcar Utiliza tira a receita
  do item em **todos** os serviços do convênio, inclusive quando vendido
  sozinho, e o custo dele continua pesando no Farol.
- Utiliza ✘ é para o que o convênio **realmente não cobre** (ex.: manipulado,
  faixa de atendimento que o contrato não prevê). Registre a decisão.

## 8. Zerar: regras de uso

- Por **item × convênio**: vale para o item em **todo** o convênio, não por
  vínculo. Consequência (limitação conhecida): **não dá** para o mesmo
  produto ser embutido no pacote A e cobrado à parte no pacote B do mesmo
  convênio.
- Registros novos nascem com Zerar **marcado** (padrão desde 18/09/2026); os
  antigos ficaram desmarcados. Pela API, em vínculo novo, **envie
  `zerarValor` explicitamente** (não confirmado o padrão da API).
- Não desce em cascata: zere **cada** item incluso, inclusive os de dentro de
  subserviços.
- Nunca zere o serviço que **é** o pacote (a aplicação vendida como pacote):
  se ele entrar como subserviço de outro serviço que é pacote fechado, sai a
  zero; e o Zerar do serviço raiz não faz nada. Ver
  [14-armadilhas-vividas.md](14-armadilhas-vividas.md) (orçamento R$ 0,00).
- Medicamento em **conta aberta**: Zerar ✘. Medicamento **incluso** num
  pacote de preço fechado (contrato diz que o preço já inclui o remédio):
  Zerar ✔. Ver conflito C2 em [15-conflitos-resolvidos.md](15-conflitos-resolvidos.md).

## 9. somarItens × Pacote × valor combinado — resumo de bolso

| Quero | Catálogo (somarItems) | Convênio: valor 🔁 | Pacote | Zerar nos itens |
|---|---|---|---|---|
| preço fixo, itens cobrados à parte | ✘ (Valor = preço) | vazio ou combinado | ✘ | irrelevante |
| preço fixo que **já inclui** itens | ✘ | vazio ou combinado | **✔** | ✔ nos inclusos, ✘ nos à parte |
| soma do que foi usado (conta aberta) | ✔ | vazio | ✘ | ✘ |
| soma + extra fixo do convênio | ✔ | extra (em **um** lugar só) | ✘ | ✘ |
| preço fechado negociado (pacote) | ✔ ou ✘ | **preço do pacote** (inclusive 0) | **✔** | ✔ nos inclusos |
