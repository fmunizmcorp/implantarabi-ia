# Índice — conhecimento/licoes-aprendidas

> **Fonte:** implantação real anterior feita sem kit + sessões de IA do mantenedor (ver [origem.md](origem.md)) · **Conferido em:** 2026-09-25
> **Vale para:** todas as sessões da IA implantadora · **Kit:** v0.1.0

Erros que já custaram caro, transformados em regra. Formato de cada lição:
**título · o que aconteceu (genérico) · regra que ficou · como detectar**.
Leia o arquivo do tema antes de trabalhar nele; na abertura de sessão, passe os
títulos de todos.

| Arquivo | Lições | Quando ler |
|---|---|---|
| [origem.md](origem.md) | De onde vêm as lições e como contribuir | Uma vez |
| [api.md](api.md) | L01–L10: chave 503/401, PUT sobrescreve, omissão limpa campos do convênio, paginação a partir de 1, envelopes, centavos, o que a API não cobre, rotas proibidas sem ordem, alcance da chave, contagem API × tela | Antes de chamar a API; ao montar um PUT |
| [dados-e-leitura.md](dados-e-leitura.md) | L11–L19: 200 vazio ≠ nada, "sucesso" ≠ gravado, campo errado, nome e ativo antes do ID, "agora" × "para sempre", linha 🔒 ≠ convênio, JSON fora do contexto, fonte primária, dado de entrada ausente | Antes de concluir qualquer coisa a partir de uma leitura |
| [cadastro-e-precos.md](cadastro-e-precos.md) | L20–L30: 0,01 proibido, regra com data, somar itens, referência circular, medicamento não faturado, política de preço para todos os tipos, pacote, serviço desligado não agenda, convênios irmãos, campo moeda na tela, medir antes de mudança em massa | Sprints de produtos, serviços e convênios |
| [contratos.md](contratos.md) | L31–L40: proposta ≠ aditivo, evidência tripla, OCR em 2 passadas, edições congeladas, limiar de autorização é de internação, urgência × eletivo, convênio de desconto, documento na pasta errada, lacuna honesta, intermediadora | Antes de analisar contratos |
| [comunicacao-com-o-usuario.md](comunicacao-com-o-usuario.md) | L41–L48: usuário leigo, "ok" ambíguo, condição vira checagem, não redescobrir, medir antes de contradizer, recomendação × regra decidida, caminho completo, status honesto | Sempre que for falar com o usuário |
| [processo-e-sessoes.md](processo-e-sessoes.md) | L49–L61: estado em arquivo, commit+push no dia, repo privado, ritual completo com o que não mudou, um convênio por vez, ler o obrigatório, script × IA, arquivo grande, confirmar o alvo, sessão curta, processo em segundo plano, verificador no fim, vigência de dado | Abertura e fechamento de sessão |

Relacionados: [../sistema-rabi/00-INDICE.md](../sistema-rabi/00-INDICE.md) ·
[../negocio-clinica/00-INDICE.md](../negocio-clinica/00-INDICE.md) ·
[../precos-e-conversao/00-INDICE.md](../precos-e-conversao/00-INDICE.md) ·
[../api-externa/00-INDICE.md](../api-externa/00-INDICE.md)
