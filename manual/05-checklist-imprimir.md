# Parte G — Checklist de 1 página (para imprimir)

> **Fonte:** este manual · **Conferido em:** 2026-09-25
> **Vale para:** produção em 25/09/2026 · **Kit:** v0.1.2

Clínica: ______________________  Repositório: rabi-implantacao-______________
Chave pedida em: ___/___/____  Vence em: ___/___/____  (pedir outra ___ dias antes)

## Preparação (uma vez) — detalhes na [Parte A](01-preparacao.md)

- [ ] A1 Conta GitHub da clínica + Claude com acesso a claude.ai/code
- [ ] A2 Chave da API pedida ao time Rabi (permissões de implantação) — **guardada, nunca no chat**
- [ ] A3 Repositório criado em github.com/fmunizmcorp/implantarabi-modelo-clinica/generate — **Private**
- [ ] A4 Settings → Actions → General → Workflow permissions → **Read and write** → Save
- [ ] A5 claude.ai/connect-github + app Claude instalado no repositório
- [ ] A6 Ambiente da clínica no Claude Code: `RABI_API_KEY` + rede liberada para `api.rabisistemas.com.br`

## Cada sessão — detalhes nas Partes [B](02-primeira-sessao.md) e [C](03-dia-a-dia-e-modos.md)

- [ ] Abrir claude.ai/code → **repositório da clínica** → **ambiente da clínica** → nova sessão
- [ ] Escrever: `Vamos implantar <Nome da Clínica>` (ou `continuar`)
- [ ] Ler o resumo: onde paramos · o que mudou · validade da chave
- [ ] Responder **uma pergunta por vez**: "sim" · "corrija para…" · "não sei — pergunte a…" · "não temos"
- [ ] Mandar documentos pedidos (anexo na conversa ou Upload no GitHub)
- [ ] Ler a **prévia** (de → para) e responder **"pode gravar"** só se estiver certo
- [ ] Conferir a **foto depois**
- [ ] Ao parar: "vamos parar por hoje" — conferir no GitHub que o `ESTADO.md` foi atualizado

## Outros modos — frases

- Atualização: `atualizar configuração: <o que mudou e a partir de quando>`
- Convênio: `convênio: configurar <nome do convênio>`
- Diagnóstico (não grava nada): `diagnóstico: <a dúvida>`

## Se der problema — [Parte E](04-problemas-e-seguranca.md)

Chave 503/401 → chave nova + trocar no ambiente · Repo público → Settings →
Change visibility → Private · Kit não baixou → sessão nova / ZIP · Actions
vermelho → A4 + Re-run · Trabalho sumiu → ver branch `claude/...`
