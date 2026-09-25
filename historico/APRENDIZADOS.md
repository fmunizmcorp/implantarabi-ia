# APRENDIZADOS do kit (para o mantenedor)

## K01 — A sessão web trabalha numa branch; a próxima abre na padrão
Cada sessão do Claude web faz push numa branch `claude/...`. Sem levar à `main`, a sessão seguinte
não vê o ESTADO nem os hooks. Regra: todo repo de clínica tem automerge `claude/** → main`.

## K02 — Repo privado não é baixado por sessão que não o tem ligado
O proxy da sessão só lê repos privados ligados a ela. Um kit privado exigiria convite + ligação em
cada clínica. Decisão: kit público e público-seguro (CI de vazamento).

## K03 — "200 da API do GitHub" não quer dizer público
Pelo proxy autenticado, repo privado ligado responde 200. Confira o campo `"private"`.

## K04 — Documentação de API externa ≠ comportamento
O Swagger de 25/09 diz 401 para chave inválida; a medição do mesmo dia deu 503. O kit trata os dois
como "problema de chave" e registra a medição para reconfirmar.

## K05 — Validação cruzada e simulação acham coisas diferentes
A revisão por leitura achou regras erradas (PUT que apagaria dados); a simulação achou quebras de
fluxo (branch, clone, imports). Fazer sempre as duas antes de publicar versão.
