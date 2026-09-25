# Lições — ler dados certo antes de concluir

> **Fonte:** registros de uma implantação real anterior e de outros projetos de IA do mesmo mantenedor (generalizados) · **Conferido em:** 2026-09-25
> **Vale para:** toda leitura de sistema externo (API, tela, arquivo) · **Kit:** v0.1.0

Origem das lições: [origem.md](origem.md).

## L11 — "200 com corpo vazio" lido como "não existe nada"

**O que aconteceu:** um atalho de leitura devolvia, em vários endereços, status
200 com corpo vazio. A sessão leu isso como dado real ("nenhum produto ligado")
e tirou quatro conclusões erradas sobre um medicamento — até mandou números
errados ao dono. O mesmo tipo de armadilha já estava documentado e não foi lido.
**Regra que ficou:** toda leitura distingue **três estados**: sucesso com
dados, sucesso vazio (o servidor disse que está vazio) e **falha** (status ≠
200, erro no corpo, **0 bytes**, formato inesperado). Leitura que falha
**interrompe** a conclusão.
**Como detectar:** respostas de 0 bytes; listas vazias onde a tela mostra itens;
"todos desligados" de repente.

## L12 — "Sucesso" na tela não prova que gravou

**O que aconteceu:** em outros projetos do mesmo mantenedor, uma importação
disse "sucesso" e gravou R$ 0,00 num lote de valor alto; outra "bateu" o valor
por coincidência de configuração; uma tela dizia "salvo" e descartava tudo.
**Regra que ficou:** o único check válido é **reler o registro gravado e
comparar com a fonte, campo a campo** — e medir o agregado antes/depois. Teste
também um caso em que a fonte difere do que o sistema calcularia, para provar
qual valor foi usado.
**Como detectar:** agregado (saldo, total, contagem) não mudou depois da
gravação; valor "próximo" mas diferente da fonte.

## L13 — Leu o campo errado e concluiu errado

**O que aconteceu:** a sessão leu o "valor unitário" de um produto num endereço
que, na verdade, trazia **saldo de estoque** (números negativos) e afirmou que
o preço estava errado. O preço de catálogo vinha de outra rota, e estava certo.
**Regra que ficou:** antes de interpretar um campo, confirme no Swagger/manual
o que ele significa naquela rota. Valor negativo em "preço" é sinal de campo
errado.
**Como detectar:** preços negativos, iguais a quantidades, ou que não batem
com a tela.

## L14 — Gravar sabendo só o ID, sem o nome e o status

**O que aconteceu:** com a tela deslogada e só os IDs da API em mãos, a sessão
gravou R$ 0,01 em 12 linhas que achava serem de um certo procedimento. Quando
leu os nomes, eram seis serviços diferentes (antibióticos, protetor gástrico,
ferro) — todos **inativos** no catálogo. Reverteu tudo, com prova de zero
diferença contra o estado original.
**Regra que ficou:** antes de gravar: **nome do item** + **ativo/inativo**
(serviço, produto, taxa e convênio) + confirmação da condição que o dono impôs.
Sem nome, não grava.
**Como detectar:** prévia de gravação sem coluna "nome" ou "status".

## L15 — "Errado agora" não é "errado para sempre"

**O que aconteceu:** num projeto do mesmo mantenedor, um totalizador divergente
foi reportado como corrupção permanente; dois dias depois estava certo sem
ninguém mexer (rotina posterior recalculou, ou correção subiu).
**Regra que ficou:** ao reportar defeito de total/saldo, diga "observado em
tempo real; não verificado se rotina posterior recalcula". Só afirme
"permanente" após reobservar numa segunda janela de tempo.
**Como detectar:** divergência em campo agregado; sistema com rotinas noturnas.

## L16 — A 1ª linha (🔒) da tela do convênio não é o valor do convênio

**O que aconteceu:** uma sessão leu o valor da primeira linha das abas do
convênio como se fosse o preço do convênio. É o valor de **origem** (cadastro).
O do convênio é o convertido (🔁) e o efetivo é o ✅.
**Regra que ficou:** leia as 3 linhas (4 na coluna Valor do serviço) com o
significado de cada uma; o que sai na guia é o ✅ (e o total é o Σ).
**Como detectar:** "todos os convênios têm o mesmo preço" = você está lendo 🔒.

## L17 — Contexto não é depósito de JSON

**O que aconteceu:** ler 200 serviços com a resposta inteira na conversa gasta
dezenas de milhares de tokens e deixa a sessão lenta e esquecida. Uma varredura
de 8 mil posições de estoque custou quase nada quando o comando gravou em
arquivo e um script devolveu três números.
**Regra que ficou:** *o terminal processa, o contexto recebe o resumo.* Leitura
grande → arquivo → script conta/filtra → 10–20 linhas na conversa.
**Como detectar:** respostas de ferramenta com milhares de linhas de JSON.

## L18 — Fonte primária prevalece sobre aviso e sobre planejamento

**O que aconteceu:** um aviso interno dizia "a API não cria depósito"; o
Swagger tinha `POST /depositos`. Em outro momento, documentos de planejamento
(histórias de usuário) descreviam como vigente algo que nunca foi para
produção.
**Regra que ficou:** ordem de confiança: **o que o sistema faz em produção
(tela/API relida) > Swagger do dia e manual oficial > avisos, wiki, planos e
memória**. Divergência vira registro, com a fonte que prevaleceu.
**Como detectar:** afirmação sem data ou sem fonte; documento marcado como
"planejamento" ou "HU".

## L19 — Script que depende de dado ausente "roda" e engana

**O que aconteceu:** scripts de processamento foram enviados sem os arquivos de
entrada; rodariam "com sucesso" sobre nada.
**Regra que ficou:** antes de processar, confirme que os arquivos de entrada
existem e têm o tamanho esperado; processe o que existe e diga exatamente o que
falta. Não declare resolvido o que depende de dado ausente.
**Como detectar:** contagem de entrada 0 ou menor que a esperada.
