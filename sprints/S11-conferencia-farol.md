# S11 — Conferência pelo Farol

> **Fonte:** https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-11 · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-11 · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#ler-farol-itens · https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#como-conferir · spec `openapi-2026-09-25.json` (`GET /convenios/{id}/farol/itens|servicos|produtos`, `GET|PUT /parametros/orcamento`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Farol › Itens e farol consolidado em produção desde set/2026) · **Kit:** v0.1.0

## Objetivo

Cada convênio foi conferido pelo Farol: nenhum item 🟣 roxo sem causa, cada
🔴 vermelho explicado, e o que o simulador previu bate com o que o Rabi calcula.
A régua do Farol (limites vermelho/amarelo) foi ajustada **antes** da leitura.

## Link do manual

- Etapa 11: https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-11
- Farol pela API: https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-11
- Como ler cada linha: https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#ler-farol-itens
- Farol consolidado: https://www.rabisistemas.com.br/manual/precos/index.html#farol-consolidado
- Kit: [08-farol](../conhecimento/precos-e-conversao/08-farol.md) · [13-conferencia-e-diagnostico](../conhecimento/precos-e-conversao/13-conferencia-e-diagnostico.md)

## Depende de

S10 (convênios com abas preenchidas). Custos de produto vêm das entradas de
estoque (S12): **roxo por falta de custo** é esperado antes da S12 e é
reconferido depois dela.

## Documentos a pedir

DI-6 (margem mínima que a clínica aceita). CV-2/CV-3 para investigar vermelhos.

## Índice de dados a coletar

| dado | campo API | obrigatório? | onde costuma estar no material do cliente | padrão sugerível | pergunta ao usuário se faltar |
|---|---|---|---|---|---|
| Limite vermelho (%) | `parametroVermelho` (`/parametros/orcamento`) | sim para o Farol | política comercial, DI-6 | **100** (padrão do sistema) | "Abaixo de qual margem a clínica quer bloquear um orçamento? O sistema vem com 100% (receita igual ao custo)." |
| Limite amarelo (%) | `parametroAmarelo` | sim | idem | **120** | "E a partir de qual margem está tudo bem? O padrão é 120%." |
| Aprovação nível 2 no amarelo | `requerAutorizacaoNivel2Amarelo` | não | regra interna | — | "Orçamento em amarelo precisa de aprovação de alguém?" |
| Aprovação nível 3 no vermelho / roxo | `requerAutorizacaoNivel3Vermelho`, `requerAutorizacaoNivel3Roxo` | não | regra interna | — | — |
| Desligar bloqueio do Farol | `desabilitarBloqueioFarol` | não | — | **não** (só com decisão escrita) | — |
| Causa de cada vermelho/roxo | — | sim | análise da IA | — | pergunta só quando a causa depende de decisão |

Margem do Rabi = receita ÷ custo × 100, comparada aos limites. 🟢 verde >
limite amarelo; 🟡 amarelo entre os limites; 🔴 vermelho ≤ limite vermelho
(bloqueia); 🟣 roxo = item sem custo ou sem preço (sempre bloqueia; é
**cadastro incompleto**, não margem ruim).

## Fila de perguntas

1. Régua: confirmar ou ajustar os limites (padrão 100/120).
2. Aprovações por cor (se a clínica quiser alçada).
3. Para cada vermelho cuja causa é **preço abaixo do custo no contrato**:
   "O <convênio> paga R$ X pelo <serviço>, e só o medicamento custa R$ Y.
   Aceitar assim, renegociar ou não atender por esse convênio?" (uma por vez).

## Enriquecimento possível

- `ferramentas/conversao/conferir_farol.py`: compara o previsto pelo simulador
  com `/farol/itens` e `/farol/servicos` e lista as divergências.
- Relatório por convênio: vermelhos e roxos com o motivo provável.

## Leitura do que já existe no Rabi e regra de não perder nada

- `GET /parametros/orcamento` antes de qualquer PUT. Sem configuração salva, a
  resposta é o número `0` cru (não é erro).
- Farol (sempre com os dois filtros de "ativo", e todas as páginas):
  - `GET /convenios/{id}/farol/servicos?servicoAtivo=true&ativoNoConvenio=true` —
    uma linha por serviço: `custo_total`, `receita_total`, `receita_propria_servico`,
    `margem_resultado_pct`, `farol`;
  - `GET /convenios/{id}/farol/itens?apenasAtivosNoConvenio=true&servicoAtivo=true`
    (e `servicoRaizId=<id>` para um serviço) — a árvore item a item: `servico_raiz_id`,
    `item_tipo`, `item_id`, `item_nome`, `custo`, `receita`, `farol`, `utiliza`;
  - `GET /convenios/{id}/farol/produtos?ativoNoConvenio=true&produtoAtivo=true`.
- O Farol também lista serviços **desativados** no catálogo: sem os filtros, a
  contagem erra.

## Gravação

| Ordem | Rota | Permissão | Lote |
|---|---|---|---|
| 1 | `GET /parametros/orcamento` → alterar só a régua aprovada → `PUT /parametros/orcamento` com **o objeto completo** | `parametro:update` | — |
| 2 | Leitura do Farol de cada convênio | `convenio:read` | — |
| 3 | Correções que o Farol revelar → voltam para a sprint da área (S06, S08, S10b) com o ritual | — | — |

- No PUT de orçamento, alguns nomes de escrita diferem da leitura (ex.: a
  resposta mostra `diasValidos`, o corpo usa `diasVencimento`) — detalhes em
  [08-farol](../conhecimento/precos-e-conversao/08-farol.md).
- A S11 **não corrige preço por conta própria**: cada correção é uma proposta,
  aprovada e gravada na sprint de origem.

## Prova

- `provas/S11/<slug>/farol-servicos.json`, `farol-itens.json`, `farol-produtos.json`
  + `relatorio.md` por convênio:
  - quantos serviços por cor;
  - **cada vermelho e roxo** com o motivo (item sem Utiliza que deveria cobrar;
    item zerado sem pacote; 0 gravado onde devia estar vazio; preço de contrato
    abaixo do custo; produto sem custo ainda; política ausente);
  - os 3 serviços conferidos na S10b (previsto × Farol).
- Na tela, o implantador pode abrir Configurações → Convênios → aba Farol › Itens
  e "Expandir serviço" para ver o mesmo.

## Armadilhas desta sprint

- Aceitar vermelho "em silêncio": vermelho é dinheiro perdido naquele serviço,
  naquele convênio — sempre investigado e decidido.
- Roxo logo após a implantação costuma ser **falta de custo** (as entradas de
  estoque vêm na S12): anote e reconfira depois.
- Item que deveria cobrar e aparece com receita 0: zerado dentro de pacote — ou
  0 gravado onde devia estar em branco.
- `utiliza: false` no Farol = custo sem receita: se o convênio paga o item, volte
  à S10b e marque Utiliza.
- Serviço ou taxa sem produto não vira roxo (custo zero é esperado).
- `desabilitarBloqueioFarol` desliga todo bloqueio em orçamento e autorização:
  só com decisão escrita.

## Definition of Ready / Definition of Done

**DoR:** S10b concluída para o convênio; régua definida (ou padrão aceito).

**DoD:**
- [ ] régua gravada e relida (ou padrão confirmado);
- [ ] relatório de Farol de **cada** convênio no repo;
- [ ] nenhum roxo sem causa anotada (roxo por falta de custo: pendência para depois da S12);
- [ ] todo vermelho explicado e decidido pelo dono (aceitar, corrigir, renegociar);
- [ ] previsto × Farol sem divergência aberta.

## Checklist de itens

| # | item | status | origem | prova | observação |
|---|---|---|---|---|---|
| S11-01 | Régua do Farol definida (limites e aprovações) | pendente | | | |
| S11-02 | Régua gravada e relida | pendente | | provas/S11/ | |
| S11-03 | Farol do Particular lido e relatado | pendente | | | |
| S11-04 | Farol do convênio <nome> lido e relatado (uma linha por convênio) | pendente | | | |
| S11-05 | Vermelhos decididos pelo dono | pendente | | | |
| S11-06 | Roxos com causa (e reconferência pós-S12 agendada) | pendente | | | |
| S11-07 | Previsto × Farol sem divergência | pendente | | | |

## O que registrar

- `dados/convenios/<slug>/farol.md` (resumo por data).
- `decisoes/DECISOES.md`: régua e cada vermelho aceito conscientemente.
- `pendencias/PENDENCIAS.md`: roxos a reconferir depois da S12.
- `ESTADO.md`: próximo passo = S12.
