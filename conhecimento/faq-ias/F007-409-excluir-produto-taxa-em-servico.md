# F007 — 409 ao inativar produto ou taxa: "está na composição de serviço ativo"

- **Rotas:** DELETE /produtos/{id} · DELETE /taxas/{id}
- **Status HTTP:** 409
- **Mensagem contém:** ITEM_EM_USO_EM_SERVICOS | em uso em | composição | serviço ativo
- **Causa:** confirmada (Swagger 22/11; produção desde 02/10/2026, #626) — o Rabi passou a **recusar**
  inativar produto/taxa usado em algum serviço ativo. Antes, a exclusão passava e o serviço ficava com
  item morto (preço e Farol errados sem aviso)
- **Status:** proteção do Rabi (não é defeito)
- **Origem:** Swagger e manual oficial

## O que fazer
1. A resposta traz em `servicos` a lista dos serviços que usam o item. Mostre ao usuário (nome e código
   do serviço, nunca valor contratado).
2. Pergunte o que ele quer, uma pergunta por vez: **substituir** por outro produto/taxa ou **retirar** do
   serviço. Cada serviço alterado passa pelo ritual (foto antes → prévia → aprovação → `PUT /servicos/{id}`
   com a **lista completa** de `produtoIds`/`servicoTaxa` desejada — lista enviada substitui → foto depois).
3. Só então repita o `DELETE` (que já exigia ordem escrita).

## O que NÃO fazer
Não "zerar" a composição de vários serviços em lote para conseguir excluir. Não mandar `[]` sem prévia:
lista vazia apaga todos os vínculos daquele tipo.
