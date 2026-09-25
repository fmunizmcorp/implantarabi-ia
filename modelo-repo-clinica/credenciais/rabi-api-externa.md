# Rabi — API externa (chave rbk_) · <NOME_DA_CLINICA>

> Texto claro por decisão do proprietário. Repo **privado**. Como a chave
> funciona: `.kit/conhecimento/api-externa/` (autenticação e chave).

api_key: <cole aqui>

| Campo | Valor |
|---|---|
| Base (produção) | https://api.rabisistemas.com.br/api/v1/integrations |
| Base (homologação) | https://api.hmg.rabisistemas.dev/api/v1/integrations |
| Ambiente desta chave | prd · hmg |
| Cabeçalho | `Authorization: Bearer <a chave acima>` |
| Documentação oficial | https://api.rabisistemas.com.br/external-docs/ |
| Entregue por / em | |
| Validade (`X-ApiKey-Expires-At`) | (preenchido por `testar_chave.py`) |
| Renovação | pelo time Rabi (sem autoatendimento); pedir **15 dias antes** de vencer |
| Segredo de ambiente | `RABI_API_KEY` configurado no Claude web? sim · não |

## Permissões testadas (`python3 .kit/ferramentas/rabi_api/testar_chave.py`)

| Área | Leitura | Escrita | Testado em |
|---|---|---|---|
| (preenchido pela ferramenta) | | | |

## Cuidados
- A chave **grava de verdade em produção**. Nada se grava sem prévia e aprovação.
- Chave inválida ou revogada: a documentação diz **401**; na prática já respondeu
  **503**. Trate os dois como problema de chave — **sem retry em laço**.
- Revogada pode continuar aceita por alguns segundos.

## Histórico de chaves (não apagar: rastreia qual chave assinou cada gravação)

| Chave | Situação (ativa/revogada/vencida) | Vigência | Permissões | Usada em |
|---|---|---|---|---|
| | | | | |
