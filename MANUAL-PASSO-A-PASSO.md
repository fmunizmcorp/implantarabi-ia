# Manual passo a passo — implantar o Sistema Rabi com a IA

> **Fonte:** este kit + guia oficial https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html + documentação do Claude Code na web https://code.claude.com/docs/en/claude-code-on-the-web · **Conferido em:** 2026-09-25
> **Vale para:** produção em 25/09/2026 (repositório-modelo por "Use this template") · **Kit:** v0.1.2

Este manual é para **quem vai implantar** o Sistema Rabi numa clínica: o dono,
alguém da equipe ou um parceiro. **Não precisa saber programar.** Você vai
clicar em algumas telas uma vez só (uns 15 minutos) e, depois disso, o trabalho
de cada dia é abrir uma conversa e responder às perguntas da IA.

## As partes do manual

| Parte | O que tem | Quando ler |
|---|---|---|
| **0** (abaixo) | o que é cada peça e quem faz o quê | antes de tudo |
| [A — Preparação](manual/01-preparacao.md) | contas, chave da API, repositório da clínica, ambiente do Claude (clique a clique) | uma vez por clínica (~15 min) |
| [B — Primeira sessão](manual/02-primeira-sessao.md) | a frase `Vamos implantar <Nome da Clínica>`, documentos, como responder e aprovar | no primeiro dia |
| [C e D — Dia a dia e outros modos](manual/03-dia-a-dia-e-modos.md) | como retomar, ver o progresso, quanto tempo leva; atualização, convênio, diagnóstico | todos os dias |
| [E e F — Problemas e segurança](manual/04-problemas-e-seguranca.md) | sintoma → o que fazer; LGPD e cuidados com a chave | quando algo não sair como esperado |
| [G — Checklist para imprimir](manual/05-checklist-imprimir.md) | 1 página: preparação + cada sessão | deixe ao lado do computador |
| [H — Para o mantenedor (Rabi)](manual/06-mantenedor.md) | publicar e atualizar o repositório-modelo | só a equipe Rabi |

Índice da pasta: [manual/00-INDICE.md](manual/00-INDICE.md).

---

## Parte 0 — O que é cada peça

São **quatro** peças. Você só mexe diretamente em duas (o repositório da
clínica, para ver o progresso, e a conversa com o Claude).

```
  KIT (público, da Rabi)                    REPOSITÓRIO DA CLÍNICA (PRIVADO)
  github.com/fmunizmcorp/implantarabi-ia     github.com/<conta-da-clínica>/rabi-implantacao-<clínica>
  ┌────────────────────────────────┐        ┌───────────────────────────────────────┐
  │ o "livro de receitas":         │ baixado│ o "caderno" desta clínica:            │
  │ como o Rabi funciona, a API,   │ sozinho│ ESTADO.md (onde paramos), documentos, │
  │ preços e convênios, o passo a  │ ──────►│ dados, provas de cada gravação,       │
  │ passo de cada etapa            │ (.kit/)│ credenciais, histórico                │
  └────────────────────────────────┘        └──────────────────┬────────────────────┘
                                                               │ lê e escreve
  REPOSITÓRIO-MODELO (público)                                  ▼
  implantarabi-modelo-clinica  ── "Use this template" ──►  CLAUDE (IA) no Claude Code na web
  (o formulário em branco que vira o caderno)               conversa com você, uma pergunta por vez
                                                               │ chave da API (rbk_…) da clínica
                                                               ▼
                                                        SISTEMA RABI da clínica
                                                        (onde os cadastros ficam de verdade)
```

- **Kit** — o conhecimento. É público e igual para todas as clínicas. Nunca
  guarda dado de clínica. A IA baixa o kit sozinha no começo de cada conversa.
- **Repositório da clínica** — o caderno de trabalho **desta** clínica. É
  **privado** (só quem você convidar vê). Guarda tudo: onde paramos, os
  documentos que você mandou, o que foi gravado, as senhas iniciais.
- **Claude (a IA)** — faz o trabalho técnico: lê documentos, monta os
  cadastros, grava no Rabi, confere e registra. Sempre mostra antes e pede sua
  aprovação para gravar.
- **Sistema Rabi** — o sistema da clínica. A IA fala com ele pela **API
  externa** (um "canal oficial" de computador para computador), usando a
  **chave da API** da clínica (um código que começa com `rbk_`).

### Quem faz o quê

| Papel | Quem é | O que faz |
|---|---|---|
| **Mantenedor** | equipe Rabi | cuida do kit e do repositório-modelo (Parte H) |
| **Dono da clínica** | a clínica | tem as contas (GitHub, Claude), recebe a chave da API, decide regras de negócio |
| **Implantador** | alguém da clínica, um parceiro ou a Rabi | abre as conversas, manda documentos, responde, aprova e confere |
| **IA implantadora** | o Claude, na conversa | todo o trabalho técnico, sempre com prévia e aprovação |

O implantador faz **só três coisas**: (1) entrega documentos e informações;
(2) aprova o que a IA mostra antes de gravar; (3) confere o que ela mostra depois.

## O caminho inteiro em 6 linhas

1. Contas: GitHub e Claude com Claude Code na web (A1).
2. Pedir a chave da API ao time Rabi (A2).
3. Criar o repositório **privado** da clínica pelo modelo (A3) e liberar a gravação automática (A4).
4. Ligar o GitHub ao Claude (A5) e criar o **ambiente da clínica** com a chave (A6).
5. Abrir uma sessão e escrever: `Vamos implantar <Nome da Clínica>` (Parte B).
6. Nos outros dias: nova sessão, mesma frase (ou "continuar") (Parte C).

Começar: [Parte A — Preparação](manual/01-preparacao.md).
