# S09 — Colaboradores e logins

> **Fonte:** https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-9 · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-9 · spec `openapi-2026-09-25.json` (`POST /colaboradores`, `/colaboradores/bulk`, `POST /colaboradores/{id}/usuario`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (criação de login pela API externa desde 24/09/2026) · **Kit:** v0.1.0

## Objetivo

Cada pessoa que atende ou usa o sistema existe como colaborador — profissionais
de saúde com conselho e especialidade certos, e a equipe de apoio — e quem vai
entrar no sistema tem **login criado** e senha inicial registrada no repo
privado. Perfis e permissões ficam na S14; grade horária, na S10.

## Link do manual

- Etapa 9: https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-9
- Tela: https://www.rabisistemas.com.br/manual/modulos/configuracoes.html#colaboradores
- CBO: https://www.rabisistemas.com.br/manual/modulos/configuracoes.html#colaboradores-cbos
- Pela API: https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-9

## Depende de

S01 (unidades onde atua). Especialidades do catálogo: IDs anotados pela tela
(S00). Conselhos: `GET /auxiliares/conselhos-profissionais`. UF (ID):
`GET /auxiliares/unidades-federativas`. Sexo: `GET /auxiliares/sexos`.

## Documentos a pedir

PE-1 (profissionais), PE-3 (quem usa o sistema), PE-4 (repasse — se já souber,
entra aqui; senão S12), SA-3.

## Índice de dados a coletar

| dado | campo API | obrigatório? | onde costuma estar no material do cliente | padrão sugerível | pergunta ao usuário se faltar |
|---|---|---|---|---|---|
| Nome completo | `nome` | sim | lista de RH, contrato, carimbo | — | — |
| CPF | `cpf` | sim | lista de RH, cadastro no conselho | — | "Qual o CPF de <nome>?" |
| Data de nascimento | `dataDeNascimento` | sim | lista de RH | — | "Qual a data de nascimento de <nome>?" |
| Sexo | `sexoId` | sim | lista de RH | — | — |
| Telefone | `telefone` | sim | lista de RH | — | "Qual telefone de contato de <nome>?" |
| Celular | `celular` | sim | lista de RH | — | idem |
| E-mail | `email` | sim | lista de RH | — | "Qual e-mail de <nome>? Ele também será o login." |
| Endereço (CEP, logradouro, número, bairro, cidade) | `endereco.*` | sim | lista de RH | pelo CEP | "Qual o CEP de <nome>?" |
| UF do endereço | `endereco.unidadeFederativa` | sim | idem | **nome por extenso** | — |
| Unidades onde atua | `empresas` (IDs) | não (recomendado) | escala | todas, se só há uma | "Em quais unidades <nome> atende?" |
| Conselho (CRM, CRO, CRP…) | `conselho[]`: `uf` (ID), `descricao`, `registroConselho` | não, mas obrigatório para profissional de saúde na prática | carimbo, receituário, site do conselho | — | "Qual o número do conselho de <nome>, e de qual estado?" |
| Especialidade | `especialidades[]`: `especialidadeId` (ID do catálogo, texto), `conselhoProfissionalId`, `numeroConselho`, `uf` (ID) | sim, se enviar especialidade | carimbo, RQE, lista de RH | — | "Qual a especialidade de <nome>?" |
| RQE | `especialidades[].rqe` | não | carimbo, site do conselho | — | — |
| Faixa etária atendida | `idadeMinimaAtendimento`, `idadeMaximaAtendimento` | não | regra da clínica | em branco | só se a clínica restringir |
| Anamnese/evolução padrão | `anamnesePadrao`, `evolucaoPadrao` | não | modelos do profissional | em branco | — |
| Cor na agenda | `corNaAgenda` | não | — | automática | — |
| Repasse | `vinculoRepasse` (`tipoVinculo`, `servicos[]`/`produtos[]`/`taxas[]` com `valorPercentual`, `valorMonetario`, `tipoCalculo`) | não | PE-4 | — | ver S12 |
| **Login: e-mail** | `POST /colaboradores/{id}/usuario` → `email` | sim, para quem usa o sistema | PE-3 | o e-mail do cadastro | — |
| **Login: senha inicial** | idem → `senha` (mínimo 8 caracteres) | sim | — | gerada pela IA, forte, trocada no 1º acesso | — |
| Nome/sobrenome do login | `primeiroNome`, `sobrenome` | não | — | tirados do nome | — |

O **CBO** (Classificação Brasileira de Ocupações) acompanha a especialidade na
tela. Confira o código com cuidado: há casos de CBO trocado entre especialidades
parecidas. Na dúvida, "não tenho certeza" + pergunta.

## Fila de perguntas

1. Confirmar a lista de pessoas (profissionais + equipe de apoio que usa o
   sistema) — PE-1 + PE-3.
2. Para cada profissional: conselho, número, UF e especialidade (confirmar o
   extraído; pedir o que falta), **uma pessoa por vez**.
3. Para a equipe de apoio: dados obrigatórios (CPF, nascimento, contato, endereço).
4. Quem precisa de login (normalmente: todos da PE-3).
5. Repasse: se já veio PE-4, confirmar; se não, deixar para a S12.

## Enriquecimento possível

- **CEP → endereço.**
- Número de conselho e RQE: consulta pública do conselho de classe, se a sessão
  tiver internet — confirmar.
- Validar CPF (dígito verificador) antes da prévia.

## Leitura do que já existe no Rabi e regra de não perder nada

- `GET /colaboradores` (todas as páginas, ativos e inativos) — casar por **CPF**
  e por nome normalizado. **Nunca duplicar:** profissional duplicado quebra
  agenda, faturamento e vínculos com convênio.
- Colaborador existente: GET completo antes de corrigir (PUT sobrescreve).
- Login: `409` em `POST /colaboradores/{id}/usuario` = **já tem login**. Não é
  erro: anote "login já existia".

## Gravação

| Ordem | Rota | Permissão | Lote |
|---|---|---|---|
| 1 | `POST /colaboradores` (o primeiro) | `colaborador:create` | — |
| 2 | `POST /colaboradores/bulk` | `colaborador:create` | até 50, depois do 1º provado |
| 3 | `POST /colaboradores/{id}/usuario` (`email`, `senha` ≥ 8) — um por pessoa | `colaborador:update` | sem lote |
| Correção | `GET /colaboradores/{id}` → `PUT /colaboradores/{id}` completo | `colaborador:update` | — |

- `POST /colaboradores` **só cadastra**: não cria acesso. O acesso é o passo 3.
- Senha inicial: gerada pela IA (8+ caracteres, letras e números), registrada
  **em texto claro** em `credenciais/CREDENCIAIS.md` do repo **privado** (seção
  "Usuários do Rabi": pessoa, e-mail, senha inicial, data, "trocar no 1º
  acesso"). Nunca em prova, issue, daily ou mensagem.
- A prévia do login mostra **quem** recebe acesso — não mostra a senha na conversa;
  ela é entregue pelo arquivo de credenciais.
- Guardar `colaboradorId` (aba Colaboradores do convênio, grade, `responsavelId`
  das escritas operacionais).

## Prova

- `provas/S09/colaborador-<slug>/` (sem necessidade de repetir o CPF no diff:
  mostrar só os campos que mudaram).
- Login: `resposta.json` do 201/409 **sem a senha**; conferência de que o
  colaborador passou a ter login (releitura do colaborador, quando mostrar) e o
  teste de entrada fica para a S14 (cada perfil loga e vê só o que deve).
- Review: pessoa, função, conselho/especialidade, unidades, login (sim/não).

## Armadilhas desta sprint

- UF **por extenso** no endereço; `uf` do conselho e da especialidade é **ID**.
- `especialidadeId` vem do catálogo de especialidades, que não tem listagem na
  API externa: anotar pela tela.
- Senha com menos de 8 caracteres → 400.
- A recepcionista também precisa ser colaboradora para ter login (o usuário
  nasce do colaborador).
- Colaborador com agendamento futuro avisa ao ser inativado — não inative sem
  decisão.
- Dados pessoais de colaboradores só no repo **privado**.

## Definition of Ready / Definition of Done

**DoR:** PE-1 e PE-3 recebidos (ou dados confirmados); IDs de especialidades.

**DoD:**
- [ ] todo colaborador existe uma vez só (por CPF), lido de volta;
- [ ] conselho, número, UF e especialidade conferidos nos profissionais de saúde;
- [ ] login criado para cada pessoa que usa o sistema (ou 409 = já tinha);
- [ ] senhas iniciais registradas em `credenciais/` (repo privado);
- [ ] IDs no dicionário; provas salvas.

## Checklist de itens

| # | item | status | origem | prova | observação |
|---|---|---|---|---|---|
| S09-01 | Lista de pessoas confirmada (profissionais + apoio) | pendente | | | |
| S09-02 | Colaborador <nome> (uma linha por pessoa) | pendente | | provas/S09/ | |
| S09-03 | Conselhos e especialidades conferidos | pendente | | | |
| S09-04 | Lista de quem recebe login aprovada | pendente | | | |
| S09-05 | Login de <nome> criado (uma linha por pessoa) | pendente | | | senha só em credenciais/ |
| S09-06 | Senhas iniciais registradas em credenciais/ | pendente | | | |
| S09-07 | Repasse coletado (ou adiado para S12) | pendente | | | |
| S09-08 | Dicionário de IDs (colaboradorId) | pendente | | | |

## O que registrar

- `dados/pessoas/colaboradores.md` (sem expor em relatório público).
- `credenciais/CREDENCIAIS.md` (logins e senhas iniciais).
- `decisoes/DECISOES.md`: quem recebeu login.
- `ESTADO.md`: próximo passo = S10.
