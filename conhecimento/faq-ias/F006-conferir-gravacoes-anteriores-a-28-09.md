# F006 — Gravações feitas pela API antes de 28/09/2026 17:43 que podem ter saído erradas sem aviso

- **Rotas:** POST /pacientes/bulk · POST /colaboradores/bulk · POST /tabelas-preco/produtos/bulk · PUT /financeiro/movimentacoes/{id} · PUT /fornecedores/{id} · POST /estoque/saida · POST /estoque/transferencia · POST /grades-equipamento · PUT /faturamento/glosas/produto
- **Status HTTP:** 200 | 201 | 207
- **Mensagem contém:** CRIADO
- **Causa:** confirmada no código do Rabi — commit `c73e84de` ("campos opcionais omitidos pela API externa quebravam ou gravavam dados errados"), em produção em 28/09/2026 às 17:43 (Brasília)
- **Status:** corrigido no Rabi; o que foi gravado **antes** precisa ser conferido uma vez
- **Origem:** leitura do código do rabi-api (`deploy_prd`) pelo mantenedor, 28/09/2026

## O que o Rabi corrigiu (e o que conferir no que já foi gravado)
| Rota | Defeito antes da correção | O que conferir (só leitura, uma vez) |
|---|---|---|
| `POST /pacientes/bulk` | respondia **CRIADO sem gravar** | contar pacientes lidos × enviados; reenviar só os que faltam |
| `POST /colaboradores/bulk` | transação aninhada (podia falhar ou não gravar) | reler os colaboradores enviados |
| `POST /tabelas-preco/produtos/bulk` | preços **sem conversão para centavos** (valor gravado ~100× menor) | reler `GET /tabelas-preco/produtos?id=<tabela>` e comparar com a origem |
| `PUT /financeiro/movimentacoes/{id}` | PUT sem `duplicatas` **apagava todas as parcelas** | reler as movimentações alteradas pela API |
| `PUT /fornecedores/{id}` | PUT sem `ativo` **reativava** o fornecedor | conferir fornecedores inativos |
| operadora, empresa, colaborador | **UF ausente gravava a primeira UF** da lista | conferir a UF |
| `POST /estoque/saida` · `/transferencia` | sem `lote`, usava **um lote qualquer** (agora `lote` é obrigatório; `null` para produto sem lote) | conferir saldos por lote |
| `POST /agendamentos` | sem contatos, desativava/quebrava os contatos do paciente | conferir contatos dos pacientes agendados pela API |
| `PUT /faturamento/glosas/*` | sem `motivoGlosado`, conectava um motivo qualquer | conferir o motivo das glosas lançadas pela API |
| `POST/PUT/DELETE /grades-equipamento` | 500 **depois** de gravar | reler as grades (a gravação costumava estar lá) |
| grade de colaborador | ficava órfã quando a associação falhava | reler as grades de colaborador |

## O que fazer
1. Veja no histórico/provas da clínica se alguma dessas rotas foi usada **antes de 28/09/2026 17:43**.
2. Se foi: faça a conferência da tabela (só leitura), registre o resultado em `pendencias/` e
   mostre ao usuário. Correção de dado = ritual de 5 passos, com aprovação.
3. Se nenhuma foi usada: registre "F006 — nada a conferir" e siga.

## O que NÃO fazer
- Não reenviar lotes inteiros "por garantia" (duplicaria). Leia antes, reenvie só o que falta.
