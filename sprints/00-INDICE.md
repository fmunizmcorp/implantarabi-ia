# Sprints S00–S17 — índice e quadro geral

> **Fonte:** https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#checklist · https://www.rabisistemas.com.br/manual/implantacao/index.html#como-escolher · https://www.rabisistemas.com.br/manual/implantacao/pre-requisitos.html#ordem-oficial · **Conferido em:** 2026-09-25
> **Vale para:** produção — ordem oficial de 16 etapas, corrigida em 24/09/2026 · **Kit:** v0.1.0

## Como ler

- **S01 a S16 = etapas 1 a 16 do guia oficial, uma para uma.** S00 (preparação)
  e S17 (estabilização e dossiê) são do kit.
- Cada sprint tem o mesmo modelo, nesta ordem: Objetivo · Link do manual ·
  Depende de · Documentos a pedir · Índice de dados a coletar · Fila de
  perguntas · Enriquecimento · Leitura do que já existe · Gravação · Prova ·
  Armadilhas · DoR/DoD · Checklist · O que registrar.
- O checklist de cada sprint é copiado para `sprints/Sxx.md` do repo da clínica
  (cabeçalho `| # | item | status | origem | prova | observação |`; status:
  `pendente`, `coletado`, `confirmado`, `gravado`, `conferido`, `n/a`, `bloqueado`).
- Toda gravação segue o [ritual de carga](../metodologia/ritual-de-carga.md);
  toda pergunta segue a [conversa com o usuário](../metodologia/conversa-com-o-usuario.md);
  todo documento pedido vem da [lista única](../metodologia/lista-unica-de-documentos.md).

## Arquivos

| Arquivo | O que tem | Quando ler |
|---|---|---|
| [S00-preparacao.md](S00-preparacao.md) | chave, repo privado, pedido único, inventário, lacunas, foto de tudo, plano por porte | sempre, primeiro |
| [S01-empresa-unidades.md](S01-empresa-unidades.md) | empresa e unidades (etapa 1) | Dia 1 |
| [S02-deposito-minimo.md](S02-deposito-minimo.md) | 1 depósito ativo por unidade (etapa 2) | Dia 1 |
| [S03-locais-e-tipos.md](S03-locais-e-tipos.md) | salas/consultórios e tabelas "tipos" (etapa 3) | Dia 1 |
| [S04-operadoras-fornecedores-fabricantes.md](S04-operadoras-fornecedores-fabricantes.md) | operadoras com planos, fornecedores, fabricantes, princípios ativos (etapa 4) | Dia 1–2 |
| [S05-taxas.md](S05-taxas.md) | catálogo de taxas (etapa 5) | Dia 2 |
| [S06-produtos-catalogo.md](S06-produtos-catalogo.md) | catálogo de produtos, sem estoque (etapa 6) | Dia 2 |
| [S07-equipamentos.md](S07-equipamentos.md) | equipamentos (etapa 7) | Dia 2 |
| [S08-servicos-e-tabela-interna.md](S08-servicos-e-tabela-interna.md) | serviços (subserviços antes) e tabela interna = preço de produto (etapa 8) | Dia 2–3 |
| [S09-colaboradores-e-logins.md](S09-colaboradores-e-logins.md) | colaboradores, especialidades e criação de login (etapa 9) | Dia 3–4 |
| [S10-convenios.md](S10-convenios.md) | visão da etapa 10: fila de convênios, Particular, grade horária | Dia 4–5 |
| [S10a-convenio-dados.md](S10a-convenio-dados.md) | dados do convênio (fase 1) | por convênio |
| [S10b-convenio-abas-e-precos.md](S10b-convenio-abas-e-precos.md) | as 6 abas e os preços (fase 2) — atenção redobrada | por convênio |
| [S11-conferencia-farol.md](S11-conferencia-farol.md) | conferência pelo Farol (etapa 11) | Dia 5 |
| [S12-financeiro-fiscal-estoque.md](S12-financeiro-fiscal-estoque.md) | contas, pagamentos, repasse, NFS-e, estoque completo (etapa 12) | Dia 5–6 |
| [S13-pacientes-e-migracao.md](S13-pacientes-e-migracao.md) | pacientes, migração em lotes, LGPD (etapa 13) | Dia 6 |
| [S14-parametros-documentos-usuarios-permissoes.md](S14-parametros-documentos-usuarios-permissoes.md) | parâmetros, documentos, impressão, perfis e permissões (etapa 14) | Dia 6–7 |
| [S15-testes-10-cenarios.md](S15-testes-10-cenarios.md) | os 10 cenários do manual + checagens da IA (etapa 15) | Dia 7 |
| [S16-go-live-e-treinamento.md](S16-go-live-e-treinamento.md) | go-live e treinamento por perfil (etapa 16) | Dia 8+ |
| [S17-estabilizacao-e-dossie.md](S17-estabilizacao-e-dossie.md) | estabilização e dossiê de entrega (kit) | Dia 9–30 |

## Quadro: sprint × etapa × dia × dependências × porte

Legenda de prioridade (do manual): 🟢 essencial · 🟡 importante · ⚪ opcional.
Tempos do manual; o prazo pressupõe documentos completos no Dia 0.

| Sprint | Etapa do manual | Dia (manual) | Depende de | Consultório individual | Clínica pequena/média | Rede / multiunidade |
|---|---|---|---|---|---|---|
| S00 Preparação | — (kit) | Dia 0 | — | 🟢 30–60 min, lista curta | 🟢 ½ a 1 dia | 🟢 1–2 dias |
| S01 Empresa e unidades | [#etapa-1](https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-1) | Dia 1 | S00 | 🟢 1 empresa (CNPJ ou CPF), ~10 min | 🟢 Dia 1 | 🟢 Semana 1, todas as unidades |
| S02 Depósito mínimo | [#etapa-2](https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-2) | Dia 1 | S01 | 🟢 1 depósito, ~2 min | 🟢 Dia 1 | 🟢 Semana 1, 1 por unidade |
| S03 Locais e tipos | [#etapa-3](https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-3) | Dia 1 | S02 | 🟢 1 local + tipos básicos, ~10 min | 🟢 Dia 1 | 🟢 Semana 1, nomes padronizados |
| S04 Operadoras, fornecedores, fabricantes | [#etapa-4](https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-4) | Dia 1–2 | S01, S03 | 🟢 só "Particular" (+1 plano), ~5 min | 🟢 Dia 1–2 | 🟢 Semana 1, catálogo central |
| S05 Taxas | [#etapa-5](https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-5) | Dia 2 | S03 (tipo de taxa) | ⚪ só se algum serviço usar taxa | 🟢 Dia 2 | 🟢 Semana 1–2 |
| S06 Produtos (catálogo) | [#etapa-6](https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-6) | Dia 2 | S02, S03, S04 | ⚪ só se algum serviço usar medicamento | 🟢 Dia 2 | 🟢 Semana 2, catálogo único |
| S07 Equipamentos | [#etapa-7](https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-7) | Dia 2 | S03 | ⚪ só se reservar aparelho | 🟢 Dia 2 | 🟡 Semana 2 |
| S08 Serviços + tabela interna | [#etapa-8](https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-8) | Dia 2–3 | S03, S05, S06, S07 | 🟢 poucos serviços, ~15 min | 🟢 Dia 2–3 | 🟢 Semana 2, sem duplicidade |
| S09 Colaboradores e logins | [#etapa-9](https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-9) | Dia 3–4 | S01, S03 | 🟢 o próprio profissional, ~10 min | 🟢 Dia 3–4 | 🟢 Semana 2–3 |
| S10 Convênios (dados, abas, grade) | [#etapa-10](https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-10) | Dia 4–5 | S04, S05, S06, S08, S09 | 🟢 "Particular" (+1), ~10 min + grade ~15 min | 🟢 Dia 4–5 | 🟢 Semana 3, em escala |
| S11 Conferência pelo Farol | [#etapa-11](https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-11) | Dia 5 | S10 (+ régua do Farol) | 🟡 conferência rápida do Particular | 🟢 Dia 5 | 🟢 Semana 3, pela API em escala |
| S12 Financeiro, fiscal, estoque | [#etapa-12](https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-12) | Dia 5–6 | S01, S06, S09 | 🟢 caixa simples, ~10 min; estoque ⚪ | 🟢 Dia 5–6 | 🟢 Semana 3–4, por unidade |
| S13 Pacientes | [#etapa-13](https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-13) | Dia 6 | S10 (convênios e planos) | 🟢 1º paciente, ~10 min; migração se houver | 🟢 Dia 6 | 🟢 Semana 4, por unidade |
| S14 Parâmetros, documentos, usuários, permissões | [#etapa-14](https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-14) | Dia 6–7 | S09 (e todo o resto) | 🟢 modelos de documento ~20 min; permissões ⚪ | 🟢 Dia 7–8 | 🟢 Semana 4, matriz documentada |
| S15 Testes (10 cenários) | [#etapa-15](https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-15) | Dia 7 | S01–S14 | 🟢 teste ponta a ponta, ~1 h | 🟢 Dia 8–9 | 🟢 Semana 4–5, na unidade-piloto |
| S16 Go-live e treinamento | [#go-live](https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#go-live) | Dia 8+ | S15 | 🟢 | 🟢 Dia 10+ | 🟢 Semana 5–6, replicação |
| S17 Estabilização e dossiê | — (kit) | Dia 9–30 | S16 | 🟢 1–2 semanas leves | 🟢 2–4 semanas | 🟢 4+ semanas |
| **Total (manual)** | | | | **~1 dia (3h30 a 6h)** | **~1 a 2 semanas** | **~3 a 6 semanas** |

## Dependências (resumo)

```
S00 → S01 Empresa → S02 Depósito mínimo → S03 Locais + tipos
                                   │
S01 ─→ S04 Operadoras/Fornecedores/Fabricantes
S03 (tipo de taxa) ─→ S05 Taxas ──────────────┐
S02+S03+S04 ─→ S06 Produtos (catálogo) ───────┤
S03 ─→ S07 Equipamentos ──────────────────────┤
                    S08 Serviços (subserviços antes dos pais) + tabela interna (preço de produto)
S01 ─→ S09 Colaboradores (+ login)            │
S04+S05+S06+S08+S09 ─→ S10 Convênios: dados → abas → grade horária
S10 ─→ S11 Farol ─→ S12 Financeiro/estoque (custos) ─→ reconferir roxos do S11
S10 ─→ S13 Pacientes ─→ S14 Parâmetros/permissões ─→ S15 Testes ─→ S16 Go-live ─→ S17
```

Três dependências que o manual antigo invertia (corrigidas em 24/09/2026):
local exige **depósito ativo** (S02 antes de S03); serviço de medicamento exige
o **produto** (S06 antes de S08); abas de preço e tabela interna exigem as
**taxas** (S05 antes de S08/S10).

## Consultório individual — como pular e compactar

O manual propõe 11 passos para o consultório. No kit eles caem assim:

| Passo do manual (consultório) | Sprint do kit | Como fica |
|---|---|---|
| 1 Empresa (CNPJ ou CPF) | S01 | normal, 1 registro |
| 2 Depósito mínimo | S02 | "Depósito Principal", sem perguntas |
| 3 1 local + tipos básicos | S03 | "Consultório 1"; tipos só os necessários |
| 4 Operadora "Particular" (+ taxas/produto se houver) | S04 (+ S05, S06 se houver) | S05/S06 viram `n/a` se nenhum serviço usa taxa ou medicamento |
| — | S07 | `n/a` salvo aparelho reservado na agenda |
| 5 Serviços | S08 | poucos; tabela interna `n/a` sem produto |
| 6 Você como colaborador | S09 | 1 colaborador + login |
| 7 Convênio "Particular" | S10 → S10a/S10b | só o Particular (e 1 plano, se atender) |
| 8 Grade de horário | S10 (bloco da grade) | 1 grade |
| — | S11 | leitura rápida do Farol do Particular |
| 9 Conta/caixa e tipos de pagamento | S12 | só isso; estoque, NFS-e e centro de custo `n/a` ou depois |
| 10 Tipos de documento | S14 | receita e atestado; permissões `n/a` com 1 usuário |
| 11 1º paciente + 1º agendamento | S13 + S15 | 1 paciente de teste; cenários 1 e 4 (+10 se houver medicamento, +7 se NFS-e) |
| — | S16/S17 | go-live no mesmo dia; S17 leve |

Regras da compactação:
- `n/a` sempre com motivo no checklist ("nenhum serviço usa medicamento").
- O ritual de carga **não** encolhe: foto antes, prévia, aprovação, prova.
- As cerimônias encolhem: planning e review de 2 linhas; daily só se passar de 1 dia.
- Ao crescer (contratar mais gente, aceitar convênios), a clínica volta às
  sprints puladas — nada precisa ser refeito.

## Rede / multiunidade — ondas

1. **Padronização central:** S01–S08 para todas as unidades (catálogos únicos).
2. **Unidade-piloto:** S09–S15 na piloto; opera de verdade alguns dias.
3. **Replicação:** as demais unidades a partir do padrão validado; S16 por unidade.

Congele os padrões antes de replicar: nomes de locais, catálogo de serviços,
matriz de permissões, política de reajuste de tabelas.
