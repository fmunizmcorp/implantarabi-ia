# Lista única de documentos — o pedido que se faz ao cliente uma vez só

> **Fonte:** plano de implantação em sprints (experiência prática, Anexo A generalizado) + https://www.rabisistemas.com.br/manual/implantacao/guia-implantacao.html#checklist · **Conferido em:** 2026-09-25
> **Vale para:** produção (ordem oficial de 16 etapas, corrigida em 24/09/2026) · **Kit:** v0.1.0

## Para que serve

Na S00 a IA manda **uma** mensagem com a lista inteira. Nada de pedir documento
"em conta-gotas" ao longo da implantação: isso cansa o cliente e atrasa tudo.
Depois, a IA só cobra **o que falta e trava a sprint da vez** (formulário de
lacunas, ver [ingestao-de-documentos.md](ingestao-de-documentos.md)).

Cada item tem um **código** (ex.: `CL-1`). As sprints citam esse código na seção
"Documentos a pedir". O inventário do repo da clínica usa o mesmo código.

## Regras do pedido

- Qualquer formato serve: PDF, foto do papel, print de tela, Excel, CSV, Word,
  exportação de outro sistema. Em qualquer ordem.
- "Se não tiver, tudo bem" — a IA pergunta depois, **uma coisa por vez**.
- Nunca pedir ao cliente para organizar, renomear ou montar planilha. Isso é
  trabalho da IA.
- Consultório individual recebe a **versão curta** (marcada ⭐ abaixo).
- Nada de credencial por e-mail ou chat público: a chave `rbk_` vai para o
  segredo do ambiente ou para `credenciais/` do repo privado.

## A lista, agrupada

### 1. Da clínica

| Código | Documento | Destrava |
|---|---|---|
| CL-1 ⭐ | Cartão CNPJ e contrato social (ou CPF, se o profissional é autônomo sem CNPJ) | S01 |
| CL-2 | Número do CNES da clínica e de cada unidade | S01 |
| CL-3 ⭐ | Lista das unidades/filiais com endereço completo, CEP e CNPJ de cada uma | S01, S02, S03 |
| CL-4 ⭐ | Lista das salas/consultórios de cada unidade (nome como a equipe chama) | S03 |
| CL-5 | Telefone, celular, e-mail e logo da clínica | S01, S14 |

### 2. Dos convênios

| Código | Documento | Destrava |
|---|---|---|
| CV-1 | Contrato assinado de cada convênio, com todos os aditivos | S04, S10a |
| CV-2 | Tabela de preços de cada convênio (consultas, procedimentos, taxas, pacotes) | S10b |
| CV-3 | Regra de materiais e medicamentos de cada convênio (Brasíndice/SIMPRO, preço de fábrica ou de consumidor, fator K, deflator) | S10a, S10b |
| CV-4 | Dados da operadora: registro ANS, CNPJ, CNES, código da clínica na operadora | S04, S10a |
| CV-5 | Planos atendidos em cada convênio | S04, S10a |
| CV-6 | Credenciamento: quais profissionais atendem por qual convênio | S10b |
| CV-7 ⭐ | Preços do particular (o que o paciente paga) — inclusive pacotes e descontos | S10 (convênio "Particular") |
| CV-8 | Relatório recente de faturamento por convênio (o que de fato se cobra hoje) | S10b, S15 |

### 3. Do que a clínica faz

| Código | Documento | Destrava |
|---|---|---|
| FA-1 ⭐ | Lista de serviços/procedimentos: nome, código (TUSS, se tiver), duração, especialidade | S08 |
| FA-2 | Lista de taxas cobradas (sala, material, aplicação…) com o valor | S05 |
| FA-3 | Lista de medicamentos e materiais usados nos atendimentos | S06 |
| FA-4 | Notas fiscais de compra recentes desses produtos | S04, S06, S12 |
| FA-5 | Lista de equipamentos que precisam ser reservados na agenda | S07 |
| FA-6 | O que vai dentro de cada serviço (ex.: aplicação + medicamento + taxa) e quais são preço fechado | S08, S10b |

### 4. Das pessoas

| Código | Documento | Destrava |
|---|---|---|
| PE-1 ⭐ | Lista de profissionais: nome, CPF, nascimento, contato, endereço, conselho (CRM, CRO…), número, UF, especialidade, RQE | S09 |
| PE-2 ⭐ | Escala de atendimento de cada profissional e de cada equipamento (dias, horários, duração da consulta, sala) | S10 (grade) |
| PE-3 | Quem vai usar o sistema e o que cada pessoa faz (recepção, enfermagem, faturamento, gestão…) | S09, S14 |
| PE-4 | Regra de repasse de cada profissional (percentual ou valor fixo; sobre o bruto ou sobre o recebido) | S12 |

### 5. Do dinheiro

| Código | Documento | Destrava |
|---|---|---|
| DI-1 ⭐ | Contas bancárias e caixas usados (sem senha de banco!) | S12 |
| DI-2 ⭐ | Formas de pagamento aceitas e taxas da maquininha | S12 |
| DI-3 | Plano de contas, categorias e centros de custo, se existirem | S12 |
| DI-4 | Dados fiscais para nota: regime tributário, inscrição municipal, código de serviço, alíquota | S12 |
| DI-5 | Regra de desconto: quem pode dar, até quanto | S14 |
| DI-6 | Margem mínima que a clínica aceita (para a régua do Farol) | S11 |

### 6. Do dia a dia

| Código | Documento | Destrava |
|---|---|---|
| DD-1 ⭐ | Modelos que a clínica imprime hoje: receita, atestado, laudo, termo, orçamento | S14 |
| DD-2 | Regras internas: agendamento, confirmação, validade de orçamento, acolhimento | S14 |
| DD-3 | Contagem de estoque atual (produto, lote, validade, quantidade), se usar estoque | S12 |

### 7. Dos sistemas anteriores

| Código | Documento | Destrava |
|---|---|---|
| SA-1 | Exportação de pacientes do sistema anterior (planilha ou CSV) | S13 |
| SA-2 | Exportação de histórico de atendimentos, só se a clínica decidir migrar | S13 |
| SA-3 | Exportação de cadastros do sistema anterior (serviços, produtos, profissionais, convênios, preços) | S05–S10 (acelera muito) |
| SA-4 | Nome do sistema anterior e quem tem acesso a ele | S00, S13 |

## A mensagem pronta (adaptar o nome)

> **Documentos para a implantação do Rabi na <CLÍNICA>**
>
> Para deixar o sistema pronto, preciso dos documentos abaixo. Pode mandar em
> **qualquer formato** (PDF, foto, print, Excel, Word) e em **qualquer ordem**,
> conforme for achando. Não precisa organizar nada: eu leio, separo e organizo.
> O que não tiver, tudo bem — eu pergunto depois, uma coisa de cada vez.
>
> **Da clínica:** cartão CNPJ · CNES · endereço de cada unidade · nome das salas.
> **Dos convênios:** contrato e aditivos · tabela de preços · regra de materiais e
> medicamentos · planos atendidos · quem atende por qual convênio.
> **Do particular:** a tabela de preços que o paciente paga.
> **Do que a clínica faz:** lista de serviços · taxas · medicamentos e materiais ·
> algumas notas fiscais de compra · equipamentos · o que vai dentro de cada serviço.
> **Das pessoas:** lista dos profissionais (com conselho e especialidade) · escala
> de cada um · quem vai usar o sistema e o que faz · regra de repasse.
> **Do dinheiro:** contas e caixas · formas de pagamento · dados de nota fiscal ·
> regra de desconto.
> **Do dia a dia:** modelos de receita, atestado, termo e orçamento · regras de
> agendamento · contagem de estoque (se tiver).
> **Do sistema que vocês usam hoje:** se der, uma exportação dos pacientes e dos
> cadastros em planilha.
>
> Depois de cada etapa eu mostro o que vou cadastrar e peço o seu "pode gravar".

**Versão curta (consultório individual):** só os itens ⭐.

## Como a IA usa esta lista depois

1. Cada arquivo recebido entra no `documentos-do-cliente/inventario.md` com o
   código (ou códigos) que ele cobre.
2. O painel de cada sprint mostra quais códigos já chegaram.
3. Código faltando que **trava** a sprint vira linha no formulário de lacunas
   (`pendencias/LACUNAS.md`), com o efeito prático explicado.
4. Código faltando que **não trava** (ex.: CL-5) não é cobrado na daily.
