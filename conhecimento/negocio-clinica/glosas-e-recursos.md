# Glosas e recursos — e como a configuração previne

> **Fonte:** https://www.rabisistemas.com.br/manual/referencia/mapa-funcional.html#glosas · `rotinas/calendario-faturamento.html#fase-3` · `modulos/faturamento-avancado.html#glosas` · método de recurso usado numa operação real de faturamento (generalizado) · **Conferido em:** 2026-09-25
> **Vale para:** Rabi em produção em 25/09/2026 (recurso por webservice é roadmap S14) · **Kit:** v0.1.0

## 1. O que é glosa

**Glosa** é a recusa, total ou parcial, de um item cobrado. Vem no retorno /
demonstrativo da operadora, com um **motivo** da TUSS Tabela 38 (mensagens de
glosa). Glosa não contestada dentro do prazo vira **perda definitiva**.

No Rabi: o retorno TISS importado dá **baixa e registra a glosa sozinho**;
em `/portal/glosas` decide-se **recurso** (contestar) ou **aceite** (estorno).
Ciclo: PENDENTE → EM_RECURSO → RECUPERADA / ACEITA / DEFINITIVA. O prazo de
recurso vem do cadastro do convênio.

## 2. Tipos de glosa

| Tipo | Exemplos | Causa típica |
|---|---|---|
| **Administrativa** | Carteirinha inválida, guia fora do prazo, senha ausente/vencida, dados incompletos, duplicidade | Recepção/autorização/prazo |
| **Técnica / de codificação** | Código TUSS inválido ou desatualizado, tabela 87 errada, CBO incompatível, quantidade acima da autorizada, valor acima do contrato | **Cadastro** (serviço, convênio, colaborador) |
| **Clínica** | Procedimento sem indicação, sem DUT, incompatível com CID | Documentação clínica |
| **Linear / de valor** | Pagou menos que a tabela (reajuste não aplicado pela operadora) | Contrato × sistema da operadora |

## 3. Classificação para decidir o recurso

| Categoria | Situação | Ação |
|---|---|---|
| **A — improcedente** (alta chance) | Item coberto no Rol negado; código correto chamado de inválido; urgência negada por falta de autorização (Lei 9.656/98 art. 35-C); prazo cumprido tratado como fora do prazo; reajuste contratual ignorado; cláusula expressa contrariada | Recorrer já |
| **B — contestável** | Cobertura ambígua; código desatualizado mas procedimento feito (corrigir e justificar); quantidade acima do habitual com relatório; material de alto custo com NF | Recorrer com documentação |
| **C — possivelmente procedente** | Fora de cobertura; experimental; prazo realmente perdido | **Não** redigir automático — levar à coordenação |

Priorize A e B, do maior valor para o menor, e **pelo prazo que vence antes**.

## 4. O recurso — fundamentação tripla

Todo recurso tem **três fundamentos**, específicos (nunca genéricos):
1. **Legal** — norma com número, ano e artigo (ex.: Lei 9.656/1998, RN da ANS
   vigente). Cite só o que conferiu na fonte.
2. **Contratual** — a cláusula e o anexo do contrato com aquela operadora.
3. **Clínica** — indicação, CID, relatório, exames (quando cabível).

Estrutura: identificação (prestador, operadora, guia, beneficiário pela
**carteirinha**, data, item, valor, motivo) → fundamentação (2–4 parágrafos) →
documentos a anexar (e de onde tirar) → pedido (cancelar a glosa e pagar em X
dias, conforme contrato).

LGPD: recurso é documento externo — só os dados necessários; nunca copie
prontuário inteiro.

## 5. Prevenção começa na configuração (o papel da IA implantadora)

| Glosa recorrente | O que configurar certo |
|---|---|
| Sem autorização | Marca `autorizacaoPrevia` nos serviços do convênio que exigem; convênio exigindo autorização no agendamento; ver [autorizacao-previa.md](autorizacao-previa.md) |
| Código / tabela 87 errados | Código TUSS e tabela 87 **por convênio** (nível 3) quando o contrato usa código próprio; ver [tiss-tuss-ans.md](tiss-tuss-ans.md) |
| CBO incompatível | Especialidades com CBO correto no colaborador e no convênio (aba Especialidades/Colaboradores) |
| Valor acima/abaixo do contrato | Preços por convênio a partir da régua contratual; política por tipo de produto; Fator K; conferir no Farol |
| Item cobrado em dobro no pacote | Pacote marcado + Zerar nos itens inclusos |
| Item não coberto cobrado | Sem Utiliza (custo sem receita) |
| Retorno cobrado como consulta | Prazo de retorno no convênio e no serviço |
| Fora do prazo | Prazos no convênio + calendário de faturamento |
| Quantidade acima da autorizada | Autorização com produtos e taxas e quantidades; reconciliação no pré-faturamento |

**Padrões** valem mais que casos: glosa do mesmo motivo em várias guias, ou do
mesmo item sempre no mesmo convênio, indica **erro de cadastro**. A IA deve
propor a correção do cadastro (com prévia e aprovação), não só o recurso.

## 6. Indicadores

Taxa de glosa (glosado ÷ faturado), recuperação (recuperado ÷ recorrido),
glosas por motivo e por convênio (Relatório agregado de glosas, #587), prazo
médio de resposta ao recurso.
