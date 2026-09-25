# ferramentas/implantacao — automações do dia a dia da sessão implantadora

| Arquivo | O que faz | Quando usar |
|---|---|---|
| `painel.py` | Regenera o painel de progresso do `ESTADO.md` (barra e % por sprint, bloqueios) a partir de `sprints/Sxx*.md` | ao fim de todo passo, antes do commit |
| `fila_perguntas.py` | Diz a PRÓXIMA ação da sprint (CONFIRMAR / SUGERIR PADRÃO / PEDIR / GRAVAR / CONFERIR), uma por vez | sempre que for falar com o usuário |
| `carga.py` | Ritual de 5 passos genérico para cadastros: `previa` (foto antes + casamento com o que existe + prévia legível, sem gravar) e `gravar` (só o plano aprovado; bulk em fatias; alteração = GET→merge→PUT completo; resposta crua, foto depois e diff) | S01–S09, S12–S13 |
| `importar_planilha.py` | Planilha/CSV do cliente ou de sistema anterior → CSV normalizado com coluna `origem` (sugere o mapa de colunas; valida CPF/CNPJ/CEP/telefone/datas/valores; marca duplicados) | ingestão de listas (profissionais, produtos, serviços, pacientes…) |
| `checklist.py` | Biblioteca: lê as tabelas de checklist das sprints | usada pelos outros |
| `tests/` | testes (pytest) | CI |

Convênios (abas de preço) NÃO usam `carga.py`: use `../conversao/montar_convenio.py` (+ simulador e conferir_farol).
Financeiro, estoque e NFS-e nunca usam `carga.py` — exigem ordem escrita (ver `../../conhecimento/api-externa/proibidas-sem-ordem-escrita.md`).
