# Índice do repositório · <NOME_DA_CLINICA>

> Repo **privado** da implantação do Sistema Rabi. Leia pelo índice; não varra a árvore.

| Caminho | O que tem | Quando ler |
|---|---|---|
| [CLAUDE.md](CLAUDE.md) | boot da sessão de IA | automático |
| [ESTADO.md](ESTADO.md) | painel: modo, sprint, %, próximo passo | toda abertura |
| [PAPEIS.md](PAPEIS.md) | quem é quem e quem aprova o quê | toda abertura |
| [diretrizes-da-equipe.md](diretrizes-da-equipe.md) | direcionamentos da equipe (valem sobre o kit) | toda abertura |
| [README.md](README.md) | explicação para humanos | quando alguém novo chega |
| [sprints/](sprints/00-INDICE.md) | status S00–S17, item a item | na sprint atual |
| [dados/](dados/00-INDICE.md) | dados normalizados por área (com ORIGEM) | ao preparar uma carga |
| [documentos-do-cliente/](documentos-do-cliente/00-INDICE.md) | originais + inventário + fichas de extração | ao receber documento |
| [provas/](provas/00-INDICE.md) | antes/resposta/depois/diff de cada gravação | ao provar e conferir |
| [credenciais/](credenciais/00-LEIA-ME.md) | chave da API, usuários e senhas (texto claro) | ao precisar de acesso |
| [config/](config/00-INDICE.md) | referências próprias da clínica | S06, S08, S10 |
| [decisoes/](decisoes/00-INDICE.md) | decisões de negócio registradas | antes de decidir de novo |
| [pendencias/](pendencias/00-INDICE.md) | lacunas de dados e pendências | toda abertura |
| [historico/](historico/00-INDICE.md) | histórico, aprendizados, dailies, reviews, mensagens verbatim | ao fechar a sessão |
| [ANALISE-CONTRATOS.md](ANALISE-CONTRATOS.md) | análise dos contratos em 6 dimensões | S10 |
| [scripts/](scripts/00-INDICE.md) | hooks de sessão | se algo no início falhar |
| [.github/](.github/00-INDICE.md) | workflow `automerge` (leva a branch `claude/...` da sessão para a `main`) | se a `main` não estiver atualizada |
| `.kit/` | kit de implantação (baixado; só leitura; fora do git) | sempre, pelo índice do kit |

> **Ferramentas só do kit:** `.kit/ferramentas/kit/verificar_tamanhos.py`,
> `verificar_links.py` e `verificar_vazamento.py` são do **mantenedor do kit**.
> **Não rode no repo da clínica** (aqui há credenciais e dados de propósito,
> e o contrato de tamanho/índice é o do kit).
