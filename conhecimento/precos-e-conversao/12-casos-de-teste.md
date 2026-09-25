# 12 — Casos de teste T1–T26 e invariantes I1–I13 (especificação do motor)

> **Fonte:** https://www.rabisistemas.com.br/manual/precos/guia-ia.html#casos-de-teste · https://www.rabisistemas.com.br/manual/precos/guia-ia.html#invariantes · https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#exemplos-conferencia · **Conferido em:** 2026-09-25
> **Vale para:** produção desde 23–24/09/2026 (T23–T26: regra vigente 25/09 e linha Σ desde 24/09) · **Kit:** v0.1.0

**Este arquivo é a especificação** do motor Python em `ferramentas/conversao/`
(`motor.py`, `simulador.py`, `tests/`). Os testes T1–T26 são os do manual,
reescritos com entradas **inequívocas**. Onde o manual deixou um valor
implícito, o kit fixou um valor e marcou **[kit]** — o resultado esperado não
depende dele, ou foi calculado com ele.

## 0. Convenções (valem para todos os casos)

- Um caso tem **um convênio C** e um **serviço raiz R**.
- `somar` = "Definir preço do serviço pelos itens" do catálogo (T/F).
- `cad` = Valor do cadastro do serviço (reais). Se `somar = T`, `cad` é
  irrelevante (base = 0 sem valor convertido).
- `V` = valor convertido do serviço no convênio: `—` = **vazio/null**;
  número = preenchido (**0 e 0,01 são preenchidos**).
- `P` = Pacote do serviço no convênio (T/F). Padrão F.
- Item de composição = `tipo nome valor·Z·U ×q` onde `valor` é o **valor
  unitário já resolvido** do item no convênio (produto: arquivo 04; taxa:
  arquivo 05), `Z` = Zerar, `U` = Utiliza. Padrões quando omitido: `Z=F`,
  `U=T`, `q=1`, custo do produto = 0.
- Subserviço = `sub nome [cad X, somar S, V V, P P, Z Z, U U] { itens }`.
  Padrões: `somar=F`, `V=—`, `P=F`, `Z=F`, `U=T`.
- Saídas: `base(R)` (= linha ✅), `Σ` = `valor(R,C)` (= linha Σ = receita do
  Farol do serviço), `custo(R)`, e por item `conta` (Sim/Não) + `motivo`
  (`NAO_UTILIZA_NO_CONVENIO` · `ZERADO_EM_PACOTE` · `PAI_FORA_DO_TOTAL`).
- Farol: régua **Vermelho 100 / Amarelo 120**; `índice = receita/custo×100`;
  `≤ 100` → VERMELHO; `100 < índice < 120` → AMARELO; `≥ 120` → VERDE;
  produto envolvido sem custo ou sem preço → ROXO; custo total 0 sem produto
  → sem farol (não roxo). (Fronteira em 120 não confirmada — ver arquivo 08.)
- Arredondamento: 2 casas, meio para cima, só no resultado final.

## 1. Casos de valor do serviço

| # | Raiz (catálogo) | Convênio: raiz | Composição (valor·Z·U ×q) | Esperado |
|---|---|---|---|---|
| **T1** | cad 100 · somar F | V — · P F | produto A 50·F·T | base 100 · **Σ 150** (itens sempre entram; até 23/09 dava 100) |
| **T2** | cad 100 · somar F | V — · P T | produto A 50·T·T | base 100 · **Σ 100** · A: Não/ZERADO_EM_PACOTE |
| **T3** | cad 100 · somar F | V — · P T | produto A 50·F·T | base 100 · **Σ 150** |
| **T4** | cad 100 [kit] · somar F | V 90 · P T | produto A 50·F·T | base 90 · **Σ 140** |
| **T5** | somar T | V — · P F | produto A 3000·T·T | base 0 · **Σ 3000** (Z ignorado: não há pacote) |
| **T6** | somar T | V 266,16 · P F | produto A 3000·F·T | base 266,16 · **Σ 3266,16** |
| **T7** | somar T | V — · P T | produto A 135,42·T·T; sub Apl [cad 80] {} | base 0 · **Σ 215,42** (nada zerado: P sem preço não é pacote fechado) |
| **T8** | somar T | V 3506,53 · P T | produto A 3000·T·T | base 3506,53 · **Σ 3506,53** · A: Não/ZERADO_EM_PACOTE |
| **T9** | somar T | V — · P F | produto A 3000·F·F | base 0 · **Σ 0** · A: Não/NAO_UTILIZA_NO_CONVENIO |
| **T10** | somar T | V — · P F | sub Sb [cad 40 [kit], U F] { produto A 50·F·T custo 20 [kit] } | **Σ 0** · Sb: Não/NAO_UTILIZA · A: Não/PAI_FORA_DO_TOTAL · **custo(R) = 20** (custo conta) |
| **T12** | cad 100 · somar F | V **0,00** · P F | produto A 50·F·T | base **0** (zero é zero; não desce ao cadastro) · **Σ 50** · ✅ = 0 |
| **T15** | cad 300 [kit] · somar F | V **0,01** · P T | sub Apl [cad 240 [kit], Z T] { taxa Sala 73,99·F·T } | base 0,01 · Apl: Não/ZERADO_EM_PACOTE (só a linha dele) · Sala: Sim · **Σ 74,00** (até 23/09 a taxa ficava fora) |
| **T16** | cad 100 · somar F | V — · P T | sub Sb [cad 40, Z F] { produto A 30·T·T } | Sb entra com 40 · A: Não/ZERADO_EM_PACOTE (contexto de pacote desce) · **Σ 140** |
| **T17** | somar T | V — · P F | sub Sb [cad 80, somar F, P F] { produto A 20·F·T } | **Σ 100** (80 + 20). Antes de 23/09 dava 80 |
| **T20** | somar T | V 266,16 · P F | produto A 3000·F·T | **✅ = 266,16** (base, procedimento do XML) · **Σ = 3266,16** (Farol / Farol › Itens) |
| **T23** | cad 100 [kit] · somar F | V 100 · P **F** | produto A 50·T·T; taxa B 30·T·T | **Σ 180** (valor combinado sem Pacote não é pacote; Z não é lido) |
| **T24** | cad 100 [kit] · somar F | V 100 · P **T** | produto A 50·T·T; taxa B 30·T·T | **Σ 100** (preço fechado) · A, B: Não/ZERADO_EM_PACOTE |
| **T25** | cad 100 [kit] · somar F | V 100 · P T | produto A 50·T·T; taxa B 30·F·T | **Σ 130** (B sem Z é cobrado à parte) |
| **T26** | somar T ("Medicamento F aplicado" no Particular) | V — · P F | produto F 900·F·T; sub Apl [cad 80, U T] {} | **✅ = 0** ("sem preço próprio: itens cobrados à parte" — não é erro) · **Σ = 980** = Farol |

## 2. Casos de orçamento (regra transacional, arquivo 06 §6)

Convênio **Pago no ato**. "Composição" = quantidade prevista no serviço;
"usou" = quantidade lançada no orçamento.

| # | Configuração | Lançado | Esperado (linhas do orçamento) |
|---|---|---|---|
| **T11** | igual a T8 (somar T, V 3506,53, P T, produto A 3000·Z T, composição 1) | A usou **2** | serviço 3506,53 + A: 1 un a R$ 0 + **1 excedente × 3000** → **total 6506,53** |
| **T18** | cad 100 · somar F · V — · **P F** · produto A 50·F·T, composição 1 | A usou **2** | serviço 100 + A **2 × 50** (quantidade inteira) → **total 200** (antes de 23/09: 100 + 50) |
| **T19** | cad 100 [kit] · somar F · P F · produto A com **U F** (preço da casa 80, custo 60 [kit]) na composição | A usou 1 | serviço 100 + A a **R$ 0,00** → total 100; custo de A (60) **conta** no Farol |

## 3. Casos de Farol consolidado

| # | Pedido | Esperado |
|---|---|---|
| **T13** | orçamento com serviço A (receita 50, custo 100 → linha VERMELHA) + serviço B (receita 500, custo 100 → linha VERDE) | consolidado = 550/200 = **275% → VERDE, não bloqueia** (a regra antiga da cor mais crítica daria vermelho). Linhas mantêm a própria cor |
| **T14** | produto X **sem Utiliza** (preço da casa 80, custo 60) + serviço Y (receita 100, custo 40) | receita X = 0; custo X conta → 100/100 = **100% → VERMELHO (≤ Vermelho = bloqueado)**. Se algum item estivesse sem custo ou sem preço → ROXO |

## 4. Casos de textos e de produto

| # | Entrada | Esperado |
|---|---|---|
| **T21** | serviço: cadastro nome "Consulta", código TUSS 10101012, código do cadastro vazio; no convênio: nome de conversão **vazio**, código **"X1"** | nome exibido = **Consulta** (vazio desce) · código = **X1** (nível 3) |
| **T22** | produto sem valor unitário no convênio (linha 🔁 vazia, FK da linha vazio, fonte da linha vazia); política do convênio p/ o tipo: tabela interna, Preço 1 = 50, FK 10; cadastro: fonte fixo, preço de venda 60 | valor = 50 × 1,10 = **55,00** (nível 2 vale para preço de produto) |

## 5. Casos complementares do kit (K1–K12) — derivados das regras do manual

Não estão numerados no manual; cada um cita a regra de origem.

| # | Entrada | Esperado | Regra |
|---|---|---|---|
| K1 | produto: valor unitário convertido 2,00, FK da linha vazio; política FK 10 | **2,00** (FK da política não se aplica a valor convertido) | árvore 3.2 |
| K2 | produto: valor unitário convertido 100, FK da linha 20 | **120,00** | árvore 3.2 |
| K3 | produto: sem convertido; linha FK 5; política fonte = tabela Preço 2 (valor 40), FK 10 | **42,00** (FK da linha herda campo a campo: 40 × 1,05) | herança campo a campo |
| K4 | produto: sem convertido; fonte resolvida = PRECO FIXO CADASTRADO (preço de venda 60); FK 25 | **60,00** (fixo não aplica FK) | fontes |
| K5 | produto: sem convertido; fonte = tabela interna Preço 1 **sem valor** para o produto; preço de venda 60; FK 10 | **66,00** (fallback preço de venda × FK) | árvore 3.2 |
| K6 | produto: sem convertido; nenhuma fonte na linha, política ou cadastro | **0,00** | árvore 3.2 |
| K7 | produto: valor unitário convertido **0** | **0,00** (não desce) | vazio ≠ zero |
| K8 | taxa: cadastro 40; convertido **0** | **0,00**; convertido vazio → **40,00** | árvore 3.3 |
| K9 | produto avulso (fora de pacote) com Z T, convertido 50 | **50,00** (Zerar nunca muda o avulso) | árvore 3.2 |
| K10 | serviço cad 100 somar F, P F; composição tem o mesmo taxa T 30 na raiz **e** dentro do sub [cad 0] | Σ = 160 (taxa conta duas vezes) → **alerta I3** | I3 |
| K11 | serviço R contém sub A; A contém R (ciclo) | o motor corta o ciclo pelo caminho visitado e emite **alerta de ciclo**; não entra em laço | ciclos |
| K12 | serviço somar T, V — , P T, produto A 50·T·T | Σ 50 (Pacote sem preço não fecha: V5) → **aviso** "Pacote sem efeito" | tabela-verdade V5 |

## 6. Invariantes I1–I13 (validar antes de concluir um convênio)

| # | Invariante (manual) | Como o motor verifica |
|---|---|---|
| I1 | Todo item de composição de serviço atendido tem Utiliza marcado no convênio | para cada serviço com U=T, listar itens com U=F; exigir decisão escrita ("não cobre") para cada um |
| I2 | Serviço com preço fechado tem Pacote marcado e itens inclusos com Zerar marcado | serviços cuja `origem`/decisão diz "pacote" → P=T, V ou fixo preenchido, e Z=T nos itens marcados como inclusos |
| I3 | Sem valor duplicado raiz × subserviço | mesma taxa/produto na raiz e em subserviço, ou valor extra no V da raiz **e** no sub → alerta |
| I4 | Nenhum serviço com valor convertido de R$ 0,01 | qualquer V = 0,01 (em serviço, produto ou taxa) → bloqueio até decisão escrita |
| I5 | Nenhum produto utilizado sem custo | produto com U=T numa composição e custo nulo/0 → ROXO previsto |
| I6 | receita_total = receita_servicos + receita_produtos + receita_taxas | Σ = base + Σ(produtos que entram) + Σ(taxas que entram) + Σ(subserviços), por recomposição |
| I7 | Valor de cadastro = 0 quando "somar itens" está marcado | somar T e `cad ≠ 0` → aviso (o sistema zera o valor fixo ao ligar somar) |
| I8 | Serviço que soma itens tem ao menos um item que conta no total, ou valor convertido preenchido | somar T, V vazio e nenhum item com conta = Sim → alerta "Σ = 0" (sintoma do orçamento R$ 0,00) |
| I9 | Preço fixo com composição e sem Pacote: confirmado que os itens são cobrados à parte | somar F, P F, composição não vazia → exigir decisão escrita "itens à parte"; senão sugerir P + Z |
| I10 | Em pacote fechado, todo item incluso dentro de subserviços tem o próprio Zerar | sub com Z=T dentro de pacote fechado cujos itens estão marcados como inclusos mas com Z=F → alerta |
| I11 | Linha ✅ = base; Farol e Farol › Itens = total | comparar `base` com `receita_propria_servico` e `Σ` com `receita_total` de `/farol/servicos` |
| I12 | Valor combinado não é pacote | serviço com V preenchido, P=F e decisão "preço fechado" → erro; nunca concluir que V embute itens sem P=T |
| I13 | Linha Σ = valor(S,C) = receita do Farol do serviço | `Σ` simulado = `receita_total` lido (tolerância R$ 0,01) |

## 7. Formato sugerido para os testes Python

```python
# ferramentas/conversao/tests/test_manual.py (exemplo de um caso)
def test_T23_valor_combinado_sem_pacote_nao_e_pacote():
    r = servico(cad=100, somar=False, conv=dict(V=100, P=False),
                itens=[produto("A", 50, Z=True, U=True), taxa("B", 30, Z=True, U=True)])
    assert r.sigma == 180 and r.base == 100
```

Os testes devem cobrir **T1–T26 + K1–K12** e as 13 invariantes. Resultado
diferente do esperado = o motor está errado (ou o manual mudou: confira a
data de "Conferido em" e reabra o manual).
