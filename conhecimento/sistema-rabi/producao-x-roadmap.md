# O que está em produção × o que é roadmap

> **Fonte:** https://www.rabisistemas.com.br/manual/roadmap/index.html#sprint11 · `roadmap/index.html#proximas` · `atualizacoes-2026/index.html#set-2509` · `referencia/mapa-funcional.html` · **Conferido em:** 2026-09-25
> **Vale para:** retrato de 25/09/2026 (fim da Sprint 11) · **Kit:** v0.1.0

**Conferido em 25/09/2026.** Este arquivo envelhece rápido. Antes de prometer
algo ao usuário, releia `roadmap/index.html` e `atualizacoes-2026/index.html`
no manual publicado. Regra do manual: **concluído no GitLab = concluído no
desenvolvimento**; chega ao ambiente da clínica nas atualizações da semana. Se
a tela ainda não mostra, diga "ainda não chegou no seu ambiente".

Legenda: ✅ em produção · 🔵 concluído no desenvolvimento, chegando · 🟠 roadmap.

## 1. Em produção (vale hoje)

### Preços e convênio (o coração da configuração)
| Item | Desde |
|---|---|
| Zero é zero, vazio é vazio, em todas as telas, Farol, pré-faturamento, contas a receber e XML | 23/09/2026 |
| Farol consolidado no orçamento, agendamento e autorização (Σ receita ÷ Σ custo) | 23/09/2026 |
| Coluna Tipo de Atendimento com 3 linhas na aba Serviços (efetivo vai ao `tipoAtendimento` do XML) | 23/09/2026 |
| Orçamento: item sem Utiliza entra a R$ 0,00 | 23/09/2026 |
| Linha ✅ do serviço = valor do próprio serviço (produtos e taxas saem nas áreas deles) | 23/09/2026 |
| Taxas, produtos e subserviços **sempre** entram na conta do serviço (salvo sem Utiliza ou zerados em pacote fechado) | 23/09/2026 |
| "Zerar valor em pacotes" por item, sem cascata | 24/09/2026 |
| Textos e valores finais convertidos em todas as telas do convênio (nome, descrição, código, tabela 87) | 24/09/2026 |
| Aba Farol › Itens com a conta de cada linha; sub-aba Farol › Serviços corrigida | 24/09/2026 |
| Coluna Valor do serviço com **4 linhas** (🔒 🔁 ✅ Σ) | 24/09/2026 (texto visível do "0,00" na linha ✅ ainda chega num ajuste) |
| Botão "Expandir serviço" (1ª versão; #625 em finalização) | 24/09/2026 |
| **Regra vigente:** valor combinado NÃO é pacote (preço fechado = combinado + Pacote + Zerar nos inclusos) | confirmada 25/09/2026 |
| Domínio da tabela 87 com 05 Brasíndice, 12 SIMPRO, 97 Taxa Própria | set/2026 |

### API externa
| Item | Desde |
|---|---|
| 268 operações / 191 caminhos / 25 grupos; chave `Bearer rbk_…` | 23–24/09/2026 |
| Correções do QA externo rodadas 1 a 3 (listas no envelope padrão, paginação real, `GET /agendamentos` exige data, filtro `servicoAtivo` no Farol, cabeçalho `X-ApiKey-Expires-At`, chave inválida → 401) | 24–25/09/2026 |
| Criação de login do colaborador: `POST /colaboradores/{id}/usuario` | 24/09/2026 |

### Operação
| Item | Desde |
|---|---|
| Status Pendente; orçamento/autorização obrigatórios conforme convênio; bloqueio de serviço por convênio; avisos na grade | jul–ago/2026 |
| Bloqueio de agendamento dentro do prazo de retorno | jul/2026 |
| Edição de Atendido com motivo + aprovação; divergências na Agenda e na Fila | ago/2026 |
| Nível de alçada; Central de pendências de alçada | ago–set/2026 |
| Fila de espera (#405), repetição com múltiplas sessões, progresso "x/y" (#603), Copiar agenda (#616) | set/2026 |
| Glosas rework (baixa/glosa automática do retorno TISS, relatório agregado) | ago/2026 |
| Reconciliação do pré-faturamento; localizar guia; importar XML de outro sistema | ago/2026 |
| Compras (1ª versão + melhorias); NF-e de fornecedor (#391) | ago–set/2026 |
| NFS-e — **1ª fase** (emissão no pagamento, por convênio, assíncrona, IBS/CBS, opt-in) | set/2026 |
| Permissões granulares (#395) | 15/09/2026 |
| Assinatura digital ICP-Brasil — **1ª fase** (fluxos liberados aos poucos) | 03/09/2026 |
| Tela de Auditoria (#185); mesclar pacientes (#546) | set/2026 |
| Notificações SMS + e-mail (lembrete, orçamento com link, autorização liberada); avisos parametrizados; confirmação de dados por SMS | jul–set/2026 |
| Impressão do orçamento = proposta (#614) | 24/09/2026 |
| Estoque: "Estoque Atual" (antigo Estoque Base); pré-faturamento não baixa mais estoque; reserva de medicamento | ago–set/2026 |

## 2. Concluído no desenvolvimento, chegando (🔵)

| Item | Observação |
|---|---|
| NFS-e — módulo completo (modelos de nota #465, gestão de notas #468, onboarding fiscal #472) | épico #462 concluído em 17/09 |
| LGPD — anonimização (#598), portabilidade só DPO/admin (#599), consentimento (#600), log de leitura do prontuário (#601) | concluído em 23/09 |

## 3. Aberto na Sprint 11 (segue para a próxima, sem data prometida)

Expandir serviço (#625, finalização) · Tokens de integração self-service em
Configurações (#624 — hoje a chave vem do portal comercial) · DRE gerencial
(#617) · Revisão de telas (#605) · Pagamento parcial obrigatório (#604) · MFA e
bloqueio de conta (#602) · Validação de tenant TalkMe (#597) · Filtros padrão
(#396) · Assinatura digital — finalização (#394) · **Pré-solicitação de
autorização (#380)**.

## 4. Roadmap S12–S14 (🟠 não prometer como vigente)

| Sprint | Semana | Foco |
|---|---|---|
| **S12** | 25/09–02/10/2026 | Links de pagamento via API multi-banco (#409) |
| **S13** | 02–09/10/2026 | Relatório de Rotina de Acolhimento (#382), Produtividade por usuário (#385), integração bancária (#343), novo layout do agendamento (#340), teste de capacidade (#365) |
| **S14** | 09–16/10/2026 | Integração TISS por webservice com operadoras (épico #618): fundação/log (#619), envio de lote com protocolo (#620), demonstrativos com baixa automática (#621), autorização online (#622), recurso e cancelamento (#623) |

Também sem data: WhatsApp nas notificações; atendimento finalizado exige
documento (#379).

## 5. Como usar este arquivo na implantação

- Ao sugerir uma configuração, só use o que está em **produção**.
- Se o usuário pedir algo do roadmap (ex.: envio de lote por webservice), diga
  "está previsto para a Sprint 14, ainda não disponível" e ofereça o caminho de
  hoje (XML pelo portal da operadora).
- Ao ver comportamento diferente do descrito aqui, **a tela e a API mandam**:
  registre a divergência no repo da clínica e sugira ao mantenedor do kit.
