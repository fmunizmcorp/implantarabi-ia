# Licenças das tabelas de referência

> **Fonte:** decisão do proprietário do kit (registrada em 25/09/2026) + sites oficiais da ANS e da ANVISA · **Conferido em:** 2026-09-25
> **Vale para:** todo o conteúdo de `referencias/` · **Kit:** v0.1.0

## Decisão do proprietário do kit (verbatim)

> "o meu material sera usado apenas para referncia de cadastro entao nao tem
> problema mas se o cliente quiser usar o dele de a opção dele dizer onde
> estarao os arquvivos atualizados dele sempre."

Consequências práticas:

1. As tabelas ficam no kit **só como referência de cadastro**: nomenclatura,
   apresentação e códigos de produtos e serviços.
2. **Preço é apenas indicativo.** A edição do kit pode estar desatualizada.
3. A clínica **pode usar as tabelas dela**: ela informa onde ficam os arquivos
   atualizados em `config/referencias-da-clinica.md` (repo da clínica). As
   tabelas dela **prevalecem** sobre as do kit.

## Situação de cada fonte

| Fonte | Quem publica | Situação | Uso permitido no kit |
|---|---|---|---|
| TUSS (terminologia, registros ANVISA, OPME) | ANS | **pública** | livre |
| TISS (XSD, domínios) | ANS | **pública** | livre |
| CMED (lista de preços de medicamentos) | ANVISA/CMED | **pública** | livre |
| Brasíndice | editora Brasíndice | **licenciada** (assinatura) | só referência de nomenclatura/códigos, por decisão do proprietário |
| SIMPRO | editora SIMPRO | **licenciada** (assinatura) | só referência de nomenclatura/códigos, por decisão do proprietário; os dados vieram de coleta de portal de operadora que publica a tabela SIMPRO |
| CBHPM 5ª edição (2008) | AMB | **licenciada** (publicação) | só o CSV de códigos/portes; o livro em PDF **não** está no kit |

## Risco (registrado)

- Brasíndice, SIMPRO e CBHPM são **obras protegidas**. Se o repositório do kit
  ficar **público**, essas tabelas ficam expostas a qualquer pessoa. O
  proprietário do kit conhece e aceitou esse risco.
- **25/09/2026:** o proprietário decidiu tornar o kit **público** (para que
  qualquer clínica baixe o kit sem convite). A decisão está registrada no
  maestro (`requisitos/raw/2026-09-25b-kit-implantacao-rabi-via-ia.md`).
- Se um titular de direitos pedir a retirada, remova as pastas `brasindice/`,
  `simpro/` e `cbhpm/` e o registro delas no `manifest.json` (as ferramentas
  continuam funcionando com TUSS, CMED e as tabelas da clínica).
- **Para preço**, a clínica deve usar a **própria edição licenciada** (ou o
  contrato do convênio), nunca o preço do kit como verdade.

## O que nunca entra aqui

- Tabela de preço **de uma clínica real** ou de um contrato real.
- Chave, senha ou qualquer dado pessoal.
- O nome de quem forneceu a coleta (o kit diz apenas "coleta de portal de
  operadora que publica a tabela SIMPRO").
