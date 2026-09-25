# S05 — Taxas

> **Fonte:** https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-5 · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-5 · https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#taxa-niveis · spec `openapi-2026-09-25.json` (`POST /taxas`, `/taxas/bulk`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (ordem corrigida em 24/09/2026: taxas antes de serviços e convênios) · **Kit:** v0.1.0

## Objetivo

O catálogo de taxas (sala, material, aplicação, guia…) existe uma vez só, com
o **valor da casa** de cada taxa, antes dos serviços, da tabela interna e das
abas de preço dos convênios — que dependem dele.

## Link do manual

- Etapa 5: https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-5
- Tela: https://www.rabisistemas.com.br/manual/modulos/configuracoes.html#taxas
- Como a taxa vira preço: https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#taxa-niveis
- Pela API: https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-5

## Depende de

S03 (tipos de taxa e de código existentes e com ID).

## Documentos a pedir

FA-2 (lista de taxas com valor). Ajudam: CV-2 (taxas que os convênios pagam),
CV-7 (particular), SA-3 (cadastro do sistema anterior).

## Índice de dados a coletar

| dado | campo API | obrigatório? | onde costuma estar no material do cliente | padrão sugerível | pergunta ao usuário se faltar |
|---|---|---|---|---|---|
| Nome da taxa | `taxas` (sic: o campo do nome chama-se `taxas`) | sim | lista de taxas, tabela do particular, tabelas dos convênios | — | — |
| Código interno | `codigoTaxa` | sim | sistema anterior, tabela do convênio | sequência da clínica: "TX-001", "TX-002"… | "A clínica tem um código para a taxa <nome>? Se não, posso numerar TX-001, TX-002…?" |
| Tipo de taxa | `tipoTaxaId` | sim | classificação | pelo nome (sala → "Sala") | "A <taxa> é de sala, de material ou de aplicação?" |
| Valor da casa (R$) | `valor` | sim | lista de taxas, tabela do particular | **nenhum** (dinheiro não tem padrão) | "Quanto a clínica cobra de <taxa> quando não há regra de convênio?" |
| Descrição | `descricao` | não | — | igual ao nome | — |
| Tipo de código | `tipoCodigoId` | não | tabela do convênio (TUSS/próprio) | — | — |
| Tabela 87 da ANS | `tabelaANS87ID` | não (recomendado p/ TISS) | tabela do convênio | pelo tipo de código | — |

O **valor da casa** é o nível mais baixo da conversão. O valor que cada convênio
paga fica na aba Taxas do convênio (S10b) — **não** aqui.

## Fila de perguntas

1. Confirmar em bloco a lista extraída (nome + valor + origem), mostrando só as
   linhas com dúvida uma a uma.
2. Tipo de cada taxa ambígua.
3. Código interno (sugerir a sequência).
4. Taxa sem valor da casa: pedir o valor (ver armadilhas).

## Enriquecimento possível

- Código TUSS/tabela 87 de taxas a partir das tabelas dos convênios (CV-2) e das
  referências TUSS do kit (`referencias/tuss/`).
- Unificar a mesma taxa com nomes diferentes nos vários contratos (uma taxa no
  catálogo; o nome de cada convênio vai no "nome convertido" da S10b).

## Leitura do que já existe no Rabi e regra de não perder nada

- `GET /taxas?ativo=true` e `GET /taxas` — casar por código e por nome
  normalizado.
- Existe → não criar; diferença de valor vira proposta (o catálogo afeta **todos**
  os convênios: decisão escrita do dono).

## Gravação

| Ordem | Rota | Permissão | Lote |
|---|---|---|---|
| 1 | `POST /taxas` (a primeira, sozinha) | `taxa:create` | — |
| 2 | `POST /taxas/bulk` (chave `taxas`) | `taxa:create` | até 50, depois da 1ª provada |
| Correção | `GET /taxas/{id}` → `PUT /taxas/{id}` com a taxa completa | `taxa:update` | — |

- Corpo mínimo: `{"taxas":"Taxa de sala","codigoTaxa":"TX-001","tipoTaxaId":<id>,"valor":45.00}`
  (valores fictícios).
- `POST /taxas` responde **200** (não 201) ao criar — não é erro.
- Guardar `taxaId` no dicionário: usado por `taxaServicoId` do serviço (S08), pela
  tabela interna e pela aba Taxas do convênio.

## Prova

- `provas/S05/taxa-<codigo>/` (antes = busca, resposta, depois, diff).
- Review: tabela nome, código, tipo, valor da casa, ativo — esperado × gravado.

## Armadilhas desta sprint

- **0,01 como marcador é proibido.** 0,00 é preço zero de verdade.
- O campo `valor` é obrigatório: se a clínica não cobra a taxa por fora de
  convênio, **pergunte** qual valor usar e registre a decisão; lembre que, sem
  conversão no convênio, é esse valor que entra na conta.
- Mudar o valor da casa depois mexe em todos os convênios que não têm conversão
  própria para a taxa — é mudança de catálogo, com análise de impacto (modo
  Atualização).
- O nome do campo é `taxas` (não `nome`).

## Definition of Ready / Definition of Done

**DoR:** tipos de taxa com ID (S03); FA-2 recebido ou lista confirmada.

**DoD:**
- [ ] toda taxa usada por serviços ou convênios existe uma vez só;
- [ ] todo valor com origem; nenhum 0,01;
- [ ] `taxaId` no dicionário; provas salvas.

## Checklist de itens

| # | item | status | origem | prova | observação |
|---|---|---|---|---|---|
| S05-01 | Lista de taxas extraída (com origem) | pendente | | | |
| S05-02 | Tipos de cada taxa confirmados | pendente | | | |
| S05-03 | Códigos internos definidos | pendente | | | |
| S05-04 | Valores da casa confirmados | pendente | | | |
| S05-05 | 1ª taxa gravada e provada | pendente | | provas/S05/ | |
| S05-06 | Demais taxas gravadas (lotes) e conferidas | pendente | | | |
| S05-07 | Dicionário de IDs (taxaId) | pendente | | | |

## O que registrar

- `dados/catalogo/taxas.csv` (nome, código, tipo, valor, ORIGEM, taxaId).
- `decisoes/DECISOES.md`: valores da casa decididos sem documento.
- `ESTADO.md`: próximo passo = S06.
