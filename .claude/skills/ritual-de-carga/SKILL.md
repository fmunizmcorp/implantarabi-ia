---
name: ritual-de-carga
description: Ritual obrigatório de 5 passos para TODA gravação no Sistema Rabi pela API externa (foto antes → prévia → aprovação → grava → foto depois + diff), com commit e atualização do ESTADO. Use sempre que for criar, alterar ou inativar qualquer cadastro no Rabi.
---

# Skill: ritual de carga

Detalhe completo: `metodologia/ritual-de-carga.md`. Aqui está o essencial.

## Antes de começar
- A sprint está com DoR (definição de pronto para começar) cumprida? (ver `sprints/Sxx-<nome>.md` do kit)
- O item está **ativo**? Você sabe o **nome** dele, não só o ID?
- A rota está liberada? Rotas de NFS-e, financeiro com dinheiro, estoque real,
  `DELETE` e `/bulk` sem prévia exigem **ordem escrita** (registrada em
  `decisoes/DECISOES.md`).

## Os 5 passos
| # | Passo | Como | Prova |
|---|---|---|---|
| 1 | **Foto antes** | `python3 ferramentas/rabi_api/foto.py antes …` (GET, confere status 200 e bytes > 0) | `provas/Sxx/<cadastro>/AAAAMMDD-HHMM/antes.json` |
| 2 | **Prévia** | tabela em português: item · campo · de → para · por quê · origem. Sem JSON. | na conversa + `previa.md` |
| 3 | **Aprovação** | "pode gravar" do usuário. Item a item no que é novo; em bloco só depois que o 1º item do bloco saiu certo | frase registrada no log da sprint |
| 4 | **Grava** | PUT = sobrescrita: **GET antes e reenviar o objeto completo**, salvo rotas que declaram upsert (abas do convênio, `/parametros/desconto`, `/parametros/financeiro`). `207` = falha parcial: reenviar só `ERRO`/`NAO_PROCESSADO`. `429`: esperar. `401`/`503`: chave — parar, sem laço de retry | `resposta.json` (status + corpo cru) |
| 5 | **Foto depois + diff** | `python3 ferramentas/rabi_api/foto.py depois …` e diff campo a campo. Não relido = **NÃO CONFIRMADO** | `depois.json`, `diff.txt` |

## Depois dos 5 passos
1. Atualize a linha do item em `sprints/Sxx.md` (repo da clínica): status `gravado` → `conferido`, coluna prova com o caminho.
2. Atualize `ESTADO.md` (% da sprint, próximo passo concreto, última sessão).
3. `git add -A && git commit -m "Sxx: <o que> (<n>) + provas" && git push`.
4. Mostre ao usuário a evolução (1 linha: "S03 70% → 80%").

## Nunca
- 0,01 como marcador; valor sem documento; dado de paciente em prova;
  chave em prova; gravar em item inativo sem perceber; gravar dois convênios ao mesmo tempo.
