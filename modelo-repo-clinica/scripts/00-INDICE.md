# scripts · <NOME_DA_CLINICA>

Hooks da sessão (configurados em `.claude/settings.json`). Não precisam ser rodados à mão.

| Script | Quando roda | O que faz |
|---|---|---|
| `sessao-inicio.sh` | início/retomada/limpeza/compactação | baixa ou atualiza o kit em `.kit/`, confere se o repo é privado, mostra o painel do `ESTADO.md`, pendências e se a chave `RABI_API_KEY` existe (sem mostrar o valor) |
| `antes-de-compactar.sh` | antes de compactar o contexto | lembra o que preservar (arquivos modificados, última prova, próximo passo) |
| `ao-parar.sh` | ao fim de cada resposta | avisa (não bloqueia) se há mudança sem commit ou se o `ESTADO.md` não foi atualizado hoje |
