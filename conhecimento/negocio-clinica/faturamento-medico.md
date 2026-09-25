# Faturamento médico — guias, lotes, prazos e recebimento

> **Fonte:** https://www.rabisistemas.com.br/manual/rotinas/calendario-faturamento.html#conceito · `modulos/faturamento-avancado.html#pre-faturamento` · `modulos/configuracoes.html#convenios-campos` · legenda de preenchimento da Guia SP/SADT de uma entidade intermediadora (generalizada) · Componente de Conteúdo e Estrutura TISS 202511 (ANS) · **Conferido em:** 2026-09-25
> **Vale para:** padrão TISS vigente e Rabi em produção em 25/09/2026 · **Kit:** v0.1.0

## 1. As guias TISS (o que cada uma cobra)

| Guia | Para quê | Observação prática |
|---|---|---|
| **Guia de Consulta** | Consulta eletiva simples | Uma consulta por guia; sem materiais/medicamentos |
| **Guia SP/SADT** (Serviço Profissional / Serviço Auxiliar de Diagnóstico e Terapia) | Exames, terapias, aplicações, procedimentos ambulatoriais, sessões | A guia mais usada numa clínica de infusão/exames; leva procedimentos + "outras despesas" (materiais, medicamentos, taxas) |
| **Anexo de Outras Despesas** | Materiais, medicamentos, taxas, diárias, gases ligados à SP/SADT ou internação | Cada item com a tabela de origem (Tabela 87) |
| **Guia de Honorários** | Honorário do profissional em atendimento hospitalar (internação) | Pouco comum em clínica ambulatorial |
| **Resumo de Internação / Solicitação de Internação** | Contas hospitalares | Fora do escopo de clínica ambulatorial |
| **Anexos de OPME, quimioterapia, radioterapia** | Solicitações específicas | Exigem autorização |
| **Guia de Recurso de Glosa** | Contestar glosa | Ver [glosas-e-recursos.md](glosas-e-recursos.md) |

Campos que mais geram glosa numa SP/SADT (conforme legendas de preenchimento):
registro ANS da operadora; número da guia e da **senha** de autorização com
validade; carteirinha e validade; contratado solicitante e executante
(código na operadora ou CNPJ/CPF); **conselho, número e UF** do profissional;
**CBO**; caráter do atendimento (eletivo × urgência); **CID-10** quando é
terapia, série ou pequena cirurgia; indicação clínica; código da tabela
(Tabela 87) + código do procedimento + quantidade solicitada/autorizada;
**tipo de atendimento**; indicador de acidente (Tabela 36); datas de realização.
No Rabi, o pré-faturamento valida boa parte disso (12 validações).

## 2. Do atendimento ao dinheiro (no Rabi)

1. **Finalizar o atendimento** gera a guia no pré-faturamento, com valores
   **congelados** no momento do atendimento (tabela mudou depois? use
   "Atualizar Valores em Massa" na conferência).
2. **Pré-faturamento** (`/portal/guia2/list/pre-faturamento`): conferir
   números, procedimentos, valores × tabela do convênio, CBO, CID, anexos;
   corrigir em lote quando o erro se repete; reconciliação
   autorizado × agendado × atendido × faturado.
3. **Fechar o lote** (`/portal/faturamento/fechar-lotes`): por convênio +
   competência; gera o **XML** na versão TISS do convênio, com hash; guias
   ficam travadas (snapshot do que foi enviado).
4. **Enviar** pelo portal/canal da operadora (webservice direto do Rabi é
   roadmap, Sprint 14) e **registrar o protocolo** em Administrar Lote.
5. **Gerar contas a receber** no mesmo dia (`/portal/lote/gerar-contas-a-receber`),
   com vencimento pelo prazo de pagamento do convênio.
6. **NFS-e** do ciclo (módulo fiscal, se ativo) e número da nota no lançamento.
7. **Retorno / demonstrativo**: importar o retorno TISS → o Rabi dá baixa no
   que foi pago e registra glosa no que foi negado.
8. **Conciliação**: conferir baixas (pagamento menor = baixa parcial), saldo em
   aberto e glosas; decidir recurso ou aceite dentro do prazo.

## 3. Prazos do contrato que viram campos do convênio

| Prazo (contrato) | Campo no Rabi (API: `ConvenioBase`) | Para que serve |
|---|---|---|
| Entrega de guias (dias após atendimento, ou janela fixa do mês) | Prazo de entrega de guias (`prazoLimiteEntregaGuias`) | Data de corte do calendário |
| Pagamento após recebimento do lote | Prazo de pagamento (`prazoPagamento`) | Vencimento do contas a receber |
| Recurso de glosa | Limite de recurso de glosa (`prazoRecursoGlosa`) | Até quando contestar |
| Resposta/pagamento do recurso | `prazoPagamentoRecursoGlosa` | Cobrar a operadora |
| Retorno de consulta | Prazo de retorno (`prazoRetorno`) | Bloqueio de cobrar retorno como nova consulta |
| Reajuste | Prazo de reajuste (`prazoReajuste`), data de reajuste | Lembrar de aplicar reajuste |
| Autorização | `prazoAutorizacao` | Validade/prazo da autorização |
| Pagamento no ato | Tela: "Pago no ato do atendimento?" (na API, provável `faturadoPagamento` — **confirme no Swagger** antes de gravar) | Convênio de desconto ou pagamento pelo próprio paciente |
| Vigência | `dataInicio` / `dataFim` / `dataRenovacao` | Contrato em vigor |

Nomes exatos e formato: [../api-externa/00-INDICE.md](../api-externa/00-INDICE.md).
Sempre extraia o prazo **do contrato ou manual do credenciado** com página e
cláusula; se não achar, pergunte — não invente prazo padrão.

## 4. Calendário de faturamento

Monte uma tabela por convênio: janela de entrega, dia de fechamento interno
(sempre **antes** do último dia), dia de conferência do retorno, dia-limite de
recurso. Os fechamentos das operadoras costumam cair perto dos dias 28, 01,
05, 10 e 20 do mês — confirme no cronograma publicado por cada uma (muda de
ano para ano). Algumas exigem também entrega **física** e envio da nota fiscal
até uma data; nota atrasada pode empurrar o pagamento para o ciclo seguinte.

Ritual semanal recomendado (`rotinas/calendario-faturamento.html#fase-2`):
conferir toda semana, fechar na janela de cada convênio, gerar contas a
receber no dia do envio.

## 5. Particularidades que aparecem em contratos

- **Tabela de referência + percentual**: ex. "CBHPM edição X com deflator de
  Y% no porte", "Brasíndice PF + 38,24% para medicamento de uso restrito
  hospitalar", "SIMPRO sem taxa de comercialização", "SIMPRO −10%". Vira
  **política de preço por tipo de produto** e **Fator K** no convênio (ver
  [fontes-de-preco.md](fontes-de-preco.md)).
- **Códigos próprios** da operadora (tabela 00) para taxas e pacotes (tabela 98).
- **Pacotes**: preço fechado que inclui itens (no Rabi: valor combinado +
  Pacote + Zerar nos inclusos).
- **Item não coberto**: fica **sem Utiliza** (custo sem receita) — não se
  inventa preço.
- **Entidades intermediadoras** (associações que faturam em nome de várias
  operadoras) têm regras próprias por subconvênio; trate cada subconvênio como
  um convênio, conferindo caso a caso.
- **Versões TISS diferentes** por tipo de guia (ex.: consulta numa versão e
  SP/SADT noutra) em alguns convênios — confira no manual do credenciado.

## 6. Indicadores do faturamento

Taxa de glosa (% do faturado), prazo médio de recebimento, guias fora do prazo,
recuperação de glosa (recurso ganho ÷ glosado), faturado × atendido
(receita esquecida). No Rabi: Dashboard → Faturamento, Relatório agregado de
glosas, Rotina de Fechamento.
