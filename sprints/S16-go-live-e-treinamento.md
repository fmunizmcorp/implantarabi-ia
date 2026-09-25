# S16 — Go-live e treinamento

> **Fonte:** https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#go-live · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#checklist-final · checklists de go-live dos três modelos por porte · **Conferido em:** 2026-09-25
> **Vale para:** produção · **Kit:** v0.1.0

## Objetivo

A clínica entra em operação numa data definida, com a equipe treinada por
perfil, todos os acessos ativos, a base conferida, o manual divulgado e o
acompanhamento da primeira semana agendado. A chave de implantação é revogada
ou reduzida ao que a integração contínua precisa.

## Link do manual

- Etapa 16 (go-live): https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#go-live
- Checklists por porte: https://www.rabisistemas.com.br/manual/implantacao/foco-consultorio-individual.html#checklist · https://www.rabisistemas.com.br/manual/implantacao/foco-clinica-pequena-media.html#checklist · https://www.rabisistemas.com.br/manual/implantacao/foco-clinica-rede.html#checklist
- Fechamento pela API: https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#checklist-final
- Manual do operador (treinamento): https://www.rabisistemas.com.br/manual/operador/manual-operador.html

## Depende de

S15 fechada, sem cenário reprovado e sem pendência bloqueante.

## Documentos a pedir

PE-3 (quem vai ser treinado). Nenhum outro.

## Índice de dados a coletar

| dado | campo API | obrigatório? | onde costuma estar no material do cliente | padrão sugerível | pergunta ao usuário se faltar |
|---|---|---|---|---|---|
| Data oficial de entrada em produção | — | sim | conversa | o 1º dia útil depois da S15 | "Qual dia a clínica começa a atender pelo Rabi?" |
| Agenda de treinamento por perfil | — | sim | PE-3 | recepção ~2 h · profissionais ~1 h · faturamento ~3 h · gestão ~1h30 | "Quando cada grupo pode parar para o treinamento?" |
| Contato de suporte na 1ª semana | — | sim | — | o implantador | "Quem a equipe chama se tiver dúvida na primeira semana?" |
| Destino da chave de implantação | — | sim | — | revogar ou reduzir | "Depois do go-live, a clínica vai manter alguma integração pela API? Se não, a chave de implantação deve ser revogada." |

## Fila de perguntas

1. Data do go-live.
2. Agenda dos treinamentos por perfil.
3. Contato de suporte e horário da varredura diária.
4. Destino da chave.

## Enriquecimento possível

- Material de treinamento **com as telas e os dados da própria clínica** (nomes de
  salas, serviços, convênios reais — nunca dados de pacientes), a partir do
  manual do operador e das rotinas do manual.
- Roteiro por perfil (do manual):
  - **Recepção:** login e navegação; cadastro de paciente e convênio; criar e
    editar agendamento; confirmação em massa; acolhimento e check-in; busca e
    histórico.
  - **Profissionais:** fila de atendimento; prontuário; procedimentos; documentos
    (atestado, receita, laudo); finalizar atendimento; histórico.
  - **Financeiro/faturamento:** registros financeiros; caixas e contas;
    pré-faturamento; fechamento de lote; glosas; relatórios e fluxo de caixa.
  - **Gestão:** dashboard; relatórios gerenciais; configurações; usuários e
    permissões; logs de auditoria; e — para a clínica — Farol, custo e reajuste.

## Leitura do que já existe no Rabi e regra de não perder nada

Checklist de go-live percorrido **com prova** de cada linha:

- todo convênio ativo, com preço conferido (S10b/S11);
- agenda aberta para as próximas 4 semanas (grades, S10);
- todo usuário consegue entrar (S14);
- estoque com saldo real na data da virada (S12, se usa);
- financeiro com conta e forma de pagamento prontos (S12);
- documentos e termos imprimindo (S14);
- parâmetros definidos (S14);
- base de pacientes conferida por amostragem (S13);
- **foto do estado inicial** de todas as áreas (como na S00) guardada no repo
  em `provas/S16/foto-go-live/` — sem dado de paciente.

## Gravação

Nenhum cadastro novo por padrão. Ações:

| O que | Como |
|---|---|
| Ativar o acesso de todos os usuários | já criados (S09) e testados (S14); entregar a cada pessoa **pelo canal que o dono escolher** a instrução de 1º acesso (a senha fica em `credenciais/`, não em mensagem pública) |
| Chave de implantação | o dono (ou o time Rabi) **revoga** no portal comercial ou reduz às permissões da integração contínua; a IA registra a data e, se houver chave de integração, a validade (`X-ApiKey-Expires-At`) com alerta de renovação |
| Divulgar o manual | https://www.rabisistemas.com.br/manual (o sistema fica em app.rabisistemas.com.br) |

## Prova

- `provas/S16/checklist-go-live.md` com cada linha: prova (arquivo) e resultado.
- `historico/reviews/S16-<data>.md`: data oficial, treinamentos (quem, quando —
  lista de presença sem dado sensível), contato de suporte.

## Armadilhas desta sprint

- Go-live com pendência bloqueante "para resolver depois".
- Senha inicial enviada em grupo de mensagens.
- Chave de implantação (com acesso a dinheiro, nota e estoque) esquecida ativa.
- Treinamento genérico: a equipe aprende melhor com as próprias salas, serviços
  e convênios.
- Rede: liberar todas as unidades juntas sem a piloto validada.

## Definition of Ready / Definition of Done

**DoR:** S15 fechada sem reprovação; data proposta.

**DoD:**
- [ ] checklist de go-live inteiro, com prova;
- [ ] data oficial registrada;
- [ ] treinamento por perfil dado, com presença registrada;
- [ ] acessos ativos; manual divulgado;
- [ ] chave de implantação revogada/reduzida (registrado);
- [ ] acompanhamento da 1ª semana agendado (S17).

## Checklist de itens

| # | item | status | origem | prova | observação |
|---|---|---|---|---|---|
| S16-01 | Data oficial de go-live definida | pendente | | | |
| S16-02 | Checklist de go-live com prova | pendente | | provas/S16/ | |
| S16-03 | Foto do estado inicial (go-live) | pendente | | | |
| S16-04 | Treinamento recepção | pendente | | | |
| S16-05 | Treinamento profissionais | pendente | | | |
| S16-06 | Treinamento financeiro/faturamento | pendente | | | |
| S16-07 | Treinamento gestão | pendente | | | |
| S16-08 | Acessos ativos e instruções de 1º acesso entregues | pendente | | | |
| S16-09 | Manual divulgado à equipe | pendente | | | |
| S16-10 | Chave de implantação revogada/reduzida | pendente | | | |
| S16-11 | Acompanhamento da 1ª semana agendado | pendente | | | |

## O que registrar

- `decisoes/DECISOES.md`: data de go-live, destino da chave.
- `credenciais/rabi-api-externa.md`: estado da chave (revogada em…, ou validade).
- `ESTADO.md`: modo = Implantação (estabilização); próximo passo = S17.
