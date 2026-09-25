# Parte A — Preparação (uma vez por clínica, ~15 minutos)

> **Fonte:** este kit ([chave-e-token](../conhecimento/api-externa/chave-e-token.md)) + https://www.rabisistemas.com.br/manual/api-externa/index.html#permissoes + https://code.claude.com/docs/en/claude-code-on-the-web · **Conferido em:** 2026-09-25
> **Vale para:** produção em 25/09/2026 · **Kit:** v0.1.2

Faça os passos **na ordem**. Cada passo diz o que você vai ver na tela e o que
fazer se não vir. As telas do GitHub e do Claude mudam de vez em quando: se um
nome de botão estiver um pouco diferente, procure o mais parecido.

Voltar ao [manual](../MANUAL-PASSO-A-PASSO.md).

---

## A1 — Contas necessárias

Você precisa de **duas contas**, em nome da clínica (ou de quem vai cuidar da
implantação):

1. **GitHub** (gratuito) — é onde fica o "caderno" da clínica.
   - Abra https://github.com/signup e siga as telas (e-mail, senha, nome de usuário).
   - Confirme o e-mail (o GitHub manda um código).
   - Já tem conta? Use a que já existe.
2. **Claude com acesso ao Claude Code na web** — é onde a IA trabalha.
   - Abra https://claude.ai e entre (ou crie a conta).
   - O Claude Code na web (https://claude.ai/code) exige um **plano pago que
     inclua o Claude Code**. **Não tenho certeza de quais planos exatamente**
     incluem: confira na página de planos do claude.ai antes de assinar.
   - Teste: abra https://claude.ai/code. Se aparecer a tela para escolher um
     repositório (ou para conectar o GitHub), está certo. Se aparecer um convite
     para assinar, o plano atual não inclui.

## A2 — Pedir a chave da API do Rabi

A **chave da API** é o código (começa com `rbk_`) que deixa a IA ler e gravar
os cadastros **desta** clínica no Rabi. Quem gera é a **Rabi Sistemas**, pelo
portal comercial (time Rabi). Não há autoatendimento.

Peça ao time Rabi (pelo mesmo canal de contato comercial ou de suporte):

> "Preciso de uma chave da API externa para a implantação da clínica
> <Nome da Clínica>, com as permissões completas de implantação."

**Permissões completas de implantação** (o time Rabi entende esta lista;
cada item é `recurso:ação`):

- `empresa:read/create/update` · `deposito:read/create` · `local:read/create` · `auxiliar:read`
- `operadora:read/create/update` · `fornecedor:read/create` · `fabricante:read/create`
- `taxa:read/create/update` · `produto:read/create/update` · `equipamento:read/create`
- `servico:read/create/update` · `colaborador:read/create/update` (o `update` também cria o **login**)
- `gradeColaborador:read/create` · `gradeEquipamento:read/create`
- `convenio:read/create/update` · `tabelaPreco:read/create/update` · `paciente:read/create/update`
- Se for migrar histórico de atendimentos: `atendimento:read/create/update`.
- Opcionais (saldo de estoque, financeiro, parâmetros): `estoque:read/create` ·
  `financeiro:read/create` · `parametro:read/update`.
- **Não peça** (a IA não usa sem ordem escrita): nenhum `:delete`, nada de
  `nfse` de escrita, `agendamento:create`, `orcamento:create/update`,
  `faturamento:create/update`.

Detalhe e explicação de cada permissão: [chave-e-token.md §6](../conhecimento/api-externa/chave-e-token.md).

**Três avisos importantes:**
- **A chave aparece uma vez só**, quando é criada. Guarde-a num lugar seguro
  (gerenciador de senhas). Perdeu? Não há como recuperar: peça outra.
- **Validade curta.** Uma chave de implantação medida em 25/09/2026 valia
  **cerca de 7 dias**. Anote a data. Peça a renovação **alguns dias antes** de
  vencer, não no dia. A IA mostra a validade no começo de toda sessão.
- **Nunca mande a chave por e-mail, WhatsApp ou no chat do Claude.** Ela vai
  só no ambiente do Claude (passo A6).

Enquanto a chave não chega, você pode seguir A3–A5 e até abrir a primeira
sessão: a IA organiza os documentos e espera a chave para gravar.

## A3 — Criar o repositório da clínica pelo modelo

O **repositório** é a pasta online (no GitHub) onde fica o caderno da clínica.
Você vai criá-lo a partir de um **modelo pronto**.

1. Entre no GitHub com a conta da clínica.
2. Abra este link: https://github.com/fmunizmcorp/implantarabi-modelo-clinica/generate
   - **O que você vê:** a tela **"Create a new repository"**, com o modelo
     `fmunizmcorp/implantarabi-modelo-clinica` já escolhido em cima.
3. **Owner** (dono): escolha a **conta da clínica** na lista.
4. **Repository name** (nome): `rabi-implantacao-<nome-da-clinica>` — tudo
   minúsculo, sem acento, com hífen. Ex.: `rabi-implantacao-clinica-exemplo`.
5. **Description**: pode deixar em branco.
6. Marque **Private** (privado). **É obrigatório.** Por quê: este repositório
   vai guardar a chave da API e as senhas iniciais dos usuários **em texto
   claro** (decisão do dono, para ninguém perder acesso). Se ficar público,
   qualquer pessoa na internet lê.
7. Deixe **"Include all branches"** desmarcado.
8. Clique em **Create repository**.
   - **O que você vê:** em alguns segundos, a página do repositório novo, com
     arquivos como `CLAUDE.md`, `ESTADO.md`, pastas `dados`, `sprints`… e um
     texto dizendo que ainda é o modelo. Está certo: a IA troca esse texto na
     primeira sessão.
   - Confira: ao lado do nome aparece a etiqueta **Private**. Se aparecer
     **Public**, veja [Parte E](04-problemas-e-seguranca.md) ("repo público").

**Se o link não abrir** (página 404 ou "not found"): o modelo ainda não foi
publicado pela Rabi. Use o **plano B**:

1. Abra https://github.com/new
2. Nome `rabi-implantacao-<nome-da-clinica>`, marque **Private**, marque
   **"Add a README file"** e clique em **Create repository**.
3. Faça A4 e A5 abaixo, abra uma sessão do Claude Code nesse repositório
   (A6 e Parte B) e envie **esta** mensagem (troque o nome e o porte):

```
Prepare este repositório como repo de implantação do Sistema Rabi.
1) Baixe o kit: git clone --depth 1 https://github.com/fmunizmcorp/implantarabi-ia .kit
2) Rode: python3 .kit/ferramentas/kit/novo_repo_clinica.py --destino . --clinica "<NOME DA CLÍNICA>" --porte <consultorio|pequena-media|rede> --forcar
3) Confira que ESTADO.md, CLAUDE.md, .claude/settings.json e .gitignore existem e que .kit/ está no .gitignore.
4) Faça commit ("S00: repo criado a partir do modelo do kit") e push. Confira que .github/workflows/automerge.yml foi junto: ele leva o trabalho da branch desta sessão para a main em ~1 min.
5) Me diga em 3 linhas o que foi criado. Não grave nada no Rabi.
```

   Porte: `consultorio` (1 profissional), `pequena-media` ou `rede` (várias
   unidades). Se o GitHub recusar o arquivo `.github/workflows/automerge.yml`,
   crie-o pela página do repositório (*Add file → Create new file*), colando o
   conteúdo de `.kit/modelo-repo-clinica/.github/workflows/automerge.yml`.
   Depois, numa sessão nova, escreva `Vamos implantar <Nome da Clínica>`.

## A4 — Liberar a gravação automática (Actions)

**Para quê:** cada conversa com a IA trabalha numa "cópia de rascunho" (uma
branch chamada `claude/...`). Um robô do GitHub (o workflow **automerge**)
leva esse trabalho para a versão principal (`main`) em cerca de 1 minuto. É a
`main` que a próxima conversa abre. Sem esta permissão, a próxima conversa não
vê o que a anterior fez.

1. Na página do repositório da clínica, clique em **Settings** (Configurações;
   ícone de engrenagem, na barra de abas do repositório, à direita).
   - Não vê **Settings**? Você não é dono/administrador do repositório. Peça ao
     dono para fazer este passo.
2. No menu da esquerda: **Actions → General**.
3. Role até **"Workflow permissions"**.
4. Marque **"Read and write permissions"**.
5. Clique em **Save**.
   - **O que você vê:** uma mensagem de confirmação no topo, e a opção marcada.
6. (Na mesma página, em cima) confira que **"Actions permissions"** está em
   **"Allow all actions and reusable workflows"** (é o padrão). Se estiver
   "Disable actions", o robô não roda.

## A5 — Ligar o GitHub ao Claude

1. Abra https://claude.ai/connect-github e siga as telas para **conectar** a
   sua conta do GitHub ao Claude (o GitHub pede para autorizar: clique em
   **Authorize**).
2. Instale o **app Claude** no repositório da clínica:
   https://github.com/apps/claude/installations/select_target
   - Escolha a **conta da clínica** (a mesma do Owner em A3).
   - Em **Repository access**, escolha **Only select repositories** e marque o
     `rabi-implantacao-<clínica>` (ou "All repositories", se preferir).
   - Clique em **Install** (ou **Save**, se já estava instalado).
3. Teste: abra https://claude.ai/code e clique na lista de repositórios. O
   `rabi-implantacao-<clínica>` tem de aparecer.
   - Não aparece? Refaça o passo 2 conferindo a conta e o repositório marcados;
     depois recarregue a página do Claude.

## A6 — Criar o ambiente da clínica no Claude e registrar a chave

O **ambiente** é a "sala de trabalho" da IA no Claude Code na web: define o
que ela pode acessar na internet e guarda a chave. Use **um ambiente por
clínica**, para a chave de uma clínica nunca se misturar com a de outra.

1. Abra https://claude.ai/code e escolha o repositório `rabi-implantacao-<clínica>`.
2. Abra o **menu do ambiente** (na barra de título da sessão, perto do nome
   do repositório; mostra o nome do ambiente atual, por exemplo "Default").
3. Crie um ambiente novo (**Add environment** ou parecido) com o nome da
   clínica, por exemplo `Rabi - Clínica Exemplo`. Se já existe, escolha-o e
   clique em **Edit**.
4. **Chave da API:**
   - Se a tela tiver a seção **"API credentials"**, cadastre a chave ali.
   - Se não tiver, em **Environment variables** (variáveis de ambiente)
     escreva uma linha exatamente assim, trocando pelo valor recebido do Rabi:
     `RABI_API_KEY=rbk_...` (sem espaços, sem aspas).
5. **Acesso à rede (Network access):** a IA precisa falar com o GitHub (para
   baixar o kit) e com a API do Rabi. Se a opção de rede for limitada a
   domínios confiáveis, **acrescente aos domínios permitidos**:
   `api.rabisistemas.com.br` (e `api.hmg.rabisistemas.dev`, se for ensaiar em
   homologação). Os níveis de acesso estão descritos em
   https://code.claude.com/docs/en/claude-code-on-the-web.
6. Clique em **Save**.
7. A chave vale nas **sessões novas**: abra uma sessão nova depois de salvar.

**Nunca cole a chave no chat.** Não é preciso: a IA lê a variável e registra
a chave no arquivo `credenciais/rabi-api-externa.md` do repositório privado,
sem a chave aparecer na conversa.

Se a tela estiver diferente destes nomes, siga a documentação oficial:
https://code.claude.com/docs/en/claude-code-on-the-web (ambientes e variáveis
de ambiente).

## A7 — Checklist da preparação

- [ ] Conta no GitHub (da clínica) criada e e-mail confirmado.
- [ ] Claude com acesso a https://claude.ai/code.
- [ ] Chave da API pedida ao time Rabi (com as permissões de implantação); data de validade anotada.
- [ ] Repositório `rabi-implantacao-<clínica>` criado pelo modelo e marcado **Private**.
- [ ] *Settings → Actions → General → Workflow permissions* = **Read and write**.
- [ ] GitHub conectado ao Claude e app Claude instalado no repositório.
- [ ] Ambiente da clínica criado no Claude Code com `RABI_API_KEY` e rede liberada para `api.rabisistemas.com.br`.

Pronto? Vá para a [Parte B — Primeira sessão](02-primeira-sessao.md).
