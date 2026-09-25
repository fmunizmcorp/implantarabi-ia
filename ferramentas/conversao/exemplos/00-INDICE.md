# Índice — exemplos (cenário fictício "Convênio A")

> **Fonte:** cenário inventado para o kit, regras do manual https://www.rabisistemas.com.br/manual/precos/arvore-de-decisao.html#exemplos · **Conferido em:** 2026-09-25
> **Vale para:** produção desde 23–25/09/2026 · **Kit:** v0.1.0

Todos os nomes, ids e valores são **fictícios** (Clínica Exemplo · Convênio A).

| Arquivo | O que tem | Quando usar |
|---|---|---|
| `cenario-convenio-a.json` | Catálogo (4 produtos, 2 taxas, 5 serviços) + convênio: consulta simples (301), aplicação com subserviço (302), medicamento aplicado em conta aberta (303), curativo em pacote fechado com Zerar (304), serviço inativo (305) | Modelo do formato de cenário |
| `precos-convenio-a.csv` | O mesmo convênio no formato do CSV, com origem | Modelo do CSV |
| `precos-com-erros.csv` | CSV com 0,01, coluna fora da aba e linha sem origem | Ver as validações |
| `atual-convenio-a.json` | Foto "antes" fictícia dos GET das abas | Ver a prévia de → para |
| `farol-servicos-convenio-a.json`, `farol-itens-convenio-a.json`, `farol-produtos-convenio-a.json` | Respostas simuladas dos GET do Farol | Ver a conferência |

Totais previstos: 301 = R$ 180,00 · 302 = R$ 121,00 · 303 = R$ 176,00 (✅ 0,00) · 304 = R$ 120,00.
