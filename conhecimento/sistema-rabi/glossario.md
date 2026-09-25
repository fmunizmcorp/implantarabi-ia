# Glossário — termos do Rabi e do faturamento em saúde

> **Fonte:** https://www.rabisistemas.com.br/manual/precos/index.html#servico-composto · `precos/arvore-de-decisao.html#tabela-mestra` · `modulos/autorizacao.html#tiss-23-87` · `tiss-tuss/index.html` · tabelas TUSS publicadas pela ANS (competência 01/2026) · **Conferido em:** 2026-09-25
> **Vale para:** produção em 25/09/2026 · **Kit:** v0.1.0

Use estas palavras do mesmo jeito com o usuário. Explique a sigla na primeira vez.

## A. Quem é quem

| Termo | O que é |
|---|---|
| **ANS** | Agência Nacional de Saúde Suplementar — regula os planos de saúde. |
| **Operadora** | A empresa do plano de saúde (tem registro ANS). No Rabi é cadastrada **antes** do convênio. |
| **Convênio** | O **contrato** entre a clínica e uma operadora (ou o "Particular"): preços, prazos, regras, o que cobre. Uma operadora pode ter mais de um convênio (ex.: contratos diferentes). |
| **Plano** | O produto que o paciente comprou da operadora (ex.: "Plano Ouro"). Fica dentro do convênio, aba Planos; o paciente tem convênio + plano + carteirinha. |
| **Particular** | Paciente que paga do bolso. No Rabi o Particular **é um convênio** — é nele que se define o preço particular. |
| **Prestador / contratado** | A clínica (ou o profissional) que presta o serviço à operadora. |
| **Beneficiário** | O paciente do plano. |
| **Carteirinha** | Número do beneficiário na operadora; vai na guia. |
| **Colaborador** | Qualquer pessoa da equipe cadastrada. Só quem tem **conselho profissional** é profissional de saúde (atende, tem grade, entra no convênio). |

## B. Documentos e fluxo da cobrança

| Termo | O que é |
|---|---|
| **TISS** | Troca de Informação em Saúde Suplementar — o padrão ANS de guias e arquivos XML entre clínica e operadora. |
| **TUSS** | Terminologia Unificada da Saúde Suplementar — os **códigos** padronizados (procedimentos, materiais, medicamentos, taxas e as tabelas de domínio). |
| **Guia** | O documento de cobrança de um atendimento: Guia de Consulta, Guia SP/SADT (exames, terapias, procedimentos ambulatoriais), Guia de Honorários, Resumo de Internação. |
| **Guia mãe / filha** | Guia principal e guias vinculadas a ela; ficam no mesmo lote. |
| **Senha / autorização** | Número que a operadora dá ao aprovar um pedido; vai na guia. |
| **Autorização prévia** | Aprovação da operadora **antes** de fazer o procedimento. No Rabi: módulo Autorização e marca `autorizacaoPrevia` no serviço do convênio. |
| **Pré-faturamento** | Conferência das guias antes de enviar (12 validações automáticas). |
| **Lote** | Conjunto de guias de um convênio e período, enviado num arquivo XML. Fechado, bloqueia edição isolada. |
| **XML TISS** | O arquivo do lote, na versão TISS configurada no convênio, com hash (código de integridade). |
| **Retorno / demonstrativo** | O que a operadora devolve: o que pagou e o que glosou. O Rabi importa e dá baixa/registra glosa automático. |
| **Glosa** | Recusa total ou parcial de um item pela operadora. |
| **Recurso de glosa** | Contestação formal, dentro do prazo do contrato. |
| **Conciliação** | Conferir o que foi cobrado × o que foi pago × o que foi glosado. |
| **Calendário de faturamento** | As janelas de entrega de guias de cada convênio no mês. |
| **Caráter do atendimento** | Eletivo ou urgência/emergência (TUSS Tabela 23). |
| **CID-10** | Código do diagnóstico. |

## C. Tabelas e códigos

| Termo | O que é |
|---|---|
| **Tabela 22** | TUSS de Procedimentos e eventos em saúde (consultas, exames, terapias, cirurgias). Código de 8 dígitos (ex.: `10101012` consulta em consultório). |
| **Tabela 18** | TUSS de Diárias, taxas e gases medicinais. |
| **Tabela 19** | TUSS de Materiais e OPME. |
| **Tabela 20** | TUSS de Medicamentos. |
| **Tabela 23** | Caráter do atendimento. |
| **Tabela 24** | CBO — especialidade do profissional. |
| **Tabela 36** | **Indicador de acidente** (trabalho, trânsito, outros). |
| **Tabela 87** | "Tabela de tabelas" — **de qual tabela vem o código do item** (ex.: 22 procedimentos, 20 medicamentos, 19 materiais, 18 taxas/diárias/gases, 00 própria da operadora, 98 própria de pacotes; no Rabi também 05 Brasíndice, 12 SIMPRO, 97 Taxa Própria). Detalhe e incertezas em [../negocio-clinica/tiss-tuss-ans.md](../negocio-clinica/tiss-tuss-ans.md). |
| **CBO / CBO-S** | Classificação Brasileira de Ocupações — código da especialidade na guia (ex.: Clínica Geral 225125, Cardiologia 225120). No Rabi chamado **CBOS**; obrigatório para faturar convênio. |
| **RQE** | Registro de Qualificação de Especialista (no CRM). Campo `rqe` da especialidade do colaborador. |
| **Conselho** | CRM, COREN, CRN, CREFITO, CRP… Número + UF vão na guia. |
| **CBHPM** | Classificação Brasileira Hierarquizada de Procedimentos Médicos (AMB): honorários por **porte** e custo operacional (UCO). |
| **Brasíndice** | Revista/tabela de preços de medicamentos (e materiais): PF e PMC. |
| **SIMPRO** | Tabela de preços de materiais e medicamentos. |
| **CMED** | Câmara que define preço máximo de medicamento (PF, PMC, PMVG) por alíquota de ICMS. |
| **PF / PMC / PMVG** | Preço Fábrica / Preço Máximo ao Consumidor / Preço Máximo de Venda ao Governo. |
| **OPME** | Órteses, Próteses e Materiais Especiais. |
| **Rol / DUT** | Rol de Procedimentos da ANS (cobertura mínima obrigatória) / Diretrizes de Utilização (condições para cobrir). |
| **Tipo de código** | No Rabi: TUSS, TISS, TGA, Tabela Própria, SIMPRO… (qual codificação o item usa). |

## D. Preço e conversão no Rabi (resumo — estudo completo em [../precos-e-conversao/00-INDICE.md](../precos-e-conversao/00-INDICE.md))

| Termo | O que é |
|---|---|
| **Valor de casa / cadastro** | O preço do item no catálogo (nível 1). |
| **3 níveis de conversão** | 3 = item dentro do convênio · 2 = política do convênio (só preço de produto) · 1 = cadastro do item. O mais específico ganha. |
| **Vazio × zero** | Campo **vazio** = "sem regra aqui, desça de nível". **0,00** = zero de verdade. Nunca usar 0,01 como marcador. |
| **3 linhas (🔒 🔁 ✅)** | Nas abas do convênio: 🔒 origem (cadastro), 🔁 o que se digita para o convênio, ✅ o que vale e sai na guia. |
| **Linha Σ** | 4ª linha só da coluna Valor do serviço: total do serviço no convênio (= receita do Farol). Em produção desde 24/09/2026. |
| **Utiliza** | "Este convênio cobre este item." Sem Utiliza: tem custo, não tem receita; no orçamento entra a R$ 0,00. |
| **Somar itens** | "Definir preço do serviço pelos itens" (no cadastro do serviço): o serviço não tem valor próprio; o preço vem dos itens. |
| **Pacote** | Marcação **por convênio**, na aba Serviços: este serviço é preço fechado. Não existe pacote no catálogo. |
| **Zerar valor em pacotes** | Marcação por item (abas Produtos, Taxas, Serviços do convênio): item já incluso no preço do pacote. Só age se o serviço-pai tem Pacote. Não desce em cascata. |
| **Valor combinado** | O valor digitado na linha 🔁 do serviço. **Não é pacote**: sozinho muda só o preço do serviço, os itens continuam somando. |
| **Fator K** | Inflator/deflator percentual aplicado sobre o preço base (ex.: +38,24% ou −10%). |
| **Política de preço por tipo de produto** | Nível 2: para cada tipo de produto do convênio, qual tabela (ex.: Brasíndice PF) e qual fator. |
| **Tabela de preços interna** | Fonte de preço de **produto** (até 3 preços). **Não** define preço particular. |
| **Subserviço** | Serviço dentro de outro (ex.: a aplicação dentro do "medicamento aplicado"). |
| **Farol** | Semáforo receita × custo: 🟢 segue, 🟡 alerta, 🔴 bloqueia (libera por alçada), 🟣 erro de preço (item sem custo ou sem receita). Régua em Parâmetros › Valores. |
| **Farol consolidado** | No orçamento/agendamento/autorização: Σ receita de todos os itens ÷ Σ custo dos produtos × 100 — um só para o conjunto (desde 23/09/2026). |
| **Nível de alçada** | Quem pode aprovar desconto, farol vermelho, edição de Atendido. Um aprova, resolve para todos do nível. |
| **Tipo de atendimento** | Classificação do atendimento (Consulta, Exame, Terapia…); o efetivo do convênio vai ao campo `tipoAtendimento` do XML. |

## E. Operação no Rabi

| Termo | O que é |
|---|---|
| **Status do agendamento** | Aguardando, Pendente (falta orçamento/autorização), Confirmado, Acolhido, Em Atendimento, Atendido, Cancelado, Remarcado. |
| **Acolhimento / check-in** | Registro da chegada; paciente vai para a fila do profissional. |
| **Encaixe** | Agendamento fora do horário regular. |
| **Depósito** | Local físico de estoque; todo local de atendimento precisa de um depósito padrão de saída ativo. |
| **Estoque Atual** | Estoque mínimo do produto (nome antigo: "Estoque Base"); abaixo dele o item fica CRÍTICO. |
| **Grade** | Horários agendáveis do profissional ou equipamento. |
| **Chave `rbk_`** | Chave da API externa da clínica. Vai só no repo privado da clínica. |
| **ATIVO / INATIVO** | Cadastros com histórico são inativados, não excluídos. Sempre confira se o item está ativo antes de mexer. |
