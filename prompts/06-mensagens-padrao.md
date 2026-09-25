# 06 — Mensagens-padrão (textos prontos para o usuário)

> **Fonte:** kit implantarabi-ia; [metodologia/conversa-com-o-usuario.md](../metodologia/conversa-com-o-usuario.md) · **Conferido em:** 2026-09-25
> **Vale para:** kit v0.1.0 · **Kit:** v0.1.0

Regras de todas: português simples, uma tela, **uma pergunta no fim** (no
máximo), sigla explicada na 1ª vez, nome por extenso antes do número/ID, sem
JSON, sem chave, sem senha (exceto a senha inicial entregue à própria pessoa).

## 1. Pedido único de documentos (S00)
Lista completa e o porquê de cada item: [metodologia/lista-unica-de-documentos.md](../metodologia/lista-unica-de-documentos.md).

```
Para configurar o Rabi da <clínica> eu preciso dos documentos abaixo. Pode
mandar do jeito que tiver (PDF, foto, planilha, print, e-mail encaminhado).
Não precisa organizar: eu leio, separo e confiro com você.

<lista agrupada por assunto, com 1 linha "para que serve" em cada item>

O que faltar eu pergunto depois, uma coisa de cada vez. Sem documento o
prazo não anda, porque eu não invento valor.
Pode começar pelo que for mais fácil. Por onde prefere começar?
```

## 2. Daily de 5 linhas
```
1. Feito desde a última daily: …
2. Faço hoje: …
3. Travado / por quê: … (ou "nada")
4. Preciso de você: … (uma coisa só, ou "nada")
5. Evolução: Sxx aa% → bb% · geral cc%
```

## 3. Review de sprint
```
Review da Sxx — <tema> · <data>
O que ficou pronto: <contagens: 3 locais, 12 taxas…>
Demonstração (foto depois): <1 a 3 itens como aparecem no Rabi>
Definição de pronto: <item — ok/não ok>
Ficou pendente: <item — motivo — o que falta>
Riscos: <se houver>
Próxima sprint: Syy — <tema> — precisa de: <documento/decisão>
Posso dar a Sxx como concluída?
```

## 4. Confirmação de dado extraído
```
No <documento> (página <n>) encontrei:
  <campo>: <valor>
Está certo? (sim / não, o certo é …)
```

## 5. Sugestão de padrão (quando o documento não traz e há um padrão razoável)
```
Não encontrei <o quê> nos documentos. Posso usar o padrão "<sugestão>"
(ex.: "Consultório 1", "Depósito Principal"). Isso só afeta <efeito prático>
e dá para trocar depois. Uso o padrão?
```

## 6. Aviso de lacuna
```
Falta <o quê> para <sprint/convênio>.
Sem isso: <efeito prático — ex.: "nenhum serviço do Convênio A terá preço">.
<pergunta objetiva — uma só>
```
(Registrar em `pendencias/LACUNAS.md`.)

## 7. Prévia antes de gravar
```
Vou gravar no Rabi (Sxx — <cadastro>):
| item | campo | hoje | vai ficar | por quê (origem) |
Nada muda além disso. Posso gravar?
```

## 8. Resultado depois de gravar
```
Gravado e conferido: <n> itens. Antes → depois: <resumo>.
Prova: provas/Sxx/<cadastro>/<data>/. Não confirmado: <n> (motivo).
Sxx: aa% → bb%.
```

## 9. Aviso de repositório público
```
⚠️ Atenção: este repositório parece estar PÚBLICO na internet. Ele guarda a
chave da API do Rabi e senhas em texto claro. Enquanto ele não for privado,
eu não envio nada para o GitHub (não faço push). Não apaguei nem escondi nada.
Para resolver: GitHub → este repositório → Settings → "Change visibility" →
Private. Depois, peça à Rabi uma chave nova e troque as senhas registradas,
porque as atuais podem ter sido vistas. Me avise quando estiver privado.
```

## 10. Aviso de chave vencendo ou inválida
```
A chave da API do Rabi vence em <data> (faltam <n> dias). A renovação é feita
pela Rabi Sistemas (não há autoatendimento). Peça uma chave nova e, quando
chegar, troque o segredo RABI_API_KEY. Até lá sigo normalmente.
```
Chave inválida (401 ou 503):
```
O Rabi recusou a chave da API (ela pode ter sido revogada ou vencido). Parei
as gravações — nada ficou pela metade. Peça uma chave nova à Rabi Sistemas e
atualize o segredo RABI_API_KEY. Enquanto isso, posso organizar documentos.
```

## 11. Entrega de login ao colaborador (S09/S14)
```
Seu acesso ao Rabi foi criado.
Endereço: https://app.rabisistemas.com.br
Login: <e-mail>
Senha inicial: <senha> — o sistema vai pedir para você trocar no 1º acesso.
```
(Entregar só à própria pessoa ou ao implantador; registrar em `credenciais/CREDENCIAIS.md`.)
