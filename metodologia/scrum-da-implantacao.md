# Scrum da implantação — as cerimônias na medida certa

> **Fonte:** plano de implantação em sprints (seção 3, "As cerimônias do Scrum") + protocolo de microsprints e PDCA do kit ([BOOTSTRAP](../BOOTSTRAP.md)) · **Conferido em:** 2026-09-25
> **Vale para:** implantação completa (S00–S17) e, de forma reduzida, os outros modos · **Kit:** v0.1.0

## Por que Scrum aqui

A implantação é longa (de 1 dia a 6 semanas), depende de documentos que chegam
aos poucos e de decisões do cliente. O Scrum dá três coisas: **ritmo** (sabe-se o
que entra hoje), **transparência** (o painel mostra o estado real) e **freio**
(nada avança sem o "pronto" da sprint anterior).

## Papéis Scrum × papéis do kit

| Papel Scrum | Papel no kit (ver [politicas.md](politicas.md) §7) | O que faz aqui |
|---|---|---|
| **Product Owner** | Dono da clínica | Decide regra de negócio (preço, pacote, repasse, quem vê o quê); aceita a review |
| **Stakeholder que aprova** | Implantador | Entrega documentos, aprova prévias, confere resultados. Pode ser o próprio dono |
| **Time de desenvolvimento** | IA implantadora | Lê, extrai, monta, grava, prova, registra |
| **Scrum Master** | IA implantadora (papel de facilitação) | Mantém o ritual, a daily, o painel, cobra lacunas e bloqueios |
| **Guardião do método** | Mantenedor do kit | Mantém sprints e metodologia; recebe sugestões de melhoria (sem dado de clínica) |

A IA acumula "time" e "Scrum Master", mas **nunca** o papel de Product Owner:
decisão de negócio é sempre do dono da clínica.

## O backlog

- O **backlog do produto** é o conjunto dos checklists das sprints S00–S17 no
  repo da clínica (`sprints/Sxx.md`), com a tabela
  `| # | item | status | origem | prova | observação |`.
- Status possíveis: `pendente → coletado → confirmado → gravado → conferido`,
  mais `n/a` (não se aplica a esta clínica, com motivo) e `bloqueado` (com o que
  destrava).
- Itens novos descobertos no caminho entram no checklist da sprint certa.
  Nada fica "na cabeça" da IA.

## Planning (início de cada sprint)

A IA apresenta, **em uma tela**:

1. Objetivo da sprint em uma frase e o link do manual.
2. O que já existe no Rabi dessa área (da foto da S00 ou relida agora).
3. O que já foi extraído dos documentos (quantos itens `coletado`).
4. O que falta (lacunas que travam) e as perguntas que virão, na ordem.
5. Estimativa honesta ("~20 minutos se as respostas vierem hoje").
6. Pergunta final: "Posso começar por <primeiro item>?"

Definition of Ready da sprint conferida antes (cada playbook tem a sua).

## Daily (uma vez por dia de trabalho, 5 linhas)

Gravada em `historico/daily/AAAA-MM-DD.md` e mostrada ao usuário:

```
Daily 03/10 — S06 Produtos
1. Ontem: 18 produtos gravados e conferidos (S06 18/40).
2. Hoje: os 22 restantes, em lotes de 10 depois do seu ok.
3. Travado: 3 produtos sem fabricante na nota — preciso da sua resposta (pergunta 1 de 3).
4. Risco: a chave vence em 12 dias; já pedi a renovação? (não)
5. Próximo passo concreto: mostrar a prévia do lote 2 de produtos.
```

- Só as lacunas que **travam a sprint da vez** aparecem na daily.
- Bloqueio **nunca fica em silêncio**: se algo travou, está na linha 3 com o que
  destrava e quem precisa agir.

## Microsprints e PDCA

- **1 detalhe = 1 microsprint:** um cadastro (ou um lote já liberado) passa pelo
  [ritual de carga](ritual-de-carga.md) inteiro, é commitado e atualiza o ESTADO.
- **A cada 5–10 microsprints, um PDCA curto** com o usuário:
  - *Plan:* o que estava previsto;
  - *Do:* o que foi feito (contagens);
  - *Check:* o que as provas mostram (algum diff inesperado? algum NÃO CONFIRMADO?);
  - *Act:* o que muda no jeito de trabalhar a partir de agora.
- O PDCA vai para `historico/HISTORICO.md` em 3–5 linhas.

## Review (fim de cada sprint)

A IA demonstra o resultado com a **foto depois**:

- tabela final do que existe agora no Rabi naquela área (nome, número, ativo);
- contagem: esperado × gravado × conferido;
- o que ficou `n/a` ou `bloqueado`, e por quê;
- onde o usuário pode ver na tela (caminho do menu).

Pergunta de aceite: "Está de acordo com a clínica? Posso fechar a S0x?"
O aceite vai para `historico/reviews/Sxx-AAAA-MM-DD.md`.

## Retro curta (fim de cada sprint, 3 linhas)

```
Retro S06: funcionou — nota fiscal deu fabricante e EAN de quase tudo;
não funcionou — 3 produtos com dose parecida quase casaram errado;
muda — conferir a dose em toda sugestão de referência.
```

Lição que serve a qualquer clínica → `historico/APRENDIZADOS.md` e, se for do
método, sugestão ao mantenedor do kit (sem dado da clínica).

## Definition of Done geral (vale para toda sprint)

- Todos os itens aplicáveis em `conferido` (ou `n/a` com motivo).
- Provas salvas (`provas/Sxx/...`) sem dado de paciente.
- Nenhum item NÃO CONFIRMADO sem pendência aberta com dono.
- `ESTADO.md` atualizado com o próximo passo concreto e a versão do kit usada.
- Review aceita e registrada. Commit + push feitos.

## Quando pular ou compactar

- **Consultório individual:** várias sprints viram minutos e algumas viram `n/a`
  (ver o quadro em [../sprints/00-INDICE.md](../sprints/00-INDICE.md)). As
  cerimônias encolhem: planning e review de 2 linhas; daily só se passar de um dia.
- **Rede:** a sprint é executada primeiro na unidade-piloto; a review inclui o
  padrão que será replicado.
- **Atualização de configuração / convênio:** ver
  [modos-de-sessao.md](modos-de-sessao.md) — as cerimônias são as mesmas, com
  escopo menor.
