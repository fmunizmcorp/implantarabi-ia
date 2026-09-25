# Partes C e D — Todos os dias e outros modos

> **Fonte:** este kit ([modos de sessão](../metodologia/modos-de-sessao.md)) + https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#tempo-estimado · **Conferido em:** 2026-09-25
> **Vale para:** produção em 25/09/2026 · **Kit:** v0.1.2

Voltar ao [manual](../MANUAL-PASSO-A-PASSO.md).

## Parte C — Todos os dias

### C1 — Retomar o trabalho

1. Abra https://claude.ai/code.
2. Escolha o **mesmo repositório** e o **mesmo ambiente** da clínica.
3. Comece uma **nova sessão** (cada dia, uma sessão nova; não precisa reabrir a antiga).
4. Escreva `Vamos implantar <Nome da Clínica>` — ou só `continuar`.

**O que você vê:** em até 8 linhas, a IA diz **onde paramos**, **o que mudou**
desde a última vez (documentos novos, respostas, validade da chave) e faz a
**próxima pergunta** (uma só). Ela não "lembra" da conversa anterior: ela
**lê o caderno** (`ESTADO.md` e o resto do repositório). Por isso nada se perde
quando a conversa acaba.

Se ela disser que a chave vence em poucos dias: peça a renovação ao time Rabi
**agora** (Parte E).

### C2 — Ver o progresso sem a IA

1. Abra o repositório da clínica no GitHub.
2. Clique em **`ESTADO.md`**. Ali está o painel: clínica, sprint atual,
   próximo passo, tabela de todas as etapas (S00 a S17) com status e %.
3. Outros lugares úteis:
   - `historico/daily/` — o resumo de 5 linhas de cada dia de trabalho.
   - `historico/reviews/` — o fechamento de cada etapa, com o antes e depois.
   - `pendencias/LACUNAS.md` — o que ainda falta de informação.
   - `pendencias/PENDENCIAS.md` — o que depende de alguém (ex.: renovar a chave).

Se o `ESTADO.md` parecer atrasado, veja "trabalho sumiu" na [Parte E](04-problemas-e-seguranca.md).

### C3 — Quanto tempo leva

Tempo do guia oficial (https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#tempo-estimado),
**com os documentos completos no começo**:

| Porte | Característica | Tempo de implantação |
|---|---|---|
| Consultório individual | 1 profissional, 1 especialidade, particular ou 1 convênio | ~1 dia |
| Clínica pequena/média | 3 a 10 profissionais, várias especialidades e convênios, estoque | 1–2 semanas |
| Rede / multiunidade | várias unidades, muitos convênios, faturamento TISS centralizado | 3–6 semanas |

O prazo anda junto com os documentos e as respostas: quanto antes chegarem,
mais rápido termina. Convênio é a parte que mais pede atenção (preços,
pacotes, regras de materiais).

## Parte D — Outros modos (com frases prontas)

A IA trabalha de **quatro** jeitos. O modo muda com a frase que você escreve
no começo da sessão:

| Modo | Para quê | Escreva, por exemplo |
|---|---|---|
| **Implantação** | configurar a clínica do zero, etapa por etapa | `Vamos implantar Clínica Exemplo` · `continuar` · `continuar implantação` |
| **Atualização de configuração** | mudar algo já configurado (reajuste, serviço, profissional ou convênio novo, correção), medindo o impacto antes | `atualizar configuração: reajuste do Convênio A a partir de 01/11` |
| **Convênio** | configurar ou revisar **um** convênio (preços, pacotes, prazos), com conferência pelo Farol | `convênio: configurar Convênio B` |
| **Diagnóstico** | **só olhar e explicar**, sem gravar nada | `diagnóstico: por que o orçamento do serviço X saiu zerado?` |

Dicas:
- **Um assunto por sessão** funciona melhor. Terminou o reajuste? Sessão nova
  para o próximo assunto.
- Em **Atualização** e **Convênio**, a IA mostra o **impacto** (o que muda em
  orçamentos, guias e no Farol) antes da prévia.
- Em **Diagnóstico**, ela não grava nada; se achar um erro, propõe a correção
  e você decide se abre uma sessão de Atualização.
- Clínica grande, com muitos convênios ao mesmo tempo: veja
  [coordenação multi-sessão](../prompts/07-coordenacao-multi-sessao.md).

Próximo: [Partes E e F — Problemas e segurança](04-problemas-e-seguranca.md).
