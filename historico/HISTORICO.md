# HISTÓRICO do kit

| Data | Versão | O que foi feito | Próximo passo |
|---|---|---|---|
| 2026-09-25 | 0.1.0 | Criação do kit a partir da experiência de implantação real, do manual oficial v2.3 e do Swagger de 25/09 (plano: `PLANO-2026-09-25.md`). | Primeira implantação-piloto com uma clínica usando o modelo; recolher lições para v0.2. |
| 2026-09-25 | 0.1.1 | Validação cruzada (19) + simulação de clínica (10) corrigidas; kit publicado na `main` e tornado público. | Piloto com a primeira clínica; reconfirmar 401×503 e os campos do Farol com chave real. |
| 2026-09-25 | 0.1.1 | Kit tornado **público** e `main` definida como branch padrão pelo Diretor (conferido: clone anônimo ok). | Piloto com a primeira clínica. |
| 2026-09-25 | 0.1.2 | Formatos reais da API confirmados com chave válida (só leitura) e incorporados ao kit; 503 reconfirmado. | Piloto; confirmar em homologação `fonte_id` = `fontePrecoCompraOptionsId` e a receita de item fora da conta. |
| 2026-09-25 | 0.2.0 | Manual passo a passo, frase 'Vamos implantar <clínica>' e ferramentas do repo-modelo. | Diretor cria o repo-modelo vazio; sessão do kit exporta o conteúdo; piloto com a 1ª clínica. |

## 2026-09-25 — v0.2.1 — passo a passo público no manual do Rabi + repo-modelo populado
- Página pública: https://www.rabisistemas.com.br/manual/implantacao/implantacao-com-ia.html (manualrabi D-34; 200 em produção).
- Kit aponta para ela (README, MANUAL-PASSO-A-PASSO, manual/07, README do modelo, README do repo-modelo).
- Repo-modelo `fmunizmcorp/implantarabi-modelo-clinica` populado por `exportar_modelo.py` (92 arquivos; `--checar` PASS).
- Próximo passo: piloto com a primeira clínica real ("Vamos implantar <Nome da Clínica>").

## 2026-09-28 — v0.3.0 — canal de aprendizados + novidades do kit + FAQ das IAs
- Canal clínica → kit (fila `contribuicoes-kit/`, filtro de privacidade, formulário de issue pública, caixa de entrada + workflow `aprendizados.yml`, consolidação `prompts/09`).
- Novidades kit → clínica (`atualizar_repo_clinica.py` + bloco NOVIDADES DO KIT no hook + "Ação nas clínicas" no CHANGELOG).
- Validação cruzada (25 achados) corrigida antes do commit (filtro, atualizador, hook, workflow, textos).
- FAQ das IAs (`conhecimento/faq-ias/`, `buscar_faq.py`, dica no erro do `cliente.py`) a partir do 1º caso real: POST /servicos 500 `reading 'filter'` (confirmado no código do Rabi) e 400 genérico na área inteira desde o deploy do Rabi de 28/09 14:08 (hipótese: migração não aplicada no banco da clínica — aguardando suporte).
- Próximo passo: resposta do suporte do Rabi ao caso F002; atualizar o status da F002.

## 2026-09-28 — v0.3.1 — F002 resolvida pelo Rabi
- Suporte do Rabi corrigiu o ambiente da 1ª clínica (sem mudança de código; conferido no deploy de 28/09 19:28 UTC). F001 segue aberta (contorno: 4 listas). Próximo passo: a clínica retoma a S08 com 1 serviço primeiro.

## 2026-09-28 — v0.3.2 — correção geral da API externa pelo Rabi
- Commit `c73e84de` (produção 17:43 BRT) corrigiu o 500 do cadastro de serviço (F001) e ~20 outros defeitos de campo omitido/gravação errada. Kit: F001 corrigida, F006 (conferência retroativa), defeitos e convenções atualizados, Swagger 28/09, `corpo_escrita.py` com `servicoTaxa` e quantidades.

## 2026-11-05 — v0.3.3 — token `rbt_` da clínica como caminho recomendado
- Decisão do Diretor (30/09/2026): o kit recomenda o token `rbt_` gerado pela clínica (Configurações › Parâmetros › Integrações, tipo "Implantação e manutenção"; editável; botão Renovar); `rbk_` do time Rabi segue como alternativa.
- `cliente.py` aceita os dois prefixos; detector de vazamento e filtro de aprendizado passaram a pegar `rbt_` (fecha o furo de segurança); testes novos; docs (S00, ESSENCIAL §6, chave-e-token, manual, prompts, modelo) atualizados.
- Próximo passo: republicar o repo-modelo (`exportar_modelo.py`) e, na 1ª clínica, conferir com um `rbt_` real (`testar_chave.py`, só leitura) o cabeçalho `X-ApiKey-Expires-At` e as 25 áreas; registrar o resultado no chave-e-token.

## 2026-11-22 — v0.4.0 — novidades do Rabi 29/09→22/11 + Swagger 22/11 + lições do NotaPlano
- Pedido do Diretor (raw maestro 2026-11-22b). Fontes: Swagger 22/11 (277 ops), código `deploy_prd` (agente de pesquisa + conferência do mantenedor no `updateConvenioController.ts`), manual D-37…D-54, base `conhecimento/` do Maestro, medição de chave (401).
- PUT parcial no kit inteiro + `corpo_parcial` no código; FAQ F007–F011; novidades do sistema; lições do NotaPlano; validação cruzada independente (2 ALTO + 10 MÉDIO corrigidos antes da publicação).
- Aviso ao manual (`manualrabi/entrada/atualizacao-2026-11-22-api-externa-limites-e-codigos.md`): limite por token, textos de 401, 409 ITEM_EM_USO, `version`, PUT do convênio parcial no código (pendência C11).
- Próximo passo: na 1ª clínica, aplicar a estrutura nova, fazer a conferência F006 ampliada e medir, num PUT real de serviço com só um campo, que o resto ficou intacto (prova antes/depois).
- Repositório-modelo republicado pela sessão do kit (`implantarabi-modelo-clinica` `e2c4450`, kit 0.4.0; `exportar_modelo.py --checar` PASS; `verificar_vazamento` PASS). O workflow `publicar-modelo` não publica sozinho: falta o secret `MODELO_PUSH_TOKEN`.
