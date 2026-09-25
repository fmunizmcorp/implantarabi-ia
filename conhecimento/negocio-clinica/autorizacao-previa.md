# Autorização prévia — quando exigir e como configurar

> **Fonte:** https://www.rabisistemas.com.br/manual/modulos/autorizacao.html#fluxo · `rotinas/autorizacao-orcamento.html#fase-3` · `regras-de-negocio/index.html#regras-junho-2026` · Swagger da API externa (schemas `ConvenioBase`, `ConvenioServicoItem`) · experiência de implantação real e manuais de credenciado (generalizados) · **Conferido em:** 2026-09-25
> **Vale para:** Rabi em produção em 25/09/2026 (autorização online com a operadora é roadmap S14) · **Kit:** v0.1.0

## 1. O que é

Aprovação da operadora **antes** do procedimento. A operadora devolve uma
**senha** (com validade) que vai na guia. Sem ela, quando o contrato exige, a
glosa é praticamente certa.

Exceção legal: urgência/emergência não depende de autorização prévia (Lei
9.656/1998, art. 35-C). Clínica ambulatorial eletiva não se apoia nisso.

## 2. Quando costuma ser exigida

| Situação | Regra prática observada |
|---|---|
| **Aplicação/infusão de medicamento em ambulatório** | **Toda aplicação costuma exigir autorização, independente do custo** — inclusive medicamento barato. Vale para terapia medicamentosa injetável, pulsoterapia, imunobiológicos, "medicamento aplicado" |
| Terapia imunobiológica, quimioterápicos, anticorpos monoclonais, interferons, alguns antifúngicos e bisfosfonatos | Autorização **sempre**; em geral com **DUT** (diretriz da ANS) + relatório médico com justificativa + exames |
| Tratamento seriado (sessões) | Autorização por quantidade de sessões; renovação quando acaba |
| Exames de média/alta complexidade, procedimentos | Conforme contrato / manual do credenciado |
| OPME | Sempre, em geral com cotações (ex.: 3 orçamentos) |
| Consulta eletiva simples | Em geral **não** exige (confirme elegibilidade da carteirinha) |

⚠️ **Limiares de valor** que aparecem em contratos ("autorização para material
ou medicamento acima de R$ 1.000/unidade", "acima de R$ 400", "≥ R$ 300") em
geral se referem à **internação hospitalar** ou ao item avulso em conta
hospitalar. Em uma implantação real, aplicar esses limiares ao **ambulatório**
foi um erro corrigido pelo gestor: no ambulatório, a aplicação de medicamento
exige autorização mesmo abaixo do limiar. **Leia a cláusula inteira** e, na
dúvida, pergunte ao faturista da clínica.

Prazos típicos de resposta da operadora constam do manual do credenciado (ex.:
"até N dias úteis para SADT de média/alta complexidade") — registre com a fonte.

## 3. Como fica no Rabi

| Onde | O quê |
|---|---|
| Convênio › aba Serviços, por serviço | Marca **autorização prévia** (`autorizacaoPrevia` em `ConvenioServicoItem`) nos serviços que o contrato exige |
| Parâmetros / convênio | **Agendamento exige autorização** e/ou **orçamento aprovado** conforme parametrização (#373/#374, em produção). Enquanto faltar, o agendamento fica **Pendente** |
| Convênio (dados) | `prazoAutorizacao` (prazo/validade) |
| Convênio (dados) | `exigirToken` — o nome sugere exigir token/código de validação do beneficiário no atendimento. **O significado exato não está documentado** no manual nem no Swagger: confirme na tela com o implantador antes de ligar. ⚠️ Num `PUT /convenios/{id}`, **omitir `exigirToken` grava `false`** — sempre reenvie o valor lido |
| Módulo Autorização | Pedido com **serviços, produtos e taxas com quantidades** (desde ago/2026), caráter (Tabela 23) e tabela 87 de cada item; só editável antes do envio; "tratamento continuado" repete o pedido; botão Agendar |
| Farol | Autorização tem Farol consolidado; alçada aprova sobre o consolidado |
| Paciente | Acompanha o andamento pelo serviço online |

**Elegibilidade:** conferir se a carteirinha está ativa e o plano cobre. No
padrão TISS existe a mensagem `verificacaoElegibilidade`; no Rabi, hoje, a
conferência é feita no portal da operadora (webservice direto é roadmap S14).
O cadastro do paciente valida o vínculo de carteirinha ativo ao criar a
autorização.

## 4. Regras de ouro na operação

1. **Pedir completo:** serviço + medicamento + materiais + taxas. O que não foi
   pedido não é faturado.
2. **Cancelado ou falta não consome** a sessão autorizada — o saldo continua.
3. Autorização aprovada **vira agendamento no mesmo dia** (botão Agendar).
4. Validade vence: acompanhe e renove antes.
5. Registre cada tratativa (protocolo, contato) na timeline da autorização.

## 5. Perguntas que a IA faz ao configurar um convênio

1. "No contrato/manual deste convênio, quais procedimentos exigem autorização?"
   (peça a página; extraia com cláusula)
2. "Toda aplicação de medicamento aqui exige senha, mesmo barata?" (padrão:
   sim — confirme)
3. "Há DUT/relatório/exames exigidos para imunobiológicos?"
4. "Qual o prazo de validade da senha e o prazo de resposta?"
5. "O convênio exige token/código do beneficiário na chegada?"

Grave a resposta em `convenios/<slug>/regua-contratual.md` do repo da clínica,
com a origem (documento, página).
