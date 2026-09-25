---
name: configurar-convenio
description: Roteiro com atenção redobrada para configurar UM convênio no Sistema Rabi (dados, prazos e as abas Serviços/Produtos/Taxas/Especialidades/Colaboradores) a partir do contrato e da tabela, usando o motor de conversão (.kit/ferramentas/conversao) para prever valores e o Farol antes e depois. Use no modo Convênio e na sprint S10/S11.
---

# Skill: configurar convênio

Prompt completo do modo: `.kit/prompts/04-modo-convenio.md`. Regras de preço:
`.kit/conhecimento/precos-e-conversao/` (leia pelo índice). Playbooks:
`.kit/sprints/S10-convenios.md` (visão), `.kit/sprints/S10a-convenio-dados.md`,
`.kit/sprints/S10b-convenio-abas-e-precos.md` e `.kit/sprints/S11-conferencia-farol.md`.

## Sequência
1. **Diagnóstico do estado** do convênio: NOVO · EM ANDAMENTO · FECHADO
   (ver `.kit/prompts/04-modo-convenio.md`). Fechado → agente `auditor-regressao` primeiro.
2. **Régua contratual** (agente `extrator-documentos`) em
   `dados/convenios/<slug>/regua-contratual.md`, cada prazo e valor com cláusula/página.
3. **A pergunta que abre tudo:** pacote fechado, conta aberta ou misto? Quais
   serviços são pacote? Sem resposta → pendência, não configura preço.
4. **CSV com ORIGEM:** `dados/convenios/<slug>/precos-<slug>.csv` (cabeçalho
   do modelo; confira as colunas aceitas em `.kit/ferramentas/conversao/montar_convenio.py`).
5. **Prever:** `python3 .kit/ferramentas/conversao/simulador.py` → Σ do serviço, linha
   "valor próprio" e Farol previstos. Mostre a prévia em tabela.
6. **Montar os corpos:** `python3 .kit/ferramentas/conversao/montar_convenio.py`
   (ordem: Utiliza → valores → textos/códigos → tipo de atendimento → Pacote/Zerar).
7. **Gravar** pela skill `ritual-de-carga`, **um convênio por vez**, lote ≤ 200
   por aba, um lote por vez (senão 429).
8. **Conferir:** `python3 .kit/ferramentas/conversao/conferir_farol.py` + agente
   `conferente-precos` (contexto limpo). Mínimo **3 serviços** conferidos:
   simples, com medicamento, com pacote.
9. **Registrar:** `decisoes.md` do convênio, `sprints/S10.md`, `ESTADO.md`,
   `ANALISE-CONTRATOS.md` (6 dimensões), commit + push.

## Regras de ouro de preço (resumo; a fonte é o kit)
- **Vazio** = "sem regra aqui", o sistema sobe de nível. **0,00** = zero de verdade. **0,01 como marcador é proibido.**
- **Valor combinado NÃO é pacote.** Preço fechado = valor combinado + **Pacote** + **Zerar** nos itens inclusos.
- Item incluso em serviço com Pacote fechado recebe Zerar; a aplicação/serviço raiz **não** é zerada.
- **Conta aberta** = sem Pacote e sem Zerar.
- Nunca Zerar um **medicamento** fora de pacote fechado (a clínica entregaria sem cobrar).
- Nunca desligar serviço que a clínica presta; nunca desligar o serviço e deixar o produto ligado.
- Tabela interna = preço de **produto**; o preço particular vem do convênio "Particular".
