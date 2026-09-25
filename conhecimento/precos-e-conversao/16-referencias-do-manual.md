# 16 — Referências canônicas do manual (URL + âncora)

> **Fonte:** manual oficial publicado em https://www.rabisistemas.com.br/manual/ (v2.3, atualizado em 25/09/2026); âncoras conferidas nos arquivos-fonte do manual · **Conferido em:** 2026-09-25
> **Vale para:** produção em 25/09/2026 · **Kit:** v0.1.0

Base: `https://www.rabisistemas.com.br/manual/`. Quando o kit e o manual
divergirem, **vale o manual** (fonte primária) — registre a divergência.

## 1. Área Preços e Conversão de Valores

### Visão geral — `precos/index.html`
- https://www.rabisistemas.com.br/manual/precos/index.html#ideia-em-uma-pagina — a ideia em uma página
- https://www.rabisistemas.com.br/manual/precos/index.html#valor-de-casa-e-por-convenio — valor da casa × por convênio
- https://www.rabisistemas.com.br/manual/precos/index.html#tres-niveis — os 3 níveis e vazio ≠ zero
- https://www.rabisistemas.com.br/manual/precos/index.html#tres-linhas — linhas 🔒 🔁 ✅
- https://www.rabisistemas.com.br/manual/precos/index.html#quatro-linhas-servico — coluna Valor com 4 linhas (Σ)
- https://www.rabisistemas.com.br/manual/precos/index.html#servico-composto — serviço composto e a conta única
- https://www.rabisistemas.com.br/manual/precos/index.html#valor-combinado-nao-e-pacote — valor combinado não é pacote
- https://www.rabisistemas.com.br/manual/precos/index.html#exemplos-de-pacote
- https://www.rabisistemas.com.br/manual/precos/index.html#custo-e-farol — custo e cores do Farol
- https://www.rabisistemas.com.br/manual/precos/index.html#farol-consolidado
- https://www.rabisistemas.com.br/manual/precos/index.html#farol-itens — Farol › Itens por linha
- https://www.rabisistemas.com.br/manual/precos/index.html#onde-aparece — onde cada configuração aparece
- https://www.rabisistemas.com.br/manual/precos/index.html#perguntas-rapidas

### Árvore de decisão — `precos/arvore-de-decisao.html`
- #visao-geral · #tabela-mestra · #vazio-zero-por-atributo · #arvores
- #arvore-servico · #arvore-produto · #arvore-taxa · #arvore-subservico · #arvore-entra · #arvore-farol · #arvore-xml
- #exemplos · #exemplo-simples · #exemplo-composto · [exemplo real antes × depois](https://www.rabisistemas.com.br/manual/precos/arvore-de-decisao.html#exemplo-noripurum)
- #checklist (conferência do implantador) · #continue
- Ex.: https://www.rabisistemas.com.br/manual/precos/arvore-de-decisao.html#tabela-mestra

### Guia do Implantador — `precos/guia-implantador.html`
- #mapa-das-telas · #tres-niveis-por-item · #produto-cadeia · #taxa-niveis · #servico-niveis · #textos-codigos
- #regra-unica · #quatro-chaves · #formula · #tabela-verdade · #valor-combinado-nao-e-pacote · #exemplos-conferencia
- #regras-subservico · #linha-check-servico · #quatro-linhas · #expandir-servico
- #ordem-configuracao · #impacto-modulos · #como-conferir · #diagnostico · #limitacoes
- Ex.: https://www.rabisistemas.com.br/manual/precos/guia-implantador.html#tabela-verdade

### Guia da Clínica — `precos/guia-clinica.html`
- #parte-1-ideia · #tabela-com-excecoes · #branco-diferente-de-zero · #tres-linhas-clinica · #quatro-linhas-clinica
- #parte-2-itens · #item-servico · #item-produto · #item-taxa
- #parte-3-convenio · #aba-dados-convenio · #abas-produtos-servicos-taxas
- #parte-4-receitas · #receita-a · #receita-b · #receita-c · #receita-d · #marque-pacote · #receita-e · #receita-f · #receita-g · #receita-h · #receita-i
- #parte-5-depois · #farol-clinica · #farol-itens · #parte-6-conferencia · #erros-comuns
- Ex.: https://www.rabisistemas.com.br/manual/precos/guia-clinica.html#receita-i

### Guia para IA — `precos/guia-ia.html`
- #regras-de-conduta · #algoritmo · #alg-produto · #alg-taxa · #alg-servico-base · #alg-servico-composto
- #alg-orcamento · #alg-farol · #alg-farol-consolidado · #alg-tipo-atendimento · #alg-textos · #alg-farol-itens
- #alg-quatro-linhas · #alg-api-pacote · #arvore-de-decisao · #checklist-perguntas · #invariantes · #casos-de-teste · #efeitos-a-jusante
- (#modelo-de-dados, #fontes-de-verdade e #consultas apontam para a wiki interna restrita — não disponível ao kit)
- Ex.: https://www.rabisistemas.com.br/manual/precos/guia-ia.html#casos-de-teste

## 2. Configurações — `modulos/configuracoes.html`

- https://www.rabisistemas.com.br/manual/modulos/configuracoes.html#convenios — convênio × operadora
- …#convenios-passo-a-passo · #convenios-campos (prazos, Pagamento no ato, Fator K) · #convenios-tabela (importar/copiar/exportar)
- …#convenios-conversao-servico — painel de conversão de serviço
- …#convenios-regras-preco-2309 — resumo das regras de preço em produção
- …#convenios-novidades-set-2026 (tabela 87 com 05/12/97; fix "Política de Preço null")
- …#convenios-novidades-ago-2026 · #convenios-novidades-jul-2026 (farol por parâmetros)
- …#convenios-cbos — especialidades e colaboradores credenciados
- …#tabela-precos · #tabela-precos-passo-a-passo — tabela interna = preço de produto
- …#servicos · #servicos-passo-a-passo
- …#tipo-atendimento · #tipos-codigo · #taxas · #parametros

## 3. API externa — `api-externa/`

### Implantação pela API — `api-externa/implantacao-via-api.html`
- https://www.rabisistemas.com.br/manual/api-externa/implantacao-via-api.html#ordem-oficial · #dependencias-corrigidas
- …#passo-5 (taxas) · #passo-6 (produtos) · #passo-8 (serviços; `somarItems`) · #passo-9b (tabela interna)
- …#passo-10 · **#convenio-fase-1** (dados do convênio, política) · **#convenio-fase-2** (abas em lote, pacote pela API)
- …**#passo-11** (conferência pelo Farol) · **#ler-farol-itens** (como ler cada linha)
- …#roteiro-ia · #checklist-final

### Visão geral e convenções — `api-externa/index.html`
- #autenticacao · #permissoes · #convencoes · #paginacao · #valores · #put · #delete · #lotes · #codigos · #nao-cobre

### Referências por operação
- `api-externa/referencia-cadastros.html`: #grupo-convenios · #op-put-convenios-id-servicos · #op-put-convenios-id-produtos · #op-put-convenios-id-taxas · #op-get-convenios-id-farol-itens · #op-get-convenios-id-farol-servicos · #op-get-convenios-id-farol-produtos · #op-put-convenios-id · #grupo-tabelas-preco · #op-get-tabelas-preco-precificacao · #op-post-tabelas-preco-produtos-bulk · #op-get-auxiliares-tabelas-ans87 · #op-post-servicos · #op-post-produtos · #op-post-taxas
- `api-externa/referencia-parametros.html`: #grupo-parametros · #op-get-parametros-orcamento
- `api-externa/erros-e-boas-praticas.html`: #lote-207 · #idempotencia · #limites · #armadilhas

Swagger oficial: https://api.rabisistemas.com.br/external-docs/ (cópia do kit:
[../api-externa/spec/openapi-2026-09-25.json](../api-externa/spec/openapi-2026-09-25.json)).

## 4. Implantação — `implantacao/guia-implantacao.html`

- …#ordem-oficial · #correcao-ordem-2409 · #dependencias
- …#etapa-5 (Taxas) · #etapa-6 (Produtos) · #etapa-8 (Serviços) · **#etapa-10** (Convênios: dados, depois abas) · **#etapa-11** (Conferência pelo Farol) · #etapa-15 (testes) · #go-live
- Ex.: https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#etapa-10

## 5. Pontos do manual sabidamente desatualizados (não usar)

- `referencia/mapa-funcional.html#configuracoes` — ainda diz que a tabela
  interna define preço particular (errado; ver
  `modulos/configuracoes.html#tabela-precos`).
