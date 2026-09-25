# Implantação do Sistema Rabi — <NOME_DA_CLINICA>

Este repositório **privado** guarda tudo da implantação do Sistema Rabi nesta
clínica: o painel de progresso, os documentos recebidos, os dados extraídos,
as provas de cada gravação, as decisões e as credenciais.

Quem trabalha nele é uma **sessão de IA (Claude)** conduzida pelo kit
`implantarabi-ia`, que é baixado automaticamente para a pasta `.kit/` no início
de cada sessão.

## O que você (pessoa) faz — só três coisas
1. **Entrega os documentos** que a IA pedir (em qualquer formato).
2. **Aprova** o que a IA mostra antes de gravar ("pode gravar").
3. **Confere** o resultado que a IA mostra depois.

Todo o resto (ler, extrair, montar, gravar, provar, registrar) é da IA.

## Como abrir uma sessão
1. Abra o Claude (web) neste repositório.
2. Confira que o segredo `RABI_API_KEY` está configurado no ambiente.
3. Cole o prompt de abertura (ver `.kit/prompts/00-COMO-COMECAR.md`) ou apenas
   diga "vamos continuar" — a sessão lê o `ESTADO.md` e diz onde parou.

## Onde fica o trabalho
Cada sessão trabalha numa branch `claude/...` e faz commit + push a cada passo.
O workflow `automerge` (em `.github/workflows/`) leva tudo para a `main` em
cerca de 1 minuto — é a `main` que a próxima sessão abre.

## Onde olhar
- **Onde estamos:** [ESTADO.md](ESTADO.md)
- **Quem é quem:** [PAPEIS.md](PAPEIS.md)
- **Tudo:** [INDICE.md](INDICE.md)

⚠️ **Este repositório tem de continuar privado**: ele guarda chave de API e
senhas em texto claro, por decisão do dono.
