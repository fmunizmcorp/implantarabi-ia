# 03 — Modo Atualização (mudar configuração que já existe)

> **Fonte:** kit implantarabi-ia; experiência de implantação real (regressões por sobrescrita e alteração em massa) · **Conferido em:** 2026-09-25
> **Vale para:** produção · **Kit:** v0.1.0

Use quando a clínica **já opera** no Rabi e quer mudar algo: novo serviço,
novo profissional, preço, taxa, parâmetro, permissão, reajuste de convênio
(reajuste de convênio: use [04-modo-convenio.md](04-modo-convenio.md)).

## Passos
1. **Entenda o pedido** e salve a mensagem verbatim em `historico/requisitos/raw/`.
   Repita em 1 linha o que entendeu e o **efeito prático** esperado. Confirme.
2. **Foto da área** (GET de tudo que a mudança toca, paginando até
   `totalPages`, conferindo **linhas lidas = total**) em
   `provas/atualizacao/<assunto>/AAAAMMDD-HHMM/antes.json`.
3. **Análise de impacto** — antes de propor:
   - quem mais usa o item (serviços compostos que contêm o produto/taxa;
     convênios que têm o serviço; colaboradores com a especialidade);
   - efeito no **Farol** dos convênios afetados (`/convenios/{id}/farol/itens`);
   - as **6 contagens de regressão** (agente `auditor-regressao`) dos convênios afetados;
   - se a mudança é no **catálogo** (serviço/produto/taxa), ela atinge **todos**
     os convênios de uma vez: diga isso com todas as letras e peça aprovação do **dono**.
4. **Prévia** em tabela (item · campo · de → para · por quê · quem é afetado).
5. **Aprovação** → **grava** pelo ritual de 5 passos (skill `ritual-de-carga`).
   PUT é **sobrescrita**: GET antes e reenviar o objeto completo, salvo as
   rotas que declaram upsert (abas do convênio e `/parametros/desconto`).
   `/parametros/financeiro` é **misto**: sempre reenvie `categoriaPagamentoId`
   e `centroDeCustoId` (omitidos viram null). Campo omitido pode ser **apagado**.
   Serviço/produto: o GET **não** é o corpo do PUT (nomes e formatos diferentes) —
   use `corpo_put_servico` / `corpo_put_produto` de `ferramentas/rabi_api/corpo_escrita.py`.
   Dados do convênio: o GET nem traz o que o PUT exige — monte o objeto da régua
   contratual + dicionário de IDs (ver `sprints/S10a`).
6. **Foto depois + diff**, Farol relido nos convênios afetados, contagens de
   regressão de novo (devem mudar **só** o que foi aprovado).
7. **Registro:** linha em `decisoes/DECISOES.md`, entrada no
   `historico/HISTORICO.md`, `ESTADO.md` (modo Atualização, próximo passo),
   commit + push. Mostre ao usuário o antes/depois em 3 linhas.

## Cuidados que já custaram caro
- `PUT /servicos/{id}` sem o objeto completo apagou composição de serviço (a
  aplicação perdeu itens). Sempre GET antes e converter com `corpo_escrita.py`.
- Alteração em massa feita fora da sessão (cópia de convênio, importação)
  aparece como muitas linhas do mesmo item com o mesmo `updatedAt`: investigue
  antes de "corrigir".
- Item **inativo** com o mesmo nome de um ativo: confira ativo/inativo e o
  **nome**, não só o ID.
