# 03 — Árvore do valor do SERVIÇO

> **Fonte:** https://www.rabisistemas.com.br/manual/precos/arvore-de-decisao.html#arvore-servico · https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#regra-unica · https://www.rabisistemas.com.br/manual/precos/guia-ia.html#alg-servico-composto · **Conferido em:** 2026-09-25
> **Vale para:** produção desde 23–24/09/2026 · regra "valor combinado não é pacote" vigente (decisão de 25/09/2026) · **Kit:** v0.1.0

## 1. As quatro chaves

| Chave | Onde fica | Escopo | Pergunta que responde |
|---|---|---|---|
| **Somar itens** ("Definir preço do serviço pelos itens"; API `somarItems`) | catálogo do serviço | o serviço em **todos** os convênios | o serviço tem valor próprio ou o valor próprio é 0? **Decide só a base** — não decide se os itens entram |
| **Pacote** | convênio › aba Serviços | serviço × convênio | este serviço, neste convênio, é um preço que já inclui itens? **Única** chave que faz um preço embutir itens. Não existe no catálogo |
| **Zerar valor em pacotes** | convênio › abas Produtos, Serviços, Taxas | item × convênio (vale para o item em **todo** o convênio, não por vínculo) | este item já está dentro do preço do pacote? |
| **Utiliza** | convênio › abas Produtos, Serviços, Taxas | item × convênio | este convênio cobre este item? |

## 2. A árvore

```
SERVIÇO S no convênio C
│
├─ A) VALOR PRÓPRIO (base)  = linha ✅ da aba Serviços = linha de procedimento do XML
│   ├─ há valor convertido do serviço no convênio (linha 🔁)?  (0,00 conta como preenchido)
│   │     sim → base = esse valor   (muda SÓ a base — valor combinado NÃO é pacote)
│   │     não → "somar itens" marcado?
│   │              sim → base = 0   (tooltip: "0,00 (sem preço próprio: itens cobrados à parte)")
│   │              não → base = Valor do cadastro do serviço
│
├─ B) ITENS — entram SEMPRE (desde 23/09/2026), cada um com as próprias conversões
│   para cada produto, taxa e subserviço da composição (quantidade q):
│     → passa pela árvore ENTRA/NÃO ENTRA (arquivo 06)
│     → se entra: soma q × valor do item (arquivos 04, 05, 06)
│
├─ C) É PACOTE DE PREÇO FECHADO?  (decide só se o Zerar dos itens é LIDO)
│     Pacote marcado no convênio  E  (serviço de preço fixo  OU  valor convertido preenchido, inclusive 0)
│       sim → itens com "Zerar" ficam fora (já estão no preço)
│       não → Zerar é ignorado; todos os itens com Utiliza entram
│
└─ TOTAL DO SERVIÇO = base + Σ itens que entram
      = receita do Farol do serviço = linha Σ da coluna Valor = o que o convênio paga
```

## 3. A fórmula (guia do implantador 3.2)

```
valor(serviço, convênio) = BASE + Σ quantidade × contribuição(item)

BASE = valor convertido no convênio, se preenchido (inclusive 0)
       senão 0 se "somar itens" · senão Valor do cadastro

contribuição(item) = 0  se Utiliza(item) desmarcado
                         (item subserviço: ele e TODA a subárvore ficam fora)
                   = 0  se há PACOTE DE PREÇO FECHADO acima (o próprio serviço
                         ou um ancestral) E o item tem Zerar
                         (item subserviço zerado: some só a BASE dele; os itens
                          de dentro seguem cada um o próprio Zerar)
                   = valor do item no convênio (pelos 3 níveis), nos demais casos
                         (subserviço: calculado por esta mesma fórmula, de baixo p/ cima)

PACOTE DE PREÇO FECHADO = Pacote ✔ E (preço fixo OU valor convertido preenchido — inclusive 0)
CUSTO = soma integral de todos os produtos da árvore (sem filtro nenhum)
```

## 4. Tabela-verdade (6 linhas)

| # | Soma itens | Pacote | Valor convertido | Resultado |
|---|---|---|---|---|
| V1 | ✘ | ✘ | — (qualquer) | valor fixo (o convertido, se houver, substitui o do cadastro só como base) **+ todos os itens com Utiliza**. Zerar não é lido. Orçamento: produtos e taxas na quantidade inteira |
| V2 | ✘ | ✔ | — (qualquer) | **preço fechado**: valor fixo (convertido, se houver) + itens **não zerados**. Orçamento: zerados → só o excedente |
| V3 | ✔ | ✘ | vazio | soma de todos os itens com Utiliza (base 0) |
| V4 | ✔ | ✘ | preenchido | valor convertido + todos os itens com Utiliza (valor combinado não é pacote: Zerar não é lido) |
| V5 | ✔ | ✔ | vazio | igual a V3 — Pacote não muda nada, Zerar não é lido (não há preço para embutir) |
| V6 | ✔ | ✔ | preenchido (inclusive 0) | **preço fechado**: valor convertido + só os itens não zerados |

Em todas: item sem Utiliza fica fora (subserviço sem Utiliza leva a
subárvore); o custo soma tudo.

## 5. Valor combinado NÃO é pacote (regra vigente, 25/09/2026)

- Digitar um valor na linha 🔁 do serviço muda **só o preço do serviço**. Os
  itens continuam somando por cima. Ex.: combinado 100 → total = 100 +
  aplicação + medicamento.
- **Preço fechado que já inclui itens exige as três coisas:**
  1. valor combinado na linha 🔁 (ou preço fixo do cadastro);
  2. **Pacote** ✔ na linha do serviço (no convênio);
  3. **Zerar** ✔ em **cada** item incluso (abas Produtos, Taxas ou Serviços),
     inclusive os que estão dentro de subserviços.
- Item incluso sem Zerar continua cobrado à parte.
- Sem Pacote, o Zerar dos itens **nem é consultado**.
- Pacote é sempre marcação **por convênio**. No catálogo só existe preço fixo
  ou soma dos itens; ambos definem só o preço do serviço.
- Na API: `valorInternoConvenio` sozinho **não fecha pacote**. Envie
  `pacote: true` no serviço e `zerarValor: true` nos itens inclusos.

## 6. O que mudou e quando (para ler documentos antigos)

| Data | Antes | Depois (vigente) |
|---|---|---|
| 23/09/2026 | serviço de preço fixo sem Pacote: itens **não** entravam; orçamento cobrava só o excedente | itens **sempre** entram; orçamento cobra quantidade inteira |
| 23/09/2026 | 0,00 no serviço era tratado como vazio no Farol e em várias telas | 0,00 = zero em todas as telas |
| 23/09/2026 | linha ✅ do serviço mostrava a soma | linha ✅ = valor próprio (base) |
| 23/09/2026 | subserviço de preço fixo "já incluía" os itens de dentro | subserviço contribui valor + itens de dentro |
| 24/09/2026 | subserviço zerado levava tudo que estava dentro | Zerar por item, **sem cascata** |
| 24/09/2026 | — | coluna Valor com 4 linhas (Σ = total) |
| 25/09/2026 | ambiguidade: valor combinado "fechava" o preço? | **não fecha**: só Pacote + Zerar |

Motivo histórico extinto: `PAI_NAO_SOMA_ITENS` (pai de preço fixo sem
Pacote) deixou de existir em 23/09/2026.

## 7. Exemplos de conferência (guia do implantador 3.4)

| Cenário | Configuração | Esperado |
|---|---|---|
| Preço fixo sem Pacote | Valor 100 · Pacote ✘ · produto 50 (Zerar ✔ ou ✘ — não é lido) | 150,00 |
| Pacote fixo | Valor 100 · Pacote ✔ · produto 50 com Zerar ✔ | 100,00 |
| Pacote fixo + extra | idem, produto com Zerar ✘ | 150,00 |
| Pacote com valor convertido | convertido 90 · Pacote ✔ · produto 50 Zerar ✘ | 140,00 |
| Valor combinado sem Pacote | convertido 100 · Pacote ✘ · produto 50 (Zerar ✔ ignorado) · taxa 30 | 180,00 |
| Valor combinado com Pacote | convertido 100 · Pacote ✔ · produto 50 Zerar ✔ · taxa 30 Zerar ✔ | 100,00 |
| Preço fechado de medicamento | Soma ✔ · convertido 3.506,53 · Pacote ✔ · medicamento Zerar ✔ | 3.506,53 |
| Taxa de aplicação + medicamento | Soma ✔ · convertido 266,16 · Pacote ✘ | 266,16 + medicamento |
| Medicamento + aplicação IM | Soma ✔ · Pacote ✔ · sem convertido · produto 135,42 Zerar ✔ · subserviço 80,00 | 215,42 (nada zerado: não há preço fechado) |
| Subserviço de preço fixo sem Pacote | raiz soma itens · subserviço fixo 80 com produto 20 (Utiliza ✔) | 100,00 |

Todos os casos numerados T1–T26: [12-casos-de-teste.md](12-casos-de-teste.md).

## 8. Exemplo numérico completo (serviço composto sem Pacote)

Cadastro: "Aplicação de medicamento X" · Valor 100,00 · soma ✘ · composição:
Medicamento X (1), Seringa (1), Soro (1), Taxa de sala (1).
Convênio Beta: serviço Utiliza ✔, Pacote ✘, valor 🔁 90,00. Política do Beta
para Medicamento: tabela interna, Preço 1, FK 10.

| Item | Origem do valor | Valor | Entra? | Custo |
|---|---|---|---|---|
| Serviço (base) | nível 3 | 90,00 | sim | — |
| Medicamento X | política: Preço 1 = 50,00 × 1,10 | 55,00 | sim | 30,00 |
| Seringa | nível 3: 2,00 (FK da linha vazio) | 2,00 | sim | 0,50 |
| Soro | Utiliza ✘ | 0,00 | **não** | 3,00 |
| Taxa de sala | nível 3: 35,00 (cadastro 40,00) | 35,00 | sim | — |
| **Total** | | **182,00** | | **33,50** → Farol 543% 🟢 |

- Linha ✅ = 90,00; linha Σ = 182,00.
- XML: procedimento 90,00 · medicamento 55,00 · seringa 2,00 · taxa 35,00.
- Variante "os 90 já incluem seringa e taxa": marcar Pacote + Zerar na
  seringa e na taxa (medicamento Zerar ✘) → receita 90 + 55 = 145,00.

## 9. Proteção contra ciclos

O sistema corta ciclos (A contém B que contém A) pelo caminho visitado. Mesmo
assim, **composição circular é erro de cadastro**: em uma implantação real,
um serviço que continha outro que o continha inflou o valor até ser
corrigido. Ver [14-armadilhas-vividas.md](14-armadilhas-vividas.md).
