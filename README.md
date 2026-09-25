# implantarabi-ia — Kit de Implantação do Sistema Rabi via IA

Kit para uma **sessão de IA (Claude)** implantar ou atualizar a configuração
do **Sistema Rabi** numa clínica pela **API externa**, sprint a sprint,
conversando **uma pergunta por vez** com quem entende da clínica e provando
cada gravação.

> Versão: veja `VERSION` · Mudanças: `CHANGELOG.md` · Índice de tudo: `INDICE.md`

## Como funciona (em uma figura)

```
 este repo (KIT, só leitura para as clínicas)          repo PRIVADO de cada clínica
 ┌──────────────────────────────────────────┐          ┌──────────────────────────────────┐
 │ conhecimento/  (Rabi, API, preços, TISS) │  .kit/   │ ESTADO.md  (onde parou)          │
 │ sprints/ S00–S17 (guia oficial 1:1)      │ ───────► │ sprints/   (checklist item a item)│
 │ metodologia/ · prompts/ · .claude/       │ (clonado │ dados/     (com origem)           │
 │ ferramentas/ (Python)                    │  na      │ documentos-do-cliente/ + inventário│
 │ referencias/ (TUSS, CMED, Brasíndice…)   │  sessão) │ provas/ · credenciais/ · histórico│
 │ modelo-repo-clinica/                     │          └───────────────┬──────────────────┘
 └──────────────────────────────────────────┘                          │ API externa (rbk_ da clínica)
                                                                        ▼
                                                               Sistema Rabi da clínica
```

## Papéis (separados)

| Papel | Quem | Responsabilidade |
|---|---|---|
| Mantenedor do kit | Rabi Sistemas | evolui este repo; nunca guarda dado de clínica aqui |
| Dono da clínica | a clínica | conta Claude, GitHub e chave `rbk_` próprios; decide regras de negócio |
| Implantador | da clínica, parceiro ou Rabi | entrega documentos, aprova prévias, confere resultados |
| IA implantadora | sessão Claude da clínica | todo o trabalho técnico, com aprovação antes de gravar |

## Começar uma clínica (3 passos)

1. Criar um repositório **privado** no GitHub da clínica (ex.: `rabi-implantacao-minhaclinica`).
2. Abrir uma sessão do Claude (web) nesse repositório e colar o texto de
   `prompts/00-COMO-COMECAR.md`. A sessão monta a estrutura a partir de `modelo-repo-clinica/`.
3. Gerar a chave da API no portal comercial do Rabi e seguir a sessão: ela se
   apresenta, mostra o plano e conduz tudo, uma pergunta por vez.

## Para o mantenedor

- Protocolo: `BOOTSTRAP.md` · Regras de escrita: `metodologia/politicas.md`
- Verificação (a CI roda o mesmo):
  ```bash
  python3 -m pytest ferramentas -q
  python3 ferramentas/kit/verificar_tamanhos.py
  python3 ferramentas/kit/verificar_links.py
  python3 ferramentas/kit/verificar_vazamento.py
  ```
- Atualizar a API: `python3 -m ferramentas.rabi_api.atualizar_spec`
