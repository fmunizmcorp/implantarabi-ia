# 08 — Contribuir com o kit (aprendizados, sem dado da clínica)

> **Fonte:** decisão do mantenedor em 25/09/2026 (canal de aprendizados) · **Conferido em:** 2026-09-25
> **Vale para:** toda sessão de clínica · **Kit:** v0.3.0

O kit melhora com o que cada implantação descobre. Você (IA da clínica) manda
para o kit **o método**, nunca o dado: forma de cálculo, correção de regra,
comportamento real da API, jeito melhor de conduzir. O mantenedor consolida
de tempos em tempos e a melhoria volta para todas as clínicas pelo `.kit/`.

## Quando registrar (sem esperar o usuário pedir)
- O Rabi real fez diferente do que o kit diz (cálculo, Farol, conversão, campo, rota, código de erro).
- Você corrigiu algo seguindo uma regra que o kit não tinha.
- Uma ferramenta do kit (`.kit/ferramentas/…`) errou ou faltou.
- Um jeito de conduzir funcionou muito melhor (ou pior) que o do kit.
- Em **toda review de sprint**: pergunte-se "algo desta sprint serve às outras clínicas?".

Não é aprendizado: preferência desta clínica (isso vai para `diretrizes-da-equipe.md`),
valor de contrato, lista de cadastros.

## Como (4 passos, uma pergunta só)
1. **Rascunho:** `python3 .kit/ferramentas/kit/filtrar_aprendizado.py novo --titulo "…" --tipo calculo|regra|api|processo|ferramenta --arquivo <arquivo do kit>`
   e preencha as seções. Escreva genérico: "um convênio com Fator K de 10% (exemplo)",
   nunca o nome do convênio com o valor contratado. Valores em R$ só com a palavra "exemplo".
2. **Filtro:** `python3 .kit/ferramentas/kit/filtrar_aprendizado.py filtrar contribuicoes-kit/<arquivo>.md`.
   BLOQUEADO → generalize e rode de novo (nunca contorne o filtro). LIMPO → ele mostra o texto final e o link.
3. **Pergunta única ao usuário — só no FIM da sessão ou da review**, nunca na abertura e nunca
   junto de outra pergunta da implantação (junte vários aprendizados nesta mesma pergunta):
   > "Aprendi algo que pode ajudar outras clínicas: <título em 1 linha>. O texto não tem nenhum
   > dado da clínica (abaixo). Posso enviar para o kit do Rabi? É só abrir o link, conferir e
   > clicar em **Submit new issue**. Atenção: a mensagem fica pública no GitHub."
   Mostre o texto final. Se tiver ferramenta de GitHub que consiga criar issue em
   `fmunizmcorp/implantarabi-ia`, pode abrir direto depois do sim (mesmo texto, label
   `aprendizado-clinica`); não tenho certeza de que a sessão da clínica tem essa permissão — se falhar, use o link.
4. **Registro:** com o número da issue, `… filtrar_aprendizado.py enviado contribuicoes-kit/<arquivo>.md --issue N`.
   Sem resposta do usuário: o item fica na fila (status `filtrado`) e o hook lembra nas próximas sessões.
   Commit + push.

Frase do usuário **`enviar aprendizados`**: percorra a fila (`contribuicoes-kit/00-INDICE.md`)
e faça os passos 2–4 para cada item `rascunho`/`filtrado`.

## Nunca
- Documento, print, JSON de prova, planilha, trecho de contrato.
- Nome da clínica, de pessoa, de paciente; CNPJ/CPF; ID do Rabi; link do repo da clínica; chave.
- Enviar sem o filtro LIMPO e sem o sim do usuário.

Pode citar: regra **pública** (ANS, TISS, manual do Rabi, norma publicada pela própria operadora).
Nome de operadora só junto de regra pública dela — **nunca** junto de valor, condição
contratual, convênio desta clínica ou prazo negociado.

**Valores:** qualquer número com cara de dinheiro (`187,43`, `R$ 90`) ou percentual com
casa decimal (`12,5%`) só passa no filtro com o marcador **`(exemplo)`** colado logo
depois do número — e tem de ser um valor inventado para ilustrar, nunca o do contrato.
Registre também em `historico/APRENDIZADOS.md` (coluna "Sugerida ao kit?").
