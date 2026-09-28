# F001 — Cadastro de serviço dá 500 "Cannot read properties of undefined (reading 'filter')"

- **Rotas:** POST /servicos · PUT /servicos
- **Status HTTP:** 500
- **Mensagem contém:** reading 'filter' | Cannot read properties of undefined
- **Causa:** confirmada no código do Rabi (`CreateServicoUseCase` faz `especialidadesId.filter(...)` sem valor padrão; leitura do `deploy_prd` em 28/09/2026)
- **Status:** **corrigido pelo Rabi em 28/09/2026, em produção às 17:43 (Brasília)** — commit `c73e84de` ("campos opcionais omitidos pela API externa quebravam ou gravavam dados errados"). Mandar as 4 listas continua sendo boa prática (corpo completo)
- **Origem:** implantação real (clínica anônima), 28/09/2026

## O que acontecia (explicação técnica, para a equipe)
A rota da API externa (`POST /api/v1/integrations/servicos`) reaproveita o use case
`CreateServicoUseCase` feito para a tela do sistema, que **sempre** manda todos os campos. O
código fazia `especialidadesId.filter(e => e !== null)` sem valor padrão. Pela API, quem não
manda `especialidadesId` (o Swagger dizia que só `nome` e `descricao` são obrigatórios) fazia
`undefined.filter(...)` → `TypeError` → **500**. Nada era gravado. Além disso, o Swagger
documentava `produtoIds`/`equipamentoIds`/`servicosRelacionados` como listas de **IDs**, mas o
use case lia **objetos** (`{id, quantidade, valorUnitario}`, `{id}`, `{servicoId, quantidade}`):
mandar IDs puros também podia quebrar ou gravar errado.

**Correção do Rabi (28/09):** `(especialidadesId ?? []).filter(...)` e um "normalizador" nas rotas
POST/PUT de serviço que aceita ID puro ou objeto; taxas passaram a `servicoTaxa: [{taxaId,
quantidade}]`. Veja também [F006](F006-conferir-gravacoes-anteriores-a-28-09.md) (outros defeitos
corrigidos na mesma hora).

## O que acontece (antes de 28/09 17:43)
O corpo foi enviado sem a lista `especialidadesId` (e/ou as outras listas). O Rabi
tenta percorrer a lista que não veio e quebra com erro 500. **Nada é gravado.**

## O que fazer
1. (Hoje não é mais obrigatório, mas continue) envie as quatro listas, mesmo vazias:
   `"especialidadesId": [], "produtoIds": [], "equipamentoIds": [], "servicosRelacionados": []`.
2. Monte o corpo com `ferramentas/rabi_api/corpo_escrita.py` (já inclui as listas).
3. Refaça **uma** vez, com o ritual (foto antes → prévia → grava → foto depois).
4. Se agora vier **400 genérico**, veja a [F002](F002-400-generico-area-inteira.md).

## Corpo mínimo que funciona (só os NOMES dos campos)
Espelhe um serviço que já existe na clínica (leia com `GET /servicos/{id}` e converta com
`corpo_escrita.py`) e troque só o que é do serviço novo:
`nome`, `descricao`, `codigo`, `tipoServicoId`, `tipoGuiaId`, `tipoAtendimento`, `tempoServico`,
`valor` (em reais), as 4 listas `especialidadesId`, `produtoIds`, `equipamentoIds`,
`servicosRelacionados` e as taxas em `servicoTaxa`. Grave **um** serviço primeiro, com foto depois; só então os demais.

## O que NÃO fazer
- Não repetir o mesmo corpo esperando outro resultado.
- Não abrir chamado por isto sem antes testar com as listas (o contorno resolve).
