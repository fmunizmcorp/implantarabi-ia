# Mapa de telas do Rabi — menu → rota → o que faz → quem usa

> **Fonte:** https://www.rabisistemas.com.br/manual/referencia/mapa-funcional.html (e âncoras de cada módulo) + `modulos/*.html` · **Conferido em:** 2026-09-25
> **Vale para:** produção em 25/09/2026; itens 🟠 são roadmap · **Kit:** v0.1.0

Rota = o que aparece depois de `app.rabisistemas.com.br`. Perfis: ver
[perfis-e-permissoes.md](perfis-e-permissoes.md).

> ⚠️ **Correção sobre o manual:** a página `referencia/mapa-funcional.html#configuracoes`
> ainda diz que a *Tabela de Preços Internos* guarda "valores dos serviços para
> atendimento particular". **Está errado.** A própria página de Configurações
> (`modulos/configuracoes.html#tabela-precos`, corrigida em 24/09/2026) diz:
> a tabela interna é **fonte de preço de PRODUTO** (até 3 preços por produto).
> **O preço do atendimento particular vem do convênio "Particular".** Siga isto.

## Agenda (`#agenda`)

| Menu / função | Rota | O que faz | Quem usa |
|---|---|---|---|
| Agenda (board) | `/portal/agenda` | Grade dia/semana; board por status (Aguardando, Pendente, Confirmado, Acolhido, Em Atendimento, Atendido, Cancelado, Remarcado); colunas de autorizações; "faltam X de Y"; sessões "x/y" | Recepção, Confirmação, Gestor |
| Novo agendamento | `/portal/agenda/criar` | Data/hora, paciente, convênio+plano, especialidade, profissional, local, equipamentos, tipo Normal/Encaixe, anexos. Exige orçamento/autorização conforme o convênio; bloqueia retorno dentro do prazo | Recepção |
| Editar | `/portal/agenda/:id/editar` | Remarcar, trocar profissional. Atendido não se edita direto (pede motivo + aprovação) | Recepção |
| Confirmação em massa | `/portal/agenda/confirmacao` | Confirma vários "Aguardando" de uma vez | Confirmação |
| Acolhimento | `/portal/agenda/acolhimento` | Lista do dia; registra chegada | Recepção |
| Check-in | `/portal/agenda/acolhimento/:id/checkin` | Status vira Acolhido; paciente entra na fila do profissional | Recepção |
| Bloqueio de agenda | `/portal/agenda/bloqueio` | Feriado, férias, manutenção (não cancela o que já existe) | Recepção, Gestor |
| Repetir (série) | botão na agenda | Sessões semanais/quinzenais/mensais | Recepção |
| Fila de espera | Agenda → Fila de Espera | Sugere encaixe quando alguém cancela; tem permissão própria | Recepção |
| Copiar agenda | Agenda / grade | Cria agenda nova de profissional ou equipamento com tudo, menos datas | Implantador, Gestor |

## Orçamento (`#orcamento`)

| Função | Rota | O que faz | Quem usa |
|---|---|---|---|
| Lista | `/portal/agenda/orcamento` | Ciclo RASCUNHO → AGUARDANDO_APROVACAO → APROVADO_CLIENTE → CONFIRMADO → AGENDADO → REALIZADO; validade padrão 30 dias | Autorizadora, Recepção |
| Novo | `/portal/agenda/orcamento/criar` | Serviços com produtos, taxas e equipamentos; preço pela conversão do convênio; **Farol consolidado**; desconto acima da alçada pede aprovação | Autorizadora, Recepção |
| Ver / aprovar | `/portal/agenda/orcamento/:id` | Enviar ao paciente (PDF + link), aprovar (cria agendamento), rejeitar, cancelar. Aprovado não se edita | Autorizadora |
| Reabrir | `/portal/agenda/orcamento/:id/reabrir` | Recupera orçamento cancelado | Autorizadora |

## Autorização (`#autorizacao`)

| Função | Rota | O que faz | Quem usa |
|---|---|---|---|
| Lista | `/portal/agenda/autorizacao` | Status AGUARDANDO/AUTORIZADA/NEGADA/FATURADA; painel "Original vs Convênio"; timeline | Autorizadora, Gestor |
| Nova | `/portal/agenda/autorizacao/criar` | Paciente + carteirinha, serviços, produtos e taxas com quantidade, caráter (Tabela 23), Tabela 87 do item | Autorizadora |
| Agendar da autorização | botão Agendar | Agendamento já preenchido | Autorizadora, Recepção |
| 🟠 Pré-solicitação | — | Validação interna antes de enviar (#380) — roadmap | — |

## Atendimento / Prontuário (`#atendimento`)

| Função | Rota | O que faz | Quem usa |
|---|---|---|---|
| Fila de atendimento | `/portal/fila-de-atendimento` | Quem fez check-in; área de divergências com botão Corrigir | Médico, Recepção |
| Prontuário | `/portal/pacientes/:id/atendimento/:id` | Anamnese, CID-10, procedimentos, prescrição, documentos por modelo; saída de estoque ligada ao atendimento | Médico |
| Finalizar | botão | Irreversível: Atendido + particular → conta a receber; convênio → guia no pré-faturamento | Médico |

## Pacientes (`#pacientes`)

| Função | Rota | O que faz | Quem usa |
|---|---|---|---|
| Lista / busca global | `/portal/pacientes` · topo de qualquer tela | Busca por nome parcial, telefone, e-mail, CPF | Recepção |
| Novo | `/portal/pacientes/criar` | Dados, CEP, contatos, convênio/plano/carteirinha, responsável, anexos até 50 MB | Recepção |
| Ficha / editar | `/portal/pacientes/:id` · `/:id/editar` | Histórico; dados pessoais bloqueados para edição (proteção) | Recepção, Médico |
| Mesclar duplicados | Pacientes | Unifica cadastros preservando histórico | Recepção, Admin |

## Financeiro (`#financeiro`)

| Função | Rota | O que faz | Quem usa |
|---|---|---|---|
| Registros | `/portal/financeiro/registros` | Lançamentos a pagar/receber; baixas (inclusive parcial) | Financeiro |
| Novo a pagar / a receber | `.../registros/pagar/criar` · `.../receber/criar` | Parcelamento UNITARIO/AGRUPADO, recorrência | Financeiro |
| Contas e caixas | `/portal/financeiro/contas-caixa` | Bancos, caixas, carteiras digitais, saldo inicial por unidade | Financeiro, Implantador |
| Histórico de contas | `/portal/financeiro/historico-contas` | Evolução do saldo | Financeiro |
| Tipos de conta / pagamento | `/portal/financeiro/tipos-de-conta` · `/tipos-de-pagamento` | Natureza da conta; formas de pagamento (dinheiro, PIX, cartões…) | Implantador |
| Categorias / centro de custo | `/portal/financeiro/categorias-de-pagamento` · `/centro-de-custo` | Classificação gerencial (base do fluxo de caixa) | Financeiro, Gestor |
| 🟠 Links de pagamento | — | Sprint 12 (#409) | — |
| 🟠 Integração bancária | — | Sprint 13 (#343) | — |

Regra de ouro do manual: todo lançamento exige conta/caixa + categoria + centro
de custo + tipo + data + valor + origem.

## Faturamento TISS e glosas (`#faturamento`, `#glosas`)

| Função | Rota | O que faz | Quem usa |
|---|---|---|---|
| Pré-faturamento | `/portal/guia2/list/pre-faturamento` | 12 validações automáticas; correção em lote; reconciliação autorizado × agendado × atendido × faturado | Faturista |
| Buscar / inserir guia | `/portal/guia/buscar` · `/portal/guia/inserir` | Localiza pelo número; insere só em lote aberto | Faturista |
| Fechar lotes | `/portal/faturamento/fechar-lotes` | Agrupa por convênio + período; gera XML na versão TISS do convênio, com hash | Faturista |
| Administrar lote | `/portal/lote/administrar-lote` | Protocolo, reabrir (com permissão), reemitir XML, PDF por guia | Faturista, Gestor |
| Gerar contas a receber | `/portal/lote/gerar-contas-a-receber` | Ponte Faturamento → Financeiro | Faturista, Financeiro |
| Importar XML / retorno | função do faturamento | Baixa e glosa automáticas a partir do retorno TISS | Faturista |
| Glosas | `/portal/glosas` | PENDENTE → EM_RECURSO → RECUPERADA / ACEITA / DEFINITIVA; prazo vem do convênio | Faturista, Gestor |
| NFS-e | módulo fiscal | 1ª fase em produção (opt-in); ver [producao-x-roadmap.md](producao-x-roadmap.md) | Faturista, Financeiro |
| 🟠 Envio por webservice | — | Sprint 14 (épico #618) | — |

## Estoque e Compras (`#estoque`, `#compras`)

| Função | Rota | O que faz | Quem usa |
|---|---|---|---|
| Produtos | `/portal/estoque/produtos` (+ `/criar`) | Catálogo: nome, tipo, fornecedor, fabricante, princípio ativo, custos, Estoque Atual (mínimo) | Estoquista |
| Tipos de produto | `/portal/estoque/produtos/tipos-produtos` | Medicamento, Material, Insumo… (antes dos produtos) | Implantador |
| Fornecedores / Fabricantes / Princípios ativos | `/portal/estoque/fornecedores` · `/fabricantes` · `/principios-ativos` | Cadastros de apoio | Estoquista |
| Depósitos | `/portal/estoque/depositos` | Farmácia, almoxarifado; **1 depósito mínimo por unidade logo após a empresa** | Estoquista, Implantador |
| Movimentação | dentro do módulo | Entradas, saídas, transferências, ajustes; baixa automática no atendimento | Estoquista |
| Compras | menu Compras | Pedidos, necessidade de compra, aprovação na Central, NF-e de fornecedor | Estoquista, Gestor |

## Relatórios e Dashboards (`#relatorios`, `#dashboards`)

Relatórios em `/portal/relatorios` (só leitura): Agenda (CSV), Rotina de
Recepção, Rotina de Autorização, Rotina de Fechamento, Ocupação, Produtividade,
Repasses, Fluxo de Caixa, Autorizações, **Médicos × Convênios e Serviços ×
Convênio com farol**, Mapa de Estoque, Pacientes em Uso, Glosas agregado,
Logs de Auditoria (`/portal/relatorios/logs-auditoria`, só admin).
Para a implantação: **Relatórios › Cadastro › Serviços × Convênios — Farol de
Margem** e **Relatórios › Agenda › Validação de Configuração** (conferência).

Dashboard: `/dashboard` e abas agendamentos, autorizacoes, orcamentos,
produtos, financeiro (exige FINANCEIRO → VIEW), faturamento.

## Configurações (`#configuracoes`) — a fundação

Na ordem oficial de implantação (corrigida em 24/09/2026):

| # | Menu | Rota | O que faz |
|---|---|---|---|
| 1 | Empresas e Unidades | `/portal/configuracoes/empresas-unidades` | CNPJ, endereço, logo; unidades físicas |
| 2 | Depósito mínimo | `/portal/estoque/depositos` | 1 por unidade — todo local exige depósito padrão de saída ativo |
| 3 | Locais / salas | `/portal/configuracoes/empresas-unidades/locais` | Consultórios e salas ("Local do Agendamento") |
| 3 | Tipos (tabelas básicas) | `/portal/configuracoes/tipo-atendimento` · `/tipos-de-codigo` · `/tipos-de-anexos` · `/tipo-identificacao` · `/servicos/tipos` · `/taxas/tipos` | Cadastros auxiliares |
| 4 | Operadoras | `/portal/configuracoes/operadoras` | Empresa do plano (antes dos convênios) |
| 4 | Fornecedores / fabricantes | `/portal/estoque/fornecedores` · `/fabricantes` | Apoio ao catálogo |
| 5 | Taxas | `/portal/configuracoes/taxas` | Sala, material, guia… (antes de serviços e convênios) |
| 6 | Produtos | `/portal/estoque/produtos` | Catálogo (antes dos serviços de medicamento) |
| 7 | Equipamentos | `/portal/configuracoes/equipamentos` | Aparelhos com grade própria |
| 8 | Serviços | `/portal/configuracoes/servicos` | Catálogo com código TUSS; subserviços antes dos pais |
| 8 | Tabela de preços internos | `/portal/configuracoes/tabela-precos-internos` | **Preço de PRODUTO** (até 3 preços); opcional |
| 9 | Colaboradores | `/portal/configuracoes/colaboradores` | E-mail (login), especialidades com CBO, conselho, repasse, grade |
| 10 | Convênios | `/portal/configuracoes/convenios` | Dados e prazos; depois abas Planos, Especialidades, Produtos, Serviços, Colaboradores, Taxas, Farol, Dados Fiscais |
| 11 | Conferência pelo Farol | Convênio › aba Farol › Itens | Cada linha com a própria conta |
| 12 | Financeiro / fiscal / estoque | Financeiro e módulo fiscal | Contas, caixas, tipos de pagamento, categorias, centros de custo, configuração fiscal |
| 13 | Pacientes | `/portal/pacientes` | Migração/importação |
| 14 | Parâmetros | `/portal/configuracoes/parametros` | Horários, obrigatoriedades, notificações, serviço online, **Parâmetros › Valores (régua do Farol)**, descontos por alçada |
| 14 | Documentos e impressão | `/portal/configuracoes/tiposDocumentoAtendimento` · `/tipo-impressao` | Modelos de atestado/receita/laudo; cabeçalho/rodapé |
| 14 | Usuários e permissões | Configurações → Colaboradores / Perfis | Permissões granulares |

Detalhe por etapa: `implantacao/guia-implantacao.html#etapa-1` … `#etapa-15`,
`#go-live`; pré-requisitos: `implantacao/pre-requisitos.html#mapa`.

## Funcionalidades transversais (`#transversais`)

Busca global · guard de edição (avisa antes de sair sem salvar) · setas
próximo/anterior · proteção contra duplo clique · Farol 🟢🟡🔴🟣 · nível de
alçada · edição de Atendido com aprovação · status Pendente · "faltam X de Y".
