# De onde vêm estas lições

> **Fonte:** registros de sessões de uma implantação real anterior do Sistema Rabi e de outros projetos de IA do mantenedor do kit · **Conferido em:** 2026-09-25
> **Vale para:** todas as clínicas · **Kit:** v0.1.0

Antes deste kit existir, uma clínica de porte médio (ambulatorial, com centro
de infusão de medicamentos e dezenas de convênios, diretos e via entidade
intermediadora) foi implantada e mantida no Rabi **sem kit**: com o manual,
planilhas, a tela do sistema e várias sessões de IA abertas conforme a
necessidade, de maio a setembro de 2026.

Essas sessões acertaram muito — e erraram também. Cada erro custou tempo,
dinheiro ou confiança, e virou uma regra. As lições L01 a L61 são esse
aprendizado, **generalizado**:

- sem nome da clínica, de pessoas, de operadoras ou de convênios;
- sem IDs internos, preços ou contratos reais;
- números aparecem só quando ajudam a dar a dimensão (ex.: "12 linhas",
  "R$ 600 por atendimento") e não identificam ninguém.

Algumas lições (L12, L15, L50, L56 a L61) vêm de outros projetos de IA do
mesmo mantenedor, porque tratam do comportamento de sessões de IA em geral:
estado em arquivo, contexto, arquivos grandes, repositório no dia zero, fonte
primária acima de aviso.

## Como uma clínica contribui

Se a sua implantação ensinar algo que sirva a todas as clínicas:
1. registre em `historico/APRENDIZADOS.md` do repo da clínica;
2. sugira ao mantenedor do kit por issue **sem nenhum dado da clínica**, no
   formato: título · o que aconteceu (genérico) · regra que ficou · como
   detectar.
