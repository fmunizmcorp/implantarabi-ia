# Como começar — para o dono da clínica ou o implantador

> **Fonte:** kit implantarabi-ia · **Conferido em:** 2026-09-25
> **Vale para:** kit v0.1.0 · **Kit:** v0.1.0

Você não precisa saber programar. São **5 passos**, uma vez só. Depois, cada
dia de trabalho é: abrir a sessão e conversar.

**O que você vai precisar:** uma conta no **GitHub**, uma conta no **Claude**
(com acesso ao Claude Code na web) e a **chave da API do Rabi** (começa com
`rbk_`; quem entrega é a Rabi Sistemas, pelo portal ou pelo suporte).

---

## Passo 1 — Criar o repositório PRIVADO da clínica no GitHub

1. Entre em https://github.com/new
2. Nome sugerido: `rabi-implantacao-<nome-da-clinica>` (minúsculas, sem acento, com hífen).
   Ex.: `rabi-implantacao-clinica-exemplo`.
3. Marque **Private** (privado). ⚠️ **Obrigatório**: este repositório vai guardar
   a chave da API e senhas em texto claro.
4. Marque "Add a README file" (para o repositório não nascer vazio) e clique em **Create repository**.

## Passo 2 — Gerar o conteúdo a partir do modelo do kit

1. Abra o Claude Code na web (https://claude.ai/code) **no repositório que você acabou de criar**.
2. Cole esta mensagem e envie:

```
Prepare este repositório como repo de implantação do Sistema Rabi.
1) Baixe o kit: git clone --depth 1 https://github.com/fmunizmcorp/implantarabi-ia .kit
2) Rode: python3 .kit/ferramentas/kit/novo_repo_clinica.py --destino . --clinica "<NOME DA CLÍNICA>" --porte <consultorio|pequena-media|rede> --forcar
3) Confira que ESTADO.md, CLAUDE.md, .claude/settings.json e .gitignore existem e que .kit/ está no .gitignore.
4) Faça commit ("S00: repo criado a partir do modelo do kit") e push. Confira que .github/workflows/automerge.yml foi junto: ele leva o trabalho da branch desta sessão para a main em ~1 min.
5) Me diga em 3 linhas o que foi criado. Não grave nada no Rabi.
```

Troque `<NOME DA CLÍNICA>` pelo nome da clínica e escolha o porte:
`consultorio` (1 profissional), `pequena-media` ou `rede` (várias unidades).

> O kit é **público**: não precisa pedir acesso. Se o passo 1 falhar, é falta
> de internet no ambiente ou o GitHub fora do ar: tente de novo em alguns
> minutos. **Plano B:** baixe o ZIP em https://github.com/fmunizmcorp/implantarabi-ia
> (botão *Code → Download ZIP*), descompacte e envie o conteúdo para a sessão,
> pedindo que ela o coloque na pasta `.kit/` (tem de existir `.kit/BOOTSTRAP.md`).
>
> Se o GitHub recusar o push do arquivo `.github/workflows/automerge.yml`,
> crie-o pela página do repositório (*Add file → Create new file*) colando o
> conteúdo de `.kit/modelo-repo-clinica/.github/workflows/automerge.yml`. Em
> *Settings → Actions → General → Workflow permissions*, marque **Read and write**.

## Passo 3 — Configurar o segredo da chave (RABI_API_KEY)

Use **um ambiente por clínica** no Claude Code na web (assim a chave de uma
clínica nunca se mistura com a de outra).

1. Na sessão deste repositório, abra o **menu do ambiente** na barra de título
   da sessão e escolha **Edit** (Editar).
2. Se houver a seção **"API credentials"**, cadastre a chave ali; se não houver,
   adicione uma **variável de ambiente**:
   - **Nome:** `RABI_API_KEY`
   - **Valor:** a chave `rbk_…` que a Rabi entregou.
3. Salve. A chave passa a valer nas **sessões novas** (abra uma sessão nova).

⚠️ **Nunca cole a chave no chat**, nem em issue, e-mail ou mensagem. Não é
preciso: a própria sessão grava o arquivo `credenciais/rabi-api-externa.md`
do repo privado **a partir da variável**, sem a chave passar pela conversa.
Detalhes: `.kit/conhecimento/api-externa/chave-e-token.md` §2.1.

## Passo 4 — Abrir a sessão de trabalho

Abra uma **nova** sessão do Claude Code na web neste repositório. A sessão
baixa o kit sozinha, lê o painel e se apresenta.

## Passo 5 — Colar o prompt de abertura (só na primeira vez)

```
Você é a IA implantadora do Sistema Rabi desta clínica. Siga o CLAUDE.md deste
repositório e o kit em .kit/. Apresente-se conforme .kit/prompts/01-abertura-sessao.md,
mostre o painel e me pergunte o modo. Uma pergunta por vez.
```

Nas próximas vezes basta escrever **"vamos continuar"**.

---

## Depois disso, o seu papel é só este
1. **Entregar** os documentos que a IA pedir (em qualquer formato).
2. **Aprovar** o que ela mostra antes de gravar ("pode gravar").
3. **Conferir** o resultado que ela mostra depois.

A IA faz o resto e salva tudo no repositório a cada passo: commit + push na
branch da sessão (`claude/...`); o workflow `automerge` leva à `main` em ~1 min;
ao abrir, a sessão confere que o `ESTADO.md` da `main` é o mais recente
(`git log origin/main -1`).
