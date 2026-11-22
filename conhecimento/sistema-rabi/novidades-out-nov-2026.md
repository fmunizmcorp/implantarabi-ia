# O que mudou no Rabi de 29/09 a 22/11/2026 — impacto na implantação

> **Fonte:** manual oficial (https://www.rabisistemas.com.br/manual/ — atualizacoes-2026, regras-de-negocio, api-externa, demandas D-37 a D-54, conferidas pela equipe do manual contra o código de produção `deploy_prd`) · Swagger de 22/11/2026 (`../api-externa/spec/openapi-2026-11-22.json`) · medição da API em 22/11 · **Conferido em:** 2026-11-22
> **Vale para:** produção em 22/11/2026 · **Kit:** v0.4.0

Leia antes de qualquer sprint se a clínica começou (ou parou) antes de novembro: várias telas e
regras mudaram. O que não tem data de produção aqui é **roadmap** — não prometa.

## 1. API externa (o que muda no trabalho da IA)

| Desde | O que mudou | Efeito no kit |
|---|---|---|
| 01–02/10 | **PUT parcial** (#634; rabi-api `7d16cd50`/`49362b61`) em serviços, **convênios**, orçamentos, pacientes (+carteira), colaboradores, grades, movimentações, guias e contas-caixa (18/11): omitido mantém · `null` limpa · lista omitida mantém · **lista enviada substitui** (`[]` apaga) | [convencoes.md §4](../api-externa/convencoes.md) e FAQ F004 reescritas |
| 02/10 | Token `rbt_` com permissões **editáveis** (sem trocar o valor), validade 30/90/365 dias ou sem; 403 traz `escopoFaltante` | [chave-e-token.md](../api-externa/chave-e-token.md), FAQ F008 |
| 02/10 | Inativar produto/taxa usado em serviço ativo → **409** com a lista (#626) | FAQ F007 |
| 13/10 | Serviço: campos `documentos` (documentos obrigatórios) e `perfilFiscalId`; o GET do serviço passa a trazer produtos, equipamentos, taxas e documentos com os nomes do PUT | S08; `corpo_escrita.py` |
| 13/10 | Produto: `codigoEAN` texto 8/12/13/14 dígitos, `codigoNCM` texto 8 dígitos (número perde zero à esquerda), `codigoProduto` até 10 caracteres (TISS); `priceType1..3` em **reais** nas duas rotas da tabela interna | S06; `corpo_escrita.py` avisa |
| 13/10 | Repasse do colaborador: item vazio = **linha geral** daquele tipo (no máximo uma por tipo) (#643) | S09 |
| 13/10 | Paciente: `nomeSocial` (o `nome` é o nome civil) | S13 |
| 13/10–19/11 | Rotas novas: `POST /financeiro/pagamentos/confirmacao`, `POST /financeiro/xml-tiss`, `.../casar-historico`, `/financeiro/contas-caixa` (5 operações) — Swagger 277 operações | contas-caixa entra na S12; as de dinheiro são [proibidas sem ordem](../api-externa/proibidas-sem-ordem-escrita.md) |
| 22/11 (medido) | Chave/token rejeitado = **401** "Token de integração inválido, revogado ou expirado." (até 25/09 era 503) | FAQ F003, `cliente.py` |

## 2. Convênio, preços e Farol

- **Tela do convênio em modo visualização** (29/09, #632) — Liberar para edição → alterar → Salvar
  no cabeçalho; desde 01/10 as abas Planos, Especialidades, Produtos, Serviços e Taxas ficam em
  **rascunho até o Salvar** (Colaboradores, Custos extras, Farol e Dados Fiscais ficam fora); botão
  **Histórico** por subaba (#638). Ações em massa (Selecionar/Desmarcar todos, Copiar, Importar)
  gravam na hora. FAQ F011.
- **Ainda evitar na tela** (manual, 02/10): "Selecionar/Desmarcar todos" na aba Serviços só mexe no
  Utiliza, qualquer que seja a coluna escolhida; **não usar "Copiar convênio"** até o Rabi confirmar
  a correção. Defeitos que apagavam valor convertido, autorização ou prazo ao salvar foram corrigidos
  em 02/10 (#639/#654).
- **Coluna Atende** (#628): serviço de especialidade que o convênio não atende fica "Não atendida" e
  não aceita Utiliza. A trava no agendamento/orçamento está **desligada desde 06/10** (temporário),
  mas segue valendo no cadastro do convênio, na API externa e na IA de atendimento (TalkMe) —
  **cadastre as especialidades do convênio** de qualquer jeito.
- **Farol com todos os custos** (12/10, #655): custo = produtos + custo extra do convênio +
  prestadores ("Serviços extras") + repasse do profissional (sem profissional definido, o **maior**
  repasse entre quem atende o serviço e aceita o convênio). Sem cor só com custo total 0; roxo com
  produto de custo 0; no limite exato do vermelho = amarelo. O bloqueio pelos custos novos nasce
  **desligado** (Parâmetros › Orçamento › "Custos extras … também bloqueiam"; antes, botão "Ver
  serviços que mudam de cor"). **Consequência na ordem:** a conferência do Farol (S11) fica completa
  só **depois** de cadastrar repasses e custos extras.
- **Referências oficiais de produto — 1ª fase** (15/10, #662): menu Estoque › Referências oficiais
  (SIMPRO, Brasíndice, CMED, TUSS…), aba no produto (código na publicação, fator de conversão) e,
  no convênio (aba Dados), o bloco **Referências oficiais por tipo de produto**. Nasce o **nível 2**
  da cadeia do produto: conversão do produto no convênio > **referência oficial** > política de
  preço/cadastro. Sem esse bloco no convênio, nada muda. A **importação por planilha foi retirada
  da tela** em 15/10 — carga de preços do nível 2 hoje depende do time Rabi. O simulador do kit
  **não modela o nível 2**: em convênio com o bloco preenchido, confie no Farol real
  ([../precos-e-conversao/04-arvore-produto-politica-fatork.md](../precos-e-conversao/04-arvore-produto-politica-fatork.md)).
- **IA de atendimento (TalkMe) e painel de disponibilidade consideram o Farol** (14/10, #664): o
  que o Farol bloqueia ou que exige aprovação não é oferecido pela IA. Um serviço só aparece para a
  IA quando **tudo** fecha: profissional com a especialidade, grade ativa com o serviço aceitando o
  convênio, especialidade "Atende" no convênio, Utiliza no serviço, convênio ativo na unidade e Farol
  liberado (#659/#664).
- Conta de recebimento do convênio é **obrigatória** para gerar contas a receber (12/10).

## 3. Agenda, orçamento e financeiro

- **Grade recusada em consultório ocupado** no mesmo dia/horário (18/11, #707) — FAQ F009.
- **Inativar grade realoca os agendamentos futuros** dela (21/11, #708 parte 1). Inativar/reativar
  colaborador sem perder grades = roadmap.
- **Orçamento:** aprovação da assistência (equipe clínica com registro de conselho) obrigatória
  para agendar (18/11, #705); status automáticos (Pago, Agendado, Concluído, Renegociado, Vencido)
  já aparecem, mas a troca automática está **desligada** em produção (#656, conferido 05/11).
- **Financeiro com padrão de controle** (12/10, #650): caixa por atendente (nasce **Desligado**),
  comprovantes, estorno, conciliação por OFX; as 9 ações novas de CONTAS CAIXAS **não são dadas a
  ninguém** automaticamente — incluir no perfil certo na S14.
- **Pix/links de pagamento** (13/10) e Asaas na conta da clínica (06/11) — configuração do dono.
- **NFS-e via NotaPlano por unidade** (30/10), credenciais em Parâmetros › Integrações (03/11):
  configuração fiscal é do dono; **nota de teste é nota real**.
- **Elegibilidade TISS** (15/10, #619): Configurações › integração TISS por operadora + Log de
  integração; permissões TISS_INTEGRACAO / TISS_ELEGIBILIDADE. Envio de lote, autorização e recurso
  por webservice (#620–#623) = roadmap.
- Receituário controlado (SNCR, 22–23/10), alergias e documentos assinados pelo profissional
  (28/10), Memed (30/10) — telas do atendimento; não fazem parte da carga da implantação.

## 4. Defeitos e cuidados que pedem conferência

- **Sexo gravado invertido pela tela até 30/10.** Pacientes cadastrados ou editados pela tela antes
  disso: conferir por amostra (S13) — sem copiar dado pessoal para o repo.
- **Migrações do banco rodam por clínica** e podem falhar numa só (mesma causa do 400 genérico de
  28/09 — FAQ F002). Depois de cada atualização do Rabi, área inteira com 400 = suporte.
- Serviços e pacientes gravados por **PUT antes de 01/10** seguiram a regra antiga (omitido apagava):
  conferência única na FAQ F006.
- Erro técnico na tela agora aparece como "Ocorreu um erro inesperado… (código XXXX)" — peça o
  código ao usuário quando ele relatar erro de tela (13/10).
- Administrador não troca senha/e-mail de quem tem acesso a outra clínica (13/10) — o próprio
  usuário usa "Esqueci minha senha".
- MFA (#602) existe, mas **não é obrigatório**.

## 5. Roadmap (não prometer)

Catálogo de atendimento em tela (#659), status automático do orçamento ligado (#656),
TISS fases 2–4 (#620–#623), app nas lojas (#661/#689), Open Finance (#651, desligado),
#708 completo, importação de referências oficiais por arquivo de cada editora.
