# `rabi_api` — cliente da API externa do Rabi (só biblioteca padrão)

> **Fonte:** Swagger https://api.rabisistemas.com.br/external-docs/ · manual https://www.rabisistemas.com.br/manual/api-externa/ · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger de 25/09/2026) · **Kit:** v0.1.0

Tudo roda da **raiz do repo**. No kit: `python3 -m ferramentas.rabi_api.<modulo>`. No repo
da clínica (kit em `.kit/`): `PYTHONPATH=.kit python3 -m ferramentas.rabi_api.<modulo>` —
assim os caminhos (`provas/…`, `credenciais/…`) continuam relativos à raiz da clínica.
Python 3.11, sem `pip install`.

## 1. Chave e ambiente

Ordem de busca: `RABI_API_KEY` (segredo de ambiente do Claude web) → linha
`api_key: rbk_...` em `credenciais/rabi-api-externa.md` (procurado na pasta atual e nas de
cima) → erro `ChaveAusente` com instruções. Base: `RABI_API_BASE` ou produção
(`https://api.rabisistemas.com.br/api/v1/integrations`). Homologação:
`RABI_API_BASE=https://api.hmg.rabisistemas.dev/api/v1/integrations`.
A chave **nunca** é impressa (aparece como `rbk_…abcd`). Detalhes:
`conhecimento/api-externa/chave-e-token.md`.

## 2. Testar a chave (sempre no começo)

```bash
python3 -m ferramentas.rabi_api.testar_chave --saida provas/S00/teste-chave-2026-10-01.md
```
Tabela área → OK / SEM PERMISSÃO / CHAVE, validade e dias restantes (alerta < 15).
Sai com código 1 se a chave foi recusada (401/503) — sem repetir em loop.

## 3. Usar o cliente

```python
from ferramentas.rabi_api.cliente import ClienteRabi, ErroRabi, resumo_lote

c = ClienteRabi()                                  # chave e base automáticas
empresas = c.ler_tudo("/empresas")                 # todas as páginas, total conferido
servicos = c.ler_tudo("/servicos", {"ativo": True})
print(c.ultima_leitura)                            # lidos, total, páginas, formato do envelope
um = c.get("/servicos/46")                         # falha se status≠2xx ou corpo vazio

# PUT: GET antes, altera só o que muda, reenvia o objeto COMPLETO
obj = c.get("/servicos/46"); obj["valor"] = 40.0
c.put("/servicos/46", obj)

# lote: fatia no limite, lê 207 por indice, devolve o que reenviar
rel = c.enviar_lote("/produtos/bulk", "produtos", lista_de_produtos, tamanho=50)
print(resumo_lote(rel)); pendentes = rel["reenviar"]   # só ERRO/NAO_PROCESSADO

# abas do convênio (upsert, até 200; colaboradores até 100)
c.enviar_lote("/convenios/12/servicos", "servicos", itens, tamanho=200, metodo="PUT")

print(c.validade, c.dias_restantes())              # X-ApiKey-Expires-At
```

Exceções: `ChaveAusente`, `ChaveInvalida` (401, ou 503 que persiste), `SemPermissao` (403,
diz a permissão), `LeituraIncompleta` (lidos ≠ total), `FormatoInesperado`, e `ErroRabi`
para o resto (tem `.status`, `.corpo`, `.mensagem_servidor()`). 429: espera 5/10/20 s e
tenta de novo (máx. 3). Rotas em que 401 é defeito conhecido (não chave) viram `ErroRabi`
com explicação.

## 4. Foto e diff (ritual de toda gravação)

```bash
P=provas/S05/taxas/2026-10-01
python3 -m ferramentas.rabi_api.foto antes  --caminho /taxas --param ativo=true --destino $P
# … prévia, aprovação, gravação …
python3 -m ferramentas.rabi_api.foto depois --caminho /taxas --param ativo=true --destino $P
python3 -m ferramentas.rabi_api.foto diff --destino $P        # grava $P/diff.txt
```
Em Python: `foto(c, caminho, destino, "antes")` e `diff(antes_json, depois_json)`.
Dados pessoais (CPF, e-mail, telefone, nascimento…; e o nome em pacientes, atendimentos,
agenda, orçamentos e tomadores) saem mascarados. `--unico` = GET sem paginar.

## 5. Atualizar o spec (mantenedor do kit)

```bash
python3 -m ferramentas.rabi_api.atualizar_spec --relatorio historico/mudancas-swagger.md
```
Baixa `swagger-ui-init.js`, extrai `swaggerDoc`, salva `spec/openapi-AAAA-MM-DD.json` (só se
mudou), lista operações adicionadas/removidas/alteradas e regenera `rotas/`. Offline:
`--arquivo-js caminho.js`. Só o gerador: `python3 -m ferramentas.rabi_api.gerar_rotas`.
Se o proxy exigir certificado próprio, defina `SSL_CERT_FILE`.

## 6. Testes

```bash
python3 -m pytest ferramentas/rabi_api -q
```
Servidor HTTP falso local (sem rede): envelopes, paginação, 207, 429, 401/403/503, corpo
vazio, máscara; e o gerador conferindo as 268 operações.
