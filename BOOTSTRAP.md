# BOOTSTRAP — Protocolo de toda sessão de implantação Rabi

> Adaptado do protocolo MAESTRO (6 Leis). Vale para a sessão do mantenedor do
> kit e para toda sessão de clínica. **Obedeça antes de qualquer ação.**

## As 6 Leis

1. **Estado vive em ARQUIVO, nunca só na conversa.** No repo da clínica a
   verdade do "agora" está em `ESTADO.md` e em `sprints/Sxx.md`. Você **relê**,
   não "lembra". Atualize depois de cada passo.
2. **Verifique antes de dizer "pronto".** Toda gravação no Rabi termina com
   *foto depois + diff*. O que não foi relido é **NÃO CONFIRMADO** — e é isso
   que se escreve.
3. **Nada se perde.** Toda mensagem do cliente/implantador vai verbatim para
   `historico/requisitos/raw/`. Toda decisão vira linha em `decisoes/DECISOES.md`.
   Todo documento recebido entra no `documentos-do-cliente/inventario.md`.
4. **1 detalhe = 1 microsprint.** Um cadastro (ou um lote aprovado) por vez:
   prévia → aprovação → grava → prova → commit → atualiza ESTADO.
   A cada 5–10 microsprints, uma revisão (PDCA) com o usuário.
5. **Kit primeiro.** Antes de agir, consulte o kit (`.kit/` no repo da
   clínica): o playbook da sprint, a API, a árvore de decisão de preços. Se o
   kit e a clínica divergirem, vale `diretrizes-da-equipe.md` da clínica, e a
   divergência é registrada.
6. **Não minta, não enrole, não invente.** Valor sem documento vira pendência,
   não chute. Diga "não tenho certeza sobre isso" e vá verificar.

## Ciclo de toda sessão

```
ABRIR → [LOOP de microsprints] → CHECKPOINT → FECHAR
```

**ABRIR (automático):**
1. Ler este BOOTSTRAP e `conhecimento/00-ESSENCIAL.md`.
2. Ler `ESTADO.md`, `PAPEIS.md`, `diretrizes-da-equipe.md` e a sprint atual.
3. Apresentar-se ao usuário (modelo em `prompts/01-abertura-sessao.md`):
   quem é, o painel de progresso, o próximo passo, e perguntar o **modo**
   (Implantação · Atualização · Convênio · Diagnóstico).

**LOOP:** Explorar → Planejar → Prévia → Aprovar → Gravar → Provar → Commit →
Atualizar `ESTADO.md` e a sprint → mostrar a evolução ao usuário.

**CHECKPOINT:** commit + push depois de cada passo concluído. Se o contexto
encher, pode limpar: o estado está nos arquivos.

**FECHAR:** `ESTADO.md` com o **próximo passo concreto**, `historico/HISTORICO.md`
atualizado, lições em `historico/APRENDIZADOS.md`, commit + push.

## Validação cruzada
Quem gravou não valida sozinho: a conferência de preços de convênio usa o
agente `conferente-precos` (contexto limpo) e a ferramenta
`ferramentas/conversao/conferir_farol.py`.

**Lema:** *Nada se perde. Tudo é verificado. Uma pergunta por vez.*
