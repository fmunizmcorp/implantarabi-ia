# Índice — conhecimento/negocio-clinica

> **Fonte:** manual oficial https://www.rabisistemas.com.br/manual/ + padrões ANS (TISS/TUSS) + experiência de faturamento e implantação real (generalizada, sem dado de clínica) · **Conferido em:** 2026-09-25
> **Vale para:** clínicas ambulatoriais no Brasil em 2026 · **Kit:** v0.1.0

Como uma clínica funciona e ganha (ou perde) dinheiro com convênios. É o
conhecimento de "gestor de faturamento" que a IA precisa para configurar o
Rabi pensando no uso real. Leia só o arquivo do assunto.

| Arquivo | O que tem | Quando ler |
|---|---|---|
| [como-funciona-uma-clinica.md](como-funciona-uma-clinica.md) | Fluxo do paciente (agendamento → chegada → atendimento → cobrança), particular × convênio, papéis, onde o dinheiro se perde | Primeira conversa com a clínica; S00 |
| [faturamento-medico.md](faturamento-medico.md) | Guias (consulta, SP/SADT, honorários), lote, XML, prazos do contrato → campos do convênio, calendário, conciliação | Sprint de convênios; ao falar com o faturista |
| [tiss-tuss-ans.md](tiss-tuss-ans.md) | Componentes TISS, versões, tabelas de domínio, **Tabela 87** (com o que é confirmado e o que não é), Tabela 36, TUSS 22, CBHPM/portes, Rol/DUT | Ao definir código, tabela 87 e tipo de atendimento de itens |
| [glosas-e-recursos.md](glosas-e-recursos.md) | Tipos de glosa, classificação A/B/C, recurso com fundamentação tripla, prevenção pela configuração | Ao conferir convênio; quando a clínica relata glosas |
| [autorizacao-previa.md](autorizacao-previa.md) | Quando exigir (infusão ambulatorial: toda aplicação), limiares de contrato × internação, `autorizacaoPrevia`, `exigirToken`, elegibilidade | Sprint de serviços e de convênios |
| [analise-de-contratos.md](analise-de-contratos.md) | 6 dimensões, régua contratual com ORIGEM, evidência tripla, proposta ≠ aditivo, OCR, edições congeladas | Antes de configurar qualquer convênio |
| [fontes-de-preco.md](fontes-de-preco.md) | SIMPRO, Brasíndice PF/PMC (unitário = total ÷ qtd), CMED por ICMS, OPME, padrões de cobrança, casamento por nome+dose | Sprint de produtos e políticas de preço |
| [materiais-medicamentos-e-servicos.md](materiais-medicamentos-e-servicos.md) | Serviço × produto × taxa, padrão aplicação + medicamento, pacote × conta aberta, o que não se cobra, estoque | Sprint de produtos e serviços |
| [profissional-de-saude.md](profissional-de-saude.md) | Conselho ativo → agenda e convênio; administrativo sem conselho; CBO (códigos confirmados); RQE | Sprint de colaboradores |
| [lgpd-na-implantacao.md](lgpd-na-implantacao.md) | Regras da IA com dado pessoal e de saúde; recursos LGPD do Rabi e status; checklist | Sempre que tocar paciente ou profissional; S13 |

Relacionados: [../sistema-rabi/00-INDICE.md](../sistema-rabi/00-INDICE.md) ·
[../precos-e-conversao/00-INDICE.md](../precos-e-conversao/00-INDICE.md) ·
[../licoes-aprendidas/00-INDICE.md](../licoes-aprendidas/00-INDICE.md)
