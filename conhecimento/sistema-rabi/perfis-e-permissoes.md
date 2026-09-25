# Perfis e permissões no Rabi

> **Fonte:** https://www.rabisistemas.com.br/manual/modulos/permissoes-granular.html#comparativo · `modulos/autenticacao.html#permissoes-acesso` · `modulos/configuracoes.html#usuarios` · `referencia/mapa-funcional.html#seguranca` · `referencia/mapa-funcional.html#visao-por-perfil` · **Conferido em:** 2026-09-25
> **Vale para:** produção desde 15/09/2026 (granular #395) · **Kit:** v0.1.0

## 1. Dois modelos — qual vale hoje

| | Modelo antigo (base histórica) | **Modelo granular (vigente desde 15/09/2026, #395)** |
|---|---|---|
| Perfis por usuário | 1 papel (Role) | **vários** perfis (PerfilPermissao) |
| Ações | 4 fixas | 10+ configuráveis |
| Granularidade | por módulo | por permissão (funcionalidade) |
| Grupos | não | sim (GrupoPermissao) |
| Onde se configura | fixo | tela de administração |
| SSO (Keycloak) | não | sincroniza grupos |

Na migração, os papéis antigos viraram perfis padrão: "Recepcionista
(padrão)", "Médico (padrão)", "Administrador (padrão)", "Gerente (padrão)".
A clínica pode ajustar ou criar perfis novos. Se o usuário tem vários perfis,
vale a **soma** (união) das ações de todos.

## 2. Grupos de funcionalidade e níveis

**Grupos (módulos):** AGENDAMENTO · ATENDIMENTO · PACIENTES · FINANCEIRO ·
FATURAMENTO · CONFIGURACOES · ESTOQUE · RELATORIOS · DASHBOARD · COMPRAS
(ago/2026). A **Fila de Espera** tem permissão própria, separada do
agendamento (#612).

**Níveis do modelo antigo** (hoje um subconjunto das ações granulares):
`NONE < VIEW < CREATE < UPDATE < DELETE`.
- VIEW = só ver. CREATE e UPDATE precisam de VIEW. DELETE com cautela.

**Ações granulares** (exemplos do manual): VIEW, CREATE, UPDATE, DELETE,
EXPORT, IMPRIMIR, AUTORIZAR, CANCELAR, REATIVAR, ESTORNAR… Há permissões
especiais configuráveis em parâmetros: aprovação dupla, quebra de bloqueio com
justificativa, e níveis de desconto ligados ao **nível de alçada**.

Tudo o que muda em perfis/grupos vai para o log de auditoria (quem, quando,
antes × depois).

## 3. Onde se configura (e o que a IA consegue fazer)

| Tarefa | Onde | Pela API externa? |
|---|---|---|
| Criar colaborador (profissional ou administrativo) | Configurações → Colaboradores | Sim (`/colaboradores`) |
| **Criar o login** do colaborador | Configurações → Colaboradores | **Sim:** `POST /colaboradores/{id}/usuario` (e-mail + senha ≥ 8 caracteres; **409 = já tem login**, não é falha). Cria o acesso no Keycloak |
| Montar perfis, grupos e atribuir ao usuário | Configurações → Colaboradores → editar → perfis | **Não** — a API externa não cobre perfis e permissões. Faça com o implantador na tela, a partir da matriz aprovada |
| Alçadas de desconto | Configurações → Parâmetros (descontos) | Parâmetros de desconto têm rota própria (ver [../api-externa/00-INDICE.md](../api-externa/00-INDICE.md)) |

A **chave da API** (`rbk_`) tem as **próprias** permissões (ex.:
`convenio:read`, `servico:update`, `equipamento:read`…). Elas controlam o que a
IA pode fazer pela API — **não** são as permissões dos usuários da clínica.

## 4. Perfis sugeridos (ponto de partida para a conversa)

Proposta do kit para a IA **sugerir** e o dono da clínica **decidir**. Ajuste
ao tamanho da clínica (em consultório pequeno, uma pessoa acumula perfis).
Legenda: V = ver · C = criar · U = editar · D = excluir · — = sem acesso.

| Grupo | Recepção | Enfermagem | Médico | Faturamento | Financeiro | Gestor | Admin/Implantador |
|---|---|---|---|---|---|---|---|
| DASHBOARD | V | V | V | V | V | V | V |
| AGENDAMENTO | V C U | V | V | V | — | V C U D | V C U D |
| Fila de espera | V C U | — | V | — | — | V C U | V C U D |
| ATENDIMENTO (fila/prontuário) | V (fila) | V C U | V C U | V | — | V | V |
| PACIENTES | V C U | V | V | V | V | V C U | V C U D |
| FATURAMENTO | — | — | — | V C U | V | V | V C U |
| FINANCEIRO | C (recebimento no caixa) | — | — | V | V C U D | V | V |
| ESTOQUE | — | V C U (consumo) | — | V | — | V | V C U D |
| COMPRAS | — | V C (pedido) | — | — | V | V C U (aprova) | V C U D |
| RELATORIOS | V (agenda/rotina) | — | V (produtividade) | V | V | V | V |
| CONFIGURACOES | — | — | — | — | — | V | V C U D |

O que cada perfil **vê e não vê**, em linguagem simples:

- **Recepção:** vê agenda, acolhimento, fila, pacientes, orçamento e registra
  recebimento particular no caixa. **Não vê** prontuário clínico, faturamento de
  convênio, fluxo de caixa completo nem configurações.
- **Enfermagem:** vê a fila e o atendimento para registrar aplicações e
  procedimentos, e o consumo de estoque. **Não vê** financeiro nem faturamento.
  O manual trata como "profissional de saúde" (tem conselho, COREN).
- **Médico:** vê a própria fila, prontuário, histórico do paciente, e a própria
  produtividade. **Não vê** financeiro, faturamento nem configurações. A fila
  mostra só os pacientes dele.
- **Faturamento:** vê pré-faturamento, lotes, glosas, autorizações e o cadastro
  de convênios em leitura. **Não edita** preços de convênio (isso é do
  implantador/gestor, com aprovação).
- **Financeiro:** lançamentos, baixas, caixas, contas a receber dos lotes,
  NFS-e. Estorno de baixa é restrito ao gerente financeiro.
- **Gestor:** vê tudo para acompanhar; aprova por alçada (desconto, farol
  vermelho, edição de Atendido, compras); relatórios com farol.
- **Admin/Implantador:** configurações, usuários e permissões. Poucas pessoas.

## 5. Regras de cuidado

1. **Menor acesso que resolve.** Comece restrito e amplie quando a equipe pedir.
2. **Dados sensíveis:** Dashboard Financeiro exige FINANCEIRO → VIEW. Logs de
   auditoria só admin/gestor. Exportação/portabilidade de dados do paciente
   (LGPD, #599, chegando) só para admin/DPO.
3. **Sessão única:** cada pessoa com o seu login — senha compartilhada quebra o
   log de auditoria (e o sistema derruba a outra sessão).
4. **Profissional de saúde = ativo com conselho.** Colaborador sem conselho é
   administrativo: não tem grade e não entra na aba Colaboradores do convênio.
   Ver [../negocio-clinica/profissional-de-saude.md](../negocio-clinica/profissional-de-saude.md).
5. **Senha inicial** criada pela IA fica registrada **só** em `credenciais/` do
   repo privado da clínica; oriente cada pessoa a trocar no primeiro acesso
   (`/portal/minha-conta`).
6. Roadmap: MFA obrigatório e bloqueio de conta (#602) ainda não estão em produção.
