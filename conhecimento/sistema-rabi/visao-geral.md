# Visão geral do Sistema Rabi

> **Fonte:** https://www.rabisistemas.com.br/manual/ (home, v2.3) · https://www.rabisistemas.com.br/manual/referencia/mapa-funcional.html · https://www.rabisistemas.com.br/manual/modulos/autenticacao.html · **Conferido em:** 2026-09-25
> **Vale para:** produção em 25/09/2026 (itens de roadmap marcados) · **Kit:** v0.1.0

## 1. O que é

O **Rabi** é um sistema de gestão para clínicas (SaaS, na internet). Ele cobre o
ciclo inteiro do paciente: **agenda → chegada → atendimento → cobrança**
(particular no Financeiro, convênio no Faturamento TISS), mais estoque,
compras, relatórios e notificações.

- **Endereço de uso:** `https://app.rabisistemas.com.br/` (produção).
  Homologação (ambiente de testes): `https://sistema.hmg.rabisistemas.dev/`.
- **Tipo de tela:** aplicação de página única (SPA, React). As telas vivem em
  `/portal/...`, exceto o painel inicial, que vive em `/dashboard`.
- **Login:** único para a clínica, por SSO (Keycloak — o serviço que guarda
  usuário e senha). **Sessão única:** o mesmo usuário não fica logado em dois
  lugares ao mesmo tempo.
- **API externa** (o caminho da IA implantadora):
  `https://api.rabisistemas.com.br/api/v1/integrations` — 268 operações em
  25 grupos, chave `Bearer rbk_…` por clínica. Detalhes em
  [../api-externa/00-INDICE.md](../api-externa/00-INDICE.md).

## 2. Módulos (menu principal)

| Módulo | Para que serve | Página do manual |
|---|---|---|
| **Dashboard** | Indicadores do dia em tempo real; cada aba só aparece para quem tem permissão no módulo | `modulos/dashboard.html` |
| **Agenda** | Grade, board por status, confirmação em massa, acolhimento, check-in, encaixe, fila de espera, bloqueio | `modulos/agendamento.html` |
| **Orçamento** | Proposta ao paciente com serviços, produtos, taxas e equipamentos; aprovação vira agendamento | `modulos/orcamento.html` |
| **Autorização** | Pedido à operadora (AGUARDANDO → AUTORIZADA/NEGADA → FATURADA) | `modulos/autorizacao.html` |
| **Atendimento / Prontuário** | Fila do profissional, prontuário, CID-10, documentos, finalizar | `modulos/prontuario.html` |
| **Pacientes** | Cadastro-mestre (CPF, contatos, convênio/plano/carteirinha, anexos) | `modulos/pacientes.html` |
| **Financeiro** | Contas a pagar/receber, contas e caixas, categorias, centro de custo | `modulos/financeiro.html` |
| **Faturamento (TISS)** | Pré-faturamento, lotes, XML, retorno, contas a receber | `modulos/faturamento-avancado.html` |
| **Glosas** | Tratativa de itens recusados pela operadora (recurso ou aceite) | `modulos/faturamento-avancado.html#glosas` |
| **Estoque** | Produtos, tipos, fornecedores, fabricantes, princípios ativos, depósitos, movimentação | `modulos/estoque.html` |
| **Compras** | Pedidos de compra, necessidade de compra, NF-e de fornecedor | `modulos/compras.html` |
| **Notificações** | SMS e e-mail ao paciente e à equipe; central de pendências de alçada | `referencia/mapa-funcional.html#notificacoes` |
| **Serviço online** | Área do paciente: agendar, acompanhar autorização, aprovar orçamento | `referencia/mapa-funcional.html#servico-online` |
| **Relatórios** | Agenda, rotinas, produtividade, repasses, fluxo de caixa, farol, estoque, auditoria | `modulos/relatorios.html` |
| **Configurações** | A fundação: empresa, locais, operadoras, convênios, serviços, taxas, colaboradores, parâmetros | `modulos/configuracoes.html` |
| **NFS-e (fiscal)** | Nota fiscal de serviço emitida pelo próprio Rabi (módulo opcional por clínica) | `rotinas/nf-particular.html` |

URL completa = `https://www.rabisistemas.com.br/manual/` + caminho da tabela.
Índice de links por assunto: [links-do-manual.md](links-do-manual.md).

## 3. Perfis de usuário (quem faz o quê)

| Perfil | Papel na clínica |
|---|---|
| Recepção | Agenda, chegada do paciente, cadastro, caixa do particular |
| Confirmação | Confirma a agenda do dia seguinte (pode ser a própria recepção) |
| Autorizadora | Autorizações e orçamentos com os convênios |
| Faturista | Guias, lotes TISS, retorno e glosas |
| Médico / profissional de saúde | Atende pela fila, registra prontuário, finaliza |
| Enfermagem | Aplicações, procedimentos, consumo de material (perfil sugerido; o manual agrupa em "profissional de saúde") |
| Financeiro | Lançamentos, baixas, caixa, NFS-e |
| Estoquista | Produtos, entradas, compras, mapa de estoque |
| Gestor | Indicadores, aprovações por alçada, renegociação |
| Implantador / Admin | Configurações, usuários e permissões |
| Paciente | Serviço online (agendar, acompanhar, aprovar) |

Permissões e perfis sugeridos: [perfis-e-permissoes.md](perfis-e-permissoes.md).
Dia a dia de cada perfil: [rotinas-da-clinica.md](rotinas-da-clinica.md).

## 4. Rotas principais (para citar ao usuário)

| Tela | Rota |
|---|---|
| Painel | `/dashboard` (abas `/dashboard/agendamentos`, `/autorizacoes`, `/orcamentos`, `/produtos`, `/financeiro`, `/faturamento`) |
| Agenda | `/portal/agenda` · criar `/portal/agenda/criar` · confirmação `/portal/agenda/confirmacao` · acolhimento `/portal/agenda/acolhimento` |
| Orçamento | `/portal/agenda/orcamento` |
| Autorização | `/portal/agenda/autorizacao` |
| Fila de atendimento | `/portal/fila-de-atendimento` |
| Pacientes | `/portal/pacientes` |
| Financeiro | `/portal/financeiro/registros` · `/portal/financeiro/contas-caixa` |
| Pré-faturamento | `/portal/guia2/list/pre-faturamento` |
| Lotes | `/portal/faturamento/fechar-lotes` · `/portal/lote/administrar-lote` · `/portal/lote/gerar-contas-a-receber` |
| Glosas | `/portal/glosas` |
| Estoque | `/portal/estoque/produtos` · `/portal/estoque/depositos` |
| Relatórios | `/portal/relatorios` · auditoria `/portal/relatorios/logs-auditoria` |
| Configurações | `/portal/configuracoes/...` (empresas-unidades, colaboradores, convenios, servicos, taxas, parametros…) |
| Minha conta | `/portal/minha-conta` |

A lista completa, tela a tela, está em [mapa-de-telas.md](mapa-de-telas.md).

## 5. Ideias centrais que a IA precisa ter na cabeça

1. **Configurações são a fundação.** Tudo depende de empresa, depósitos, locais,
   taxas, produtos, serviços, colaboradores e convênios bem cadastrados, **nesta
   ordem** (ordem oficial corrigida em 24/09/2026 —
   `implantacao/pre-requisitos.html#ordem-oficial`).
2. **Operadora ≠ convênio ≠ plano.** A operadora é a empresa do plano de saúde;
   o convênio é o contrato dela com a clínica (preços, prazos, regras); o plano
   é o produto que o paciente tem. Ver [glossario.md](glossario.md).
3. **O preço é resolvido por convênio**, em 3 níveis (item no convênio →
   política do convênio para produto → cadastro do item). Vazio sobe de nível;
   **0,00 é zero de verdade**. Estudo completo em
   [../precos-e-conversao/00-INDICE.md](../precos-e-conversao/00-INDICE.md).
4. **Particular é um convênio.** O preço do atendimento particular vem do
   convênio "Particular". A **tabela de preços interna** é fonte de preço de
   **produto**, não do atendimento particular (corrigido no manual em 24/09).
5. **Farol** 🟢🟡🔴🟣 compara receita do convênio com custo dos produtos. No
   orçamento, agendamento e autorização ele é **consolidado** (um só para o
   conjunto) desde 23/09/2026.
6. **Finalizar o atendimento dispara a cobrança**: particular → conta a receber;
   convênio → guia no pré-faturamento. Configuração errada vira glosa ou receita
   perdida lá na frente.

## 6. Status honesto

- Em produção e roadmap, com datas: [producao-x-roadmap.md](producao-x-roadmap.md).
- "Concluído no GitLab" = concluído no **desenvolvimento**; chega ao ambiente
  da clínica nas atualizações da semana. Se a tela ainda não mostra, diga isso
  ao usuário — não prometa.
