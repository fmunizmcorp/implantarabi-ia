# Como atualizar as referências

> **Fonte:** `ferramentas/referencias/normalizar.py` · **Conferido em:** 2026-09-25
> **Vale para:** kit v0.1.0 e repos de clínica · **Kit:** v0.1.0

Há dois casos: o **mantenedor do kit** troca a edição do kit; ou a **clínica**
aponta as tabelas dela (que prevalecem).

## 1. Mantenedor: trocar por uma edição nova (no kit)

Rode o subcomando da fonte com o arquivo bruto novo. Ele **substitui** as fatias
do conjunto, refaz o `00-INDICE.md` e atualiza o `manifest.json`. Os brutos
**não** entram no kit.

Ordem: CMED primeiro (o Brasíndice usa a CMED para preencher o princípio ativo).

```bash
N="python3 ferramentas/referencias/normalizar.py"
# CMED (ANVISA): planilhas PMC e PMVG/PF da mesma data (xlsx precisa de openpyxl;
# sem ele, exporte para CSV e passe o CSV)
$N cmed --pmc CMED_PMC_AAAAMMDD.xlsx --pmvg CMED_PMVG_PF_AAAAMMDD.xlsx \
   --edicao AAAAMMDD --data AAAA-MM-DD --tuss-registros "REGISTROS ANVISA NA TUSS DE MEDICAMENTOS.xlsx"
# Brasíndice medicamentos: edição nova + (opcional) a anterior e o arquivo "Outros Fármacos"
$N brasindice-medicamentos --principal Brasindice_NNNN_Medicamentos.txt --edicao NNNN \
   --anterior Brasindice_MMMM_Medicamentos.txt \
   --complementar Brasindice_MMMM_MedicamentosFarmacos.txt --edicao-complementar MMMM
$N brasindice-materiais --principal Brasindice_NNNN_Materiais.txt --edicao NNNN
# SIMPRO (arquivo pipe com VIGENCIA_ATUAL "Desde dd/mm/aaaa R$ x,xxx"), um por tipo
$N simpro --tipo material --arquivo SIMPRO_MATERIAL.csv --edicao AAAA-MM-DD --data "AAAA-MM-DD (coleta)"
# TUSS (ANS)
$N tuss-historico --arquivo "Padrão TISS - Histórico da TUSS - AAAAMM.txt" --competencia AAAAMM
$N tuss-registros-anvisa --arquivo "REGISTROS ANVISA NA TUSS DE MEDICAMENTOS AAAAMM.xlsx" --competencia AAAAMM
$N tuss-opme --nomes-tecnicos "NOMES TÉCNICOS NA TUSS DE OPME AAAAMM.xlsx" \
   --fabricantes "MATERIAIS FABRICANTES NA TUSS DE OPME AAAAMM.xlsx" \
   --envio-individualizado "NOMES TECNICOS ENVIO INDIVIDUALIZADO NA TUSS DE OPME AAAAMM.xlsx" --competencia AAAAMM
# CBHPM (CSV de códigos/portes) e TISS (pasta dos XSD da versão)
$N cbhpm --arquivo CBHPM_PORTES_por_codigo_TUSS.csv
$N tiss --schemas pasta/dos/xsd --versao 4.03.00
```

Depois, confira (tudo tem que passar):

```bash
du -sh referencias                                     # alvo < 80 MB
find referencias -name '*.csv' -size +5M               # não pode listar nada
python3 -m pytest ferramentas/referencias -q
python3 ferramentas/referencias/buscar.py "dipirona 500 mg" --limite 3
```

Regras:

- **Só a edição mais recente** de cada tabela fica no kit.
- Se a edição nova vier com **layout diferente**, confira as colunas cruzando
  alguns EAN com a CMED antes de confiar (foi assim que se descobriu que o
  layout antigo documentado do Brasíndice tinha colunas trocadas).
- Se o total passar de 80 MB, **não use gzip** (a IA precisa de `grep`):
  descarte colunas sem uso e documente no índice do conjunto.
- Registre a troca em `CHANGELOG.md` e `historico/HISTORICO.md` do kit.

## 2. Clínica: usar as tabelas dela (prevalecem)

1. Pergunte ao cliente **se ele tem tabelas próprias** (assinatura Brasíndice/
   SIMPRO, CBHPM do contrato, tabela de operadora) e **onde ficam os arquivos
   atualizados** dele. Uma pergunta por vez.
2. Coloque os arquivos no repo **privado** da clínica (ex.:
   `dados/referencias/`) — CSV com cabeçalho, ou normalize com
   `normalizar.py --saida dados/referencias <subcomando> …` (gera fatias ≤ 4 MB,
   índice e `manifest.json`).
3. Preencha `config/referencias-da-clinica.md` (coluna "Onde está") com o
   caminho de cada tabela, a edição e a data.
4. Use sempre com `--referencias-clinica config/referencias-da-clinica.md`:

   ```bash
   python3 .kit/ferramentas/referencias/buscar.py "dipirona 500 mg" \
       --referencias-clinica config/referencias-da-clinica.md
   python3 .kit/ferramentas/referencias/enriquecer_produtos.py dados/produtos/produtos.csv \
       --referencias-clinica config/referencias-da-clinica.md
   ```

   O parâmetro aceita também uma pasta ou um CSV. Resultados da clínica ganham
   preferência e aparecem marcados como `clinica/…`.
5. Quando o cliente receber edição nova, **troque o arquivo** no mesmo caminho
   e atualize a edição/data no `config/referencias-da-clinica.md`.

CSV próprio simples é aceito: separador `;` `,` ou tab; colunas reconhecidas
`produto` (ou `nome`/`descricao`), `apresentacao`, `laboratorio`, `ean`,
`registro_anvisa`, `codigo_tuss`, `codigo_fonte`, `pf_total`, `pmc_total`,
`preco_ref`, `edicao`.
