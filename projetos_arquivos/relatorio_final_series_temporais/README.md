# 🛢️ Produção de Petróleo no Brasil (2001-2025): Uma Análise de Séries Temporais

Este repositório consolida o Projeto Final desenvolvido para a disciplina de **Análise de Séries Temporais** do curso de Estatística da Universidade Federal do Ceará (UFC), sob a orientação da **Prof. Drª Jeniffer Johana Duarte Sanchez**.

O trabalho investiga a dinâmica macroeconômica da produção de petróleo brasileira ao longo de mais de duas décadas, respondendo à pergunta central: **"Existe um Ciclo Anual na Produção de Petróleo no Brasil?"**.

---

## 🎯 Objetivos do Projeto

A análise teve como objeto de estudo a série mensal do volume de petróleo produzido no Brasil (em $m^3$) entre Janeiro de 2001 e Maio de 2025. Os principais objetivos englobaram:
1. **Análise Exploratória e Visualização:** Mapear a evolução histórica, o crescimento ano a ano (YoY) e a variância mensal da produção.
2. **Detecção de Padrões:** Investigar, através de testes estatísticos formais, a presença de tendência estocástica/determinística e de sazonalidade rígida.
3. **Estabilização da Série:** Aplicar transformações matemáticas (Logaritmo Natural e Diferenciação) para controlar a variância explosiva e garantir a estacionariedade.
4. **Modelagem e Previsão:** Contrastar o desempenho preditivo de modelos da classe **SARIMA** (Metodologia Box-Jenkins) com modelos de Suavização Exponencial (**Holt-Winters**).

---

## 🛠️ Metodologia e Destaques Analíticos

O pipeline analítico foi inteiramente desenvolvido em **R**, mesclando o rigor estatístico com visualizações de alto nível (`ggplot2`). Os destaques incluem:

* **Estudo Sazonal Aprofundado:** Utilização de Gráficos de Violino combinados com Boxplots e análise de variância mensal com bandas de confiança para mapear o comportamento intra-anual da produção.
* **Diagnóstico Formal:** Validação de hipóteses através de uma bateria de testes: ADF e KPSS (Estacionariedade), Mann-Kendall (Tendência) e QS (Sazonalidade).
* **Ajuste Fino de Modelos (SARIMA):** Com base no decaimento das funções ACF e PACF da série transformada ($\Delta \ln(Y_t)$), foi estruturado um modelo SARIMA manual com parâmetros estrategicamente fixados em zero (`fixed`), garantindo alta parcimônia sem perda de capacidade explicativa.
* **Validação de Resíduos:** Verificação de ruído branco iterativa via Teste de Ljung-Box, Q-Q Plots e Testes de Normalidade (Shapiro-Wilk e Jarque-Bera).
* **Forecast Competitivo:** Geração de previsões sobre o conjunto de teste (Out-of-Sample), comparando diretamente a acurácia (RMSE, MAPE) do modelo SARIMA contra o método Holt-Winters Aditivo.

---

---

## 📖 Como Visualizar os Resultados

O repositório foi pensado tanto para o público técnico (estatísticos e cientistas de dados) quanto para o público de negócios.

+ 📊 Para uma visão executiva e visual dos insights:

     - 👉 **[Acesse os Slides da Apresentação (PDF)](./Apresentação_Petróleo_Séries_Temporais.pdf)**

+ 🔬 Para o aprofundamento matemático, equações e diagnóstico completo:

    - 👉 **[Leia o Relatório Técnico Final (PDF)](./Séries_Temporais_RELATÓRIO_FINAL.pdf)**

---

## 📂 Estrutura do Repositório

O projeto foi estruturado seguindo as melhores práticas de organização para Ciência de Dados, separando a base bruta, os códigos fonte, os elementos visuais e as apresentações executivas:

```text
├── dataset/
│   └── Produção Mensal de Petróleo no Brasil.xlsx  # Base histórica (2001-2025)
├── graphics/
│   └── [Gráficos exportados do R em alta resolução]
├── script/
│   └── script_relatorio_final_series_temporais.R                           # Rotina completa em R (EDA, Testes, Modelos e Previsão)
├── Séries_Temporais_RELATÓRIO_FINAL.pdf            # Relatório Técnico Oficial
├── Apresentação_Petróleo_Séries_Temporais.pdf      # Slides da apresentação final
└── README.md                                       # Este documento