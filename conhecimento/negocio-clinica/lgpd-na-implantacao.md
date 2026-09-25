# LGPD na implantação — como a IA trata dado pessoal e de saúde

> **Fonte:** Lei 13.709/2018 (LGPD) · https://www.rabisistemas.com.br/manual/regras-de-negocio/index.html#seguranca-compliance · `modulos/pacientes.html#lgpd-set-2026` · política do kit (`metodologia/politicas.md`, seções 3 a 5) · checklist de compliance usado numa operação real (generalizado) · **Conferido em:** 2026-09-25
> **Vale para:** toda sessão de implantação · **Kit:** v0.1.0

## 1. Por que importa

Clínica trata **dado pessoal** (nome, CPF, contato) e **dado pessoal
sensível** (saúde: diagnóstico, prontuário, medicamentos, carteirinha de plano).
A LGPD exige finalidade, necessidade (o mínimo), segurança e registro. A IA
implantadora vê esses dados pela API — e responde por não espalhá-los.

## 2. Regras da IA (sem exceção)

1. **Nenhum nome, CPF, data de nascimento, telefone, e-mail ou texto clínico
   de paciente** em prova, relatório, issue, log, mensagem ou commit. Use só o
   **identificador interno** (ID do Rabi) ou a matrícula/carteirinha quando o
   documento exige.
2. **Rotas de paciente e histórico de atendimento** (`/pacientes/*`,
   `/atendimentos/historico`) só com ordem escrita e finalidade clara (ex.:
   migração). Nunca "para ver como está".
3. **Migração de pacientes**: lotes pequenos, conferência **por amostra**,
   sem guardar extrato no repo. O `.gitignore` do repo da clínica bloqueia
   `dados/pacientes/`. Apague arquivos temporários ao fim.
4. **Não despeje JSON de paciente** no contexto da conversa: grave em arquivo
   temporário fora do repo e leia só contagens/resumos.
5. **Credenciais** (chave `rbk_`, senhas iniciais) só em `credenciais/` do repo
   **privado** da clínica. Confira que o repo é privado na abertura.
6. **Dados de profissionais** (CPF, conselho) também são pessoais: repo
   privado, nunca no kit.
7. **Documentos para fora** (recurso de glosa, e-mail a operadora): só o
   necessário; nada de prontuário inteiro.
8. **Kit público-seguro:** lição útil para outras clínicas vai ao mantenedor
   **sem** nenhum dado da clínica.

## 3. O que o Rabi oferece (para configurar e orientar)

| Recurso | Status (25/09/2026) |
|---|---|
| Logs de auditoria (quem fez o quê, quando) + tela de Auditoria (#185) | ✅ produção |
| Sessão única por usuário; SSO Keycloak | ✅ produção |
| Dados pessoais do paciente bloqueados para edição nas telas (#592) | ✅ produção |
| Permissões granulares (restringir quem vê o quê) | ✅ produção |
| Anonimização e exclusão sem apagar prontuário (#598) | 🔵 concluído no desenvolvimento, chegando |
| Exportação/portabilidade só para admin/DPO, com log (#599) | 🔵 chegando |
| Consentimento do paciente e do responsável legal (#600) | 🔵 chegando |
| Log de leitura do prontuário (#601) | 🔵 chegando |
| MFA obrigatório e bloqueio de conta (#602) | 🟠 roadmap |

## 4. Checklist LGPD da implantação (sugerir à clínica)

- [ ] Quem é o **encarregado (DPO)** da clínica? (registrar em `PAPEIS.md`)
- [ ] Perfis com **menor acesso** necessário; prontuário só para profissionais
      de saúde; exportação de dados só admin/DPO.
- [ ] Um **login por pessoa** (nada de usuário compartilhado).
- [ ] Termo de consentimento/ciência do paciente definido (quando o recurso
      chegar, configurar no Rabi).
- [ ] Notificações: conferir filtros antes de campanhas (dado de contato usado
      só para a finalidade informada).
- [ ] Anexos de pacientes classificados por tipo; nada de documentos pessoais
      em pastas compartilhadas fora do sistema.
- [ ] Repo da clínica **privado**; credenciais só lá.

A IA **aponta** riscos e sugere; decisões jurídicas e o texto de termos são da
clínica (com o seu jurídico). Não afirme artigo de lei sem ter conferido o texto.
