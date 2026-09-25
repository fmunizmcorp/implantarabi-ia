# 07 — Coordenação multi-sessão (implantações grandes)

> **Fonte:** experiência de implantação real (coordenadora + sessões de convênio, generalizado) · **Conferido em:** 2026-09-25
> **Vale para:** kit v0.1.0 · **Kit:** v0.1.0

Para clínica grande, rede ou muitos convênios, uma sessão só fica longa e cara.
Divida em **uma sessão coordenadora** + **uma sessão por convênio** (e, se
precisar, uma sessão de implantação para os cadastros gerais). Todas no
**mesmo repo da clínica**, cada uma na sua branch ou em horários diferentes.
Custo e produtividade: [metodologia/agentes-e-produtividade.md](../metodologia/agentes-e-produtividade.md).

```
              DONO / IMPLANTADOR
                    │ decide
                    ▼
          SESSÃO COORDENADORA
   (fila, contexto, conferência, fala com o dono)
        ├──► sessão do Convênio A   (04-modo-convenio)
        ├──► sessão do Convênio B   (04-modo-convenio)
        └──► sessão do Convênio C   (04-modo-convenio)
```

## A coordenadora
1. **Decide a fila** de convênios (maior faturamento e mais simples primeiro;
   o **Particular** antes de todos) e confirma com o dono.
2. **Prepara o pacote de contexto** de cada convênio em
   `dados/convenios/<slug>/`: nome e ID no Rabi, contrato e aditivos
   (nº do inventário), tabela, **modelo de cobrança** (pacote/conta aberta/misto
   e quais serviços são pacote), o que já foi feito, armadilhas específicas.
3. **Abre a sessão do convênio** com o prompt abaixo.
4. **Cobra** a daily de 5 linhas; **confere o relatório** antes de levar ao
   dono: toda linha de preço tem origem? ativo × inativo conferido? regra de
   pacote aplicada? nenhum 0,01? Farol lido e vermelhos explicados? provas
   existem? — **relatório sem prova volta**.
5. **Só ela** mexe no que é transversal (catálogo de serviço/produto/taxa,
   parâmetros, qualquer coisa que atinja mais de um convênio) — com decisão
   escrita do dono.
6. **Só ela** fala com o dono, em uma tela, com a decisão que precisa.
7. Registra: `ESTADO.md` (tabela de convênios), provas, `decisoes/DECISOES.md`.

## Prompt para abrir uma sessão de convênio
```
Você é a sessão do convênio <NOME> (ID <ID>) da clínica <CLÍNICA>. Siga o
CLAUDE.md deste repo e .kit/prompts/04-modo-convenio.md. Seu contexto está em
dados/convenios/<slug>/. Você fala com a sessão coordenadora (não com o dono).
Comece pelo Passo −1: diga se o convênio está NOVO, EM ANDAMENTO ou FECHADO,
com a prova. Não grave nada antes da aprovação.
```

## Matriz de permissões por tipo de sessão

| Ação | Coordenadora | Sessão de convênio | Sessão de implantação |
|---|---|---|---|
| Ler tudo (Rabi e repo) | ✅ | ✅ | ✅ |
| Catálogo (serviço, produto, taxa) | ✅ com decisão escrita do dono | ❌ | ✅ (é o trabalho dela, S05–S08) |
| Configurar **um** convênio | ✅ | ✅ só o dela | ✅ um de cada vez |
| Mais de um convênio ao mesmo tempo | ❌ (item a item, um por vez) | ❌ | ❌ |
| Criar login e senha inicial | ❌ | ❌ | ✅ (S09/S14) |
| Parâmetros, permissões, documentos | ✅ com aprovação | ❌ | ✅ (S14) |
| Pacientes (migração) | ❌ | ❌ | ✅ só com ordem escrita (S13) |
| NFS-e, dinheiro, estoque real, `DELETE`, `/bulk` sem prévia | só com ordem escrita | ❌ | só com ordem escrita |
| Falar com o dono | ✅ | ❌ (fala com a coordenadora) | ✅ (se não houver coordenadora) |
| Commit + push no repo da clínica | ✅ | ✅ (só os arquivos do convênio dela) | ✅ |

## Para não brigar pelo mesmo arquivo
- Cada sessão de convênio escreve só em `dados/convenios/<slug>/`,
  `provas/S10/<slug>/`, `provas/S11/<slug>/`.
- `ESTADO.md`, `decisoes/DECISOES.md` e `pendencias/` são atualizados **pela
  coordenadora** (as sessões de convênio relatam; ela registra).
- Antes de todo push: `git pull --rebase`. Conflito → pare e avise a coordenadora.
- **Um lote por vez por clínica** na API (senão 429): combine a vez pela coordenadora.

## O que é determinístico não precisa de IA
Foto, contagem, Farol, 6 contagens de regressão, varredura de `updatedAt`,
diff: são scripts (`.kit/ferramentas/`) e podem rodar sem sessão de IA. A IA
fica para julgamento (contrato, preço, classificação, proposta, relatório). A
gravação continua sempre com aprovação humana.
