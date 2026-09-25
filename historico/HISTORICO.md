# HISTÓRICO do kit

| Data | Versão | O que foi feito | Próximo passo |
|---|---|---|---|
| 2026-09-25 | 0.1.0 | Criação do kit a partir da experiência de implantação real, do manual oficial v2.3 e do Swagger de 25/09 (plano: `PLANO-2026-09-25.md`). | Primeira implantação-piloto com uma clínica usando o modelo; recolher lições para v0.2. |
| 2026-09-25 | 0.1.1 | Validação cruzada (19) + simulação de clínica (10) corrigidas; kit publicado na `main` e tornado público. | Piloto com a primeira clínica; reconfirmar 401×503 e os campos do Farol com chave real. |
| 2026-09-25 | 0.1.1 | Kit tornado **público** e `main` definida como branch padrão pelo Diretor (conferido: clone anônimo ok). | Piloto com a primeira clínica. |
| 2026-09-25 | 0.1.2 | Formatos reais da API confirmados com chave válida (só leitura) e incorporados ao kit; 503 reconfirmado. | Piloto; confirmar em homologação `fonte_id` = `fontePrecoCompraOptionsId` e a receita de item fora da conta. |
| 2026-09-25 | 0.2.0 | Manual passo a passo, frase 'Vamos implantar <clínica>' e ferramentas do repo-modelo. | Diretor cria o repo-modelo vazio; sessão do kit exporta o conteúdo; piloto com a 1ª clínica. |

## 2026-09-25 — v0.2.1 — passo a passo público no manual do Rabi + repo-modelo populado
- Página pública: https://www.rabisistemas.com.br/manual/implantacao/implantacao-com-ia.html (manualrabi D-34; 200 em produção).
- Kit aponta para ela (README, MANUAL-PASSO-A-PASSO, manual/07, README do modelo, README do repo-modelo).
- Repo-modelo `fmunizmcorp/implantarabi-modelo-clinica` populado por `exportar_modelo.py` (92 arquivos; `--checar` PASS).
- Próximo passo: piloto com a primeira clínica real ("Vamos implantar <Nome da Clínica>").
