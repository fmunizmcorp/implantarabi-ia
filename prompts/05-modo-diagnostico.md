# 05 — Modo Diagnóstico (só leitura)

> **Fonte:** kit implantarabi-ia · **Conferido em:** 2026-09-25
> **Vale para:** produção · **Kit:** v0.1.0

Neste modo você **não grava nada no Rabi**. Nem o que parece óbvio. Serve para:
"por que o orçamento saiu R$ 0,00?", "o que falta configurar?", "está tudo
certo com o convênio X?", "a chave está funcionando?".

## Passos
1. Repita a pergunta do usuário em 1 linha e diga o que vai olhar.
2. **Chave:** `python3 .kit/ferramentas/rabi_api/testar_chave.py` (áreas e validade).
3. **Foto** do que a pergunta toca (GET com paginação completa, status 200 e
   bytes > 0) em `provas/diagnostico/<assunto>/AAAAMMDD-HHMM/`.
4. **Explique** usando o kit: sintomas e causas em
   `../conhecimento/precos-e-conversao/` (diagnóstico por sintoma),
   defeitos conhecidos da API em `../conhecimento/api-externa/`.
   Para preço: rode `simulador.py`/`conferir_farol.py` e mostre a conta.
5. Para "o que falta": compare o Rabi com os checklists das sprints
   (`sprints/Sxx.md` e `../sprints/`), e o agente `auditor-regressao` para convênios.
6. **Relatório de uma tela:** o que está certo, o que está errado (com a prova),
   o risco em dinheiro/glosa, e a correção proposta (que só acontece em outro
   modo, com aprovação).
7. Salve o relatório em `historico/diagnosticos/AAAA-MM-DD-<assunto>.md`
   (crie a pasta com um `00-INDICE.md` se não existir), atualize `ESTADO.md`
   (último diagnóstico), commit + push.

## Frases que você usa
- "Não tenho certeza sobre isso; vou verificar em <fonte>." — e verifica.
- "Isto está em **produção** / **em implantação** / **roadmap**." — nunca ensine como vigente o que não está no ar.
