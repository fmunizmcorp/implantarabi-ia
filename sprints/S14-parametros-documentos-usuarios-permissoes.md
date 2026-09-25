# S14 — Parâmetros, documentos, usuários e permissões

> **Fonte:** https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-14 · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-14 · https://www.rabisistemas.com.br/manual/modulos/permissoes-granular.html#modelos · spec `openapi-2026-09-25.json` (`/parametros/*`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (permissões granulares entregues em 15/09/2026) · **Kit:** v0.1.0

## Objetivo

O sistema se comporta como a clínica trabalha (parâmetros), imprime os papéis
que ela usa (tipos de documento e de impressão), e cada pessoa entra com o
próprio usuário e vê **só o que a função precisa** (perfis e permissões
granulares) — testado em login real.

## Link do manual

- Etapa 14: https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-14
- Parâmetros: https://www.rabisistemas.com.br/manual/modulos/configuracoes.html#parametros
- Tipos de documento: https://www.rabisistemas.com.br/manual/modulos/configuracoes.html#tipos-documento
- Impressão: https://www.rabisistemas.com.br/manual/modulos/configuracoes.html#tipo-impressao
- Permissões granulares: https://www.rabisistemas.com.br/manual/modulos/permissoes-granular.html#modelos
- Pela API: https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-14
- Kit: [../conhecimento/sistema-rabi/perfis-e-permissoes.md](../conhecimento/sistema-rabi/perfis-e-permissoes.md)

## Depende de

S09 (colaboradores e logins) e, na prática, de todas as sprints anteriores
(parâmetros de orçamento, estoque e financeiro dependem do que existe).

## Documentos a pedir

DD-1 (modelos impressos), DD-2 (regras internas), DI-5 (desconto e alçada),
PE-3 (quem faz o quê).

## Índice de dados a coletar

### Parâmetros (API — sempre GET antes e objeto completo no PUT)

| dado | campo API | obrigatório? | onde costuma estar no material do cliente | padrão sugerível | pergunta ao usuário se faltar |
|---|---|---|---|---|---|
| Validade do orçamento (dias) | `PUT /parametros/orcamento` → `diasVencimento` | não | DD-2 | 30 | "O orçamento vale por quantos dias?" |
| Considerações do orçamento | `consideracoes` | não | modelo de orçamento (DD-1) | — | — |
| Régua do Farol | `parametroVermelho`, `parametroAmarelo`, aprovações | — | já feito na S11 | — | — |
| Descontos por nível (%) | `PUT /parametros/desconto` → `descontoNivel1..3`, `limiteParcelasDesconto` | não | DI-5 | — | "Até quantos % a recepção pode dar de desconto sem pedir a ninguém?" |
| Quem tem cada nível de desconto / alçada de compra | `POST /parametros/desconto/colaborador/{id}?nivel=` · `POST /parametros/alcada-compra/colaborador/{id}?nivel=` | não | DI-5 | — | "Quem pode aprovar descontos maiores?" |
| Acolhimento (documentos conferidos na chegada) | `PUT /parametros/acolhimento` | não | DD-2 | — | "A recepção confere algum documento do paciente na chegada? Quais?" |
| Termo de consentimento | `PUT /parametros/termo` → `conteudo` (obrigatório) | não | DD-1 | — | "A clínica usa termo de consentimento? Pode me mandar o texto?" |
| Avisos | `PUT /parametros/avisos/{chave}` (`AUTORIZACAO_VENCENDO`, `GRADE_PENDENTE_GUIA`, `GRADE_AUTORIZACAO_VENCENDO`) → `habilitado`, `limiar` | não | DD-2 | — | — |
| Serviços online (agendamento, confirmação…) | `PATCH /parametros/servicos-online/...` | não | DD-2 | desligados | "A clínica quer agendamento online pelo paciente?" |
| Dashboards por perfil | `PUT /parametros/dashboard-permissoes/*`, `/parametros/dashboard-atribuicao` (exigem `perfilPermissaoId`) | não | PE-3 | — | — |

### Documentos e impressão (tela)

| dado | onde | padrão sugerível | pergunta se faltar |
|---|---|---|---|
| Tipos de documento de atendimento (receita, atestado, laudo, encaminhamento) | Configurações → Tipos de Documento de Atendimento | modelos com as variáveis do sistema (ex.: nome do paciente, data, nome do profissional) no lugar dos campos variáveis | "Pode me mandar uma receita e um atestado que vocês usam hoje?" |
| Tipos de impressão (cabeçalho e rodapé) | Configurações → Tipos de Impressão | logo + dados da unidade | — |
| Kits de documentos (por convênio) | tela | — | — |

A IA monta o texto de cada modelo a partir do papel que a clínica já usa
(mantém o texto da clínica, troca só os campos variáveis) e entrega pronto
para o implantador colar na tela.

### Usuários, perfis e permissões (tela)

| dado | onde | padrão sugerível | pergunta se faltar |
|---|---|---|---|
| Logins | já criados na S09 (`POST /colaboradores/{id}/usuario`) | — | — |
| Perfis/grupos e permissões por funcionalidade e ação (Exportar, Imprimir, Autorizar, Cancelar, Estornar…) | Configurações → Colaboradores (usuários e perfis) — **não há rota na API externa** | matriz mínima por função (abaixo) | "Recepção pode cancelar agendamento? Pode dar estorno?" |

Matriz de partida (o manual indica e a clínica refina por ação):

| Perfil | Ponto de partida | Não deve ter |
|---|---|---|
| Administrador/gestor | tudo | — (restrito ao gestor) |
| Recepção | Agendamento (ver/criar/editar) + Pacientes (ver/criar/editar) + orçamento e recebimento | Configurações, custo, Farol, contratos, relatório financeiro |
| Profissional de saúde | Atendimento (criar) + Agendamento (ver) + Pacientes (ver) | Financeiro, contratos |
| Enfermagem | agenda, atendimento, estoque de uso | financeiro, contratos |
| Financeiro/faturamento | Financeiro + Faturamento + Relatórios (ver) | folha, configurações |

## Fila de perguntas

1. Regras internas (uma por mensagem): validade do orçamento, desconto por nível,
   quem aprova, acolhimento, termo, avisos, serviços online.
2. Modelos de documento: pedir os papéis que faltam.
3. Matriz de permissões: mostrar a matriz de partida; perguntar só as exceções.
4. Teste de login: combinar com cada pessoa (ou com o implantador) quando testar.

## Enriquecimento possível

- Transformar os modelos em papel (DD-1) em texto com variáveis, pronto para colar.
- Matriz de permissões gerada a partir de PE-3 (função de cada pessoa).

## Leitura do que já existe no Rabi e regra de não perder nada

- `GET` de cada parâmetro antes do PUT. Respostas-armadilha: `orcamento` pode vir
  como `0` cru; `acolhimento`, `servicos-online` e `termo` como `null` (200);
  `desconto` como 404 se nunca configurado; `desconto/colaborador/{id}` sem
  cadastro vem com `nivelAlcada: "NIVEL0"`. Nada disso é erro de chave.
- Perfis existentes: conferidos na tela com o implantador (print).

## Gravação

| Ordem | O que | Rota | Permissão |
|---|---|---|---|
| 1 | Parâmetros de orçamento, desconto, financeiro, estoque, acolhimento, termo, avisos, serviços online | `GET` → `PUT`/`PATCH /parametros/...` com o objeto completo | `parametro:update` |
| 2 | Nível de desconto e alçada de compra por colaborador | **pela tela** — pela API, hoje, falha sempre (defeito documentado: a chave nunca é tratada como administrador) | — |
| 3 | Tipos de documento, impressão, kits | tela, com o texto entregue pela IA | — |
| 4 | Perfis e permissões | tela, com a matriz aprovada | — |
| 5 | Dashboards por perfil | `PUT /parametros/dashboard-*` (com `perfilPermissaoId`) | `parametro:update` |
| 6 | Teste de login de **cada perfil** | a pessoa (ou o implantador) entra em app.rabisistemas.com.br com a senha inicial de `credenciais/` e confere o que vê | — |

- Só `/parametros/desconto` declara que campo omitido mantém o valor; mesmo
  assim, reenvie tudo.
- `PUT /parametros/termo` exige `conteudo`.

## Prova

- Parâmetros: ritual normal (`provas/S14/parametros-<nome>/`).
- Tela: `provas/S14/tela.md` com o que foi criado e a confirmação do implantador.
- Login: `provas/S14/logins.md` — por perfil: entrou (sim/não), vê o que deve
  (sim/não), não vê o que não deve (sim/não). **Sem senha no arquivo de prova.**

## Armadilhas desta sprint

- Dar Configurações para recepção ou Financeiro para profissional sem motivo
  escrito.
- PUT parcial de parâmetro gravando `null` em vínculos.
- Tentar gravar nível de desconto/alçada pela API (falha por defeito conhecido).
- `desabilitarBloqueioFarol` ligado "para facilitar": desliga todo bloqueio de
  margem — só com decisão escrita.
- Parâmetro de dashboard sem `perfilPermissaoId` na leitura.

## Definition of Ready / Definition of Done

**DoR:** logins criados (S09); DD-1 e DD-2 recebidos ou regras confirmadas.

**DoD:**
- [ ] cada parâmetro com resposta escrita da clínica, gravado e relido;
- [ ] todo documento que a clínica imprime existe como modelo;
- [ ] matriz de permissões aprovada e aplicada na tela;
- [ ] login testado em **cada perfil**; ninguém com permissão além do necessário;
- [ ] provas salvas.

## Checklist de itens

| # | item | status | origem | prova | observação |
|---|---|---|---|---|---|
| S14-01 | Parâmetros de orçamento (validade, considerações) | pendente | | provas/S14/ | |
| S14-02 | Descontos por nível | pendente | | | |
| S14-03 | Nível de desconto e alçada por colaborador (tela) | pendente | | | |
| S14-04 | Acolhimento | pendente | | | |
| S14-05 | Termo de consentimento | pendente | | | |
| S14-06 | Avisos e serviços online | pendente | | | |
| S14-07 | Tipos de documento de atendimento (tela) | pendente | | | |
| S14-08 | Tipos de impressão (tela) | pendente | | | |
| S14-09 | Matriz de permissões aprovada | pendente | | | |
| S14-10 | Perfis aplicados na tela | pendente | | | |
| S14-11 | Login testado — perfil <nome> (uma linha por perfil) | pendente | | | |

## O que registrar

- `dados/parametros.md` (valores decididos e origem).
- `dados/permissoes/matriz.md`.
- `decisoes/DECISOES.md`: regras internas e exceções de permissão.
- `ESTADO.md`: próximo passo = S15.
