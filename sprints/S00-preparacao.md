# S00 — Preparação

> **Fonte:** https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-0 · https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#inicio-rapido · spec `conhecimento/api-externa/spec/openapi-2026-09-25.json` · **Conferido em:** 2026-09-25
> **Vale para:** produção (API externa, Swagger de 25/09/2026) · **Kit:** v0.1.0

## Objetivo

Ter a chave testada, o repo privado da clínica pronto, o pedido único de
documentos enviado, o inventário do que chegou, a **foto inicial de tudo que já
existe no Rabi** e o plano da clínica por porte — antes de gravar qualquer coisa.

## Link do manual

- Passo 0 da implantação pela API: https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-0
- Passo 0 do início rápido (ambiente pelo site): https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#inicio-rapido
- Como escolher o modelo por porte: https://www.rabisistemas.com.br/manual/implantacao/index.html#como-escolher

## Depende de

Nada. É a porta de entrada. Se o ambiente da clínica ainda não existe, o
cadastro é self-service em www.rabisistemas.com.br (escolher plano e pagar):
**decisão comercial da clínica** — a IA explica e espera; não contrata nem paga.

## Documentos a pedir

A lista inteira, uma vez: [lista única](../metodologia/lista-unica-de-documentos.md)
(versão curta ⭐ para consultório individual). Para destravar a S01 são
indispensáveis **CL-1** e **CL-3**.

## Índice de dados a coletar

| dado | campo API | obrigatório? | onde costuma estar no material do cliente | padrão sugerível | pergunta ao usuário se faltar |
|---|---|---|---|---|---|
| Chave da API da clínica | cabeçalho `Authorization: Bearer rbk_…` | sim | portal comercial do Rabi (mostrada uma única vez) | — | "Você já gerou a chave de integração do Rabi para a clínica? Ela começa com rbk_. Guarde no segredo do ambiente com o nome RABI_API_KEY." |
| Validade da chave | cabeçalho `X-ApiKey-Expires-At` | sim (registrar) | vem na 1ª resposta da API | — | (a IA lê sozinha) |
| Ambiente (produção ou homologação) | base `https://api.rabisistemas.com.br/api/v1/integrations` ou `https://api.hmg.rabisistemas.dev/api/v1/integrations` | sim | quem gerou a chave sabe | produção só com autorização | "Esta chave é do ambiente de teste ou do sistema de verdade da clínica?" |
| Repo da clínica é privado? | — | sim | GitHub da clínica | privado | "Seu repositório no GitHub está como privado? Ele vai guardar senhas." |
| Porte da clínica | — | sim | CL-3, PE-1, CV-1 | o menor dos dois em dúvida | "Quantos profissionais atendem e em quantos endereços?" |
| Papéis (dono, implantador) | `PAPEIS.md` do repo | sim | conversa | — | "Quem vai aprovar o que eu cadastrar: você ou outra pessoa?" |
| Sistema anterior | — | não | SA-4 | — | "A clínica usa outro sistema hoje? Qual?" |
| Data desejada de go-live | — | não | conversa | pela tabela de porte | "Tem uma data em mente para começar a atender pelo Rabi?" |

## Fila de perguntas

1. Modo da sessão (Implantação / Atualização / Convênio / Diagnóstico) — ver
   [modos de sessão](../metodologia/modos-de-sessao.md).
2. Chave (se não estiver no segredo do ambiente) e ambiente.
3. Quem aprova (papéis).
4. Porte (confirmar o que a IA deduziu dos documentos).
5. **Enviar o pedido único de documentos** (uma mensagem só).
6. Data desejada de go-live.

Confirmar: o que a IA já deduziu (porte, papéis). Pedir: a chave e a autorização
de ambiente. Nunca perguntar o que a API responde sozinha.

## Enriquecimento possível

- Se a sessão tiver acesso à internet: dados públicos do CNPJ (razão social,
  endereço), CNES público do estabelecimento, lista de operadoras ativas da ANS.
  Sempre como **sugestão com origem**, confirmada depois nas sprints.

## Leitura do que já existe no Rabi — a FOTO INICIAL DE TUDO

**Nada existente é sobrescrito sem prévia.** A foto inicial é o seguro da
clínica e a base para "não criar de novo". Salvar em `provas/S00/foto-inicial/`:

| Área | Leitura (percorrer todas as páginas; `pageSize` até 200) |
|---|---|
| Empresas/unidades | `GET /empresas` (lista inteira, ativas e inativas) |
| Depósitos | `GET /depositos` |
| Locais | `GET /locais` |
| Auxiliares (14) | `GET /auxiliares/tipos-produto`, `tipos-codigo`, `tabelas-ans87`, `regimes-atendimento`, `tipos-servico`, `tipos-guia`, `tipos-taxa`, `unidades-medida`, `principios-ativos`, `sexos`, `estados-civis`, `conselhos-profissionais`, `unidades-federativas`, `tipos-atendimento` |
| Operadoras | `GET /operadoras` (+ `GET /operadoras/{id}` para os planos) |
| Fornecedores / Fabricantes | `GET /fornecedores`, `GET /fabricantes` |
| Taxas / Produtos / Equipamentos | `GET /taxas`, `GET /produtos`, `GET /equipamentos` |
| Serviços | `GET /servicos` (resumida) e `GET /servicos/{id}` para os compostos |
| Tabelas de preço interna | `GET /tabelas-preco` (confira o formato: já foi lista crua) |
| Colaboradores | `GET /colaboradores` |
| Convênios | `GET /convenios` + as 6 abas de cada um + `farol/servicos` |
| Grades | `GET /grades-colaborador`, `GET /grades-equipamento` (filtrar por colaborador/local) |
| Parâmetros | `GET /parametros/orcamento`, `/financeiro`, `/estoque`, `/desconto`, `/acolhimento`, `/termo`, `/avisos` |
| Pacientes | **só a contagem** (`total` de `GET /pacientes?page=1&pageSize=1`) — nenhum dado pessoal no repo |

Resumo em `provas/S00/foto-inicial/RESUMO.md`: por área, quantos registros,
quantos ativos, e o que chama atenção (duplicatas, nomes estranhos, inativos).
Se a clínica **não** está vazia, a implantação vira "completar e corrigir": cada
sprint compara documento × Rabi antes de propor.

Respostas-armadilha já documentadas: `GET /parametros/orcamento` sem
configuração devolve o número `0` cru; `acolhimento`, `servicos-online` e
`termo` podem devolver `null` com 200; `GET /parametros/desconto` devolve 404 se
nunca configurado — nada disso é erro de chave.

## Gravação

Nenhuma gravação no Rabi nesta sprint. Gravações só no repo da clínica:
`credenciais/rabi-api-externa.md` (base, validade, permissões alcançadas — a
chave em si preferencialmente no segredo `RABI_API_KEY`), `ESTADO.md`,
`PAPEIS.md`, `documentos-do-cliente/inventario.md`, `pendencias/LACUNAS.md`.

**Teste da chave:** `GET /empresas` → 200; ler `X-ApiKey-Expires-At`; testar a
leitura das 25 áreas (ferramenta do kit `ferramentas/rabi_api/testar_chave.py`)
e registrar quais áreas a chave alcança. 403 numa área = a chave não tem aquela
permissão: anotar e pedir ao time Rabi uma chave com o kit de implantação.
401/503 = problema com a chave: parar, sem repetir em laço. Se a chave vence
antes do fim previsto da implantação, pedir a nova **agora** (não há renovação
automática nem autoatendimento).

**IDs que só existem na tela** (não há rota de listagem na API externa) — anotar
no dicionário de IDs quando a sprint precisar: especialidades (catálogo),
categorias de pagamento, contas/caixas, centros de custo, motivos de
movimentação de estoque, kits de documentos, modelos de XML do convênio, tipos
de contrato, tipos de anexo, perfis de permissão, fontes de preço de compra.

## Prova

- `provas/S00/teste-chave.md`: status por área, validade, data.
- `provas/S00/foto-inicial/` + `RESUMO.md`.
- `documentos-do-cliente/inventario.md` com o que chegou.
- Mensagem do pedido único gravada em `historico/requisitos/raw/`.

## Armadilhas desta sprint

- Repo público com credencial: **não fazer push** de credenciais até o dono
  decidir; avisar por escrito, sem apagar nem mascarar nada.
- `page=0` na API externa devolve 400 (começa em 1); `pageSize` máximo 200.
- Parar a leitura quando uma página vem menor que `pageSize` — errado; vá até
  `totalPages`.
- Leitura com 200 e corpo vazio = leitura falhada.
- Tratar 503 como instabilidade e repetir em laço.
- Chave com permissões demais usada na integração contínua depois: no go-live, a
  chave de implantação é revogada ou reduzida (S16).

## Definition of Ready / Definition of Done

**DoR:** repo da clínica criado do modelo; usuário disponível para conversar.

**DoD:**
- [ ] chave testada, validade registrada, áreas alcançadas anotadas;
- [ ] repo confirmado privado (ou risco registrado por escrito);
- [ ] modo e papéis registrados (`ESTADO.md`, `PAPEIS.md`);
- [ ] pedido único enviado e registrado;
- [ ] foto inicial de todas as áreas + resumo;
- [ ] inventário dos documentos recebidos até agora;
- [ ] formulário de lacunas com o que trava a S01;
- [ ] plano da clínica por porte (sprints aplicáveis, `n/a`, datas) no `ESTADO.md`;
- [ ] **para a S01 começar:** CL-1 e CL-3 recebidos (ou dados confirmados na conversa).

## Checklist de itens

| # | item | status | origem | prova | observação |
|---|---|---|---|---|---|
| S00-01 | Modo da sessão definido | pendente | | | |
| S00-02 | Papéis definidos (dono, implantador) | pendente | | | |
| S00-03 | Repo da clínica confirmado privado | pendente | | | |
| S00-04 | Chave testada (GET /empresas 200) | pendente | | provas/S00/teste-chave.md | |
| S00-05 | Validade da chave registrada (X-ApiKey-Expires-At) | pendente | | | |
| S00-06 | Áreas alcançadas pela chave (25) | pendente | | | |
| S00-07 | Pedido único de documentos enviado | pendente | | | |
| S00-08 | Inventário dos documentos recebidos | pendente | | | |
| S00-09 | Formulário de lacunas | pendente | | | |
| S00-10 | Foto inicial de todas as áreas + resumo | pendente | | provas/S00/foto-inicial/ | |
| S00-11 | Porte e plano da clínica (sprints aplicáveis) | pendente | | | |
| S00-12 | Data desejada de go-live | pendente | | | |

## O que registrar

- `ESTADO.md`: modo, sprint atual = S01, porte, versão do kit, próximo passo concreto.
- `decisoes/DECISOES.md`: ambiente (produção/homologação), porte, go-live desejado.
- `pendencias/LACUNAS.md`: documentos que travam as próximas sprints.
- `historico/daily/` — daily nº 1.
