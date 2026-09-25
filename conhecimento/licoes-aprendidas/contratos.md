# Lições — contratos, cobertura e regras de operadora

> **Fonte:** registros de uma operação real de faturamento e credenciamento (mai a set/2026), generalizados · **Conferido em:** 2026-09-25
> **Vale para:** leitura de qualquer contrato de credenciamento · **Kit:** v0.1.0

Método completo: [../negocio-clinica/analise-de-contratos.md](../negocio-clinica/analise-de-contratos.md).
Origem: [origem.md](origem.md).

## L31 — Proposta comercial não é aditivo

**O que aconteceu:** cartas-proposta de extensão enviadas **pela clínica** eram
tratadas como aditivos. Nenhum documento comprovava o aceite da operadora — e a
lista ampliada já estava em uso no sistema. Em outro caso, uma planilha de
preços "extracontratual" não assinada quase entrou como regra.
**Regra que ficou:** só vale o que está **assinado pelas duas partes** (ou
publicado pela operadora). Proposta vira "pendente de confirmação".
**Como detectar:** documento assinado só pela clínica; ausência de número de
aditivo/data de assinatura da operadora.

## L32 — Evidência tripla para cobertura

**O que aconteceu:** em vários contratos o único anexo assinado e legível
listava 1 especialidade, e a clínica faturava 10 a 18. Faturar prova uso, não
cobertura (pode ser tolerância da operadora ou aditivo escaneado não lido).
**Regra que ficou:** cobertura confirmada = (1) documento assinado pela
operadora + (2) tabela/código do item + (3) faturamento real pago. Só (3) =
bandeira vermelha: confirmar com a operadora antes de mudar o sistema.
**Como detectar:** especialidade/serviço faturado sem cláusula ou anexo.

## L33 — Contrato escaneado: OCR em duas passadas

**O que aconteceu:** cerca de 4 em cada 10 contratos principais eram imagem
sem texto — o maior gargalo de qualidade. A 1ª passada de OCR (português, 300
dpi) recuperou ~85% dos valores de tabela; o resto ficou em branco.
**Regra que ficou:** OCR antes de analisar; 2ª passada a 600 dpi e recorte da
coluna de valores com contraste aumentado; marcar na régua quais valores vieram
de OCR e conferir por amostra com o usuário.
**Como detectar:** PDF sem texto selecionável; tabela com células vazias.

## L34 — Edições de tabela congeladas no contrato

**O que aconteceu:** um contrato fixava Brasíndice e SIMPRO de edições de 2017
e 2018; a tabela do ano corrente não se aplicava. Outro usava a CBHPM 5ª
edição (2008) com deflator sobre porte e custo operacional.
**Regra que ficou:** extraia a **edição** junto com a tabela. Sem o arquivo
daquela edição, registre lacuna; não use a atual como aproximação sem
autorização escrita.
**Como detectar:** cláusula citando número de edição ou ano da tabela.

## L35 — Limiar de valor para autorização é de internação

**O que aconteceu:** limiares como "autorização para item acima de R$ 1.000"
foram aplicados ao ambulatório. O gestor corrigiu: no atendimento ambulatorial
(centro de infusão), **toda aplicação de medicamento exige autorização**,
mesmo barata; o limiar é de conta hospitalar.
**Regra que ficou:** leia a cláusula inteira (internação × ambulatório); na
dúvida, pergunte. Padrão ambulatorial: aplicação de medicamento com
autorização prévia.
**Como detectar:** limiar em R$ numa cláusula sobre materiais/medicamentos
"em internação" ou "conta hospitalar".

## L36 — Acréscimo de urgência não vale para atendimento eletivo

**O que aconteceu:** a regra da CBHPM de +30% em urgência/emergência (noite,
fim de semana) foi levantada como "receita a recuperar". A clínica atendia só
das 7h às 19h, ambulatorial e eletiva, inclusive fins de semana — o gatilho é o
**caráter** de urgência, não o dia. Não havia nada a cobrar.
**Regra que ficou:** antes de apontar receita perdida, confirme o gatilho da
regra com o perfil real da clínica.
**Como detectar:** "oportunidade" baseada só em horário/dia.

## L37 — Nem todo "convênio" é plano de saúde TISS

**O que aconteceu:** um convênio de desconto (o beneficiário paga com
desconto) e uma parceria de encaminhamento (sem guia nem glosa) estavam
cadastrados como planos; gerariam guia TISS e erro de envio.
**Regra que ficou:** pergunte "emite guia para uma operadora?". Se não, é
convênio de pagamento no ato/desconto, sem faturamento TISS.
**Como detectar:** "operadora" sem registro ANS; contrato de desconto.

## L38 — Documento na pasta errada; nome igual não é conteúdo igual

**O que aconteceu:** um edital estava arquivado na pasta de outro convênio; dois
arquivos de mesmo nome e tamanho parecido tinham conteúdos diferentes (um com
dezenas de linhas mais novas).
**Regra que ficou:** identifique o documento pelo **conteúdo** (partes,
cabeçalho, datas), não pelo nome ou pasta; compare por hash/diff antes de
tratar como duplicado.
**Como detectar:** partes do contrato não batem com a pasta; hashes diferentes.

## L39 — Lacuna honesta vale mais que valor inventado

**O que aconteceu:** coletas rasas usaram valores "modelo" de um convênio para
outros (valores idênticos em contratos diferentes = template). Onde faltava a
tabela ou a edição, o certo foi registrar a lacuna com o motivo.
**Regra que ficou:** sem fonte, **não** há valor: registre "falta X do contrato
Y" e pergunte. Valores iguais entre convênios diferentes = suspeita de cópia.
**Como detectar:** mesmo preço em vários convênios; valor sem ORIGEM.

## L40 — Intermediadora: regra geral + regra por subconvênio

**O que aconteceu:** dezenas de convênios eram faturados por uma entidade
intermediadora; a regra geral dela valia, mas cada subconvênio tinha
particularidades (tabelas, fatores, limiares, códigos próprios).
**Regra que ficou:** trate cada subconvênio como um convênio próprio, com régua
própria; nunca misture dados entre convênio direto e convênio via
intermediadora da mesma operadora.
**Como detectar:** mesma operadora aparecendo "direta" e "via entidade".
