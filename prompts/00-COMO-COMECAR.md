# Como começar — resumo de 1 tela

> **Fonte:** kit implantarabi-ia · **Conferido em:** 2026-09-25
> **Vale para:** kit v0.1.2 (repositório-modelo por "Use this template") · **Kit:** v0.1.2

O passo a passo completo, clique a clique, está no
**[MANUAL-PASSO-A-PASSO.md](../MANUAL-PASSO-A-PASSO.md)**. Este é só o resumo.

## Uma vez por clínica (~15 min) — [Parte A](../manual/01-preparacao.md)

1. **Contas:** GitHub (gratuito) e Claude com acesso ao Claude Code na web (https://claude.ai/code).
2. **Chave da API** (`rbk_…`): pedir ao time Rabi, com as permissões de
   implantação. Aparece uma vez só; vale ~7 dias — renovar antes de vencer.
3. **Repositório da clínica:** https://github.com/fmunizmcorp/implantarabi-modelo-clinica/generate
   → Owner = conta da clínica → nome `rabi-implantacao-<clinica>` → **Private** → *Create repository*.
   (Link não abre? Plano B na [Parte A, passo A3](../manual/01-preparacao.md#a3--criar-o-repositório-da-clínica-pelo-modelo).)
4. **Gravação automática:** *Settings → Actions → General → Workflow permissions → Read and write → Save*.
5. **GitHub no Claude:** https://claude.ai/connect-github e app Claude no repositório.
6. **Ambiente da clínica** no Claude Code (menu do ambiente → *Edit*):
   `RABI_API_KEY=rbk_…` e rede liberada para `api.rabisistemas.com.br`.
   **Nunca cole a chave no chat.**

## Toda sessão — [Partes B e C](../manual/02-primeira-sessao.md)

Abra https://claude.ai/code → repositório da clínica → ambiente da clínica →
nova sessão → escreva:

```
Vamos implantar <Nome da Clínica>
```

Na primeira vez a IA baixa o kit, personaliza o repositório, confere
privacidade e chave, fotografa o que já existe no Rabi, pede os documentos de
uma vez e mostra o plano. Nas outras, diz onde parou e faz a próxima pergunta
(também vale escrever só `continuar`).

Outros modos: `atualizar configuração: …` · `convênio: …` · `diagnóstico: …`
([Parte D](../manual/03-dia-a-dia-e-modos.md)).

## O seu papel
1. **Entregar** os documentos que a IA pedir (em qualquer formato).
2. **Aprovar** o que ela mostra antes de gravar ("pode gravar").
3. **Conferir** o resultado que ela mostra depois.

Problemas: [Parte E](../manual/04-problemas-e-seguranca.md) · Para imprimir: [Parte G](../manual/05-checklist-imprimir.md).
