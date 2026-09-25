# O que a API externa não cobre — e como fazer (tela ou, em último caso, API interna)

> **Fonte:** Swagger, seção "O que esta API NÃO cobre" (snapshot `spec/openapi-2026-09-25.json`) · https://www.rabisistemas.com.br/manual/api-externa/index.html#nao-cobre · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-0 · experiência de implantação real (22–24/09/2026) · **Conferido em:** 2026-09-25
> **Vale para:** produção (25/09/2026) · **Kit:** v0.1.0

## 1. O que a API externa não cobre (Swagger + manual)

| O que | Como fazer | Sprint |
|---|---|---|
| **Criar tipos auxiliares** (tipo de produto, de código, de serviço, de guia, de taxa, unidade de medida, princípio ativo, conselho…) | a API só **lê** (`GET /auxiliares/*`). Faltou um? a pessoa cria **pela tela**, e a IA relê o id | S00 · S03 |
| **Perfis e permissões de usuário** (grupos de perfil, permissões por tela, papel do colaborador) | **pela tela** (Configurações › permissões). A API só expõe permissão/atribuição de **dashboard** (grupo Parâmetros) | S14 |
| Documentos, modelos e **tipos de impressão**, tipos de documento, de identificação, **kits de documento**, tipos de anexo | pela tela | S14 |
| **Lote e XML de faturamento** (fechar lote, gerar XML) | pela tela | S15 · S17 |
| Exclusão de fornecedor | pela tela (a exclusão interna é física — por isso não foi exposta) | — |
| **Preço de venda calculado do produto** | a API expõe o `valorUnitario` bruto; o preço que a engine calcula, não. Para conferir preço efetivo num convênio, use o Farol (`GET /convenios/{id}/farol/produtos`) | S11 |
| Certificado digital, numeração e sincronização do NFS-e com a prefeitura | configuração de infraestrutura — pela tela, com o dono/contador | S12 |
| Bloqueio de agenda, fila de espera, confirmação por SMS | pela tela | — |
| Finalização de atendimento (a que **baixa estoque**) e recursos usados no atendimento | a API de atendimentos é para **migrar histórico**, não para operar a clínica ao vivo | — |
| Exclusão de prontuário, de movimentação financeira, de anexo de paciente | não existe | — |
| Importar/exportar Excel | não existe em nenhum módulo | — |
| O total Σ do serviço no convênio (`efetivo.totalConvenio`, a 4ª linha da coluna Valor na tela) | não aparece na API externa. Use `receita_total` de `GET /convenios/{id}/farol/servicos` | S11 |
| Auditoria (quem mudou o quê) | pela tela (Relatórios › Logs de auditoria) | S17 |
| O orçamento **como o paciente vê e paga** | tela do orçamento (e `GET /orcamentos/{id}/{isAgendamento}` para leitura) | S15 |

## 2. IDs que só existem na tela

O Swagger **não tem listagem** destes cadastros, mas outras rotas pedem o id deles. A IA
**pede ao implantador** (uma pergunta por vez) para abrir a tela e informar o id — ou
lê o id em algum registro que já o usa (ex.: um convênio já cadastrado traz o id do kit
de documentos).

| Cadastro | Onde é pedido o id | Tela (manual) |
|---|---|---|
| **Especialidades** (catálogo) | serviços (`especialidadesId`), colaboradores (`especialidades[].especialidadeId`), aba Especialidades do convênio | Configurações › Especialidades |
| **Categorias de pagamento** | `POST /financeiro/movimentacoes` (`categoriaDePagamentoId`), `/parametros/financeiro` | Financeiro › Categorias de pagamento |
| **Contas / caixas** | movimentações (`contasCaixaId`) | Financeiro › Contas e caixas |
| **Centros de custo** | `/parametros/financeiro` (`centroDeCustoId`) | Financeiro › Centro de custo |
| Motivos de movimentação de estoque | `POST /estoque/entrada|saida|transferencia` (`motivoId`) | Estoque |
| Kits de documentos | convênio, aba Serviços (`kitDocumentoId`) | Configurações |
| Modelos de XML do convênio (`xmlConsultaId`, `xmlSpSadtId`) | convênio | Configurações › Convênios |
| Tipos de contrato, tipos de anexo | colaborador, anexo de paciente | Configurações |
| **Perfis de permissão** (`perfilPermissaoId`) | `GET/PUT /parametros/dashboard-*` | Configurações › permissões |
| Fontes de preço de compra (`fontePrecoCompraOptionsId`) | aba Produtos do convênio | Configurações › Convênios |

Exceção útil: o **motivo de cancelamento** tem leitura em
`GET /agendamentos/motivo-cancelamento`.

Registre cada id obtido assim em `dados/ids-da-tela.md` do repo da clínica (nome → id →
quem informou → data), para não perguntar duas vezes.

## 3. Rotas que existem mas **não funcionam com chave** (use a tela)

Declarado no próprio Swagger de 25/09/2026 — toda chamada por chave recebe **401**, mesmo
com a permissão certa (não é problema da chave):

| Rota | O que faria | Como fazer hoje |
|---|---|---|
| `POST /parametros/desconto/colaborador/{id}` | conceder nível de desconto (alçada) ao colaborador | pela tela |
| `POST /parametros/alcada-compra/colaborador/{id}` | conceder alçada de compra ao colaborador | pela tela |
| `POST /parametros/acolhimento/atualizar-validacoes/{pacienteId}` | marcar validações do acolhimento do paciente | pela tela |

Mais defeitos em [defeitos-conhecidos.md](defeitos-conhecidos.md).

## 4. A API interna — só como último recurso

A **API interna** é a que a própria tela usa. Ela não é contrato público: muda sem aviso,
o Swagger interno é **parcial e às vezes desatualizado**, e o login é de **pessoa**. Por
isso o kit só a admite quando: (1) a API externa não cobre, (2) fazer pela tela com a
pessoa não é viável, e (3) há **ordem escrita** do dono
([proibidas-sem-ordem-escrita.md](proibidas-sem-ordem-escrita.md)).

O que se aprendeu numa implantação real (use com cautela):

| Ponto | Detalhe |
|---|---|
| Base | `https://api.rabisistemas.com.br` (sem `/api/v1/integrations`); rotas começam em `/api/...` |
| Autenticação | `Authorization: Bearer <token>` do **login de uma pessoa** — o token que o navegador logado guarda. **Expira em ~5 minutos**: releia antes de cada bloco |
| Paginação | começa em **`page=0`** — o contrário da externa. `page=1` é a **segunda** página |
| Corpo das gravações | o Swagger interno não bate com a tela (ex.: o corpo real de serviço tem campos que o Swagger não mostra; `especialidadesId` × `ServicoEspecialidade`; `somarItems` × `somarItens`). **Nome errado apaga o campo.** Antes da primeira gravação de cada tipo, **capture o corpo real** que a tela envia (a pessoa salva uma vez pela tela; a IA copia o corpo) e grave com ele |
| Formulário da tela | com a janela do navegador em segundo plano, o formulário pode **descartar alterações** sem avisar — a janela fica em primeiro plano |
| Endereço das telas | `https://app.rabisistemas.com.br/portal/...` (sem `/portal` dá 404) |
| Leitura | sempre conferir **status e tamanho** da resposta; corpo vazio com 200 já gerou conclusões erradas |

Nunca: pedir a senha de uma pessoa na conversa; guardar token de pessoa no repo; usar a
API interna para algo que a externa faz.

## 5. Ordem de preferência (resumo)

1. **API externa** com a chave da clínica (sempre que a rota existir e funcionar).
2. **Tela**, com a pessoa, guiada pela IA passo a passo — e a IA **relê pela API externa**
   para provar (foto depois).
3. **API interna**, só com ordem escrita, corpo capturado da tela, e prova pela API externa.
