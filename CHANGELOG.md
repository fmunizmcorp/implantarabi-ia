# CHANGELOG

## v0.1.1 — 2026-09-25
- Validação cruzada (19 achados) corrigida: PUT de convênio montado da régua (o GET não traz tudo);
  conversor leitura→escrita para serviço/produto (`ferramentas/rabi_api/corpo_escrita.py`);
  `montar_cenario.py` para o simulador; `/parametros/financeiro` misto; Zerar só em pacote fechado;
  caminho único das provas de convênio; Fator K da linha; Farol verde > amarelo; CSV de 21 colunas.
- Simulação de clínica ponta a ponta (10 achados) corrigida: checagem de repo privado pelo campo
  `private`; automerge `claude/** → main` no repo da clínica; kit público (clone sem convite);
  CLIs rodando por caminho de arquivo; `testar_chave` falha claro sem conexão; importador com
  sinônimos de conselho, e-mail e origem com caminho; hook Stop bloqueia encerrar com trabalho
  não enviado; leitura do kit incondicional; passo a passo real da chave (um ambiente por clínica).
- Kit publicado na branch `main`.

## v0.1.0 — 2026-09-25
- Primeira versão do kit: conhecimento (Sistema Rabi, API externa com 268 operações do Swagger de 25/09,
  preços e conversão por convênio, negócio de clínica/TISS, lições), metodologia Scrum, sprints S00–S17
  alinhadas às 16 etapas do guia oficial corrigido em 24/09, prompts de sessão (implantação, atualização,
  convênio, diagnóstico), modelo de repo de clínica, agentes/skills/commands, ferramentas Python
  (cliente da API, motor de conversão com casos T1–T26 do manual, referências, ingestão, painel e fila de
  perguntas, importador de planilhas) e tabelas de referência normalizadas.
