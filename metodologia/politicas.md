# Políticas do kit e dos repos de clínica

> **Fonte:** decisões do mantenedor (2026-09-25) + protocolo MAESTRO · **Conferido em:** 2026-09-25
> **Vale para:** kit e todos os repos de clínica · **Kit:** v0.1.0

> Contrato de escrita para **todo autor** (humano, sessão ou agente) do kit e
> dos repos de clínica. A CI (`ferramentas/kit/verificar_*.py`) cobra as
> regras marcadas com ⚙️.

## 1. Tamanho e índices (para a IA conseguir ler)

- ⚙️ **Nenhum `.md` passa de 40 KB.** Se for crescer, quebre em arquivos por
  assunto e crie um índice.
- ⚙️ **Nenhum arquivo de dados passa de 5 MB.** Tabelas grandes são fatiadas
  (`parte-001.csv`, `parte-002.csv`…, ou por letra inicial) com um índice.
- ⚙️ **Toda pasta de conteúdo tem `00-INDICE.md`.** O índice lista cada
  arquivo com 1 linha dizendo *o que tem* e *quando ler*.
- A leitura é **por índice**: abra o índice, depois só o arquivo necessário.
  Nunca varra a árvore inteira nem faça `cat` de JSON/CSV grande. Use
  `grep`, `head` ou as ferramentas Python.
- ⚙️ Links internos são **relativos** e precisam existir.

## 2. Forma de cada documento de conhecimento

Cabeçalho obrigatório (bloco de citação logo abaixo do título):

```
> **Fonte:** <URL do manual com âncora | arquivo de origem> · **Conferido em:** AAAA-MM-DD
> **Vale para:** <produção desde … | em implantação | roadmap> · **Kit:** vX.Y.Z
```

- Português do Brasil, frases curtas, sem jargão não explicado. Sigla
  explicada na primeira vez.
- **Fonte primária prevalece**: o manual oficial
  (`https://www.rabisistemas.com.br/manual/…`) e o Swagger
  (`https://api.rabisistemas.com.br/external-docs/`). O kit **resume e aponta**;
  não duplica páginas inteiras.
- Status honesto: diga **em produção**, **em implantação** ou **roadmap**. Nunca
  ensine como vigente o que não está em produção.
- Nomes de arquivo: minúsculas, sem acento, com hífen (`arvore-servico.md`).

## 3. O kit é público-seguro

**Nunca** entram no kit:
- chave `rbk_`, senha, token, URL com credencial;
- nome, CPF, CNPJ, e-mail ou telefone de pessoa ou clínica real;
- IDs internos, preços ou contratos de uma clínica real.

Exemplos usam dados **fictícios** ("Clínica Exemplo", "Convênio A",
"Dra. Ana Exemplo", CPF de teste). ⚙️ A CI procura padrões de chave e CPF.

As tabelas de referência (`referencias/`) são exceção explícita e documentada
em `referencias/LICENCAS.md`.

## 4. Credenciais — só no repo privado da clínica

- O repo da clínica **tem que ser privado**. A sessão confere isso na abertura
  e avisa por escrito se não for.
- Credenciais ficam em **texto claro** em `credenciais/` (política do
  proprietário), organizadas por serviço e ambiente, com data, onde são usadas
  e como trocar. **Nunca** mascarar, apagar ou trocar por placeholder.
- Chave da API: preferir o segredo de ambiente `RABI_API_KEY` do Claude web.
  O arquivo `credenciais/rabi-api-externa.md` é o registro para consulta
  humana (ver `conhecimento/api-externa/chave-e-token.md`).
- Credenciais **nunca** vão para issue, prova, relatório ou mensagem pública.

## 5. Dado pessoal (LGPD)

- Pacientes, prontuário e histórico de atendimento: **nenhum** nome, CPF ou
  texto clínico em prova, relatório, issue ou log. Só identificadores internos.
- Migração de pacientes: lotes pequenos, conferência por amostra. Não guardar
  extrato no repo. O `.gitignore` da clínica bloqueia `dados/pacientes/`.

## 6. Nada se perde

- Mensagem do cliente/implantador → `historico/requisitos/raw/AAAA-MM-DD-NN-assunto.md`
  (verbatim).
- Decisão → `decisoes/DECISOES.md` (uma linha: data, decisão, quem decidiu, por quê).
- Direcionamento da equipe para a IA → `diretrizes-da-equipe.md`.
- Documento recebido → `documentos-do-cliente/` (original intocado) +
  linha no `inventario.md`.
- Lição → `historico/APRENDIZADOS.md`. Se servir a todas as clínicas, a
  clínica sugere ao mantenedor do kit (issue no repo do kit **sem dado da
  clínica**).

## 7. Papéis (separados)

| Papel | Quem | Pode | Não pode |
|---|---|---|---|
| **Mantenedor do kit** | Rabi / Diretor | alterar o kit | guardar dado de clínica no kit |
| **Dono da clínica** | a clínica | contratar, decidir regra de negócio, ter a conta Claude, o GitHub e a chave `rbk_` | — |
| **Implantador** | alguém da clínica, parceiro ou o próprio Rabi | entregar documentos, aprovar prévias, conferir resultados | delegar decisão de negócio à IA |
| **IA implantadora** | a sessão Claude da clínica | ler o kit; ler e gravar no Rabi pela API **com aprovação**; gravar no repo da clínica; commit+push | alterar o kit; chamar rota proibida sem ordem escrita; inventar dado |

## 8. Git

- A sessão da clínica faz **commit + push** a cada passo concluído, com
  mensagem em PT-BR (`S03: taxas gravadas (12) + provas`).
- O push vai para a **branch da sessão** (`claude/...`: cada sessão do Claude
  Code na web trabalha numa). O workflow `.github/workflows/automerge.yml` do
  repo da clínica leva o trabalho para a `main` em ~1 min; a próxima sessão
  abre na `main`.
- Ao abrir, a sessão confere que o `ESTADO.md` da `main` é o mais recente
  (`git fetch origin main && git log origin/main -1`).
- Nada fica só no container. Se o push falhar, a sessão avisa e tenta de novo;
  o hook de parada bloqueia o encerramento se houver algo sem commit/push.

## 9. Versão

SemVer no `VERSION` do kit. O repo da clínica registra em `ESTADO.md` a versão
do kit que usou em cada sprint.
