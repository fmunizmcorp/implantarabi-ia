# S03 — Locais e tipos (tabelas básicas)

> **Fonte:** https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-3 · https://www.rabisistemas.com.br/manual/implantacao/pre-requisitos.html#fase2 · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-3 · spec `openapi-2026-09-25.json` (`POST /locais`, `GET /auxiliares/*`) · **Conferido em:** 2026-09-25
> **Vale para:** produção · **Kit:** v0.1.0

## Objetivo

Cada sala/consultório existe como **local**, apontando para o depósito ativo da
sua unidade; e as tabelas básicas ("tipos") que os cadastros seguintes usam
existem e têm os IDs anotados.

## Link do manual

- Etapa 3: https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-3
- Tipos (fase 2): https://www.rabisistemas.com.br/manual/implantacao/pre-requisitos.html#fase2
- Tela de locais: https://www.rabisistemas.com.br/manual/modulos/configuracoes.html#locais
- Pela API: https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-3

## Depende de

S02 (depósito **ativo** em cada unidade).

## Documentos a pedir

CL-4 (salas por unidade). Para os tipos: FA-1, FA-2, FA-3 (mostram que tipos de
serviço, taxa e produto a clínica usa).

## Índice de dados a coletar

### Locais (um por sala/consultório)

| dado | campo API | obrigatório? | onde costuma estar no material do cliente | padrão sugerível | pergunta ao usuário se faltar |
|---|---|---|---|---|---|
| Nome do local | `nome` | sim (único na unidade) | lista de salas, planta, escala da recepção | **"Consultório 1"**, "Consultório 2", **"Sala de Aplicação 1"**, "Sala de Exames 1" | "Quantos consultórios e salas a unidade <nome> tem? Posso chamá-los de Consultório 1, 2…?" |
| Unidade | `empresaId` | sim | S01 | — | — |
| Depósito padrão de saída | `depositoPadraoSaidaId` | sim (ativo) | S02 | o depósito mínimo da unidade | — |

### Tipos (tabelas básicas)

Pela API externa os tipos são **só leitura** (grupo Auxiliares). O que faltar é
criado **pela tela** pelo implantador, com o passo a passo dado pela IA; depois a
IA relê o auxiliar e anota o ID.

| Tipo | Leitura na API | Onde criar na tela | É usado em | Padrão sugerível (se não existir) |
|---|---|---|---|---|
| Tipos de Serviço | `GET /auxiliares/tipos-servico` | Configurações → Serviços → Tipos | S08 (`tipoServicoId`) | Consulta, Exame, Procedimento, Aplicação |
| Tipos de Taxa | `GET /auxiliares/tipos-taxa` | Configurações → Taxas → Tipos | S05 (`tipoTaxaId`) | Sala, Material, Aplicação |
| Tipos de Produto | `GET /auxiliares/tipos-produto` | Estoque → Produtos → Tipos de Produto | S06, S10a (política por tipo) | usar os que já vêm no sistema (Medicamento, Material Hospitalar…) |
| Tipos de Atendimento | `GET /auxiliares/tipos-atendimento` | Configurações → Tipo de Atendimento | S08, S10b (coluna Tipo de Atendimento) | Primeira consulta, Retorno, Urgência, Telemedicina |
| Tipos de Código | `GET /auxiliares/tipos-codigo` | Configurações → Tipos de Código | S05, S06, S08, S10b | TUSS, CBHPM, Próprio |
| Tabela 87 (ANS) | `GET /auxiliares/tabelas-ans87` | (domínio fixo) | S05, S06, S08, S10b | — (é a "tabela de tabelas" da TISS: diz de qual tabela vem o código do item) |
| Tipos de Guia / Regimes | `GET /auxiliares/tipos-guia`, `/regimes-atendimento` | (domínio) | S08 | — |
| Unidades de medida | `GET /auxiliares/unidades-medida` | tela, se faltar | S06 | — |
| Tipos de Anexo | **sem leitura na API** | Configurações → Tipos de Anexos | S13 (anexos do paciente) | Documento de identidade, Carteirinha, Pedido médico, Laudo |
| Tipos de Identificação | **sem leitura na API** | Configurações → Tipos de Identificação | S13 | RG, CNH, Passaporte |

Tipos de conta, de pagamento e categorias ficam na S12; tipos de documento de
atendimento e de impressão, na S14.

## Fila de perguntas

1. Confirmar a lista de locais por unidade (extraída de CL-4 ou sugerida).
2. Confirmar cada tipo **que falta** (mostrar os que já existem no Rabi e os que a
   clínica usa nos documentos; sugerir só o que falta).
3. Para cada tipo que falta: passo a passo de tela para o implantador, **um tipo
   por mensagem**, e pedido de "feito".

## Enriquecimento possível

- Deduzir os tipos necessários dos documentos (ex.: a tabela do convênio usa
  códigos TUSS e CBHPM → tipos de código TUSS e CBHPM).

## Leitura do que já existe no Rabi e regra de não perder nada

- `GET /locais` (lista) — casar por **nome normalizado + unidade**.
- `GET /auxiliares/*` (as 14 rotas) — não criar tipo que já existe com outro nome
  parecido; em dúvida, mostrar ao usuário os dois nomes.
- Local existente apontando para depósito inativo → propor correção (PUT
  completo do local), não criar outro.

## Gravação

| Ordem | Rota | Permissão | Lote |
|---|---|---|---|
| 1 | Tipos que faltam: **pela tela** (implantador) | — | — |
| 2 | Reler `GET /auxiliares/*` e anotar IDs | `auxiliar:read` | — |
| 3 | `POST /locais` (um por local) | `local:create` | sem lote |
| Correção | `GET /locais/{id}` → `PUT /locais/{id}` completo | `local:update` | — |

- Corpo mínimo: `{"nome":"Consultório 1","empresaId":<id>,"depositoPadraoSaidaId":<id>}`.
- 422 = depósito inativo ou inexistente (volte à S02). 409 = já existe local
  com esse nome na unidade → reutilizar.
- Guardar `localId` no dicionário de IDs (grades e agenda usam).

## Prova

- `provas/S03/local-<nome>/` (antes/resposta/depois/diff).
- `provas/S03/auxiliares-depois.json`: os tipos relidos após a criação pela tela.
- Tabela da review: local, unidade, depósito padrão (nome), ativo, `localId`.

## Armadilhas desta sprint

- Criar local antes do depósito ativo → 422.
- Nomes diferentes para a mesma sala em unidades diferentes (rede): padronize
  antes ("Consultório 1" em todas).
- Tipo duplicado com grafia diferente ("Consulta" × "Consultas") confunde
  relatórios e a política de preço por tipo de produto.
- Tipos de produto: todos os tipos que os produtos da clínica usam precisarão de
  política de preço em **cada** convênio (S10a) — inclusive subtipos. Cadastre
  só os necessários, sem inventar tipo novo à toa.
- Pedir ao implantador o que a API lê sozinha (os IDs dos auxiliares).

## Definition of Ready / Definition of Done

**DoR:** S02 conferida (depósito ativo por unidade); CL-4 recebido ou lista de
salas confirmada na conversa.

**DoD:**
- [ ] todo local existe, com depósito padrão **ativo** da própria unidade;
- [ ] todo tipo necessário existe e o ID está no dicionário;
- [ ] tipos criados pela tela relidos pela API (quando há leitura);
- [ ] provas salvas.

## Checklist de itens

| # | item | status | origem | prova | observação |
|---|---|---|---|---|---|
| S03-01 | Lista de locais por unidade confirmada | pendente | | | |
| S03-02 | Local "Consultório 1" (um item por local) | pendente | | provas/S03/ | |
| S03-03 | Tipos de Serviço conferidos/criados | pendente | | | |
| S03-04 | Tipos de Taxa conferidos/criados | pendente | | | |
| S03-05 | Tipos de Produto conferidos/criados | pendente | | | |
| S03-06 | Tipos de Atendimento conferidos/criados | pendente | | | |
| S03-07 | Tipos de Código conferidos/criados | pendente | | | |
| S03-08 | Tipos de Anexo e de Identificação (tela) | pendente | | | |
| S03-09 | Dicionário de IDs (localId e auxiliares) | pendente | | | |

## O que registrar

- `dados/estrutura/locais.md` e dicionário de IDs.
- `decisoes/DECISOES.md`: nomes padronizados de locais e tipos criados.
- `ESTADO.md`: próximo passo = S04.
