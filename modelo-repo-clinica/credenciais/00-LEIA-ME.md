# credenciais · <NOME_DA_CLINICA> — LEIA ANTES

> ⚠️ **Este repositório TEM DE SER PRIVADO.** As credenciais ficam aqui em
> **texto claro**, por decisão do proprietário, para que qualquer sessão
> continue o trabalho sem que ninguém precise procurar ou recriar nada.

## Regras (valem para qualquer pessoa ou sessão de IA)
1. **Nunca** mascarar, apagar ou trocar credencial por placeholder. Chave velha
   não se apaga: vai para o histórico com a situação (revogada, vencida).
2. **Nunca** copiar credencial para issue, prova, relatório, daily, review,
   mensagem pública ou para o kit.
3. O token da API do Rabi (`rbt_` recomendado ou `rbk_`) deve estar **também** no segredo de ambiente
   `RABI_API_KEY` do Claude web (preferido pelas ferramentas). O arquivo
   `rabi-api-externa.md` é o registro para consulta humana.
4. Se o repositório ficar **público**: avise o dono por escrito, não faça push,
   e peça a troca (rotação) de todas as credenciais daqui.
5. Toda credencial nova: **data**, **quem entregou**, **onde é usada**, **como trocar**.

| Arquivo | O que tem |
|---|---|
| [CREDENCIAIS.md](CREDENCIAIS.md) | todas as credenciais por serviço e ambiente (Rabi web, usuários criados, GitHub, outros) |
| [rabi-api-externa.md](rabi-api-externa.md) | o token da API externa — `rbt_` da clínica (recomendado) ou chave `rbk_` do time Rabi —, validade, permissões testadas e histórico |
