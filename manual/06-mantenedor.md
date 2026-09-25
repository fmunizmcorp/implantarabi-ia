# Parte H — Para o mantenedor (Rabi): publicar e atualizar o repositório-modelo

> **Fonte:** este kit ([ferramentas/kit](../ferramentas/kit/00-INDICE.md)) · **Conferido em:** 2026-09-25
> **Vale para:** kit v0.1.2 · **Kit:** v0.1.2

Voltar ao [manual](../MANUAL-PASSO-A-PASSO.md).

O repositório-modelo `fmunizmcorp/implantarabi-modelo-clinica` é a cópia
pública de `modelo-repo-clinica/` (com os marcadores do nome, porte etc. ainda
sem trocar). As clínicas o copiam pelo botão **Use this template**. A troca dos
marcadores é feita na primeira sessão da clínica por
`ferramentas/kit/personalizar_clinica.py`.

## H1 — Primeira vez (à mão, ~3 minutos)

A integração do Claude **não cria repositórios**: este passo é do dono da conta.

1. Abra https://github.com/new com a conta `fmunizmcorp`.
2. **Repository name:** `implantarabi-modelo-clinica`. Marque **Public**.
   Marque **Add a README file**. Clique em **Create repository**.
3. No repositório novo: **Settings → General** → marque **Template repository**
   (logo abaixo do nome do repositório). Salva sozinho.
4. Confira: abra https://github.com/fmunizmcorp/implantarabi-modelo-clinica/generate
   — tem de abrir a tela "Create a new repository" com o modelo escolhido.

## H2 — Enviar o conteúdo (escolha um jeito)

**Jeito A — pela sessão do kit (manual):** numa sessão do Claude Code com
acesso de escrita ao repositório-modelo, peça: "exporte o modelo para o
implantarabi-modelo-clinica". A sessão roda:

```bash
git clone https://github.com/fmunizmcorp/implantarabi-modelo-clinica /tmp/modelo
python3 ferramentas/kit/exportar_modelo.py --destino /tmp/modelo
python3 ferramentas/kit/exportar_modelo.py --checar /tmp/modelo
cd /tmp/modelo && git add -A && git commit -m "modelo: kit $(cat VERSION)" && git push origin HEAD:main
```

**Jeito B — automático pelo workflow** `.github/workflows/publicar-modelo.yml`
(roda a cada push na `main` do kit que mexa no modelo, e também por
*Actions → Publicar repositório-modelo → Run workflow*):

1. GitHub → foto do perfil → **Settings → Developer settings → Personal access
   tokens → Fine-grained tokens → Generate new token**.
2. **Repository access:** *Only select repositories* → `implantarabi-modelo-clinica`.
3. **Permissions → Repository permissions:** **Contents: Read and write** e
   **Workflows: Read and write** (o modelo leva `.github/workflows/automerge.yml`;
   sem "Workflows" o GitHub recusa esse arquivo).
4. Gere e copie o token.
5. No repositório do **kit**: **Settings → Secrets and variables → Actions →
   New repository secret** → nome `MODELO_PUSH_TOKEN`, valor = o token → **Add secret**.
6. Rode o workflow uma vez (*Actions → Publicar repositório-modelo → Run
   workflow*) e confira o verde.

Sem o secret, o workflow só mostra um aviso e termina verde. Quando o token
vencer, o workflow fica vermelho no `git clone`/`push`: gere outro e troque o
secret.

## H3 — Depois de cada mudança no modelo

- Mexeu em `modelo-repo-clinica/` (ou em `exportar_modelo.py`)? Com o secret,
  o workflow publica sozinho. Sem ele, repita o Jeito A.
- Clínicas que **já** criaram o repositório não recebem as mudanças do modelo
  automaticamente (o "Use this template" copia uma vez só). O que muda para
  elas vem pelo kit em `.kit/` a cada sessão; agentes, skills e comandos novos
  são avisados pelo hook e trazidos com
  `python3 .kit/ferramentas/kit/novo_repo_clinica.py --destino . --atualizar-claude`.
- Nunca coloque dado de clínica real no modelo: ele é público.
