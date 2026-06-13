# ==============================================================================
# ANÁLISE DE SÉRIES TEMPORAIS: Produção Mensal de Petróleo no Brasil
# Relatório Final
# Autor: Douglas Chaves Moura
# ==============================================================================

# 1. PACOTES E CONFIGURAÇÕES GLOBAIS -------------------------------------------

suppressPackageStartupMessages({
  library(readxl)        # Leitura de arquivos Excel
  library(fpp2)          # Dados e funções de forecast
  library(forecast)      # Funções principais para modelagem
  library(tseries)       # Testes estatísticos para séries temporais
  library(Kendall)       # Teste de Mann-Kendall
  library(randtests)     # Teste de Cox-Stuart
  library(seastests)     # Testes de sazonalidade
  library(dplyr)         # Manipulação de dados
  library(ggplot2)       # Gráficos
  library(gridExtra)     # Para arranjar múltiplos plots
  library(scales)        # Formatação de eixos
  library(psych)         # Estatísticas descritivas
})

# Criação de um tema padronizado para limpar o código dos gráficos
tema_custom <- theme_bw(base_size = 18) +
  theme(
    axis.text = element_text(size = 22),
    axis.text.x = element_text(angle = 0, hjust = 0.5),
    axis.title = element_text(size = 24),
    plot.title = element_text(size = 26, hjust = 0.5, face = "bold"),
    panel.grid.major.x = element_line(color = "gray80", linewidth = 0.4),
    panel.grid.minor.x = element_line(color = "gray95", linewidth = 0.3),
    legend.position = "bottom",
    legend.title = element_text(size = 20),
    legend.text = element_text(size = 18)
  )

# 2. CARREGAMENTO E PREPARAÇÃO DOS DADOS ---------------------------------------

# Assumindo que o arquivo está na pasta 'dados' do repositório
dados <- read_excel("dados/Produção Mensal de Petróleo no Brasil.xlsx", 
                    col_types = c("date", "numeric"))

colnames(dados) <- c("data", "producao")

# Criando a série temporal
serie_petroleo <- ts(dados$producao, 
                     start = c(2001, 1),
                     end = c(2025, 5), 
                     frequency = 12)

# Criando um dataframe auxiliar para os gráficos ggplot
serie_df <- data.frame(
  data = seq.Date(from = as.Date("2001-01-01"), 
                  by = "month", 
                  length.out = length(serie_petroleo)),
  valor = as.numeric(serie_petroleo)
)

# 3. ANÁLISE DESCRITIVA E EXPLORATÓRIA -----------------------------------------

cat("=== INFORMAÇÕES BÁSICAS DA SÉRIE ===\n")
cat("Classe:", class(serie_petroleo), "\n")
cat("Início:", start(serie_petroleo), "\n")
cat("Fim:", end(serie_petroleo), "\n")
cat("Frequência:", frequency(serie_petroleo), "\n")
print(summary(serie_petroleo))

# Estatísticas descritivas detalhadas
describe(serie_petroleo)
describeBy(serie_petroleo, cycle(serie_petroleo))

# 3.1 Visualização da Série Temporal (Base R e ggplot2)
autoplot(serie_petroleo, lwd = 1.25, color = "#0f52ba") +
  labs(y = "Volume Produzido (M^3)", x = "Ano") +
  scale_y_continuous(labels = label_number(big.mark = ".", decimal.mark = ","))

ggplot(serie_df, aes(x = data, y = valor)) +
  geom_line(color = "#0f52ba", linewidth = 2.25) +
  labs(x = "Tempo", y = expression("Volume Produzido (em " * m^3 * ")")) +
  scale_x_date(limits = as.Date(c("2000-12-01", "2025-05-01")), date_breaks = "2 years", date_labels = "%Y") +
  scale_y_continuous(labels = label_number(scale = 1e-6, suffix = "M", big.mark = ".", decimal.mark = ",")) +
  tema_custom

# 3.2 Histograma e Densidade
ggplot(serie_df, aes(x = valor)) +
  geom_histogram(aes(y = after_stat(density)), bins = 30, fill = "#0f52ba", color = "black") +
  stat_function(fun = dnorm, args = list(mean = mean(serie_df$valor), sd = sd(serie_df$valor)), 
                color = "black", linewidth = 2.25) +
  labs(x = "Valores da série", y = "Densidade") +
  scale_x_continuous(breaks = c(5e6, 9e6, 13e6, 17e6),
                     labels = function(x) paste0(format(round(x/1e6, 1), big.mark = ".", decimal.mark = ","), "M")) +
  tema_custom

# 3.3 Decomposição da Série
decomposicao_serie <- decompose(serie_petroleo, type = "multiplicative")
plot(decomposicao_serie)

# 3.4 Sazonalidade (Boxplot Mensal e Violino)
meses_pt <- c("Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez")

df_grafico <- data.frame(
  mes = factor(month.abb[cycle(serie_petroleo)], levels = month.abb, labels = meses_pt),
  valor = as.numeric(serie_petroleo)
)

ggplot(df_grafico, aes(x = mes, y = valor)) +
  geom_violin(trim = TRUE, fill = "#0f52ba", alpha = 1) +
  geom_boxplot(width = 0.4, color = "#8BBEE8", alpha = 0.21, outlier.colour = "#FF4500", outlier.size = 3) +
  stat_summary(fun = mean, geom = "point", shape = 19, size = 3, fill = "black") +
  labs(x = "Mês", y = expression("Volume Produzido (em " * m^3 * ")")) +
  scale_y_continuous(labels = function(x) ifelse(x == 0, "0", paste0(format(round(x/1e6, 1), decimal.mark=","), "M"))) +
  tema_custom

# 3.5 Crescimento e Variância
df_ano <- dados %>%
  mutate(ano = as.integer(format(data, "%Y"))) %>%
  group_by(ano) %>%
  summarise(total_anual = sum(producao, na.rm = TRUE)) %>%
  mutate(yoy = 100 * (total_anual / lag(total_anual) - 1))

ggplot(df_ano[-1, ], aes(x = ano, y = yoy, fill = yoy >= 0)) +
  geom_col(show.legend = FALSE, width = 0.9) +
  scale_fill_manual(values = c(`TRUE` = "#09703b", `FALSE` = "#D72631")) +
  geom_text(aes(label = ifelse(is.na(yoy), "", paste0(format(yoy, digits=2, nsmall=1, decimal.mark=","), "%"))), 
            vjust = ifelse(df_ano$yoy[-1] >= 0, -0.5, 1.2), size = 5) +
  labs(x = "Ano", y = "Crescimento (%)") +
  geom_hline(yintercept = 0, color = "#555555", linetype = 2, linewidth = 1.2) +
  scale_x_continuous(breaks = seq(2001, 2025, by = 2)) +
  tema_custom

# 4. TESTES FORMAIS DE HIPÓTESES -----------------------------------------------

cat("\n=== TESTES DE ESTACIONARIEDADE ===\n")
# H0: série possui raiz unitária (não estacionária) / H1: estacionária
adf.test(serie_petroleo)
# H0: série é estacionária / H1: possui raiz unitária
kpss.test(serie_petroleo)
# Conclusão: Pelos testes a série é não estacionária

cat("\n=== TESTES DE TENDÊNCIA ===\n")
# H0: não há tendência monotônica / H1: existe tendência
MannKendall(serie_petroleo)
# H0: coeficiente de tendência = 0 / H1: coeficiente ≠ 0
summary(lm(serie_petroleo ~ seq_along(serie_petroleo)))
# Conclusão: Existe tendência monotônica e o coeficiente tempo é significativo.

cat("\n=== TESTES DE SAZONALIDADE ===\n")
# H0: não há sazonalidade / H1: existe sazonalidade
qs(serie_petroleo, freq = frequency(serie_petroleo))
# Conclusão: Existe SIM sazonalidade!

# 5. TRANSFORMAÇÕES PARA ESTACIONARIEDADE --------------------------------------

cat("\n=== ANÁLISE DE VARIABILIDADE ===\n")
cat("Variância original:", var(serie_petroleo), "\n")
cat("Variância do log:", var(log(serie_petroleo)), "\n")
# Aplicando log para diminuir a variabilidade
# Aplicando a primeira diferença na transformação logarítmica
cat("Variância do log diferenciado:", var(diff(log(serie_petroleo))), "\n")

# Gráfico da primeira diff do log da série
df_diff_log <- na.omit(serie_df %>% mutate(diff_log_valor = c(NA, diff(log(valor)))))
ggplot(df_diff_log, aes(x = data, y = diff_log_valor)) +
  geom_line(color = "#0f52ba", linewidth = 2.25) +
  labs(x = "Tempo", y = expression("1ª Dif. do log(Produção) [" * Delta * "ln(m"^3 * ")]")) +
  scale_x_date(limits = as.Date(c("2000-12-01", "2025-05-01")), date_breaks = "2 years", date_labels = "%Y") +
  tema_custom

# Visualização da autocorrelação (ACF/PACF)
ggtsdisplay(diff(log(serie_petroleo)))

# 6. SEPARAÇÃO EM TREINO E TESTE -----------------------------------------------

# É uma boa prática separar os dados para treinar o modelo e avaliar a previsão
treino <- window(serie_petroleo, start = start(serie_petroleo), end = c(2021, 4))
teste <- window(serie_petroleo, start = c(2021, 5))

autoplot(serie_petroleo) +
  autolayer(treino, series = "Treino") +
  autolayer(teste, series = "Teste") +
  ggtitle("Divisão da Série em Treino e Teste") +
  tema_custom

# 7. MODELAGEM ARIMA (BOX-JENKINS) ---------------------------------------------

# --- Opção B: Ajuste Automático (Benchmark) ---
fit_auto <- auto.arima((treino), seasonal = TRUE, stepwise = FALSE, approximation = FALSE, d = 1)
summary(fit_auto)

# --- Opção A: Ajuste Manual (baseado na análise ACF/PACF) ---
modelo_arima_manual <- Arima(log(treino), order = c(2,1,3), seasonal = c(0,1,1), fixed = c(0,NA,NA,NA,NA,NA))
summary(modelo_arima_manual)

# Diagnóstico do Modelo Manual
ggtsdisplay(modelo_arima_manual$residuals)

# Função para avaliação avançada de modelos
avaliar_modelo <- function(modelo, nome_modelo) {
  cat("\n=== AVALIAÇÃO DO MODELO", nome_modelo, "===\n")
  print(summary(modelo))
  cat("\n--- Teste de Ljung-Box ---\n")
  print(Box.test(modelo$residuals, lag = 10, type = "Ljung-Box"))
  cat("\n--- Teste de Jarque-Bera ---\n")
  print(jarque.bera.test(modelo$residuals))
  cat("\n--- Teste de Shapiro-Wilk ---\n")
  if(length(modelo$residuals) <= 5000) print(shapiro.test(modelo$residuals))
  return(modelo)
}

avaliar_modelo(modelo_arima_manual, "ARIMA(2,1,3)(0,1,1) com Parâmetro Fixo")

# H0: Os resíduos são normalmente distribuídos. Queremos p-valor > 0.05.
shapiro.test(modelo_arima_manual$residuals)
# Histograma dos Resíduos
ggplot(data.frame(res = as.numeric(modelo_arima_manual$residuals)), aes(x = res)) + 
  geom_histogram(aes(y = after_stat(density)), bins = 30, fill = "#0f52ba", color = "black") +
  stat_function(fun = dnorm, args = list(mean = mean(modelo_arima_manual$residuals), sd = sd(modelo_arima_manual$residuals)), linewidth = 2.5) +
  labs(x = "Resíduos", y = "Densidade") +
  tema_custom

# 8. PREVISÃO E AVALIAÇÃO DO DESEMPENHO (SARIMA vs HOLT-WINTERS) ---------------

# Lista de modelos candidatos
modelos <- list(
  modelo_1 = Arima(log(treino), order = c(0,1,1), seasonal = c(0,1,1)),
  modelo_2 = Arima(log(treino), order = c(1,1,1), seasonal = c(0,1,1)),
  modelo_3 = Arima(log(treino), order = c(2,1,1), seasonal = c(0,1,1)),
  modelo_manual = modelo_arima_manual
)

# Previsão com o melhor modelo escolhido (exemplo: modelo_2)
previsao_sarima <- forecast(modelos$modelo_2, h = length(teste))

# Previsão Alternativa: Holt-Winters Aditivo (aplicado no Log)
modelo_hw <- HoltWinters(log(treino), seasonal = "additive")
previsao_hw <- forecast(modelo_hw, h = length(teste))

cat("\n=== ACURÁCIA: SARIMA vs HOLT-WINTERS ===\n")
cat("Acurácia SARIMA:\n")
print(accuracy(previsao_sarima, log(teste)))
cat("Acurácia Holt-Winters:\n")
print(accuracy(previsao_hw, log(teste)))

# 9. PLOT FINAL: DADOS REAIS VS PREVISÕES --------------------------------------

autoplot(log(treino), size = 1.2) +
  autolayer(previsao_hw, series = "Previsão Holt-Winters", size = 1.5, PI = FALSE) +
  autolayer(previsao_sarima$mean, series = "Previsão SARIMA", size = 1.5, alpha = 0.8) +
  autolayer(log(teste), series = "Dados Reais", size = 1.2) +
  labs(x = "Tempo", y = expression("Logaritmo Natural da Produção (ln(m"^3*"))")) +
  scale_x_continuous(breaks = seq(2001, 2025, by = 2)) +
  scale_color_manual(name = "Legenda:",
                     values = c("Previsão Holt-Winters" = "#09703b", 
                                "Previsão SARIMA" = "#0f52ba", 
                                "Dados Reais" = "#D72631")) +
  tema_custom