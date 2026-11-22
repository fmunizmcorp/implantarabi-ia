# F003 — Chave recusada: 401 "Token de integração inválido, revogado ou expirado."

- **Rotas:** qualquer
- **Status HTTP:** 401 | 503
- **Mensagem contém:** Token de integração inválido | revogado ou expirado | Chave de API inválida | Token não fornecido | Não foi possível validar a chave
- **Causa:** confirmada — chave/token vencido, revogado, renovado (o valor antigo morre na hora), digitado errado ou ausente
- **Status:** comportamento esperado. **Medido em 22/11/2026:** chave `rbk_` falsa, token `rbt_` falso e requisição sem cabeçalho → todos **401**. O 503 que o kit mediu em 25/09 (defeito nº 1) **não acontece mais**; 503 hoje = falha de rede/validação do lado do Rabi
- **Origem:** medições de 24–25/09 e 22/11/2026

## O que fazer
Pare na primeira recusa (o `cliente.py` já para). Depois, conforme o tipo:
- **Token `rbt_`** (recomendado): o administrador da clínica abre **Configurações › Parâmetros ›
  Integrações**, confere se o token está ativo e no prazo e, se venceu, clica **Renovar** — isso gera
  um valor **novo** e invalida o anterior. Troque `RABI_API_KEY` (ou a linha `api_key:`) e rode
  `testar_chave.py`.
- **Chave `rbk_`**: peça a nova ao time Rabi pelo mesmo canal da atual.
- Recebeu **503**? Espere alguns minutos e tente **uma** vez; persistindo, é o Rabi (status/rede), não a chave.

Previna: o cabeçalho `X-ApiKey-Expires-At` (UTC) diz quando vence; token sem validade não manda o
cabeçalho. Detalhe: [../api-externa/chave-e-token.md](../api-externa/chave-e-token.md).

## O que NÃO fazer
Não repetir em loop. Nunca pedir a chave/token no chat. Não renovar o `rbt_` "por via das dúvidas"
com outra sessão usando o mesmo valor (ela cai na hora).
