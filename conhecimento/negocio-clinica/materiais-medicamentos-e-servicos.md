# Materiais, medicamentos e serviços — como a clínica usa e como cadastrar

> **Fonte:** https://www.rabisistemas.com.br/manual/modulos/estoque.html#cadastrar-produto · `precos/index.html#servico-composto` · `precos/guia-clinica.html#parte-4-receitas` · `modulos/configuracoes.html#servicos` · experiência de implantação real num centro de infusão (generalizada) · **Conferido em:** 2026-09-25
> **Vale para:** Rabi em produção em 25/09/2026 · **Kit:** v0.1.0

## 1. Três tipos de item

| Item | O que é | Exemplo | Onde se cadastra |
|---|---|---|---|
| **Serviço** | O que a clínica faz e cobra | Consulta, exame, "aplicação endovenosa", "medicamento X aplicado" | Configurações → Serviços (código TUSS 22) |
| **Produto** | O que se consome e tem estoque | Medicamento, soro, equipo, seringa, luva, curativo | Estoque → Produtos (tipo, fabricante, depósito) |
| **Taxa** | Cobrança acessória | Taxa de sala, de material, de observação | Configurações → Taxas |

Um serviço pode ter **composição**: produtos, taxas e **subserviços** que ele
consome. A composição serve para três coisas: **cobrança** (os itens entram na
guia), **custo** (o Farol) e **estoque** (baixa no atendimento).

## 2. O padrão "aplicação + medicamento"

Numa clínica de infusão/injeção, o jeito que funciona:

```
Serviço "Medicamento X aplicado EV"  (soma itens = ligado; código TUSS da terapia)
 ├─ Subserviço "Aplicação endovenosa"   (preço fixo da aplicação)
 │    ├─ Produtos: soro, equipo, cateter, seringa, agulha, swab, luva, curativo, gaze
 │    └─ Taxas: sala / observação (se o contrato cobra)
 └─ Produto "Medicamento X" (quantidade por aplicação)
```

- "Definir preço do serviço pelos itens" (**somar itens**) **ligado** no
  serviço de medicamento: o preço é a aplicação + o medicamento. Em uma
  implantação real, uma sessão de IA concluiu o contrário ("desligar somar
  itens") e o gestor corrigiu: é justamente esse campo que faz a soma — é o
  conceito.
- Vias diferentes = aplicações diferentes (endovenosa, intramuscular,
  subcutânea), cada uma com o seu preço fixo e materiais.
- **Não crie referência circular** (serviço A dentro de B e B dentro de A):
  infla a receita do Farol. Aconteceu numa implantação real e deixou o Farol
  mostrando receita que não existia.
- Mesmo procedimento com dois cadastros (duplicado, mesmo código TUSS) gera
  confusão de agenda e de guia — unifique e inative o sobrante.

## 3. Pacote × conta aberta

- **Conta aberta** (padrão): cada item com Utiliza entra na conta com o seu
  preço convertido. Sem Pacote e sem Zerar.
- **Pacote de preço fechado** (quando o contrato ou a clínica cobra um preço
  único por tudo): valor combinado na linha 🔁 do serviço **+ Pacote** marcado
  na linha do serviço (no convênio) **+ Zerar valor em pacotes** em cada item
  **incluso**. O serviço raiz não é zerado. Item não incluso fica sem Zerar e
  continua cobrado à parte.
- **Valor combinado sozinho não é pacote**: os itens continuam somando por cima.
- Os itens têm preço cadastrado mesmo quando estão num pacote, porque **podem
  ser usados fora dele** — aí precisam ser cobrados.

Detalhe, árvores e testes: [../precos-e-conversao/00-INDICE.md](../precos-e-conversao/00-INDICE.md).

## 4. O que normalmente não é cobrado do convênio

| Item | Configuração usual | Porquê |
|---|---|---|
| Manipulados | Sem Utiliza | Operadoras não pagam; custo continua no Farol |
| Vacinas | Sem Utiliza (no convênio) | Em geral não cobertas; particular pode cobrar |
| Material de limpeza | Sem Utiliza | Não é item de paciente |
| Item sem correspondência nas tabelas | Sem Utiliza até haver regra | Sem código/preço não há cobrança válida |
| Item que o convênio não paga, mas precisa ficar disponível | Utiliza com **0,00** (zero real) — só quando o contrato diz que é incluso/zero | Zero é zero; **0,01 nunca** |

Confirme cada categoria com a clínica: é decisão de negócio.

## 5. Estoque na prática

- **Depósito**: pelo menos 1 por unidade (farmácia/almoxarifado); cada local de
  atendimento aponta para um depósito padrão de saída **ativo**.
- **Estoque Atual** (mínimo) por produto → item CRÍTICO e previsão no
  agendamento.
- **Lote e validade** controlados nas entradas (movimentação; importação de
  NF-e de fornecedor carrega estoque e contas a pagar).
- **Baixa no atendimento**: o consumo sai vinculado ao atendimento que consumiu.
  O **pré-faturamento não baixa mais estoque** (desde set/2026).
- Produtos controlados: board mostra "faltam X de Y" (previsto × agendado).
- **Reserva de medicamento** para o agendamento (em produção desde ago/2026).
- **Não confunda preço com saldo:** em uma implantação real, uma leitura de
  "valor unitário" num endereço de produto trazia **saldo de estoque**
  (negativo), não preço. O preço de catálogo se lê pela rota de preço/conversão.

## 6. Perguntas úteis à clínica

1. "Quais serviços vocês fazem com medicamento? Por quais vias?"
2. "A aplicação tem preço próprio? Muda por via?"
3. "Quais materiais entram em cada aplicação, e em que quantidade?"
4. "Algum preço é fechado (pacote)? O que está incluso?"
5. "Manipulados, vacinas e limpeza: cobram de alguém?"
6. "Em qual depósito fica cada coisa? Controlam lote e validade?"
