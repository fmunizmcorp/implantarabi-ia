# CLAUDE.md — Implantação do Sistema Rabi · <NOME_DA_CLINICA>

> Carregado automaticamente em toda sessão deste repositório (repo **privado**
> da clínica). O kit de implantação fica em `.kit/` (baixado pelo hook de
> início de sessão; **somente leitura**).

@.kit/BOOTSTRAP.md
@.kit/conhecimento/00-ESSENCIAL.md

## Ao abrir a sessão (sempre, nesta ordem)
1. Confira a saída do hook de início (`scripts/sessao-inicio.sh`): kit baixado?
   versão? repo privado? chave `RABI_API_KEY` definida?
   - Se `.kit/` não existia quando a sessão começou, **leia agora**
     `.kit/BOOTSTRAP.md` e `.kit/conhecimento/00-ESSENCIAL.md` (os imports acima
     só funcionam quando o kit já está baixado).
   - Se o kit não baixou: siga a instrução impressa pelo hook e **não** comece a gravar nada.
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
4. **Commit + push a cada passo concluído** (mensagem em PT-BR, ex.:
   `S05: taxas gravadas (12) + provas`). Nada fica só no container.
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
