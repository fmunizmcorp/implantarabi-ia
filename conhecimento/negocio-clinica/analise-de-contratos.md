# Análise de contratos com operadoras — o que extrair e como virar configuração

> **Fonte:** método de revisão de contratos em 6 dimensões usado numa operação real de faturamento (generalizado) · lições da mesma operação (evidência tripla, OCR, proposta ≠ aditivo) · https://www.rabisistemas.com.br/manual/modulos/configuracoes.html#convenios-campos · **Conferido em:** 2026-09-25
> **Vale para:** qualquer contrato de credenciamento · **Kit:** v0.1.0

O convênio é **o coração** da configuração, e o contrato é a fonte da verdade
do convênio. A IA lê o contrato inteiro (com aditivos, anexos e manual do
credenciado), extrai com **página e cláusula**, e só então propõe a
configuração. Nunca "deduz" um preço.

## 1. As 6 dimensões

| # | Dimensão | O que extrair | Vira no Rabi |
|---|---|---|---|
| 1 | **Cobertura** | Procedimentos cobertos (com TUSS), exclusões, o que exige autorização, alta complexidade, especialidades credenciadas, planos cobertos | Utiliza por item; autorização prévia; aba Especialidades; aba Planos |
| 2 | **Remuneração** | Tabela de referência (CBHPM edição X, Brasíndice PF/PMC, SIMPRO, tabela própria), percentual/fator sobre a tabela, preços próprios, pacotes, regras de reajuste (índice, periodicidade), último e próximo reajuste | Política de preço por tipo de produto; Fator K; valores convertidos (nível 3); Pacote + Zerar; datas de reajuste |
| 3 | **Prazos** | Entrega de guias, pagamento, recurso de glosa, resposta ao recurso, retorno, vigência | Campos de prazo do convênio ([faturamento-medico.md](faturamento-medico.md)) |
| 4 | **Obrigações da clínica** | Documentos por procedimento, fluxo de autorização, credenciamento (CNES, conselhos), versão TISS, forma de envio, nota fiscal | Kits de documentos; parâmetros; versão do XML |
| 5 | **Obrigações da operadora** | Garantia de pagamento, juros/multa por atraso, notificação de glosa e de mudanças | Registro para cobrança e negociação |
| 6 | **Alertas** | Cláusulas que prejudicam a clínica; cláusulas a favor (usar em recurso); lacunas | Lista de riscos no repo da clínica |

## 2. A régua contratual (o produto da leitura)

Para cada convênio, monte uma "régua" — a tabela que diz, item a item, **quanto
e como cobrar**, com a coluna **ORIGEM** (documento, página, cláusula/linha):

| Item (serviço/produto/taxa) | Código e tabela 87 | Coberto? | Regra de preço | Autorização? | Pacote/incluso? | ORIGEM |
|---|---|---|---|---|---|---|

Essa régua é a entrada para configurar o convênio pela API (estudo em
[../precos-e-conversao/00-INDICE.md](../precos-e-conversao/00-INDICE.md)).

## 3. Cuidados que custaram caro em implantações reais

1. **Proposta comercial ≠ aditivo.** Carta-proposta enviada **pela clínica**
   sem aceite formal da operadora **não é contrato**. Só vale o que está
   assinado pelas duas partes (ou publicado pela operadora).
2. **Evidência tripla para lista de especialidades** (e para qualquer
   cobertura duvidosa):
   (a) anexo ou carta **assinada pela operadora**;
   (b) tabela de valores ou código específico para aquele item;
   (c) faturamento real recorrente e pago.
   As três convergem = alta confiança. Só (c) = bandeira vermelha — faturar
   prova uso, não prova cobertura; confirme com a operadora. Em uma
   implantação real, vários contratos listavam 1 especialidade no anexo
   assinado enquanto a clínica faturava 10–18.
3. **Contratos escaneados sem texto** são o maior gargalo: faça **OCR** antes
   de analisar (Tesseract em português, 300 dpi; uma 2ª passada a 600 dpi e
   recorte da coluna de valores com contraste aumentado recuperam os valores
   que ficam em branco na 1ª). Registre quais páginas vieram de OCR.
4. **Edições congeladas:** alguns contratos fixam uma edição antiga de tabela
   (ex.: "Brasíndice edição N de 2018", "SIMPRO edição M de 2017", "CBHPM 5ª
   ed."). A tabela mais nova **não se aplica**.
5. **Valores idênticos entre convênios diferentes** são sinal de **template**
   copiado, não de contrato. Confira cada um contra o seu contrato.
6. **Documento arquivado na pasta errada** acontece (edital de um convênio na
   pasta de outro). Confira cabeçalho e partes do documento, não o nome do
   arquivo.
7. **Sem contrato legível → lacuna honesta**, não valor inventado: registre
   "falta o valor X do contrato" e pergunte.
8. **Entidades intermediadoras** (associação que representa várias
   operadoras): regra geral da entidade + regras por subconvênio; trate cada um
   como convênio e confira caso a caso.
9. **Reajuste de tabela só sobe o que o contrato manda** — nunca sobrescreva um
   preço contratual por um valor de tabela "atual" sem a cláusula.

## 4. Adequações que a IA pode sugerir (sempre como proposta)

- Procedimentos que a clínica faz e o contrato não cobre → pedir inclusão em
  aditivo.
- Preços defasados em relação à tabela de referência → comparativo dos 20
  procedimentos mais frequentes (valor contratado × referência, diferença em
  R$ e %, impacto anual) para renegociação.
- Prazos ou regras ambíguas → pedir esclarecimento por escrito.
- Cláusulas usáveis em recurso de glosa → anotar para o faturista.

A decisão de negócio é **do dono da clínica**. A IA mostra números e riscos;
não decide.

## 5. O que pedir ao usuário (pedido único)

Contrato e **todos** os aditivos (assinados), anexos de preço, manual do
credenciado/prestador, cronograma de faturamento do ano, tabelas próprias da
operadora, comunicados/informativos de regra de cobrança, e — se existir — um
demonstrativo de pagamento recente (mostra o que a operadora realmente paga).
Tudo entra em `documentos-do-cliente/` com linha no inventário.

## 6. Onde registrar

No repo da clínica: `ANALISE-CONTRATOS.md` (resumo por convênio nas 6
dimensões) e `dados/convenios/<slug>/regua-contratual.md` (régua com ORIGEM).
