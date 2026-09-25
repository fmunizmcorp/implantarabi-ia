# Preços e conversão de valores — índice e ordem de leitura

> **Fonte:** https://www.rabisistemas.com.br/manual/precos/index.html (área Preços e Conversão de Valores, 25/09/2026) + Swagger 25/09/2026 + experiência de implantação real (generalizada) · **Conferido em:** 2026-09-25
> **Vale para:** produção desde 23–24/09/2026 (regra única de preço; valor combinado ≠ pacote vigente desde 25/09) · **Kit:** v0.1.0

Esta pasta é o **estudo profundo do coração do Rabi**: como cada item
(serviço, subserviço, produto, taxa) é convertido para cada convênio — nome,
código, tabela 87, tipo de atendimento, valor, se entra na conta — e como
isso vira Farol, guia e XML. Bem configurado, multiplica a produtividade da
clínica; mal configurado, perde receita ou gera glosa. **Nenhuma regra aqui
é inventada**: onde as fontes não fecham, está escrito **não confirmado** e
como verificar.

## Ordem de leitura

**Primeira vez (obrigatório, nesta ordem):**

| # | Arquivo | O que tem | Quando ler |
|---|---|---|---|
| 1 | [01-conceitos.md](01-conceitos.md) | catálogo × convênio, tipos de item, 3 níveis, vazio ≠ zero por atributo, 0,01 proibido, conversão de nome/código/descrição, tabela 87 | sempre, antes de tudo |
| 2 | [02-tabela-mestra.md](02-tabela-mestra.md) | atributo × tipo de item × precedência + nomes de campo da API por aba | antes de montar qualquer CSV |
| 3 | [03-arvore-servico.md](03-arvore-servico.md) | as 4 chaves, árvore e fórmula do serviço, tabela-verdade V1–V6, valor combinado ≠ pacote, o que mudou e quando | ao configurar serviços |
| 4 | [04-arvore-produto-politica-fatork.md](04-arvore-produto-politica-fatork.md) | cadeia do produto, 5 fontes, tabela interna Preço 1/2/3, política por tipo, Fator K, embalagem ÷ quantidade, PF/PMC, custo | ao configurar produtos/política |
| 5 | [05-arvore-taxa.md](05-arvore-taxa.md) | taxa: 2 níveis, sem FK, armadilhas de taxa em dobro | ao configurar taxas |
| 6 | [06-arvore-subservico-e-entra-sai.md](06-arvore-subservico-e-entra-sai.md) | Utiliza/Pacote/Zerar/somarItens, motivos de exclusão, tabela-verdade E1–E6, algoritmo recursivo, regra do orçamento | ao montar pacotes e serviços compostos |
| 7 | [07-quatro-linhas-do-valor.md](07-quatro-linhas-do-valor.md) | 🔒 🔁 ✅ Σ; o que a API externa expõe (receita_total; efetivo.totalConvenio não) | ao conferir a aba Serviços |
| 8 | [08-farol.md](08-farol.md) | Farol por item, serviço, consolidado; cores e limites; alçada; `/parametros/orcamento`; `/farol/*` | ao conferir e ao explicar vermelhos |
| 9 | [09-tipo-de-atendimento-e-xml.md](09-tipo-de-atendimento-e-xml.md) | tipo de atendimento efetivo, congelamento no atendimento, pré-faturamento, Atualizar Valores em Massa, XML | ao configurar tipo de atendimento e explicar guias |

**Para executar (modo Convênio):**

| # | Arquivo | O que tem | Quando ler |
|---|---|---|---|
| 10 | [10-do-contrato-a-configuracao.md](10-do-contrato-a-configuracao.md) | **o método**: régua contratual, 4 perguntas, árvore de decisão, ordem de gravação, **CSV `precos-<convenio>.csv` (21 colunas)**, mapeamento coluna → API, pacote pela API | antes de cada convênio |
| 11 | [11-receitas.md](11-receitas.md) | receitas A–I do manual + J–L da experiência, com configuração e resultado | ao traduzir cada caso do contrato |
| 12 | [12-casos-de-teste.md](12-casos-de-teste.md) | **especificação do motor**: T1–T26, K1–K12, invariantes I1–I13 | ao simular/validar e ao programar `ferramentas/conversao` |
| 13 | [13-conferencia-e-diagnostico.md](13-conferencia-e-diagnostico.md) | conferência pós-gravação, 3 serviços mínimos, 15 sintomas + 12 erros comuns, contagens de regressão R1–R6 | depois de gravar e antes de mexer em convênio já configurado |

**Para não errar de novo e para consultar:**

| # | Arquivo | O que tem | Quando ler |
|---|---|---|---|
| 14 | [14-armadilhas-vividas.md](14-armadilhas-vividas.md) | 21 armadilhas reais generalizadas (orçamento R$ 0,00, 0,01, PUT que apaga, política vazia…) | antes da primeira gravação de cada sessão |
| 15 | [15-conflitos-resolvidos.md](15-conflitos-resolvidos.md) | C1–C7 do plano + C8–C16 da área de preços: versões, decisão, fonte que prevalece | quando dois documentos disserem coisas diferentes |
| 16 | [16-referencias-do-manual.md](16-referencias-do-manual.md) | links canônicos (URL + âncora) do manual e da API | para citar a fonte ao usuário |

## Leitura mínima por situação

| Situação | Leia |
|---|---|
| sessão nova, qualquer modo | 01 → 14 (armadilhas) |
| configurar um convênio do zero | 01 → 02 → 03 → 04 → 06 → 10 → 11 → 13 |
| reajuste de valores de um convênio | 01 → 10 §2 e §6–§8 → 13 §6 (regressão) |
| "o valor veio errado / o orçamento saiu zero" | 13 §3–§5 → 06 → 14 A1 |
| explicar a um usuário leigo | 11 (receitas) + 07 (linhas) |
| programar ou revisar o motor Python | 03 §3 → 04 §1 → 06 §5–§6 → 08 §2 → **12** |

## Resumo em 10 linhas (se você só puder ler isto)

1. Três níveis: item no convênio → política do convênio (só preço de produto) → cadastro.
2. **Vazio ≠ zero.** Vazio desce; 0,00 é zero. **Nunca 0,01** como marcador.
3. **Utiliza** = o convênio cobre. Padrão desmarcado → causa nº 1 de "valor menor".
4. Itens (produtos, taxas, subserviços) **sempre entram** na conta do serviço.
5. Só saem: sem Utiliza, ou **Zerar** dentro de **pacote de preço fechado**.
6. **Valor combinado não é pacote.** Preço fechado = valor + **Pacote** + **Zerar** nos inclusos.
7. Zerar é por item e **não desce em cascata**; só a falta de Utiliza leva a subárvore.
8. Linha ✅ = valor próprio (procedimento do XML); linha **Σ** = total = receita do Farol = `receita_total`.
9. Produto: valor convertido × FK da linha; senão fonte/tipo/FK herdados campo a campo; FK é **percentual**.
10. Confira sempre: simulador × `/farol/servicos` × `/farol/itens` × orçamento de teste; 3 serviços por convênio.
