# Lições — cadastro, preços e Farol

> **Fonte:** registros de uma implantação real anterior (sessões de jun a set/2026), generalizados · regras vigentes em https://www.rabisistemas.com.br/manual/precos/index.html#servico-composto · **Conferido em:** 2026-09-25
> **Vale para:** regras de preço em produção desde 23–25/09/2026 · **Kit:** v0.1.0

O estudo completo de preços está em
[../precos-e-conversao/00-INDICE.md](../precos-e-conversao/00-INDICE.md); aqui
ficam só as lições vividas. Origem: [origem.md](origem.md).

## L20 — R$ 0,01 como "marcador" é proibido

**O que aconteceu:** para marcar "sem valor" ou "incluso", usou-se R$ 0,01 em
vários convênios, porque o sistema tratava 0,00 como vazio. Em 23/09/2026 o
Rabi passou a tratar **0,00 como zero real** e **vazio como "sobe de nível"**
em todas as telas, Farol e XML. Os 0,01 viraram lixo que aparece na guia.
**Regra que ficou:** zero = 0,00; "não tenho regra aqui" = **vazio**. Nunca
0,01. Ao encontrar 0,01 na clínica, proponha limpar (com prévia).
**Como detectar:** valores 0,01 no convênio; linha ✅ mostrando 0,01.

## L21 — O comportamento mudou: reconfirme antes de aplicar regra antiga

**O que aconteceu:** num dia mediu-se "zero se comporta como vazio" (12 casos
de 12); quatro dias depois, o contrário, porque a correção subiu em partes.
**Regra que ficou:** regra de sistema tem data. Antes de agir sobre ela,
confira em `producao-x-roadmap` e meça num caso real (Farol › Itens).
**Como detectar:** conhecimento sem "vale desde"; resultado do Farol diferente
do previsto.

## L22 — "Somar itens" é o conceito, não o defeito

**O que aconteceu:** uma sessão concluiu que serviços de medicamento deveriam
ter "Definir preço do serviço pelos itens" **desligado**. O dono corrigiu: é
esse campo que faz o serviço valer aplicação + medicamento. A conta foi provada
em 10 serviços de 10.
**Regra que ficou:** serviço de medicamento aplicado = soma itens ligado
(aplicação + medicamento + o que entra). Antes de propor mudar um conceito,
leia o normativo e pergunte.
**Como detectar:** proposta de "desligar somar itens" em massa.

## L23 — Referência circular infla a receita

**O que aconteceu:** um serviço A foi colocado dentro de B, que já estava
dentro de A. O Farol passou a mostrar receita inexistente (até R$ 600 por
atendimento em dezenas de convênios). O vínculo tinha sido criado dias antes,
fora das sessões.
**Regra que ficou:** ao montar composição, verifique ciclos; em dúvida, o
serviço "maior" contém o menor, nunca os dois.
**Como detectar:** receita do Farol maior que a soma esperada; "Expandir
serviço" mostrando o próprio serviço dentro de si.

## L24 — Medicamento aplicado e não faturado

**O que aconteceu:** um medicamento caro não tinha **linha nenhuma** no
convênio Particular e estava com Utiliza desligado em três convênios de uma
mesma operadora: a clínica aplicava, tinha o custo e só faturava a aplicação.
Farol vermelho. Ligar o item (1 campo por convênio) trouxe a receita ao valor
certo e tirou do vermelho.
**Regra que ficou:** depois de configurar, **varra o Farol vermelho/roxo** e os
serviços com medicamento cujo Σ ≈ só a aplicação. Ligar item em convênio com
contrato é decisão do dono (a operadora paga à parte?).
**Como detectar:** Σ do serviço ≈ preço da aplicação; custo > receita.

## L25 — Particular sem política de preço = material a R$ 0,00

**O que aconteceu:** o convênio Particular não tinha **política de preço por
tipo de produto**; todos os materiais saíam a R$ 0,00 no orçamento. Em outro
convênio, faltavam subtipos de produto (ex.: um tipo "imuno…" diferente de
outro parecido) — produto sem política fica sem preço.
**Regra que ficou:** todo convênio que cobra produto precisa de política para
**todos os tipos e subtipos** de produto usados (ou preço no nível 3). Confira
contra a lista de tipos do catálogo.
**Como detectar:** orçamento particular com materiais a zero; produtos sem
preço num convênio.

## L26 — Pacote é preço fechado; "cobrar tudo" pode ser abusivo

**O que aconteceu:** uma sessão sugeriu "desmarcar o pacote no particular para
cobrar tudo". Errado: o pacote é um preço fechado que a clínica vende; o que
está dentro sai a R$ 0,00 **e isso está certo**. Os itens têm preço cadastrado
porque podem ser usados **fora** do pacote.
**Regra que ficou:** preço fechado = valor combinado + Pacote + Zerar nos
inclusos (regra vigente em 25/09/2026). Valor combinado sozinho não é pacote.
Não mexa em pacote sem entender o que a clínica vende.
**Como detectar:** proposta que aumenta muito o total de um serviço vendido
como pacote.

## L27 — Serviço desligado não agenda

**O que aconteceu:** numa família de convênios, **todos** os medicamentos
intramusculares estavam desligados (só a aplicação estava ligada): a atendente
não conseguia agendar. O cadastro certo existia, ativo, mas desligado; o antigo,
inativo, seguia ligado.
**Regra que ficou:** ao configurar um convênio, confira por **via** e por tipo
de serviço se o que a clínica faz está ligado. Garanta o cadastro **ativo**
ligado; vínculo de inativo não resolve.
**Como detectar:** reclamação "não aparece no agendamento"; serviços ativos com
Utiliza desligado.

## L28 — Convênios "irmãos" não são iguais

**O que aconteceu:** três convênios da mesma operadora tinham configurações
diferentes entre si (aplicação vazia num, zero nos outros; taxas ligadas só em
um). Um valor que parecia "de todos" era só de alguns.
**Regra que ficou:** nunca copie configuração entre convênios presumindo o
mesmo contrato; confira cada um contra o seu contrato. "Copiar de outro
convênio" só com a régua dos dois conferida.
**Como detectar:** mesma operadora, resultados de Farol diferentes para o mesmo
serviço.

## L29 — Na tela: campo moeda só grava depois de sair do campo

**O que aconteceu:** valores digitados e salvos com o cursor ainda no campo se
perdiam; o Fator K exibia ponto depois de digitado com vírgula; um clique na
linha vizinha quase gravou um percentual no item errado; automação de tela por
coordenadas errava.
**Regra que ficou:** na tela: digitar → sair do campo → reler → só então
salvar; localizar elementos pelo rótulo, nunca por coordenada; reler as linhas
vizinhas antes de salvar. A validação final é o pré-faturamento/Farol.
**Como detectar:** valor some depois de salvar; percentual em linha errada.

## L30 — Estudo de mudança em massa: medir antes de afirmar

**O que aconteceu:** um estudo sobre trocar um subserviço de aplicação no
catálogo afirmou quatro coisas (perda de R$ 852, receita falsa em 50
convênios…) — as quatro estavam erradas. Medido de novo "com a calculadora",
os caminhos davam o mesmo número. O dono tinha razão.
**Regra que ficou:** mudança de catálogo que afeta muitos convênios exige
medição **convênio a convênio** (antes/depois previstos pelo simulador e
conferidos no Farol) antes de recomendar. Mostre as contas.
**Como detectar:** conclusão em R$ sem tabela de medição por convênio.
