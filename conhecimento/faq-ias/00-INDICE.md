# FAQ das IAs — erro → o que fazer

> **Fonte:** implantações reais (clínicas anônimas) + leitura do código do Rabi (`deploy_prd`, só leitura) + medições da API · **Conferido em:** 2026-09-28
> **Vale para:** toda sessão de clínica e do mantenedor · **Kit:** v0.3.0

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
| [F001](F001-servicos-500-filter.md) | POST/PUT /servicos · 500 · `reading 'filter'` | aberto no Rabi — contorno: mandar as 4 listas |
| [F002](F002-400-generico-area-inteira.md) | leitura **e** gravação da mesma área · 400 · "Erro ao processar a operação" | aguardando suporte do Rabi |
| [F003](F003-chave-recusada.md) | qualquer · 503/401 · "Não foi possível validar a chave" | esperado — renovar a chave |
| [F004](F004-put-apagou-campos.md) | PUT · 200 · campos sumiram | documentado — PUT completo |
| [F005](F005-leitura-incompleta.md) | listagens · contagem não bate | documentado — `ler_tudo()` |

Formato de cada entrada: cabeçalho com **Rotas / Status HTTP / Mensagem contém**
(usados pela busca; alternativas separadas por `|`), **Causa** (confirmada ou hipótese,
com a fonte), **Status**, **Origem** (sempre anônima) e as seções *O que fazer* / *O que
NÃO fazer*. Defeitos gerais da API: [../api-externa/defeitos-conhecidos.md](../api-externa/defeitos-conhecidos.md).
