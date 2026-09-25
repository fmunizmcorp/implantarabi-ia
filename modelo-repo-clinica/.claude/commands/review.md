---
description: Prepara a review de fechamento da sprint atual (demonstração com foto depois, DoD, pendências) e salva em historico/reviews/.
---
1. Releia a sprint atual (`sprints/Sxx.md` da clínica) e a DoD (definição de pronto) do playbook do kit.
2. Chame o agente `validador-cruzado` sobre as provas da sprint (contexto limpo).
3. Monte a review no modelo de `.kit/prompts/06-mensagens-padrao.md`: o que foi cadastrado (contagens), **foto depois** de 1–3 itens como demonstração, DoD item a item (ok/não ok), o que ficou pendente e por quê, riscos, próxima sprint.
4. Salve em `historico/reviews/Sxx-AAAA-MM-DD.md`, registre a versão do kit usada na tabela de `ESTADO.md`.
5. Peça **uma** decisão: "Posso dar a Sxx como concluída?" — só marque 100% depois do sim.
6. Commit + push.
