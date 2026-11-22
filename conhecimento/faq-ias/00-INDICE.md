# FAQ das IAs — erro → o que fazer

> **Fonte:** implantações reais (clínicas anônimas) + leitura do código do Rabi (`deploy_prd`, só leitura) + medições da API · **Conferido em:** 2026-11-22
> **Vale para:** toda sessão de clínica e do mantenedor · **Kit:** v0.4.0

**Regra:** deu erro no Rabi? **Antes** de tentar de novo ou perguntar ao usuário, procure aqui:

```bash
python3 .kit/ferramentas/kit/buscar_faq.py "<trecho da mensagem>" --status <código> --rota "<MÉTODO /rota>"
```

O `cliente.py` já mostra "possível FAQ: Fxxx" no próprio erro. O kit (`.kit/`) é
atualizado a cada sessão; no meio de uma sessão, `git -C .kit pull` traz o FAQ mais novo.
Não achou? Resolva como der, e registre o caso como aprendizado tipo `api`
(`prompts/08-contribuir-com-o-kit.md`): o mantenedor transforma em entrada nova.

| Entrada | Sintoma (rota · status · mensagem) | Status |
|---|---|---|
| [F001](F001-servicos-500-filter.md) | POST/PUT /servicos · 500 · `reading 'filter'` | **corrigido pelo Rabi em 28/09 17:43** (explicação técnica na entrada) |
| [F002](F002-400-generico-area-inteira.md) | leitura **e** gravação da mesma área · 400 · "Erro ao processar a operação" | resolvido pelo Rabi em 28/09 — se voltar, mesma mensagem ao suporte |
| [F003](F003-chave-recusada.md) | qualquer · **401** "Token de integração inválido, revogado ou expirado" (até 25/09: 503) | esperado — `rbt_`: Renovar; `rbk_`: pedir ao time Rabi |
| [F004](F004-put-apagou-campos.md) | PUT · 200 · campos/vínculos sumiram | documentado — rotas parciais: foi `null` ou lista enviada; demais: PUT completo |
| [F005](F005-leitura-incompleta.md) | listagens · contagem não bate | documentado — `ler_tudo()` |
| [F006](F006-conferir-gravacoes-anteriores-a-28-09.md) | gravações **antes de 28/09 17:43** (lotes, PUT financeiro/fornecedor, estoque, UF…), PUT de serviço/paciente/convênio **antes de 01/10**, composição sem valor **antes de 02/10**, sexo pela tela **antes de 30/10** | corrigido no Rabi — conferir uma vez o que foi gravado antes |
| [F007](F007-409-excluir-produto-taxa-em-servico.md) | DELETE /produtos · /taxas · 409 · "composição de serviço ativo" | proteção do Rabi (02/10) — ajustar os serviços antes |
| [F008](F008-403-escopo-faltante.md) | qualquer · 403 · `escopoFaltante` | esperado — liberar só a permissão necessária |
| [F009](F009-grade-recusada-consultorio-ocupado.md) | grades · recusa · consultório ocupado | regra do Rabi (18/11) |
| [F010](F010-422-status-automatico-orcamento.md) | PUT /orcamentos/status · 422/409 | regra do Rabi — só com ordem escrita |
| [F011](F011-convenio-modo-visualizacao.md) | tela do convênio · "não edita / não salvou" | comportamento da tela (29/09–02/10) |

Formato de cada entrada: cabeçalho com **Rotas / Status HTTP / Mensagem contém**
(usados pela busca; alternativas separadas por `|`), **Causa** (confirmada ou hipótese,
com a fonte), **Status**, **Origem** (sempre anônima) e as seções *O que fazer* / *O que
NÃO fazer*. Defeitos gerais da API: [../api-externa/defeitos-conhecidos.md](../api-externa/defeitos-conhecidos.md).
