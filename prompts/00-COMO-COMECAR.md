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
4) Faça commit ("S00: repo criado a partir do modelo do kit") e push.
5) Me diga em 3 linhas o que foi criado. Não grave nada no Rabi.
```

Troque `<NOME DA CLÍNICA>` pelo nome da clínica e escolha o porte:
`consultorio` (1 profissional), `pequena-media` ou `rede` (várias unidades).

> Se o passo 1 da mensagem falhar por falta de acesso ao kit, peça à Rabi
> Sistemas acesso de leitura ao repositório `implantarabi-ia` para a sua conta
> GitHub (ou uma cópia do kit).

## Passo 3 — Configurar o segredo da chave (RABI_API_KEY)

No Claude Code na web, nas configurações do **ambiente** deste repositório,
crie a variável de ambiente (segredo):

- **Nome:** `RABI_API_KEY`
- **Valor:** a chave `rbk_…` que a Rabi entregou.

Não cole a chave em issue, e-mail ou mensagem pública. A sessão também vai
registrá-la no arquivo `credenciais/rabi-api-externa.md` do repo privado.

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

A IA faz o resto e salva tudo no repositório (commit + push) a cada passo.
