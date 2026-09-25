#!/usr/bin/env bash
# Stop: aviso (NÃO bloqueia). Mudança sem commit? ESTADO.md sem atualização hoje?
set -uo pipefail
RAIZ="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
cd "$RAIZ" 2>/dev/null || exit 0
SUJOS="$(git status --porcelain 2>/dev/null | grep -v '^?? \.kit' | wc -l | tr -d ' ')"
HOJE="$(TZ=America/Sao_Paulo date +%Y-%m-%d)"
AVISOS=""
if [ "${SUJOS:-0}" != "0" ]; then
  AVISOS="${AVISOS}- Há ${SUJOS} arquivo(s) sem commit. Faça commit + push (nada fica só no container).\n"
fi
if [ -f ESTADO.md ] && ! grep -q "$HOJE" ESTADO.md; then
  AVISOS="${AVISOS}- ESTADO.md não foi atualizado hoje ($HOJE). Atualize o próximo passo concreto e a última sessão.\n"
fi
if [ -n "$AVISOS" ]; then
  echo "== Aviso ao parar (não bloqueia) =="
  printf "%b" "$AVISOS"
fi
exit 0
