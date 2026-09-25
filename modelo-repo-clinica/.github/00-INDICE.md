# .github · <NOME_DA_CLINICA>

> **Fonte:** kit implantarabi-ia (modelo-repo-clinica) · **Conferido em:** 2026-09-25
> **Vale para:** kit v0.1.0 · **Kit:** v0.1.0

| Arquivo | O que faz |
|---|---|
| `workflows/automerge.yml` | a cada push numa branch `claude/...` (a branch de cada sessão do Claude Code na web), leva o trabalho para a `main` em cerca de 1 minuto. Se a `main` não existir, cria. Em conflito, vale a versão da branch (trabalho mais recente). |

**Por que existe:** cada sessão na web trabalha numa branch `claude/...`; a
sessão seguinte abre na branch padrão (`main`). Sem o automerge, a próxima
sessão não veria o `ESTADO.md` atualizado.

**Se não funcionar:** em *Settings → Actions → General → Workflow permissions*
do repo, marque **Read and write permissions**. Se o push do arquivo do
workflow for recusado (algumas contas pedem permissão extra para
`.github/workflows/`), o dono cria o arquivo pela página do GitHub (*Add file →
Create new file*, caminho `.github/workflows/automerge.yml`) colando o conteúdo
de `.kit/modelo-repo-clinica/.github/workflows/automerge.yml`.
