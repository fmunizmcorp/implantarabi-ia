# INDICE — mapa de tudo no kit

> Regra: abra o índice da pasta e só então o arquivo de que precisa (`metodologia/politicas.md` §1).

## Comece por aqui
| Arquivo | Para quem |
|---|---|
| [README.md](README.md) | qualquer pessoa: o que é, papéis, como começar |
| [BOOTSTRAP.md](BOOTSTRAP.md) | toda sessão: as 6 leis e o ciclo da sessão |
| [conhecimento/00-ESSENCIAL.md](conhecimento/00-ESSENCIAL.md) | toda sessão: o mínimo de cor (importado no boot) |
| [prompts/00-COMO-COMECAR.md](prompts/00-COMO-COMECAR.md) | dono/implantador de uma clínica nova |

## Pastas
| Pasta | Conteúdo |
|---|---|
| [conhecimento/](conhecimento/00-INDICE.md) | preços e conversão (o coração) · API externa (268 operações) · Sistema Rabi · negócio de clínica/TISS · lições aprendidas |
| [metodologia/](metodologia/00-INDICE.md) | políticas · Scrum da implantação · ritual de carga · conversa com o usuário · ingestão de documentos · modos de sessão · agentes e produtividade · lista única de documentos |
| [sprints/](sprints/00-INDICE.md) | S00 preparação · S01–S16 = etapas 1–16 do guia oficial · S17 estabilização (S10a/S10b: convênio) |
| [prompts/](prompts/00-INDICE.md) | abertura de sessão · modos implantação / atualização / convênio / diagnóstico · mensagens-padrão · coordenação multi-sessão |
| [ferramentas/](ferramentas/00-INDICE.md) | Python: cliente da API, motor de conversão, carga com ritual, fila de perguntas, painel, importador, referências, ingestão, kit |
| [referencias/](referencias/00-INDICE.md) | TUSS, CMED, Brasíndice, SIMPRO, CBHPM, domínios TISS — normalizados e fatiados · [LICENCAS.md](referencias/LICENCAS.md) |
| [modelo-repo-clinica/](modelo-repo-clinica/README.md) | o que é copiado para o repo privado de cada clínica |
| [historico/](historico/00-INDICE.md) | histórico do kit e plano de origem |
| `.claude/` | agentes (extrator-documentos, conferente-precos, auditor-regressao, consolidador, validador-cruzado), skills (ritual-de-carga, configurar-convenio, enriquecer-produtos), comandos (/status, /proximo, /daily, /review) |

## Por situação
| Situação | Leia |
|---|---|
| Vou configurar um convênio | `sprints/S10b-convenio-abas-e-precos.md` → `conhecimento/precos-e-conversao/10-do-contrato-a-configuracao.md` → skill `configurar-convenio` |
| Recebi uma pilha de documentos | `metodologia/ingestao-de-documentos.md` → agente `extrator-documentos` |
| Preciso cadastrar produtos/medicamentos | `sprints/S06-produtos-catalogo.md` → skill `enriquecer-produtos` |
| A clínica pediu uma mudança depois do go-live | `prompts/03-modo-atualizacao.md` → agente `auditor-regressao` |
| A API respondeu algo estranho | `conhecimento/api-externa/convencoes.md` → `defeitos-conhecidos.md` |
| Valor saiu errado no orçamento/Farol | `conhecimento/precos-e-conversao/13-conferencia-e-diagnostico.md` |
