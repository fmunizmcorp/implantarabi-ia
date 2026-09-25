# 09 — Tipo de atendimento, congelamento e XML TISS

> **Fonte:** https://www.rabisistemas.com.br/manual/precos/arvore-de-decisao.html#arvore-xml · https://www.rabisistemas.com.br/manual/precos/guia-ia.html#alg-tipo-atendimento · https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#impacto-modulos · https://www.rabisistemas.com.br/manual/precos/index.html#onde-aparece · **Conferido em:** 2026-09-25
> **Vale para:** produção desde 23/09/2026 (tipo de atendimento por convênio no XML) · **Kit:** v0.1.0

## 1. Tipo de atendimento efetivo

```
tipo_atendimento_efetivo(S, C) = tipo_atendimento_convertido(S, C) se definido no convênio
                                 senão tipo_atendimento do cadastro do serviço
```

- Tela: aba Serviços do convênio, coluna **Tipo de Atendimento** (3 linhas
  🔒/🔁/✅). Escolha na 🔁 o tipo que a **operadora exige** e confira na ✅.
- API: `PUT /convenios/{id}/servicos` → `tipoAtendimentoId` (aceita `null`
  = volta ao do cadastro). Ids em `GET /auxiliares/tipos-atendimento`.
  No cadastro do serviço: `POST /servicos` → `tipoAtendimento` (id).
- O efetivo vai para: o **atendimento**, o **pré-faturamento** e o campo
  **`tipoAtendimento` do XML**.
- Pergunta para o contrato/manual da operadora: *qual tipo de atendimento a
  operadora exige para este procedimento?* (ex.: consulta, SADT/terapia,
  pequena cirurgia…). Erro aqui é glosa, não erro de preço.

## 2. Do cadastro até a guia: onde calcula e onde congela

```
CADASTRO / CONVÊNIO ──► AGENDAMENTO / ORÇAMENTO / AUTORIZAÇÃO ──► ATENDIMENTO ──► PRÉ-FATURAMENTO ──► LOTE / XML
   (configuração)          calculam NA HORA (lêem a config)       CONGELA         trabalha no congelado   gera o arquivo
```

| Parte do sistema | O que faz com os preços |
|---|---|
| Agenda › Agendamento | valor efetivo do serviço e a composição no convênio (itens com Utiliza); item zerado a 0 só em pacote fechado; botão **Custos do agendamento** (custo × venda × margem); Farol consolidado |
| Agenda › Orçamento | só convênio **Pago no ato**; linha do serviço (valor próprio) + linhas de produtos/taxas; regra transacional do arquivo 06 §6; Farol consolidado e pedido de aprovação por nível |
| Agenda › Autorização | valores convertidos + Farol por item (orientação); consolidado bloqueia; colunas Valor, Parcelas máx., Farol |
| **Atendimento** | **congela**: valor do cadastro do serviço, valor convertido, código, tipo de código, tabela 87, nome, tipo de atendimento e a conversão de cada produto/taxa. Mudar o cadastro depois **não altera** atendimentos já criados |
| Faturamento › Pré-Faturamento | usa os congelados; editar Valor por item; **Anular** item; **Atualizar Valores em Massa** (exceto lote fechado) |
| Faturamento › Administrar Lotes | fecha o lote e gera o XML (Baixar XML) |
| Relatórios | mesmas contas da aba Farol; "Receita Própria" = valor próprio; "Receita Total" = árvore inteira |

## 3. Atualizar Valores em Massa

- Pré-Faturamento › botão **Atualizar Valores em Massa** refaz a
  "fotografia" com os preços atuais, pela **mesma cadeia**: valor específico
  do convênio é respeitado **mesmo se 0**; vazio → valor do cadastro.
- **Lote fechado não recalcula.**
- Use depois de corrigir um preço quando há atendimentos ainda não
  faturados com o valor antigo. Sempre com prévia e aprovação da clínica (é
  alteração em massa de valores a receber).
- Sintoma "mudei o preço e a guia de ontem não mudou" = congelamento, não
  erro de configuração.

## 4. Como sai no XML TISS

```
XML TISS (Administrar Lotes › Baixar XML)
├─ linha de PROCEDIMENTO (o serviço)
│    valor      = valor PRÓPRIO do serviço (congelado) × quantidade   ← igual à linha ✅
│    código     = código no convênio → código do convênio → código do cadastro → TUSS
│    tabela 87  = convênio → cadastro
│    tipoAtendimento = tipo do convênio → cadastro do serviço
├─ PRODUTOS → nas áreas deles, agrupados pela tabela 87
│    (20/05 medicamentos · 19/00 materiais · 18 gases), com valor, código e nome convertidos
├─ TAXAS → na área de taxas, com valor, código e nome convertidos
└─ fora do XML: itens ANULADOS no pré-faturamento e guias FILHAS (só a guia mãe entra)
```

- Total da guia = serviço (valor próprio × qtd) + taxas + produtos.
- Quem **soma tudo** é o Farol (e a linha Σ); a linha de procedimento do
  XML **não** soma produtos e taxas.
- Serviço que soma itens: linha própria = valor convertido (ou 0); os itens
  saem nas linhas de despesa.
- Nome e descrição convertidos vão **literalmente** para o XML: nada de
  comentários nesses campos.

## 5. Conferência final recomendada (experiência)

"O auditor da operadora não abre o Rabi; ele vê o XML." Depois de configurar
um convênio, sempre que possível:
1. faça um agendamento/atendimento de teste (ambiente de homologação ou
   paciente de teste combinado com a clínica);
2. leve ao pré-faturamento e confira itens, códigos, tabela 87, quantidades
   e valores;
3. se a clínica permitir, gere o XML de um lote de teste e confira linha a
   linha contra o contrato.

> Rotas de pré-faturamento, lote e XML estão fora do escopo de
> configuração; só com ordem escrita da clínica (ver lista de rotas
> proibidas sem ordem escrita na pasta da API externa).
