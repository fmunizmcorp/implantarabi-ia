# S13 — Pacientes e migração

> **Fonte:** https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-13 · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-13 · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#migracao-historico · https://www.rabisistemas.com.br/manual/modulos/pacientes.html#lgpd-set-2026 · spec `openapi-2026-09-25.json` (`POST /pacientes`, `/pacientes/bulk`, `/pacientes/{id}/convenios`, `/pacientes/{id}/anexos`, `/atendimentos*`) · **Conferido em:** 2026-09-25
> **Vale para:** produção · **Kit:** v0.1.0

## Objetivo

A base de pacientes da clínica (se houver) está no Rabi, com convênio, plano e
carteirinha, **sem duplicatas** e **sem nenhum dado pessoal fora do Rabi** —
nem em prova, nem em relatório, nem no repo. Clínica nova sem base: só o
paciente de teste da S15. Histórico de atendimentos só se o dono decidir, por
escrito.

**É a etapa mais arriscada da implantação:** é a única que move dado pessoal e
de saúde em volume.

## Link do manual

- Etapa 13: https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-13
- Pela API: https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-13
- Migração de histórico: https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#migracao-historico
- LGPD no cadastro: https://www.rabisistemas.com.br/manual/modulos/pacientes.html#lgpd-set-2026
- Kit: [../conhecimento/negocio-clinica/lgpd-na-implantacao.md](../conhecimento/negocio-clinica/lgpd-na-implantacao.md) · [politicas.md §5](../metodologia/politicas.md)

## Depende de

S10 (convênios e planos existem — a carteirinha aponta para eles); S03 (tipos de
anexo, se for anexar); S09 (colaboradores, se migrar atendimentos).

## Documentos a pedir

SA-1 (exportação de pacientes), SA-2 (histórico — só se for migrar), SA-4 (qual
sistema). Ver [lista única](../metodologia/lista-unica-de-documentos.md).

## Regras de LGPD desta sprint (valem acima de tudo)

1. O arquivo exportado **não entra no repo**. Fica fora do Git (o `.gitignore` da
   clínica bloqueia `dados/pacientes/`), é processado e **apagado do container**
   ao fim, com registro de que foi apagado.
2. Prova, relatório, daily, issue, log: **só contagens e IDs internos do Rabi**.
   Nenhum nome, CPF, data de nascimento, telefone, e-mail ou texto clínico.
3. A conversa com o usuário também evita dado pessoal: "a linha 214 do arquivo
   tem CPF inválido" — não o CPF.
4. Base legal e ciência: o dono da clínica confirma por escrito que a migração
   é da própria clínica (controladora dos dados) e autoriza o envio.
5. Lotes pequenos, conferência por amostra, e nada de "tudo de uma vez".

## Índice de dados a coletar

| dado | campo API | obrigatório? | onde costuma estar no material do cliente | padrão sugerível | pergunta ao usuário se faltar |
|---|---|---|---|---|---|
| Nome | `nome` | sim | exportação | — | — |
| CPF | `cpf` | sim pelo manual (salvo recém-nascido) | exportação | — | — |
| Recém-nascido sem CPF | `atendimentoRn` + `cpfMae` | se for o caso | exportação | — | — |
| Sexo | `sexoId` | sim | exportação | — (mapear o código do outro sistema para `GET /auxiliares/sexos`) | "No sistema antigo, o que significa o código 'I' em sexo?" |
| Contato | `contato[]` com `email` **e** `celular` (e `telefone`, `pessoaDeContato`) | sim (e-mail e celular no item de contato) | exportação | — | ver armadilhas |
| Endereço | `endereco` (`cep`, `endereco`, `numero`, `complemento`, `bairro`, `cidade`, `unidadeFederativaId`) | objeto obrigatório | exportação | pelo CEP | — |
| Data de nascimento | `dataDeNascimento` | não na API (recomendado) | exportação | — | — |
| RG, órgão, UF do RG | `rg`, `orgaoEmissor`, `ufRg` | não | exportação | — | — |
| Estrangeiro, estado civil, profissão | `estrangeiro`, `estadoCivil`, `profissao` | não | exportação | — | — |
| Convênio / plano / carteirinha / validade | `convenioPlano[]`: `convenioId`, `planoId`, `numeroDaCarterinha`, `validade`, `ativo` | `convenioId` se enviar | exportação | — | mapear o nome do convênio do sistema antigo para o `convenioId` |
| Anexos | `POST /pacientes/{id}/anexos` (multipart `file`, até 10 arquivos JPG/PNG/PDF de até 10 MB; `tipoAnexoId` opcional) | não | — | — | só se o dono pedir |

## Fila de perguntas

1. "A clínica tem base de pacientes em outro sistema? Consegue exportar em
   planilha?" (se não: sprint vira só o paciente de teste da S15).
2. Autorização escrita de migração (LGPD).
3. Mapa de colunas: confirmar as colunas que a IA não conseguiu mapear sozinha
   (uma pergunta por coluna ambígua).
4. Mapa de convênios: nome no sistema antigo → convênio do Rabi (confirmar os
   que não casaram).
5. Regras de corte: pacientes inativos há anos entram? Sem CPF entram?
6. Histórico de atendimentos: migrar ou não? (decisão escrita).

## Enriquecimento possível

- **CEP → endereço** (em lote, sem gravar o resultado no repo).
- Validação de CPF (dígito verificador) e normalização de telefone e datas.
- Mapeamento automático de colunas por nome e amostra — ver
  [ingestão de documentos](../metodologia/ingestao-de-documentos.md) (seção "Importação de sistemas anteriores").

## Leitura do que já existe no Rabi e regra de não perder nada

- `GET /pacientes` (paginado) para saber **quantos** existem e, na memória do
  script, casar por CPF antes de enviar — **sem gravar** a leitura em arquivo.
- Paciente que já existe (mesmo CPF) **não** se cria de novo: no envio simples, o
  sistema responde 409; no lote, vem como erro no 207. Esses casos viram a
  contagem "já existiam".
- Vínculo de convênio: `GET /pacientes/{id}/convenios` antes de criar outro;
  `POST /pacientes/{id}/convenios` **sempre cria** um novo; corrigir é
  `PUT /pacientes/{id}/convenios/{vinculoId}` com o vínculo completo.

## Gravação

| Ordem | O que | Rota | Permissão | Lote |
|---|---|---|---|---|
| 1 | Normalizar, deduplicar, mapear (fora do repo) | script | — | — |
| 2 | **1 paciente** (amostra), provado | `POST /pacientes` | `paciente:create` | — |
| 3 | Lote de 10, conferido por amostra | `POST /pacientes/bulk` (chave `pacientes`) | `paciente:create` | 10 |
| 4 | Lotes de 50, **um de cada vez** | idem | idem | até 50 |
| 5 | Vínculos extras de convênio | `POST /pacientes/{id}/convenios` | `paciente:update` | — |
| 6 | Anexos (se decidido) | `POST /pacientes/{id}/anexos` | `paciente:update` | até 10 arquivos por chamada |
| 7 | Histórico (só com ordem escrita) | `POST /atendimentos` → `PUT /atendimentos/{id}` com `responsavelId` e `horarioInicio` real (repetindo `pacienteId` e `empresaId`) → `POST /atendimentos/prontuario` | `atendimento:create/update` | um por vez no começo |

- **207:** reenviar só os itens com `ERRO`/`NAO_PROCESSADO`, depois de corrigir a
  causa; 429 = outro lote em andamento (esperar).
- 400 = CPF inválido ou contato obrigatório ausente.
- `PUT /pacientes/{id}` **sobrescreve**: campo omitido é apagado. GET antes.
- Histórico: o atendimento é gravado com a hora "agora" — o PUT com a data real é
  obrigatório; cria um agendamento sintético e um prontuário vazio; o texto do
  prontuário **sobrescreve** sem versão anterior; não há exclusão. Conferência:
  `GET /atendimentos/historico?pacienteId=…` (pacienteId é obrigatório).

## Prova

Só números e IDs internos, em `provas/S13/`:

```
lote-003: enviados 50 · criados 47 · já existiam (CPF) 2 · erro 1 (linha 153: CPF inválido)
amostra conferida: 5 IDs do Rabi relidos, convênio e plano corretos (sim/sim)
```

- Conferência por amostra: a cada lote, reler 3–5 pacientes por ID e comparar
  **na memória** com a origem (nome, convênio, plano, carteirinha); registrar
  apenas "confere/não confere".
- Contagem final: linhas do arquivo × criados × já existiam × descartados (com o
  motivo agregado).

## Armadilhas desta sprint

- **Contato exige e-mail e celular** no schema da API. Paciente sem e-mail: **não
  invente e-mail**. Não tenho certeza de como o Rabi quer esse caso pela API —
  registre como pendência para o time Rabi; alternativas: cadastrar esses pela
  tela ou deixá-los para o primeiro atendimento.
- CPF duplicado na própria exportação (mesma pessoa duas vezes): deduplicar
  antes, com a regra aprovada (qual registro fica).
- Carteirinha já usada por outro paciente → 400.
- Nome de convênio do sistema antigo que não existe no Rabi: pare e pergunte —
  nunca crie convênio nesta sprint.
- Guardar o CSV exportado no repo (proibido) ou colar linhas dele na conversa.
- Migrar prontuário sem decisão escrita: é dado de saúde e não se desfaz.

## Definition of Ready / Definition of Done

**DoR:** convênios e planos existem (S10); autorização escrita de migração; mapa
de colunas e de convênios aprovado.

**DoD:**
- [ ] base migrada (ou `n/a` sem base), contagens fechando;
- [ ] amostra conferida em cada lote;
- [ ] nenhum dado pessoal no repo, na conversa registrada ou nas provas;
- [ ] arquivo exportado apagado do container, com registro;
- [ ] histórico migrado **ou** decisão de não migrar registrada.

## Checklist de itens

| # | item | status | origem | prova | observação |
|---|---|---|---|---|---|
| S13-01 | Existe base a migrar? | pendente | | | se não, itens 02–10 `n/a` |
| S13-02 | Autorização escrita de migração (LGPD) | pendente | | | |
| S13-03 | Mapa de colunas aprovado | pendente | | | |
| S13-04 | Mapa de convênios aprovado | pendente | | | |
| S13-05 | Normalização e deduplicação feitas | pendente | | | |
| S13-06 | 1º paciente gravado e provado | pendente | | provas/S13/ | |
| S13-07 | Lote de 10 conferido | pendente | | | |
| S13-08 | Lotes de 50 (uma linha por lote) | pendente | | | |
| S13-09 | Contagem final fechada | pendente | | | |
| S13-10 | Arquivo exportado apagado do container | pendente | | | |
| S13-11 | Decisão sobre histórico de atendimentos | pendente | | | |

## O que registrar

- `dados/migracao/mapa-colunas-<sistema>.md` e mapa de convênios (sem dados pessoais).
- `decisoes/DECISOES.md`: autorização, regras de corte, histórico sim/não.
- `ESTADO.md`: próximo passo = S14.
