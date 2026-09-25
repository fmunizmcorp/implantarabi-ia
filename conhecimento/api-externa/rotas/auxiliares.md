# Rotas — Auxiliares (14 operações)

> **Fonte:** Swagger oficial https://api.rabisistemas.com.br/external-docs/ (snapshot `spec/openapi-2026-09-25.json`) · **Conferido em:** 2026-09-25
> **Vale para:** produção (Swagger publicado em 2026-09-25) · **Kit:** v0.1.0

> Arquivo **gerado** por `ferramentas/rabi_api/gerar_rotas.py` — não edite à mão; rode `python3 -m ferramentas.rabi_api.atualizar_spec` para atualizar. Toda rota pode responder também `401` (chave rejeitada), `403` (chave sem a permissão) e `503` (falha ao validar a chave) — ver [convenções](../convencoes.md) e [chave e token](../chave-e-token.md).

## Operações

- `GET /auxiliares/tipos-produto`
- `GET /auxiliares/tipos-codigo`
- `GET /auxiliares/tabelas-ans87`
- `GET /auxiliares/regimes-atendimento`
- `GET /auxiliares/tipos-servico`
- `GET /auxiliares/tipos-guia`
- `GET /auxiliares/tipos-taxa`
- `GET /auxiliares/unidades-medida`
- `GET /auxiliares/principios-ativos`
- `GET /auxiliares/sexos`
- `GET /auxiliares/estados-civis`
- `GET /auxiliares/conselhos-profissionais`
- `GET /auxiliares/unidades-federativas`
- `GET /auxiliares/tipos-atendimento`

### `GET /auxiliares/tipos-produto`

- **Permissão:** `auxiliar:read` · **Manual:** [op-get-auxiliares-tipos-produto](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-auxiliares-tipos-produto)
- **Resumo:** Listar tipos de produto

**Respostas:**
- `200` Lista — campos: `dados`; item de `dados`: `id`, `nome`

### `GET /auxiliares/tipos-codigo`

- **Permissão:** `auxiliar:read` · **Manual:** [op-get-auxiliares-tipos-codigo](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-auxiliares-tipos-codigo)
- **Resumo:** Listar tipos de código

**Respostas:**
- `200` Lista — campos: `dados`; item de `dados`: `id`, `nome`

### `GET /auxiliares/tabelas-ans87`

- **Permissão:** `auxiliar:read` · **Manual:** [op-get-auxiliares-tabelas-ans87](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-auxiliares-tabelas-ans87)
- **Resumo:** Listar tabelas de domínio ANS 87

**Respostas:**
- `200` Lista — campos: `dados`; item de `dados`: `id`, `codigo`, `descricao`

### `GET /auxiliares/regimes-atendimento`

- **Permissão:** `auxiliar:read` · **Manual:** [op-get-auxiliares-regimes-atendimento](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-auxiliares-regimes-atendimento)
- **Resumo:** Listar regimes de atendimento

**Respostas:**
- `200` Lista — campos: `dados`; item de `dados`: `id`, `codigo`, `nome`

### `GET /auxiliares/tipos-servico`

- **Permissão:** `auxiliar:read` · **Manual:** [op-get-auxiliares-tipos-servico](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-auxiliares-tipos-servico)
- **Resumo:** Listar tipos de serviço

**Respostas:**
- `200` Lista — campos: `dados`; item de `dados`: `id`, `nome`

### `GET /auxiliares/tipos-guia`

- **Permissão:** `auxiliar:read` · **Manual:** [op-get-auxiliares-tipos-guia](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-auxiliares-tipos-guia)
- **Resumo:** Listar tipos de guia

**Respostas:**
- `200` Lista — campos: `dados`; item de `dados`: `id`, `nome`

### `GET /auxiliares/tipos-taxa`

- **Permissão:** `auxiliar:read` · **Manual:** [op-get-auxiliares-tipos-taxa](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-auxiliares-tipos-taxa)
- **Resumo:** Listar tipos de taxa

**Respostas:**
- `200` Lista — campos: `dados`; item de `dados`: `id`, `nome`

### `GET /auxiliares/unidades-medida`

- **Permissão:** `auxiliar:read` · **Manual:** [op-get-auxiliares-unidades-medida](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-auxiliares-unidades-medida)
- **Resumo:** Listar unidades de medida

**Respostas:**
- `200` Lista — campos: `dados`; item de `dados`: `id`, `codigo`, `termo`, `descricao`

### `GET /auxiliares/principios-ativos`

- **Permissão:** `auxiliar:read` · **Manual:** [op-get-auxiliares-principios-ativos](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-auxiliares-principios-ativos)
- **Resumo:** Listar princípios ativos

**Respostas:**
- `200` Lista — campos: `dados`; item de `dados`: `id`, `nome`

### `GET /auxiliares/sexos`

- **Permissão:** `auxiliar:read` · **Manual:** [op-get-auxiliares-sexos](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-auxiliares-sexos)
- **Resumo:** Listar sexos

**Respostas:**
- `200` Lista — campos: `dados`; item de `dados`: `id`, `codigo`, `descricao`

### `GET /auxiliares/estados-civis`

- **Permissão:** `auxiliar:read` · **Manual:** [op-get-auxiliares-estados-civis](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-auxiliares-estados-civis)
- **Resumo:** Listar estados civis

**Respostas:**
- `200` Lista — campos: `dados`; item de `dados`: `id`, `codigo`, `nome`

### `GET /auxiliares/conselhos-profissionais`

- **Permissão:** `auxiliar:read` · **Manual:** [op-get-auxiliares-conselhos-profissionais](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-auxiliares-conselhos-profissionais)
- **Resumo:** Listar conselhos profissionais

**Respostas:**
- `200` Lista — campos: `dados`; item de `dados`: `id`, `codigo`, `descricao`

### `GET /auxiliares/unidades-federativas`

- **Permissão:** `auxiliar:read` · **Manual:** [op-get-auxiliares-unidades-federativas](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-auxiliares-unidades-federativas)
- **Resumo:** Listar unidades federativas

**Respostas:**
- `200` Lista — campos: `dados`; item de `dados`: `id`, `codigo`, `descricao`, `uf`

### `GET /auxiliares/tipos-atendimento`

- **Permissão:** `auxiliar:read` · **Manual:** [op-get-auxiliares-tipos-atendimento](https://www.rabisistemas.com.br/manual/api-externa/referencia-cadastros.html#op-get-auxiliares-tipos-atendimento)
- **Resumo:** Listar tipos de atendimento

**Respostas:**
- `200` Lista — campos: `dados`; item de `dados`: `id`, `codigo`, `nome`
