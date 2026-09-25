# CLAUDE.md — Implantação do Sistema Rabi · <NOME_DA_CLINICA>

> Carregado automaticamente em toda sessão deste repositório (repo **privado**
> da clínica). O kit de implantação fica em `.kit/` (baixado pelo hook de
> início de sessão; **somente leitura**).

## FRASES DE DISPARO (leia antes de tudo)

O usuário não cola prompt: ele escreve **uma frase**. Reconheça e siga:

| O usuário escreve | Modo | Prompt do modo |
|---|---|---|
| "Vamos implantar <clínica>", "continuar", "continuar implantação" | **Implantação** | `.kit/prompts/02-modo-implantacao.md` |
| "atualizar configuração …" (ex.: reajuste, serviço novo) | **Atualização** | `.kit/prompts/03-modo-atualizacao.md` |
| "convênio …" (ex.: "convênio: configurar Convênio B") | **Convênio** | `.kit/prompts/04-modo-convenio.md` |
| "diagnóstico …" (ex.: "diagnóstico: por que o orçamento saiu zerado?") | **Diagnóstico** (só leitura) | `.kit/prompts/05-modo-diagnostico.md` |

Frase ambígua ou só "oi": faça a abertura (`.kit/prompts/01-abertura-sessao.md`)
e pergunte o modo. **Uma pergunta por mensagem.**

### PRIMEIRA VEZ — o repositório ainda não foi personalizado
Sinal: o resumo do hook diz **"ainda não personalizado — primeira vez"** (a
linha **Clínica:** do `ESTADO.md` ainda mostra o marcador do modelo, entre `<` e `>`).
Faça, nesta ordem, **sem pedir licença para cada passo**:
1. **Personalizar** com o nome que o usuário disse:
   `python3 .kit/ferramentas/kit/personalizar_clinica.py --clinica "Nome Dito" --porte <consultorio|pequena-media|rede>`.
   Se não souber o porte, faça **só esta pergunta** (uma): "A clínica é um
   consultório de 1 profissional, uma clínica pequena/média ou uma rede com
   várias unidades?". Não pergunte mais nada antes de personalizar.
2. **Conferir** que o repo é **privado** (saída do hook) e a chave: `RABI_API_KEY`
   definida? Rode `python3 .kit/ferramentas/rabi_api/testar_chave.py --saida provas/S00/teste-chave-<data>.md`.
   Faltou chave: explique o passo A6 de `.kit/manual/01-preparacao.md` (variável
   no ambiente da clínica). **Nunca peça a chave no chat.** Repo público: aviso
   de repo público (`.kit/prompts/06-mensagens-padrao.md`) e **nenhum push de credencial**.
3. **Foto inicial** do que já existe no Rabi (se houver chave), em
   `provas/S00/foto-inicial/` (só leitura; pacientes só contagem).
4. **Pedido único de documentos** (`.kit/metodologia/lista-unica-de-documentos.md`;
   versão curta ⭐ para consultório).
5. **Commit + push** ("S00: repositório personalizado para a clínica + foto inicial").
6. **Apresente o plano** da clínica (sprints S00–S17 com o tempo do porte) e
   faça **a primeira pergunta** (uma só).

### RETOMADA — o repositório já é da clínica
Leia `ESTADO.md`, a sprint atual (`sprints/Sxx.md`), `pendencias/LACUNAS.md`, a
última daily (`historico/daily/`), os documentos novos que o hook listou e o
histórico recente de `historico/requisitos/raw/`. Responda em **até 8 linhas**:
onde paramos · o que mudou desde a última sessão (documentos novos, respostas,
chave) · **a PRÓXIMA pergunta** (uma só).

### NOME DIVERGENTE
Se o usuário disser "Vamos implantar" com **outra** clínica: não personalize,
não grave nada. Diga que **este repositório é da clínica** registrada no
`ESTADO.md`, que cada clínica tem o seu repositório (criado pelo modelo:
`.kit/manual/01-preparacao.md`, passo A3) e pergunte se ele abriu o repositório
errado. (O `personalizar_clinica.py` recusa com código 3.)

## PRIMEIRA AÇÃO de toda sessão (sem exceção)
Ler **`.kit/BOOTSTRAP.md`** e **`.kit/conhecimento/00-ESSENCIAL.md`** com a
ferramenta de leitura, antes de responder qualquer coisa. O hook de início já
baixou o kit; **se `.kit/` não existir, rode `bash scripts/sessao-inicio.sh`**
e leia os dois arquivos em seguida. (Os imports abaixo são só um bônus: numa
sessão nova na web o `.kit/` ainda não existe quando este arquivo é lido.)

@.kit/BOOTSTRAP.md
@.kit/conhecimento/00-ESSENCIAL.md

## Ao abrir a sessão (sempre, nesta ordem)
1. Confira a saída do hook de início (`scripts/sessao-inicio.sh`): kit baixado?
   versão? repo privado? chave `RABI_API_KEY` definida? último commit da `main`?
   - Se o kit não baixou: siga a instrução impressa pelo hook e **não** comece a gravar nada.
   - Confira que está trabalhando sobre o `ESTADO.md` mais recente:
     `git fetch origin main && git log origin/main -1 -- ESTADO.md`. Se a
     `main` estiver atrás de uma branch `claude/...` antiga, avise antes de seguir.
2. Leia `ESTADO.md`, `PAPEIS.md`, `diretrizes-da-equipe.md` e a sprint atual
   (`sprints/Sxx.md` aqui + o playbook `.kit/sprints/Sxx-<nome>.md`).
3. Aplique as **FRASES DE DISPARO** acima (primeira vez × retomada × nome
   divergente). Se a frase não indicar o modo, apresente-se usando
   `.kit/prompts/01-abertura-sessao.md` e pergunte o modo. Prompts de cada
   modo: `.kit/prompts/02` a `05`.

## Regras de ouro
1. **Uma pergunta por vez**, em português simples, dizendo o efeito prático.
2. **Ritual de 5 passos** em toda gravação no Rabi: foto antes → prévia →
   aprovação → grava → foto depois + diff (skill `ritual-de-carga`).
   O que não foi relido é **NÃO CONFIRMADO**.
3. **Convênio com atenção redobrada:** um convênio por vez, CSV com ORIGEM,
   previsão com `.kit/ferramentas/conversao/simulador.py`, conferência com
   `.kit/ferramentas/conversao/conferir_farol.py` e agente `conferente-precos`
   (skill `configurar-convenio`).
4. **Commit + push a cada passo concluído**, na branch da sessão
   (`claude/...`), mensagem em PT-BR (ex.: `S05: taxas gravadas (12) + provas`).
   O workflow `.github/workflows/automerge.yml` leva o trabalho para a `main`
   em ~1 min (é a `main` que a próxima sessão abre). Nada fica só no container:
   o hook de parada bloqueia o encerramento se houver algo sem commit/push.
5. **O kit é só leitura.** Nunca edite `.kit/`. Lição útil para todas as
   clínicas → sugestão ao mantenedor do kit, **sem dado da clínica**.
6. **Este repo tem de ser PRIVADO** (guarda chave e senhas em texto claro). Se
   o hook avisar que está público: avise por escrito (modelo em
   `.kit/prompts/06-mensagens-padrao.md`) e **não faça push** até o dono decidir.
   Não apague nem mascare credencial.
7. **Nada por dedução.** Valor sem documento vira linha em `pendencias/LACUNAS.md`.
8. **Nada se perde:** mensagem do cliente → `historico/requisitos/raw/`;
   decisão → `decisoes/DECISOES.md`; direcionamento → `diretrizes-da-equipe.md`;
   documento → `documentos-do-cliente/` + `inventario.md`.
9. **LGPD:** nenhum nome/CPF/prontuário de paciente em prova, relatório, issue ou log.
10. **Rotas proibidas sem ordem escrita** (NFS-e, dinheiro, estoque real,
    `DELETE`, `/bulk` sem prévia): ver `.kit/conhecimento/api-externa/`.

## Se o kit e a clínica divergirem
Vale `diretrizes-da-equipe.md` desta clínica; registre a divergência em
`decisoes/DECISOES.md`.

## Ao compactar contexto
Preserve: arquivos modificados, sprint atual, próximo passo de `ESTADO.md`,
último caminho de prova e o que está aguardando aprovação.

## Referência do manual em cada etapa
Em cada sprint, prévia e pergunta, termine com **"📖 Para saber mais: <link>"** — o link da etapa no manual oficial (seção "Link do manual" de `.kit/sprints/Sxx-*.md`; tabela completa em `.kit/manual/07-onde-ler-mais-no-manual.md`). O painel do `ESTADO.md` também mostra esse link por sprint.
