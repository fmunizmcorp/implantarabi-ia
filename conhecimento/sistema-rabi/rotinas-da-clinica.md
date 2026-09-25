# Rotinas da clínica — o dia a dia que a configuração precisa servir

> **Fonte:** https://www.rabisistemas.com.br/manual/rotinas/index.html#qual-rotina e as 7 páginas de `rotinas/` · `referencia/mapa-funcional.html#visao-por-perfil` · **Conferido em:** 2026-09-25
> **Vale para:** produção em 25/09/2026 · **Kit:** v0.1.0

**Por que a IA implantadora lê isto:** configurar é preparar o sistema para o
trabalho real. Cada rotina abaixo termina com "**o que a configuração precisa
garantir**" — use isso para decidir o que perguntar e o que testar.

| Perfil | Rotinas |
|---|---|
| Recepção / atendente | Recepção · Confirmação de agenda · Sucesso do paciente |
| Autorização / orçamento | Autorização e orçamento · Sucesso do paciente |
| Faturista | Calendário de faturamento · Autorização e orçamento |
| Financeiro | NF particular · Calendário de faturamento |
| Liderança | Liderança de atendimento · Sucesso do paciente |
| Médico | Sucesso do paciente (a parte clínica é o prontuário) |

## 1. Recepção (`rotinas/recepcao.html`)

**Objetivo:** nenhum paciente entra sem estar em ordem (cadastro,
autorização/orçamento, pagamento) e nenhuma pendência passa para o dia seguinte.

Fases: abertura (caçar agendamentos **Pendentes**, conferir autorizações do
dia, confirmar retardatários) → chegada (busca global, atualizar contatos e
carteirinha) → **check-in** (`/portal/agenda/acolhimento`, status Acolhido,
paciente na fila) → cadastro de paciente novo (buscar CPF antes; anexos até
50 MB) → agendamento e remarcação (o sistema aplica exigências do convênio e
bloqueia retorno no prazo) → encaixe e fila de espera → **caixa do particular**
(sempre a partir do orçamento; recebimento lançado na hora na conta/caixa
certa) → fechamento (todo agendamento do dia com status final).

Erros comuns: check-in de agendamento Pendente; paciente duplicado; particular
sem orçamento; recebimento não lançado; cobrar retorno como consulta nova.

**A configuração precisa garantir:** convênios com obrigatoriedade de
orçamento/autorização e prazo de retorno corretos; locais e grades dos
profissionais; tipos de pagamento, contas/caixas da recepção e categorias;
preço do convênio Particular; Farol e alçadas de desconto definidos.

## 2. Confirmação de agenda (`rotinas/confirmacao-agenda.html`)

**Objetivo:** agenda de amanhã (D-1) 100% definida — Confirmado, Cancelado ou
Remarcado. Procedimentos complexos com D-2; sexta confirma sábado a segunda.

Fases: levantar a agenda e as pendências (Relatório de Agenda filtrado por
"Aguardando" vira a lista de ligação) → **1ª onda automática** (lembrete por
SMS/e-mail com link; o paciente confirma sozinho; o médico recebe só os
confirmados) → priorizar contato humano (primeira consulta, idosos,
procedimentos com medicação) → ligar e confirmar em massa
(`/portal/agenda/confirmacao`) → remarcar na mesma ligação → no-show do dia →
fechamento.

**A configuração precisa garantir:** celular e e-mail dos pacientes corretos;
notificações e avisos parametrizados ligados em Parâmetros; horários de envio
combinados com a equipe. WhatsApp automático **não** existe ainda.

## 3. Autorização e orçamento (`rotinas/autorizacao-orcamento.html`)

**Objetivo:** zero pedido parado; toda autorização liberada vira agendamento no
mesmo dia; todo orçamento com próxima ação.

Fases: a fila de trabalho está no board (status Pendente, colunas de
autorização) → receber o pedido e montar o orçamento (serviços + produtos +
taxas + equipamentos; Farol consolidado) → solicitar a autorização **completa**
(serviço, produtos e taxas com quantidades) → acompanhar prazos e registrar
tratativas → autorização aprovada vira agendamento pelo botão Agendar →
fechamento.

Erros comuns: pedir só o serviço (o que não foi pedido não é faturado);
desconto acima da alçada "por fora"; orçamento expirar (validade padrão 30
dias); ignorar Farol 🟣 (é erro de preço no cadastro, não caso de alçada).

**A configuração precisa garantir:** composição dos serviços (quais produtos e
taxas cada um consome); marca de autorização prévia nos serviços do convênio;
preços e custos completos (senão Farol roxo); régua do Farol e níveis de
alçada; validade de orçamento.

## 4. Calendário de faturamento (`rotinas/calendario-faturamento.html`)

**Objetivo:** 100% das guias dentro da janela de cada convênio, sem glosa
evitável.

Fases: (1) prazos no cadastro do convênio — entrega de guias, pagamento,
recurso de glosa, pagamento do recurso, retorno, reajuste, pagamento no ato;
(2) ritual semanal — conferir no pré-faturamento, corrigir em lote, fechar o
lote na janela, gerar XML e PDF por guia, registrar protocolo em Administrar
Lote, gerar contas a receber no mesmo dia, registrar a NFS-e; (3) retorno da
operadora — importar o retorno TISS (baixa e glosa automáticas), conferir,
decidir recurso ou aceite dentro do prazo; (4) casos especiais — importar XML
de outro sistema.

Dica do manual: os fechamentos das operadoras costumam cair perto dos dias 28,
01, 05, 10 e 20 — sempre confirmar no portal de cada uma.

**A configuração precisa garantir:** todos os prazos do contrato no convênio
(ver [../negocio-clinica/faturamento-medico.md](../negocio-clinica/faturamento-medico.md));
versão TISS do XML por convênio; CBO de cada especialidade; códigos TUSS e
tabela 87 corretos; tipo de atendimento efetivo por serviço.

## 5. Liderança de atendimento (`rotinas/lideranca-atendimento.html`)

**Objetivo:** zero pendência atravessando o dia; exceções aprovadas com
critério; indicadores cobrados todo dia.

Fases: panorama de 10 minutos no Dashboard → acompanhar recepção e times em
tempo real (board, fila de divergências) → **aprovações por alçada** (desconto,
farol vermelho, edição de Atendido, compras — na Central de Notificações) →
indicadores (ocupação, produtividade, relatórios com farol) → fechamento.

Erros comuns: aprovar alçada "no atacado"; gerir por planilha paralela; logins
compartilhados.

**A configuração precisa garantir:** níveis de alçada e quem pertence a cada
nível; perfis com as abas certas do Dashboard; um login por pessoa.

## 6. Sucesso do paciente (`rotinas/sucesso-do-paciente.html`)

**Objetivo:** zero paciente perdido, zero horário vazio, retornos em dia.

Fases: panorama da jornada → acompanhar o paciente (autorização liberada e não
agendada, orçamentos abertos) → retornos (o sistema bloqueia retorno antes do
prazo) → resgate de pacientes sumidos → relacionamento (campanhas com filtro e
confirmação de envio) → fechamento.

Lembrete: cancelado ou falta **não** consome a sessão autorizada.

**A configuração precisa garantir:** prazo de retorno por convênio e por
serviço; notificações ligadas; tipos de atendimento (Primeira consulta,
Retorno…).

## 7. NF particular (`rotinas/nf-particular.html`)

**Objetivo:** todo recebimento particular registrado, com NFS-e emitida e o
número da nota no lançamento.

Fases: registrar o recebimento na hora → emitir a NFS-e no Rabi (módulo fiscal
ativo, 1ª fase em produção) ou, sem o módulo, no emissor externo → amarrar o
número da nota ao lançamento → recibo → conferência diária do caixa.

**A configuração precisa garantir:** contas/caixas, tipos de pagamento,
categorias e centros de custo; se a clínica aderir, configuração fiscal
(inscrição, regime, código de serviço/alíquota, certificado) — confirme com o
contador.

## 8. Médico (visão por perfil)

Manhã: e-mail com a agenda do dia (só confirmados) → fila de atendimento.
Durante: prontuário (anamnese, CID-10, procedimentos, documentos por modelo) →
**Finalizar** a cada consulta (dispara financeiro/faturamento). Fechamento: fila
zerada e sem divergências.

**A configuração precisa garantir:** grade do profissional, especialidades com
CBO e conselho, modelos de documento (atestado, receita, laudo), tipos de
impressão com logo.

## 9. Como a IA usa isto na implantação

- No fim de cada sprint, pergunte: "qual rotina isto habilita, e o que falta
  para ela rodar?".
- Os **10 cenários de teste** do guia (`implantacao/guia-implantacao.html#etapa-15`)
  percorrem estas rotinas; rode-os antes do go-live.
- Treinamento no go-live é **por perfil**, só com as telas daquele perfil
  (`referencia/mapa-funcional.html#visao-por-perfil`).
