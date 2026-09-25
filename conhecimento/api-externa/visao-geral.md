# Visão geral da API externa do Rabi

> **Fonte:** https://www.rabisistemas.com.br/manual/api-externa/index.html#o-que-e · Swagger https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção desde 23–24/09/2026; correções do QA externo 100% em produção desde 25/09/2026 · **Kit:** v0.1.0

## 1. O que é

A **API externa** do Sistema Rabi é uma API REST (padrão OpenAPI 3.0, versão 1.0.0).
Ela deixa um sistema de fora — ou uma IA, como você — **cadastrar e consultar a
clínica inteira usando uma chave** (`rbk_...`), sem abrir a tela e sem login de pessoa.

- Passa pelas **mesmas validações da tela**: o que a tela recusa, a API também recusa,
  com um código de erro que diz o motivo.
- A chave já carrega **a clínica** (não se informa "tenant" nas chamadas), **as
  permissões** e **a validade**.
- No Swagger de 25/09/2026: **191 caminhos**, **268 operações** (método + caminho),
  **25 grupos**, **88 permissões**, 155 schemas.

## 2. Endereços

| O quê | Endereço | Quando usar |
|---|---|---|
| Produção | `https://api.rabisistemas.com.br/api/v1/integrations` | implantação real da clínica (padrão do `cliente.py`) |
| Homologação (o Swagger chama de "Desenvolvimento") | `https://api.hmg.rabisistemas.dev/api/v1/integrations` | ensaiar antes de tocar na produção. IDs de homologação **não valem** em produção |
| Swagger (documentação interativa oficial) | https://api.rabisistemas.com.br/external-docs/ | fonte primária; o spec fica em `swagger-ui-init.js` (objeto `swaggerDoc`) |
| Manual comentado | https://www.rabisistemas.com.br/manual/api-externa/ | visão geral, roteiro de implantação, referência, erros |

Exemplo: a rota `/empresas` em produção é
`https://api.rabisistemas.com.br/api/v1/integrations/empresas`.
Para trocar de ambiente no kit, defina a variável `RABI_API_BASE`.

## 3. Os 25 grupos

Ordem do roteiro de implantação do manual (grupos 1 a 20) e depois os de operação
(21 a 25). O detalhe de cada rota está em [rotas/00-INDICE.md](rotas/00-INDICE.md).

| # | Grupo | O que cobre | Operações | Sprint do kit |
|---|---|---|---|---|
| 1 | Empresas | empresa e unidades | 5 | S01 |
| 2 | Depósitos | depósitos de estoque | 6 | S02 (mínimo) · S12 |
| 3 | Locais | salas/consultórios de cada unidade | 5 | S03 |
| 4 | Auxiliares | tabelas de domínio (tipos, UF, conselhos…) — **só leitura** | 14 | S00 |
| 5 | Operadoras | operadoras de convênio, com planos | 6 | S04 |
| 6 | Fornecedores | fornecedores | 5 | S04 |
| 7 | Fabricantes | fabricantes de produtos | 6 | S04 |
| 8 | Taxas | taxas cobradas pela clínica | 6 | S05 |
| 9 | Produtos | medicamentos, materiais, insumos (catálogo) | 6 | S06 |
| 10 | Equipamentos | aparelhos | 6 | S07 |
| 11 | Serviços | serviços e procedimentos, com composição | 6 | S08 |
| 12 | Colaboradores | profissionais e equipe, **inclusive login** | 7 | S09 |
| 13 | Tabelas de Preço | tabela interna = preço de **produto** | 8 | S08 |
| 14 | Convênios | dados + 6 abas em lote + **Farol** | 21 | S10 · S11 |
| 15 | Grade de Colaborador | horários de agenda do profissional | 7 | S10 (depois dos convênios) |
| 16 | Grade de Equipamento | horários do equipamento | 5 | S10 |
| 17 | Financeiro | movimentações financeiras | 5 | S12 |
| 18 | Estoque | entrada, saída, transferência, saldo | 12 | S12 |
| 19 | Pacientes | cadastro, convênios do paciente, anexos | 11 | S13 |
| 20 | Parâmetros | regras de negócio, avisos, agendamento online, dashboards | 45 | S14 |
| 21 | Agendamentos | buscar horário, agendar, cancelar, listar | 8 | S15 (testes) |
| 22 | Orçamentos | orçamento antes do atendimento | 10 | S15 |
| 23 | Atendimentos | atendimento e prontuário — **para migrar histórico** | 6 | S13 |
| 24 | Faturamento | pré-faturamento, divergência, recebimento, glosa | 24 | S15 · S17 |
| 25 | NFS-e | nota fiscal de serviço e tomadores | 28 | S12 (conferência) |
| | **Total** | | **268** | |

Conferência feita por script em 25/09/2026: soma = 268 operações, 191 caminhos
(`python3 -m ferramentas.rabi_api.gerar_rotas`).

## 4. API externa × API interna × tela — quando usar cada uma

| Caminho | O que é | Use quando | Não use quando |
|---|---|---|---|
| **API externa** (esta) | chave `rbk_` da clínica, rotas documentadas no Swagger | **sempre que a rota existir** — é o caminho principal do kit | a rota não existe ou tem defeito conhecido ([defeitos-conhecidos.md](defeitos-conhecidos.md)) |
| **Tela** do sistema (`https://app.rabisistemas.com.br/portal/...`) | uma pessoa (ou você guiando a pessoa) clica | o que a API não cobre: tipos auxiliares, especialidades, perfis de permissão, documentos e impressão, contas/caixas, categorias, centros de custo… | quando a API cobre (a tela é lenta e sem prova automática) |
| **API interna** (a que a tela usa) | token de login de pessoa, curto | **só como último recurso**, com aprovação escrita, para o que nem a API externa nem uma pessoa na tela resolvem | como caminho normal — não é contrato público, muda sem aviso |

Detalhes em [nao-coberto-e-api-interna.md](nao-coberto-e-api-interna.md).

## 5. Como a IA usa a API neste kit

1. **Chave**: segredo de ambiente `RABI_API_KEY` (ou registro no repo privado) — ver
   [chave-e-token.md](chave-e-token.md).
2. **Teste**: `python3 -m ferramentas.rabi_api.testar_chave --saida provas/S00/teste-chave.md`.
3. **Leitura**: sempre pelo cliente (`ler_tudo`), que pagina, normaliza e confere o total.
4. **Gravação**: sempre no ritual de 5 passos (foto antes → prévia → aprovação → grava →
   foto depois + diff), com `ferramentas/rabi_api/foto.py`.
5. **Regras**: [convencoes.md](convencoes.md) (paginação, envelope, PUT, lotes, erros) e
   [proibidas-sem-ordem-escrita.md](proibidas-sem-ordem-escrita.md).
6. **Ordem**: [ordem-de-carga-via-api.md](ordem-de-carga-via-api.md).

Ferramentas: [../../ferramentas/rabi_api/README.md](../../ferramentas/rabi_api/README.md).

## 6. O que mudou recentemente (para não usar conhecimento velho)

| Data | Mudança | Efeito prático |
|---|---|---|
| 24/09/2026 (tarde) | API passa de 29 operações em 3 áreas para 268 em 25 | a implantação quase inteira passa a ser pela API externa |
| 24/09/2026 | autenticação é `Authorization: Bearer rbk_...` | o cabeçalho antigo `X-API-Key` responde 401 |
| 24/09/2026 (noite) | nova rota `POST /colaboradores/{id}/usuario` | o login do colaborador é criado pela API externa |
| 24/09/2026 | `equipamento:read` passou a existir na chave | grupo Equipamentos legível |
| 25/09/2026 | envelope único nas listagens; `GET /agendamentos` exige `data`; grades paginadas | ver [convencoes.md](convencoes.md) |
| 25/09/2026 | cabeçalho `X-ApiKey-Expires-At` em toda resposta de sucesso | monitorar a validade — ver [chave-e-token.md](chave-e-token.md) |
| 25/09/2026 | documentação: chave rejeitada responde **401**; 503 fica para falha de rede | **medido em 25/09/2026 03:07: chave inexistente ainda responde 503.** Trate 401 e 503 como problema de chave, sem repetir em loop |

Roadmap (não prometer): geração de chave self-service dentro do sistema (issue #624,
sem data).
