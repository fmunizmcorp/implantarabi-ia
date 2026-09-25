# Partes E e F — Problemas comuns e segurança

> **Fonte:** este kit ([chave-e-token](../conhecimento/api-externa/chave-e-token.md), [políticas](../metodologia/politicas.md)) · **Conferido em:** 2026-09-25
> **Vale para:** produção em 25/09/2026 · **Kit:** v0.1.2

Voltar ao [manual](../MANUAL-PASSO-A-PASSO.md).

> 🔒 **Validade curta é proteção, não problema** (decisão do proprietário, 25/09/2026): a chave **deve** expirar, e pedir uma chave nova ao time Rabi é o **fluxo normal** da implantação. A sessão avisa com antecedência, pede a chave nova ao dono e segue — nunca trata o vencimento como falha nem tenta contornar a expiração.

## Parte E — Problemas comuns (sintoma → o que fazer)

### A chave está vencendo ou venceu
**Sintoma:** a IA avisa "a chave vence em N dias", ou diz que a API respondeu
**503** ("Não foi possível validar a chave de API") ou **401**.
**O que fazer:**
1. Peça uma **chave nova** ao time Rabi (mesmas permissões — lista no passo A2
   da [Parte A](01-preparacao.md)).
2. No Claude Code: menu do ambiente da clínica → **Edit** → troque o valor de
   `RABI_API_KEY` (ou em "API credentials") → **Save**.
3. Abra uma **sessão nova** e escreva `continuar`. A IA testa a chave nova e
   registra a troca.
A IA **não fica tentando de novo** com chave ruim: ela para e avisa.

### O repositório está público
**Sintoma:** a IA avisa "o repositório está PÚBLICO", ou você vê a etiqueta
**Public** ao lado do nome no GitHub.
**O que fazer:**
1. No repositório: **Settings** → role até o fim (**Danger Zone**) →
   **Change visibility** → **Change to private** → confirme digitando o nome.
2. Se uma chave já tiver ido para o repositório enquanto ele estava público:
   peça ao time Rabi para **revogar** essa chave e emitir outra.
A IA não grava credenciais enquanto o repositório estiver público.

### A sessão não achou o kit
**Sintoma:** a IA diz que o download do kit falhou ou que `.kit/` não existe.
**O que fazer:**
1. Feche e abra uma **sessão nova** (costuma ser falha momentânea de internet).
2. Confira o **acesso à rede** do ambiente (passo A6): o GitHub tem de estar liberado.
3. **Plano B (ZIP):** baixe o kit em https://github.com/fmunizmcorp/implantarabi-ia
   (botão **Code → Download ZIP**), anexe o ZIP na conversa e peça: "coloque o
   conteúdo deste ZIP na pasta .kit/ (tem de existir .kit/BOOTSTRAP.md) e não
   versione". Sem o kit, a IA **não grava nada** no Rabi.

### O robô que leva o trabalho para a main falhou
**Sintoma:** na aba **Actions** do repositório aparece um "X" vermelho no
**automerge**; ou a sessão nova não vê o trabalho de ontem.
**O que fazer:**
1. Refaça o passo **A4** (*Settings → Actions → General → Workflow permissions →
   Read and write → Save*).
2. Na aba **Actions**, abra o automerge com erro e clique em **Re-run jobs**.
3. Ainda vermelho? Numa sessão, escreva: "o automerge falhou, veja e corrija".

### O trabalho "sumiu"
**Sintoma:** a sessão nova não mostra o que foi feito na anterior.
**O que fazer:**
1. No GitHub, clique no seletor de branch (onde está escrito **main**) e veja
   se existe uma branch `claude/...` recente. O trabalho está lá.
2. Veja a aba **Actions**: o automerge dessa branch rodou? Se não, veja o item
   anterior.
3. Numa sessão nova, escreva: "o trabalho da branch claude/... não chegou na
   main". A IA confere e traz.
Nada se perde: toda sessão faz commit + push a cada passo.

### Trocar de implantador
**O que fazer:**
1. Dê acesso ao repositório para a pessoa nova: **Settings → Collaborators →
   Add people** (ela precisa de conta no GitHub).
2. Dê acesso ao **ambiente** da clínica no Claude Code (ou crie o ambiente na
   conta dela, com a mesma chave — passo A6).
3. A pessoa nova abre uma sessão e escreve `continuar`. A IA retoma pelo
   `ESTADO.md` e atualiza os papéis em `PAPEIS.md`.

### A IA pediu algo que você não tem
**O que fazer:** responda "não temos" (ou "não sei — pergunte a Fulano"). Vira
uma **pendência** anotada; a IA não inventa valor. Se aquilo trava uma etapa,
ela diz o efeito prático e segue com o que der.

### A IA falou de outra clínica
**Sintoma:** você escreveu `Vamos implantar <outra clínica>` e ela respondeu
que "este repositório é da clínica X".
**O que fazer:** você abriu o repositório errado. Cada clínica tem o **seu**
repositório (passo A3). Abra a sessão no repositório certo.

## Parte F — Segurança e LGPD

- **Repositório privado, sempre.** Ele guarda a chave da API e as senhas
  iniciais em texto claro (decisão do dono, para ninguém perder acesso). Só
  convide quem trabalha na implantação.
- **Credenciais só lá.** Chave e senhas nunca vão para e-mail, WhatsApp, chat,
  issue, print ou relatório.
- **Uma chave por clínica** e **um ambiente por clínica** no Claude Code.
- **Pacientes** (LGPD — Lei Geral de Proteção de Dados): nome, CPF e texto de
  prontuário **nunca** entram em prova, relatório ou histórico. A IA usa só o
  número interno. Planilhas de pacientes não ficam no repositório.
- **Senha de banco, nunca.** Para o financeiro basta o nome da conta/caixa.
- **Ao terminar a implantação** (se desejar): peça ao time Rabi para
  **revogar** a chave de implantação ou reduzir às permissões do uso diário.
  Pode também remover a variável `RABI_API_KEY` do ambiente.

Próximo: [Parte G — Checklist para imprimir](05-checklist-imprimir.md).
