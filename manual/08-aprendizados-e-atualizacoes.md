# Parte I — Aprendizados e atualizações

> **Fonte:** este kit (canal de aprendizados, v0.3.0) · **Conferido em:** 2026-09-25
> **Vale para:** produção em 25/09/2026 · **Kit:** v0.3.0

Duas coisas acontecem sozinhas, em toda clínica, para o kit ficar cada vez melhor.

## I1 — A IA manda ao kit o que aprendeu (com o seu clique)

Quando a IA descobre algo que serve a **todas** as clínicas (uma conta que o
Rabi faz diferente do que o kit dizia, uma regra que faltava, um comportamento
da API, um jeito melhor de conduzir), ela:

1. escreve o aprendizado **sem nenhum dado da clínica** (nada de nome, CNPJ,
   CPF, pessoa, paciente, código interno, valor do contrato);
2. passa por um **filtro automático** que bloqueia qualquer coisa parecida com
   dado da clínica;
3. mostra a você o texto final e pergunta **uma vez**: "Posso enviar para o kit?".

Se você disser sim, ela entrega um **link**. Abra, confira o texto e clique em
**Submit new issue** (é preciso estar logado no GitHub). Pronto.

**Atenção:** o texto enviado fica **público** no GitHub do kit. Por isso a
regra é rígida: só o método, nunca o dado. Na dúvida, diga "não envie".

Tem vários aprendizados guardados? Escreva `enviar aprendizados`.

## I2 — A IA se atualiza sozinha com as novidades do kit

Em toda sessão a IA baixa a versão mais nova do kit. Se houver novidade, ela:

- conta em até 3 linhas o que mudou para a sua clínica;
- atualiza as instruções e os scripts do repositório da clínica (nunca os seus
  dados, documentos, provas ou senhas) e salva;
- se a novidade mexer em algo que **já foi gravado** no Rabi (por exemplo, uma
  regra de preço), abre uma pendência e propõe um **diagnóstico** (só leitura).
  Nada é corrigido no Rabi sem a sua aprovação.

Você não precisa fazer nada, só ler o resumo.

## I3 — Quem consolida

A equipe Rabi lê os aprendizados enviados de tempos em tempos, confere, e o que
for aprovado entra no kit. Na sessão seguinte, **todas** as clínicas recebem.
