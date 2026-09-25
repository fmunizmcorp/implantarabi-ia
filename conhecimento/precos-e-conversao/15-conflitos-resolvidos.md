# 15 — Conflitos entre as fontes e como foram resolvidos

> **Fonte:** manual oficial https://www.rabisistemas.com.br/manual/ (25/09/2026) · spec `../api-externa/spec/openapi-2026-09-25.json` · documento normativo de pacote da experiência (24/09/2026) · documentos da experiência (jun–set/2026) · **Conferido em:** 2026-09-25
> **Vale para:** produção em 25/09/2026 · **Kit:** v0.1.0

**Critério geral:** prevalece o **manual oficial de 25/09/2026** + o **Swagger
de 25/09/2026** + a **regra normativa de pacote** (decisão do proprietário,
24/09, confirmada pelo manual em 25/09). Documento mais antigo que conflite
com eles é **histórico**. Quando nenhuma fonte primária resolve, o kit
marca **não confirmado** e diz como verificar.

## Os 7 conflitos registrados no plano do kit

### C1. Quem cria o login do colaborador
- **Versões:** (a) "a IA só cadastra; o login é feito pela tela/pelo dono";
  (b) "a IA cria o login".
- **Decisão:** a IA cria o login pela rota **externa**
  `POST /colaboradores/{id}/usuario` (`colaborador:update`; `409` = já tem
  login) e define a senha inicial, registrada no repo **privado** da clínica.
- **Prevalece:** manual (implantacao-via-api.html#passo-9) + decisão do
  proprietário. Detalhe fora desta pasta (API externa / sprint de
  colaboradores).

### C2. Zerar em medicamento
- **Versões:** (a) "**nunca** marcar Zerar num medicamento — a clínica
  entregaria o remédio sem cobrar" (scripts de sessão, 24/09); (b) manual,
  Receita D: medicamento **incluso** num pacote fechado recebe Zerar.
- **Decisão:** Zerar é por item e **só age dentro de pacote de preço
  fechado**. Medicamento em **conta aberta** → Zerar ✘ (e é aí que a regra
  "nunca" nasceu). Medicamento **incluso** no preço fechado de um pacote
  (contrato diz que o preço já inclui o remédio) → Zerar ✔. A **aplicação**
  (serviço raiz que é o pacote) **não** recebe Zerar. Conta aberta = sem
  Pacote e sem Zerar.
- **Prevalece:** manual (guia-clinica.html#receita-d, guia-ia.html#arvore-de-decisao) + normativo de pacote.

### C3. Semântica do PUT
- **Versões:** (a) "PUT atualiza só o que foi enviado"; (b) "PUT sobrescreve
  o registro inteiro" (vivido: valor e especialidade apagados).
- **Decisão:** tratar **todo PUT como sobrescrita** (GET antes, reenviar o
  objeto completo com os nomes de escrita), **exceto** as rotas que declaram
  upsert/merge: abas do convênio `PUT /convenios/{id}/servicos|taxas|produtos|colaboradores|especialidades`
  (campo omitido mantém; `null` limpa os valores) e `/parametros/desconto`.
  `/parametros/financeiro` é **misto**: omitir `categoriaPagamentoId`/`centroDeCustoId`
  grava null — reenvie sempre os dois.
- **Prevalece:** Swagger 25/09 (descrição de cada rota).

### C4. 0,00 × vazio
- **Versões:** (a) documentos até 22/09: "0 no serviço vira vazio e cai no
  catálogo; use 0,01 para marcar"; "nunca gravar zero num serviço esperando
  R$ 0,00"; (b) manual 23–25/09: 0,00 é zero em todas as telas; vazio desce.
- **Decisão:** **0,00 = zero real; vazio (`null`) = sem regra, desce de
  nível; 0,01 como marcador é PROIBIDO.**
- **Prevalece:** manual (precos/index.html#tres-niveis; arvore-de-decisao.html#vazio-zero-por-atributo).

### C5. Pacote no convênio Particular
- **Versões:** (a) estudo de 23/09: "desmarcar Pacote da aplicação no
  Particular — o particular paga tudo"; (b) correção do proprietário no
  mesmo dia e normativo de 24/09: o pacote é um preço fechado; o que está
  dentro sai a R$ 0,00 e isso está certo; o Particular **trabalha com
  pacote** nas aplicações.
- **Decisão:** no Particular (e em todo convênio que trabalha com pacote),
  a aplicação é **P ✔ Z ✘**; materiais e taxas dela **Z ✔**; serviços de
  medicamento em conta aberta **P ✘ Z ✘** (Receita J, arquivo 11).
- **Prevalece:** normativo de pacote + manual (valor combinado ≠ pacote).

### C6. Permissão `equipamento:read`
- **Versões:** (a) "a chave não tem/ a rota não existe"; (b) existe.
- **Decisão:** `equipamento:read` **existe** (corrigido em 24/09). Detalhe
  na documentação da API externa do kit.
- **Prevalece:** Swagger 25/09.

### C7. Login pela rota interna × externa
- **Versões:** (a) usar rota interna da tela; (b) rota externa.
- **Decisão:** rota **externa** `POST /colaboradores/{id}/usuario`. API
  interna só quando não houver rota externa e com ordem escrita.
- **Prevalece:** manual (passo-9) + Swagger 25/09.

## Outros conflitos da área de preços

### C8. Valor combinado fecha o preço?
- **Versões:** (a) "escreva o valor à mão no serviço e o pacote fecha"; (b)
  "valor combinado muda só a base; os itens somam por cima".
- **Decisão:** **valor combinado NÃO é pacote.** Preço fechado = V + Pacote
  + Zerar nos inclusos. Na API, `pacote: true` é obrigatório.
- **Prevalece:** manual 25/09 (regra vigente, decisão do proprietário).

### C9. O que é o "nível 2"
- **Versões:** (a) plano de sprints: "nível 2 = valor por especialidade /
  regra intermediária"; (b) manual: nível 2 = **Política de Preço por Tipo
  de Produto**, só para preço de produto.
- **Decisão:** (b). Serviço e taxa têm só convênio → cadastro.
- **Prevalece:** manual (arvore-de-decisao.html#tabela-mestra).

### C10. Tabela interna define preço particular?
- **Versões:** (a) manual antigo e `mapa-funcional` (ainda desatualizado):
  "tabela interna define o valor das consultas particulares"; (b)
  configuracoes.html#tabela-precos (corrigido 24/09): é fonte de preço de
  **produto**.
- **Decisão:** tabela interna = preço de **produto**. Particular vem do
  convênio "Particular".
- **Prevalece:** configuracoes.html#tabela-precos (24/09).

### C11. Item que o convênio não paga: desligar ou ligar com zero?
- **Versões:** (a) regra antiga de projeto: "se o convênio não paga o item,
  ele fica LIGADO, com 0,00 e Zerar ✔ — nunca desligado"; (b) manual:
  Utiliza = "o convênio cobre"; não cobre → Utiliza ✘ (custo sem receita).
- **Decisão:** distinguir três casos: **incluso em pacote** → U ✔ + Z ✔;
  **gratuito** → U ✔ + V 0,00; **não coberto** (o convênio não paga nunca,
  nem dentro de pacote) → U ✘, com decisão escrita. Serviço que a clínica
  presta **nunca** fica U ✘ (não agenda).
- **Prevalece:** manual (receitas F, G, I) com a cautela da regra antiga
  para itens de pacote.

### C12. Farol › Itens pela API traz "conta no total" e motivo? — RESOLVIDO em 25/09
- **Versões:** (a) plano de sprints: `/farol/itens` traz `conta_no_total`,
  `motivo_exclusao`, `receita_total_servico`; `/farol/produtos` traz
  `origem_receita`, `fonte_nome`, `fator_k`, `dbg_*`; (b) Swagger e manual
  25/09: itens trazem só `servico_raiz_id, item_tipo, item_id, item_nome,
  custo, receita, farol, utiliza`; margem, valor efetivo e Conta no total
  **só na tela**.
- **Evidência:** leitura real (só GET) na API de **produção** em 25/09/2026:
  `conta_no_total` e `motivo_exclusao` **existem** na resposta; a resposta
  real de itens usa `receita_item_total`, `custo_item_total`,
  `utiliza_no_convenio`, `quantidade_efetiva`, `receita_unitaria` e os totais
  do serviço raiz — e **não** traz `custo`, `receita`, `farol`, `utiliza` do
  Swagger. `/farol/produtos` traz `origem_receita`, `fonte_id`, `fonte_nome`,
  `fator_k`, `receita_sem_zerar`, `custo_status` e `dbg_*`. Lista completa em
  [08-farol.md §3](08-farol.md#3-aba-farol-do-convênio-e-api).
- **Decisão:** vale a **resposta real**; o Swagger está incompleto no Farol
  ([defeitos-conhecidos](../api-externa/defeitos-conhecidos.md)).
  `conferir_farol.py` usa os nomes reais como primários (inclusive
  `conta_no_total`/`motivo_exclusao`) e aceita os do Swagger por
  compatibilidade; `montar_cenario.py` usa `/farol/produtos` para custo,
  fonte, Fator K e para conferir o preço previsto.
- **Ainda aberto:** o significado exato de `receita_item_total` em item fora
  da conta, de `quantidade_efetiva` e de `receita` com `zerar_valor`, e se
  `fonte_id` = `fontePrecoCompraOptionsId` — o kit aceita as leituras
  possíveis até confirmar gravando 1 item em homologação.
- **Prevalece:** resposta real de produção (25/09) sobre Swagger 25/09 e
  guia-ia.html#alg-farol-itens.

### C13. Fronteiras exatas do Farol
- **Versões:** manual "≤ Vermelho → bloqueado" e T14 (100 = bloqueado);
  página da API: "verde ≥ amarelo; amarelo ≥ vermelho".
- **Decisão (motor):** `≤ Vermelho` → VERMELHO; entre → AMARELO; `≥ Amarelo`
  → VERDE. **Não confirmado** no limite do amarelo; testar em homologação.

### C14. Restrito hospitalar com política PMC
- **Versões:** (a) experiência 12/09: "o Rabi não tem plano B; sai R$ 0,00";
  (b) manual 25/09: tabela interna sem valor → Preço de venda tabela × FK.
- **Decisão:** vale o manual; em ambos os casos o preço **não** é o do
  contrato → usar PF + x% para restritos. Conferir em `/farol/produtos`.

### C15. Contar serviços ligados pela API externa
- **Versões:** (a) "contar só pela API interna — a externa conta vínculos de
  serviços desativados"; (b) o kit trabalha pela API externa.
- **Decisão:** contar pela externa **cruzando com `ativo`** do catálogo e
  usando os filtros `servicoAtivo`/`apenasAtivosNoConvenio`/`ativoNoConvenio`.
- **Prevalece:** Swagger 25/09 (filtros disponíveis) + cautela da experiência.

### C16. Zerar sozinho basta em produto/taxa?
- **Versões:** (a) observação de 24/09 (manhã): "o item incluso precisa do
  Zerar **e** do 0,00 gravado"; (b) manual: Zerar por item age sozinho em
  pacote fechado (produção desde 24/09).
- **Decisão:** (b). Não grave 0,00 "para garantir": ele vira preço zero
  também quando o item é vendido sozinho.
- **Prevalece:** manual 24–25/09.
