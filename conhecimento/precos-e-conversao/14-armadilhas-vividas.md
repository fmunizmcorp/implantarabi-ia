# 14 — Armadilhas vividas (lições reais, generalizadas)

> **Fonte:** experiência de uma implantação real (jun–set/2026), generalizada e sem dados da clínica; conferida contra o manual oficial https://www.rabisistemas.com.br/manual/precos/ (25/09/2026) · **Conferido em:** 2026-09-25
> **Vale para:** produção desde 23–24/09/2026 (onde a lição é anterior, está dito) · **Kit:** v0.1.0

Cada armadilha: **o que aconteceu → por quê → como evitar**. Valores e
nomes são ilustrativos.

## A1. Orçamento particular de medicamento saindo R$ 0,00

- **O que aconteceu.** No convênio Particular, a aplicação endovenosa
  vendida sozinha orçava certo (valor fixo, materiais e taxas a 0 dentro
  dela). Mas os serviços "Medicamento X aplicado EV" (somar ✔, contendo a
  aplicação + o medicamento) saíram **R$ 0,00** em orçamentos reais —
  serviço, remédio, materiais e taxas. Em ~300 serviços de medicamento com
  a aplicação como subserviço, o risco era o mesmo.
- **Por quê.** Combinação de marcações erradas no convênio: as aplicações
  estavam com **Zerar ✔** (além de Pacote ✔) e os próprios serviços de
  medicamento também com Zerar ✔; com somar ✔ e sem valor combinado, a base
  do serviço é 0 e tudo dependia dos itens — que acabaram zerados. O caso
  ocorreu na janela de transição das regras (23/09, noite, antes do "Zerar
  sem cascata" de 24/09).
- **Hipótese errada da época (não repita):** "com somar ✔ o valor digitado
  à mão é ignorado". Falso: somar ✔ ignora o **Valor do catálogo**, não o
  **valor combinado do convênio** (que é a base, inclusive 0).
- **Como evitar.** Receita J do arquivo 11: a aplicação **é** o pacote (P ✔,
  **Z ✘ nela**); materiais e taxas dela Z ✔; serviço de medicamento em conta
  aberta P ✘ Z ✘; medicamento Z ✘. Invariante **I8** (somar sem nada que
  conte → Σ 0). E sempre um **orçamento de teste** de medicamento.

## A2. O marcador R$ 0,01

- **O que aconteceu.** Antes de 23/09/2026, 0,00 era tratado como vazio em
  várias telas; usou-se 0,01 como "marca" de linha. Depois da correção, os
  0,01 viraram **preço de verdade**: serviços saindo 300,01 ou 0,01; Farol
  distorcido.
- **Como evitar.** Nunca gravar 0,01. Varrer (contagem R2) e, para cada um,
  perguntar: marcador (limpar → `null`) ou preço simbólico decidido (manter
  e registrar a decisão)?

## A3. PUT que apagou valor e especialidade

- **O que aconteceu.** Uma correção de um serviço do catálogo apagou o
  **valor** e a **especialidade**. O PUT substitui o registro inteiro, e os
  nomes de campo da **leitura** diferem dos da **escrita**: leitura
  `somarItens` × escrita `somarItems`; leitura de especialidades
  (`ServicoEspecialidade` na API interna) × escrita `especialidadesId`.
  Enviar o nome da leitura = campo ignorado = apagado.
- Outros pares iguais: convênio `registroANS` (criação) × `codigoANS`
  (atualização); parâmetros de orçamento `diasVencimento`/`consideracoes`
  (envio) × `diasValidos`/`consideracoesGerais` (resposta).
- **Como evitar.** GET → alterar só o que muda → reenviar o objeto
  **completo** com os nomes de **escrita** do Swagger → reler e fazer diff.
  Trate todo PUT como sobrescrita, salvo as rotas que declaram upsert.

## A4. Editar por ID sem ler nome e "ativo"

- **O que aconteceu.** Com o sistema deslogado e só os ids em mãos, uma
  sessão gravou valores em 12 vínculos que, ao se ler os nomes, eram de
  serviços **inativos** e de outra natureza (a condição dada pela clínica
  não se cumpria). Foi revertido e conferido (zero diferenças).
- Achado relacionado: serviços inativos continuavam ligados nos convênios
  com código antigo, enquanto os cadastros **ativos** corretos estavam com
  Utiliza ✘ — a recepção não conseguia agendar o serviço certo.
- **Como evitar.** Antes de gravar: conferir **nome, ativo e natureza** de
  cada item, não só o id. Regra permanente: avaliar ativo/inativo de
  serviço, produto, taxa e convênio **antes** de qualquer escrita.

## A5. Composição circular

- **O que aconteceu.** Um serviço continha outro que o continha (A ⊃ B ⊃ A)
  e o valor inflou.
- **Como evitar.** O sistema corta ciclos, mas é erro de cadastro. O
  simulador acusa ciclo (K11) e a IA propõe a composição correta.

## A6. "Desligar" ≠ "não cobrar"

- Para item **incluso em pacote**, o certo é **Utiliza ✔ + Zerar ✔** (e, se
  ele nunca tem preço próprio no convênio, valor 0,00) — nunca desligar.
  Desligar tira a receita do item em **todos** os serviços do convênio,
  inclusive vendido sozinho, e o custo continua no Farol.
- Serviço desligado não pode ser agendado: nunca desligue serviço que a
  clínica presta.
- Não desligue um serviço deixando o produto dele ligado (a clínica não é
  farmácia).
- Utiliza ✘ só para o que o convênio **realmente não cobre**, com decisão
  escrita.

## A7. Política salva vazia apaga a política

- **O que aconteceu.** Um convênio apareceu com a política de preço **vazia**
  (0 linhas) — apagada num salvamento antigo. Materiais e medicamentos
  caíram no preço da casa.
- Pela API: `politicasPorTipoProduto` enviado = lista completa; lista vazia
  inativa todas.
- **Como evitar.** Nunca salvar política vazia. Conferir a política na tela
  / relatório antes e depois de qualquer edição do convênio.

## A8. Fator K: default 1 e unidade

- Linha nova pode nascer com FK **1** (na planilha, 1 = +100%).
- Tela/API: percentual (`16`); planilha: decimal (`0.16`). Errar = 100×.
- Clicar por coordenada na tela já sobrescreveu a linha **errada** da
  política (linhas a ~40 px). Use os campos pelo nome/rótulo ou a API.
- **Como evitar.** Gravar FK explícito; conferir o efetivo (receita no
  `/farol/produtos`) contra a conta à mão.

## A9. Contratos irmãos divergentes

- **O que aconteceu.** Três convênios com o **mesmo** contrato (réplicas)
  tinham a mesma aplicação configurada diferente: vazio num, 0,00 nos
  outros — o mesmo medicamento saía 300,01 num e 0,01 nos outros; e taxas
  ligadas num e ausentes nos outros.
- **Como evitar.** Irmãos servem para **detectar** inconsistência, nunca
  para decidir o valor: cada um é conferido contra o contrato dele. Atenção:
  contratos "parecidos" com partes diferentes (ex.: direto × via
  intermediadora) são **contratos diferentes** — nunca copie configuração
  de um para o outro.

## A10. Edição em massa fora das sessões

- **O que aconteceu.** Conversões sumiram em dezenas de convênios de uma vez
  — alguém alterou em massa (ex.: "copiar configurações", "selecionar
  todos", importação) fora das sessões controladas.
- **Como detectar.** Muitas linhas do **mesmo serviço** alteradas na **mesma
  hora** em muitos convênios (`updatedAt`) — contagem R6.
- **Como evitar.** Copiar de convênio, "Selecionar/Desativar todos" e
  importação Excel são gravação em massa: **só com ordem escrita** e prévia.

## A11. Limitação: mesmo produto em dois pacotes do mesmo convênio

Zerar é por item × convênio. **Não dá** para o produto ser embutido no
pacote A e cobrado à parte no pacote B do mesmo convênio. Saídas: ajustar o
preço fechado de B para incluir o item, ou cadastrar um produto/serviço
distinto — decisão da clínica. Registre como limitação conhecida.

## A12. Leitura "vazia" com status 200

- **O que aconteceu.** Um atalho de leitura devolvia corpo vazio com
  status 200; foi lido como "nenhum produto ligado". Conclusões erradas
  sobre preço de medicamento saíram daí.
- **Como evitar.** Leitura sem bytes ou com status ≠ 2xx = **falhada**.
  Conferir `linhas lidas = total`. Paginar até `totalPages` (API externa:
  `page` começa em 1). Na API interna antiga, `page` começava em 0 e pedir
  `page=1` pulava a primeira página em silêncio.

## A13. Ler o campo errado

- Um campo `valorUnitario` de uma leitura interna de produto era **saldo de
  estoque** (negativo), não preço — quase virou "correção" de preço.
- **Como evitar.** Preço efetivo por convênio: `/farol/produtos` (`receita`)
  ou a tela. Nunca "conserte" um preço a partir de campo cujo significado
  não foi confirmado.

## A14. Categoria de produto lida pela ordem da tela

Uma leitura pela **ordem** das linhas trocou duas categorias e gerou 76
divergências falsas (teria invertido fonte e FK de duas categorias). Use
sempre o **id** do tipo de produto.

## A15. Medicamento ausente da composição ou sem linha no convênio

- **O que aconteceu.** Em alguns convênios o medicamento de um serviço não
  tinha linha na aba Produtos (ou estava com U ✘ por decisão pendente): a
  clínica aplicava e **não faturava** o remédio; o custo contava e o Farol
  ficava vermelho.
- **Como evitar.** I1 + Farol › Itens: todo item da composição com U ✔ onde
  o convênio paga. Vermelho sempre investigado.

## A16. Julgar preço comparando com a tabela de mercado ou com outro convênio

Erro de método: o valor da casa é o **particular** e varia por desenho; cada
convênio tem o seu contrato. A régua é **a cláusula do contrato daquele
convênio** e o que sai na guia. Código diferente por convênio **não** é
defeito. Categoria "sem linha de política" **não** é defeito por si.

## A17. Preço unitário calculado por divisão

Em conferências a partir de pagamentos, dividir `valor pago ÷ quantidade`
só é válido quando a quantidade existe na fonte; muitas coletas trazem o
**total da linha**. Valores ≤ R$ 0,05 são simbólicos (nunca viram preço).
Diferença > 5× ou descrição que não bate = **suspeito** (o mesmo código
pode servir a outro item): não aplicar sem abrir a guia.

## A18. Restrito hospitalar com política "PMC"

Item sem PMC com política PMC não tem preço de contrato (a experiência viu
R$ 0,00; o manual descreve fallback para o preço de venda da casa × FK —
nenhum dos dois é o contrato). Restrito: política PF + x%.

## A19. Excel do convênio

- A planilha de importação é **sempre** a exportada do próprio Rabi (preserva
  ids e ordem de colunas); o cabeçalho é lido pelo nome exato.
- Capitalização difere por aba (Produtos `SIM/NAO`; Serviços `Sim/Não`).
- Tabela 87 em formato "código - texto" foi rejeitada **em silêncio** nas
  abas Serviços e Produtos.
- FK na planilha é decimal.
- Importação Excel é gravação em massa: só com ordem escrita. Prefira a API
  (upsert com resposta item a item).

## A20. Formulário que descarta alterações

Numa operação pela tela, alterações foram descartadas com a janela em
segundo plano. Prefira a API; se usar a tela, janela em primeiro plano e
**recarregar e reler** depois de salvar.

## A21. Observações antigas que não valem mais

| Dizia-se | Hoje (manual 25/09) |
|---|---|
| "0,00 no serviço vira vazio e cai no catálogo" | 0,00 é zero (desde 23/09) |
| "Zerar em produto/taxa não zera sozinho; precisa gravar 0,00 junto" | Zerar age sozinho dentro de pacote fechado (desde 24/09) |
| "a API não expõe a conversão de taxa por convênio" | `GET/PUT /convenios/{id}/taxas` na API externa |
| "zerar o subserviço zera tudo dentro dele" | só a base dele (desde 24/09) |
| "preço fixo sem Pacote já inclui a composição" | itens sempre entram (desde 23/09) |
| "valor combinado fecha o preço" | não: só Pacote + Zerar (25/09) |
