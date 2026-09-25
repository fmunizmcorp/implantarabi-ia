# S02 — Depósito mínimo (1 por unidade)

> **Fonte:** https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-2 · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-2 · spec `openapi-2026-09-25.json` (`POST /depositos`, `/depositos/bulk`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (dependência corrigida em 24/09/2026) · **Kit:** v0.1.0

## Objetivo

Cada unidade tem **um depósito ativo** para servir de "depósito padrão de saída"
dos locais. Vale mesmo para quem não usa estoque. O resto do estoque fica na S12.

## Link do manual

- Etapa 2: https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-2
- Tela: https://www.rabisistemas.com.br/manual/modulos/estoque.html#deposito-minimo
- Pela API: https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-2

## Depende de

S01 (`empresaId` de cada unidade).

## Documentos a pedir

Nenhum novo. Usa CL-3 (unidades). Se a clínica já tem farmácia/almoxarifado com
nome próprio, DD-3 ajuda a escolher o nome.

## Índice de dados a coletar

| dado | campo API | obrigatório? | onde costuma estar no material do cliente | padrão sugerível | pergunta ao usuário se faltar |
|---|---|---|---|---|---|
| Unidade do depósito | `empresaId` | sim | S01 | a unidade da vez | — |
| Nome do depósito | `descricaoDeposito` | sim (único por unidade) | nome da farmácia/almoxarifado, se houver | **"Depósito Principal"** (rede: "Depósito Principal — <unidade>") | "Posso criar o depósito com o nome 'Depósito Principal'? Ele só serve para as salas funcionarem." |

## Fila de perguntas

1. Sugerir o padrão "Depósito Principal" (uma pergunta, para todas as unidades).
2. Se a clínica já usa um nome (ex.: "Farmácia"), confirmar esse nome.

## Enriquecimento possível

Nenhum.

## Leitura do que já existe no Rabi e regra de não perder nada

- `GET /depositos?ativo=true` e `GET /depositos` (inclui inativos).
- Já existe depósito **ativo** na unidade → **não criar outro**: usar o existente.
- Existe só **inativo** → perguntar se reativa (PUT completo) ou cria novo.
- Ambientes criados pelo site podem já vir com depósito.

## Gravação

| Ordem | Rota | Permissão | Lote |
|---|---|---|---|
| 1 | `POST /depositos` (1 unidade) ou `POST /depositos/bulk` (várias) | `deposito:create` | até 50 (chave `depositos`) — só depois do 1º provado |
| Correção | `GET /depositos/{id}` → `PUT /depositos/{id}` completo | `deposito:update` | — |

- Corpo mínimo: `{"empresaId": <id>, "descricaoDeposito": "Depósito Principal"}`.
- 409 = já existe depósito com esse nome nessa unidade → reutilizar.
- Guardar o `depositoId` no dicionário de IDs: é exigido por `POST /locais`
  (`depositoPadraoSaidaId`) e por `POST /produtos` (`depositoId`).

## Prova

- `provas/S02/deposito-<unidade>/` com antes (lista da unidade), resposta,
  depois (`GET /depositos/{id}`), diff.
- Conferir: **ativo = true**, unidade certa, nome certo.

## Armadilhas desta sprint

- Criar **só o mínimo** agora. Depósitos adicionais, entradas, saldo e custos
  ficam para a S12.
- Um aviso interno antigo dizia que "a API não cria depósito": o Swagger
  publicado tem `POST /depositos` — prevalece o Swagger.
- Inativar o depósito depois quebra os locais que apontam para ele.

## Definition of Ready / Definition of Done

**DoR:** `empresaId` de todas as unidades conhecidos (S01 conferida).

**DoD:**
- [ ] toda unidade tem 1 depósito **ativo**, lido de volta;
- [ ] `depositoId` por unidade no dicionário de IDs;
- [ ] provas salvas.

## Checklist de itens

| # | item | status | origem | prova | observação |
|---|---|---|---|---|---|
| S02-01 | Nome do depósito aprovado | pendente | | | padrão "Depósito Principal" |
| S02-02 | Depósito da unidade 1 ativo | pendente | | provas/S02/ | |
| S02-03 | Depósitos das demais unidades (uma linha por unidade) | pendente | | | |
| S02-04 | Dicionário de IDs atualizado (depositoId) | pendente | | | |

## O que registrar

- Dicionário de IDs (`depositoId` por unidade).
- `decisoes/DECISOES.md`: nome adotado.
- `ESTADO.md`: próximo passo = S03.
