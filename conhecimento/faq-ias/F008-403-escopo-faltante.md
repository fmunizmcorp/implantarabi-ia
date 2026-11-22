# F008 — 403: a chave/token não tem a permissão da rota (`escopoFaltante`)

- **Rotas:** qualquer
- **Status HTTP:** 403
- **Mensagem contém:** escopoFaltante | permissão | Permissão
- **Causa:** confirmada (Swagger 22/11) — cada rota exige uma permissão (ex.: `convenio:create`). A
  resposta 403 traz a permissão que falta em `escopoFaltante` e, em `error`, onde liberá-la
- **Status:** comportamento esperado
- **Origem:** Swagger e manual oficial

## O que fazer
- Leia `escopoFaltante` e compare com a sprint: a permissão é **necessária** para o passo atual?
- **Token `rbt_`:** o administrador da clínica edita as permissões do **mesmo** token em
  Configurações › Parâmetros › Integrações (não troca o valor). A mudança vale **na requisição seguinte** —
  repita a chamada uma vez.
- **Chave `rbk_`:** as permissões são definidas pelo time Rabi; peça a inclusão.
- Peça só o necessário. Permissões que o kit recomenda **não** dar ao token de implantação: as de
  `delete`, emissão/cancelamento de NFS-e e `financeiro:create/update` — quando forem precisas, libere,
  use com ordem escrita e retire depois ([../api-externa/proibidas-sem-ordem-escrita.md](../api-externa/proibidas-sem-ordem-escrita.md)).

## O que NÃO fazer
Não pedir "todas as permissões" para não ser incomodado. Não insistir em loop.
