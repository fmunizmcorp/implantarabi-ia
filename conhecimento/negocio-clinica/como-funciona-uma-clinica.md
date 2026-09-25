# Como funciona uma clínica — o fluxo do paciente e do dinheiro

> **Fonte:** https://www.rabisistemas.com.br/manual/referencia/mapa-funcional.html#visao-por-perfil · `rotinas/recepcao.html` · `rotinas/autorizacao-orcamento.html` · `modulos/prontuario.html#finalizar` · experiência de implantação real (generalizada) · **Conferido em:** 2026-09-25
> **Vale para:** qualquer clínica ambulatorial; telas do Rabi em produção em 25/09/2026 · **Kit:** v0.1.0

## 1. O fluxo em uma linha

```
Pedido/contato → (orçamento | autorização) → AGENDAMENTO → confirmação
  → CHEGADA (acolhimento/check-in) → ATENDIMENTO → FINALIZAR
  → particular: recebimento no caixa (+ NFS-e)
  → convênio: guia → pré-faturamento → lote/XML → envio → retorno → pagamento ou glosa → recurso
```

## 2. Passo a passo (e a tela do Rabi)

| Etapa | O que acontece na vida real | No Rabi |
|---|---|---|
| 1. Contato | Paciente liga, manda mensagem ou agenda pelo serviço online | Busca global; `/portal/pacientes/criar` se for novo |
| 2. Cadastro | CPF, contatos, endereço, convênio + plano + carteirinha, responsável (menor/idoso) | Pacientes |
| 3a. Particular | A clínica monta um **orçamento**; o paciente aprova (pode pagar antes ou no dia) | Orçamento → aprovar vira agendamento |
| 3b. Convênio | Se o procedimento exige, a clínica pede **autorização prévia** à operadora e recebe uma **senha** | Autorização (AGUARDANDO → AUTORIZADA/NEGADA) |
| 4. Agendamento | Data, profissional, local, equipamento; tipo Normal ou Encaixe | `/portal/agenda/criar`; fica **Pendente** se faltar orçamento/autorização exigidos |
| 5. Confirmação | Véspera: lembrete automático + ligação para quem não respondeu | `/portal/agenda/confirmacao` |
| 6. Chegada | Recepção confere dados e carteirinha, faz o **check-in** | Acolhimento → status Acolhido → fila do profissional |
| 7. Atendimento | Consulta, exame, aplicação, procedimento; registra no prontuário e o que foi consumido | Fila de atendimento → prontuário |
| 8. Finalizar | O profissional encerra o registro | Botão Finalizar: Atendido; gera cobrança |
| 9a. Cobrança particular | Recebe no caixa; emite nota fiscal | Financeiro (a receber) + NFS-e |
| 9b. Cobrança convênio | A guia vai para conferência e sai num lote para a operadora | Pré-faturamento → Fechar lote → XML → Administrar lote → Contas a receber |
| 10. Retorno | Operadora paga o lote, total ou parcialmente; o que não pagou é **glosa** | Importar retorno TISS → baixa e glosa automáticas → Glosas (recurso ou aceite) |
| 11. Retorno clínico | Paciente volta dentro do **prazo de retorno** (em geral sem nova cobrança) | Bloqueio de retorno pelo prazo do convênio |

## 3. Particular × convênio

| | Particular | Convênio |
|---|---|---|
| Quem paga | O paciente | A operadora (às vezes com coparticipação do paciente) |
| Documento antes | Orçamento | Autorização prévia (quando o contrato exige) |
| Preço | O que a clínica define (no Rabi: convênio "Particular") | O que está no **contrato** (tabelas de referência + percentuais + preços próprios) |
| Quando recebe | No ato ou parcelado | Semanas depois, após envio do lote e processamento |
| Risco | Inadimplência, desconto excessivo | **Glosa**, prazo perdido, preço defasado |
| Nota fiscal | Por atendimento/recebimento | Em geral por lote/competência |

Existem também **convênios de desconto** (não são plano de saúde: o próprio
beneficiário paga com desconto, sem guia TISS) e **parcerias de
encaminhamento** (sem guia nem glosa). Em uma implantação real, cadastrá-los
como plano TISS gerou erro de envio. Pergunte sempre: "este convênio emite
guia para uma operadora?".

## 4. Papéis na clínica

| Papel | Faz |
|---|---|
| Recepção | Cadastro, agenda, chegada, caixa do particular |
| Confirmação / relacionamento | Confirma a agenda, resgata faltosos, cuida dos retornos |
| Autorizadora / orçamentista | Pedidos às operadoras, orçamentos, acompanhamento |
| Profissionais de saúde | Médicos, enfermagem, nutrição, fisioterapia, psicologia… (têm **conselho**) |
| Faturista | Guias, lotes, retorno, glosas e recursos |
| Financeiro | Contas a pagar/receber, caixa, repasse, nota fiscal |
| Estoque / farmácia | Produtos, lotes, validade, compras, consumo nos atendimentos |
| Gestor / liderança | Indicadores, aprovações (alçada), negociação com operadoras |
| Credenciamento / contratos | Contratos com operadoras, aditivos, reajustes |

Em clínica pequena, 2 ou 3 pessoas acumulam tudo — a configuração (perfis,
alçadas) tem de refletir isso.

## 5. Onde o dinheiro se perde (o que a configuração previne)

1. **Atender sem autorização** que o contrato exige → glosa certa.
2. **Item consumido que não entra na guia** (material, medicamento, taxa) →
   receita perdida sem ninguém perceber.
3. **Preço desatualizado** (reajuste não aplicado, tabela antiga) → cobra menos.
4. **Código errado** (TUSS, tabela 87, CBO) → glosa por codificação.
5. **Fora do prazo** de entrega de guias ou de recurso → perda definitiva.
6. **Retorno cobrado como consulta nova** → glosa e desgaste com a operadora.
7. **Pacote mal configurado** → cobra em dobro (glosa) ou cobra a menos.

Por isso a IA configura com cuidado: composição dos serviços, Utiliza, preços
por convênio, prazos e o Farol como conferência. Estudo de preços:
[../precos-e-conversao/00-INDICE.md](../precos-e-conversao/00-INDICE.md).

## 6. Tipos de atendimento comuns numa clínica ambulatorial

- **Consulta** (primeira vez, retorno, teleconsulta).
- **Exames** no consultório (ECG, ultrassom…), muitas vezes com equipamento
  que precisa de grade própria.
- **Terapias e aplicações**: infusão ou injeção de medicamento (endovenosa,
  intramuscular, subcutânea), com o **serviço de aplicação + o medicamento +
  materiais + taxas**. É onde mais aparecem pacotes e autorizações.
- **Procedimentos** (curativos, pequenas cirurgias ambulatoriais).
- **Sessões em série** (fisioterapia, tratamentos seriados) com autorização
  por quantidade.

Ver [materiais-medicamentos-e-servicos.md](materiais-medicamentos-e-servicos.md).
