"""
==============================================================================
DOCHMO Analytics — Geração de Gráficos de Análise Espacial
Estudo de Caso: Índice de Progresso Social (IPS) Brasil — 2024 vs. 2025
==============================================================================
Autor: Douglas Chaves Moura
Descrição: Este script Python realiza o pipeline analítico de importação de dados,
           cálculo estatístico de quartis e outliers (notação de boxplot clássica do R),
           geoprocessamento de limites municipais com simplificação topológica e 
           geração automatizada de visualizações em HTML interativo com a biblioteca Plotly.
Diretrizes Visuais: Segue estritamente a identidade DOCHMO (Playfair Display para títulos,
                    Inter para rótulos, gradientes institucionais e fundos transparentes).
==============================================================================
"""

import os
import json
import numpy as np
import pandas as pd
import geopandas as gpd
import geobr
import plotly.graph_objects as go
import plotly.express as px
from plotly.colors import sample_colorscale, diverging

# Supressão de warnings de projeções cartográficas e bibliotecas GeoJSON
import warnings
warnings.filterwarnings("ignore")

# ==============================================================================
# 1. DESIGN SYSTEM & CONSTANTES VISUAIS DOCHMO
# ==============================================================================
FONT_TITLE = "Playfair Display"
FONT_BODY = "Inter, sans-serif"

# Paleta Cromática Institucional
COLOR_GOLD = "#D7B56D"            # Dourado corporativo principal
COLOR_WHITE = "#F8F9FA"           # Branco neve para textos em destaque
COLOR_BLUE_LIGHT = "#42A5F5"      # Azul claro para o gradiente base de 2024
COLOR_WHITE_MUTED = "#BBD9F5"     # Azul/Branco pastel para textos secundários e eixos
COLOR_GRID = "rgba(255, 255, 255, 0.05)" # Ranhuras e linhas de grade discretas
BG_TRANSPARENT = "rgba(0,0,0,0)"  # Fundo nulo para integração perfeita em iframes

# Cores Estatísticas do Boxmap (Baseadas na paleta RdBu/Dourada do R)
BOXMAP_PALETTE = {
    "Outlier Superior": "#004383",  # Azul marinho escuro (excelência máxima)
    "> 75%": "#2772B2",             # Azul médio
    "50% - 75%": "#8FC3E5",         # Azul claro/médio
    "25% - 50%": "#FDBE84",         # Salmão pastel/Pêssego
    "< 25%": "#E36F22",             # Laranja de transição
    "Outlier Inferior": "#A03016",  # Vermelho terroso (vulnerabilidade extrema)
    "Sem Dados": "#F3F3F3"          # Cinza claro neutro
}

# ==============================================================================
# 2. ESTRUTURA DE DIRETÓRIOS E AUXILIARES DE EXPORTAÇÃO
# ==============================================================================
DIR_SCRIPT = os.path.dirname(os.path.abspath(__file__))
DIR_DATASETS = os.path.join(os.path.dirname(DIR_SCRIPT), "datasets")
DIR_GRAPHICS = os.path.join(os.path.dirname(DIR_SCRIPT), "graphics")

# Garante que a pasta de destino dos arquivos HTML exista
os.makedirs(DIR_GRAPHICS, exist_ok=True)

def path_data(filename):
    """Retorna o caminho absoluto do arquivo na pasta de dados."""
    return os.path.join(DIR_DATASETS, filename)

def path_out(filename):
    """Retorna o caminho absoluto para o arquivo de saída na pasta de gráficos."""
    return os.path.join(DIR_GRAPHICS, filename)

def apply_dochmo_layout(fig, title_text, height=580, margin=None):
    """
    Aplica o padrão estético compartilhado da marca DOCHMO às figuras Plotly.
    
    Parâmetros:
        fig (go.Figure): A figura Plotly a ser estilizada.
        title_text (str): Título principal do gráfico.
        height (int): Altura do gráfico em pixels.
        margin (dict, opcional): Margens personalizadas (l, r, t, b).
    """
    if margin is None:
        margin = dict(l=20, r=20, t=50, b=20)
    
    fig.update_layout(
        paper_bgcolor=BG_TRANSPARENT,
        plot_bgcolor=BG_TRANSPARENT,
        height=height,
        margin=margin,
        separators=",.",  # Formatação padrão brasileira (vírgula decimal, ponto de milhar)
        font=dict(family=FONT_BODY, color=COLOR_WHITE_MUTED, size=13),
        title=dict(
            text=title_text,
            font=dict(family=FONT_TITLE, size=20, color=COLOR_GOLD),
            x=0.5
        ),
        legend=dict(
            font=dict(color=COLOR_WHITE_MUTED, size=12),
            bgcolor=BG_TRANSPARENT
        ),
        hoverlabel=dict(
            bgcolor="#0F1C36",
            font=dict(family=FONT_BODY, color=COLOR_WHITE, size=13),
            bordercolor=COLOR_GOLD,
        )
    )
    return fig

def save_plotly_html(fig, filepath, display_modebar=False, scroll_zoom=False):
    """
    Grava a figura do Plotly em arquivo HTML estático importando o core via CDN,
    e injeta uma folha de estilo CSS personalizada para sanitizar elementos do Mapbox.
    """
    fig.write_html(
        filepath,
        include_plotlyjs="cdn",
        full_html=True,
        config={"displayModeBar": display_modebar, "scrollZoom": scroll_zoom, "responsive": True}
    )
    
    # Injeta folha de estilo para ocultar controles redundantes e duplicados do Mapbox GL
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        css_style = """
        <style>
            /* Remove botões de atribuição e controles do Mapbox que geram efeito de sobreposição */
            .mapboxgl-ctrl {
                display: none !important;
            }
        </style>
        """
        content = content.replace("</head>", f"{css_style}</head>")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
    print(f"[OK] Gerado: {os.path.basename(filepath)}")

# ==============================================================================
# 3. CARREGAMENTO E SANEAMENTO DE DADOS
# ==============================================================================
print("Carregando bases de dados do IPS...")
df_2024 = pd.read_excel(path_data("IPSBrasil2024.xlsx"))
df_2025 = pd.read_excel(path_data("IPSBrasil2025.xlsx"))

# Renomeia colunas para nomenclatura de manipulação padronizada
colunas_nomes = ["codigo_ibge", "municipio", "uf", "ips", "moradia", "seguranca_pessoal", "saude_bem_estar", "subnutricao"]
df_2024.columns = colunas_nomes
df_2025.columns = colunas_nomes


# ==============================================================================
# 4. GERAÇÃO DOS GRÁFICOS
# ==============================================================================

def gerar_g01_bar_estados():
    """Gera o Gráfico 01: Média do IPS por Estado em 2024 (Barras Horizontais)."""
    # Agrupa dados municipais por estado e extrai a média aritmética
    df_estado = df_2024.groupby("uf")["ips"].mean().reset_index()
    df_estado = df_estado.sort_values(by="ips", ascending=True) # Ordem crescente para visualização em pilha
    
    # Define a paleta de gradiente contínuo base
    escala_g01 = [[0.0, COLOR_BLUE_LIGHT], [1.0, COLOR_GOLD]]
    min_ips, max_ips = df_estado["ips"].min(), df_estado["ips"].max()
    norm_vals = ((df_estado["ips"] - min_ips) / (max_ips - min_ips)).tolist()

    # Aplica amostragem de cores baseada nos valores normalizados
    cores_barras = sample_colorscale(escala_g01, norm_vals) 
    cores_texto = ["black"] * len(norm_vals)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_estado["ips"],
        y=df_estado["uf"],
        orientation="h",
        # Formatação direta para exibição em português do Brasil (1 casa decimal)
        text=df_estado["ips"].apply(lambda x: f"{x:.1f}".replace(".", ",")),
        texttemplate="%{text}",
        textposition="auto",
        insidetextfont=dict(size=13, color=cores_texto),
        outsidetextfont=dict(size=10, color=COLOR_WHITE_MUTED),
        marker=dict(
            color=df_estado["ips"],
            coloraxis="coloraxis"
        ),
        hoverlabel=dict(
            bgcolor=cores_barras,
            font_color=cores_texto,
            font_size=13
        ),
        hovertemplate="<b>Estado: %{y}</b><br>IPS Médio: %{x:,.2f}<extra></extra>"
    ))
    
    apply_dochmo_layout(fig, "Média do IPS por Estado (2024)", height=520, margin=dict(l=45, r=25, t=50, b=35))
    fig.update_layout(
        coloraxis=dict(
            colorscale=[[0.0, COLOR_BLUE_LIGHT], [1.0, COLOR_GOLD]],
            showscale=False
        ),
        xaxis=dict(title="IPS Médio", showgrid=False),
        yaxis=dict(title="Estado (UF)", showgrid=False, dtick=1, tickfont=dict(size=10), ticklabelstandoff=10)
    )
    
    save_plotly_html(fig, path_out("ips_bar_estados_2024.html"))

def gerar_g02_variacao_estados():
    """Gera o Gráfico 02: Variação Média do IPS (2024-2025) por Estado (RdBu Divergente)."""
    # Realiza o merge das séries de 2024 e 2025 e computa o delta de progresso interanual
    df_comp = df_2024[["codigo_ibge", "uf", "ips"]].rename(columns={"ips": "ips_2024"}).merge(
        df_2025[["codigo_ibge", "ips"]].rename(columns={"ips": "ips_2025"}),
        on="codigo_ibge"
    )
    df_comp["variacao"] = df_comp["ips_2025"] - df_comp["ips_2024"]
    
    # Agrupa a variação por unidade federativa
    df_var = df_comp.groupby("uf")["variacao"].mean().reset_index()
    df_var = df_var.sort_values(by="variacao", ascending=True)
    
    # Centraliza a escala RdBu de forma simétrica ao redor do valor 0
    max_val = max(abs(df_var["variacao"].min()), abs(df_var["variacao"].max()))
    norm_vals = ((df_var["variacao"] + max_val) / (2 * max_val)).tolist()
    cores_barras = sample_colorscale(diverging.RdBu, norm_vals)
    
    # Determina o contraste de texto dinâmico para etiquetas internas
    cores_texto = ["white" if (v < 0.20 or v > 0.80) else "black" for v in norm_vals]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_var["variacao"],
        y=df_var["uf"],
        orientation="h",
        text=df_var["variacao"].apply(lambda x: f"{x:.2f}".replace(".", ",")),
        texttemplate="%{text}",
        textposition="auto",
        # Rótulos externos ganham contraste branco sutil para evitar colisão no fundo escuro
        insidetextfont=dict(size=13, color=cores_texto),
        outsidetextfont=dict(size=7, color=COLOR_WHITE_MUTED),
        marker=dict(
            color=df_var["variacao"],
            coloraxis="coloraxis"
        ),
        hoverlabel=dict(
            bgcolor=cores_barras,
            font_color=cores_texto,
            font_size=13
        ),
        hovertemplate="<b>Estado: %{y}</b><br>Variação Média: %{x:,.3f}<extra></extra>"
    ))
    
    apply_dochmo_layout(fig, "Variação Média do IPS (2024-2025)", height=520, margin=dict(l=45, r=25, t=50, b=35))
    fig.update_layout(
        coloraxis=dict(
            colorscale="RdBu",
            cmin=-max_val,
            cmax=max_val,
            showscale=False
        ),
        xaxis=dict(title="Variação do IPS", showgrid=False),
        yaxis=dict(title="Estado (UF)", showgrid=False, dtick=1, tickfont=dict(size=10))
    )
    
    save_plotly_html(fig, path_out("ips_variacao_estados.html"))

def gerar_g03_scatter_ceara():
    """Gera o Gráfico 03: Dispersão IPS 2024 vs 2025 (Destaque Ceará e Regressão Linear)."""
    df_comp = df_2024[["codigo_ibge", "municipio", "uf", "ips"]].rename(columns={"ips": "ips_2024"}).merge(
        df_2025[["codigo_ibge", "ips"]].rename(columns={"ips": "ips_2025"}),
        on="codigo_ibge"
    )
    df_comp["variacao"] = df_comp["ips_2025"] - df_comp["ips_2024"]
    df_comp["destaque"] = np.where(df_comp["uf"] == "CE", "Ceará", "Outros Estados")
    
    media_2024 = df_comp["ips_2024"].mean()
    media_2025 = df_comp["ips_2025"].mean()
    
    # Ajusta a reta OLS para projeção de correlação
    slope, intercept = np.polyfit(df_comp["ips_2024"], df_comp["ips_2025"], 1)
    x_range = np.array([df_comp["ips_2024"].min(), df_comp["ips_2024"].max()])
    y_reg = slope * x_range + intercept
    
    fig = go.Figure()
    
    # 1. Plot de fundo (Todos os outros estados em azul suave translúcido)
    df_outros = df_comp[df_comp["destaque"] == "Outros Estados"]
    fig.add_trace(go.Scattergl(
        x=df_outros["ips_2024"],
        y=df_outros["ips_2025"],
        mode="markers",
        name="Outros Estados",
        marker=dict(color="rgba(66, 165, 245, 0.2)", size=5.8),
        hovertext=df_outros["municipio"],
        customdata=np.column_stack((df_outros["ips_2024"], df_outros["variacao"])),
        hoverlabel=dict(
            bgcolor="rgba(66, 165, 245, 0.7)",
            font_color="white",
            font_size=13
        ),
        hovertemplate="<b>%{hovertext}</b><br>IPS 2024: %{x:,.2f}<br>IPS 2025: %{y:,.2f}<br>Variação: %{customdata[1]:,.2f}<extra></extra>"
    ))
    
    # 2. Destaque do Ceará (Pontos dourados sólidos e ligeiramente maiores)
    df_ceara = df_comp[df_comp["destaque"] == "Ceará"]
    fig.add_trace(go.Scattergl(
        x=df_ceara["ips_2024"],
        y=df_ceara["ips_2025"],
        mode="markers",
        name="Ceará",
        marker=dict(color=COLOR_GOLD, size=7, line=dict(color="#FDBE84", width=0.5)),
        hovertext=df_ceara["municipio"],
        customdata=np.column_stack((df_ceara["ips_2024"], df_ceara["variacao"])),
        hoverlabel=dict(
            bgcolor=COLOR_GOLD,
            font_color="black",
            font_size=13
        ),
        hovertemplate="<b>%{hovertext}</b><br>IPS 2024: %{x:,.2f}<br>IPS 2025: %{y:,.2f}<br>Variação: %{customdata[1]:,.2f}<extra></extra>"
    ))
    
    # 3. Reta de Regressão Linear Geral
    fig.add_trace(go.Scatter(
        x=x_range,
        y=y_reg,
        mode="lines",
        name="Regressão Geral",
        line=dict(color="rgba(255, 255, 255, 0.5)", width=2),
        hoverinfo="skip"
    ))
    
    # Cria os eixos de quadrante de média (estilo quadrante de dependência espacial)
    shapes = [
        # Linha vertical (Média IPS 2024)
        dict(
            type="line",
            x0=media_2024, x1=media_2024,
            y0=0, y1=1, yref="y domain",
            line=dict(color="rgba(255, 255, 255, 0.2)", dash="dash", width=1)
        ),
        # Linha horizontal (Média IPS 2025)
        dict(
            type="line",
            x0=0, x1=1, xref="x domain",
            y0=media_2025, y1=media_2025,
            line=dict(color="rgba(255, 255, 255, 0.2)", dash="dash", width=1)
        )
    ]
    
    apply_dochmo_layout(fig, "Dispersão IPS 2024 vs 2025 (Destaque: Ceará)", height=500, margin=dict(l=50, r=30, t=60, b=50))
    fig.update_layout(
        shapes=shapes,
        xaxis=dict(title="IPS 2024", showgrid=True, gridcolor=COLOR_GRID),
        yaxis=dict(title="IPS 2025", showgrid=True, gridcolor=COLOR_GRID),
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1)
    )
    
    save_plotly_html(fig, path_out("ips_scatter_24_25.html"))

def boxplot_stats(series):
    """
    Simula e calcula as estatísticas reais do método boxplot.stats do R.
    Retorna os limites dos whiskers inferior/superior (sem outliers), quartis e mediana.
    """
    series = series.dropna()
    q1 = np.percentile(series, 25)
    q2 = np.percentile(series, 50)
    q3 = np.percentile(series, 75)
    iqr = q3 - q1
    
    lower_whisker_limit = q1 - 1.5 * iqr
    upper_whisker_limit = q3 + 1.5 * iqr
    
    # Limites baseados em pontos reais nos extremos do intervalo
    non_outliers = series[(series >= lower_whisker_limit) & (series <= upper_whisker_limit)]
    lower_whisker = non_outliers.min()
    upper_whisker = non_outliers.max()
    
    return lower_whisker, q1, q2, q3, upper_whisker

def classify_boxplot(val, stats):
    """Classifica valores individuais nas faixas estatísticas do Boxplot."""
    lower_w, q1, q2, q3, upper_w = stats
    if pd.isna(val):
        return "Sem Dados"
    elif val > upper_w:
        return "Outlier Superior"
    elif val >= q3:
        return "> 75%"
    elif val >= q2:
        return "50% - 75%"
    elif val >= q1:
        return "25% - 50%"
    elif val >= lower_w:
        return "< 25%"
    else:
        return "Outlier Inferior"

def round_floats(obj, decimals=5):
    """Função recursiva para truncar a precisão de coordenadas geográficas no GeoJSON."""
    if isinstance(obj, float):
        return round(obj, decimals)
    elif isinstance(obj, dict):
        return {k: round_floats(v, decimals) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [round_floats(x, decimals) for x in obj]
    else:
        return obj

def gerar_g04_boxmap():
    """Gera o Gráfico 04: Boxmap do IPS 2024 por Município (Mapbox Otimizado e Responsivo)."""
    print("Baixando/Carregando malhas municipais do IBGE (ano 2020)...")
    municipios = geobr.read_municipality(year=2020)
    
    # Simplificação geométrica sutil para controle de tamanho de arquivo de visualização web
    print("Simplificando malhas geométricas sutilmente (tolerância = 0.0015)...")
    municipios["geometry"] = municipios["geometry"].simplify(tolerance=0.0015, preserve_topology=True)
    
    filename = "ips_boxmap_2024.html"

    print("Preparando dados do Boxmap...")
    mapa_df = municipios.merge(df_2024, left_on="code_muni", right_on="codigo_ibge", how="left")
    
    # Executa a separação das fatias de Tukey (notação R)
    stats_ips = boxplot_stats(mapa_df["ips"])
    mapa_df["Categoria_Temp"] = mapa_df["ips"].apply(classify_boxplot, args=(stats_ips,))
    counts = mapa_df["Categoria_Temp"].value_counts()
    
    def fmt(val):
        return f"{val:.2f}".replace(".", ",")
        
    lower_w, q1, q2, q3, upper_w = stats_ips
    
    # Formatação de faixas idêntica à legenda do boxmap no R
    intervals = {
        "Outlier Superior": f"[{fmt(upper_w)}+]",
        "> 75%": f"[{fmt(q3)} – {fmt(upper_w)}]",
        "50% - 75%": f"[{fmt(q2)} – {fmt(q3)})",
        "25% - 50%": f"[{fmt(q1)} – {fmt(q2)})",
        "< 25%": f"[{fmt(lower_w)} – {fmt(q1)})",
        "Outlier Inferior": f"[<{fmt(lower_w)}]",
        "Sem Dados": ""
    }
    
    def get_legend_name(cat):
        n = counts.get(cat, 0)
        if cat == "Sem Dados":
            return f"Sem Dados ({n})"
        return f"{cat} {intervals[cat]} ({n})"
        
    mapa_df["Categoria"] = mapa_df["Categoria_Temp"].apply(get_legend_name)
    
    # Transposição para projeção esférica padrão de Mapbox
    if mapa_df.crs != "EPSG:4326":
        mapa_df = mapa_df.to_crs("EPSG:4326")
        
    # Extrai o GeoJSON filtrando apenas o pareamento de IDs para otimização extrema do arquivo
    geojson_dict = json.loads(mapa_df[['code_muni', 'geometry']].to_json())
    
    print("Otimizando precisão das coordenadas geométricas do GeoJSON...")
    geojson_dict = round_floats(geojson_dict, decimals=5)
    
    fig = go.Figure()
    
    categorias_ordem = [
        "Outlier Superior",
        "> 75%",
        "50% - 75%",
        "25% - 50%",
        "< 25%",
        "Outlier Inferior",
        "Sem Dados"
    ]
    
    BOXMAP_PALETTE_FULL = {
        get_legend_name("Outlier Superior"): "#004383",
        get_legend_name("> 75%"): "#2772B2",
        get_legend_name("50% - 75%"): "#8FC3E5",
        get_legend_name("25% - 50%"): "#FDBE84",
        get_legend_name("< 25%"): "#E36F22",
        get_legend_name("Outlier Inferior"): "#A03016",
        get_legend_name("Sem Dados"): "#F3F3F3"
    }
    
    # Mapeia contraste de hover para as cores de fundo
    HOVER_TEXT_COLORS = {
        get_legend_name("Outlier Superior"): "white",
        get_legend_name("> 75%"): "white",
        get_legend_name("50% - 75%"): "black",
        get_legend_name("25% - 50%"): "black",
        get_legend_name("< 25%"): "black",
        get_legend_name("Outlier Inferior"): "white",
        get_legend_name("Sem Dados"): "black"
    }

    # Gera traces independentes por categoria estatística para compor a legenda do Plotly
    for cat_raw in categorias_ordem:
        cat_full = get_legend_name(cat_raw)
        sub_df = mapa_df[mapa_df["Categoria"] == cat_full]
        if sub_df.empty:
            continue
            
        sub_codes = set(sub_df["code_muni"].astype(int))
        sub_geojson = {
            "type": "FeatureCollection",
            "features": [f for f in geojson_dict["features"] if int(f["properties"]["code_muni"]) in sub_codes]
        }
            
        fig.add_trace(go.Choroplethmapbox(
            geojson=sub_geojson,
            locations=sub_df["code_muni"],
            featureidkey="properties.code_muni",
            z=np.ones(len(sub_df)),
            colorscale=[[0, BOXMAP_PALETTE_FULL[cat_full]], [1, BOXMAP_PALETTE_FULL[cat_full]]],
            showscale=False,
            showlegend=True,
            name=cat_full,
            hovertext=sub_df["municipio"],
            customdata=np.column_stack((sub_df["ips"], sub_df["uf"], sub_df["Categoria_Temp"])),
            hovertemplate="<b>Município:</b> %{hovertext}<br><b>UF:</b> %{customdata[1]}<br><b>IPS:</b> %{customdata[0]:.2f}<br><b>Categoria:</b> %{customdata[2]}<extra></extra>",
            marker=dict(opacity=0.85, line=dict(color="rgba(0,0,0,0.1)", width=0.1)),
            hoverlabel=dict(
                bgcolor=BOXMAP_PALETTE_FULL[cat_full],
                font=dict(color=HOVER_TEXT_COLORS[cat_full], size=13)
            )
        ))
        
    apply_dochmo_layout(fig, "Boxmap: IPS Brasil por Município (2024)", height=550, margin=dict(l=0, r=0, t=50, b=0))
    fig.update_layout(
        mapbox=dict(
            center=dict(lat=-14.235, lon=-51.925),
            zoom=3.5,
            style="carto-darkmatter"
        ),
        legend=dict(
            orientation="v",
            yanchor="bottom", y=0.05,
            xanchor="left", x=0.02,
            font=dict(color=COLOR_WHITE, size=11),
            bgcolor="rgba(10, 20, 40, 0.85)",
            bordercolor=COLOR_GOLD,
            borderwidth=1
        )
    )
    
    save_plotly_html(fig, path_out(filename), display_modebar=False, scroll_zoom=True)


# ==============================================================================
# 5. EXECUÇÃO EM LOTE
# ==============================================================================
if __name__ == "__main__":
    print("\n--- INICIANDO EXPORTAÇÃO DOS GRÁFICOS EM PYTHON ---")
    gerar_g01_bar_estados()
    gerar_g02_variacao_estados()
    gerar_g03_scatter_ceara()
    gerar_g04_boxmap()
    print("\n--- PROCESSO CONCLUÍDO COM SUCESSO ---")
