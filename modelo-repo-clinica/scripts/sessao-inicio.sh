#!/usr/bin/env bash
# SessionStart do repo da clínica: baixa/atualiza o kit em .kit/ e mostra o painel.
# Nunca falha a sessão (sempre exit 0). Nunca imprime segredo.
set -uo pipefail
RAIZ="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
cd "$RAIZ" 2>/dev/null || exit 0

KIT_URL="${KIT_URL:-https://github.com/fmunizmcorp/implantarabi-ia}"
KIT_REF="${KIT_REF:-}"   # opcional: branch/tag do kit

echo "== Implantação Rabi · sessão da clínica (SessionStart) =="

# 1) Kit em .kit/ (somente leitura)
if [ -d .kit/.git ]; then
  if git -C .kit pull --ff-only --quiet >/dev/null 2>&1; then
    echo "Kit: atualizado (.kit/)"
  else
    echo "Kit: NÃO consegui atualizar agora; usando a cópia que já está em .kit/ (pode estar desatualizada)."
  fi
elif [ -f .kit/BOOTSTRAP.md ]; then
  echo "Kit: usando cópia manual em .kit/ (sem git; não atualiza sozinha)."
else
  if [ -n "$KIT_REF" ]; then ARGS=(--depth 1 --branch "$KIT_REF"); else ARGS=(--depth 1); fi
  if git clone "${ARGS[@]}" --quiet "$KIT_URL" .kit >/dev/null 2>&1; then
    echo "Kit: baixado agora em .kit/ -> LEIA .kit/BOOTSTRAP.md e .kit/conhecimento/00-ESSENCIAL.md antes de agir."
  else
    echo "Kit: FALHOU o download de $KIT_URL"
    echo "  O que fazer (diga isto ao usuário, em português simples):"
    echo "  - Se o kit é PRIVADO: o dono do kit (Rabi) precisa dar acesso de leitura à conta GitHub"
    echo "    ligada a esta sessão; ou peça uma cópia do kit e coloque-a na pasta .kit/ deste repo."
    echo "  - Se foi rede: tente de novo em alguns minutos (feche e reabra a sessão)."
    echo "  - Sem o kit NÃO grave nada no Rabi. Pode só organizar documentos e conversar."
  fi
fi
if [ -f .kit/VERSION ]; then echo "Versão do kit: $(cat .kit/VERSION)"; fi

# 2) Repo privado? (heurística: a API pública do GitHub só enxerga repo público)
REMOTO="$(git remote get-url origin 2>/dev/null || true)"
if [ -n "$REMOTO" ]; then
  DONO_REPO="$(echo "$REMOTO" | sed -E 's#\.git$##; s#^.*[/:]([^/]+/[^/]+)$#\1#')"
  if command -v curl >/dev/null 2>&1; then
    COD="$(curl -s -o /dev/null -m 5 -w '%{http_code}' "https://api.github.com/repos/$DONO_REPO" 2>/dev/null || echo 000)"
    case "$COD" in
      200) echo "!!! ATENÇÃO: o repo $DONO_REPO parece PÚBLICO. Ele guarda chave e senhas em texto claro."
           echo "!!! Avise o dono por escrito (.kit/prompts/06-mensagens-padrao.md) e NÃO faça push até ele tornar privado." ;;
      404) echo "Repo: $DONO_REPO não é visível publicamente (ok: privado)." ;;
      *)   echo "Repo: não consegui conferir a visibilidade de $DONO_REPO (código $COD). Confira na abertura." ;;
    esac
  fi
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

# 6) Agentes/skills do kit mudaram?
if [ -d .kit/modelo-repo-clinica/.claude ] && ! diff -rq .kit/modelo-repo-clinica/.claude/agents .claude/agents >/dev/null 2>&1; then
  echo "Aviso: os agentes do kit mudaram. Para atualizar: python3 .kit/ferramentas/kit/novo_repo_clinica.py --destino . --atualizar-claude"
fi

echo ">>> Apresente-se com .kit/prompts/01-abertura-sessao.md e pergunte o MODO. Uma pergunta por vez."
echo "== fim =="
exit 0
