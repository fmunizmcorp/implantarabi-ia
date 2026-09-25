# CLAUDE.md — Kit de Implantação do Sistema Rabi via IA

> Carregado automaticamente em toda sessão aberta **neste repositório** (o kit).
> Sessões de **clínica** não abrem este repo diretamente: elas usam o
> `CLAUDE.md` do repo da clínica, que traz o kit para `.kit/` e importa
> os mesmos arquivos abaixo.

@BOOTSTRAP.md
@conhecimento/00-ESSENCIAL.md

## Quem está nesta sessão

Este repo é o **kit** (a "escola"). Ele **não guarda dado de nenhuma clínica**
e **nenhuma credencial**. Dados, provas e chaves vivem no repo **privado** de
cada clínica, criado a partir de `modelo-repo-clinica/`.

| Se você é… | Então… |
|---|---|
| **Sessão do mantenedor** (Rabi/Diretor evoluindo o kit) | Pode alterar o kit. Siga `metodologia/politicas.md` e registre em `CHANGELOG.md` + `historico/HISTORICO.md`. |
| **Sessão de clínica** que leu o kit por engano aqui | **Não altere nada.** Vá para o repo da clínica. Se ele não existe: `prompts/00-COMO-COMECAR.md`. |

## Mapa rápido (leia sob demanda, pelo índice)

- `INDICE.md` — índice-mestre de tudo
- `conhecimento/` — Sistema Rabi, API externa, **preços e conversão** (o coração), negócio de clínica, lições
- `metodologia/` — Scrum da implantação, ritual de carga, conversa com o usuário, ingestão de documentos, modos, políticas
- `sprints/` — S00 a S17 (S01–S16 = etapas 1–16 do guia oficial)
- `prompts/` — abertura de sessão (implantação / atualização / convênio / diagnóstico) e mensagens-padrão
- `ferramentas/` — Python: cliente da API, **motor de conversão de valores**, referências, ingestão, kit
- `referencias/` — tabelas-base (TUSS, CMED, Brasíndice, SIMPRO, CBHPM, domínios ANS)
- `modelo-repo-clinica/` — o que é copiado para cada clínica

## Ao compactar contexto
Preserve SEMPRE: arquivos modificados, comandos de verificação
(`python3 -m pytest ferramentas -q`, `python3 ferramentas/kit/verificar_tamanhos.py`,
`python3 ferramentas/kit/verificar_links.py`) e o próximo passo registrado em
`historico/HISTORICO.md`.
