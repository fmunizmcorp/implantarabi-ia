# 04 — Modo Convênio (um convênio, atenção redobrada)

> **Fonte:** experiência de implantação real (roteiro de sessão de convênio, generalizado) + https://www.rabisistemas.com.br/manual/precos/ · **Conferido em:** 2026-09-25
> **Vale para:** produção (regras de preço vigentes desde 23–25/09/2026) · **Kit:** v0.1.0

Você cuida de **um convênio só**: `<NOME DO CONVÊNIO>` (ID no Rabi `<ID>`). Não
abre outro, não mexe em outro, não copia de outro sem ordem. Se esta sessão foi
aberta por uma **sessão coordenadora** ([07](07-coordenacao-multi-sessao.md)),
você fala com ela; senão, com o implantador/dono.

Leia antes (pelo índice): `../conhecimento/precos-e-conversao/` (zero × vazio,
Pacote/Zerar/Utiliza, 4 linhas do Valor, Farol), `../conhecimento/api-externa/`
(convenções, proibidas), [S10](../sprints/S10-convenios.md) (visão), [S10a — dados do convênio](../sprints/S10a-convenio-dados.md),
[S10b — abas e preços](../sprints/S10b-convenio-abas-e-precos.md) e
[S11](../sprints/S11-conferencia-farol.md). Skill: `configurar-convenio`.

## A ordem que não muda
```
DIAGNOSTICAR → RÉGUA → LEVANTAR → COMPARAR → RELATÓRIO → APROVAÇÃO item a item → GRAVAR → PROVAR → REGISTRAR
```
A única coisa que você faz sem aprovação é **ler**.

## Passo −1 · Em que pé está este convênio?
Leia: linha do convênio no `ESTADO.md`, `dados/convenios/<slug>/` (régua,
CSV, decisões), provas anteriores em `provas/S10/<slug>/`, pendências, e o
`updatedAt` das linhas no Rabi. Classifique e **diga ao usuário com a prova**:

| Estado | Como reconhecer | O que fazer |
|---|---|---|
| **NOVO** | sem prova anterior, nada além do cadastro inicial | roteiro completo |
| **EM ANDAMENTO** | há relatório/prova parcial ou pendência aberta | continuar **de onde parou**: conferir no Rabi que o já provado continua igual (vale a leitura, não o relatório); listar (a) aprovado e gravado, (b) aprovado e não gravado, (c) esperando decisão, (d) nunca avaliado |
| **FECHADO** | conferido no Farol, sem pendência | agente `auditor-regressao` primeiro; só mexe se houver fato novo (aditivo, reajuste, regressão, decisão) |

## Passo 1 · Régua contratual (antes de olhar o sistema)
Do contrato e aditivos (agente `extrator-documentos`), preencha
`dados/convenios/<slug>/regua-contratual.md`: vigência, reajuste, prazos
(pagamento, guias, glosa, autorização), fator K, tabelas de referência — **cada
um com cláusula/página**. **A pergunta que abre tudo:** pacote fechado, conta
aberta ou misto? Quais serviços são pacote? Sem resposta, não se configura preço.

## Passo 2 · Levantar o estado atual
GET de `/convenios/{id}` e das abas `servicos`, `produtos`, `taxas`,
`especialidades`, `colaboradores`, planos, e do Farol (`farol/itens`,
`farol/servicos`, `farol/produtos`), paginando até `totalPages`
(`page` começa em 1, `pageSize` ≤ 200). Salve como foto antes. Confira
**linhas lidas = total** e **status 200 com bytes > 0**. Cruze com o catálogo
(`ativo`): abas e Farol também listam itens desativados.

## Passo 3 · CSV com ORIGEM e comparação
Monte `dados/convenios/<slug>/precos-<slug>.csv` (toda linha com documento e
página). Rode `python3 .kit/ferramentas/conversao/simulador.py` para prever o
total de cada serviço, a linha do valor próprio e o Farol. Classifique cada diferença:

| Grupo | O que é | O que você faz |
|---|---|---|
| **A — sustentado** | mudança com cláusula/linha da tabela que a sustenta | propõe |
| **B — precisa de decisão** | análise pronta + pergunta objetiva | pergunta (uma por vez) |
| **C — sem base** | falta documento | lacuna em `pendencias/LACUNAS.md` |

## Passo 4 · Relatório e parada
Uma tela: modelo de cobrança, contagens (serviços, produtos, taxas, ligados,
vermelhos no Farol), o que já está certo, o que muda (grupo A com origem), as
perguntas (B), as lacunas (C). **Pare e espere a aprovação item a item.**

## Passo 5 · Gravar só o aprovado
`python3 .kit/ferramentas/conversao/montar_convenio.py` monta os corpos na
ordem Utiliza → valores → textos/códigos → tipo de atendimento → Pacote/Zerar.
Abas do convênio são **upsert** (campo omitido mantém, `null` limpa, `0` é zero).
Até 200 itens por chamada, **um lote por vez** (senão 429). **207 = falha
parcial**: reenvie só `ERRO`/`NAO_PROCESSADO` (índice começa em 0).

## Passo 6 · Provar
Foto depois + diff campo a campo + **segunda leitura** (pega o que foi aceito e
não persistiu). Rode `python3 .kit/ferramentas/conversao/conferir_farol.py` e
chame o agente `conferente-precos`. Mínimo **3 serviços** conferidos por
inteiro: simples, com medicamento, com pacote. Explique cada vermelho do Farol.

## Passo 7 · Registrar
`decisoes.md` do convênio, `sprints/S10.md`/`S11.md`, `ANALISE-CONTRATOS.md`
(6 dimensões + sugestões de adequação do contrato), `ESTADO.md`, commit + push.

## Regras de preço (a fonte é o kit; aqui só o que mais erra)
- **Vazio** = sem regra neste nível (o sistema sobe de nível). **0,00** = zero de verdade. **0,01 como marcador: proibido.**
- **Valor combinado não é pacote.** Preço fechado = valor combinado + **Pacote** + **Zerar** nos itens inclusos. Sem Pacote, o Zerar nem é consultado.
- Item incluso em serviço com Pacote fechado recebe Zerar; a aplicação/serviço raiz **não** é zerado. Conta aberta = sem Pacote e sem Zerar.
- **Nunca** Zerar medicamento fora de pacote fechado (sairia sem cobrança). Orçamento de medicamento saindo R$ 0,00 é sintoma de Zerar no lugar errado.
- Nunca desligar serviço que a clínica presta; nunca desligar o serviço e deixar o produto ligado.
- Preço particular vem do convênio **Particular**; tabela interna é preço de **produto**.

## Proibições deste modo
Mexer no catálogo (serviço/produto/taxa) — é transversal, só com decisão do dono
e no modo Atualização; mexer em outro convênio; copiar convênio
(`/copiar`, `toggle-all`, importação de Excel); `DELETE`; `POST /convenios/bulk`;
NFS-e, financeiro, estoque; reaproveitar ID de vínculo de outro convênio; dado
de paciente em arquivo.

## Armadilhas já vividas
| Armadilha | Como evitar |
|---|---|
| leitura com status 200 e corpo vazio | conferir status **e** bytes; sem bytes = leitura falhada |
| gravar em item inativo | conferir ativo/inativo e o nome |
| 207 tratado como sucesso | ler `resultados` item a item |
| chave revogada responde 503 (não 401) | parar; é chave, sem retry em laço |
| alteração em massa fora da sessão | agrupar por `updatedAt` (mesmo item, mesma hora, vários convênios) |
| contar vínculos incluindo serviços desativados | cruzar com `GET /servicos` (`ativo`) |
