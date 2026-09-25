# Ingestão de documentos — do arquivo do cliente ao dado com origem

> **Fonte:** plano de implantação em sprints (Sprint 0, Anexos B e C) + aprendizados de OCR e extração em implantação real · **Conferido em:** 2026-09-25
> **Vale para:** toda sessão de clínica · **Kit:** v0.1.0

## Princípios

1. **Qualquer formato é aceito.** PDF com texto, PDF escaneado, foto de papel,
   print, Excel, CSV, Word, exportação de outro sistema, e-mail colado.
2. **O original nunca é alterado.** Vai para `documentos-do-cliente/` como
   chegou, sem renomear. Trabalho se faz em cópias/extrações.
3. **Todo dado tem origem.** Documento + página + linha (ou célula). Sem origem,
   não entra na prévia.
4. **Valor sem documento = pendência**, não chute.
5. **O terminal processa, o contexto recebe o resumo.** Documento grande não é
   colado inteiro na conversa (ver [agentes-e-produtividade.md](agentes-e-produtividade.md)).

## Passo 1 — Inventário (com hash)

Para cada arquivo recebido, uma linha em `documentos-do-cliente/inventario.md`:

| Campo | Exemplo |
|---|---|
| nº | 007 |
| arquivo (caminho completo no repo) | `documentos-do-cliente/2026-10-02/Tabela Convenio A 2026.pdf` |
| recebido em / de quem | 02/10/2026, implantador |
| tipo e tamanho | PDF escaneado, 14 páginas, 3,2 MB |
| hash SHA-256 (8 primeiros) | `4f1c9a2e` |
| códigos da lista única que cobre | CV-2, CV-3 |
| sprint(s) que destrava | S10b |
| legibilidade | boa / parcial (pág. 9 ilegível) / ruim |
| status | recebido → extraído → conferido |

O hash evita processar o mesmo arquivo duas vezes quando o cliente reenvia com
outro nome. A ferramenta `ferramentas/ingestao/inventario.py` do kit calcula
hash, tipo e páginas e aponta PDFs sem texto (candidatos a OCR).

## Passo 2 — Extração por tipo de arquivo

| Tipo | Como extrair | Cuidados |
|---|---|---|
| PDF com texto | extração de texto por página (ferramenta de PDF) | tabelas quebram colunas: confira totais |
| PDF escaneado / foto | **OCR** (Tesseract, português, 300 dpi) | valores em célula clara falham: 2ª passada a 600 dpi e recorte da coluna de valor com mais contraste recupera a maior parte; o que continuar ilegível vira pendência |
| Excel / CSV | leitura por script (colunas e linhas) | aba escondida, célula mesclada, número salvo como texto, vírgula × ponto |
| Word | extração de texto e tabelas | numeração de cláusulas some; guarde a página |
| Exportação de outro sistema | CSV/planilha: mapear colunas → campos (ver abaixo) | códigos internos do outro sistema **não** são IDs do Rabi |
| Print de tela | OCR + leitura visual | confirmar com o usuário o que ficou ambíguo |

Numa implantação real, a maior parte dos contratos chegou **escaneada sem
texto** — o OCR é o primeiro passo, não o último.

## Passo 3 — Ficha de extração por documento

Para cada documento, um arquivo em `documentos-do-cliente/fichas/<nº>-<nome-curto>.md`:

```
# Ficha 007 — Tabela Convênio A 2026
Origem: documentos-do-cliente/2026-10-02/Tabela Convenio A 2026.pdf (sha 4f1c9a2e)
Cobre: CV-2, CV-3 · Sprint: S10b · Extraído em: 2026-10-02 · Método: OCR 300 dpi + 2ª passada 600 dpi

| dado | valor | página | linha/célula | confiança | observação |
|---|---|---|---|---|---|
| Consulta eletiva (TUSS 10101012) | 120,00 | 2 | L14 | alta | |
| Taxa de sala | 45,00 | 3 | L2 | média | OCR leu "4S,00"; conferido visualmente |
| Materiais | Brasíndice PF + 10% | 5 | cláusula 7.2 | alta | vira política por tipo de produto |
| Pág. 9 | — | 9 | — | ilegível | pendência L-12 |
```

- **Confiança:** alta (texto limpo), média (OCR conferido), baixa (inferido ou
  borrado — não entra sem confirmação).
- A ficha é a **única** fonte que a prévia pode citar como origem.

## Passo 4 — Mapear documento → dados → sprint

Depois da ficha, os dados vão para os arquivos normalizados do repo da clínica
(`dados/<área>/...`, ex.: `dados/convenios/convenio-a/precos.csv` com a coluna
`ORIGEM` = "ficha 007, p. 2, L14"). O checklist da sprint muda o item de
`pendente` para `coletado`.

Um documento pode alimentar várias sprints (o contrato do convênio alimenta
S04, S10a e S10b). A ficha lista todas.

## Passo 5 — Documentos grandes: em lotes, com checkpoint no arquivo

- Documento com muitas páginas (tabela de 300 procedimentos, contrato de 80
  páginas) é processado **em lotes** (ex.: 20 páginas por vez).
- Depois de cada lote, grave na ficha: "processado até a página 40" + commit.
  Se a sessão cair ou o contexto encher, a próxima continua da página 41.
- Nunca carregue o documento inteiro no contexto. O script extrai para arquivo;
  a IA lê o resumo e as linhas com dúvida.
- Em implantação grande, vários documentos independentes podem ser extraídos
  em paralelo por subagentes (um por documento), cada um devolvendo só um
  resumo curto e gravando a ficha em arquivo.

## Contradições entre documentos

Quando dois documentos dizem coisas diferentes (contrato × aditivo, tabela 2025
× 2026, lista da recepção × lista do faturamento):

1. Mostre **os dois**, com origem de cada um.
2. Recomende qual vale e por quê (ex.: "o aditivo é mais recente e está
   assinado; a tabela solta não tem assinatura").
3. Pergunte ao usuário. Registre a decisão em `decisoes/DECISOES.md`.
4. Nunca escolha em silêncio.

Regra prática vivida: **faturamento real prova uso, não prova contrato.** Uma
especialidade ou item faturado há anos pode não estar no contrato assinado —
isso é bandeira para confirmar com a operadora, não confirmação.

Outra: **proposta comercial não é aditivo.** Só vale o documento assinado pelas
duas partes.

## Importação de sistemas anteriores (planilhas e CSV)

1. **Inventário** do arquivo exportado (SA-1, SA-3) como qualquer documento.
2. **Mapa de colunas** em `dados/migracao/mapa-colunas-<sistema>.md`:
   `coluna do arquivo → campo do Rabi → regra de normalização`.
   Ex.: `DT_NASC → dataDeNascimento → dd/mm/aaaa para aaaa-mm-dd`.
3. **Normalizar:** CPF/CNPJ só dígitos e com dígito verificador válido;
   telefone com DDD; CEP com 8 dígitos; nomes sem espaço duplo; datas ISO;
   valores com ponto decimal; UF no formato que cada rota pede (sigla em
   empresas; nome por extenso em operadoras e colaboradores).
4. **Deduplicar:** por CPF (pessoas), CNPJ (empresas, operadoras,
   fornecedores), nome normalizado + código (serviços, produtos). Duplicata
   vira lista para o usuário decidir — nunca descarte em silêncio.
5. **Comparar com o que já existe no Rabi** (foto da S00): o que casa não se
   cria de novo.
6. **Lotes de 50**, um de cada vez, com o ritual de carga. O primeiro item
   sozinho, provado, antes do primeiro lote.
7. Pacientes seguem as regras de LGPD da S13 (sem extrato no repo).

## Formulário de lacunas

Em `pendencias/LACUNAS.md`, uma linha por lacuna:

| # | Sprint | O que falta | Pergunta ao usuário (simples) | Se não vier, o que acontece | Status |
|---|---|---|---|---|---|
| L-01 | S10a | contrato do Convênio A | "Você tem o contrato assinado do Convênio A? Sem ele eu não tenho o prazo de glosa." | o convênio entra sem prazo e a clínica pode perder prazo de recurso | aberta |

- Na daily, cobre **só** as lacunas que travam a sprint da vez.
- Lacuna resolvida: status `resolvida em <data>`, com a origem do dado.
