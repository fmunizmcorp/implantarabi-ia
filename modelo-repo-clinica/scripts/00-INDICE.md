# scripts · <NOME_DA_CLINICA>

Hooks da sessão (configurados em `.claude/settings.json`). Não precisam ser rodados à mão.

| Script | Quando roda | O que faz |
|---|---|---|
| `sessao-inicio.sh` | início/retomada/limpeza/compactação | imprime primeiro o **resumo de retomada** (clínica ou "primeira vez", modo, sprint, próximo passo, lacunas abertas, última daily, documentos fora do inventário, validade da chave registrada, se `RABI_API_KEY` existe — sem o valor); depois baixa ou atualiza o kit em `.kit/`, confere se o repo é privado (campo `private` da API do GitHub), mostra o último commit da `main`, mostra o painel do `ESTADO.md`, pendências e se a chave `RABI_API_KEY` existe (sem mostrar o valor) |
| `antes-de-compactar.sh` | antes de compactar o contexto | lembra o que preservar (arquivos modificados, última prova, próximo passo) |
| `ao-parar.sh` | ao fim de cada resposta | se há arquivo sem commit ou commit sem push (fora de `.kit/`), **bloqueia o encerramento uma vez** pedindo commit + push e ESTADO.md atualizado; na segunda vez deixa encerrar |
