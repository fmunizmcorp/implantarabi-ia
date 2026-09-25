#!/usr/bin/env bash
# PreCompact: lembra o que tem de sobreviver ao resumo. Nunca falha.
set -uo pipefail
RAIZ="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
cd "$RAIZ" 2>/dev/null || exit 0
echo "== PreCompact (clínica): preserve OBRIGATORIAMENTE no resumo =="
echo "- Modo atual, sprint atual e o que está AGUARDANDO APROVAÇÃO (prévia mostrada e não aprovada)."
echo "- Arquivos modificados nesta sessão:"
git status --porcelain 2>/dev/null | head -30 | sed 's/^/    /'
echo "- Última prova gravada:"
ls -1td provas/S*/*/* 2>/dev/null | head -3 | sed 's/^/    /'
grep -m1 -F "**Próximo passo concreto:**" ESTADO.md 2>/dev/null | sed 's/^/- /'
echo "Depois de compactar: releia ESTADO.md e a sprint atual. A verdade está nos arquivos."
exit 0
