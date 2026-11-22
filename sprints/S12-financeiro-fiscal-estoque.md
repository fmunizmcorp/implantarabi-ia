# S12 — Financeiro, fiscal e estoque

> **Fonte:** https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-12 · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-12 · https://www.rabisistemas.com.br/manual/implantacao/pre-requisitos.html#fase5 · spec `openapi-2026-09-25.json` (`/estoque/*`, `/depositos`, `/parametros/financeiro|estoque`, `/nfse/*`, `PUT /colaboradores/{id}`) · **Conferido em:** 2026-09-25
> **Vale para:** produção; NFS-e: 1ª fase em produção (módulo opt-in, com taxa); modelos de nota, gestão de notas e onboarding fiscal concluídos no desenvolvimento em 17/09/2026 e chegando nas atualizações — confirmar no ambiente · **Kit:** v0.1.0

## Objetivo

O dinheiro que entra e sai tem para onde ir (contas/caixas, tipos e categorias
de pagamento, centros de custo), o repasse de cada profissional está definido,
a nota fiscal está resolvida (módulo ativado e configurado **ou** decisão de não
usar registrada) e, se a clínica usa estoque, depósitos, saldo inicial e custos
estão lançados — o que também tira os roxos de "falta de custo" do Farol.

## Link do manual

- Etapa 12: https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-12
- Financeiro: https://www.rabisistemas.com.br/manual/modulos/financeiro.html#tipos-pagamento · https://www.rabisistemas.com.br/manual/modulos/financeiro.html#categorias · https://www.rabisistemas.com.br/manual/modulos/financeiro.html#centro-custo
- Fiscal: https://www.rabisistemas.com.br/manual/modulos/configuracoes.html#config-fiscal
- Estoque: https://www.rabisistemas.com.br/manual/modulos/estoque.html#depositos · https://www.rabisistemas.com.br/manual/modulos/estoque.html#ordem-implantacao-depois
- Pela API: https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-12

## Depende de

S01 (unidades), S06 (produtos), S09 (colaboradores — repasse e `responsavelId`).

## Documentos a pedir

DI-1 (contas e caixas), DI-2 (formas de pagamento e taxas de cartão), DI-3
(plano de contas, categorias, centros de custo), DI-4 (dados fiscais), PE-4
(repasse), DD-3 (contagem de estoque), FA-4 (notas fiscais: valor de compra).

## Índice de dados a coletar

### Financeiro (a maior parte é feita **pela tela** — a API externa não cria)

| dado | campo API | obrigatório? | onde costuma estar no material do cliente | padrão sugerível | pergunta ao usuário se faltar |
|---|---|---|---|---|---|
| Tipos de conta | tela (Financeiro → Tipos de Conta) | sim p/ contas | — | Caixa, Conta bancária, Conta digital | — |
| Contas e caixas | tela (Financeiro → Contas e Caixas) | sim | DI-1 | "Caixa Recepção — <unidade>" | "Em qual conta entra o dinheiro dos convênios? E o do particular?" |
| Tipos de pagamento | tela (Financeiro → Tipos de Pagamento) | sim | DI-2 | Dinheiro, PIX, Cartão de débito, Cartão de crédito, Transferência | "Quais formas de pagamento a clínica aceita?" |
| Taxa e prazo do cartão | tela (tipo de pagamento) | não | contrato da maquininha | — | "Qual a taxa da maquininha no débito e no crédito à vista? Em quantos dias cai?" |
| Categorias de pagamento | tela (Financeiro → Categorias) | sim p/ lançamentos | DI-3 | Consultas, Procedimentos, Material, Salários, Aluguel | — |
| Centros de custo | tela (Financeiro → Centro de Custo) | não | DI-3 | por unidade/setor (rede) | "A clínica separa as despesas por setor ou unidade?" |
| Limites e padrões financeiros | `PUT /parametros/financeiro`: `limiteMaximoRecebimento`, `limiteMaximoPagamento`, `valorMinimoParcela`, `categoriaPagamentoId`, `centroDeCustoId` | não | regra interna | — | — |
| **Repasse por profissional** | `vinculoRepasse` no colaborador (`tipoVinculo`; `servicos[]`/`produtos[]`/`taxas[]` com `valorPercentual`, `valorMonetario`, `tipoCalculo`) — por `GET` + `PUT /colaboradores/{id}` completo | não | PE-4, contrato do profissional | — | "Como é o acerto com <nome>? Percentual, valor fixo por procedimento ou salário?" e "O percentual é sobre o valor cobrado ou sobre o que o convênio efetivamente paga?" |

### Fiscal (NFS-e)

| dado | onde | obrigatório? | onde costuma estar | padrão sugerível | pergunta se faltar |
|---|---|---|---|---|---|
| A clínica vai emitir NFS-e pelo Rabi? | decisão comercial (módulo opt-in, com taxa) | sim (decisão) | — | — | "A clínica quer emitir as notas pelo Rabi? É um módulo contratado à parte." |
| Inscrição municipal, regime, código de serviço, alíquota, provedor | tela (configuração fiscal da clínica) | se ativar | DI-4, contador | — | "Pode me passar o contato do contador ou os dados da nota que vocês emitem hoje?" |
| Emitentes e perfis fiscais (leitura) | `GET /nfse/emitentes`, `GET /nfse/perfis-fiscais` | — | — | — | — |

### Estoque completo (se a clínica usa)

| dado | campo API | obrigatório? | onde costuma estar | padrão sugerível | pergunta se faltar |
|---|---|---|---|---|---|
| Depósitos adicionais | `POST /depositos` (`empresaId`, `descricaoDeposito`) | não | DD-3 | "Farmácia", "Sala de Medicação" | "Além do Depósito Principal, a clínica guarda material em outro lugar?" |
| Saldo inicial por produto/lote | `POST /estoque/entrada`: `responsavelId`, `produtoId`, `localizacaoId` (= depósito), `motivoId` (de ENTRADA, ID só na tela), `quantidade`; e `valorCompra` (reais), `lote`, `validade`, `fornecedorId`, `notaFiscal`, `data`, `produtoEmCaixaQuantidade` | os 5 primeiros | DD-3 (contagem), FA-4 (nota) | — | "A contagem foi feita em que dia? Este é o saldo?" |
| Reserva de medicamento por paciente | `PUT /parametros/estoque` (`reservaMedicamentoAtiva`) | não | regra interna | desligada | — |

## Fila de perguntas

1. Formas de pagamento (confirmar padrão) → contas/caixas → categorias → centros
   de custo (cada um com o passo a passo de tela para o implantador).
2. Repasse: **uma pessoa por vez**, com a pergunta da base de cálculo
   (bruto × recebido) — é fonte comum de atrito com o profissional.
3. NFS-e: decisão; se sim, dados fiscais (via contador).
4. Estoque: usa? Se sim, contagem e data da contagem.

## Enriquecimento possível

- Valor de compra e fornecedor a partir das notas fiscais (FA-4).
- Categorias sugeridas a partir do plano de contas da contabilidade (DI-3).

## Leitura do que já existe no Rabi e regra de não perder nada

- `GET /parametros/financeiro` e `/estoque` (sem configuração, vêm reduzidos).
- `GET /depositos`, `GET /estoque/saldo-produtos` (confira o formato do
  envelope), `GET /estoque?produtoId=&localizacaoId=` (paginado).
- `GET /colaboradores/{id}` antes de gravar repasse (foto antes; o GET traz `vinculoRepasse` no formato do PUT).
- **Contas e caixas têm API desde 18/11/2026:** `GET /financeiro/contas-caixa` (filtro `numero`
  com ou sem pontuação, `busca`, `ativo`), `GET /financeiro/contas-caixa/tipos`,
  `POST /financeiro/contas-caixa` (sem `tipoDeContaId` = Conta Corrente; número repetido → 409
  com o id existente — complete pelo PUT) e `PUT /financeiro/contas-caixa/{id}` (grava só o
  enviado; `ativo: false` desativa, não há DELETE). Uso típico: completar agência e número das
  contas antigas. **Dados bancários só de documento do dono, destacados na prévia** (para onde
  vai o dinheiro). Categorias, tipos de pagamento e centros de custo seguem **sem leitura** na
  API externa: conferência na tela e IDs no dicionário.
- **Financeiro com padrão de controle** (12/10, #650): caixa por atendente nasce **Desligado**;
  as 9 ações novas de CONTAS CAIXAS não são dadas a ninguém automaticamente (incluir no perfil
  certo na S14). Pix/links e Asaas (13/10 e 06/11), NFS-e via NotaPlano por unidade (30/10;
  credenciais em Parâmetros › Integrações) e elegibilidade TISS (15/10) são **configuração do
  dono na tela** — a IA lista o que falta e não liga nada que cobre ou emita sozinho
  (`metodologia/licoes-de-implantacao-com-ia.md` §5–§6). Nota de teste é nota **real**.
- Depósito **inativo** recusa entrada/saída/transferência com 422 (21/10).

## Gravação

| Ordem | O que | Como | Permissão |
|---|---|---|---|
| 1 | Tipos de conta → contas/caixas → tipos de pagamento → categorias → centros de custo | **tela**, passo a passo dado pela IA | — |
| 2 | Parâmetros financeiros | `GET` → `PUT /parametros/financeiro` com **todos** os campos | `parametro:update` |
| 3 | Repasse por profissional | `GET /colaboradores/{id}` → `PUT` completo com `vinculoRepasse` | `colaborador:update` |
| 4 | NFS-e | ativação e configuração fiscal pela tela (decisão comercial) | — |
| 5 | Depósitos adicionais | `POST /depositos` | `deposito:create` |
| 6 | Saldo inicial | `POST /estoque/entrada` — **só com ordem escrita** (estoque real) | `estoque:create` |
| 7 | Parâmetros de estoque | `GET` → `PUT /parametros/estoque` | `parametro:update` |
| 8 | Reconferir os roxos da S11 | Farol relido | `convenio:read` |

- **Movimentação financeira** (`POST /financeiro/movimentacoes` e `/bulk`) pode
  **emitir NFS-e automaticamente**: não se usa na implantação, salvo migração de
  saldo decidida por escrito e com a configuração fiscal conferida antes.
- Entrada de estoque: primeiro 1 produto, provado; depois o resto, com a lista
  mostrada item a item.

## Prova

- Financeiro pela tela: `provas/S12/financeiro-tela.md` com o que foi criado
  (nome e ID) e a confirmação do implantador (print sem dado pessoal).
- Parâmetros e repasse: ritual normal.
- Estoque: saldo relido por depósito (`GET /estoque/saldo-produtos`) × contagem —
  diferenças **uma a uma**, sem arredondar nem "ajustar" por conta própria.
- Farol relido: roxos de falta de custo resolvidos.

## Armadilhas desta sprint

- `PUT /parametros/financeiro`: omitir `categoriaPagamentoId`/`centroDeCustoId`
  (ou mandar 0, "" ou false) grava `null` — reenvie tudo.
- Repasse é gravado **no colaborador** (quem procura em Financeiro não acha). O PUT do
  colaborador é parcial desde 01/10: `vinculoRepasse` só muda quando enviado, e as listas
  `produtos`/`servicos`/`taxas` enviadas substituem as atuais. Item com serviço/produto/taxa
  vazio = **linha geral** daquele tipo (no máximo uma por tipo, #643). O repasse entra no
  **custo do Farol** desde 12/10 — rode a conferência da S11 depois.
- NFS-e é opt-in e tem custo: sem o módulo, o cenário 7 da S15 é **escopo não
  contratado**, não teste reprovado.
- `valorCompra` em reais.
- `motivoId` de entrada e os IDs de contas/categorias só existem na tela.

## Definition of Ready / Definition of Done

**DoR:** S09 concluída; DI-1 e DI-2 (mínimo) recebidos.

**DoD:**
- [ ] contas/caixas, tipos e categorias de pagamento criados e conferidos na tela;
- [ ] centros de custo (se usar);
- [ ] repasse definido por profissional, com a base de cálculo escrita (ou `n/a`);
- [ ] NFS-e ativada e configurada **ou** decisão de não usar registrada;
- [ ] estoque: saldo conferido contra a contagem, com a data (ou `n/a`);
- [ ] roxos de falta de custo da S11 reconferidos; provas salvas.

## Checklist de itens

| # | item | status | origem | prova | observação |
|---|---|---|---|---|---|
| S12-01 | Tipos de conta e contas/caixas (tela) | pendente | | provas/S12/ | |
| S12-02 | Tipos de pagamento (tela) | pendente | | | |
| S12-03 | Categorias de pagamento (tela) | pendente | | | |
| S12-04 | Centros de custo (tela) | pendente | | | |
| S12-05 | Parâmetros financeiros | pendente | | | |
| S12-06 | Repasse de <profissional> (uma linha por profissional) | pendente | | | |
| S12-07 | Decisão sobre NFS-e | pendente | | | |
| S12-08 | Configuração fiscal (se ativar) | pendente | | | |
| S12-09 | Depósitos adicionais | pendente | | | |
| S12-10 | Saldo inicial lançado (ordem escrita) | pendente | | | |
| S12-11 | Parâmetros de estoque | pendente | | | |
| S12-12 | Roxos da S11 reconferidos | pendente | | | |

## O que registrar

- Dicionário de IDs (contas, categorias, centros de custo, motivos).
- `decisoes/DECISOES.md`: base do repasse, NFS-e sim/não, data da contagem.
- `ESTADO.md`: próximo passo = S13.
