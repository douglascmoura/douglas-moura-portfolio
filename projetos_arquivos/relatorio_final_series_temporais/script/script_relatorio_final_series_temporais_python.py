#!/usr/bin/env python
# coding: utf-8

# # ANÁLISE DE SÉRIES TEMPORAIS: Produção Mensal de Petróleo no Brasil
# **Autor:** Douglas Chaves Moura  
# **Metodologia:** Box-Jenkins (SARIMA) e Suavização Exponencial (Holt-Winters)  
# 
# Este notebook apresenta a análise exploratória, testes estatísticos formais de estacionariedade, transformações matemáticas e a modelagem preditiva do volume de petróleo produzido no Brasil (2001-2025).

# ## 1. CONFIGURAÇÕES GLOBAIS E IMPORTAÇÕES

# ##### **Nota**: Utilizando a versão Python 3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)] on win32
# 
# As bibliotecas `pymannkendall`, `pmdarima` e `sklearn` tem um melhor suporte para as versões 3.11 e 3.12

# In[2]:


import warnings
from pathlib import Path
import numpy as np
import pandas as pd
import scipy.stats as stats
import pymannkendall as mk
import pmdarima as pm
import statsmodels.api as sm
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.stats.diagnostic import acorr_ljungbox
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Ignorar warnings de otimização numérica do statsmodels
warnings.filterwarnings("ignore")

# Formatação númerica das casas decimais no estilo pt_BR
def fmt_br(x, casas=2):
    return (
        f'{x:,.{casas}f}'
        .replace(',', 'X')
        .replace('.', ',')
        .replace('X', '.')
    )


# ## 2. CARREGAMENTO E PREPARAÇÃO DOS DADOS

# In[3]:


# Leitura vetorizada do Excel
CAMINHO_DIR = Path.cwd().resolve()
dados = pd.read_excel(CAMINHO_DIR / "Produção Mensal de Petróleo no Brasil.xlsx")
dados.columns = ["data", "producao"]

# Conversão para Datetime e truncamento estrito em Maio de 2025
dados["data"] = pd.to_datetime(dados["data"])
dados = dados[(dados["data"] >= "2001-01-01") & (dados["data"] <= "2025-05-01")]

# Criando a Série Temporal indexada com frequência estável de início de mês (MS)
dados.set_index("data", inplace=True)
serie_petroleo = dados["producao"].asfreq("MS")

# Dataframe auxiliar para compatibilidade estrutural
serie_df = serie_petroleo.reset_index()
serie_df.columns = ["data", "valor"]


# ## 3. ANÁLISE DESCRITIVA E EXPLORATÓRIA

# In[4]:


print("=== INFORMAÇÕES BÁSICAS DA SÉRIE ===")
print(f"Classe: {type(serie_petroleo)}")
print(f"Início: {serie_petroleo.index.min().strftime('%Y-%m')}")
print(f"Fim: {serie_petroleo.index.max().strftime('%Y-%m')}")
print(f"Frequência: {serie_petroleo.index.freqstr}")
print("\n--- Sumário Estatístico ---")
print(serie_petroleo.describe().apply(fmt_br))

# Estatísticas descritivas detalhadas por Mês (Equivalente ao describeBy do R)
serie_df["mes_num"] = serie_df["data"].dt.month
meses_pt = {1:"Jan", 2:"Fev", 3:"Mar", 4:"Abr", 5:"Mai", 6:"Jun", 7:"Jul", 8:"Ago", 9:"Set", 10:"Out", 11:"Nov", 12:"Dez"}
serie_df["mes"] = serie_df["mes_num"].map(meses_pt)

descritiva_mensal = serie_df.groupby("mes")["valor"].describe()


# ### 3.1 Visualização da Série Temporal (Plotly Interativo)

# In[ ]:


# 1. Dicionário de tradução dos meses
meses_pt = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun', 
            7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}

# 2. Criamos uma coluna auxiliar no DataFrame APENAS para o texto do Hover
serie_df['data_hover'] = serie_df['data'].dt.month.map(meses_pt) + " de " + serie_df['data'].dt.year.astype(str)

# 3. Passamos essa coluna escondida no 'custom_data'
fig_serie = px.line(
    serie_df, x="data", y="valor", 
    title="Série Temporal da Produção Mensal de Petróleo",
    custom_data=['data_hover'] 
)

# 4. Desenhamos a caixa de texto (Hover) com HTML e formatação D3
fig_serie.update_traces(
    line_width=2.5, line_color="#0f52ba", 
    # %{customdata[0]} puxa o Mês em PT-BR
    # %{y:,.0f} puxa o número.
    hovertemplate="<b>%{customdata[0]}</b><br>Volume: %{y:,.0f} m³<extra></extra>"
)

# 5. Adicionamos o separators=",." no Layout
fig_serie.update_layout(
    separators=",.", 
    template="plotly_white",
    title=dict(x=0.5, font=dict(size=22, family="Arial Black")),
    xaxis_title="Tempo",
    yaxis_title="Volume Produzido (m³)",
    yaxis=dict(tickformat=",.0f", showgrid=True, gridcolor="rgba(220, 220, 220, 0.5)"),
    xaxis=dict(showgrid=True, gridcolor="rgba(220, 220, 220, 0.5)"),
    font=dict(family="Arial", size=14)
)
fig_serie.show()


# ### 3.2 Histograma e Densidade

# In[ ]:


# 1. Cálculos da Curva Normal
mu = serie_df["valor"].mean()
std = serie_df["valor"].std() # Em pandas moderno, .std() resolve direto
x_azul = np.linspace(serie_df["valor"].min(), serie_df["valor"].max(), 100)
p_azul = stats.norm.pdf(x_azul, mu, std)

# 2. Criação do Histograma Base
fig_hist = px.histogram(
    serie_df, x="valor", nbins=30, marginal="box", histnorm="probability density", 
    title="Histograma e Curva de Densidade Teórica", color_discrete_sequence=["#0f52ba"]
)

# 3. Adição da Curva Normal Teórica
fig_hist.add_trace(go.Scatter(
    x=x_azul, y=p_azul, mode="lines", name="Densidade Normal", 
    line=dict(color="black", width=2.5)
))

# 4. Formatação EXCLUSIVA das Barras do Histograma
fig_hist.update_traces(
    selector=dict(type="histogram"), # Aplica SÓ nas barras
    marker_line_color="white", marker_line_width=1,
    # %{x:,.0f} formata o volume com ponto de milhar
    # %{y:.2e} formata a densidade (que é um número minúsculo) em notação científica
    hovertemplate="<b>Volume: %{x:,.0f} m³</b><br>Densidade real: %{y:.2e}<extra></extra>"
)

# 5. Formatação EXCLUSIVA da Curva Normal (Scatter)
fig_hist.update_traces(
    selector=dict(type="scatter", mode="lines"), # Aplica SÓ na linha preta
    hovertemplate="<b>Volume Teórico: %{x:,.0f} m³</b><br>Densidade teórica: %{y:.2e}<extra></extra>"
)

# 6. Layout Global e Padrão Brasileiro
fig_hist.update_layout(
    separators=",.",
    height=700,
    width=1200,
    template="plotly_white",
    title=dict(x=0.5, font=dict(size=22, family="Arial Black")),
    xaxis_title="Valores da Série (Volume m³)",
    yaxis_title="Densidade de Probabilidade",
    xaxis=dict(tickformat=",.0f"),
    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
    font=dict(family="Arial", size=14)
)

fig_hist.show()


# ### 3.3 Decomposição da Série

# In[ ]:


decomposicao = seasonal_decompose(serie_petroleo, model="multiplicative")

# 1. Dicionário de tradução e criação da lista de datas formatadas
meses_pt = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho', 
            7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
hover_datas = [f"{meses_pt[d.month]} de {d.year}" for d in decomposicao.observed.index]

fig_decomp = make_subplots(rows=4, cols=1, shared_xaxes=True, subplot_titles=["Observado", "Tendência", "Sazonalidade", "Resíduo"])

# 2. Adicionando Traces com formatação específica para cada unidade de medida
fig_decomp.add_trace(go.Scatter(
    x=decomposicao.observed.index, y=decomposicao.observed, name="Observado", line=dict(color="#0f52ba"),
    customdata=hover_datas,
    hovertemplate="%{customdata}<br><b>Volume: %{y:,.0f} m³</b><extra></extra>"
), row=1, col=1)

fig_decomp.add_trace(go.Scatter(
    x=decomposicao.trend.index, y=decomposicao.trend, name="Tendência", line=dict(color="#09703b"),
    customdata=hover_datas,
    hovertemplate="%{customdata}<br><b>Tendência: %{y:,.0f} m³</b><extra></extra>"
), row=2, col=1)

fig_decomp.add_trace(go.Scatter(
    x=decomposicao.seasonal.index, y=decomposicao.seasonal, name="Sazonalidade", line=dict(color="#FF4500"),
    customdata=hover_datas,
    hovertemplate="%{customdata}<br><b>Índice Sazonal: %{y:.4f}</b><extra></extra>"
), row=3, col=1)

fig_decomp.add_trace(go.Scatter(
    x=decomposicao.resid.index, y=decomposicao.resid, name="Resíduo", mode="markers", marker=dict(color="gray"),
    customdata=hover_datas,
    hovertemplate="%{customdata}<br><b>Resíduo: %{y:.4f}</b><extra></extra>"
), row=4, col=1)

# 3. Formatação Individual dos Eixos Y de cada Subplot
fig_decomp.update_yaxes(tickformat=",.0f", row=1, col=1) # Volume inteiro (com ponto)
fig_decomp.update_yaxes(tickformat=",.0f", row=2, col=1) # Volume inteiro (com ponto)
fig_decomp.update_yaxes(tickformat=",.3f", row=3, col=1) # Índice com 3 casas decimais (com vírgula)
fig_decomp.update_yaxes(tickformat=",.3f", row=4, col=1) # Índice com 3 casas decimais (com vírgula)

# 4. Layout Global e Padrão BR
fig_decomp.update_layout(
    separators=",.",
    height=800, 
    template="plotly_white",
    title=dict(text="Decomposição Multiplicativa da Série", x=0.5, font=dict(size=22, family="Arial Black")),
    showlegend=False,
    font=dict(family="Arial", size=14),
    hovermode="x unified" # Alinha o tooltip verticalmente (excelente para subplots!)
)

fig_decomp.show()


# ### 3.4 Sazonalidade (Boxplot Mensal e Violino Combinados)

# In[ ]:


fig_sazonal = go.Figure()
ordenacao_meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

fig_sazonal = px.violin(
    serie_df, x="mes", y="valor", box=True, points="all", 
    category_orders={"mes": ordenacao_meses},
    title="Distribuição Mensal da Produção (Violino + Boxplot)", 
    color_discrete_sequence=["#0f52ba"]
)

# 1. Limpando a caixa de informações interativa (Hover)
fig_sazonal.update_traces(
    hovertemplate="<b>Mês: %{x}</b><br>Volume: %{y:,.0f} m³<extra></extra>"
)

# 2. Personalização Individual e Padrão BR
fig_sazonal.update_layout(
    separators=",.",
    height=700,
    template="plotly_white",
    title=dict(x=0.5, font=dict(size=22, family="Arial Black")),
    xaxis_title="Mês",
    yaxis_title="Volume Produzido (m³)",
    yaxis=dict(tickformat=",.0f"),
    font=dict(family="Arial", size=14)
)

fig_sazonal.show()


# ### 3.5 Crescimento YoY Anual

# In[ ]:


df_ano = serie_df.copy()
df_ano["ano"] = df_ano["data"].dt.year
df_ano_agrupado = df_ano.groupby("ano")["valor"].sum().reset_index()
df_ano_agrupado["yoy"] = df_ano_agrupado["valor"].pct_change() * 100
df_ano_agrupado = df_ano_agrupado.dropna()

df_ano_agrupado["cor"] = np.where(df_ano_agrupado["yoy"] >= 0, "#09703b", "#D72631")

fig_yoy = px.bar(
    df_ano_agrupado, x="ano", y="yoy", 
    title="Crescimento Anual Ano a Ano (%)", 
    color="cor", color_discrete_map="identity"
)

# 1. Aplicando o texto na barra e o Hover de forma explícita
fig_yoy.update_traces(
    textposition="outside",
    texttemplate="%{y:,.1f}%", # Força a obediência ao 'separators' para o texto em cima da barra
    hovertemplate="<b>Ano: %{x}</b><br>Crescimento: %{y:,.2f}%<extra></extra>"
)

# 2. Personalização Individual e Padrão BR
fig_yoy.update_layout(
    separators=",.",
    height=700,
    template="plotly_white",
    title=dict(x=0.5, font=dict(size=22, family="Arial Black")),
    xaxis_title="Ano",
    yaxis_title="Crescimento (%)",
    xaxis=dict(tickmode="linear", dtick=1), # Proteção Enterprise: Impede que o eixo crie anos quebrados (ex: 2015.5)
    yaxis=dict(tickformat=",.1f", ticksuffix="%"), # Formata o eixo Y para já exibir o símbolo de %
    font=dict(family="Arial", size=14)
)

fig_yoy.show()


# ## 4. TESTES FORMAIS DE HIPÓTESES

# In[79]:


print("\n=== TESTES DE ESTACIONARIEDADE ===")
adf_stat, adf_p, _, _, _, _ = adfuller(serie_petroleo, autolag="AIC")
print(f"ADF p-valor: {adf_p:.4f} (H0: Possui Raiz Unitária / Não Estacionária)")

kpss_stat, kpss_p, _, _ = kpss(serie_petroleo, regression="c")
print(f"KPSS p-valor: {kpss_p:.4f} (H0: Série é Estacionária)")

print("\n=== TESTES DE TENDÊNCIA ===")
mk_res = mk.original_test(serie_petroleo)
print(f"Mann-Kendall: Tendência {mk_res.trend} | p-valor: {mk_res.p:.4f}")

# Regressão linear simples contra o tempo
X_tempo = sm.add_constant(np.arange(len(serie_petroleo)))
mod_tendencia = sm.OLS(serie_petroleo.values, X_tempo).fit()
print(f"Regressão Coeficiente Angular p-valor: {mod_tendencia.pvalues[1]:.4e}")

print("\n=== TESTES DE SAZONALIDADE ===")
# Nota: Como o teste QS pertence ao pacote 'seastests' exclusivo do R, 
# a alternativa mais rigorosa em Python é o teste não-paramétrico de Kruskal-Wallis 
# para avaliar se os meses possuem distribuições significativamente distintas (sazonalidade estrutural).
grupos_mensais = [group["valor"].values for name, group in serie_df.groupby("mes_num")]
kw_stat, kw_p = stats.kruskal(*grupos_mensais)
print(f"Kruskal-Wallis p-valor inter-mensal: {kw_p:.4e} (H0: Sem Sazonalidade / Médias Iguais)")


# ## 5. TRANSFORMAÇÕES PARA ESTACIONARIEDADE

# In[ ]:


print("\n=== ANÁLISE DE VARIABILIDADE ===")
print(f"Variância original: {serie_petroleo.var():.4e}")
print(f"Variância do log: {np.log(serie_petroleo).var():.4f}")
print(f"Variância do log diferenciado: {np.log(serie_petroleo).diff().dropna().var():.4f}")

serie_diff_log = np.log(serie_petroleo).diff().dropna()

# 1. Tradução dos meses para o Hover Interativo
meses_pt = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho', 
            7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
hover_datas_diff = [f"{meses_pt[d.month]} de {d.year}" for d in serie_diff_log.index]

fig_diff = px.line(
    x=serie_diff_log.index, 
    y=serie_diff_log.values, 
    title="1ª Diferença do log(Produção)",
    custom_data=[hover_datas_diff] # Injetando as datas em PT-BR
)

# 2. Formatação da Linha e do Tooltip (4 casas decimais)
fig_diff.update_traces(
    line_color="#0f52ba", line_width=1.5,
    hovertemplate="<b>%{customdata[0]}</b><br>Δ ln(m³): %{y:,.4f}<extra></extra>"
)

# 3. Personalização Individual Embutida e Padrão BR
fig_diff.update_layout(
    separators=",.",
    template="plotly_white",
    title=dict(x=0.5, font=dict(size=22, family="Arial Black")),
    xaxis_title="Tempo",
    yaxis_title="Δ ln(m³)",
    yaxis=dict(tickformat=",.4f"), # Garante as 4 casas decimais na régua do eixo Y
    font=dict(family="Arial", size=14)
)
fig_diff.show()

# Funções auxiliares interativas para autocorrelação (ACF / PACF) em Plotly
def plot_correlogramas(serie, lags=36):
    acf_vals = sm.tsa.stattools.acf(serie, nlags=lags)
    pacf_vals = sm.tsa.stattools.pacf(serie, nlags=lags)
    limite = 1.96 / np.sqrt(len(serie))

    fig = make_subplots(rows=1, cols=2, subplot_titles=["Função de Autocorrelação (ACF)", "Função de Autocorrelação Parcial (PACF)"])
    x_lags = np.arange(lags + 1)

    # 1. ACF com formatação de 3 casas decimais
    fig.add_trace(go.Bar(
        x=x_lags, y=acf_vals, marker_color="#0f52ba", name="ACF",
        hovertemplate="<b>Lag: %{x}</b><br>Autocorrelação: %{y:,.3f}<extra></extra>"
    ), row=1, col=1)

    # 2. PACF com formatação de 3 casas decimais
    fig.add_trace(go.Bar(
        x=x_lags, y=pacf_vals, marker_color="#09703b", name="PACF",
        hovertemplate="<b>Lag: %{x}</b><br>Correlação Parcial: %{y:,.3f}<extra></extra>"
    ), row=1, col=2)

    # 3. Laço de repetição para configurar as linhas limite
    for c in [1, 2]:
        fig.add_hline(y=limite, line_dash="dash", line_color="red", row=1, col=c)
        fig.add_hline(y=-limite, line_dash="dash", line_color="red", row=1, col=c)

        # Garante que os valores na régua Y tenham 2 casas decimais e usem a vírgula
        fig.update_yaxes(tickformat=",.2f", row=1, col=c)
        # Garante que os lags (Eixo X) sejam contados de 4 em 4 como números inteiros
        fig.update_xaxes(tickmode="linear", dtick=4, row=1, col=c)

    # 4. Personalização Individual Embutida e Padrão BR
    fig.update_layout(
        separators=",.",
        template="plotly_white",
        title=dict(text="Análise de Autocorrelação (ACF e PACF)", x=0.5, font=dict(size=22, family="Arial Black")),
        showlegend=False,
        font=dict(family="Arial", size=14)
    )
    fig.show()

# Chamando a função
plot_correlogramas(serie_diff_log)


# ## 6. SEPARAÇÃO EM TREINO E TESTE

# In[ ]:


# Corte temporal exato
treino = serie_petroleo.loc[:"2021-04-01"]
teste = serie_petroleo.loc["2021-05-01":"2025-05-01"]

# 1. Tradução dos meses para o Hover Interativo
meses_pt = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho', 
            7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}

hover_treino = [f"{meses_pt[d.month]} de {d.year}" for d in treino.index]
hover_teste = [f"{meses_pt[d.month]} de {d.year}" for d in teste.index]

fig_split = go.Figure()

# 2. Adicionando as linhas com CustomData e HoverTemplate formatado
fig_split.add_trace(go.Scatter(
    x=treino.index, y=treino.values, mode="lines", name="Conjunto de Treino", 
    line=dict(color="#0f52ba", width=2.5),
    customdata=hover_treino,
    hovertemplate="<b>%{customdata}</b><br>Volume: %{y:,.0f} m³<extra></extra>"
))

fig_split.add_trace(go.Scatter(
    x=teste.index, y=teste.values, mode="lines", name="Conjunto de Teste", 
    line=dict(color="#FF4500", width=2.5),
    customdata=hover_teste,
    hovertemplate="<b>%{customdata}</b><br>Volume: %{y:,.0f} m³<extra></extra>"
))

# 3. Personalização Individual Embutida e Padrão BR
fig_split.update_layout(
    separators=",.",
    height=700,
    template="plotly_white",
    title=dict(text="Divisão da Série Temporal em Treino e Teste", x=0.5, font=dict(size=22, family="Arial Black")),
    xaxis_title="Tempo",
    yaxis_title="Volume Produzido (m³)",
    yaxis=dict(tickformat=",.0f"),
    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
    font=dict(family="Arial", size=14),
    hovermode="x unified" # Alinha as informações numa linha vertical interativa
)

fig_split.show()


# ## 7. MODELAGEM ARIMA (BOX-JENKINS)

# In[ ]:


# --- Opção B: Ajuste Automático (Benchmark) ---
fit_auto = pm.auto_arima(treino, seasonal=True, m=12, d=1, stepwise=False, approximation=False, trace=False)
print("\n=== RESUMO AUTO.ARIMA (BENCHMARK) ===")
print(fit_auto.summary())

# --- Opção A: Ajuste Manual SARIMA(2,1,3)(0,1,1)12 ---
# Em R, 'fixed' fixa o parâmetro AR1 em zero. Em Python (statsmodels), realizamos isso 
# aplicando o método 'fit_constrained' para mapear restrições estruturais de forma explícita.
treino_log = np.log(treino)
modelo_manual = SARIMAX(treino_log, order=(2, 1, 3), seasonal_order=(0, 1, 1, 12),
                        enforce_stationarity=False, enforce_invertibility=False)

# Forçando o coeficiente ar.L1 (phi_1) a ser rigidamente zero
resultado_manual = modelo_manual.fit_constrained({"ar.L1": 0.0}, disp=False)
print("\n=== RESUMO MODELO MANUAL DETALHADO ===")
print(resultado_manual.summary())

# Diagnóstico de resíduos do modelo manual
residuos_manual = resultado_manual.resid.dropna()
plot_correlogramas(residuos_manual)

# Função Avançada de Avaliação Reutilizável
def avaliar_modelo_python(modelo_fit, nome_modelo):
    print(f"\n=== AVALIAÇÃO DO MODELO: {nome_modelo} ===")
    residuos = modelo_fit.resid.dropna()

    # Ljung-Box
    lb_p = acorr_ljungbox(residuos, lags=[10], return_df=True)["lb_pvalue"].values[0]
    print(f"Teste de Ljung-Box (lag=10) p-valor: {lb_p:.5f}")

    # Jarque-Bera
    jb_stat, jb_p, _, _ = sm.stats.jarque_bera(residuos)
    print(f"Teste de Jarque-Bera p-valor: {jb_p:.5e}")

    # Shapiro-Wilk
    sw_stat, sw_p = stats.shapiro(residuos)
    print(f"Teste de Shapiro-Wilk p-valor: {sw_p:.5f}")

avaliar_modelo_python(resultado_manual, "SARIMA(2,1,3)(0,1,1)12 com phi_1=0")


# ## 8. PREVISÃO E AVALIAÇÃO DO DESEMPENHO

# In[ ]:


# Gerando a grade de modelos concorrentes
modelos_grade = {
    "modelo_1": SARIMAX(treino_log, order=(0,1,1), seasonal_order=(0,1,1,12)).fit(disp=False),
    "modelo_2": SARIMAX(treino_log, order=(1,1,1), seasonal_order=(0,1,1,12)).fit(disp=False),
    "modelo_3": SARIMAX(treino_log, order=(2,1,1), seasonal_order=(0,1,1,12)).fit(disp=False),
    "modelo_manual": resultado_manual
}

# Escolhendo o modelo candidato para previsão
passos_previsao = len(teste)
previsao_log_sarima = modelos_grade["modelo_2"].get_forecast(steps=passos_previsao).predicted_mean

# Previsão Alternativa: Holt-Winters Aditivo aplicado na série em Log
modelo_hw = ExponentialSmoothing(treino_log, trend="add", seasonal="add", seasonal_periods=12).fit()
previsao_log_hw = modelo_hw.forecast(steps=passos_previsao)

# Métricas de Acurácia Customizadas (Equivalente ao accuracy do R)
teste_log = np.log(teste)

def calcular_metricas(pred, real, nome):
    me = np.mean(pred - real)
    rmse = np.sqrt(mean_squared_error(real, pred))
    mae = mean_absolute_error(real, pred)
    mape = np.mean(np.abs((real - pred) / real)) * 100
    print(f"Métricas {nome} -> ME: {me:.4f} | RMSE: {rmse:.4f} | MAE: {mae:.4f} | MAPE: {mape:.2f}%")

print("\n=== ACURÁCIA NO CONJUNTO DE TESTE ===")
calcular_metricas(previsao_log_sarima, teste_log, "SARIMA")
calcular_metricas(previsao_log_hw, teste_log, "Holt-Winters")


# ## 9. PLOT FINAL: DADOS REAIS VS PREVISÕES

# In[ ]:


# ==============================================================================
# MODELAGEM E PREVISÃO
# ==============================================================================

# Modelagem SARIMA
modelo_sarima = SARIMAX(
    treino_log,
    order=(2, 1, 3),
    seasonal_order=(0, 1, 1, 12),
    enforce_stationarity=False,
    enforce_invertibility=False
)
resultado_sarima = modelo_sarima.fit(disp=False, maxiter=200)

# Previsão SARIMA
previsao_sarima = resultado_sarima.get_forecast(steps=len(teste_log))
sarima_mean = previsao_sarima.predicted_mean
sarima_ci = previsao_sarima.conf_int(alpha=0.05)

# Modelagem e Previsão Holt-Winters Aditivo no Log
modelo_hw = ExponentialSmoothing(
    treino_log, 
    trend='add', 
    seasonal='add', 
    seasonal_periods=12
).fit()
previsao_hw = modelo_hw.forecast(len(teste_log))

# ==============================================================================
# VISUALIZAÇÃO INTERATIVA ENTERPRISE
# ==============================================================================

# 1. Tradução dos meses para o Hover Interativo
meses_pt = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho', 
            7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}

# Geramos os rótulos de data. Note que usamos o mesmo 'hover_teste' para os 3 modelos preditivos
hover_treino = [f"{meses_pt[d.month]} de {d.year}" for d in treino_log.index]
hover_teste = [f"{meses_pt[d.month]} de {d.year}" for d in teste_log.index] 

fig_final = go.Figure()

# Dados de Treino
fig_final.add_trace(go.Scatter(
    x=treino_log.index, y=treino_log.values, mode='lines', name='Treino', 
    line=dict(color='gray', width=2),
    customdata=hover_treino,
    hovertemplate="<b>%{customdata}</b><br>Treino: %{y:,.4f}<extra></extra>"
))

# Dados Reais (Teste)
fig_final.add_trace(go.Scatter(
    x=teste_log.index, y=teste_log.values, mode='lines', name='Dados Reais', 
    line=dict(color='#D72631', width=2.5),
    customdata=hover_teste,
    hovertemplate="<b>%{customdata}</b><br>Real: %{y:,.4f}<extra></extra>"
))

# Previsão SARIMA
fig_final.add_trace(go.Scatter(
    x=sarima_mean.index, y=sarima_mean.values, mode='lines', name='Previsão SARIMA', 
    line=dict(color='#0f52ba', width=2.5),
    customdata=hover_teste,
    hovertemplate="<b>%{customdata}</b><br>SARIMA: %{y:,.4f}<extra></extra>"
))

# Intervalo de Confiança SARIMA
fig_final.add_trace(go.Scatter(
    x=list(sarima_ci.index) + list(sarima_ci.index)[::-1],
    y=list(sarima_ci.iloc[:, 1]) + list(sarima_ci.iloc[:, 0])[::-1],
    fill='toself', fillcolor='rgba(15, 82, 186, 0.2)', line=dict(color='rgba(255,255,255,0)'),
    name='IC 95% SARIMA', showlegend=False,
    hoverinfo='skip' # Impede que a sombra crie caixas inúteis no mouse
))

# Previsão Holt-Winters
fig_final.add_trace(go.Scatter(
    x=previsao_hw.index, y=previsao_hw.values, mode='lines', name='Previsão Holt-Winters', 
    line=dict(color='#09703b', dash='dash', width=2.5),
    customdata=hover_teste,
    hovertemplate="<b>%{customdata}</b><br>Holt-Winters: %{y:,.4f}<extra></extra>"
))

# Layout Global, Padrão BR e Consistência Estética
fig_final.update_layout(
    separators=",.",
    height=500,
    template="plotly_white",
    title=dict(text="Comparativo Final de Projeções: Real vs SARIMA vs Holt-Winters", font=dict(size=22, family="Arial Black")),
    xaxis_title="Tempo",
    yaxis_title="Log(Volume Produzido)",
    yaxis=dict(tickformat=",.4f"), # Garante as 4 casas decimais na régua do eixo Y
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), 
    font=dict(family="Arial", size=14),
    hovermode="x unified" 
)

fig_final.show()

