# Chave (`rbk_`), permissões, validade e configuração na clínica

> **Fonte:** https://www.rabisistemas.com.br/manual/api-externa/index.html#autenticacao · #permissoes · Swagger https://api.rabisistemas.com.br/external-docs/ (seção "Autenticação" e "Permissões", snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger de 25/09/2026) · **Kit:** v0.1.0

## 1. De onde vem a chave

- A chave é gerada **no portal comercial da Rabi**, **por clínica**. Na geração são
  definidos: a **clínica** (a chave só enxerga os dados dela), as **permissões** e a
  **validade**.
- O token completo (`rbk_...`) aparece **uma única vez**, na criação. Perdeu? Não há como
  recuperar: peça outra chave.
- **Não existe renovação automática nem autoatendimento.** Chave nova é emitida pelo **time
  Rabi**, pelo mesmo canal usado para gerar a atual. (Geração self-service dentro do
  sistema é **roadmap** — issue #624, sem data.)
- Toda chamada leva o cabeçalho `Authorization: Bearer rbk_...`. O cabeçalho antigo
  `X-API-Key` **não funciona mais** (401).

Quem pede a chave é o **dono da clínica** (ver `metodologia/politicas.md`, papéis). A IA
nunca pede para o usuário colar a chave na conversa.

## 2. Configurar a chave na clínica (faça as duas coisas)

A ordem de busca do `cliente.py` é: **variável de ambiente `RABI_API_KEY` → arquivo
`credenciais/rabi-api-externa.md` (linha `api_key:`) → erro claro**. A base vem de
`RABI_API_BASE` (sem ela, produção).

### 2.1 Segredo de ambiente `RABI_API_KEY` no Claude Code na web (preferido)

Passos simples para o dono da clínica (ou implantador):

1. Abra a sessão da clínica no Claude Code na web (claude.ai/code).
2. No **título da sessão**, abra o menu do **ambiente de nuvem** e escolha **Editar**
   (Edit).
3. Onde houver a seção de **credenciais de API**, cadastre ali; se não houver, adicione
   uma **variável de ambiente**:
   - nome: `RABI_API_KEY`
   - valor: a chave `rbk_...` recebida do time Rabi
4. (Opcional) para ensaiar em homologação, outra variável:
   `RABI_API_BASE=https://api.hmg.rabisistemas.dev/api/v1/integrations`.
5. Salve e **abra uma sessão nova** — a variável só aparece nas sessões iniciadas depois.

> **Não tenho certeza** de que os nomes dos botões serão exatamente estes: a tela do
> produto muda com frequência. Se não achar, siga a documentação oficial:
> https://code.claude.com/docs/en/claude-code-on-the-web (parte de ambientes / variáveis de
> ambiente).

Na abertura da sessão, a IA confere **sem mostrar a chave**:
`python3 -c "import os;print('RABI_API_KEY', 'presente' if os.environ.get('RABI_API_KEY') else 'AUSENTE')"`.

### 2.2 Registro em texto claro no repo PRIVADO da clínica

Política do proprietário (`metodologia/politicas.md` §4): credenciais ficam em **texto
claro**, no repo **privado** da clínica, para consulta humana e como segunda fonte do
cliente. **Nunca** no kit, em issue, prova, relatório ou mensagem.

Arquivo `credenciais/rabi-api-externa.md` (modelo — valores fictícios):

```markdown
# Chave da API externa do Rabi — Clínica Exemplo

api_key: rbk_COLE_A_CHAVE_AQUI
base: https://api.rabisistemas.com.br/api/v1/integrations
ambiente: produção
validade (X-ApiKey-Expires-At): 2026-12-31T23:59:59.000Z
permissões testadas: 25/25 áreas OK em 2026-10-01 (provas/S00/teste-chave-2026-10-01.md)
registrada em: 2026-10-01 · por: implantador (nome no PAPEIS.md)
onde é usada: sessão Claude da clínica (segredo RABI_API_KEY) e ferramentas/rabi_api
como trocar: pedir chave nova ao time Rabi; atualizar o segredo e esta linha; rodar testar_chave
```

Regras:
- a linha **`api_key: rbk_...`** fica sozinha na linha, no começo — é ela que o
  `cliente.py` procura (`grep -n "^api_key:" credenciais/rabi-api-externa.md`);
- **quem escreve o arquivo**: a IA, lendo a variável `RABI_API_KEY` que já está no
  ambiente (sem a chave passar pela conversa), ou o implantador, editando o arquivo
  direto no GitHub;
- antes de gravar, a IA confere que o repo é **privado**; se for público, **não grava** e
  avisa por escrito;
- a cada troca de chave: atualizar segredo + arquivo + rodar o teste da seção 5.

## 3. Validade — `X-ApiKey-Expires-At`

- Toda resposta **autenticada com sucesso** traz o cabeçalho `X-ApiKey-Expires-At`
  (data/hora ISO 8601, ex.: `2026-12-31T23:59:59.000Z`).
- O `cliente.py` guarda o valor da última resposta (`cliente.validade`) e calcula
  `cliente.dias_restantes()`.
- **Alerta 15 dias antes:** se faltarem menos de 15 dias, a IA avisa o dono da clínica
  **no começo da sessão** e registra a pendência (`pendencias/PENDENCIAS.md`): "pedir chave
  nova ao time Rabi". Sem chave nova, a integração para com 401 no dia do vencimento.
- Antes de uma implantação longa: se a chave vence antes do fim previsto, peça a nova
  **antes de começar**.

## 4. Revogação

- A chave é revogada no portal comercial (pelo time Rabi / dono da clínica).
- Depois de revogada, **pode continuar aceita por até 60 segundos**.
- Ao terminar a implantação (S16/S17): revogar a chave de implantação ou reduzi-la às
  permissões da integração contínua (checklist do manual,
  https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#checklist-final).

## 5. Testar a chave

```bash
python3 -m ferramentas.rabi_api.testar_chave --saida provas/S00/teste-chave-AAAA-MM-DD.md
```

Faz **uma leitura por grupo** (25 áreas), só `GET`, sem exibir dado de registro (pacientes:
só a contagem). Mostra a tabela área → OK / SEM PERMISSÃO / CHAVE, a validade e os dias
restantes, e grava um resumo Markdown **sem a chave**.

| Resposta | O que significa | O que fazer |
|---|---|---|
| **401** | chave rejeitada: ausente, errada, vencida ou revogada | **não repetir**; conferir a chave; pedir nova ao time Rabi |
| **403** | chave válida, mas **sem a permissão** da rota (a mensagem diz qual, ex.: `'paciente:read'`) | pedir chave com a permissão (tabela da seção 7) |
| **503** | pelo Swagger de 25/09: falha de rede/tempo ao validar a chave. **Na prática, chave inexistente ainda responde 503** (medido em 25/09/2026 03:07) | o cliente tenta **uma vez** de novo e depois para com `ChaveInvalida`; sem loop. Se persistir com chave certa, avisar o time Rabi |

Atenção: em 3 rotas de parâmetros e nas 3 rotas `PUT /faturamento/glosas/*`, **401 não é
problema de chave** — ver [defeitos-conhecidos.md](defeitos-conhecidos.md). O cliente
trata essas rotas à parte.

## 6. Kit mínimo de permissões

Peça ao time Rabi uma chave com **só o necessário** (manual,
https://www.rabisistemas.com.br/manual/api-externa/index.html#permissoes). Cada recurso
tem catálogo próprio: `empresa:*` não dá acesso a `convenio` nem a `local`.

**Implantação completa (S01–S14):**
`empresa:read/create/update` · `deposito:read/create` · `local:read/create` ·
`auxiliar:read` · `operadora:read/create/update` · `fornecedor:read/create` ·
`fabricante:read/create` · `taxa:read/create/update` · `produto:read/create/update` ·
`equipamento:read/create` · `servico:read/create/update` ·
`colaborador:read/create/update` (o `update` também cria o **login**) ·
`gradeColaborador:read/create` · `gradeEquipamento:read/create` ·
`convenio:read/create/update` · `tabelaPreco:read/create/update` ·
`paciente:read/create/update`.

**Se for migrar histórico:** `atendimento:read/create/update`.

**Opcionais** (saldo inicial de estoque, movimentação financeira, parâmetros pela API):
`estoque:read/create` · `financeiro:read/create` · `parametro:read/update`.

**Para o modo Diagnóstico (só leitura), recomendado pelo kit:** todas as `:read` (25
recursos) — é o que o `testar_chave.py` confere.

**Deixe de fora até precisar (e só com ordem escrita):** todo `:delete`; `nfse:create`,
`nfse:update`, `nfse:delete`; `agendamento:create`/`delete`; `orcamento:create`/`update`;
`faturamento:create`/`update` — ver [proibidas-sem-ordem-escrita.md](proibidas-sem-ordem-escrita.md).

## 7. As 88 permissões (do Swagger de 25/09/2026)

Formato `recurso:ação`. São 25 recursos × 4 ações = 100 combinações, das quais **12 não
existem**: `auxiliar:create/update/delete` (auxiliares são só leitura), `fornecedor:delete`
(exclusão interna é física, não foi exposta), `tabelaPreco:delete`, `financeiro:delete`,
`estoque:update/delete`, `agendamento:update` (cancelar usa `agendamento:delete`),
`orcamento:delete`, `atendimento:delete`, `faturamento:delete`. 100 − 12 = **88**.
`financeiro:create/update` e `orcamento:create` **podem disparar NFS-e automática**.

### 7.1 Mapa por recurso (quantas rotas cada permissão libera)

| Recurso | read | create | update | delete |
|---|---|---|---|---|
| `empresa` | ✅ 2 | ✅ 1 | ✅ 1 | ✅ 1 |
| `deposito` | ✅ 2 | ✅ 2 | ✅ 1 | ✅ 1 |
| `local` | ✅ 2 | ✅ 1 | ✅ 1 | ✅ 1 |
| `auxiliar` | ✅ 14 | — | — | — |
| `operadora` | ✅ 2 | ✅ 2 | ✅ 1 | ✅ 1 |
| `fornecedor` | ✅ 2 | ✅ 2 | ✅ 1 | — |
| `fabricante` | ✅ 2 | ✅ 2 | ✅ 1 | ✅ 1 |
| `taxa` | ✅ 2 | ✅ 2 | ✅ 1 | ✅ 1 |
| `produto` | ✅ 2 | ✅ 2 | ✅ 1 | ✅ 1 |
| `equipamento` | ✅ 2 | ✅ 2 | ✅ 1 | ✅ 1 |
| `servico` | ✅ 2 | ✅ 2 | ✅ 1 | ✅ 1 |
| `colaborador` | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 1 |
| `tabelaPreco` | ✅ 4 | ✅ 1 | ✅ 3 | — |
| `convenio` | ✅ 11 | ✅ 2 | ✅ 7 | ✅ 1 |
| `gradeColaborador` | ✅ 3 | ✅ 1 | ✅ 1 | ✅ 2 |
| `gradeEquipamento` | ✅ 2 | ✅ 1 | ✅ 1 | ✅ 1 |
| `financeiro` | ✅ 2 | ✅ 2 | ✅ 1 | — |
| `estoque` | ✅ 9 | ✅ 3 | — | — |
| `paciente` | ✅ 4 | ✅ 2 | ✅ 4 | ✅ 1 |
| `parametro` | ✅ 21 | ✅ 3 | ✅ 20 | ✅ 1 |
| `agendamento` | ✅ 6 | ✅ 1 | — | ✅ 1 |
| `orcamento` | ✅ 6 | ✅ 1 | ✅ 3 | — |
| `atendimento` | ✅ 2 | ✅ 2 | ✅ 2 | — |
| `faturamento` | ✅ 16 | ✅ 1 | ✅ 7 | — |
| `nfse` | ✅ 14 | ✅ 8 | ✅ 3 | ✅ 3 |

### 7.2 Cada permissão e as rotas que ela libera

| Permissão | Rotas liberadas |
|---|---|
| `empresa:read` | `GET /empresas` · `GET /empresas/{id}` |
| `empresa:create` | `POST /empresas` |
| `empresa:update` | `PUT /empresas/{id}` |
| `empresa:delete` | `DELETE /empresas/{id}` |
| `deposito:read` | `GET /depositos` · `GET /depositos/{id}` |
| `deposito:create` | `POST /depositos` · `POST /depositos/bulk` |
| `deposito:update` | `PUT /depositos/{id}` |
| `deposito:delete` | `DELETE /depositos/{id}` |
| `local:read` | `GET /locais` · `GET /locais/{id}` |
| `local:create` | `POST /locais` |
| `local:update` | `PUT /locais/{id}` |
| `local:delete` | `DELETE /locais/{id}` |
| `auxiliar:read` | as 14 rotas `GET /auxiliares/*` |
| `operadora:read` | `GET /operadoras` · `GET /operadoras/{id}` |
| `operadora:create` | `POST /operadoras` · `POST /operadoras/bulk` |
| `operadora:update` | `PUT /operadoras/{id}` |
| `operadora:delete` | `DELETE /operadoras/{id}` |
| `fornecedor:read` | `GET /fornecedores` · `GET /fornecedores/{id}` |
| `fornecedor:create` | `POST /fornecedores` · `POST /fornecedores/bulk` |
| `fornecedor:update` | `PUT /fornecedores/{id}` |
| `fabricante:read` | `GET /fabricantes` · `GET /fabricantes/{id}` |
| `fabricante:create` | `POST /fabricantes` · `POST /fabricantes/bulk` |
| `fabricante:update` | `PUT /fabricantes/{id}` |
| `fabricante:delete` | `DELETE /fabricantes/{id}` |
| `taxa:read` | `GET /taxas` · `GET /taxas/{id}` |
| `taxa:create` | `POST /taxas` · `POST /taxas/bulk` |
| `taxa:update` | `PUT /taxas/{id}` |
| `taxa:delete` | `DELETE /taxas/{id}` |
| `produto:read` | `GET /produtos` · `GET /produtos/{id}` |
| `produto:create` | `POST /produtos` · `POST /produtos/bulk` |
| `produto:update` | `PUT /produtos/{id}` |
| `produto:delete` | `DELETE /produtos/{id}` |
| `equipamento:read` | `GET /equipamentos` · `GET /equipamentos/{id}` |
| `equipamento:create` | `POST /equipamentos` · `POST /equipamentos/bulk` |
| `equipamento:update` | `PUT /equipamentos/{id}` |
| `equipamento:delete` | `DELETE /equipamentos/{id}` |
| `servico:read` | `GET /servicos` · `GET /servicos/{id}` |
| `servico:create` | `POST /servicos` · `POST /servicos/bulk` |
| `servico:update` | `PUT /servicos/{id}` |
| `servico:delete` | `DELETE /servicos/{id}` |
| `colaborador:read` | `GET /colaboradores` · `GET /colaboradores/{id}` |
| `colaborador:create` | `POST /colaboradores` · `POST /colaboradores/bulk` |
| `colaborador:update` | `PUT /colaboradores/{id}` · `POST /colaboradores/{id}/usuario` |
| `colaborador:delete` | `DELETE /colaboradores/{id}` |
| `tabelaPreco:read` | `GET /tabelas-preco` · `GET /tabelas-preco/{id}` · `GET /tabelas-preco/precificacao` · `GET /tabelas-preco/produtos` |
| `tabelaPreco:create` | `POST /tabelas-preco` |
| `tabelaPreco:update` | `PUT /tabelas-preco/{id}` · `POST /tabelas-preco/produtos` · `POST /tabelas-preco/produtos/bulk` |
| `convenio:read` | `GET /convenios` · `GET /convenios/{id}/colaboradores` · `GET /convenios/{id}/taxas` · `GET /convenios/{id}/servicos` · `GET /convenios/{id}/produtos` · `GET /convenios/{id}/especialidades` · `GET /convenios/{id}/planos` · `GET /convenios/{id}/farol/produtos` · `GET /convenios/{id}/farol/servicos` · `GET /convenios/{id}/farol/itens` · `GET /convenios/{id}` |
| `convenio:create` | `POST /convenios` · `POST /convenios/bulk` |
| `convenio:update` | `PUT /convenios/{id}/colaboradores` · `PUT /convenios/{id}/taxas` · `PUT /convenios/{id}/servicos` · `PUT /convenios/{id}/produtos` · `PUT /convenios/{id}/especialidades` · `PUT /convenios/{id}/planos` · `PUT /convenios/{id}` |
| `convenio:delete` | `DELETE /convenios/{id}` |
| `gradeColaborador:read` | `GET /grades-colaborador` · `GET /grades-colaborador/filter` · `GET /grades-colaborador/{id}` |
| `gradeColaborador:create` | `POST /grades-colaborador` |
| `gradeColaborador:update` | `PUT /grades-colaborador/{id}` |
| `gradeColaborador:delete` | `DELETE /grades-colaborador/{id}` · `DELETE /grades-colaborador/unique/{id}` |
| `gradeEquipamento:read` | `GET /grades-equipamento` · `GET /grades-equipamento/{id}` |
| `gradeEquipamento:create` | `POST /grades-equipamento` |
| `gradeEquipamento:update` | `PUT /grades-equipamento/{id}` |
| `gradeEquipamento:delete` | `DELETE /grades-equipamento/{id}` |
| `financeiro:read` | `GET /financeiro/movimentacoes` · `GET /financeiro/movimentacoes/{id}` |
| `financeiro:create` | `POST /financeiro/movimentacoes` · `POST /financeiro/movimentacoes/bulk` |
| `financeiro:update` | `PUT /financeiro/movimentacoes/{id}` |
| `estoque:read` | `GET /estoque` · `GET /estoque/saldo-produtos` · `GET /estoque/{id}` · `GET /estoque/historico/{id}` · `GET /estoque/ultima-compra/{id}` · `GET /estoque/movimentacao/{id}` · `GET /estoque/buscar/{lote}/{produtoId}/{localizacaoId}` · `GET /estoque/lotes-produtos/{idProduto}/{idLocalizacao}` · `POST /estoque/previsao` |
| `estoque:create` | `POST /estoque/entrada` · `POST /estoque/saida` · `POST /estoque/transferencia` |
| `paciente:read` | `GET /pacientes` · `GET /pacientes/{id}` · `GET /pacientes/{id}/convenios` · `GET /pacientes/{id}/anexos` |
| `paciente:create` | `POST /pacientes` · `POST /pacientes/bulk` |
| `paciente:update` | `PUT /pacientes/{id}` · `POST /pacientes/{id}/convenios` · `PUT /pacientes/{id}/convenios/{vinculoId}` · `POST /pacientes/{id}/anexos` |
| `paciente:delete` | `DELETE /pacientes/{id}` |
| `parametro:read` | `GET /parametros/desconto` · `GET /parametros/desconto/colaboradores/{nivel}` · `GET /parametros/desconto/colaborador/{id}` · `GET /parametros/alcada-compra/colaborador/{id}` · `GET /parametros/financeiro` · `GET /parametros/orcamento` · `GET /parametros/estoque` · `GET /parametros/avisos` · `GET /parametros/avisos/{chave}` · `GET /parametros/acolhimento` · `GET /parametros/acolhimento/validar/{pacienteId}` · `GET /parametros/acolhimento/historico-confirmacoes/{pacienteId}` · `GET /parametros/servicos-online` · `GET /parametros/servicos-online/link` · `GET /parametros/servicos-online/agendamento/perguntas` · `GET /parametros/servicos-online/agendamento/perguntas/por-especialidade` · `GET /parametros/servicos-online/agendamento/perguntas/colaborador/{colaboradorId}` · `GET /parametros/termo` · `GET /parametros/dashboard-permissoes/graficos` · `GET /parametros/dashboard-permissoes/dashboards` · `GET /parametros/dashboard-atribuicao` |
| `parametro:create` | `POST /parametros/desconto/colaborador/{id}` · `POST /parametros/alcada-compra/colaborador/{id}` · `POST /parametros/servicos-online/agendamento/perguntas` |
| `parametro:update` | `PUT /parametros/desconto` · `PUT /parametros/financeiro` · `PUT /parametros/orcamento` · `PUT /parametros/estoque` · `PUT /parametros/avisos/{chave}` · `PUT /parametros/acolhimento` · `POST /parametros/acolhimento/atualizar-validacoes/{pacienteId}` · `PATCH /parametros/servicos-online/habilitar` · `PATCH /parametros/servicos-online/agendamento/habilitar` · `PATCH /parametros/servicos-online/agendamento/mudanca-colaborador/habilitar` · `PATCH /parametros/servicos-online/confirmacao/habilitar` · `PATCH /parametros/servicos-online/prontuario/habilitar` · `PATCH /parametros/servicos-online/lista-medico-convenio/habilitar` · `PATCH /parametros/servicos-online/textos-informativos` · `PUT /parametros/servicos-online/agendamento/perguntas/{id}` · `POST /parametros/servicos-online/agendamento/perguntas/{perguntaId}/colaborador/{colaboradorId}` · `PUT /parametros/termo` · `PUT /parametros/dashboard-permissoes/graficos` · `PUT /parametros/dashboard-permissoes/dashboards` · `PUT /parametros/dashboard-atribuicao` |
| `parametro:delete` | `DELETE /parametros/servicos-online/agendamento/perguntas/{id}` |
| `agendamento:read` | `GET /agendamentos/datas/disponiveis` · `POST /agendamentos/horarios/disponiveis` · `GET /agendamentos/locais/disponiveis` · `GET /agendamentos/motivo-cancelamento` · `GET /agendamentos` · `GET /agendamentos/{id}` |
| `agendamento:create` | `POST /agendamentos` |
| `agendamento:delete` | `PATCH /agendamentos/{id}/cancelar` |
| `orcamento:read` | `GET /orcamentos` · `GET /orcamentos/status` · `GET /orcamentos/consideracoes` · `GET /orcamentos/{id}/{isAgendamento}` · `GET /orcamentos/anexo/listar/{orcamentoId}` · `GET /orcamentos/anexo/listar-necessarios/{pacienteId}` |
| `orcamento:create` | `POST /orcamentos` |
| `orcamento:update` | `PUT /orcamentos/{id}` · `PUT /orcamentos/status/{idOrcamento}/{idStatus}` · `POST /orcamentos/anexo/vincular/{anexoId}/{orcamentoId}` |
| `atendimento:read` | `GET /atendimentos/{id}` · `GET /atendimentos/historico` |
| `atendimento:create` | `POST /atendimentos` · `POST /atendimentos/novo-prontuario` |
| `atendimento:update` | `PUT /atendimentos/{id}` · `POST /atendimentos/prontuario` |
| `faturamento:read` | `GET /faturamento/guias` · `GET /faturamento/guias/buscar-por-numero-guia` · `GET /faturamento/guias/pacientes` · `GET /faturamento/guias/info-extras/{guiaMae}/{guiaFilha}` · `GET /faturamento/guias/valores-atualizados/{guiaMae}/{guiaFilha}` · `GET /faturamento/guias/conversoes-convenio/{guiaMae}/{guiaFilha}/{convenioId}` · `GET /faturamento/guias/{guiaMae}/filhas` · `GET /faturamento/guias/servico/{guiaFilha}` · `GET /faturamento/guias/valores-atendimento/{atendimentoId}` · `GET /faturamento/divergencias` · `GET /faturamento/recebimento` · `GET /faturamento/recebimento/opcoes` · `GET /faturamento/glosas` · `GET /faturamento/glosas/guia/{guiaMae}` · `GET /faturamento/glosas/status` · `GET /faturamento/glosas/motivos` |
| `faturamento:create` | `POST /faturamento/recebimento/registrar` |
| `faturamento:update` | `PUT /faturamento/guias/{servicoAtendimentoId}` · `PUT /faturamento/guias/{guiaMae}/confirmar` · `POST /faturamento/divergencias/{numeroGuiaMae}/faturar-diferenca` · `POST /faturamento/recebimento/devolver` · `PUT /faturamento/glosas/produto` · `PUT /faturamento/glosas/taxa` · `PUT /faturamento/glosas/servico` |
| `nfse:read` | `GET /nfse/emitentes` · `GET /nfse/emitentes/{id}` · `GET /nfse/perfis-fiscais` · `GET /nfse/perfis-fiscais/{id}` · `GET /nfse/tomadores` · `GET /nfse/tomadores/{id}` · `POST /nfse/tomadores/sincronizar-paciente/{pacienteId}` · `GET /nfse/notas` · `GET /nfse/notas/{id}` · `GET /nfse/notas/{id}/xml` · `GET /nfse/notas/{id}/links` · `GET /nfse/notas/{id}/danfse.html` · `GET /nfse/notas/{id}/danfse.pdf` · `GET /nfse/notas/{id}/tentativas` |
| `nfse:create` | `POST /nfse/tomadores` · `POST /nfse/tomadores/bulk` · `POST /nfse/notas` · `POST /nfse/notas/{id}/emitir` · `POST /nfse/notas/{id}/consultar-protocolo` · `POST /nfse/notas/{id}/emitir-contingencia` · `POST /nfse/notas/{id}/transmitir-contingencia` · `POST /nfse/notas/{id}/substituir` |
| `nfse:update` | `PUT /nfse/tomadores/{id}` · `POST /nfse/tomadores/{id}/completar` · `PUT /nfse/notas/{id}/tomador` |
| `nfse:delete` | `POST /nfse/notas/{id}/desistir` · `POST /nfse/notas/{id}/cancelar` · `POST /nfse/notas/{id}/analise-fiscal` |

Conferência (script sobre o spec): **88 permissões distintas**, todas as 268 operações com
permissão declarada. A lista também está no manual, com links para cada rota:
https://www.rabisistemas.com.br/manual/api-externa/index.html#permissoes.
