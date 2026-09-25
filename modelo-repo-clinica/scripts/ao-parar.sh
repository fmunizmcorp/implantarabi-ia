#!/usr/bin/env bash
# Stop: impede encerrar a resposta com trabalho fora do GitHub.
# Lê o JSON do hook no stdin. Se há mudança sem commit ou commit sem push,
# devolve {"decision":"block","reason":...} (a sessão continua e faz o push).
# stop_hook_active=true (já bloqueou uma vez nesta volta) -> não bloqueia de novo.
# Ignora .kit/. Nunca falha a sessão (sempre exit 0). Nunca imprime segredo.
set -uo pipefail
ENTRADA="$(cat 2>/dev/null || true)"
ATIVO="$(printf '%s' "$ENTRADA" | python3 -c 'import sys,json
try:
    print("sim" if json.load(sys.stdin).get("stop_hook_active") is True else "nao")
except Exception:
    print("nao")' 2>/dev/null || echo nao)"
[ "$ATIVO" = "sim" ] && exit 0

RAIZ="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
cd "$RAIZ" 2>/dev/null || exit 0
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

SUJOS="$(git status --porcelain 2>/dev/null | grep -vE '^.. "?\.kit(/|$)' || true)"
NAO_ENVIADOS=""
if git rev-parse --abbrev-ref --symbolic-full-name '@{u}' >/dev/null 2>&1; then
  NAO_ENVIADOS="$(git log --oneline '@{u}..' 2>/dev/null || true)"
elif git rev-parse HEAD >/dev/null 2>&1 && git remote get-url origin >/dev/null 2>&1; then
  # branch nova sem upstream: tudo o que ainda não está em nenhum remoto
  NAO_ENVIADOS="$(git log --oneline HEAD --not --remotes 2>/dev/null || true)"
fi

[ -z "$SUJOS" ] && [ -z "$NAO_ENVIADOS" ] && exit 0

SUJOS="$SUJOS" NAO_ENVIADOS="$NAO_ENVIADOS" python3 - <<'PY'
import json, os
sujos = [l[3:] for l in os.environ.get("SUJOS", "").splitlines() if l.strip()]
nao = [l for l in os.environ.get("NAO_ENVIADOS", "").splitlines() if l.strip()]
partes = []
if sujos:
    lista = ", ".join(sujos[:5]) + (f" e mais {len(sujos) - 5}" if len(sujos) > 5 else "")
    partes.append(f"{len(sujos)} arquivo(s) sem commit ({lista})")
if nao:
    partes.append(f"{len(nao)} commit(s) sem push")
print(json.dumps({
    "decision": "block",
    "reason": "Há mudanças sem commit/push: " + "; ".join(partes)
              + ". Faça commit+push e atualize o ESTADO.md antes de encerrar.",
}, ensure_ascii=False))
PY
exit 0
