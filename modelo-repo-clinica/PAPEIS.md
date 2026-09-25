# Papéis · <NOME_DA_CLINICA>

> Preencha na S00. A IA pergunta **uma coisa por vez** até completar.
> Tabela-base de papéis: `.kit/metodologia/politicas.md` (seção 7).

## Pessoas

| Papel | Nome | Contato (e-mail/telefone) | Observação |
|---|---|---|---|
| **Dono da clínica** (decide regra de negócio; dono da conta Claude, do GitHub e da chave `rbk_`) | | | |
| **Implantador** (entrega documentos, aprova prévias, confere resultados) | | | |
| Responsável pelo **faturamento/convênios** | | | |
| Responsável pelo **financeiro** | | | |
| Responsável pela **recepção/agenda** | | | |
| **Contato no Rabi** (suporte / chave da API) | | | |
| **Mantenedor do kit** | Rabi Sistemas | (repo do kit) | só ele altera o kit |

## Quem aprova o quê

| Assunto | Quem aprova | Como aprova (ex.: "pode gravar" no chat) |
|---|---|---|
| Gravação de cadastro no Rabi (S01–S09, S12–S14) | Implantador | "pode gravar" após a prévia |
| Preço e regra de convênio (S10–S11) | Dono (ou quem ele indicar por escrito) | "pode gravar" item a item |
| Criação de logins e senha inicial (S09/S14) | Implantador | lista aprovada |
| Migração de pacientes (S13) | Dono | ordem escrita em `decisoes/DECISOES.md` |
| Rotas proibidas (NFS-e, dinheiro, estoque real, DELETE, bulk) | Dono | **ordem escrita** em `decisoes/DECISOES.md` |
| Go-live (S16) | Dono | "pode ativar" após os 10 cenários aprovados |

## O que a IA pode e não pode
- **Pode:** ler o kit; ler e gravar no Rabi pela API **com aprovação**; gravar e
  fazer commit+push neste repo; criar logins de colaboradores e registrar a
  senha inicial em `credenciais/CREDENCIAIS.md`.
- **Não pode:** alterar o kit; chamar rota proibida sem ordem escrita; inventar
  dado; decidir regra de negócio; guardar dado de paciente em prova/relatório.
