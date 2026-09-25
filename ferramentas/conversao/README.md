# Motor de conversão de valores (preços por convênio)

> **Fonte:** https://www.rabisistemas.com.br/manual/precos/guia-ia.html#algoritmo · https://www.rabisistemas.com.br/manual/precos/arvore-de-decisao.html#arvores · https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#tabela-verdade · spec `conhecimento/api-externa/spec/openapi-2026-09-25.json` · **Conferido em:** 2026-09-25
> **Vale para:** produção desde 23–24/09/2026 (regras de preço), 24/09 (4 linhas), 25/09 (valor combinado não é pacote) · **Kit:** v0.1.0

Ferramentas em Python 3.11, só biblioteca padrão, para **montar**, **prever** e
**conferir** a configuração de preços de um convênio no Sistema Rabi.

Elas **não gravam nada**. Quem grava é o cliente da API
(`ferramentas/rabi_api/cliente.py`), sempre depois da aprovação humana.

**Como rodar:** da raiz do repo, pelo caminho do arquivo. No repo da clínica:
`python3 .kit/ferramentas/conversao/<x>.py …` (como nos exemplos abaixo). No
próprio kit (mantenedor), tire o `.kit/`.

O motor é uma **previsão**. Quem manda é o Rabi. Toda gravação termina com
`conferir_farol.py`, que compara a previsão com o que o Rabi devolve.

## Módulos

| Arquivo | O que faz |
|---|---|
| `modelo.py` | Dados: `Servico`, `Produto`, `Taxa`, `Vinculo`, `ConfigItem` (item no convênio, nível 3), `PoliticaTipoProduto` (nível 2), `Convenio`, `Catalogo`. Lê o cenário JSON. `None` = vazio; `0.0` = zero. |
| `motor.py` | As árvores do manual: valor do produto (2.1), da taxa (2.2), base do serviço (2.3), serviço composto recursivo (2.4), orçamento (2.5), Farol e Farol consolidado (2.6/2.7), tipo de atendimento (2.8), textos (2.9), Farol › Itens (2.10), 4 linhas (2.11), ciclos e invariantes I1–I13. |
| `montar_cenario.py` | CLI. Monta o `cenario.json` do simulador a partir das fotos da API + políticas da régua, e lista as **lacunas** (o que a API não devolve). |
| `simulador.py` | CLI. Imprime, por serviço: 🔒 casa · 🔁 combinado · ✅ próprio · Σ total, custo, Farol (% e cor) e a árvore de itens com "conta" ou "FORA (motivo)". |
| `montar_convenio.py` | CLI. Lê `precos-<slug>.csv`, valida e gera os corpos dos `PUT /convenios/{id}/produtos, /taxas, /servicos` (lotes de até 200), o `manifesto.json` e a `previa.md` (de → para). |
| `conferir_farol.py` | CLI. Compara a previsão com os GET de `/convenios/{id}/farol/servicos, /itens, /produtos` e lista as divergências. |
| `tests/` | T1–T26 do manual, exemplos numéricos, invariantes, ciclos, CLIs e campos × spec. |
| `exemplos/` | Cenário fictício "Convênio A" em JSON e CSV, fotos de GET simuladas. |

## Como a sessão de IA usa (modo Convênio)

1. **Monte o CSV** `precos-<slug>.csv` a partir do contrato. Toda linha tem
   **origem** (contrato, anexo, e-mail). Linha sem origem é rejeitada.
2. **Foto antes:** leia o catálogo e o convênio com o cliente
   (`ClienteRabi.ler_tudo("/convenios/12/servicos")` etc.), salve cada leitura em JSON e
   monte o cenário com `montar_cenario.py` (seção abaixo). Monte também o `atual.json`
   (`{"servicos": …, "produtos": …, "taxas": …}`) para a prévia de → para.
3. **Simule:**
   `python3 .kit/ferramentas/conversao/simulador.py cenario.json --csv precos-convenio-a.csv --invariantes`.
   Mostre ao usuário o Σ de 3 serviços (um simples, um com medicamento, um pacote).
   Nunca mostre JSON ao usuário.
4. **Prévia:**
   `python3 .kit/ferramentas/conversao/montar_convenio.py precos-convenio-a.csv --convenio-id 12 --saida saida/ --catalogo cenario.json --atual atual.json`.
   Mostre a `previa.md` (item · campo · de → para · porquê). Com erro, nenhum lote é gerado (código 2).
5. **Aprovação** do implantador.
6. **Grave** na ordem do `manifesto.json` (fases: Utiliza → valores → textos → tipo de
   atendimento → Pacote/Zerar), um lote por vez:
   `cliente.enviar_lote(ch["caminho"], ch["aba"], corpo[ch["aba"]], tamanho=200, metodo="PUT")`.
   Em 207, reenvie só os itens `reenviar`.
7. **Foto depois + conferência:** leia `/farol/servicos`, `/farol/itens` e `/farol/produtos`
   (todas as páginas) e rode
   `python3 .kit/ferramentas/conversao/conferir_farol.py cenario.json --csv precos-convenio-a.csv --servicos s.json --itens i.json --produtos p.json --ignorar-inativos --saida provas/.../conferencia.md`.
   Divergência = investigar antes de dizer "pronto" (código de saída 1).

Estudo das regras: [casos de teste](../../conhecimento/precos-e-conversao/12-casos-de-teste.md) ·
[árvore do serviço](../../conhecimento/precos-e-conversao/03-arvore-servico.md).

## O CSV `precos-<slug>.csv`

Separador `;` (ou `,`), UTF-8. As 21 colunas (`montar_convenio.COLUNAS`):
`tipo; id_rabi; nome_rabi; nome_convenio; descricao_convenio; codigo; tipo_codigo_id; tabela87_id; tipo_atendimento_id; utiliza; valor_combinado; pacote; zerar; autorizacao_previa; retorno; fator_k; fonte_preco; tipo_precificacao; parcelas; origem; observacao`.
Obrigatórias: `tipo`, `id_rabi`, `origem`.

| Célula | Vazia significa | Observação |
|---|---|---|
| `valor_combinado`, `fator_k` | **sem regra** → envia `null` (a API **limpa** o campo) | `=` ou `manter` = não envia (mantém). `0` / `0,00` = zero de verdade. Aceita `1.234,56`. **`0,01` = ERRO.** |
| `utiliza`, `pacote`, `zerar`, `autorizacao_previa`, `retorno` | não envia (mantém) | `sim`/`não` (ou s/n, 1/0, x) |
| textos e ids | não envia (mantém) | `limpar` em `tipo_atendimento_id` envia `null` |
| `fonte_preco` | não envia | número da opção; nome só com `--fontes fontes.json` (`{"nome": id}`) |
| `tipo_precificacao` | não envia | `PRECO_1`, `1` ou `Preço 1` |

### Mapa coluna → campo da API (conferido no spec)

| Coluna | Serviço (`ConvenioServicoItem`) | Produto (`ConvenioProdutoItem`) | Taxa (`ConvenioTaxaItem`) |
|---|---|---|---|
| id_rabi | servicoId | produtoId | taxaId |
| utiliza · zerar | utiliza · zerarValor | utiliza · zerarValor | utiliza · zerarValor |
| valor_combinado | valorInternoConvenio | valorUnitarioConversao | valorConvertido |
| nome_convenio | nomeConversao | nomeConversao | nomeConvertido |
| descricao_convenio | descricaoConvenio | descricaoConversao | descricaoConvertida |
| codigo | codigo | codigoConversao | codigo |
| tipo_codigo_id · tabela87_id | tipoCodigoId · tabela87ANSId | idem | idem |
| pacote | pacote | — (erro) | — (erro) |
| tipo_atendimento_id | tipoAtendimentoId | — | — |
| autorizacao_previa · retorno | autorizacaoPrevia · retornoServico | — | — |
| parcelas | parcelasMaximas | parcelasMaximas | — |
| fator_k · fonte_preco · tipo_precificacao | — | fatorK (texto "10,5") · fontePrecoCompraOptionsId · tipoPrecificacao | — |

Coluna que não existe na aba do item = **ERRO** (ex.: `pacote` em produto, `fator_k` em taxa).

### Validações antes de gerar

- **ERRO** (bloqueia): origem vazia, tipo/id inválido, item repetido, `0,01`, valor negativo,
  Fator K fora de −100…2000, coluna inexistente na aba, fonte sem id, ciclo de subserviços.
- **AVISO** (mostrar ao humano): valor combinado sem Pacote em serviço com composição
  ("valor combinado não é pacote"), Zerar sem pacote fechado acima, Utiliza = não com valor,
  I1, I2, I3, I5, I7, I8, I9, I10, I12 (com `--catalogo`), `nome_rabi` diferente do catálogo.

## Montar o cenário a partir da API (`montar_cenario.py`)

```bash
python3 .kit/ferramentas/conversao/montar_cenario.py --convenio-id 12 --nome "Convênio A" \
  --servicos fotos/servicos.json --produtos fotos/produtos.json --taxas fotos/taxas.json \
  --conv-servicos fotos/conv-servicos.json --conv-produtos fotos/conv-produtos.json \
  --conv-taxas fotos/conv-taxas.json --politicas dados/convenios/convenio-a/politicas.json \
  [--farol-produtos …] [--ultima-compra …] [--tabelas-preco …] [--precificacao …] \
  [--parametros …] [--composicao …] [--complemento-produtos …] \
  --saida dados/convenios/convenio-a/cenario.json
python3 .kit/ferramentas/conversao/simulador.py dados/convenios/convenio-a/cenario.json \
  --csv dados/convenios/convenio-a/precos-convenio-a.csv --invariantes
```

| Campo do cenário | Rota de origem (ou arquivo do repo) |
|---|---|
| `catalogo.servicos[]`: `nome`, `valor_cadastro`, `somar_itens`, `ativo`, `codigo_tuss`, `tipo_atendimento` | `GET /servicos/{id}` (`valor`, `somarItens`, `codigoTUSS`, `tipoAtendimentoId`, `tipoCodigoId`, `tabelaANS87ID`) |
| `catalogo.servicos[].itens` | `--composicao` (árvore da S08: dicionário de IDs / foto da prova da criação). O `GET /servicos/{id}` **real** (25/09) **não traz** a composição nem as especialidades; se algum dia trouxer (`produtos`/`ServicoProduto`, `servicosRelacionados`, `taxaServico`, `equipamentos`), é usada |
| `catalogo.produtos[]`: `nome`, `tipo_produto`, `codigo` | `GET /produtos` (`TipoProduto.nome`, `codigoProduto`) |
| `catalogo.produtos[].custo` | `--complemento-produtos` ou `GET /convenios/{id}/farol/produtos` (`custo`) |
| `catalogo.produtos[].fonte_preco`, `tipo_precificacao`, `fator_k` | `--complemento-produtos` (cadastro, aba Estoque); na falta, `GET /convenios/{id}/farol/produtos` (`fonte_nome`/`fonte_id`, `tipo_precificacao`, `fator_k`) — **valor efetivo neste convênio** (pode vir da política ou da linha): vira lacuna avisando que a linha 🔒 e outros convênios podem divergir |
| `catalogo.produtos[].preco_venda_tabela` | `--complemento-produtos`; na falta, `/farol/produtos` `dbg_preco_venda_tabela_centavos` ÷ 100 |
| `catalogo.produtos[].ultima_pesquisa`, `preco_medio` | **só** `--complemento-produtos` (aba Estoque) |
| `catalogo.produtos[].ultima_compra` | `GET /estoque/ultima-compra/{id}` (`ultimaCompraUnitaria`; `0` = sem dado); na falta, `/farol/produtos` `dbg_ultima_compra_reais` |
| conferência do preço do produto | `/farol/produtos` `receita_sem_zerar` (ou `receita` se não zerado): previsão ≠ Rabi vira lacuna |
| `catalogo.produtos[].precos_tabela` | `GET /tabelas-preco/produtos?id=<tabela>` (`tabelaPrecoInterna.precificacao1..3`) |
| `catalogo.taxas[]` | `GET /taxas` (`taxas` = nome, `codigoTaxa`, `valor`) |
| `convenio.servicos[]` | `GET /convenios/{id}/servicos` (`valorInternoConvenio`, `pacote`, `zerarValor`, `nomeConversao`, `tipoAtendimentoId`…) |
| `convenio.produtos[]` | `GET /convenios/{id}/produtos` (`valorUnitarioConversao`, `fatorK`, `fontePrecoCompraOptionsId` → nome por `GET /tabelas-preco/precificacao` — id **não confirmado**) |
| `convenio.taxas[]` | `GET /convenios/{id}/taxas` (`valorConvertido`, `zerarValor`, `nomeConvertido`) |
| `convenio.politicas[]` | **régua contratual** (`--politicas`): a API **não** devolve `politicasPorTipoProduto` |
| `convenio.parametro_vermelho/amarelo` | `GET /parametros/orcamento` (`parametroVermelho`, `parametroAmarelo`); sem ele, 100/120 |

Tudo que falta vira uma linha em `_lacunas` (no JSON e na tela). **Previsão com lacuna
aberta não é prova**: resolva ou diga ao usuário qual número pode estar errado.

## Formato do cenário JSON

`{"catalogo": {"produtos": [...], "taxas": [...], "servicos": [...]}, "convenio": {...}}` —
ver `exemplos/cenario-convenio-a.json`. No catálogo, serviço tem `itens`
(`{"tipo": "produto" (ou taxa, subservico, equipamento), "id", "quantidade"}`) e `somar_itens`;
produto tem `custo`, `preco_venda_tabela`, `fonte_preco`, `tipo_precificacao`,
`fator_k`, `ultima_compra`, `ultima_pesquisa`, `preco_medio`, `precos_tabela`
(`{"Nome da tabela": {"PRECO_1": 50}}`). No convênio: `politicas` (nível 2) e
`servicos`/`produtos`/`taxas` com `utiliza`, `valor_convertido`, `pacote`, `zerar`,
`fator_k`, textos e códigos.

## Interpretações (onde o manual deixa margem)

1. **T10, T13, T14, T15** não dão todos os números (custo, valor do subserviço). Os testes usam
   valores ilustrativos, explicados no docstring de cada caso. T13 e T14 foram montados como
   orçamento: o custo vem de produto da composição **sem Utiliza** (receita 0, custo conta).
2. **Linha 🔒 de serviço que soma itens** = Σ quantidade × preço de casa de cada item;
   subserviço entra com a própria linha 🔒 (recursivo).
3. **"Sem preço"** (Farol consolidado roxo) = produto com Utiliza cuja cadeia não achou fonte nem
   valor. Um `0,00` digitado é "gratuito", não "sem preço".
4. **"Sem custo"** = custo vazio **ou ≤ 0**. Serviço ou taxa sem produto: sem Farol (não é roxo).
5. **Cores:** índice ≤ Vermelho → VERMELHO; ≤ Amarelo → AMARELO; acima → VERDE (T14: 100% na
   régua 100/120 = vermelho).
6. **Arredondamento:** preço de produto com Fator K é arredondado a centavos.
7. **Filhos de subserviço** mostram valores por 1 unidade do pai; o pai multiplica.
8. **Orçamento:** "usados" é informado por `tipo:id` e vale para todas as ocorrências do item na
   árvore. Item embutido = pacote fechado acima **e** Zerar do próprio item.
9. **Farol pela API — nomes REAIS (medidos em produção em 25/09/2026).** O Swagger está
   incompleto e, em `/farol/itens`, usa nomes que a resposta real não tem (`custo`, `receita`,
   `farol`, `utiliza`). O `conferir_farol.py` usa os nomes reais como primários e aceita os do
   Swagger por compatibilidade:
   - `/farol/itens`: `receita_item_total`, `receita_unitaria`, `custo_item_total`, `quantidade`,
     `quantidade_efetiva`, `conta_no_total`, `motivo_exclusao`, `utiliza_no_convenio`,
     `zerar_valor`, `servico_pai_id` e, repetidos em cada linha, os totais do serviço raiz
     (`receita_total_servico`, `custo_total_servico`, `margem_servico_pct`, `farol_servico`);
   - `/farol/servicos`: além do Swagger, `receita_produtos`, `receita_servicos`,
     `receita_taxas`, `custo_produtos`, `somar_itens`, `zerar_valor`, `qtd_*`;
   - `/farol/produtos`: `receita`, `receita_sem_zerar`, `custo`, `custo_status`, `fator_k`,
     `fonte_id`, `fonte_nome`, `origem_receita`, `tipo_precificacao`, `zerar_valor` e campos
     `dbg_*` (em centavos quando o nome diz `_centavos`).
   Ainda **não confirmado** pela fonte (o kit aceita as duas leituras, nunca acusa erro por elas):
   `receita_item_total` de item fora da conta (0 ou preço cheio, se `conta_no_total` concorda);
   `quantidade_efetiva` (quantidade × pais, ou 0 se fora); `receita` de produto com
   `zerar_valor` (preço ou 0); `receita_servicos` (com ou sem o valor próprio); e se
   `fonte_id` = `fontePrecoCompraOptionsId` (grave 1 item e releia).
10. **Código do serviço no convênio:** a coluna `codigo` vai para `codigo` (nível 3).
    O spec também tem `codigoConvenio` e `codigoTuss`; o kit não os preenche.
11. **Vazio no CSV limpa** valor e Fator K (envia `null`). Use `=` ou `manter` para não mexer.

## Limitações

- Não calcula preço por **tabela TUSS/CBHPM** nem porte: o valor combinado vem do contrato.
- Não lê a Política de Preço do convênio pela API: informe-a no cenário (`politicas`).
- Equipamento não tem valor (aparece como `EQUIPAMENTO_SEM_VALOR`, motivo do kit, não da tela).
- Não modela alçada (nível 2/3) nem o parâmetro que desliga o bloqueio do Farol.
- Valores congelados no atendimento/pré-faturamento não são simulados.
- `CICLO_CORTADO` e `ITEM_NAO_ENCONTRADO_NO_CATALOGO` são motivos do kit.

## Verificação

```
cd <raiz do kit> && python3 -m pytest ferramentas/conversao -q
```
