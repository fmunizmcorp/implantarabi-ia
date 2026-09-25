# 11 — Receitas: "quero cobrar assim, como configuro?"

> **Fonte:** https://www.rabisistemas.com.br/manual/precos/guia-clinica.html#parte-4-receitas (Receitas A–I) · https://www.rabisistemas.com.br/manual/precos/guia-clinica.html#marque-pacote · experiência real (receitas J–L, generalizadas) · **Conferido em:** 2026-09-25
> **Vale para:** produção desde 23–24/09/2026 · **Kit:** v0.1.0

Valores ilustrativos. Nomes fictícios ("Convênio Alfa", "Convênio Beta"…).
Cada receita traz: a situação, a configuração exata (tela e CSV do arquivo
10) e o resultado esperado (linha ✅, linha Σ, orçamento). Depois de aplicar,
confira sempre pela linha Σ / Farol (arquivo 13).

Legenda CSV: `U`=utiliza · `V`=valor_combinado · `P`=pacote · `Z`=zerar ·
`vazio`=campo vazio (sem regra).

---

## A — Preço igual para todo mundo (consulta simples)

Consulta a R$ 300 em qualquer convênio.
- Catálogo: Valor = 300,00; somar itens ✘.
- Em cada convênio que atende: aba Serviços › U ✔; V vazio.
- **Resultado:** ✅ = Σ = 300,00 em todos. Sem produto → sem farol de margem
  (não fica roxo).

## B — Preço diferente em um convênio

Casa R$ 300; Convênio Alfa paga R$ 180.
- Receita A + Alfa › aba Serviços: U ✔, V = 180,00 (linha 🔁); opcional:
  nome convertido "CONSULTA ELETIVA", código do contrato, tipo de
  atendimento exigido.
- **Resultado:** Alfa ✅ = Σ = 180,00; demais 300,00. Código vazio no Alfa →
  código do cadastro.

## C — Medicamento aplicado: cobra o remédio + a aplicação (conta aberta)

"Ferro aplicado na veia" = medicamento (preço varia) + aplicação (R$ 80).
1. Produto (medicamento) com preço e **custo** (aba Estoque).
2. Serviço "Aplicação endovenosa": Valor = 80,00 (preço fixo, somar ✘).
3. Serviço "Ferro aplicado na veia": **somar ✔**; aba Produtos: medicamento
   ×1; aba Servicos: "Aplicação endovenosa" ×1.
4. No convênio: U ✔ no serviço, no medicamento e na aplicação; **P ✘, Z ✘**.
- **Resultado:** ✅ = 0,00 ("sem preço próprio") · Σ = medicamento + 80,00.
  Se o preço do medicamento mudar, o serviço muda junto.
- ⚠️ Valor diferente da aplicação no convênio: ponha em **um** lugar só — no
  subserviço "Aplicação endovenosa" dentro do convênio **ou** como valor
  combinado do "Ferro aplicado" (que soma por cima dos itens) — nunca nos
  dois (soma duas vezes).

## D — Preço fechado por convênio (pacote)

Convênio Beta paga R$ 3.500,00 pela aplicação completa, já com o medicamento.
1. Serviço montado como em C.
2. Beta › Serviços › "Ferro aplicado": V = 3.500,00; U ✔; **P ✔**; Z ✘.
3. Beta › Produtos › medicamento: U ✔; **Z ✔**.
4. Beta › Serviços › "Aplicação endovenosa": U ✔; **Z ✔** (se incluída).
5. Produtos/taxas **de dentro** da aplicação que também estão nos 3.500
   (ex.: taxa de sala, materiais): **Z ✔ em cada um** (Zerar não cascateia).
- **Resultado:** ✅ = Σ = 3.500,00. Orçamento: se lançar mais medicamento
  que o previsto na composição, **só o excedente** é cobrado.
- ⚠️ Sem o passo P ✔, os 3.500 seriam só a base e medicamento + aplicação
  somariam por cima.

### Quadro "digitei um valor e os itens continuaram somando" → marque Pacote

Valor combinado muda só o preço do serviço. Para preço fechado: (1) V na
linha 🔁 + (2) **P ✔** no serviço + (3) **Z ✔** em cada item incluso. Item
sem Z continua cobrado à parte. Sem P, o Z nem é consultado.

## E — Pacote de preço fixo com alguns itens cobrados à parte

"Aplicação de medicamento X" = R$ 100,00; seringa incluída; medicamento
(R$ 50) à parte.
- Catálogo: Valor = 100,00; somar ✘; aba Produtos: seringa, medicamento.
- Convênio: serviço U ✔ **P ✔**; seringa U ✔ **Z ✔**; medicamento U ✔ **Z ✘**.
- **Resultado:** Σ = 100 + 50 = **150,00** (✅ = 100,00). Se o medicamento
  também for zerado: Σ = 100,00.

## F — O convênio não cobre um item

- No convênio, U ✘ naquele produto/taxa/serviço.
- **Resultado:** item sem receita **naquele convênio** (em todos os serviços,
  inclusive vendido sozinho); o custo continua no Farol. Orçamento: entra a
  R$ 0,00. Subserviço sem U: ele e tudo dentro dele a R$ 0,00.
- ⚠️ Não use F para "incluir" um item num pacote — para isso é U ✔ + Z ✔
  (receita I). Serviço sem U não pode ser agendado.

## G — Item gratuito para um convênio

- No convênio, linha 🔁 do item: V = **0,00** (zero é zero). U ✔.
- **Resultado:** o item sai a 0,00 (não desce para o cadastro).

## H — Todos os medicamentos do convênio seguem uma tabela + percentual

"Convênio Gama: medicamentos pela tabela de referência + 15%."
- Gama › Dados do convênio › Política de Preço por Tipo de Produto ›
  Adicionar: Tipo = Medicamento · Fonte = a tabela/coluna · FK = 15.
- **Resultado:** todos os medicamentos do Gama = valor da fonte × 1,15,
  exceto os com valor unitário convertido próprio na aba Produtos.
- Cuidado: salvar a política **vazia** apaga a política; pela API, a lista
  enviada é a lista completa.

## I — "Meu preço fixo já inclui os materiais"

"Curativo" = R$ 120,00 fechado no Convênio Delta, com gaze, soro e taxa de
sala inclusos; a pomada especial é cobrada à parte.
- Catálogo: somar ✘; Valor = 120,00 (ou deixe o da casa e use V = 120,00 no
  Delta). Composição: gaze, soro, pomada (Produtos) e taxa de sala (Taxas).
- Delta › Serviços › Curativo: U ✔ **P ✔**.
- Delta › Produtos: gaze e soro U ✔ **Z ✔**; pomada U ✔ **Z ✘**.
- Delta › Taxas: taxa de sala U ✔ **Z ✔**.
- Item incluso dentro de subserviço: zere o **próprio** item.
- Conferir: Expandir serviço e Farol › Itens (gaze, soro e taxa com Conta no
  total = Não; pomada = Sim).
- **Resultado:** Σ = 120,00 + pomada. Orçamento: quantidade prevista de
  gaze, soro e taxa a R$ 0,00; excedente cobrado.
- ⚠️ Sem Pacote, nem preço fixo nem valor combinado incluem nada: o serviço
  cobra fixo + todos os itens com U na quantidade inteira (mudou em
  23/09/2026).

---

## Receitas da experiência real (generalizadas)

## J — Aplicação vendida sozinha **e** dentro de serviços de medicamento, num convênio que trabalha com pacote (inclusive Particular)

Situação: a clínica tem os serviços gerais "Aplicação endovenosa / IM / SC"
com preço fixo que **já inclui** os materiais e as taxas da aplicação. Os
serviços de medicamento ("Medicamento X aplicado EV") usam somar ✔ e contêm
a aplicação como subserviço + o medicamento.
- Catálogo: aplicações somar ✘ com valor fixo; serviços de medicamento
  somar ✔ (preço = aplicação + medicamento).
- Convênio: cada **aplicação** U ✔ **P ✔ Z ✘** (ela é o pacote, não um item
  dentro de pacote); **materiais e taxas da aplicação** U ✔ **Z ✔**; o
  **serviço de medicamento** em conta aberta: U ✔ **P ✘ Z ✘**; o
  **medicamento** U ✔ **Z ✘**.
- **Resultado esperado:** aplicação sozinha Σ = valor fixo da aplicação
  (materiais e taxas a 0 dentro dela); serviço de medicamento Σ = valor
  fixo da aplicação + medicamento.
- ⚠️ Se a aplicação estiver com Z ✔, o serviço de medicamento pode sair
  **R$ 0,00** no orçamento (ver armadilha A1 em
  [14-armadilhas-vividas.md](14-armadilhas-vividas.md)).
- Preço promocional só num convênio (ex.: aplicação mais barata só nos
  medicamentos de ferro do Particular): manter **dois** serviços de
  aplicação no catálogo (normal e promocional) e usar o promocional só na
  composição daqueles medicamentos, ligado (U ✔) só no convênio certo — é
  mais robusto que 5 valores combinados manuais com Pacote.

## K — Medicamento por pacote contratado (convênio que só paga pacotes)

Situação: o contrato paga um valor único por "Medicamento X aplicado"
(inclui aplicação, material, taxa e remédio).
- Convênio: serviço de medicamento U ✔ **P ✔** V = valor do contrato;
  subserviço aplicação U ✔ **Z ✔**; medicamento U ✔ **Z ✔**; materiais e
  taxas U ✔ **Z ✔** (cada um, inclusive os de dentro da aplicação).
- Marque Pacote **só** nos serviços que o contrato prevê e a clínica atende.
  Não abra serviços sem base contratual.
- **Resultado:** Σ = valor do contrato; Farol = contrato ÷ custo do remédio e
  materiais (pode ficar amarelo/vermelho: é informação para a clínica, não
  erro de configuração).

## L — Código de procedimento só para autorização (valor zero) + taxa paga

Situação: a operadora exige um código de procedimento para autorizar (sem
honorário) e paga o atendimento por uma taxa específica.
- Convênio: serviço U ✔, **V = 0,00** (zero é zero), código do contrato,
  `autorizacao_previa` ✔; a taxa correspondente U ✔ com V = valor do
  contrato; medicamento/material conforme a política.
- **Resultado:** ✅ do serviço = 0,00; Σ = taxa + produtos. Honorário nesse
  código seria glosa.

---

## Tabela de bolso

| Receita | somar | V (serviço) | P | Z itens inclusos | Z itens à parte | Σ esperado |
|---|---|---|---|---|---|---|
| A | ✘ | vazio | ✘ | — | — | valor da casa |
| B | ✘ | valor | ✘ | — | — | valor combinado |
| C | ✔ | vazio | ✘ | — | ✘ | Σ itens |
| D | ✔ | preço fechado | ✔ | ✔ | ✘ | preço fechado (+ à parte) |
| E | ✘ | vazio | ✔ | ✔ | ✘ | fixo + à parte |
| I | ✘ | vazio ou valor | ✔ | ✔ | ✘ | fixo + à parte |
| J (aplicação) | ✘ | vazio | ✔ (Z do próprio ✘) | ✔ | — | fixo da aplicação |
| J (medicamento) | ✔ | vazio | ✘ | — | ✘ | aplicação + remédio |
| K | ✔ | valor do contrato | ✔ | ✔ | — | valor do contrato |
| L | ✘ | 0,00 | ✘ | — | — | taxa + produtos |
