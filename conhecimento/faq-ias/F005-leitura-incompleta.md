# F005 — A contagem lida pela API não bate com a tela / leitura "vazia"

- **Rotas:** listagens (GET com page/pageSize)
- **Status HTTP:** 200 | 400
- **Mensagem contém:** page | pageSize
- **Causa:** confirmada — `page` começa em 1, `pageSize` máximo 200; é preciso ler até `totalPages`; 200 com corpo vazio é leitura falha
- **Status:** documentado
- **Origem:** implantação real anterior

## O que fazer
Use `ler_tudo()` do `ferramentas/rabi_api/cliente.py` (confere o total). Filtros de ativo
podem explicar diferenças com a tela. Detalhe:
[../api-externa/convencoes.md](../api-externa/convencoes.md) e
[../licoes-aprendidas/dados-e-leitura.md](../licoes-aprendidas/dados-e-leitura.md).
