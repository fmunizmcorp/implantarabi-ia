# CLAUDE.md — Implantação do Sistema Rabi · <NOME_DA_CLINICA>

> Carregado automaticamente em toda sessão deste repositório (repo **privado**
> da clínica). O kit de implantação fica em `.kit/` (baixado pelo hook de
> início de sessão; **somente leitura**).

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
3. Apresente-se usando `.kit/prompts/01-abertura-sessao.md`: quem você é, o
   painel, o próximo passo e **qual modo** (Implantação · Atualização ·
   Convênio · Diagnóstico). Prompts de cada modo: `.kit/prompts/02` a `05`.

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
