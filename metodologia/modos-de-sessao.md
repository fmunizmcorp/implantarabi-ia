# Modos de sessão — implantação, atualização, convênio e diagnóstico

> **Fonte:** plano de implantação em sprints + roteiros de sessão coordenadora, de convênio e de implantação (experiência prática, generalizada) · **Conferido em:** 2026-09-25
> **Vale para:** toda sessão de clínica · **Kit:** v0.1.0

Ao abrir, a sessão lê o `ESTADO.md` e pergunta ao usuário o **modo** (ou
confirma o que está registrado). Cada modo usa o mesmo
[ritual de carga](ritual-de-carga.md) e a mesma
[conversa](conversa-com-o-usuario.md); muda o escopo.

| Modo | Quando | Escreve no Rabi? | Sprints |
|---|---|---|---|
| **1. Implantação** | Clínica nova, ou ainda não terminou a implantação | Sim, com aprovação | S00 → S17 |
| **2. Atualização de configuração** | Clínica já em uso; muda algo pontual | Sim, com aprovação | a sprint da área afetada |
| **3. Convênio** | Convênio novo, reajuste, correção de preço | Sim, com aprovação | S10a/S10b/S11 de um convênio |
| **4. Diagnóstico** | "O orçamento está saindo errado", "confere se está tudo certo" | **Não** — só leitura | nenhuma escrita |

## Modo 1 — Implantação completa

- Segue as sprints na ordem de [../sprints/00-INDICE.md](../sprints/00-INDICE.md)
  (S00 → S17), com as compactações por porte.
- Se o `ESTADO.md` mostra uma sprint em andamento, **continua de onde parou**
  (lê o checklist; itens `conferido` não se refazem — só se confere, por amostra,
  que continuam assim no Rabi).
- Pode entrar em modo 3 dentro da S10 (cada convênio como uma subsessão).

## Modo 2 — Atualização de configuração

Exemplos: reajuste de preço da casa, novo serviço, novo produto, novo
profissional, nova sala, mudança de repasse, novo usuário.

1. **Diagnóstico:** o que o usuário quer, em uma frase; que área é; que sprint
   do kit cobre essa área (ex.: novo serviço → S08 e, se tiver preço por
   convênio, S10b).
2. **Foto da área:** GET de tudo que a mudança toca (o item e seus vizinhos).
   Ex.: novo serviço composto → o catálogo de serviços, os produtos e taxas da
   composição, e a aba Serviços de cada convênio que vai cobrá-lo.
3. **Análise de impacto** antes da prévia:
   - quais convênios são afetados (o catálogo vale para todos);
   - **Farol antes** dos serviços afetados (`/farol/servicos` e `/farol/itens`);
   - **as 6 contagens de regressão** (abaixo) dos convênios afetados;
   - o que muda em dinheiro, em uma frase ("o Convênio A passa a pagar R$ 12,00
     a mais por aplicação").
4. **Mesmo ritual:** prévia → aprovação → grava → foto depois + diff.
5. **Depois:** Farol depois e contagens depois; o que mudou além do esperado é
   regressão — pare e avise.
6. **Registro:** linha em `decisoes/DECISOES.md`, entrada no
   `historico/HISTORICO.md`, item no checklist da sprint (novo item com status).

## Modo 3 — Convênio (novo, reajuste ou correção)

**Um convênio por sessão, um convênio por vez.** Nunca dois em paralelo: é
assim que se troca preço de contrato.

### Passo −1 — Diagnóstico do estado do convênio

Antes de tudo, descubra em que pé o convênio está. **Nunca trate como novo sem
conferir** — refazer do zero o que estava certo apaga trabalho aprovado.

Leia, nesta ordem: o checklist de S10a/S10b desse convênio no repo; os relatórios
e decisões anteriores dele (`dados/convenios/<slug>/`); as pendências; e, no
Rabi, a data da última alteração das linhas quando disponível.

| Estado | Como reconhecer | O que fazer |
|---|---|---|
| **NOVO** | sem checklist conferido, sem relatório anterior, nada configurado além do cadastro inicial | roteiro completo (S10a → S10b → S11) |
| **EM ANDAMENTO** | há relatório ou itens gravados, mas nem tudo `conferido`; ou há pendência aberta | **continua de onde parou** (ver abaixo) |
| **FECHADO** | tudo `conferido`, sem pendência | **regressão primeiro**; só mexe se houver fato novo (aditivo, reajuste, decisão, regressão) |

**EM ANDAMENTO — o caso mais comum:**

1. Não refaça o que foi aprovado e provado: releia no Rabi e confirme que está
   igual à última prova. Bateu → "conferido, sem mudança".
2. O relatório diz o que se pretendia; **a leitura do sistema diz o que está**.
   Divergiu → é regressão: pare e avise.
3. Monte a lista do que falta separando: (a) aprovado e gravado; (b) aprovado e
   **não** gravado; (c) esperando decisão; (d) nunca avaliado.
4. Mostre essa lista ao usuário antes de retomar.

**A primeira coisa que a sessão entrega é uma tela dizendo o estado e por quê.**

### Passo 0 — As 6 contagens de regressão

Antes de mexer num convênio que já teve trabalho gravado, conte e compare com a
última contagem registrada (em `dados/convenios/<slug>/contagens.md`):

| # | Contagem | Como |
|---|---|---|
| 1 | Serviços com **Utiliza** marcado — só de serviços **ativos** no catálogo | `GET /convenios/{id}/servicos` cruzado com `GET /servicos?ativo=true` |
| 2 | Serviços com Utiliza **sem valor combinado** (vazio) | mesma leitura |
| 3 | Serviços com **Pacote** marcado | mesma leitura |
| 4 | Itens (serviços, produtos, taxas) com **Zerar** marcado | abas Serviços, Produtos e Taxas |
| 5 | Produtos e taxas com **Utiliza** marcado | `GET /convenios/{id}/produtos` e `/taxas` |
| 6 | Serviços com Farol **vermelho ou roxo** | `GET /convenios/{id}/farol/servicos?farol=VERMELHO,ROXO&servicoAtivo=true` (use os nomes de cor exatamente como a API os devolve — confira na primeira leitura) |

- Leia **todas** as páginas (`linhas lidas = total`).
- O Farol também lista serviços **desativados** no catálogo: cruze sempre com o
  campo `ativo` antes de contar. Contar vínculo de serviço inativo como "ligado"
  já gerou erro grande numa implantação real.
- Não bateu com a última contagem → **regressão**: identifique os itens, busque
  o valor original **na fonte** (documento/prova anterior, não na memória) e
  avise antes de qualquer outra coisa.
- Sinal de alteração em massa feita por fora: muitas linhas do mesmo serviço
  mudadas na mesma hora em vários convênios.

### Passo 1 — A régua contratual

Do contrato e dos aditivos (antes de olhar o sistema), monte
`dados/convenios/<slug>/regua-contratual.md`, **cada item com a cláusula**:
vigência, reajuste (data e índice), renovação, prazo de pagamento, prazo de
entrega de guias, prazo de recurso de glosa e de pagamento do recurso, prazo de
autorização, prazo de retorno, fator K / regra de materiais e medicamentos, e o
**modelo de cobrança**: pacote fechado, conta aberta ou misto — e **quais**
serviços são pacote e o que está dentro de cada pacote.

A pergunta que abre tudo: **este convênio paga pacote fechado, conta aberta ou
preço fixo? Quais serviços são pacote?** Sem essa resposta não se configura nada.

### Passo 2 — Estado atual, campo a campo

Foto antes do convênio inteiro: dados, as 6 abas e as 3 leituras do Farol
(`/farol/itens`, `/farol/servicos`, `/farol/produtos`). Detalhe em
[../sprints/S10b-convenio-abas-e-precos.md](../sprints/S10b-convenio-abas-e-precos.md).

### Passo 3 — Comparar item a item e classificar

| Classe | O que é | O que a IA faz |
|---|---|---|
| **A — incontroverso** | a mudança pronta, com a cláusula ou linha da tabela que a sustenta | propõe na prévia |
| **B — precisa de decisão** | a análise pronta e **uma** pergunta objetiva | pergunta ao dono da clínica |
| **C — não sei tratar** | o que falta e onde procurar | vira lacuna/pendência |

**Nada entra por dedução.** Valor sem documento é classe C.
Mesmo a classe A só é gravada **depois da aprovação** — a classe muda o que se
pergunta, não quando se grava.

### Passo 4 — Executar o aprovado, provar, registrar

Ritual de carga, aba por aba, na ordem da S10b. Depois: diff, segunda leitura
fria, Farol relido com cada vermelho e roxo explicado, contagens depois
registradas em `contagens.md`, e o estado do convênio atualizado.

## Modo 4 — Diagnóstico (só leitura)

- **Nenhuma** escrita no Rabi. Se durante o diagnóstico surgir uma correção, ela
  vira proposta; para gravar, a sessão muda para o modo 2 ou 3 **com o
  consentimento explícito** do usuário.
- Roteiro: sintoma em uma frase → leitura das áreas envolvidas → hipótese com a
  prova (qual campo, qual valor, qual regra) → proposta de correção classificada
  A/B/C → registro em `historico/diagnosticos/AAAA-MM-DD-<assunto>.md`.
- Sintomas clássicos de preço e a leitura que os explica estão em
  `conhecimento/precos-e-conversao/` do kit (diagnóstico). Exemplos:
  orçamento de medicamento saindo R$ 0,00; "digitei um valor e os itens
  continuaram somando" (falta marcar Pacote); item com receita 0 que deveria
  cobrar (zerado em pacote, ou 0 gravado onde devia estar em branco).

## Troca de modo no meio da sessão

Permitida, mas **dita em voz alta**: "Vou sair do diagnóstico e propor uma
correção (modo Atualização). Posso?" A troca vai para o `ESTADO.md`.
