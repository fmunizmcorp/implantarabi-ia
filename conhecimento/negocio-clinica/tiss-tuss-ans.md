# TISS, TUSS e ANS — o padrão que a guia precisa seguir

> **Fonte:** https://www.rabisistemas.com.br/manual/tiss-tuss/index.html#tabelas-dominio · `modulos/autorizacao.html#tiss-23-87` · `precos/arvore-de-decisao.html#tabela-mestra` · publicações da ANS guardadas numa base de referência (Componente de Conteúdo e Estrutura TISS 202511; planilha "Termos vigentes TUSS" 2026.01; XSD 4.03.00) · **Conferido em:** 2026-09-25
> **Vale para:** padrão TISS/TUSS vigente em 2026 (confirme a versão no portal da ANS) · **Kit:** v0.1.0

## 1. O que é cada coisa

- **ANS** regula os planos de saúde e publica o padrão **TISS** (obrigatório
  para trocar informação entre prestador e operadora — RN 501/2022, confirme a
  norma vigente no site da ANS).
- **TISS** tem componentes:
  1. **Organizacional** — regras de uso;
  2. **Conteúdo e Estrutura** — as mensagens e guias (campos, obrigatoriedade);
  3. **Representação de Conceitos em Saúde** — a terminologia **TUSS**;
  4. **Segurança e Privacidade**;
  5. **Comunicação** — os **XML/XSD** (esquemas) e o webservice.
- **Versão**: cada convênio usa uma versão TISS do XML (na base de referência:
  XSD **4.03.00**, jan/2026). O Rabi gera o XML na versão configurada no
  convênio. Operadora pode exigir versões diferentes por tipo de guia.
- **Mensagens TISS** (ex.: `loteGuias`, `recursoGlosa`, `solicitacaoProcedimento`,
  `verificacaoElegibilidade`, `demonstrativosRetorno`, `cancelaGuia`,
  `envioDocumentos`). Hoje o Rabi gera o **lote em XML** e importa o
  **retorno**; enviar por webservice é roadmap (Sprint 14).

## 2. TUSS — as terminologias (tabelas de domínio)

Nome oficial de cada uma conforme a planilha da ANS "Termos vigentes TUSS"
(competência 2026.01):

| Nº | Terminologia | Uso no Rabi |
|---|---|---|
| **18** | Diárias, taxas e gases medicinais | Código de taxas |
| **19** | Materiais e OPME | Código de materiais |
| **20** | Medicamentos | Código de medicamentos |
| **22** | Procedimentos e eventos em saúde | Código de serviços (consultas, exames, terapias) |
| **23** | Caráter do atendimento | Eletivo × urgência/emergência (autorização) |
| **24** | CBO | Especialidade do profissional (o "CBOS") |
| **26** | Conselho profissional | Sigla do conselho na guia |
| **36** | **Indicador de acidente** | Trabalho / trânsito / outros |
| **38** | Mensagens (glosas, negativas e outras) | Motivos de glosa no retorno |
| **50** | Tipo de atendimento | Campo `tipoAtendimento` do XML |
| **52** | Tipo de consulta | Primeira, retorno… |
| **54** | Tipo de guia | — |
| **87** | **Relação das terminologias unificadas** ("tabela de tabelas") | De qual tabela vem o código do item |

Outras existentes (resumo): 25 código da despesa, 34 forma de pagamento, 35
grau de participação, 39 motivo de encerramento, 41 regime de internação, 43
sexo, 45–47 status (solicitação, cancelamento, protocolo), 59 UF, 60 unidade
de medida, 61 via de acesso, 62 via de administração, 72 tipo de identificação
do beneficiário, 74 motivos de ausência do código de validação, 76 regime de
atendimento, 81 tipo de documento.

## 3. Tabela 87 — de onde vem o código do item

Cada item da guia diz **de qual tabela** é o código dele. Errar a tabela 87 é
glosa por codificação.

| Código | Significado | Confiança |
|---|---|---|
| **22** | Procedimentos e eventos em saúde (TUSS) | ✅ confirmado (nome ANS + uso no Rabi) |
| **20** | Medicamentos (TUSS) | ✅ confirmado |
| **19** | Materiais e OPME (TUSS) | ✅ confirmado |
| **18** | Diárias, taxas e gases medicinais (TUSS) | ✅ confirmado |
| **00** | Tabela própria da operadora | ✅ observado no domínio do Rabi |
| **98** | Tabela própria de pacotes | ✅ observado no domínio do Rabi |
| **05** | Brasíndice | ✅ no domínio do Rabi desde set/2026 · ⚠️ **não confirmei** se consta da Tabela 87 ANS vigente (constava em versões antigas do TISS) |
| **12** | SIMPRO | ✅ no domínio do Rabi desde set/2026 · ⚠️ mesma ressalva do 05 |
| **97** | Taxa própria | ✅ no domínio do Rabi desde set/2026 · ⚠️ **não confirmei** na publicação da ANS — trate como código aceito pelo Rabi e confirme com a operadora |
| 90 | Tabela própria de pacote odontológico | ⚠️ de memória, não conferido em fonte — não use sem confirmar |

O manual do Rabi mostra o agrupamento do XML como "20/05 medicamentos · 19/00
materiais · 18 gases/taxas" (`precos/arvore-de-decisao.html#arvore-xml`). A
planilha de termos da ANS guardada na base **não traz a lista de códigos da
Tabela 87** (só o nome da tabela); por isso as ressalvas acima. **Na dúvida:
use o que o contrato/manual do credenciado da operadora manda** e registre a
fonte.

## 4. Tabela 36 × Tabela 87 (confusão comum)

- **Tabela 36 = indicador de acidente** (legenda de preenchimento: trabalho =
  0, trânsito = 1, outros = 2 — confirme o código de "não acidente" na versão
  vigente).
- **Tabela 87 = tabela de tabelas** (a referência do código do item).
- O manual corrigiu em 24/09/2026 um texto que trocava as duas. Não repita o erro.

## 5. Códigos TUSS de procedimento (Tabela 22)

- 8 dígitos. A maior parte segue os capítulos da **CBHPM**: 1 procedimentos
  gerais (consultas — ex. `10101012` consulta em consultório), 2 procedimentos
  clínicos (terapias e aplicações — ex. `20104383` pulsoterapia intravenosa por
  sessão, `20104391`/`20104421` terapia imunobiológica IV/SC por sessão,
  `20104545` terapia medicamentosa injetável ambulatorial), 3 cirúrgicos e
  invasivos, 4 diagnósticos e terapêuticos (exames, SADT).
- Códigos de medicamentos (Tabela 20) e materiais (Tabela 19) têm
  numeração própria da TUSS; o Brasíndice/SIMPRO trazem a correspondência
  TUSS de cada apresentação (ver [fontes-de-preco.md](fontes-de-preco.md)).
- ⚠️ Um glossário interno antigo dizia que "materiais e medicamentos TUSS são o
  EAN de 13 dígitos" e que os códigos 50–99 eram taxas/materiais. **Não use**
  essa regra: confira o código na planilha TUSS vigente.

## 6. CBHPM e portes

- **CBHPM** (AMB): cada procedimento tem um **porte** (1A a 14C) com valor em
  R$, e às vezes **custo operacional (UCO)** e porte anestésico.
- Contratos dizem "CBHPM edição X, com deflator/inflator Y% sobre porte e UCO".
  A **edição** importa: contratos antigos usam edições antigas (ex.: 5ª ed. de
  2008) — nunca aplique a edição mais nova sem o contrato dizer.
- Regras gerais de equipe e acumulação (confirme no contrato): cirurgião 100%,
  1º auxiliar 30%, 2º e 3º 20%; 2º procedimento pela mesma via 70%, demais 50%.
- Acréscimo de urgência (ex.: +30% fora do horário) **só** vale para ato com
  **caráter** de urgência/emergência. Clínica ambulatorial eletiva não cobra —
  em uma implantação real isso foi levantado por engano como "receita a
  recuperar".

## 7. Rol da ANS e DUT

- **Rol de Procedimentos e Eventos em Saúde**: cobertura mínima obrigatória
  dos planos (RN 465/2021 e atualizações — confirme a RN vigente).
- **DUT** (Diretrizes de Utilização, anexo do Rol): condições clínicas para a
  cobertura (ex.: terapia imunobiológica exige DUT + relatório + exames).
- Algumas operadoras têm **coberturas extra-Rol** próprias, válidas só para
  alguns planos. A cobertura é por **plano**, não só por convênio.
- Lei 9.656/1998, art. 35-C: urgência/emergência não depende de autorização
  prévia (argumento frequente em recurso).

## 8. Como a IA usa isto

1. Serviço: código TUSS 22 + tabela 87 = 22 (ou 00/98 quando o contrato usa
   código próprio/pacote). Medicamento: 20 (ou 05 se o convênio pede Brasíndice).
   Material: 19 (ou 12/00). Taxa: 18 (ou 97/00).
2. Tipo de atendimento efetivo por serviço no convênio (vai ao XML).
3. Confirme com o manual do credenciado de cada operadora: versão TISS, tabela
   87 esperada por tipo de item, códigos próprios.
4. Onde não houver certeza, **escreva "não confirmado"** e pergunte ao
   faturista da clínica.
