# Lições — processo de trabalho e sessões de IA

> **Fonte:** registros de uma implantação real anterior + lições de sessões de IA do mesmo mantenedor (estado em arquivo, contexto, arquivos grandes, repositório no dia zero, fonte primária) — generalizados · **Conferido em:** 2026-09-25
> **Vale para:** toda sessão da IA implantadora · **Kit:** v0.1.0

Origem: [origem.md](origem.md).

## L49 — Estado vive em arquivo, não na conversa

**O que aconteceu:** conversas longas foram compactadas ou encerradas e
decisões ficaram "só na memória". A sessão seguinte repetiu perguntas e refez
medições.
**Regra que ficou:** toda decisão, pendência (com dono e caminho) e próximo
passo vai para arquivo no repo da clínica (`ESTADO.md`, `pendencias/`,
`decisoes/`). A sessão **relê**, não "lembra". Item só sai da lista de
pendências quando feito **e provado**.
**Como detectar:** "como combinamos antes" sem arquivo que registre.

## L50 — Escrito no disco não é salvo: commit + push no mesmo dia

**O que aconteceu:** vários documentos importantes ficaram dias só na pasta
local, sem commit. Em outro projeto, 12 dias de código viveram só no container
da sessão, que foi reciclado — sobrou só uma cópia colada no chat.
**Regra que ficou:** a cada passo concluído, **commit + push** (mensagem em
PT-BR) e dizer ao usuário que fez. Se o push falhar, avisar e tentar de novo;
nunca "deixar para depois". Repositório de destino inexistente não é motivo
para esperar: guarde num lugar durável no mesmo dia.
**Como detectar:** `git status` com mudanças não enviadas no fim da conversa.

## L51 — Antes do primeiro push: o repositório é privado?

**O que aconteceu:** o repositório guardava chave da API e senhas em texto
claro (por decisão do dono). Isso só é seguro em repositório **privado**.
**Regra que ficou:** na abertura, confira a visibilidade do repo da clínica e
avise por escrito se for público. Credencial nunca vai para o kit, issue,
prova ou relatório.
**Como detectar:** repo público com pasta `credenciais/`.

## L52 — Ritual de gravação completo, inclusive o que NÃO devia mudar

**O que aconteceu:** as gravações bem-sucedidas seguiram sempre: foto antes →
prévia → aprovação → gravação → foto depois → diff. A prova incluía "exatamente
3 campos mudaram em 526 produtos, e nada mais". Quando o diff foi ignorado,
campos sumiram (L02).
**Regra que ficou:** o diff confere o alterado **e** o resto (contagens,
cabeçalho do convênio). O que não foi relido é **NÃO CONFIRMADO**.
**Como detectar:** prova sem contagem de "não alterados".

## L53 — Um convênio por vez; o primeiro item prova o lote

**O que aconteceu:** alterações em vários convênios ao mesmo tempo misturaram
provas e dificultaram reverter.
**Regra que ficou:** um convênio por vez: termina, prova, só então o próximo.
Em lote, grava **um** item, relê, confere — e só então o resto, com aprovação.
**Como detectar:** provas de convênios diferentes no mesmo passo.

## L54 — Leia o conhecimento obrigatório inteiro no início

**O que aconteceu:** o projeto tinha dezenas de armadilhas já pagas
documentadas; a sessão não as leu e caiu em várias (L11, L44).
**Regra que ficou:** na abertura, leia o índice e os arquivos obrigatórios do
modo da sessão (`00-ESSENCIAL.md`, lições, diretrizes da equipe) **antes** de
medir ou propor.
**Como detectar:** erro repetido que já está numa lição.

## L55 — Script para contar; IA para julgar

**O que aconteceu:** listar arquivos e contar itens com sub-agentes gastava
muito; um script fazia em 1 segundo. Varreduras diárias (foto, contagens,
Farol vermelho, diff) não precisam de IA nenhuma.
**Regra que ficou:** tarefa mecânica (listar, contar, comparar, diff) → script
(`ferramentas/`). IA só para o que exige julgamento (contrato, preço,
classificação, explicação). Delegação a sub-agente: resultado em arquivo,
resumo curto na resposta.
**Como detectar:** a IA lendo item por item o que um `python` contaria.

## L56 — Arquivo grande: gere por código e valide; `.md` ≤ 40 KB

**O que aconteceu:** a ferramenta de escrita de arquivos pode truncar arquivos
grandes (30–50 KB+) sem erro; um mapa de rotas de 181 KB não cabia no
conhecimento carregado em toda conversa.
**Regra que ficou:** JSON/CSV grandes são gerados por script (`json.dump`) e
validados logo depois (`json.load`, contagem); documentos `.md` ≤ 40 KB,
quebrados por assunto com índice; tabela grande fatiada.
**Como detectar:** arquivo termina no meio; `json.load` falha; `.md` > 40 KB.

## L57 — Confirme o alvo antes de "consertar" ou regenerar

**O que aconteceu:** alegaram que 17 arquivos estavam truncados; a validação
mostrou que estavam íntegros — era uma cópia local desatualizada. Regenerar às
cegas teria destruído trabalho correto.
**Regra que ficou:** alegação de corrupção/erro se confirma no **estado real**
(remoto, sistema em produção) antes de agir.
**Como detectar:** "está tudo errado" sem medição anexada.

## L58 — Sessão curta e focada; compactar sem perder

**O que aconteceu:** sessões longas ficam caras (cada turno reprocessa tudo) e
esquecem regras do começo.
**Regra que ficou:** uma sessão por convênio ou por sprint, com relatório e
encerramento. Ao compactar, preserve: arquivos alterados, comandos de
verificação e o próximo passo (que já está no `ESTADO.md`).
**Como detectar:** conversa com centenas de turnos; regra do início violada.

## L59 — Processo em segundo plano pode morrer entre chamadas

**O que aconteceu:** em ambiente de sessão, um processo lançado em segundo
plano numa chamada não existia mais na seguinte.
**Regra que ficou:** tarefas longas rodam dentro do tempo da chamada (dividindo
o escopo) e gravam progresso em arquivo para retomar.
**Como detectar:** "vou checar o processo" e ele não existe.

## L60 — Verificador roda depois da última edição

**O que aconteceu:** em outro projeto, verificações foram rodadas e depois veio
"só mais um ajuste" — que quebrou o que tinha passado.
**Regra que ficou:** a evidência de "pronto" é a saída do verificador **depois**
da última alteração (tamanhos, links, testes, releitura na API).
**Como detectar:** hora do último teste anterior à última edição.

## L61 — Dado versionado por data precisa dizer qual é o vigente

**O que aconteceu:** coletas foram acumuladas em pastas por data sem indicar
qual valia hoje; ninguém sabia qual usar. Um arquivo de rastreabilidade de
preços ficou só numa pasta de downloads de um computador.
**Regra que ficou:** todo dado com data tem marcação de vigência (ou índice
dizendo o vigente) e fica **versionado no repo**, nunca só numa máquina.
**Como detectar:** várias versões do mesmo dado sem "vigente"; caminho de
arquivo fora do repositório.
