# F011 — Na tela do convênio "não consigo editar" / "salvei e não gravou"

- **Rotas:** tela do convênio (não é erro da API)
- **Status HTTP:** —
- **Mensagem contém:** Liberar para edição | modo visualização | não salvou
- **Causa:** confirmada no manual (produção desde 29/09–02/10/2026, #632/#638) — o convênio salvo abre
  **só para leitura**. Para mudar: **Liberar para edição** → alterar → **Salvar** no cabeçalho. Desde 01/10
  as abas gravam **só** pelo Salvar do cabeçalho (sair da aba sem salvar perde a mudança). Cada aba tem
  histórico de alterações (#638)
- **Status:** comportamento da tela
- **Origem:** manual oficial

## O que fazer
Quando guiar uma pessoa na tela (ou pedir a conferência visual), diga a sequência completa: Liberar
para edição → alterar → Salvar no cabeçalho → conferir. Pela API as abas (`PUT /convenios/{id}/...`)
seguem gravando direto — e a tela mostra o resultado no histórico da aba.

Outras regras da mesma tela que confundem:
- Coluna **Atende** (#628): serviço de especialidade que o convênio não atende aparece "Não atendida" e
  **não aceita Utiliza** — cadastre a especialidade no convênio antes.
- Para gerar contas a receber, o convênio precisa da **conta de recebimento** preenchida.

## O que NÃO fazer
Não concluir "a API não gravou" pela tela sem recarregar e olhar o histórico da aba.
