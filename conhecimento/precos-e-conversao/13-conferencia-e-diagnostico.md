# 13 — Conferência depois de gravar e diagnóstico

> **Fonte:** https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#como-conferir · https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#diagnostico · https://www.rabisistemas.com.br/manual/precos/guia-clinica.html#erros-comuns · https://www.rabisistemas.com.br/manual/precos/arvore-de-decisao.html#checklist · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#passo-11 · https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#ler-farol-itens · experiência real (generalizada) · leitura real (GET) da API de produção em 25/09/2026 · **Conferido em:** 2026-09-25
> **Vale para:** produção desde 23–24/09/2026 · **Kit:** v0.1.0

Gravar não é terminar. **Relido = confirmado.** Um convênio só está pronto
quando o que o Rabi calcula bate com o que o contrato manda — conferido pela
API, pela tela e por um orçamento/agendamento de teste.

## 1. Sequência de conferência de um convênio

1. **Releia as abas** (`GET /convenios/{id}/servicos|produtos|taxas`,
   paginando até `total`) e faça o **diff campo a campo** contra o CSV
   aprovado. Depois, uma **segunda leitura fria** (pega o que foi aceito e
   não persistiu).
2. **Farol por serviço:**
   `GET /convenios/{id}/farol/servicos?servicoAtivo=true&ativoNoConvenio=true&pageSize=200`
   - `receita_total` = Σ previsto pelo simulador (I13);
   - `receita_propria_servico` = base prevista (✅, I11);
   - `receita_produtos` + `receita_taxas` (+ `receita_servicos` dos subserviços) explicam a Σ;
   - `custo_total` / `custo_produtos`, `farol` e `margem_resultado_pct` coerentes com custo e régua;
   - `somar_itens` e `zerar_valor` iguais ao que foi gravado.
3. **Farol por item** de cada serviço conferido:
   `GET /convenios/{id}/farol/itens?servicoRaizId=<id>&apenasAtivosNoConvenio=true&servicoAtivo=true&pageSize=200`
   - uma linha por item, com os nomes da **resposta real** (medida em 25/09/2026;
     o Swagger usa outros nomes): `item_tipo, item_id, item_nome,
     servico_pai_id, quantidade, quantidade_efetiva, receita_unitaria,
     receita_item_total, custo_item_total, utiliza_no_convenio, zerar_valor`;
   - **`conta_no_total` + `motivo_exclusao`** (`NAO_UTILIZA_NO_CONVENIO`,
     `ZERADO_EM_PACOTE`, `PAI_FORA_DO_TOTAL`) vêm pela API: conferência
     **primária** de "entra / não entra" — compare com a previsão item a item;
   - cada linha repete os totais do serviço raiz (`receita_total_servico`,
     `custo_total_servico`, `margem_servico_pct`, `farol_servico`): têm de
     bater com o passo 2;
   - `receita_unitaria` diferente do previsto = cadeia de preço errada
     (valor convertido, política, Fator K ou fonte — arquivo 04).
4. **Farol por produto:**
   `GET /convenios/{id}/farol/produtos?ativoNoConvenio=true&produtoAtivo=true&pageSize=200`
   - `receita_sem_zerar` = preço do produto no convênio antes do Zerar (arquivo 04);
     `receita` pode vir 0 com `zerar_valor` (não confirmado — o kit aceita as duas);
   - `origem_receita`, `fonte_nome`/`fonte_id`, `tipo_precificacao`, `fator_k`
     mostram **de onde** saiu o preço: use para achar a causa de um preço errado;
   - `custo` nulo (ou `custo_status` indicando falta) → roxo: falta custo;
     confira de novo após as entradas de estoque;
   - `dbg_*_centavos` estão em **centavos** (divida por 100 antes de comparar).
   - Tudo isso é feito por
     `python3 .kit/ferramentas/conversao/conferir_farol.py cenario.json --servicos s.json --itens i.json --produtos p.json --ignorar-inativos`
     (nomes reais como primários; aceita também os do Swagger).
5. **Tela** (a IA descreve e o usuário confere, ou a IA lê se tiver acesso):
   - aba Serviços › linhas ✅ e Σ; botão **Expandir serviço** (árvore como
     sairá na guia, com farol por item);
   - aba Farol › Serviços › clicar no serviço › **Itens**: coluna **Conta no
     total** Sim/Não só onde deveria.
6. **Relatórios** (Relatórios › Agenda › **Validação de Configuração Por
   Convênio** / **Por Item** — exporta Valor, Política de Preço, Fator K,
   Utiliza, Pacote, Zerar; Relatórios › Cadastro › **Serviços × Convênios —
   Farol de Margem** — Receita Total, Custo Total, Margem %).
7. **Orçamento ou agendamento de teste** (convênio Pago no ato → orçamento;
   senão agendamento) › **Custos**: total e Farol consolidado batem com o
   Farol do convênio. Nenhum orçamento de medicamento pode sair R$ 0,00.
   (Criar orçamento/agendamento é escrita operacional: só com ordem
   escrita e, de preferência, em homologação.)

## 2. Mínimo de 3 serviços por convênio

| Tipo | Exemplo | O que prova |
|---|---|---|
| **simples** | consulta | valor combinado ou da casa, código, nome e tipo de atendimento |
| **com medicamento** | "Medicamento X aplicado EV" (somar ✔) | política/FK do produto, aplicação, ✅ = 0 e Σ = aplicação + remédio |
| **com pacote** | um serviço P ✔ com itens zerados | Σ = preço fechado (+ itens à parte); itens inclusos com receita 0 |

Se o convênio não tem pacote, troque o 3º por um serviço com taxa. Registre
os três em `provas/` com antes/depois e o Farol.

## 3. Os 15 sintomas → causa → correção (guia do implantador)

| # | Sintoma | Causa provável | Correção |
|---|---|---|---|
| 1 | receita do serviço menor que o esperado | Utiliza desmarcado em itens/subserviços; Pacote + Zerar indevidos | marcar Utiliza; rever Pacote/Zerar |
| 2 | serviço de preço fixo "engordou" depois de 23/09/2026 | itens passaram a entrar sempre | se o fixo já os incluía: Pacote no serviço + Zerar nos inclusos |
| 3 | subserviço zerado, mas taxa/material de dentro continua na receita | correto desde 24/09 (Zerar sem cascata) | zerar o próprio item, se incluso |
| 4 | receita em dobro | mesmo valor na raiz e no subserviço (ex.: taxa de aplicação) | manter em um lugar só |
| 5 | preço fechado somando o medicamento | falta Pacote no serviço ou Zerar no medicamento | marcar os dois |
| 6 | "o valor combinado não fechou o preço" | valor combinado não é pacote; sem Pacote o Zerar nem é lido | Pacote + Zerar nos inclusos |
| 7 | linha ✅ do serviço em 0,00 | serviço soma itens sem valor combinado | nada: total está na Σ / Farol |
| 8 | marcar Pacote não mudou nada | serviço soma itens e não tem valor convertido (V5) | correto; para preço fechado, informar o valor |
| 9 | FK da política "não aplicou" no produto | há valor unitário convertido na linha (só recebe o FK da própria linha) | limpar o convertido (`null`) ou pôr FK na linha |
| 10 | produto a R$ 0 | sem fonte resolvida, 0,00 digitado, ou fonte "fixo" sem preço de venda | corrigir fonte/política; limpar 0,00 indevido |
| 11 | R$ 0,01 em serviço | marcador antigo | limpar (vazio), salvo preço simbólico decidido |
| 12 | linha ✅ mostra só o serviço, sem os itens | correto: ✅ = procedimento do XML | total na Σ / Farol › Itens |
| 13 | Farol roxo / Sem custo | produto sem custo (sem compra e sem Última Compra (Unidade)) | informar custo / lançar entrada de estoque |
| 14 | guia não refletiu o novo preço | valores congelados no atendimento | Pré-Faturamento › Atualizar Valores em Massa |
| 15 | tela do convênio e guia com valores diferentes | atendimento anterior à mudança, ou valor editado no pré-faturamento | idem 14; conferir edição manual |

## 4. Os 12 erros comuns (guia da clínica)

| # | Sintoma | Causa | Solução |
|---|---|---|---|
| 1 | item sumiu da conta | Utiliza desmarcado | marcar Utiliza |
| 2 | valor veio o da casa | linha 🔁 em branco | digitar o valor combinado |
| 3 | valor veio zero | 0,00 onde deveria ficar vazio (ou ✅ de serviço que soma itens — normal) | Limpar valor |
| 4 | "digitei 0,00 e veio o cadastro" | comportamento antigo, corrigido em 23/09 | nada; para "sem preço" deixe vazio |
| 5 | pacote somando o medicamento | falta Zerar no medicamento ou Pacote no serviço | marcar os dois |
| 6 | valor combinado e itens continuaram somando | faltou Pacote | Pacote + Zerar nos inclusos |
| 7 | linha ✅ do serviço 0,00 | soma itens sem valor combinado | nada |
| 8 | preço fixo passou a cobrar materiais | itens sempre entram | Receita I |
| 9 | zerei o subserviço e a taxa continua | Zerar por item | zerar a taxa |
| 10 | aplicação cobrada duas vezes | valor no serviço e no subserviço | deixar em um só |
| 11 | Farol roxo | produto sem custo | informar custo |
| 12 | mudei o preço e a guia antiga não mudou | atendimento congela | Atualizar Valores em Massa |

## 5. Sintoma grave: orçamento de medicamento a R$ 0,00

Se um orçamento (ou Σ) de serviço de medicamento sai zero:
1. o serviço tem somar ✔ e V vazio (base 0)? então tudo depende dos itens;
2. algum ancestral é pacote fechado e os itens (inclusive a **aplicação**)
   estão com Zerar? → a aplicação é o pacote, não item: Zerar ✘ nela;
3. o medicamento está com U ✘, sem preço (fonte vazia / política ausente) ou
   com 0,00 gravado?
4. o medicamento está **ausente da composição** ou sem linha no convênio?
Ver armadilha A1 em [14-armadilhas-vividas.md](14-armadilhas-vividas.md).

## 6. Contagens de regressão (antes de mexer num convênio já configurado)

Rode sempre antes de trabalhar num convênio que já tem configuração, e
compare com a última contagem registrada no repo da clínica:

| # | Contagem | Como |
|---|---|---|
| R1 | itens com Utiliza (por aba) | `GET /convenios/{id}/servicos|produtos|taxas` → `utiliza=true` **cruzado com ativo no catálogo** |
| R2 | itens com valor convertido (e quantos com 0 e com 0,01) | `valorInternoConvenio` / `valorUnitarioConversao` / `valorConvertido` não nulos |
| R3 | serviços com Pacote | `pacote=true` |
| R4 | itens com Zerar | `zerarValor=true` por aba |
| R5 | serviços com Farol VERMELHO e ROXO | `/farol/servicos?farol=VERMELHO,…&servicoAtivo=true` |
| R6 | alterações em massa | muitas linhas do **mesmo serviço** alteradas na **mesma hora** em muitos convênios (`updatedAt`) = edição em massa fora das sessões |

Não bateu → **é regressão**: pare, identifique o item pelo id, busque o valor
original **na fonte** (contrato/decisão, não na memória nem em relatório
antigo) e avise antes de gravar qualquer coisa.

> `updatedAt` dos **vínculos** não consta no Swagger (existe no cadastro de
> serviço, `GET /servicos`). Se a resposta real das abas não o trouxer,
> detecte alteração em massa comparando fotos datadas (`provas/`).

## 7. Cuidados de contagem e leitura

- **As listas do Farol e das abas incluem serviços inativos** no catálogo e
  vínculos antigos. Use `servicoAtivo=true`, `apenasAtivosNoConvenio=true`,
  `ativoNoConvenio=true` e cruze com `GET /servicos` (`ativo`). Numa
  implantação real, a contagem pela API deu ~74% a mais que a tela.
- Nunca conclua "N serviços vinculados" sem esse cruzamento.
- **Leitura com status 200 e corpo vazio é leitura falhada**, não "zero
  itens". Confira status **e** tamanho; confira `linhas lidas = total`.
- Antes de gravar em qualquer item, confira **nome e ativo**, não só o id.
- Vermelho não se aceita em silêncio: explique cada um (arquivo 08 §6) e
  apresente a lista com causa na revisão da sprint.

## 8. Checklist de fechamento do convênio

- [ ] régua contratual com cláusula de cada item;
- [ ] política por tipo de produto conferida (tela/relatório);
- [ ] todo item que o convênio cobre com Utiliza; nada de U ✘ sem decisão escrita;
- [ ] nenhum 0,01 marcador; vazio onde não há regra;
- [ ] Pacote só onde há preço fechado — e em **todo** preço fechado;
- [ ] Zerar em cada item incluso (inclusive dentro de subserviços);
- [ ] tipo de atendimento conforme a operadora;
- [ ] I1–I13 sem violação; simulador = Farol lido (Σ e base);
- [ ] 3 serviços conferidos (simples, medicamento, pacote) com provas;
- [ ] lista de vermelhos/roxos com causa apresentada ao implantador;
- [ ] contagens R1–R6 registradas para a próxima regressão.
