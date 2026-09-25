# S01 — Empresa e unidades

> **Fonte:** https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-1 · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-1 · spec `openapi-2026-09-25.json` (`POST /empresas`, schema `EmpresaEscrita`) · **Conferido em:** 2026-09-25
> **Vale para:** produção · **Kit:** v0.1.0

## Objetivo

A clínica e cada uma das suas unidades existem no Rabi, com CNPJ, endereço e
contatos corretos, lidas de volta pela API.

## Link do manual

- Etapa 1: https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-1
- Tela: https://www.rabisistemas.com.br/manual/modulos/configuracoes.html#empresas-unidades
- Pela API: https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-1

## Depende de

S00 (chave testada, foto inicial feita).

## Documentos a pedir

CL-1 (cartão CNPJ / contrato social), CL-2 (CNES), CL-3 (unidades e endereços),
CL-5 (contatos). Ver [lista única](../metodologia/lista-unica-de-documentos.md).

## Índice de dados a coletar

Uma linha por **unidade** (cada unidade é um registro de "Empresas e Unidades";
a API chama de *empresa*).

| dado | campo API | obrigatório? | onde costuma estar no material do cliente | padrão sugerível | pergunta ao usuário se faltar |
|---|---|---|---|---|---|
| Razão social | `razaoSocial` | sim | cartão CNPJ, contrato social | — | "Qual é a razão social que aparece no cartão CNPJ?" |
| Nome fantasia | `nomeFantasia` | sim | cartão CNPJ, fachada, site | o nome como a clínica se apresenta | "Como a clínica é conhecida pelos pacientes?" |
| CNPJ (ou CPF, se autônomo sem CNPJ) | `cnpj` | sim (único) | cartão CNPJ | — | "Qual o CNPJ desta unidade? Se for o mesmo da matriz, me diga." |
| CEP | `endereco.Cep` | sim (objeto endereço) | cartão CNPJ, conta de consumo | — | "Qual o CEP da unidade <nome>?" |
| Logradouro | `endereco.Endereco` | sim | idem | pelo CEP | (confirmar o que veio do CEP) |
| Número | `endereco.Numero` | sim | idem | — | "Qual o número do endereço?" |
| Complemento | `endereco.Complemento` | não | idem | — | — |
| Bairro | `endereco.Bairro` | sim | idem | pelo CEP | (confirmar) |
| Cidade | `endereco.Cidade` | sim | idem | pelo CEP | (confirmar) |
| UF | `endereco.unidadeFederativaId` | sim | idem | aceita a **sigla** ("DF") | (confirmar) |
| CNES | `cnes` | não (recomendado) | alvará, cadastro CNES, cabeçalho de guia TISS | — | "Qual o número do CNES da clínica? Costuma estar no alvará ou nas guias de convênio." |
| Telefone(s) | `telefone`, `telefone2` | não | papel timbrado, site | — | "Qual o telefone fixo da recepção?" |
| Celular(es) | `celular`, `celular2` | não | idem | — | — |
| E-mail(s) | `email`, `email2` | não | idem | — | "Qual e-mail a clínica usa para contato?" |
| Vigência do endereço | `dataInicioVigencia`, `dataFimVigencia`, `dataRenovacao` | não | contrato de locação, alvará | em branco | só se o cliente quiser controlar |
| Tipo de contrato | `tipoContratoId` | não | — | em branco | ID só na tela; deixar em branco |
| Logo | — (tela) | não | CL-5 | — | a IA orienta o upload pela tela |

## Fila de perguntas

1. Confirmar **quantas unidades** e quais têm CNPJ próprio (mostrar a lista
   extraída de CL-3).
2. Para cada unidade: confirmar razão social, nome fantasia, CNPJ e endereço
   extraídos (mostrar a origem).
3. Pedir CNES se não veio.
4. Pedir contatos só se o cliente quiser que apareçam em impressos.

Confirmar o que veio do cartão CNPJ. Sugerir o endereço a partir do CEP. Pedir
CNES e contatos. Uma pergunta por mensagem.

## Enriquecimento possível

- **CEP → endereço** (logradouro, bairro, cidade, UF) por serviço público de CEP,
  se a sessão tiver internet; sempre confirmado.
- **CNPJ público** (razão social, nome fantasia, endereço, situação cadastral):
  conferir se o CNPJ está ativo e se o endereço bate.
- **CNES público**: número do estabelecimento pelo CNPJ.
- Validar dígitos verificadores de CNPJ/CPF antes da prévia.

## Leitura do que já existe no Rabi e regra de não perder nada

- `GET /empresas` devolve a lista inteira (ativas **e** inativas), sem paginação
  de fato. Casar por **CNPJ** (só dígitos).
- Já existe com o mesmo CNPJ → **não criar**: comparar campo a campo e propor só
  as diferenças (PUT completo, ver abaixo). Existe **inativa** → perguntar se
  reativa (decisão escrita).
- Ambientes criados pelo site podem já trazer a empresa da clínica: é o caso mais
  comum — a S01 vira conferência e complemento.

## Gravação

| Ordem | Rota | Permissão | Lote |
|---|---|---|---|
| 1 | `POST /empresas` (matriz) | `empresa:create` | sem lote — uma chamada por unidade |
| 2 | `POST /empresas` (cada filial) | `empresa:create` | idem |
| Correção | `GET /empresas/{id}` → alterar → `PUT /empresas/{id}` com a empresa **inteira** | `empresa:update` | — |

- `PUT /empresas/{id}` **substitui o cadastro por completo** (diz a própria rota):
  campo omitido some. Sempre GET antes e reenvio completo.
- 409 = CNPJ já existe (inclusive em empresa desativada): reutilizar o ID.
- Guardar o `empresaId` de cada unidade no dicionário de IDs (`dados/dicionario-de-ids.md`) — é usado
  por depósitos, locais, colaboradores (`empresas`) e convênios (`empresaId`,
  `unidadesIds`).
- Exemplo mínimo (fictício):
  `{"razaoSocial":"Clínica Exemplo LTDA","nomeFantasia":"Clínica Exemplo","cnpj":"<CNPJ válido>","endereco":{"Cep":"70000000","Endereco":"Rua Exemplo","Numero":"1","Bairro":"Centro","Cidade":"Brasília","unidadeFederativaId":"DF"}}`

## Prova

- `provas/S01/empresa-<slug>/antes.json` (busca pelo CNPJ), `resposta.json`,
  `depois.json` (`GET /empresas/{id}`), `diff.txt`.
- Tabela final para a review: unidade, CNPJ, CNES, cidade/UF, ativo, `empresaId`.
- Conferir: nenhum CNPJ duplicado; endereço completo; nome fantasia como a
  clínica quer que apareça.

## Armadilhas desta sprint

- **Unidade × local × filial.** Cada unidade que aparece em "Empresas e
  Unidades" é um registro de empresa; sala/consultório é **local** (S03).
  O convênio aponta para `empresaId` e `unidadesIds` — errar aqui obriga a
  refazer convênio depois.
- **Unidade sem CNPJ próprio** (mesmo CNPJ em outro endereço): como o CNPJ é
  único no cadastro (409), **não tenho certeza** de como o Rabi quer esse caso.
  Não invente: registre como pendência e pergunte ao time Rabi; enquanto isso,
  trate o endereço extra como locais dentro da mesma unidade, se o cliente
  aceitar.
- UF: aqui aceita **sigla**; em operadoras e colaboradores é **nome por extenso**.
- Grupo empresarial (mais de um CNPJ sob a mesma gestão) não tem rota na API
  externa: se a tela exigir, é feito pela tela.
- PUT parcial apaga dados de contato e vigência.

## Definition of Ready / Definition of Done

**DoR:** S00 concluída; CL-1 e CL-3 recebidos (ou dados confirmados na conversa).

**DoD:**
- [ ] toda unidade existe no Rabi, lida de volta pela API;
- [ ] nenhum CNPJ duplicado; nenhuma unidade inativa sem decisão;
- [ ] `empresaId` de cada unidade no dicionário de IDs;
- [ ] provas salvas; review aceita.

## Checklist de itens

| # | item | status | origem | prova | observação |
|---|---|---|---|---|---|
| S01-01 | Lista de unidades confirmada (quantas, quais com CNPJ próprio) | pendente | | | |
| S01-02 | Unidade 1 (matriz): razão social, fantasia, CNPJ | pendente | | | |
| S01-03 | Unidade 1: endereço completo | pendente | | | |
| S01-04 | Unidade 1: CNES e contatos | pendente | | | |
| S01-05 | Unidade 1 gravada e conferida | pendente | | provas/S01/ | |
| S01-06 | Demais unidades (uma linha por unidade) | pendente | | | |
| S01-07 | Dicionário de IDs atualizado (empresaId) | pendente | | | |
| S01-08 | Logo enviado pela tela (se desejado) | pendente | | | |

## O que registrar

- `dados/empresa/unidades.md` (dados normalizados com origem).
- Dicionário de IDs (`empresaId` por unidade).
- `decisoes/DECISOES.md`: como filiais e endereços extras foram modelados.
- `ESTADO.md`: próximo passo = S02.
