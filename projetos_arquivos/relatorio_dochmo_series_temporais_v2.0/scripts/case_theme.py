"""
==============================================================================
DOCHMO Analytics — Sistema de Identidade Visual para Gráficos
Versão 2.0 (Relatório Técnico Independente)
==============================================================================
Autor: Douglas Chaves Moura
Propósito: Este módulo estabelece o padrão estético corporativo e o tema
           compartilhado para as visualizações de séries temporais geradas via
           Plotly. O design baseia-se em um esquema de cores escuro de alto
           contraste (Navy escuro + Dourado institucional) para garantir que
           as visualizações se fundam organicamente com o background da página.
==============================================================================
"""

import plotly.graph_objects as go

# ==============================================================================
# 1. PALETA DE CORES INSTITUCIONAL (DOCHMO DESIGN TOKENS)
# ==============================================================================

# Fundo transparente para permitir que o gráfico adote o background do elemento pai (HTML)
BG_TRANSPARENT = "rgba(0,0,0,0)"

# Dourado Institucional (Cor de destaque e identidade da marca DOCHMO)
COLOR_GOLD = "#D7B56D"

# Dourado Translúcido (Utilizado para preenchimentos de áreas e hover discreto)
COLOR_GOLD_SOFT = "rgba(215, 181, 109, 0.25)"

# Dourado de Baixa Opacidade (Utilizado para demarcar limites de áreas como sombreados)
COLOR_GOLD_FAINT = "rgba(215, 181, 109, 0.12)"

# Branco Neve (Alto contraste para eixos, textos e rótulos de dados reais observados)
COLOR_WHITE = "#F8F9FA"

# Branco Suave (Opacidade para atenuar textos secundários e linhas de projeção históricas)
COLOR_WHITE_SOFT = "rgba(248, 249, 250, 0.65)"

# Branco de Baixa Opacidade (Utilizado em tracejados secundários de dados de treinamento)
COLOR_WHITE_FAINT = "rgba(248, 249, 250, 0.15)"

# Verde Floresta (Cor de destaque para as projeções e estimativas do modelo Holt-Winters)
COLOR_GREEN = "#4CAF50"

# Vermelho Alerta (Destaque para dados reais no horizonte de teste e intervenções)
COLOR_RED = "#E74C3C"

# Azul Pastel (Representação do modelo de intervenção estatística clássico SARIMA)
COLOR_BLUE = "#5B8FD9"

# Cor das linhas de grade (Grids horizontais)
GRID_COLOR = "rgba(248, 249, 250, 0.08)"

# Família tipográfica corporativa padrão adotada em todo o portfólio (Google Fonts)
FONT_FAMILY = "Inter, sans-serif"


# ==============================================================================
# 2. FUNÇÕES DE FORMATAÇÃO E EXPORTAÇÃO
# ==============================================================================

def apply_dochmo_theme(fig: go.Figure, height: int = 480) -> go.Figure:
    """
    Aplica o tema visual corporativo DOCHMO a um objeto de figura Plotly.
    
    Ajusta a paleta de cores interna para fundo transparente (paper e plot), gridlines
    horizontais e verticais de baixo contraste, tamanho padrão responsivo do card e
    fontes tipográficas da família 'Inter'.
    
    Parâmetros:
    -----------
    fig : plotly.graph_objects.Figure
        A figura Plotly bruta a ser estilizada.
    height : int, opcional
        A altura total em pixels desejada para a visualização (padrão é 480px).
        
    Retorna:
    --------
    plotly.graph_objects.Figure
        A figura Plotly estilizada de acordo com os padrões da marca.
    """
    fig.update_layout(
        paper_bgcolor=BG_TRANSPARENT,
        plot_bgcolor=BG_TRANSPARENT,
        font=dict(family=FONT_FAMILY, color=COLOR_WHITE_SOFT, size=13),
        height=height,
        margin=dict(l=60, r=30, t=40, b=50),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="left", x=0,
            font=dict(color=COLOR_WHITE_SOFT, size=12),
            bgcolor=BG_TRANSPARENT
        ),
        hoverlabel=dict(
            bgcolor="#0F1C36",
            font=dict(family=FONT_FAMILY, color=COLOR_WHITE, size=13),
            bordercolor=COLOR_GOLD,
        ),
    )
    # Configurações do Eixo X (Tempo)
    fig.update_xaxes(
        showgrid=False,
        showline=True, linecolor=COLOR_WHITE_FAINT,
        tickfont=dict(color=COLOR_WHITE_SOFT),
        zeroline=False,
    )
    # Configurações do Eixo Y (Volume ou Índices)
    fig.update_yaxes(
        showgrid=True, gridcolor=GRID_COLOR,
        showline=False,
        tickfont=dict(color=COLOR_WHITE_SOFT),
        zeroline=False,
    )
    return fig


def write_case_html(fig: go.Figure, path: str):
    """
    Exporta uma figura Plotly estilizada como um arquivo HTML estático (standalone).
    
    A diretiva 'include_plotlyjs="cdn"' assegura que o script Plotly.js básico seja
    carregado externamente via CDN, resultando em arquivos finais extremamente leves 
    e otimizados para rápida renderização dentro de iframes no site.
    
    Parâmetros:
    -----------
    fig : plotly.graph_objects.Figure
        A figura Plotly estilizada e pronta para exportação.
    path : str
        O caminho relativo ou absoluto onde o arquivo HTML final será salvo.
    """
    fig.write_html(
        path,
        include_plotlyjs="cdn",
        full_html=True,
        config={"displayModeBar": False, "responsive": True},
    )
    print(f"[OK] Salvo com sucesso no caminho: {path}")
