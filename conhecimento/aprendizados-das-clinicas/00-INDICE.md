# Índice — conhecimento/aprendizados-das-clinicas

> **Fonte:** issues `aprendizado-clinica` do kit, enviadas pelas IAs das clínicas · **Conferido em:** 2026-09-25
> **Vale para:** mantenedor do kit (consolidação) e curiosos · **Kit:** v0.3.0

O conhecimento que as implantações descobrem **volta para o kit** por aqui.
Só entra o **método** (cálculo, regra, comportamento da API, processo,
ferramenta). **Nunca** dado de clínica, pessoa ou paciente.

```
 IA da clínica                        kit (este repo)                      todas as clínicas
 ─────────────                        ───────────────                      ────────────────
 contribuicoes-kit/  ── filtro ──►  issue pública (formulário)  ──►  caixa-de-entrada.md
 (rascunho)          (LIMPO)        label aprendizado-clinica        (workflow aprendizados.yml)
                     + sim do        ▲ 2ª trava: coletar_aprendizados.py      │
                       usuário       │ sinaliza "revisar-privacidade"         ▼ consolidar (prompts/09)
                                                                   lição Lnn / correção / teste
                                                                   → VERSION + CHANGELOG ("Ação nas clínicas")
                                                                   → .kit/ de cada clínica na próxima sessão
```

| Arquivo | O que tem | Quando ler |
|---|---|---|
| [caixa-de-entrada.md](caixa-de-entrada.md) | issues abertas e fechadas (gerado; não edite) | ao consolidar |
| [consolidados.md](consolidados.md) | decisão de cada issue e onde entrou no kit | antes de decidir um item parecido |

Como enviar (clínica): [../../prompts/08-contribuir-com-o-kit.md](../../prompts/08-contribuir-com-o-kit.md) ·
Como consolidar (mantenedor): [../../prompts/09-consolidar-aprendizados.md](../../prompts/09-consolidar-aprendizados.md) ·
Lições já consolidadas: [../licoes-aprendidas/00-INDICE.md](../licoes-aprendidas/00-INDICE.md)
