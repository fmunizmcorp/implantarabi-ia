# Ordem de carga pela API externa (passos 0 a 14) × sprints do kit

> **Fonte:** https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#ordem-oficial (passos #passo-0 a #passo-14, #dependencias-corrigidas, #checklist-final) · https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html (#etapa-1 a #etapa-16) · **Conferido em:** 2026-09-25
> **Vale para:** produção (ordem oficial revisada em 24/09/2026) · **Kit:** v0.1.0

## 1. A ordem oficial (vale para tela e API)

```
Empresa → Depósito mínimo → Locais e tipos → Operadoras/Fornecedores/Fabricantes → Taxas
→ Produtos (catálogo) → Equipamentos → Serviços (subserviços ANTES dos pais) [+ tabela interna]
→ Colaboradores (+ login) → Convênios (dados, depois abas) [+ grades] → Conferência pelo Farol
→ Financeiro/Fiscal/Estoque → Pacientes → Parâmetros e Permissões → Testes → Go-live
```

A API recusa com código de erro quando a ordem é violada (a tela só "não mostra a opção").
**90% dos 422 são pré-requisito faltando.**

**As 3 dependências que estavam invertidas no manual antigo** (corrigidas em 24/09/2026):
1. `POST /locais` exige `depositoPadraoSaidaId` de depósito **ativo** (e `POST /produtos`
   exige `depositoId`) → **depósito mínimo por unidade antes dos locais** (senão 422 "O
   depósito padrão de saída selecionado está inativo ou não existe").
2. Serviço de medicamento aponta para o produto (`produtoIds`) → **produtos antes dos
   serviços** (senão a composição não tem para onde apontar e consertar exige PUT completo).
3. Abas Taxas/Serviços do convênio, tabela interna e `taxaServicoId` do serviço exigem as
   taxas → **taxas antes de produtos, serviços e convênios** (senão 207 com ERRO "taxa
   inexistente").

## 2. Passo a passo

| Passo API | Sprint | O que | Rotas (lote) | Precisa de | Entrega para os próximos | Conferir |
|---|---|---|---|---|---|---|
| **0** | **S00** | Preparação: chave, validade, dicionário de ids, ids só da tela, planilha limpa | `GET /auxiliares/*` (14) · `testar_chave.py` | chave com o kit de permissões | ids de tipo de produto/código/serviço/guia/taxa, unidades, UF, conselhos, sexos, tabela ANS 87, tipos de atendimento | teste da chave gravado; `X-ApiKey-Expires-At` anotado |
| **1** | **S01** | Empresa e unidades | `POST /empresas` (sem lote) | UF (id ou sigla) | `empresaId` (depósitos, locais, convênios, colaboradores) | `GET /empresas`; 409 = CNPJ já existe → reutilizar |
| **2** | **S02** | Depósito mínimo **por unidade** | `POST /depositos` · `/depositos/bulk` (50) | `empresaId` | `depositoId` (locais, produtos) | `GET /depositos?ativo=true`; 409 = nome repetido na unidade |
| **3** | **S03** | Locais (e conferência dos tipos) | `POST /locais` (sem lote) | `empresaId`, `depositoPadraoSaidaId` ativo | `localId` (grades, agenda) | `GET /locais`; tipos faltando → tela |
| **4** | **S04** | Operadoras (com planos), fornecedores, fabricantes | `POST /operadoras/bulk` · `/fornecedores/bulk` · `/fabricantes/bulk` (50) | UF **por extenso** | `operadoraId` + ids de planos (`GET /operadoras/{id}`), `fornecedorId`, `fabricanteId` | `GET /operadoras/{id}`; `identificacaoPrestadorXML` definido |
| **5** | **S05** | Taxas | `POST /taxas` · `/taxas/bulk` (50) | `tipoTaxaId` (auxiliar) | `taxaId` (serviço, abas do convênio) | `GET /taxas?ativo=true` (o POST responde 200) |
| **6** | **S06** | Produtos (catálogo) | `POST /produtos` · `/produtos/bulk` (50) | `depositoId`, `tipoProdutoId`, `fabricanteId`, `unidadeDeMedidaId` | `produtoId` (composição, aba Produtos, estoque, tabela interna) | `GET /produtos?ativo=true&nome=…`; 422 = referência inválida |
| **7** | **S07** | Equipamentos | `POST /equipamentos/bulk` (50) | — | `equipamentoId` (composição, grade de equipamento) | `GET /equipamentos`; 409 = nome ativo repetido |
| **8** | **S08** | Serviços: **subserviços primeiro**, depois os pais | `POST /servicos` · `/servicos/bulk` (50) | taxas, produtos, equipamentos, especialidades (id da tela) | `servicoId` (aba Serviços, agenda, orçamento) | `GET /servicos/{id}` mostra a composição (leitura `somarItens`, escrita `somarItems`) |
| **9b** | **S08** | Tabela de preço interna (= preço de **produto**) | `POST /tabelas-preco` · `POST /tabelas-preco/produtos/bulk` (200, upsert) | produtos | id da tabela (política de preço do convênio) | `GET /tabelas-preco/produtos?id=…` (o POST simples responde antes de gravar) |
| **9** | **S09** | Colaboradores e **login** | `POST /colaboradores/bulk` (50) · `POST /colaboradores/{id}/usuario` | UF por extenso, `conselhoProfissionalId`, especialidades | `colaboradorId` (aba Colaboradores, grades, `responsavelId`) | `GET /colaboradores/{id}`; login: 201, `409` = já tem |
| **10** | **S10** | Convênios — **fase 1: dados** | `POST /convenios` · `/convenios/bulk` (50; `cnpj` obrigatório no lote) | `empresaId` (texto), `unidadesIds`, `operadoraId` (texto) | `convenioId` | `GET /convenios/{id}`; 409 = CNPJ; 422 = empresa/operadora/kit |
| **10** | **S10** | Convênios — **fase 2: abas**, uma por vez por convênio: Planos → Especialidades → Taxas → Produtos → Serviços → Colaboradores | `PUT /convenios/{id}/planos` · `/especialidades` · `/taxas` · `/produtos` · `/servicos` (200) · `/colaboradores` (100) — upsert | tudo acima | a configuração de preço | `GET` de cada aba; 207 → reenviar só ERRO |
| **10b** | **S10** | Grades de horário | `POST /grades-colaborador` (lista em `colaboradorGrade`) · `POST /grades-equipamento` (lista direta) | colaboradores, equipamentos, locais, convênios | agenda pronta | `GET /grades-colaborador?colaboradorId=…&localId=…&vigenteEm=…` (grade de equipamento grava e devolve 500 — reler) |
| **11** | **S11** | Conferência pelo **Farol** (todo convênio) | `GET /convenios/{id}/farol/itens?apenasAtivosNoConvenio=true&servicoAtivo=true` · `/farol/servicos` · `/farol/produtos` | abas gravadas | relatório: vermelhos e roxos explicados | mínimo 3 serviços por convênio (simples, com medicamento, com pacote) |
| **12** | **S12** | Financeiro, fiscal e estoque (entradas com `valorCompra` → custo do Farol) | `POST /estoque/entrada` · `POST /financeiro/movimentacoes(/bulk)` — **só com ordem escrita** | depósitos, produtos, `responsavelId`, `motivoId`, contas/categorias (ids da tela) | saldo e custo; roxos do Farol somem | `GET /estoque/saldo-produtos`; reler o Farol |
| **13** | **S13** | Pacientes (e, se houver, histórico) | `POST /pacientes/bulk` (50, um lote por vez) · `/pacientes/{id}/convenios` · `/anexos` · `POST /atendimentos` + `PUT /atendimentos/{id}` · `POST /atendimentos/prontuario` | convênios e planos; colaboradores | base de pacientes | amostra por GET (sem PII na prova); `GET /atendimentos/historico?pacienteId=…` |
| **14** | **S14** | Parâmetros e permissões | `/parametros/*` (GET antes de PUT, objeto completo) · perfis de permissão **pela tela** | tudo | regras de negócio | GET depois de cada PUT |
| — | **S15** | Testes de validação (10 cenários do guia) | leitura + agendamento/orçamento **só em homologação ou com ordem** | S01–S14 | aprovação dos cenários | manual #etapa-15 |
| — | **S16** | Go-live | revogar a chave de implantação ou reduzir permissões; registrar validade da chave contínua | S15 | clínica operando | manual #checklist-final |
| — | **S17** | Estabilização e dossiê | leituras, Farol, `testar_chave.py` | — | dossiê final | — |

> Nota de numeração: o passo "9b" (tabela interna) vem **antes** do 9 na execução (depois
> de taxas e produtos, antes dos convênios) — por isso fica na S08 do kit. O guia oficial
> põe a tabela interna junto de Serviços.

## 3. Checklist de fechamento (do manual)

- [ ] Toda unidade tem depósito ativo e todo local aponta para um depósito ativo.
- [ ] Nenhum `0.01` gravado como "sem valor".
- [ ] Todo serviço composto criado depois dos seus subserviços e produtos.
- [ ] Cada convênio com as 6 abas conferidas por GET e o Farol lido — vermelhos e roxos explicados.
- [ ] Colaboradores que usam o sistema têm login.
- [ ] Nenhuma correção por PUT parcial (fora das abas do convênio, PUT com objeto completo, conferido por GET).
- [ ] Valores de faturamento lidos conforme a descrição da rota (reais × centavos/texto).
- [ ] Data de `X-ApiKey-Expires-At` registrada, com alerta de renovação.
- [ ] Chave de implantação revogada (ou reduzida às permissões da integração contínua).

## 4. Regras que valem em todos os passos

- Ritual de 5 passos em toda gravação (foto antes → prévia → aprovação → grava → foto
  depois + diff) — `ferramentas/rabi_api/foto.py`.
- Antes de criar, **procure** (o cliente pode já ter cadastrado): 409 = reutilize o id.
- Mapa "id de origem → id Rabi" no repo da clínica, atualizado a cada `CRIADO`.
- Ensaiar em homologação o roteiro com uma amostra; produção só com autorização.
- Regras de preço (vazio ≠ zero, Utiliza, Pacote/Zerar, valor combinado ≠ pacote): ver
  `conhecimento/precos-e-conversao/` e https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#convenio-fase-2.
