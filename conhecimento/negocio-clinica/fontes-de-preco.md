# Fontes de preço — SIMPRO, Brasíndice, CMED, TUSS e OPME

> **Fonte:** layout dos arquivos oficiais usados numa implantação real (Brasíndice TXT edição de maio/2026, SIMPRO, CMED PF/PMC/PMVG), regras de cobrança de dezenas de convênios (só os padrões, generalizados), lições de casamento de produtos · https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#produto-cadeia · **Conferido em:** 2026-09-25
> **Vale para:** mercado brasileiro em 2026 · **Kit:** v0.1.0

As tabelas-base ficam em `referencias/` do kit (ver `referencias/00-INDICE.md`
quando existir); a clínica pode apontar as próprias em
`config/referencias-da-clinica.md`, que prevalecem. Como o preço chega ao item
no Rabi: [../precos-e-conversao/00-INDICE.md](../precos-e-conversao/00-INDICE.md).

## 1. As fontes

| Fonte | O que traz | Atualização | Observação |
|---|---|---|---|
| **Brasíndice** | Medicamentos (e um arquivo de materiais): **PF** (preço fábrica) e **PMC** (preço máximo ao consumidor), por apresentação | Edições frequentes (numeração sequencial, várias por ano) | Arquivo TXT com separador vírgula, latin-1 |
| **SIMPRO** | Materiais (e medicamentos), preço de referência por apresentação | Periódica | Muito usado para material descartável e OPME |
| **CMED** (ANVISA) | Preço **máximo** permitido: PF, PMC e **PMVG** (venda ao governo), por **alíquota de ICMS** | Mensal; reajuste anual | Teto legal; útil para conferir se um preço é plausível |
| **TUSS 20 / 19** (ANS) | Códigos de medicamentos (com registro ANVISA) e de materiais/OPME (fabricante, nome técnico) | Mensal/competência | Código que vai na guia |
| **CBHPM** (AMB) | Procedimentos por porte + UCO | Edições | Ver [tiss-tuss-ans.md](tiss-tuss-ans.md) |
| **Tabela própria** | Preços/códigos definidos pela operadora | Contrato | Tabela 87 = 00 (própria) ou 98 (pacotes) |
| **Nota fiscal (NF)** | Custo real de compra | Por compra | Base de OPME e de itens fora das tabelas |

## 2. Brasíndice — campos que importam

Principais colunas do arquivo de medicamentos: laboratório, código do produto,
nome, **código da apresentação**, descrição da apresentação, **PMC total**,
**PF total**, **quantidade na embalagem**, PMC unitário, PF unitário, edição,
genérico (S/N), **EAN**, **registro ANVISA**, **restrito hospitalar (S/N)**,
**código TUSS** do item, GGREM, código TISS.

- **Unitário = total ÷ quantidade da embalagem** (o arquivo de medicamentos já
  traz o unitário; o de materiais, não — calcule).
- A cobrança é por **unidade usada** (ampola, frasco), então quase sempre o
  **unitário**.
- "Restrito hospitalar" costuma mudar a regra de preço (ver §4).

## 3. CMED — PF/PMC/PMVG por ICMS

A CMED publica o preço de cada apresentação **para cada alíquota de ICMS**
(0%, 12%, 17%, 18%, 19%, 20%, 21%, 22%… — a lista varia). Use a alíquota da
**UF da clínica** (pergunte ou confira com o contador). PMVG é o teto em venda
a órgão público. Chave de casamento: **EAN** ou **registro ANVISA**.

## 4. Como os contratos costumam mandar cobrar (padrões de mercado)

Padrões recorrentes em regras de cobrança de convênios (cada contrato tem a sua
combinação — **extraia do contrato**, nunca aplique por padrão):

| Item | Padrões comuns |
|---|---|
| Medicamento de uso comum | Brasíndice **PMC** |
| Medicamento de uso restrito hospitalar | Brasíndice **PF + percentual** (ex.: +38,24%, +25%, +15%) |
| Oncológicos | Brasíndice PF (às vezes capítulo próprio, com ICMS isento) |
| Medicamento fora do Brasíndice | SIMPRO; se não houver, NF + % |
| Material descartável | **SIMPRO sem taxa** de comercialização, ou SIMPRO −10% / −15% / −20%, ou SIMPRO +16% |
| Material fora do SIMPRO | Brasíndice materiais, ou **NF + 16%** |
| OPME | Autorização prévia; **3 cotações**; menor cotação ou NF + %; às vezes a operadora compra |
| Dietas enterais/parenterais | Brasíndice com desconto ou acréscimo próprio |
| Taxas, diárias, gases | Tabela própria da operadora ou anexo do contrato |
| Genéricos | Algumas operadoras exigem prioridade para genérico |
| Item retirado da tabela | Algumas mandam usar a **última publicação** em que constava |
| Não remunerado | Alguns contratos simplesmente não pagam material/medicamento ou certos itens (ex.: viscossuplementação) → **sem Utiliza** |

No Rabi isso vira: **política de preço por tipo de produto** (qual tabela e
qual coluna para Medicamento, Material, Imunobiológico…) + **Fator K** (o %)
no convênio, e exceções por item no nível 3. Atenção: **todos** os tipos e
subtipos de produto usados precisam de política — tipo sem política fica sem
preço no convênio.

## 5. Edições congeladas

Alguns contratos fixam uma **edição antiga** (ex.: "Brasíndice edição N de
2018", "SIMPRO edição M de 2017"). Nesses convênios a edição atual **não
vale**: é preciso a edição do contrato. Se a clínica não tiver o arquivo
daquela edição, registre a lacuna — não use a atual como aproximação sem
autorização escrita.

## 6. Casar o produto da clínica com a tabela

1. **EAN costuma vir 0** (ou vazio) no catálogo de produtos do sistema — em uma
   implantação real, 100% dos produtos estavam sem EAN. Casamento por código
   dá 0%.
2. Case por **nome + dose + apresentação**:
   - normalize (maiúsculas, sem acento);
   - princípio ativo ou marca (primeira palavra);
   - **dose/concentração** por expressão regular, ex.
     `(\d+(?:[.,]\d+)?)\s*(MG|G|MCG|UI|ML|MG/ML|%)`;
   - apresentação (ampola, frasco-ampola, seringa preenchida; volume).
3. **Dose é discriminante crítico**: mesma substância ou mesma marca com dose
   diferente (100 mg × 500 mg; 40 mg × 80 mg; 200 × 400) é **outro produto**.
   Depois do casamento automático, rode uma auditoria que compara a dose dos
   dois lados e marque divergências.
4. Mostre ao usuário **candidatos com pontuação** para confirmar; nunca grave
   um casamento de baixa confiança sem aprovação.
5. Registre a origem do preço de cada produto (tabela, edição, coluna, linha).
   Sugira à clínica cadastrar o EAN nos produtos (facilita tudo depois).

## 7. O que normalmente **não** se cobra

Manipulados, vacinas (em geral não pagas pelas operadoras), material de
limpeza e itens sem correspondência nas tabelas costumam ficar **sem Utiliza**
no convênio (custo sem receita). Confirme com a clínica — ver
[materiais-medicamentos-e-servicos.md](materiais-medicamentos-e-servicos.md).
