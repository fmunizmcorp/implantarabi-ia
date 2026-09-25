# 02 — Modo Implantação (clínica do zero, S00 → S17)

> **Fonte:** manual oficial https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html (16 etapas, 10 cenários de teste) + experiência de implantação real · **Conferido em:** 2026-09-25
> **Vale para:** produção (ordem oficial desde 24/09/2026) · **Kit:** v0.1.0

Você conduz a implantação do Sistema Rabi **do começo ao go-live**: plano,
documentos, extração, cadastro pela API, provas, testes e entrega.

**Como se entra neste modo:** o usuário escreve `Vamos implantar <Nome da
Clínica>` (ou `continuar` / `continuar implantação`) — ninguém cola prompt.
Primeira vez (repo ainda com o marcador do modelo): rotina PRIMEIRA VEZ do
`CLAUDE.md` da clínica, começando por
`python3 .kit/ferramentas/kit/personalizar_clinica.py --clinica "<nome dito>" --porte <porte>`
(pergunte só o porte, se não souber). Nas outras vezes: RETOMADA em até 8
linhas. Guia do humano: [MANUAL-PASSO-A-PASSO.md](../MANUAL-PASSO-A-PASSO.md).
Método: [metodologia/scrum-da-implantacao.md](../metodologia/scrum-da-implantacao.md) e
[metodologia/ritual-de-carga.md](../metodologia/ritual-de-carga.md).

## A ordem oficial (não inverta)
Cada sprint depende das anteriores. Playbook de cada uma em `../sprints/`:

| Sprint | Etapa do manual | Playbook |
|---|---|---|
| S00 | preparação | [S00-preparacao.md](../sprints/S00-preparacao.md) |
| S01 | 1 · Empresa e unidades | [S01-empresa-unidades.md](../sprints/S01-empresa-unidades.md) |
| S02 | 2 · Depósito mínimo (1 por unidade) — local exige depósito ativo | [S02-deposito-minimo.md](../sprints/S02-deposito-minimo.md) |
| S03 | 3 · Locais e tipos | [S03-locais-e-tipos.md](../sprints/S03-locais-e-tipos.md) |
| S04 | 4 · Operadoras, fornecedores, fabricantes | [S04-operadoras-fornecedores-fabricantes.md](../sprints/S04-operadoras-fornecedores-fabricantes.md) |
| S05 | 5 · Taxas | [S05-taxas.md](../sprints/S05-taxas.md) |
| S06 | 6 · Produtos (catálogo) | [S06-produtos-catalogo.md](../sprints/S06-produtos-catalogo.md) |
| S07 | 7 · Equipamentos | [S07-equipamentos.md](../sprints/S07-equipamentos.md) |
| S08 | 8 · Serviços (subserviços antes) + tabela interna (preço de **produto**) | [S08-servicos-e-tabela-interna.md](../sprints/S08-servicos-e-tabela-interna.md) |
| S09 | 9 · Colaboradores (+ logins) | [S09-colaboradores-e-logins.md](../sprints/S09-colaboradores-e-logins.md) |
| S10 | 10 · Convênios (dados, depois abas) | [S10-convenios.md](../sprints/S10-convenios.md) |
| S11 | 11 · Conferência pelo Farol | [S11-conferencia-farol.md](../sprints/S11-conferencia-farol.md) |
| S12 | 12 · Financeiro, fiscal e estoque | [S12-financeiro-fiscal-estoque.md](../sprints/S12-financeiro-fiscal-estoque.md) |
| S13 | 13 · Pacientes | [S13-pacientes-e-migracao.md](../sprints/S13-pacientes-e-migracao.md) |
| S14 | 14 · Parâmetros, documentos, usuários e permissões | [S14-parametros-documentos-usuarios-permissoes.md](../sprints/S14-parametros-documentos-usuarios-permissoes.md) |
| S15 | 15 · Testes (10 cenários) | [S15-testes-10-cenarios.md](../sprints/S15-testes-10-cenarios.md) |
| S16 | 16 · Go-live e treinamento | [S16-go-live-e-treinamento.md](../sprints/S16-go-live-e-treinamento.md) |
| S17 | estabilização e dossiê | [S17-estabilizacao-e-dossie.md](../sprints/S17-estabilizacao-e-dossie.md) |

## Como você trabalha
1. **S00 primeiro, com porta de saída:** repo privado, papéis, chave testada,
   **foto inicial** de todas as áreas do Rabi (nada existente é sobrescrito sem
   prévia), **pedido único de documentos**
   ([lista](../metodologia/lista-unica-de-documentos.md); texto em [06](06-mensagens-padrao.md)).
2. **Documentos:** cada arquivo que chega → `documentos-do-cliente/recebidos/AAAA-MM-DD/`
   → `inventario.py` → `extrair_texto.py` → agente `extrator-documentos` → ficha
   → dados em `dados/` com ORIGEM ([método](../metodologia/ingestao-de-documentos.md)).
   Material grande: em lotes, com checkpoint (commit) a cada lote.
3. **Fila de perguntas por sprint:** para cada dado, escolha **confirmar** o que
   foi extraído, **sugerir um padrão** (ex.: "Consultório 1", "Depósito Principal")
   ou **pedir**. Uma pergunta por vez, dizendo o efeito prático.
4. **Toda gravação** pelo ritual de 5 passos (skill `ritual-de-carga`). Item a
   item no que é novo; em bloco só depois que o 1º item do bloco saiu certo.
5. **Convênios (S10–S11):** siga [04-modo-convenio.md](04-modo-convenio.md), um convênio por vez.
6. **Logins (S09/S14):** você cria pela rota externa `POST /colaboradores/{id}/usuario`
   (senha inicial ≥ 8 caracteres; `409` = já tem login, não é erro), registra a
   senha inicial em `credenciais/CREDENCIAIS.md` e avisa da troca no 1º acesso.
   Perfis e permissões: ver o playbook da S14 (parte pode exigir a tela).
7. **Depois de cada passo:** atualize `sprints/Sxx.md` e `ESTADO.md`, commit +
   push, e mostre a evolução ("S05: 60% → 80%").
8. **Daily** de 5 linhas a cada dia de trabalho; **review** ao fechar cada
   sprint, com a foto depois (comandos `/daily` e `/review`). PDCA a cada 5–10 microsprints.
9. **S15:** os 10 cenários do manual + conferência de valor (3 serviços por
   convênio). Nenhum go-live com cenário reprovado. Dados de teste são
   cancelados/inativados, nunca apagados.

## Tempo por porte (manual)
Guia oficial (https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#tempo-estimado):
consultório individual **~1 dia** · clínica pequena/média **1–2 semanas** ·
rede/multiunidade **3–6 semanas** — **com documentos completos no início**.
Diga isso ao usuário quando faltar documento: o prazo anda com os documentos.

## Nunca
Inverter a ordem; gravar sem prévia e aprovação; inventar valor; chamar rota
proibida sem ordem escrita (NFS-e, dinheiro, estoque real, `DELETE`, `/bulk`
sem prévia); guardar dado de paciente em prova.
