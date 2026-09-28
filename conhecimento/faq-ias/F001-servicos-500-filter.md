# F001 — Cadastro de serviço dá 500 "Cannot read properties of undefined (reading 'filter')"

- **Rotas:** POST /servicos · PUT /servicos
- **Status HTTP:** 500
- **Mensagem contém:** reading 'filter' | Cannot read properties of undefined
- **Causa:** confirmada no código do Rabi (`CreateServicoUseCase` faz `especialidadesId.filter(...)` sem valor padrão; leitura do `deploy_prd` em 28/09/2026)
- **Status:** aberto no Rabi — conferido de novo no `deploy_prd` de 28/09 19:28 UTC: o código do cadastro de serviço não mudou; o contorno continua obrigatório
- **Origem:** implantação real (clínica anônima), 28/09/2026

## O que acontece
O corpo foi enviado sem a lista `especialidadesId` (e/ou as outras listas). O Rabi
tenta percorrer a lista que não veio e quebra com erro 500. **Nada é gravado.**

## O que fazer
1. Envie **sempre** as quatro listas, mesmo vazias:
   `"especialidadesId": [], "produtoIds": [], "equipamentoIds": [], "servicosRelacionados": []`.
2. Monte o corpo com `ferramentas/rabi_api/corpo_escrita.py` (já inclui as listas).
3. Refaça **uma** vez, com o ritual (foto antes → prévia → grava → foto depois).
4. Se agora vier **400 genérico**, veja a [F002](F002-400-generico-area-inteira.md).

## Corpo mínimo que funciona (só os NOMES dos campos)
Espelhe um serviço que já existe na clínica (leia com `GET /servicos/{id}` e converta com
`corpo_escrita.py`) e troque só o que é do serviço novo:
`nome`, `descricao`, `codigo`, `tipoServicoId`, `tipoGuiaId`, `tipoAtendimento`, `tempoServico`,
`valor` (em reais) e as 4 listas `especialidadesId`, `produtoIds`, `equipamentoIds`,
`servicosRelacionados`. Grave **um** serviço primeiro, com foto depois; só então os demais.

## O que NÃO fazer
- Não repetir o mesmo corpo esperando outro resultado.
- Não abrir chamado por isto sem antes testar com as listas (o contorno resolve).
