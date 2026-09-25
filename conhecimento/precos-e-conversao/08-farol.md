# 08 — Farol de margem (item, serviço, consolidado) e alçada

> **Fonte:** https://www.rabisistemas.com.br/manual/precos/index.html#custo-e-farol · https://www.rabisistemas.com.br/manual/precos/arvore-de-decisao.html#arvore-farol · https://www.rabisistemas.com.br/manual/precos/guia-ia.html#alg-farol · https://www.rabisistemas.com.br/manual/precos/guia-ia.html#alg-farol-consolidado · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-11 · spec 25/09 (`/parametros/orcamento`, `/convenios/{id}/farol/*`) · leitura real (GET) da API de produção em 25/09/2026 · **Conferido em:** 2026-09-25
> **Vale para:** Farol consolidado em produção desde 23/09/2026; Farol › Itens por linha desde 24/09/2026 · **Kit:** v0.1.0

O Farol compara **quanto entra** com **quanto custa**:
`índice = receita ÷ custo × 100`. Ex.: 120 = receita 20% maior que o custo.
É a **prova** de que a conversão está certa: depois de configurar um
convênio, o Farol mostra onde a clínica perde dinheiro.

## 1. Cores e limiares

| Cor | Significado | Efeito |
|---|---|---|
| 🟢 Verde | margem saudável (índice > limite Amarelo) | passa |
| 🟡 Amarelo | atenção (entre os limites) | pode exigir aprovação **nível 2** |
| 🔴 Vermelho | crítica (índice ≤ limite Vermelho) | **bloqueia**; pode ser liberado por **nível 3**, se a clínica permitir |
| 🟣 Roxo | **erro de cadastro**: produto sem custo, ou receita/custo ausente com produto envolvido | **sempre bloqueia**; corrigir o cadastro |

- Limites: Configurações › Parâmetros › aba **Valores** ("Parâmetros de
  Margem do Orçamento"): **Parâmetro Vermelho (%)** e **Parâmetro Amarelo
  (%)**. Padrão **100 / 120**.
- Serviço ou taxa **sem nenhum produto** não vira roxo (custo zero é
  esperado) — fica sem farol de margem.
- Roxo **não é margem ruim**: é cadastro incompleto.

> **Fronteiras exatas (não confirmado).** O manual diz "≤ Vermelho →
> bloqueado" (e o caso T14 trata índice = 100 como bloqueado); a página da
> API diz "amarelo ≥ limite vermelho". Para o motor do kit: `índice ≤
> Vermelho → VERMELHO`; `Vermelho < índice ≤ Amarelo → AMARELO`; `índice >
> Amarelo → VERDE` (é o que `ferramentas/conversao/motor.py` faz). Confira um caso exatamente no limite em homologação.

### 1.1 Parâmetros pela API

`GET /parametros/orcamento` (`parametro:read`) · `PUT /parametros/orcamento`
(`parametro:update`). Campos: `parametroVermelho`, `parametroAmarelo`,
`requerAutorizacaoNivel2Amarelo`, `requerAutorizacaoNivel3Vermelho`,
`requerAutorizacaoNivel3Roxo`, `desabilitarBloqueioFarol`.
- Sem configuração salva, o GET devolve o número **`0`** cru (não objeto).
- Nomes do corpo divergem da resposta: envie `diasVencimento` (a resposta
  mostra `diasValidos`) e `consideracoes` (resposta: `consideracoesGerais`).
- Trate o PUT como sobrescrita: GET antes, reenvie tudo.
- `desabilitarBloqueioFarol` desliga **todo** bloqueio de Farol em Orçamento
  e Autorização — só com decisão escrita da clínica.
- Ajuste a régua **antes** da conferência pelo Farol (etapa de convênios); os
  demais parâmetros ficam para a etapa final (Parâmetros e Permissões).

## 2. Os quatro faróis e o escopo de cada um

| Farol | Receita | Custo | Onde aparece |
|---|---|---|---|
| **do produto** | valor convertido do produto (arquivo 04) | custo da aba Estoque | aba Produtos (bolinha); `/farol/produtos` |
| **da taxa** | só a taxa | 0 (sem farol de margem) | aba Taxas |
| **do serviço** | **total** do serviço (base + itens que entram) = linha Σ | Σ custo de **todos** os produtos da árvore, **inclusive os que ficaram fora** | aba Serviços (bolinha da ✅), Farol › Serviços, relatórios; `/farol/servicos` |
| **consolidado** | Σ receita de **todos** os serviços, produtos e taxas do pedido | Σ custo de **todos** os produtos envolvidos | orçamento, agendamento, autorização |

```
FAROL CONSOLIDADO (orçamento, agendamento, autorização) — desde 23/09/2026
  receita = Σ receita(item, C) de TODOS os serviços, produtos e taxas do pedido
            (só itens com Utiliza geram receita; item sem Utiliza: receita 0, custo CONTA)
  custo   = Σ custo de TODOS os produtos envolvidos
  algum item sem custo ou sem preço → ROXO (bloqueia)
  índice  = receita / custo × 100 → cor pelos limites
```

- Substitui a regra antiga da **cor mais crítica**: um serviço vermelho
  sozinho não bloqueia se o conjunto fecha verde — e o conjunto pode ficar
  vermelho com todos os serviços verdes.
- Cada linha continua mostrando a própria cor, **só para orientar** (achar o
  item que puxa o resultado).
- A **aprovação por alçada** (nível 2 ou 3) olha o **consolidado**.
  Aprovação Presencial (senha) ou Remoto (notificação).
- Autorização: mostra "dados de conversão" e Farol por item (orientação);
  quem bloqueia é o consolidado.

## 3. Aba Farol do convênio e API

> **Leitura real de 25/09/2026** (só GET, produção): as três rotas devolvem
> **mais campos que o Swagger** — e, em `/farol/itens`, **outros nomes**. Vale a
> resposta real (tabela abaixo); o Swagger de 25/09 está incompleto no Farol.

| Sub-aba (tela) | API externa | Campos da resposta REAL (medida em 25/09) |
|---|---|---|
| Farol › Serviços | `GET /convenios/{id}/farol/servicos` | `servico_id, servico, servico_convenio_id, codigo, codigo_tuss, tipo_codigo, tabela_ans_87, convenio, convenio_id, servico_ativo, ativo_no_convenio, somar_itens, zerar_valor, receita_propria_servico, receita_servicos, receita_produtos, receita_taxas, receita_total, custo_produtos, custo_total, margem_resultado_pct, farol, qtd_produtos, qtd_subservicos, qtd_taxas, qtd_taxas_nao_utilizadas, tem_taxas` |
| Farol › Itens | `GET /convenios/{id}/farol/itens` | por linha: `servico_raiz_id, servico_raiz, servico_pai_id, servico_pai, nivel, caminho, item_tipo, item_id, item_nome, item_descricao, codigo, tipo_codigo, tabela_ans_87, unidade_medida, quantidade, quantidade_efetiva, receita_unitaria, receita_item_total, custo_unitario, custo_item_total, utiliza_no_convenio, zerar_valor, conta_no_total, motivo_exclusao, pacote_pai, somar_itens`; repetidos do serviço raiz: `receita_total_servico, custo_total_servico, margem_servico_pct, farol_servico`; e `convenio, convenio_id` |
| Farol › Produtos | `GET /convenios/{id}/farol/produtos` | `produto_id, produto, produto_cadastro, descricao_convertida, codigo, codigo_produto, codigo_ean, apresentacao, contendo, unidade_medida, fabricante, tipo_produto, tipo_codigo, tipo_codigo_id, tabela_ans_87, tabela_ans_87_id, convenio, convenio_id, produto_ativo, ativo_no_convenio, zerar_valor, origem_receita, fonte_id, fonte_nome, tipo_precificacao, fator_k, flag_padrao_calcular, receita, receita_centavos, receita_sem_zerar, custo, custo_status, margem_resultado_pct, farol, data_inicio_vigencia, data_fim_vigencia` e diagnóstico `dbg_*` |

Filtros (do Swagger): serviços e produtos aceitam `farol` (lista por vírgula),
`ativoNoConvenio`, `servicoAtivo`/`produtoAtivo`, nome, `codigo`, `search`,
`sortBy/sortOrder`; itens aceitam `servicoRaizId`, `itemTipo`, `itemNome`,
`search`, `apenasAtivosNoConvenio`, `servicoAtivo`. Todas paginadas no
**envelope padrão** `dados/page/pageSize/total/totalPages`, permissão `convenio:read`.

**Atenção aos nomes em `/farol/itens`:** o Swagger promete `custo`, `receita`,
`farol` e `utiliza`; a resposta real traz `custo_item_total`,
`receita_item_total`, `utiliza_no_convenio` e **não tem farol por item** (só
`farol_servico`). O `conferir_farol.py` usa os nomes reais e aceita os do
Swagger por compatibilidade.

**Farol › Itens: cada linha reflete só ela** (desde 24/09/2026): produto/taxa
→ valor efetivamente considerado (0 se fora), custo, receita e margem da
linha; subserviço → total do que está dentro dele; serviço raiz → total do
serviço (= Farol do serviço).

**Conta no total pela API — agora existe.** A coluna da tela "Conta no total"
(Sim/Não) e o motivo **vêm na resposta real**: `conta_no_total` e
`motivo_exclusao` (`NAO_UTILIZA_NO_CONVENIO`, `ZERADO_EM_PACOTE`,
`PAI_FORA_DO_TOTAL`). Use-os como conferência **primária**; a margem por linha
continua sendo calculada (`receita / custo × 100`).

Leituras úteis para diagnóstico:
- `/farol/produtos`: `origem_receita` + `fonte_nome` + `fator_k` +
  `tipo_precificacao` dizem **de onde saiu o preço** do produto neste convênio
  (valor efetivo: linha, política ou cadastro); `receita_sem_zerar` é o preço
  antes do Zerar; `custo` + `custo_status` + `flag_padrao_calcular` explicam o
  custo (roxo). Campos `dbg_*` terminados em `_centavos` estão **em centavos**
  (`dbg_preco_venda_tabela_centavos`, `dbg_valor_conversao_convenio_centavos`,
  `dbg_precificacao_tabela_centavos`); `dbg_ultima_compra_reais` em reais.
- `fonte_id` **provavelmente** é o mesmo id de `fontePrecoCompraOptionsId` da
  aba Produtos — **ainda não confirmado**: grave 1 item em homologação e releia.
- Ainda não confirmado: se `receita_item_total` de item fora da conta vem 0 ou
  com o preço cheio; se `quantidade_efetiva` é quantidade × pais ou 0 quando
  fora; se `receita` de produto com `zerar_valor` vem 0. O `conferir_farol.py`
  aceita as duas leituras enquanto `conta_no_total` concordar com a previsão.

Valores do campo `farol`: o spec mostra `"VERDE"`; os demais esperados são
`"AMARELO"`, `"VERMELHO"` e o roxo (o manual chama de `SEM_CUSTO`/roxo).
**Não confirmado** o texto exato do roxo: trate qualquer valor fora de
VERDE/AMARELO/VERMELHO (ou `null` com produto envolvido) como roxo e registre.

## 4. ⚠️ O Farol inclui serviços inativos

As listas do Farol trazem também serviços **inativos no catálogo** e
vínculos antigos. Numa implantação real, a contagem pela API externa deu
~74% a mais que a tela (vínculos de serviços desativados). Antes de contar
ou reportar vermelhos:
- use `servicoAtivo=true` (e `apenasAtivosNoConvenio=true` em itens,
  `ativoNoConvenio=true` em serviços/produtos);
- cruze com `GET /servicos` (campo `ativo`);
- nunca conclua "N serviços vinculados" pela API externa sem esse cruzamento.

## 5. Custo do produto

Aba Estoque › Última Compra (Padrão Calcular ✔ → última entrada; ✘ → valor
em "Última Compra (Unidade)"). Sem custo → roxo. O custo é o mesmo em todos
os convênios. Detalhe: [04-arvore-produto-politica-fatork.md §8](04-arvore-produto-politica-fatork.md).

## 6. Como ler um vermelho (sempre investigar, nunca aceitar em silêncio)

1. Falta item ligado (Utiliza ✘ em algo que o convênio paga)?
2. Preço abaixo do contrato (valor 🔁 errado, política errada, FK errado)?
3. Item zerado indevidamente (Pacote + Zerar onde o contrato é conta aberta)?
4. Custo errado (unidade da embalagem, última compra atípica)?
5. Medicamento ausente da composição / não utilizado (custo conta, receita não)?
6. Contrato realmente deficitário → registrar e levar à clínica (decisão de negócio).

Exemplos: T13, T14 em [12-casos-de-teste.md](12-casos-de-teste.md);
diagnóstico em [13-conferencia-e-diagnostico.md](13-conferencia-e-diagnostico.md).

## 7. Outros faróis do sistema (não confundir)

- Farol de **% de gastos do convênio** (jul/2026): indicador do percentual de
  gastos do convênio — outro conceito.
- Visão geral do farol com lista de cruzamentos serviço × convênio e produto
  × convênio (ago/2026).
- Relatórios com farol: Serviços × Convênios — Farol de Margem.
