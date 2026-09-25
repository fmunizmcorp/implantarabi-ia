#!/usr/bin/env bash
# SessionStart do KIT (sessão do mantenedor). Só lê e imprime; nunca falha a sessão.
set -uo pipefail
RAIZ="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
cd "$RAIZ" 2>/dev/null || exit 0

echo "== KIT implantarabi-ia (SessionStart) =="
echo "Versão do kit: $(cat VERSION 2>/dev/null || echo '?')"
echo ">>> Leia BOOTSTRAP.md e metodologia/politicas.md antes de alterar o kit."
echo ">>> O kit NÃO guarda dado de clínica nem credencial. Sessão de clínica aqui? Não altere nada: MANUAL-PASSO-A-PASSO.md (resumo: prompts/00-COMO-COMECAR.md)"
echo
echo "--- Índice-mestre (INDICE.md, primeiras linhas) ---"
if [ -f INDICE.md ]; then head -n 30 INDICE.md; else echo "(INDICE.md ainda não existe)"; fi
echo
echo "--- Próximo passo (historico/HISTORICO.md) ---"
if [ -f historico/HISTORICO.md ]; then
  grep -i -m3 -A1 "próximo passo" historico/HISTORICO.md || echo "(sem 'Próximo passo' registrado)"
else
  echo "(historico/HISTORICO.md ainda não existe)"
fi
echo
echo "--- Verificações (rode antes de dizer 'pronto') ---"
echo "python3 -m pytest ferramentas -q"
echo "python3 ferramentas/kit/verificar_tamanhos.py && python3 ferramentas/kit/verificar_links.py && python3 ferramentas/kit/verificar_vazamento.py"
echo "== fim =="
exit 0
