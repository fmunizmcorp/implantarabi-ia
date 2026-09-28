# F003 — Chave recusada: 503 "Não foi possível validar a chave de API." ou 401

- **Rotas:** qualquer
- **Status HTTP:** 503 | 401
- **Mensagem contém:** Não foi possível validar a chave | Token não fornecido
- **Causa:** confirmada — chave vencida, revogada, ainda não ativada ou ausente (a validade curta é proteção)
- **Status:** comportamento esperado (o 503 no lugar do 401 é defeito conhecido nº 1)
- **Origem:** medições de 24–25/09/2026

## O que fazer
Pare na primeira recusa (o `cliente.py` já faz 1 nova tentativa e para). Peça chave nova ao
dono/time Rabi e troque `RABI_API_KEY` no ambiente. Detalhe:
[../api-externa/chave-e-token.md](../api-externa/chave-e-token.md) ·
[../api-externa/defeitos-conhecidos.md](../api-externa/defeitos-conhecidos.md) (nº 1).

## O que NÃO fazer
Não repetir em loop. Nunca pedir a chave no chat.
