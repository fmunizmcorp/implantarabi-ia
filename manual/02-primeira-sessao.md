# Parte B — Primeira sessão

> **Fonte:** este kit ([lista única de documentos](../metodologia/lista-unica-de-documentos.md), [ritual de carga](../metodologia/ritual-de-carga.md), [conversa com o usuário](../metodologia/conversa-com-o-usuario.md)) · **Conferido em:** 2026-09-25
> **Vale para:** produção em 25/09/2026 · **Kit:** v0.1.2

Antes: faça toda a [Parte A](01-preparacao.md). Voltar ao [manual](../MANUAL-PASSO-A-PASSO.md).

## B1 — Abrir a sessão e dizer a frase

1. Abra https://claude.ai/code.
2. Escolha o **repositório** `rabi-implantacao-<clínica>`.
3. Escolha o **ambiente** da clínica (o do passo A6, com a chave).
4. Comece uma **nova sessão** (caixa de mensagem vazia).
5. Escreva **exatamente** (com o nome real da clínica) e envie:

```
Vamos implantar Clínica Exemplo
```

Pronto. Não precisa colar nenhum outro texto.

## B2 — O que a IA faz sozinha (sem você pedir)

Nos primeiros minutos você vai ver a IA trabalhando. Ela:

1. **Baixa o kit** (o "livro de receitas") para a pasta `.kit/`.
2. **Personaliza o repositório** com o nome da clínica. Se ela não souber o
   porte, faz **uma** pergunta: "A clínica é um consultório de 1 profissional,
   uma clínica pequena/média ou uma rede com várias unidades?".
3. **Confere** se o repositório é privado e se a chave da API está no
   ambiente (e até quando ela vale). Faltou a chave? Ela explica o passo A6 —
   **não mande a chave no chat**.
4. **Fotografa** o que já existe no seu Rabi (só leitura), para nunca
   sobrescrever nem duplicar um cadastro que a clínica já fez.
5. **Salva** tudo no repositório (commit + push).
6. **Mostra o plano** da clínica (as etapas S00 a S17) e faz a **primeira pergunta**.

## B3 — O pedido único de documentos

A IA manda **uma** mensagem com a lista inteira do que precisa. Você manda o
que tiver, **em qualquer formato** (PDF, foto do papel, print, Excel, Word,
exportação do sistema antigo) e **em qualquer ordem**. Não precisa organizar
nem renomear nada. O que não tiver, tudo bem: ela pergunta depois, uma coisa
por vez.

Resumo do que ela vai pedir (lista completa com códigos:
[lista-unica-de-documentos.md](../metodologia/lista-unica-de-documentos.md);
consultório recebe a versão curta):

| Grupo | Exemplos |
|---|---|
| Da clínica | cartão CNPJ, CNES, endereço de cada unidade, nome das salas, logo |
| Dos convênios | contrato e aditivos, tabela de preços, regra de materiais e medicamentos, planos, quem atende por qual convênio |
| Do particular | a tabela que o paciente paga (inclusive pacotes e descontos) |
| Do que a clínica faz | serviços/procedimentos, taxas, medicamentos e materiais, notas fiscais de compra, equipamentos, o que vai dentro de cada serviço |
| Das pessoas | profissionais (conselho, especialidade), escalas, quem usa o sistema e o que faz, regra de repasse |
| Do dinheiro | contas e caixas (**sem senha de banco**), formas de pagamento e taxas da maquininha, dados de nota fiscal, regra de desconto, margem mínima |
| Do dia a dia | modelos de receita, atestado, termo e orçamento; regras de agendamento; contagem de estoque |
| Do sistema anterior | exportação de pacientes e de cadastros (acelera muito) |

## B4 — Como enviar documentos

**Jeito 1 — anexar na conversa** (o mais simples):
- Clique no ícone de **anexo** (clipe ou "+") na caixa de mensagem, escolha os
  arquivos e envie. Pode mandar vários de uma vez.
- A IA guarda o original em `documentos-do-cliente/` e anota no inventário.

**Jeito 2 — pelo GitHub** (bom para muitos arquivos ou arquivos grandes):
1. Abra o repositório da clínica no GitHub.
2. Entre na pasta `documentos-do-cliente` e clique em **Add file → Upload files**.
3. Arraste os arquivos (ou uma pasta inteira) para a área indicada. Não se
   preocupe com a subpasta: a IA move cada arquivo para
   `documentos-do-cliente/recebidos/<data>/` e anota no inventário.
4. Em baixo, clique em **Commit changes**.
5. Na conversa, escreva: "mandei documentos pelo GitHub". Na sessão seguinte,
   a IA também avisa sozinha que há **documentos novos**.

**Arquivos grandes:** o GitHub pela web aceita até **25 MB por arquivo**. Maior
que isso: divida (ex.: um PDF de contrato em partes, ou uma planilha por ano)
ou mande em partes pela conversa.

## B5 — Como responder

A IA faz **uma pergunta por vez**, em português simples, dizendo o efeito
prático. Responda do jeito mais curto:

| Situação | Responda |
|---|---|
| Ela mostrou um dado e está certo | "sim" ou "correto" |
| Está errado | "corrija para …" (ex.: "corrija para Consultório 2") |
| Ela sugeriu um padrão e serve | "pode usar o padrão" |
| Você não sabe | "não sei — pergunte à Fulana do financeiro" (ela anota como pendência) |
| A clínica não tem | "não temos" (vira pendência ou "não se aplica") |
| Quer parar por hoje | "vamos parar por hoje" (ela salva e diz onde parou) |

## B6 — A prévia, a aprovação e a "foto depois"

Nada é gravado no Rabi sem você ver antes. Para **cada** gravação:

1. **Foto antes** — a IA lê como está hoje no Rabi.
2. **Prévia** — ela mostra uma tabela: item, campo, **de → para**, por quê.
3. **Aprovação** — você lê e responde **"pode gravar"** (ou "corrija …").
   - Em listas grandes, ela grava o **primeiro item**, mostra que saiu certo e
     só então pede para gravar o resto em bloco.
4. **Grava** — ela grava pelo canal oficial (API).
5. **Foto depois** — ela lê de novo e mostra o que mudou. O que não foi relido
   aparece como **NÃO CONFIRMADO**.

Ela nunca faz sem **ordem escrita** sua: emitir ou cancelar nota fiscal, mexer
em dinheiro, mexer em estoque real, inativar/excluir cadastro, gravar em massa
sem prévia.

Próximo: [Parte C — Todos os dias](03-dia-a-dia-e-modos.md).
