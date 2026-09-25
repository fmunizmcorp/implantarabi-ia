# Lições — comunicação com o usuário (dono, implantador, equipe)

> **Fonte:** registros de uma implantação real anterior e instruções do mantenedor às sessões de IA (generalizados) · **Conferido em:** 2026-09-25
> **Vale para:** toda conversa da IA implantadora · **Kit:** v0.1.0

Método de conversa do kit: `metodologia/` (conversa com o usuário). Origem:
[origem.md](origem.md).

## L41 — Usuário leigo: não devolva tarefa técnica

**O que aconteceu:** o dono é leigo de propósito e pediu para ser tratado
assim. Mensagens como "verifique o log", "procure o ID", "monte a planilha"
travam o trabalho e o irritam.
**Regra que ficou:** se a IA tem acesso, a IA faz. Ao usuário vai **uma tela**:
o que mudou, o que significa em **R$ ou em risco de glosa**, e a decisão
precisa que falta. O detalhe fica no repositório.
**Como detectar:** mensagem com comando, JSON ou pedido de investigação ao
usuário.

## L42 — "Ok" para uma pergunta com duas opções não é resposta

**O que aconteceu:** a sessão ofereceu dois caminhos (A: dar valor e marcar
pacote; B: desligar as linhas) e o dono respondeu "ok". Não dava para saber qual.
**Regra que ficou:** pergunta de decisão tem opções rotuladas e **uma pergunta
por vez**; resposta ambígua → "Para eu não errar: A ou B?".
**Como detectar:** resposta curta que não contém a letra/opção.

## L43 — Condição do dono vira checagem explícita antes de gravar

**O que aconteceu:** o dono autorizou "**se** os itens forem mesmo daquele
procedimento no contrato". A sessão viu o código e achou suficiente; os itens
eram outros. Gravou e teve de reverter.
**Regra que ficou:** toda condição do tipo "se…" vira um item de conferência
com evidência (nome, contrato, página) mostrado **antes** de gravar.
**Como detectar:** aprovação condicional no histórico sem registro da checagem.

## L44 — Não apresente como descoberta o que já está escrito

**O que aconteceu:** a sessão apresentou como achados novos quatro coisas que o
conhecimento do projeto já documentava. Perdeu confiança e tempo do dono.
**Regra que ficou:** antes de afirmar "descobri", procure no kit e no repo da
clínica (lições, decisões, diretrizes). Se já existe, cite o registro.
**Como detectar:** o achado aparece em `licoes-aprendidas/` ou `decisoes/`.

## L45 — Meça antes de contradizer; ordem da culpa

**O que aconteceu:** em vários momentos o dono disse "confira, acho que está
certo" — e estava. A sessão tinha afirmado o contrário sem medir. Em outro
projeto, culpou-se o sistema por um erro de operação.
**Regra que ficou:** seja crítica, mas **com número medido**. Diga "não tenho
certeza" e vá à fonte. Ao ver um erro, investigue nesta ordem: **meu erro →
erro do processo → erro do sistema**.
**Como detectar:** afirmação categórica sem medição anexada.

## L46 — Recomendação não pode contrariar regra já decidida

**O que aconteceu:** a sessão recomendou "desligar" itens que o convênio não
paga; a regra do projeto dizia o contrário para aquele caso (fica ligado, com
o tratamento definido). Retirou a recomendação.
**Regra que ficou:** antes de recomendar, confira `decisoes/` e
`diretrizes-da-equipe.md` do repo da clínica e as regras vigentes do kit.
**Como detectar:** recomendação sem citar a regra que a apoia.

## L47 — Arquivo citado = caminho completo e o que ele contém

**O que aconteceu:** usuário leigo se perde com "veja o arquivo X".
**Regra que ficou:** cite o caminho completo (ou o link) e diga em 1 linha o
que há lá e o que fazer (em geral: nada, é registro).
**Como detectar:** menção a arquivo sem caminho.

## L48 — Honestidade de status: produção × chegando × roadmap

**O que aconteceu:** materiais de treinamento chegaram a vender como
disponível algo que era roadmap, e a negar uma função que já estava no ar.
**Regra que ficou:** toda função citada ao usuário vem com o status real e a
data (ver [../sistema-rabi/producao-x-roadmap.md](../sistema-rabi/producao-x-roadmap.md)). "Concluído no
desenvolvimento" ≠ "no seu ambiente".
**Como detectar:** promessa sem data; função que a tela não mostra.
