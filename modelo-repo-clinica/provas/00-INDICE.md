# provas · <NOME_DA_CLINICA>

> Prova de **toda** gravação no Rabi (ritual de 5 passos). Sem prova, não está feito.

## Convenção de pastas

```
provas/Sxx/<cadastro>/AAAAMMDD-HHMM/
    antes.json      GET antes de gravar (status 200 e bytes > 0 conferidos)
    previa.md       tabela mostrada ao usuário (item · campo · de → para · por quê · origem)
    resposta.json   status HTTP + corpo cru da gravação
    depois.json     GET depois de gravar
    diff.txt        diferença campo a campo (antes × depois)
```

Exemplos: `provas/S05/taxas/20261002-1030/`, `provas/S10/convenio-a/20261006-1415/`.
Outras: `provas/S00/foto-inicial/…` (foto de todas as áreas), `provas/regressao/…`
(agente `auditor-regressao`), `provas/S11/<slug>/…/conferencia.md` (agente `conferente-precos`),
`provas/atualizacao/<assunto>/…` (modo Atualização), `provas/diagnostico/<assunto>/…` (modo Diagnóstico, só leitura).

Gerar com `python3 .kit/ferramentas/rabi_api/foto.py`.

## Regras
- **Sem PII:** nada de nome, CPF, nascimento ou prontuário de paciente. Provas de
  pacientes (S13) guardam só IDs internos e contagens.
- **Sem credencial:** nunca a chave `rbk_` nem senha em prova.
- Não relido depois = **NÃO CONFIRMADO** (escrito assim no log da sprint).
- JSON grande: guarde o arquivo, mas mostre ao usuário só o resumo.

| Sprint | Pastas de prova |
|---|---|
| (vazio) | |
