#!/usr/bin/env bash
# SessionStart do repo da clínica: baixa/atualiza o kit em .kit/ e mostra o painel.
# Nunca falha a sessão (sempre exit 0). Nunca imprime segredo.
set -uo pipefail
RAIZ="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
cd "$RAIZ" 2>/dev/null || exit 0

KIT_URL="${KIT_URL:-https://github.com/fmunizmcorp/implantarabi-ia}"   # kit PÚBLICO
KIT_REF="${KIT_REF:-main}"   # branch/tag do kit
export GIT_TERMINAL_PROMPT=0  # nunca travar pedindo usuário/senha
TO=""; command -v timeout >/dev/null 2>&1 && TO="timeout 60"

echo "== Implantação Rabi · sessão da clínica (SessionStart) =="

# 1) Kit em .kit/ (somente leitura)
if [ -d .kit/.git ]; then
  if $TO git -C .kit pull --ff-only --quiet >/dev/null 2>&1; then
    echo "Kit: atualizado (.kit/)"
  else
    echo "Kit: NÃO consegui atualizar agora; usando a cópia que já está em .kit/ (pode estar desatualizada)."
  fi
elif [ -f .kit/BOOTSTRAP.md ]; then
  echo "Kit: usando cópia manual em .kit/ (sem git; não atualiza sozinha)."
else
  if $TO git clone --depth 1 --branch "$KIT_REF" --quiet "$KIT_URL" .kit >/dev/null 2>&1; then
    echo "Kit: baixado agora em .kit/ -> LEIA .kit/BOOTSTRAP.md e .kit/conhecimento/00-ESSENCIAL.md antes de agir."
  else
    rm -rf .kit 2>/dev/null
    echo "Kit: FALHOU o download de $KIT_URL (branch $KIT_REF)."
    echo "  Causa provável: sem internet no ambiente ou GitHub fora do ar (o kit é público)."
    echo "  O que fazer (diga isto ao usuário, em português simples):"
    echo "  - Tente de novo em alguns minutos (feche e abra uma nova sessão)."
    echo "  - Plano B (cópia manual): baixe o ZIP do kit em"
    echo "    $KIT_URL (botão Code > Download ZIP), descompacte e coloque o conteúdo"
    echo "    na pasta .kit/ deste repo (tem de existir .kit/BOOTSTRAP.md). Não versione .kit/."
    echo "  - Sem o kit NÃO grave nada no Rabi. Pode só organizar documentos e conversar."
  fi
fi
if [ -f .kit/VERSION ]; then echo "Versão do kit: $(cat .kit/VERSION)"; fi

# 2) Repo privado? Lê o campo "private" da API do GitHub (no Claude Code na web
#    o proxy devolve 200 também para o repo privado ligado à sessão; o código
#    HTTP sozinho NÃO prova nada).
REMOTO="$(git remote get-url origin 2>/dev/null || true)"
if [ -n "$REMOTO" ]; then
  DONO_REPO="$(echo "$REMOTO" | sed -E 's#\.git$##; s#^.*[/:]([^/]+/[^/]+)$#\1#')"
  PRIV="?"
  if command -v curl >/dev/null 2>&1 && command -v python3 >/dev/null 2>&1; then
    PRIV="$(curl -s -m 8 "https://api.github.com/repos/$DONO_REPO" 2>/dev/null \
      | python3 -c 'import sys,json
try:
    v=json.load(sys.stdin).get("private")
    print("true" if v is True else "false" if v is False else "?")
except Exception:
    print("?")' 2>/dev/null || echo "?")"
  fi
  case "$PRIV" in
    true)  echo "Repo: $DONO_REPO é privado: ok." ;;
    false) echo "!!! ATENÇÃO: o repo $DONO_REPO está PÚBLICO. Não grave credenciais (chave, senhas) nele."
           echo "!!! Peça ao dono para torná-lo privado (modelo em .kit/prompts/06-mensagens-padrao.md)." ;;
    *)     echo "Repo: não consegui conferir a visibilidade de $DONO_REPO — confirme com o dono que ele é PRIVADO antes de gravar credenciais." ;;
  esac
fi

# 2b) A main está em dia? (o workflow automerge leva a branch claude/... para a main)
if $TO git fetch --quiet origin main >/dev/null 2>&1; then
  echo "Último commit na main: $(git log -1 --format='%cd · %s' --date=format:'%d/%m/%Y %H:%M' origin/main 2>/dev/null)"
  echo "  Confira que o ESTADO.md desta sessão é o mais recente (git log origin/main -1 -- ESTADO.md)."
fi

# 3) Painel (ESTADO.md)
if [ -f ESTADO.md ]; then
  for campo in "Clínica" "Porte" "Modo atual" "Sprint atual" "Próximo passo concreto" "Última sessão"; do
    grep -m1 -F "**$campo:**" ESTADO.md 2>/dev/null | sed 's/^- //; s/\*\*//g'
  done
else
  echo "(ESTADO.md não existe — o repo foi gerado do modelo? Ver .kit/prompts/00-COMO-COMECAR.md)"
fi

# 4) Pendências abertas
if [ -f pendencias/PENDENCIAS.md ]; then
  N="$(grep -ci '| *aberta *|' pendencias/PENDENCIAS.md 2>/dev/null || true)"
  echo "Pendências abertas: ${N:-0} (pendencias/PENDENCIAS.md)"
fi
if [ -f pendencias/LACUNAS.md ]; then
  N="$(grep -ci '| *aberta *|' pendencias/LACUNAS.md 2>/dev/null || true)"
  echo "Lacunas de dados abertas: ${N:-0} (pendencias/LACUNAS.md)"
fi

# 5) Chave da API (sem imprimir o valor)
if [ -n "${RABI_API_KEY:-}" ]; then
  echo "Chave RABI_API_KEY: definida no ambiente (valor não exibido)."
elif grep -qE '^api_key: *rbk_' credenciais/rabi-api-externa.md 2>/dev/null; then
  echo "Chave RABI_API_KEY: não está no ambiente; há chave registrada em credenciais/rabi-api-externa.md."
else
  echo "Chave RABI_API_KEY: NÃO definida. Peça ao dono (modelo em .kit/prompts/01-abertura-sessao.md)."
fi

# 6) Agentes/skills/comandos do kit mudaram?
if [ -d .kit/modelo-repo-clinica/.claude ]; then
  MUDOU=""
  for pasta in agents skills commands; do
    if ! diff -rq ".kit/modelo-repo-clinica/.claude/$pasta" ".claude/$pasta" >/dev/null 2>&1; then MUDOU="$MUDOU $pasta"; fi
  done
  if [ -n "$MUDOU" ]; then
    echo "Aviso: o kit mudou em .claude/{${MUDOU# }}. Para atualizar: python3 .kit/ferramentas/kit/novo_repo_clinica.py --destino . --atualizar-claude"
  fi
fi

echo ">>> Apresente-se com .kit/prompts/01-abertura-sessao.md e pergunte o MODO. Uma pergunta por vez."
echo "== fim =="
exit 0
