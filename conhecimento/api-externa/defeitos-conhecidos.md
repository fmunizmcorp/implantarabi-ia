# Defeitos conhecidos da API externa — o que foi corrigido, o que resta, como detectar

> **Fonte:** experiência de implantação real (medições de 24/09/2026, tarde e noite, só leitura) · Swagger de 25/09/2026 (descrições das rotas, snapshot `spec/openapi-2026-09-25.json`) · https://www.rabisistemas.com.br/manual/api-externa/index.html#novidades · https://www.rabisistemas.com.br/manual/api-externa/erros-e-boas-praticas.html#armadilhas · **Conferido em:** 2026-09-25
> **Vale para:** produção em 25/09/2026 · **Kit:** v0.1.0

Status honesto: **"corrigido (medido)"** = medido em produção depois da correção;
**"corrigido (declarado)"** = o manual/Swagger de 25/09 diz que entrou em produção, mas o
kit ainda não mediu — o cliente continua tolerante ao comportamento antigo.

## 1. Quadro geral

| # | Defeito | Status em 25/09/2026 | Como detectar em execução | O que o kit faz |
|---|---|---|---|---|
| 1 | Chave inválida ou revogada responde **503** (`"Não foi possível validar a chave de API."`); a documentação promete 401 | **NÃO corrigido na prática**: o manual/Swagger de 25/09 dizem "chave rejeitada = 401", mas **medido em 25/09/2026 03:07**: chave inexistente → **503**; sem cabeçalho → 401 `"Token não fornecido."` | 503 que não passa na 2ª tentativa | `cliente.py`: 1 nova tentativa e depois `ChaveInvalida` — **sem loop** |
| 2 | Rotas `PUT`/`PATCH` sem dizer se sobrescrevem ou mantêm | mitigado: o Swagger agora manda tratar como sobrescrita toda rota que não declare; 39 de 53 continuam sem declarar | foto depois + diff mostra campo que sumiu | regra do kit: GET → altera → PUT completo ([convencoes.md](convencoes.md) §4) |
| 3 | Swagger se contradizia sobre criar login | corrigido (medido 24/09 noite): existe `POST /colaboradores/{id}/usuario` | `409` = já tem login | criar login só com lista aprovada |
| 4 | 4 listagens fora do envelope `dados` (`/tabelas-preco` lista crua; `/orcamentos` `{message,data}`; `/financeiro/movimentacoes` `{data,meta}`; `/estoque/saldo-produtos` `{items…}`) | corrigido (declarado 25/09) | `normalizar_envelope()` informa o formato lido em `ultima_leitura["formato"]` | o cliente aceita os 5 formatos |
| 5 | Rotas sem paginação real (`/estoque` devolvia 7,9 MB; grades e agenda devolviam tudo) | `/estoque`: corrigido (medido 24/09). Grades e `/agendamentos`: corrigido (declarado 25/09 — agenda exige `data`) | `pageSize` da resposta maior que o pedido | ler com filtros; `ler_tudo()` confere total |
| 6 | `GET /faturamento/divergencias` respondia 500 | corrigido (medido 24/09) | — | — |
| 7 | `GET /atendimentos/historico` exigia `pacienteId` sem declarar (erro genérico) | corrigido (medido 24/09): declarado; erro `"Informe pacienteId."` | 400 | sempre mandar `pacienteId` |
| 8 | Faltava `equipamento:read` na chave | corrigido (medido 24/09) | 403 em `/equipamentos` | `testar_chave.py` mostra |
| 9 | Operações sem schema de resposta | melhorou: 155 schemas no Swagger de 25/09 (eram 91 operações sem schema em 24/09) | — | ler a descrição da rota |
| 10 | "Valores sempre em reais" tinha exceções | corrigido no texto (25/09): "reais na maioria"; exceções ditas por rota | somas 100× maiores | tabela de centavos em [convencoes.md](convencoes.md) §3 |
| 11 | Validade da chave só se descobria no 401 | corrigido (declarado 25/09): cabeçalho `X-ApiKey-Expires-At` | cabeçalho ausente = chave antiga/servidor antigo | `cliente.validade`, alerta < 15 dias |
| 12 | `/farol/itens` sem filtro de serviço ativo (listava serviços desativados: contagens infladas) | corrigido (declarado 25/09): filtro `servicoAtivo` | total de raízes muito maior que os serviços ativos | usar `apenasAtivosNoConvenio=true&servicoAtivo=true`; cruzar com `GET /servicos?ativo=true` |

## 2. Defeitos que o Swagger de 25/09 **declara em aberto** ("reportado ao time")

| Rota | Defeito | Como detectar | Contorno |
|---|---|---|---|
| `POST /parametros/desconto/colaborador/{id}` | por chave **sempre 401** (código fixa `isAdmin=false`), mesmo com a permissão. `nivel` vai na **query**, não no corpo | 401 nesta rota | pela **tela**. O cliente não confunde com chave inválida |
| `POST /parametros/alcada-compra/colaborador/{id}` | mesmo defeito: sempre 401 | idem | pela tela |
| `POST /parametros/acolhimento/atualizar-validacoes/{pacienteId}` | sempre 401 (a chave não carrega colaborador) | idem | pela tela |
| `PUT /faturamento/glosas/produto` · `/taxa` · `/servico` | `motivoGlosado` inexistente devolve **401** (parece chave); `valorPagoGlosa` em **centavos**; o id do corpo é o da linha de **conversão** (`produtoConvercao`/`taxaConvercao`/`servicoConversao`), apesar do nome `ProdutoAtendimentoId` | 401 nestas rotas | conferir o motivo em `GET /faturamento/glosas/motivos` |
| `POST /grades-equipamento`, `PUT` e `DELETE /grades-equipamento/{id}` | **gravam certo e devolvem 500** (erro depois do commit) | 500 nestas rotas | **não repetir**: reler com `GET /grades-equipamento?equipamentoId=…` e comparar |
| `PUT /grades-colaborador/{id}` | o `{id}` do caminho é **ignorado**; o corpo é **lista direta** e cada item leva o próprio `id`. Grade inexistente vira **500**, não 404 | 500 | conferir o `id` no corpo antes; reler depois |
| `POST /tabelas-preco/produtos` | responde **antes de gravar** (corpo vazio) — sucesso não garante gravação | corpo vazio no sucesso | sempre `GET /tabelas-preco/produtos?id=<tabela>` depois (o ritual já faz) |
| `GET /agendamentos/motivo-cancelamento` | em erro de banco responde **200 com o número `401` no corpo** | corpo = `401` | o cliente levanta `ErroRabi` ("erro disfarçado") |
| `GET /estoque/historico/{id}` | sem paginação real (histórico completo do produto) | resposta grande | usar por produto, com cuidado |
| `POST /atendimentos` | grava sempre a data/hora de **agora** | data do atendimento = hoje | em seguida `PUT /atendimentos/{id}` com `horarioInicio` real e `responsavelId` (repita `pacienteId`/`empresaId`) |
| `PUT /parametros/desconto`, `PUT /parametros/financeiro` | atualizam "a primeira linha que existir" (`findFirst` sem filtro) | — | GET antes e depois |
| `GET /orcamentos` | o **formato do item muda** conforme `pacienteId` é informado ou não; sem `pacienteId`, a página é filtrada depois de paginar | itens com campos diferentes; `dados` menor que `pageSize` | tratar os dois formatos; percorrer por `totalPages` |

## 3. Pontos de atenção que não são defeito, mas derrubam scripts

- Respostas sem configuração: `0` cru (`/parametros/orcamento`), `null` com 200
  (`/parametros/acolhimento`, `/servicos-online`, `/termo`), 404 (`/parametros/desconto`).
- `POST /taxas` responde 200 (não 201); vários `PUT` respondem 202.
- `registroANS` (criação) × `codigoANS` (atualização) no convênio; `somarItems` (escrita)
  × `somarItens` (leitura) no serviço.
- UF por extenso em operadora e colaborador (sigla dá 404).
- `GET /faturamento/guias/pacientes` limitado a 50 por padrão.

## 4. Como a sessão da clínica reporta um defeito novo

1. Reproduza **só com leitura**, se possível. Guarde a resposta (sem dado pessoal e sem a
   chave) em `provas/`.
2. Registre em `historico/APRENDIZADOS.md` da clínica.
3. Se servir a todas as clínicas, sugira ao mantenedor do kit (issue no repo do kit, **sem
   dado da clínica**) — ele atualiza este arquivo e, se for o caso, o `cliente.py`.
4. Depois de cada atualização do Swagger (`python3 -m ferramentas.rabi_api.atualizar_spec`),
   o mantenedor revisa este quadro: `grep -rn -i "reportado\|bug conhecido" conhecimento/api-externa/rotas/`.
