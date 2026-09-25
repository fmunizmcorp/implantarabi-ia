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

# 0) RESUMO DE RETOMADA (máx. ~10 linhas; nunca imprime segredo)
#    O marcador do nome é montado em duas partes para a personalização não trocá-lo aqui.
MARCA_NOME="<NOME_DA""_CLINICA>"
campo() { grep -m1 -F "**$1:**" ESTADO.md 2>/dev/null | sed 's/^- //; s/\*\*[^*]*:\*\* *//'; }
echo "== RESUMO DE RETOMADA =="
if [ ! -f ESTADO.md ]; then
  echo "Clínica: (ESTADO.md não existe — este repo não veio do modelo?)"
elif grep -qF "$MARCA_NOME" ESTADO.md 2>/dev/null; then
  echo "Clínica: ainda não personalizado — primeira vez (o usuário diz: Vamos implantar <nome da clínica>)"
else
  echo "Clínica: $(campo 'Clínica')"
fi
if [ -f ESTADO.md ]; then
  echo "Modo: $(campo 'Modo atual') · Sprint atual: $(campo 'Sprint atual')"
  echo "Próximo passo: $(campo 'Próximo passo concreto')"
fi
N_LAC=0
[ -f pendencias/LACUNAS.md ] && N_LAC="$(grep -ciE '\|[[:space:]]*(aberta|aberto|pendente)[[:space:]]*\|[[:space:]]*$' pendencias/LACUNAS.md 2>/dev/null || true)"
echo "Lacunas abertas: ${N_LAC:-0} (pendencias/LACUNAS.md)"
ULT_DAILY="$(ls -1 historico/daily/*.md 2>/dev/null | grep -v '/00-INDICE\.md$' | sort | tail -n 1)"
echo "Última daily: ${ULT_DAILY:-nenhuma ainda}"
if [ -d documentos-do-cliente ]; then
  NOVOS=""; N_NOVOS=0
  while IFS= read -r -d '' ARQ; do
    BASE="$(basename "$ARQ")"
    if ! grep -qF -- "$BASE" documentos-do-cliente/inventario.md 2>/dev/null; then
      N_NOVOS=$((N_NOVOS + 1)); [ "$N_NOVOS" -le 3 ] && NOVOS="$NOVOS; ${ARQ#documentos-do-cliente/}"
    fi
  done < <(find documentos-do-cliente -type f ! -name '00-INDICE.md' ! -name 'inventario.md' \
             ! -name 'README.md' ! -name '.gitkeep' ! -path '*/fichas-de-extracao/*' -print0 2>/dev/null)
  if [ "$N_NOVOS" -gt 0 ]; then
    echo "Documentos novos (fora do inventário): $N_NOVOS → ${NOVOS#; }$([ "$N_NOVOS" -gt 3 ] && echo ' …')"
  else
    echo "Documentos novos (fora do inventário): 0"
  fi
fi
VALIDADE="$(grep -iE 'validade|expires' credenciais/rabi-api-externa.md 2>/dev/null \
  | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -n 1)"
if [ -n "$VALIDADE" ] && command -v python3 >/dev/null 2>&1; then
  DIAS="$(python3 -c 'import sys,datetime as d
try:
    from zoneinfo import ZoneInfo; h=d.datetime.now(ZoneInfo("America/Sao_Paulo")).date()
except Exception:
    h=d.date.today()
print((d.date.fromisoformat(sys.argv[1])-h).days)' "$VALIDADE" 2>/dev/null || echo "?")"
  echo "Validade da chave (registrada): $VALIDADE (faltam $DIAS dias; renovar com o time Rabi antes de vencer)"
else
  echo "Validade da chave: sem data registrada em credenciais/rabi-api-externa.md"
fi
if [ -n "${RABI_API_KEY:-}" ]; then echo "RABI_API_KEY: definida (valor não exibido)"; else echo "RABI_API_KEY: NÃO definida no ambiente"; fi
echo "== fim do resumo =="

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

# 3) Painel (ESTADO.md) — o resto já saiu no resumo de retomada
if [ -f ESTADO.md ]; then
  for campo in "Porte" "Bloqueios" "Última sessão"; do
    grep -m1 -F "**$campo:**" ESTADO.md 2>/dev/null | sed 's/^- //; s/\*\*//g'
  done
else
  echo "(ESTADO.md não existe — o repo foi gerado do modelo? Ver .kit/MANUAL-PASSO-A-PASSO.md)"
fi

# 4) Pendências abertas
if [ -f pendencias/PENDENCIAS.md ]; then
  N="$(grep -ci '| *aberta *|' pendencias/PENDENCIAS.md 2>/dev/null || true)"
  echo "Pendências abertas: ${N:-0} (pendencias/PENDENCIAS.md)"
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

echo ">>> Siga as FRASES DE DISPARO do CLAUDE.md (primeira vez × retomada). Abertura: .kit/prompts/01-abertura-sessao.md. Uma pergunta por vez."
echo "== fim =="
exit 0
