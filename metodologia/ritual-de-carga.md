# Ritual de carga — os 5 passos de toda gravação no Rabi

> **Fonte:** plano de implantação em sprints (seção "O ritual de toda carga", experiência prática) + https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#checklist-final · **Conferido em:** 2026-09-25
> **Vale para:** toda escrita pela API externa, em qualquer modo de sessão · **Kit:** v0.1.0

## A regra

**Nenhuma gravação acontece fora deste ritual.** Nem "um campinho só", nem
"é só corrigir o nome". O ritual existe porque, numa implantação real,
gravações "óbvias" apagaram campos, caíram em itens inativos e foram dadas como
feitas sem terem persistido.

```
1 FOTO ANTES → 2 PRÉVIA (tabela, sem JSON) → 3 APROVAÇÃO → 4 GRAVA (guarda a resposta crua) → 5 FOTO DEPOIS + DIFF
```

Onde fica a prova, no repo da clínica:
`provas/Sxx/<cadastro>/<data>/antes.json`, `resposta.json`, `depois.json`, `diff.txt`
(a pasta com a data permite repetir a carga do mesmo cadastro sem apagar a prova anterior).
Prova **nunca** contém dado de paciente (ver [politicas.md](politicas.md) §5).

## Passo 1 — Foto antes

- Leia o estado atual pela API (GET) e salve o JSON bruto em `antes.json`.
- **A leitura só vale se:** o status for 200 **e** o corpo tiver bytes **e**
  `linhas lidas = total` (percorra até `page = totalPages`; não pare quando uma
  página vier menor). Leitura que falhou não permite conclusão nenhuma.
- Em cadastro novo, a foto antes é a **busca** que prova que o item ainda não
  existe (ex.: `GET /produtos?nome=...`, `GET /empresas` e procurar o CNPJ).
- Antes de mexer em item existente, confira duas coisas e escreva-as na prévia:
  1. **Ativo ou inativo?** Item inativo não se toca sem decisão escrita.
  2. **O nome do item, não só o ID.** "Gravei em Aplicação endovenosa (46)"
     vale. "Gravei no 46" não vale.

## Passo 2 — Prévia ao humano

- Uma **tabela legível**, nunca JSON. Colunas típicas:
  `item | campo | hoje | vai ficar | por quê (origem)`.
- Nome por extenso primeiro, ID depois e entre parênteses.
- Toda linha tem a **origem**: documento + página/linha, ou "padrão sugerido
  pela IA e aceito em <data>", ou "decisão de <pessoa> em <data>".
- Valor sem origem **não entra na prévia**: vira pendência.
- Diga o efeito prático quando houver ("a partir daqui, o particular passa a
  cobrar R$ 150,00 pela consulta").
- Se a prévia for grande, mostre um resumo (quantos novos, quantos mudam,
  quantos iguais) e os 5–10 primeiros; o resto fica em arquivo no repo.

## Passo 3 — Aprovação

- **Item a item no que é novo.** A primeira taxa, o primeiro produto, o
  primeiro serviço composto, o primeiro convênio: um por vez.
- **Em bloco só depois que o primeiro item do bloco saiu provado** (passo 5
  feito e conferido). Ex.: grave 1 produto, prove, e só então peça aprovação
  para os outros 49 do lote.
- A aprovação é explícita ("pode gravar", "sim, grava"). Silêncio, "acho que
  sim" ou "depois vejo" **não** são aprovação.
- A aprovação é registrada: linha em `decisoes/DECISOES.md` quando envolve regra
  de negócio; mensagem verbatim em `historico/requisitos/raw/`.

## Passo 4 — Grava

- Chame a rota e guarde a **resposta crua com o status** em `resposta.json`.
- **PUT = sobrescrita.** Antes de todo PUT: GET do objeto completo → altere só o
  que foi aprovado → reenvie **o objeto inteiro**. Exceções (upsert, campo
  omitido mantém, `null` limpa, `0` é zero): as abas
  `PUT /convenios/{id}/servicos|taxas|produtos|colaboradores|especialidades|planos`
  e `/parametros/desconto`. Mesmo em `/parametros/financeiro`, reenvie tudo:
  omitir conta ou centro de custo já gravou `null` na prática.
- **Lotes:** até 50 nos `/bulk` de cadastro; 200 nas abas do convênio (100 na
  aba Colaboradores) e em `/tabelas-preco/produtos/bulk`; 100 em
  `/nfse/tomadores/bulk`. **Um lote por vez** por clínica (o segundo simultâneo
  recebe 429). O lote pode ser interrompido em ~45 segundos: prefira lotes
  menores se a resposta demorar.
- **207 = falha parcial.** Leia `resultados[]` pelo `indice` (começa em 0) e
  reenvie **só** os itens com `ERRO` ou `NAO_PROCESSADO`. Liste para o usuário
  o que não entrou e por quê.
- **409** = já existe: busque pelo GET, reutilize o ID, **não crie outro**.
- **422** = falta pré-requisito (ordem das sprints!). **400** = campo inválido
  (leia `issues[]`). **403** = a chave não tem essa permissão: pare e avise.
- **401 ou 503** = problema com a chave (a documentação diz 401; na prática, chave
  revogada já respondeu 503). **Não entre em laço de nova tentativa.** Tente uma
  vez depois de alguns segundos; se repetir, pare, registre e avise o
  implantador (a chave pode ter vencido — veja `X-ApiKey-Expires-At`).
- **500 depois de gravar:** a rota `POST|PUT|DELETE /grades-equipamento` tem um
  defeito documentado — grava certo e devolve 500. Não repita: vá direto ao
  passo 5 e confira pela leitura.

## Passo 5 — Foto depois + diff

- Releia **pela API** o que foi gravado (GET do item, e da aba inteira quando
  for convênio). Salve em `depois.json`.
- Gere o `diff.txt` campo a campo (antes × depois) e mostre ao usuário **só o
  que mudou**, em tabela.
- Confira: mudou exatamente o que foi aprovado? Algum campo que **não** estava na
  prévia mudou (sinal de PUT parcial ou nome de campo errado)?
- Em convênios, faça também uma **segunda leitura fria** alguns minutos depois
  (pega a gravação que o sistema aceitou e não persistiu) e releia o Farol.
- **Se a releitura falhou**, o estado é **NÃO CONFIRMADO** — e é isso que se
  escreve no checklist, no ESTADO e para o usuário. Nunca "provavelmente gravou".

## Depois do passo 5

1. Atualize o item no checklist da sprint (`gravado` → `conferido`), com o
   caminho da prova.
2. Atualize `ESTADO.md` (painel e próximo passo concreto).
3. Commit + push com mensagem em português (`S05: taxa "Taxa de sala" gravada + prova`).
4. Mostre a evolução ao usuário (barra da sprint — ver
   [conversa-com-o-usuario.md](conversa-com-o-usuario.md)).

## Chamadas que nunca entram no ritual sem **ordem escrita**

Elas têm efeito que não se desfaz ou que atinge dinheiro, fisco ou estoque real.
Precisam de uma ordem escrita do dono da clínica (registrada em
`decisoes/DECISOES.md`), além do ritual:

| Tipo | Rotas |
|---|---|
| Nota fiscal | `POST /nfse/notas/{id}/emitir`, `/emitir-contingencia`, `/transmitir-contingencia`, `/cancelar`, `/substituir` |
| Dinheiro (pode emitir NFS-e automática) | `POST /financeiro/movimentacoes` e `/bulk`, `PUT /financeiro/movimentacoes/{id}`, `POST /orcamentos` com pagamento no ato |
| Estoque real | `POST /estoque/entrada`, `/saida`, `/transferencia` |
| Inativação | qualquer `DELETE` |
| Massa | `/bulk` antes do primeiro item provado; várias abas de convênio de uma vez |
| Dado clínico | `POST /atendimentos`, `/atendimentos/prontuario`, `/atendimentos/novo-prontuario` |

A lista completa e atualizada fica em `conhecimento/api-externa/` do kit
(arquivo de rotas proibidas sem ordem escrita).

## Resumo em 7 linhas (para colar no início de uma sessão)

1. Foto antes (status 200 + bytes + total lido).
2. Ativo/inativo e nome antes de mexer.
3. Prévia em tabela, com origem de cada valor.
4. Aprovação item a item no novo; em bloco só depois do primeiro provado.
5. PUT = objeto completo (salvo abas do convênio e desconto).
6. Grava, guarda resposta crua; 207 → reenvia só os com erro.
7. Foto depois + diff; sem releitura = NÃO CONFIRMADO.
