# Metodologia — índice

> **Fonte:** protocolo do kit ([BOOTSTRAP](../BOOTSTRAP.md)) + plano de implantação em sprints (experiência prática, generalizada) · **Conferido em:** 2026-09-25
> **Vale para:** toda sessão (mantenedor do kit e sessões de clínica) · **Kit:** v0.1.0

Como a IA trabalha, independente da sprint. As sprints (`../sprints/`) dizem
**o quê**; esta pasta diz **como**.

| Arquivo | O que tem | Quando ler |
|---|---|---|
| [politicas.md](politicas.md) | contrato de escrita do kit e dos repos de clínica: tamanho e índices, forma dos documentos, kit público-seguro, credenciais, LGPD, nada se perde, papéis, Git, versão | antes de escrever qualquer arquivo |
| [ritual-de-carga.md](ritual-de-carga.md) | os 5 passos de toda gravação (foto antes → prévia → aprovação → grava → foto depois + diff), PUT = sobrescrita, lotes, 207/409/422/401/503, chamadas que exigem ordem escrita | antes de toda gravação no Rabi |
| [conversa-com-o-usuario.md](conversa-com-o-usuario.md) | o motor de perguntas (confirmar / sugerir padrão / pedir), uma pergunta por mensagem, falas boas e ruins, nome antes do ID, "não tenho certeza", barra de evolução | antes de falar com o usuário |
| [lista-unica-de-documentos.md](lista-unica-de-documentos.md) | o pedido único ao cliente, com códigos (CL, CV, FA, PE, DI, DD, SA) e a sprint que cada item destrava; mensagem pronta | S00, e sempre que uma sprint cita um código |
| [ingestao-de-documentos.md](ingestao-de-documentos.md) | qualquer formato → inventário com hash → ficha de extração com página/linha → dados → sprint; OCR; lotes com checkpoint; contradições; importação de outros sistemas; formulário de lacunas | quando chega documento |
| [scrum-da-implantacao.md](scrum-da-implantacao.md) | papéis Scrum × papéis do kit, backlog = checklists, planning, daily de 5 linhas, PDCA, review com foto depois, retro, DoD geral | no início e no fim de cada sprint |
| [modos-de-sessao.md](modos-de-sessao.md) | Implantação, Atualização de configuração, Convênio (NOVO / EM ANDAMENTO / FECHADO, contagens R1–R6, régua, classes A/B/C) e Diagnóstico (só leitura) | na abertura da sessão |
| [agentes-e-produtividade.md](agentes-e-produtividade.md) | script × subagente, extrator em paralelo, conferente-precos, auditor de regressão, "o terminal processa, o contexto recebe o resumo", custo | antes de ler muito dado ou documento grande |

## Ordem de leitura sugerida (primeira sessão de uma clínica)

1. `politicas.md` → 2. `modos-de-sessao.md` → 3. `conversa-com-o-usuario.md` →
4. `ritual-de-carga.md` → 5. `lista-unica-de-documentos.md` →
6. `ingestao-de-documentos.md` → os demais quando precisar.

Ferramentas citadas nestes arquivos ficam em `ferramentas/` do kit (no repo da
clínica, em `.kit/ferramentas/`): painel
(`python3 .kit/ferramentas/implantacao/painel.py --repo .`) e fila de perguntas
(`python3 .kit/ferramentas/implantacao/fila_perguntas.py --repo . --sprint Sxx`).
