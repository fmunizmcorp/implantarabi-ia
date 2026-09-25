# Lições — API externa do Rabi

> **Fonte:** registros de uma implantação real anterior (sessões de 22 a 25/09/2026, incluindo leitura real só-GET em 25/09), generalizados · https://www.rabisistemas.com.br/manual/api-externa/erros-e-boas-praticas.html#armadilhas · **Conferido em:** 2026-09-25
> **Vale para:** API externa em produção em 25/09/2026 · **Kit:** v0.1.0

Convenções atuais da API: [../api-externa/00-INDICE.md](../api-externa/00-INDICE.md).
Origem das lições: [origem.md](origem.md).

## L01 — Chave inválida já respondeu 503, não 401

**O que aconteceu:** a chave foi trocada três vezes num mesmo dia; as revogadas
passaram a responder 503 (`"Não foi possível validar a chave de API."`). Reconfirmado em
25/09 ~12h em produção **e** homologação: chave inexistente e chave real não aceita
(revogada/não ativada) → 503; sem cabeçalho → 401. Uma sessão que tratasse 503
como instabilidade ficaria em laço de nova tentativa, sem nunca avisar que a
chave morreu.
**Regra que ficou:** 401 **e** 503 no primeiro teste = problema de chave. Pare,
avise o usuário, peça a chave nova. Sem retry em loop. (O Swagger de 25/09 diz 401 para chave rejeitada e 503 só para falha de rede —
na prática, 503 = chave não aceita. Trate os dois do mesmo jeito.) A validade
medida de uma chave de implantação foi de **~7 dias**: olhe
`X-ApiKey-Expires-At` em toda abertura e peça a renovação cedo.
**Como detectar:** toda chamada falha com 401/503 desde o início da sessão;
cabeçalho `X-ApiKey-Expires-At` ausente ou vencido.

## L02 — PUT sobrescreve: campo omitido ou com nome errado é APAGADO

**O que aconteceu:** para tirar um vínculo de um serviço, a sessão montou o
corpo do PUT com os nomes de campo que a **leitura** devolve. A gravação usa
nomes diferentes (ex.: um nome no plural e outro com uma letra trocada). Os
campos "não reconhecidos" foram tratados como ausentes: o valor do serviço foi
de R$ 600,00 para R$ 0,00 e a especialidade sumiu. A restauração pela API não
funcionou; só pela tela.
**Regra que ficou:** PUT é **sobrescrita**, exceto as rotas que declaram
upsert (abas do convênio e dois parâmetros). Sempre: GET antes → montar o
objeto **completo** com os nomes do **schema de escrita** do Swagger → prévia →
gravar → GET depois e comparar **todos** os campos, não só o alterado. Para
`/servicos` e `/produtos`, converta a leitura com `ferramentas/rabi_api/corpo_escrita.py`
(ele recusa quando falta campo obrigatório de escrita). A leitura real (medida em
25/09/2026) mostra por quê: o `GET /servicos/{id}` **não traz** a composição
(produtos, taxa, subserviços, equipamentos) nem as especialidades — elas têm de
vir do dicionário de IDs / da foto da prova da criação (S08); o `GET /produtos/{id}`
traz fabricante, tipo, unidade e depósito **aninhados** (objeto, não id).
**Como detectar:** diff depois × antes mostra campos que você não pretendia
mudar (zerados, vazios, listas encolhidas).

## L03 — No convênio, omitir campo também limpa coisas

**O que aconteceu:** a documentação da rota de atualização do convênio avisa:
omitir a operadora remove a operadora; omitir datas de fim/reajuste/renovação
limpa as datas; omitir `exigirToken` grava `false`; a lista de políticas por
tipo de produto, quando enviada, é a lista completa (as que faltarem são
inativadas).
**Regra que ficou:** no PUT dos **dados** do convênio, mande o objeto
**completo**. O `GET /convenios/{id}` real (medido em 25/09/2026) traz datas,
prazos, `exigirToken` e `faturadoPagamento` — use-o como base; mas
`unidadesIds` e `politicasPorTipoProduto` **NÃO vêm** (nem `fatorK`): complete
da régua contratual (`dados/convenios/<slug>/regua-contratual.md`) + dicionário
de IDs (`dados/dicionario-de-ids.md`). Confira os nomes de leitura × escrita no
schema do PUT (`ConvenioUpdate`) antes de reenviar (ex.: a leitura traz
`empresaPrincipalId`, a escrita pede `empresaId`) e confira na tela antes e
depois. Nunca mande só "o que mudou", nem "o GET cru".
**Como detectar:** depois do PUT, operadora vazia, datas nulas, políticas
inativadas.

## L04 — Paginação da API externa começa em 1

**O que aconteceu:** `page=0` devolveu erro 400. A API interna (outra, usada
pela tela) começa em 0 — misturar as duas confunde.
**Regra que ficou:** API externa: `page` a partir de 1, `pageSize` até 200;
percorra até `totalPages` e confira o `total`.
**Como detectar:** 400 na primeira página; soma de itens lidos ≠ `total`.

## L05 — Formatos de lista diferentes e listas que "não paginavam"

**O que aconteceu:** até 24/09, quatro listagens vinham fora do envelope padrão
e algumas devolviam a lista inteira ignorando `pageSize` (uma delas, com 8 mil
itens e quase 8 MB). Corrigido em produção em 25/09.
**Regra que ficou:** o cliente normaliza qualquer envelope e confere `total`;
nunca presuma o formato; leitura grande vai para arquivo, não para a conversa.
**Como detectar:** resposta sem `dados`/`total`; tamanho de resposta muito
acima do esperado.

## L06 — Unidades e formatos que fogem da regra

**O que aconteceu:** algumas leituras de faturamento vinham em **centavos** (a
regra geral é reais); um "valor total" era só o do serviço, sem produtos e
taxas; parâmetros nunca configurados devolviam o número `0` cru, `null` com
200, ou 404; um `id` de status era texto.
**Regra que ficou:** leia a descrição da rota no Swagger antes de interpretar
um número; guarde a unidade junto do valor; "não configurado" é estado válido,
não erro.
**Como detectar:** valores 100× maiores; totais que não batem com a guia;
corpo `0`/`null` em parâmetro.

## L07 — A API externa não cobre tudo

**O que aconteceu:** perfis e permissões, modelos de documento e impressão,
lotes/XML de faturamento e auditoria ficavam fora da API externa. A tentação é
usar a API interna da tela (token de 5 minutos, nomes não documentados) — foi
por ela que aconteceu a L02.
**Regra que ficou:** o que a API externa não cobre é feito **na tela**, com o
implantador, a partir de uma prévia aprovada. API interna só com ordem escrita.
**Como detectar:** rota não existe no Swagger do dia.

## L08 — Há rotas que não se chamam sem ordem escrita

**O que aconteceu:** a chave da clínica grava em nota fiscal, dinheiro e
estoque real. O dono pediu "muito cuidado no uso".
**Regra que ficou:** sem ordem escrita do dono, **não** chamar: emitir,
cancelar ou substituir NFS-e; criar/alterar movimentações financeiras (podem
disparar NFS-e); entrada/saída/transferência de estoque; `DELETE` (inativa);
rotas `/bulk` sem prévia item a item; criação de login fora da sprint de
colaboradores; leitura de pacientes e histórico sem finalidade. Lista completa
em `../api-externa/`.
**Como detectar:** a rota tem efeito fiscal, financeiro, de estoque, de acesso
ou em massa.

## L09 — Conferir o alcance da chave no início de toda sessão

**O que aconteceu:** o "conhecimento antigo" dizia que a chave só alcançava 3
áreas; já alcançava as 25. Outra vez faltava uma permissão de leitura
(equipamentos), liberada depois.
**Regra que ficou:** abertura de sessão = teste de leitura em todas as áreas
(1 item por área) + validade da chave; gravar o resultado no repo da clínica.
**Como detectar:** 403 em uma área; `X-ApiKey-Expires-At` perto de vencer.

## L10 — Contagem da API ≠ contagem da tela

**O que aconteceu:** a API mostrava 335 serviços ligados num convênio e a tela
193. A diferença eram vínculos de serviços **inativos no catálogo** que
continuavam ligados no convênio.
**Regra que ficou:** ao contar, cruze com o status do item no catálogo (ativo ×
inativo). Vínculo de item inativo é resíduo — não "conserte" dando valor a ele.
**Como detectar:** contagens diferentes entre API e tela; itens com código
estranho ao convênio (ex.: código de outro procedimento).
