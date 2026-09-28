# CHANGELOG

## v0.3.1 — 2026-09-28
- FAQ F002 resolvida pelo suporte do Rabi (correção de ambiente em 28/09) + seção "Se voltar a acontecer";
  F001 reconferida no código de 28/09 19:28 (continua aberta) + corpo mínimo que funciona; defeito nº 17 resolvido.
- Ação nas clínicas: se a S08 (serviços) parou pelo 400 genérico, confirme `GET /servicos/{id}` = 200 e retome — 1 serviço primeiro com o ritual completo e as 4 listas (FAQ F001); só então o resto.

## v0.3.0 — 2026-09-25
- Canal de aprendizados clínica → kit: fila `contribuicoes-kit/` no repo da clínica,
  `ferramentas/kit/filtrar_aprendizado.py` (filtro de privacidade + link pré-preenchido),
  formulário de issue `aprendizado-clinica`, `coletar_aprendizados.py` + workflow `aprendizados.yml`
  (caixa de entrada + 2ª trava `revisar-privacidade`), área `conhecimento/aprendizados-das-clinicas/`,
  `prompts/08-contribuir-com-o-kit.md` e `prompts/09-consolidar-aprendizados.md`, manual Parte I.
- Novidades kit → clínica: `ferramentas/kit/atualizar_repo_clinica.py` (--novidades/--checar/--aplicar/
  --marcar-visto) e bloco NOVIDADES DO KIT no hook; convenção `Ação nas clínicas:` neste CHANGELOG.
- FAQ das IAs `conhecimento/faq-ias/` (F001 500 `reading 'filter'` em /servicos; F002 400 genérico na área
  inteira — ambiente do Rabi; F003–F005) + `ferramentas/kit/buscar_faq.py`; o erro do `cliente.py` sugere a entrada;
  regra "erro → FAQ primeiro" no ESSENCIAL e no CLAUDE.md do modelo; defeitos 16 e 17.
- Validação cruzada (25 achados) corrigida: filtro de privacidade (CSV com `;`, nomes de PAPEIS/dados e nome
  parcial, IDs camelCase, valores sem R$ e percentuais só com `(exemplo)`, sites sem http, tokens do GitHub; sem
  falso positivo em especialidades/"idade"); atualizador preserva `.gitignore`/`settings.json`/bloco REGRAS-LOCAIS,
  guarda cópia em `historico/estrutura-anterior/`, não ressuscita arquivo apagado e não perde novidades;
  hook avisa quando não consegue verificar; workflow com rebase antes do push; pergunta de envio só no fim.
- Ação nas clínicas: se a API der erro, consulte o FAQ (`buscar_faq.py`) antes de tentar de novo.
- Ação nas clínicas: aplicar a estrutura nova (`atualizar_repo_clinica.py --aplicar`) — traz a fila `contribuicoes-kit/`, as regras NOVIDADES DO KIT e APRENDIZADOS PARA O KIT no CLAUDE.md e o hook novo; depois `--marcar-visto`.

## v0.2.1 — 2026-09-25
- Passo a passo do implantador publicado como página pública no manual oficial do Rabi:
  https://www.rabisistemas.com.br/manual/implantacao/implantacao-com-ia.html (links em README, MANUAL-PASSO-A-PASSO, manual/07, README do modelo e do repo-modelo).

## v0.2.0 — 2026-09-25
- MANUAL-PASSO-A-PASSO.md + manual/ (8 partes): passo a passo detalhado para o implantador leigo.
- Frase de disparo no repo da clínica: "Vamos implantar <clínica>" (primeira vez personaliza; depois retoma
  de onde parou); resumo de retomada no início de cada sessão.
- Repositório-modelo (GitHub Template) `implantarabi-modelo-clinica`: `exportar_modelo.py`,
  `personalizar_clinica.py` e workflow `publicar-modelo.yml` (secret MODELO_PUSH_TOKEN).

## v0.1.2 — 2026-09-25
- Leitura real (só GET) com chave válida incorporada: envelopes padronizados em produção; campos reais
  do Farol (`conta_no_total`, `motivo_exclusao`, `receita_sem_zerar`, `fonte_id`…) — Swagger incompleto;
  GET real de convênio, serviço e produto documentados; `conferir_farol.py` e `montar_cenario.py` usam
  os campos reais; 503 reconfirmado para chave não aceita; validade de chave medida em ~7 dias.

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
