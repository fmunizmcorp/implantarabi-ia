# S04 — Operadoras, fornecedores e fabricantes

> **Fonte:** https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-4 · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-4 · spec `openapi-2026-09-25.json` (`POST /operadoras`, `/fornecedores`, `/fabricantes` e os `/bulk`) · **Conferido em:** 2026-09-25
> **Vale para:** produção · **Kit:** v0.1.0

## Objetivo

Toda operadora com que a clínica trabalha (incluindo a **"Particular"**) existe
com seus planos; e os fornecedores e fabricantes dos produtos existem para a S06.

## Link do manual

- Etapa 4: https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-4
- Telas: https://www.rabisistemas.com.br/manual/modulos/configuracoes.html#operadoras · https://www.rabisistemas.com.br/manual/modulos/estoque.html#fornecedores · https://www.rabisistemas.com.br/manual/modulos/estoque.html#fabricantes
- Pela API: https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-4

## Depende de

S01 (clínica existe). Princípios ativos e unidades de medida conferidos na S03.

## Documentos a pedir

CV-1 (contratos: qualificação da operadora), CV-4 (registro ANS, CNPJ, CNES,
código do prestador), CV-5 (planos), FA-4 (notas fiscais: fornecedor e
fabricante), FA-3 (lista de produtos: fabricante).

## Índice de dados a coletar

### Operadora (uma por operadora; os convênios vêm na S10)

| dado | campo API | obrigatório? | onde costuma estar no material do cliente | padrão sugerível | pergunta ao usuário se faltar |
|---|---|---|---|---|---|
| Nome | `nome` | sim | capa do contrato, carteirinha | — | — |
| Descrição | `descricao` | sim | idem | igual ao nome | — |
| Registro ANS | `registroANS` | sim | capa/rodapé do contrato, carteirinha, site da ANS | — | "Qual o registro ANS da <operadora>? Costuma estar na carteirinha do paciente." |
| CNPJ | `cnpj` | sim | qualificação das partes no contrato | — | "Qual o CNPJ da <operadora>?" |
| CNES | `codigoCNES` | sim | contrato, cadastro da operadora | — | "O contrato informa o CNES da <operadora>?" |
| Endereço (CEP, logradouro, número, bairro, cidade) | `endereco.cep`, `.endereco`, `.numero`, `.bairro`, `.cidade` | sim | qualificação das partes | pelo CEP | (confirmar) |
| UF | `endereco.unidadeFederativa` | sim | idem | **nome por extenso** ("Distrito Federal"), não a sigla | — |
| Complemento | `endereco.complemento` | não | idem | — | — |
| Razão social | `razaoSocial` | não | contrato | — | — |
| Código da clínica na operadora | `codigoOperadora` | não | contrato, guias TISS, portal da operadora | — | "Qual é o código da clínica na <operadora>? Aparece nas guias." |
| Inscrição municipal | `im` | não | — | em branco | — |
| Como o prestador aparece no XML TISS | `identificacaoPrestadorXML` (`CNPJ` ou `CODIGO_NA_OPERADORA`) | não (recomendado) | manual TISS da operadora | `CNPJ` | "A <operadora> identifica a clínica pelo CNPJ ou por um código próprio nas guias?" |
| Contatos | `contato[]` (`pessoaDeContato`, `email`, `telefone`, `celular`) | não | contrato, e-mails | — | — |
| Planos | `plano[].nome` | sim, se enviar planos | anexo de planos, carteirinhas | — | "Quais planos da <operadora> a clínica atende? Se atende todos, me diga." |

### Fornecedor

| dado | campo API | obrigatório? | onde costuma estar | padrão sugerível | pergunta se faltar |
|---|---|---|---|---|---|
| Nome | `nome` | sim | nota fiscal de compra | — | — |
| CNPJ | `cnpj` | sim | nota fiscal | — | — |
| Inscrição (estadual) | `inscricao` | sim | nota fiscal (cabeçalho do emitente) | — | "A nota do <fornecedor> tem inscrição estadual? Se for isento, me diga." |
| Telefone | `telefoneFornecedor` | sim | nota fiscal, site | — | "Qual o telefone do <fornecedor>?" |
| Tipo de prestador | `tipoPrestadorDeServico` | não | — | em branco | — |

### Fabricante

| dado | campo API | obrigatório? | onde costuma estar | padrão sugerível | pergunta se faltar |
|---|---|---|---|---|---|
| Nome | `nome` | sim | nota fiscal (descrição do item), bula, tabelas de referência | pelas referências do kit | "O <produto> é de qual laboratório/fabricante?" |

### Princípio ativo

Só leitura na API (`GET /auxiliares/principios-ativos`). O que faltar é criado
pela tela (Estoque → Princípios Ativos) pelo implantador.

## Fila de perguntas

1. Confirmar a **lista de operadoras** (dos contratos) + a "Particular".
2. Para cada operadora: confirmar os dados extraídos; pedir os obrigatórios que
   faltam (registro ANS, CNES), **uma pergunta por vez**.
3. Planos de cada operadora.
4. Fornecedores: confirmar em bloco os extraídos das notas; pedir inscrição e
   telefone que faltarem.
5. Fabricantes: confirmar em bloco; perguntar só os ambíguos.

## Enriquecimento possível

- **Registro ANS e CNPJ** pela lista pública de operadoras ativas da ANS (dados
  abertos), se a sessão tiver internet — confirmar sempre.
- **CEP → endereço.**
- **Fabricante** a partir das referências do kit (`referencias/`: Brasíndice,
  SIMPRO, CMED trazem laboratório/fabricante) ou das tabelas próprias da clínica
  indicadas em `config/referencias-da-clinica.md`.

## Leitura do que já existe no Rabi e regra de não perder nada

- `GET /operadoras` (+ `GET /operadoras/{id}` para planos e contatos) — casar
  por **CNPJ** e por registro ANS.
- `GET /fornecedores?search=` — casar por CNPJ.
- `GET /fabricantes` — casar por nome normalizado (sem "LTDA", "S.A.", acento).
- Existe → reutilizar ID; diferenças viram proposta de correção.

## Gravação

| Ordem | Rota | Permissão | Lote |
|---|---|---|---|
| 1 | `POST /operadoras` ou `/operadoras/bulk` (chave `operadoras`) | `operadora:create` | até 50, depois do 1º provado |
| 2 | `POST /fornecedores` ou `/fornecedores/bulk` | `fornecedor:create` | até 50 |
| 3 | `POST /fabricantes` ou `/fabricantes/bulk` | `fabricante:create` | até 50 |
| 4 | Princípios ativos que faltam: tela → reler `GET /auxiliares/principios-ativos` | — | — |
| Correção | GET → `PUT /operadoras/{id}` com **listas completas** de planos e contatos | `operadora:update` | — |

- Guardar `operadoraId`, os IDs dos **planos** (`GET /operadoras/{id}` →
  `plano[].id`), `fornecedorId`, `fabricanteId` no dicionário.
- `PUT /operadoras/{id}`: o plano ou contato que faltar na lista é **removido**.
- Fornecedor não tem exclusão pela API.

## Prova

- `provas/S04/operadora-<slug>/`, `fornecedor-<slug>/`, `fabricante-<slug>/`.
- Tabela da review: operadora, ANS, CNPJ, planos (nomes), ativo; fornecedores e
  fabricantes com contagem esperado × gravado.

## Armadilhas desta sprint

- **Operadora "Particular":** é a base do convênio "Particular" (S10). A API
  exige registro ANS, CNPJ e CNES, que não existem para "Particular". **Não
  tenho certeza** de qual valor o Rabi espera: primeiro veja se o ambiente já
  traz uma operadora "Particular" (ambientes novos costumam trazer); se não,
  crie pela **tela** (Configurações → Operadoras) com orientação do time Rabi.
  Nunca invente um registro ANS.
- UF por extenso aqui (e sigla em empresas).
- `identificacaoPrestadorXML` errado faz a operadora recusar o XML TISS.
- Fabricante é obrigatório no produto (S06): cadastre ao menos um por produto.
- Dose/marca parecidas na nota fiscal geram fabricante errado: confirme.

## Definition of Ready / Definition of Done

**DoR:** CV-1/CV-4 de pelo menos as operadoras da vez; FA-4 ou FA-3 para
fornecedores/fabricantes.

**DoD:**
- [ ] toda operadora (incluindo "Particular") existe, com planos, lida de volta;
- [ ] fornecedores e fabricantes dos produtos da S06 existem;
- [ ] princípios ativos necessários existem;
- [ ] IDs no dicionário; provas salvas.

## Checklist de itens

| # | item | status | origem | prova | observação |
|---|---|---|---|---|---|
| S04-01 | Lista de operadoras confirmada | pendente | | | |
| S04-02 | Operadora "Particular" existe | pendente | | | |
| S04-03 | Operadora <nome> + planos (uma linha por operadora) | pendente | | provas/S04/ | |
| S04-04 | Fornecedores extraídos das notas | pendente | | | |
| S04-05 | Fornecedores gravados e conferidos | pendente | | | |
| S04-06 | Fabricantes gravados e conferidos | pendente | | | |
| S04-07 | Princípios ativos conferidos (tela, se faltar) | pendente | | | |
| S04-08 | Dicionário de IDs (operadoras, planos, fornecedores, fabricantes) | pendente | | | |

## O que registrar

- `dados/operadoras/`, `dados/estoque/fornecedores.csv`, `fabricantes.csv` (com ORIGEM).
- Dicionário de IDs.
- `decisoes/DECISOES.md`: como a "Particular" foi criada; identificação no XML.
- `ESTADO.md`: próximo passo = S05.
