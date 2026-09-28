# F002 — 400 "Erro ao processar a operação. Tente novamente em instantes." na leitura E na gravação da mesma área

- **Rotas:** qualquer (visto em GET /servicos/{id} e POST /servicos)
- **Status HTTP:** 400 | 500
- **Mensagem contém:** Erro ao processar a operação | Tente novamente em instantes
- **Causa:** hipótese forte, **não confirmada**: a clínica tem banco próprio no Rabi e a
  migração de uma atualização recente não foi aplicada nesse banco (a tabela não tem as
  colunas novas; qualquer leitura/gravação dela falha). Caso real: deploy do Rabi em
  28/09/2026 14:08 (colunas novas em `servico` — pagamento parcial) e, a partir dessa
  tarde, `GET /servicos/1` e `POST /servicos` com 400 numa clínica, enquanto em outra
  clínica as mesmas rotas respondiam 200.
- **Status:** **resolvido pelo suporte do Rabi em 28/09/2026** (correção de ambiente, informada pelo mantenedor; nenhuma mudança de código no rabi-api). A clínica confirma com `GET /<área>/{id}` = 200 antes de retomar.
- **Causa confirmada?** a correção foi de ambiente, o que confirma a hipótese na prática; o Rabi não publicou a causa exata
- **Origem:** implantação real (clínica anônima), 28/09/2026

## Como reconhecer (faça só leituras)
1. Uma leitura que **funcionava antes** agora dá 400 genérico (ex.: `GET /servicos/{id}` de um item existente).
2. A **lista** da mesma área ou **outras áreas** ainda respondem 200 (ex.: `GET /convenios`).
3. O corpo enviado não muda nada: com ou sem campos extras, o erro é o mesmo.
4. Coincide com uma atualização recente do Rabi (veja as "Novidades" do manual oficial).

Se os 4 batem, **não é o seu corpo**: é o ambiente da clínica no Rabi.

## O que fazer
1. **Pare** as gravações dessa área. Siga com sprints que não dependem dela.
2. Confirme que nada mudou (foto depois = foto antes) e registre as provas.
3. Mande ao dono a mensagem pronta para o suporte (abaixo) e registre em `pendencias/`.
4. Quando o Rabi responder, releia a área e só então retome. Informe o kit pelo canal
   de aprendizados (`enviar aprendizados`) se a causa for outra.

## Mensagem pronta para o suporte do Rabi
> Clínica <nome>, API externa em produção: desde <data/hora>, `GET /api/v1/integrations/<área>/<id>`
> e `POST /<área>` respondem 400 "Erro ao processar a operação". Leituras de outras áreas funcionam.
> Coincide com a atualização de <data/hora>. Podem conferir se a migração foi aplicada no banco
> desta clínica (migrate deploy)? As requisições e respostas exatas estão anexas.

## Se voltar a acontecer
Cada atualização do Rabi pode trazer mudanças no banco (a de 28/09 19:28 UTC trouxe duas, em
financeiro/DRE). Se, depois de uma atualização, **outra área** passar a responder o mesmo 400
genérico na leitura e na gravação, é o mesmo caso: pare, prove que nada mudou e mande a mensagem
pronta acima trocando a área e o horário.

## O que NÃO fazer
- Não trocar campos às cegas nem repetir várias vezes (não é o corpo).
- Não criar o cadastro por outro caminho "para contornar" sem o dono decidir.
