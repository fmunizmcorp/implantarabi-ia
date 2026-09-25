# 08 — Farol de margem (item, serviço, consolidado) e alçada

> **Fonte:** https://www.rabisistemas.com.br/manual/precos/index.html#custo-e-farol · https://www.rabisistemas.com.br/manual/precos/arvore-de-decisao.html#arvore-farol · https://www.rabisistemas.com.br/manual/precos/guia-ia.html#alg-farol · https://www.rabisistemas.com.br/manual/precos/guia-ia.html#alg-farol-consolidado · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-11 · spec 25/09 (`/parametros/orcamento`, `/convenios/{id}/farol/*`) · **Conferido em:** 2026-09-25
> **Vale para:** Farol consolidado em produção desde 23/09/2026; Farol › Itens por linha desde 24/09/2026 · **Kit:** v0.1.0

O Farol compara **quanto entra** com **quanto custa**:
`índice = receita ÷ custo × 100`. Ex.: 120 = receita 20% maior que o custo.
É a **prova** de que a conversão está certa: depois de configurar um
convênio, o Farol mostra onde a clínica perde dinheiro.

## 1. Cores e limiares

| Cor | Significado | Efeito |
|---|---|---|
| 🟢 Verde | margem saudável (índice ≥ limite Amarelo) | passa |
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
> Vermelho → VERMELHO`; `Vermelho < índice < Amarelo → AMARELO`; `índice ≥
> Amarelo → VERDE`. Confira um caso exatamente no limite em homologação.

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

| Sub-aba (tela) | API externa | Campos (spec 25/09) |
|---|---|---|
| Farol › Produtos | `GET /convenios/{id}/farol/produtos` | `produto_id, produto, codigo, custo, receita, margem_resultado_pct, farol, ativo_no_convenio, produto_ativo` · filtros `farol` (lista por vírgula), `ativoNoConvenio`, `produtoAtivo`, `produto`, `codigo`, `search`, `sortBy/sortOrder` |
| Farol › Serviços | `GET /convenios/{id}/farol/servicos` | `servico_id, servico, codigo, custo_total, receita_total, receita_propria_servico, margem_resultado_pct, farol, ativo_no_convenio, servico_ativo` · filtros `farol`, `ativoNoConvenio`, `servicoAtivo`, `servico`, `codigo`, `search`, `sortBy/sortOrder` |
| Farol › Itens | `GET /convenios/{id}/farol/itens` | `servico_raiz_id, item_tipo, item_id, item_nome, custo, receita, farol, utiliza` · filtros `servicoRaizId`, `itemTipo`, `itemNome`, `search`, `apenasAtivosNoConvenio`, `servicoAtivo` |

Todas paginadas (`page`, `pageSize`, envelope `dados/page/pageSize/total/totalPages`),
permissão `convenio:read`.

**Farol › Itens: cada linha reflete só ela** (desde 24/09/2026): produto/taxa
→ valor efetivamente considerado (0 se fora), custo, receita, margem e farol
da linha; subserviço → total do que está dentro dele; serviço raiz → total do
serviço (= Farol do serviço).

**O que só existe na tela:** margem da linha, "valor efetivo" e a coluna
**Conta no total** (Sim/Não) com o motivo (`NAO_UTILIZA_NO_CONVENIO`,
`ZERADO_EM_PACOTE`, `PAI_FORA_DO_TOTAL`). Pela API:
- margem = `receita / custo × 100` (calcule);
- `utiliza: false` → fora por NAO_UTILIZA;
- `utiliza: true` e `receita = 0` → zerado em pacote fechado **ou** valor
  gravado como 0 quando deveria ser vazio — confira qual.

> Experiência (não confirmado no Swagger): em uma implantação real,
> respostas de `/farol/itens` e `/farol/produtos` trouxeram campos extras
> (`conta_no_total`, `motivo_exclusao`, `receita_total_servico`,
> `origem_receita`, `fonte_nome`, `fator_k`, `receita_sem_zerar`, `dbg_*`).
> O spec de 25/09/2026 **não** os documenta. Se a resposta real os trouxer,
> use-os como conferência extra; **nunca** dependa deles.

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
