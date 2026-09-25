# Agentes e produtividade — gastar contexto só com julgamento

> **Fonte:** guia de escolha de roteiro de sessão (seção de custo) e aprendizados de implantação real (extração paralela, scripts × subagentes) · **Conferido em:** 2026-09-25
> **Vale para:** toda sessão de clínica · **Kit:** v0.1.0

## A regra de ouro

> **O terminal processa, o contexto recebe o resumo.**

O que mais gasta (e mais piora a qualidade da sessão) é despejar dados no
contexto: uma leitura de 200 serviços com todos os campos são dezenas de
milhares de tokens. O que a IA precisa ver é **o resumo e as exceções**.

- **Nunca** `cat` de JSON ou CSV grande. Grave a resposta em arquivo e leia com
  script: contagens, filtros, as 10–20 linhas que importam.
- Leia o kit **pelo índice** (`00-INDICE.md` → arquivo necessário), uma vez.
- Documento grande do cliente: extração por script para arquivo; a conversa
  recebe a ficha resumida e as linhas com dúvida.

## Script quando precisa contar; agente quando precisa entender

| Trabalho | Quem faz | Por quê |
|---|---|---|
| Listar arquivos, hash, páginas, detectar PDF sem texto | script (`ferramentas/ingestao/`) | mecânico; subagente só gastaria contexto |
| Fotos antes/depois, diff, contagens, paginação até o fim | script (`ferramentas/rabi_api/`) | determinístico |
| Prever o valor do serviço e o Farol antes de gravar | script (`ferramentas/conversao/simulador.py`) | as regras são algoritmo |
| Conferir o previsto × o Farol real | script (`ferramentas/conversao/conferir_farol.py`) | comparação linha a linha |
| Painel e fila de perguntas | script (`ferramentas/implantacao/painel.py`, `fila_perguntas.py`) | lê o checklist do repo |
| Ler um contrato e montar a régua contratual | IA (ou subagente extrator) | exige interpretação |
| Classificar A/B/C, propor, explicar ao usuário | IA principal | julgamento e conversa |
| Conferir preços de convênio sem ter escrito | subagente `conferente-precos` | validação cruzada exige contexto limpo |

Os caminhos acima são do kit (no repo da clínica ficam em `.kit/ferramentas/…`).

## Subagentes: quando usar

1. **Extrator de documentos — em paralelo, um por documento.** Implantação com
   muitos documentos (10+ contratos, tabelas longas): dispare um subagente por
   documento. Cada um:
   - lê só o seu documento;
   - grava a ficha de extração em arquivo (ver
     [ingestao-de-documentos.md](ingestao-de-documentos.md));
   - devolve **só** um resumo curto (até ~150 palavras): o que cobriu, o que ficou
     ilegível, contradições encontradas.
   Numa implantação real, dezenas de extrações paralelas rodaram sem saturar o
   contexto principal justamente por esse formato "delega e resume".
2. **Conferente de preços — contexto limpo.** Depois de gravar as abas de um
   convênio, um subagente que **não** participou da gravação recebe: a régua
   contratual, o CSV de preços com ORIGEM e o Farol relido. Ele aponta
   divergências. Quem gravou não valida sozinho.
3. **Auditor de regressão.** Antes de mexer em convênio `FECHADO` ou em modo de
   atualização: roda as 6 contagens e a comparação com a última prova e devolve
   só o que mudou.
4. **Consolidador (fim de sprint grande).** Junta provas, contagens e
   pendências no texto da review.

Regras para qualquer subagente:

- Recebe instruções completas (ele não vê a conversa).
- **Nunca grava no Rabi.** Escrita é sempre da sessão principal, com aprovação.
- Grava o resultado em arquivo e devolve só o resumo.
- Nunca recebe a chave em texto no prompt: usa o mesmo segredo de ambiente.

## Uma sessão por convênio (implantações grandes)

- Clínica com muitos convênios: cada convênio numa sessão própria (modo
  Convênio), curta, que termina com relatório, provas, contagens e commit.
- Cada turno de uma sessão longa reprocessa tudo o que veio antes: sessão curta
  com estado em arquivo é mais barata **e** mais precisa.
- A sessão principal (a "coordenadora" da implantação) mantém a fila de
  convênios no `ESTADO.md` e decide a ordem com o dono da clínica.

## Custo — o que pesa, em ordem

| # | O que gasta | Como cortar |
|---|---|---|
| 1 | Resposta de API despejada no contexto | gravar em arquivo, ler resumo |
| 2 | Documento inteiro colado no chat | ficha de extração + linhas com dúvida |
| 3 | Sessão longa demais | uma sessão por convênio/sprint grande; estado em arquivo |
| 4 | Reler o que já leu | ler o kit uma vez, pelo índice |
| 5 | Subagente para tarefa mecânica | script |

## Rotinas só de leitura fora da IA

Varreduras determinísticas (fotos, contagens de regressão, Farol vermelho e
roxo, conferência preço do sistema × tabela do contrato, validade da chave)
podem rodar por agendamento, sem IA, num servidor controlado pela clínica —
**somente leitura**. Gravação continua sempre na sessão, com aprovação humana.
Isso é opcional e decisão da clínica; se adotado, a chave dessa rotina deve ter
**só permissões de leitura**.

## Contexto enchendo

Pode limpar sem medo **se** o estado estiver nos arquivos: checklist da sprint,
`ESTADO.md` com o próximo passo concreto, provas e decisões commitadas. Ao
compactar, preserve: arquivos modificados, sprint atual, próximo passo e os
comandos de verificação.
