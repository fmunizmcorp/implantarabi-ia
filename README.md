# implantarabi-ia — Kit de Implantação do Sistema Rabi via IA

Kit para uma **sessão de IA (Claude)** implantar ou atualizar a configuração
do **Sistema Rabi** numa clínica pela **API externa**, sprint a sprint,
conversando **uma pergunta por vez** com quem entende da clínica e provando
cada gravação.

> 🌐 **Passo a passo do implantador (página pública no manual do Rabi):** https://www.rabisistemas.com.br/manual/implantacao/implantacao-com-ia.html

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

## Começar uma clínica

Guia completo, clique a clique, para o implantador leigo:
**[MANUAL-PASSO-A-PASSO.md](MANUAL-PASSO-A-PASSO.md)**. Em resumo:

1. Criar o repositório **privado** da clínica pelo modelo:
   https://github.com/fmunizmcorp/implantarabi-modelo-clinica/generate
   (*Use this template*, marcar **Private**).
2. Pedir a chave da API ao time Rabi e guardá-la no **ambiente da clínica** do
   Claude Code na web (variável `RABI_API_KEY`; nunca no chat).
3. Abrir uma sessão no Claude Code na web nesse repositório e escrever:
   `Vamos implantar <Nome da Clínica>`. A IA personaliza o repositório,
   confere tudo e conduz a implantação, uma pergunta por vez.

## Para o mantenedor

- Protocolo: `BOOTSTRAP.md` · Regras de escrita: `metodologia/politicas.md`
- Verificação (a CI roda o mesmo):
  ```bash
  python3 -m pytest ferramentas -q
  python3 ferramentas/kit/verificar_tamanhos.py
  python3 ferramentas/kit/verificar_links.py
  python3 ferramentas/kit/verificar_vazamento.py
  python3 ferramentas/kit/sincronizar_claude_modelo.py --checar
  python3 ferramentas/kit/gerar_sprints_modelo.py --checar
  ```
- Repositório-modelo (GitHub Template): `ferramentas/kit/exportar_modelo.py`;
  publicação automática pelo workflow `publicar-modelo.yml` com o secret
  `MODELO_PUSH_TOKEN` ([manual/06-mantenedor.md](manual/06-mantenedor.md)).
- Atualizar a API: `python3 ferramentas/rabi_api/atualizar_spec.py`
