# Profissional de saúde — conselho, CBO, RQE, agenda e convênio

> **Fonte:** https://www.rabisistemas.com.br/manual/modulos/configuracoes.html#colaboradores-cbos · `implantacao/guia-implantacao.html#etapa-9` · Swagger da API externa (schema `ColaboradorEspecialidadeInput`) · regra de negócio definida numa implantação real (generalizada) · TUSS Tabelas 24 e 26 (ANS) · **Conferido em:** 2026-09-25
> **Vale para:** Rabi em produção em 25/09/2026 · **Kit:** v0.1.0

## 1. A regra

Entre os colaboradores **ativos**, **profissional de saúde é só quem tem
conselho profissional cadastrado** (CRM, COREN, CRN, CREFITO, CRP, CRF, CRBM…).

| Situação | É profissional de saúde? | Tem grade (agenda)? | Entra no convênio (aba Colaboradores)? |
|---|---|---|---|
| Ativo **com** conselho + especialidade | Sim | Sim | Sim, nos convênios em que atende |
| Ativo **sem** conselho | Não — é **administrativo** (recepção, faturamento, apoio) | Não | **Não** |
| Inativo | Não entra em nada | Não | Não |
| Não cadastrado | Não cadastrar por conta própria — perguntar | — | — |

Em uma implantação real, administrativos (e até um usuário de teste do
desenvolvimento) estavam marcados como "atende" em convênios — foi preciso
desmarcar. Profissional com conselho mas **número do conselho em branco** é
erro de cadastro a corrigir (a guia exige número e UF).

## 2. O que cadastrar por profissional

| Campo | Por quê | Na API (`ColaboradorEspecialidadeInput`) |
|---|---|---|
| Nome, e-mail único (vira o login) | Identificação e acesso | colaborador |
| Empresa principal / unidades | Onde atende | colaborador |
| **Especialidade(s)** | Uma pessoa pode ter várias | `especialidadeId` |
| **Conselho** (sigla, Tabela 26) | Vai na guia | `conselhoProfissionalId` |
| **Número do conselho** + **UF** | Vai na guia | `numeroConselho`, `uf` |
| **RQE** (registro de qualificação de especialista) | Exigido por algumas operadoras para especialista | `rqe` |
| Idade mínima/máxima atendida | Evita agendar criança com quem não atende | `idadeMinimaAtendimento`, `idadeMaximaAtendimento` |
| Anamnese/evolução padrão | Agiliza o prontuário | `anamnesePadrao`, `evolucaoPadrao` |
| Percentual de repasse | Relatório de Repasses | colaborador |
| **Grade horária** | Define horários agendáveis | grade de colaborador |
| Login | Acesso ao sistema | `POST /colaboradores/{id}/usuario` (409 = já tem) |

## 3. CBO (o "CBOS" do Rabi)

O código **CBO** da especialidade vai na guia e é **obrigatório** para faturar
convênio. Códigos confirmados no manual do Rabi:

| Especialidade | CBO |
|---|---|
| Clínica geral | 225125 |
| Cardiologia | 225120 |
| Pediatria | 225124 |
| Ginecologia e obstetrícia | 225250 |
| Fisioterapia | 223605 |
| Psicologia (clínica) | 251510 |
| Nutrição | 223710 |

Outros vistos em fonte da implantação real: médico geneticista 225175.
⚠️ Atenção a trocas comuns: **225105 é médico acupunturista**, não clínico
geral. Para qualquer outra especialidade (infectologia, dermatologia,
reumatologia, enfermagem etc.), **confira o código na Tabela 24 (CBO) da TUSS
vigente** antes de gravar — não use de memória.

No convênio, o **credenciamento por CBO** define quem aparece no agendamento
daquele convênio: só especialidades credenciadas. A lista de especialidades
credenciadas vem do **contrato** (evidência tripla — ver
[analise-de-contratos.md](analise-de-contratos.md)).

## 4. Perguntas da IA na sprint de colaboradores

1. "Me envie a lista da equipe: nome, função, e-mail e, para quem atende,
   conselho + número + UF + especialidade + RQE." (planilha ou foto de
   documento servem)
2. "Quem atende convênio e quais convênios? Alguém atende só particular?"
3. "Idade mínima/máxima de atendimento de cada um?"
4. "Horários de atendimento de cada profissional (dias, horas, local)?"
5. "Percentual de repasse?" (se a clínica usa)
6. "Quem precisa de login e com qual perfil?" (ver
   [../sistema-rabi/perfis-e-permissoes.md](../sistema-rabi/perfis-e-permissoes.md))

## 5. Regras de cuidado

- Confira **ativo/inativo** antes de mexer em qualquer colaborador.
- Não mexa na aba Colaboradores de convênio sem aprovação item a item.
- Dados de profissional (CPF, conselho) são pessoais: ficam no repo privado da
  clínica, nunca em prova pública ou issue do kit.
- Enfermagem costuma atender em todos os convênios (aplicações); médicos,
  nutrição e fisioterapia variam por contrato — pergunte.
