<a name="topo"></a>
<p align="center">
  <img src="assets/img/logo_dochmo.png" width="380" alt="DOCHMO Portfolio Logo"/>
</p>

<h1 align="center">🌐 DOCHMO — Portfólio de Estatística, Data Science & Data Storytelling</h1>

<p align="center">
  <a href="https://pages.cloudflare.com"><img src="https://img.shields.io/badge/Cloudflare_Pages-F38020?style=for-the-badge&logo=cloudflare&logoColor=white" alt="Cloudflare Pages"/></a>
  <a href="#"><img src="https://img.shields.io/badge/HTML5_--_CSS3-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5 & CSS3"/></a>
  <a href="#"><img src="https://img.shields.io/badge/JavaScript-ES6+-gold?style=for-the-badge&logo=javascript&logoColor=white" alt="JavaScript ES6+"/></a>
  <a href="#"><img src="https://img.shields.io/badge/GSAP-Animations-88CE02?style=for-the-badge&logo=greensock&logoColor=white" alt="GSAP Animations"/></a>
  <a href="#"><img src="https://img.shields.io/badge/Plotly.js-Interactive-80CFEA?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly.js"/></a>
  <a href="#"><img src="https://img.shields.io/badge/LaTeX-MathJax_3-008080?style=for-the-badge&logo=LaTeX&logoColor=white" alt="LaTeX MathJax"/></a>
  <a href="https://douglas-moura-portfolio.pages.dev"><img src="https://img.shields.io/badge/Portfolio-Douglas_Chaves_Moura-0A1630?style=for-the-badge&logo=googlepubsub&logoColor=white" alt="Portfolio"/></a>
</p>

Este repositório contém o código-fonte completo e a arquitetura web do **site oficial e portfólio web da marca DOCHMO**, desenvolvido por mim, **Douglas Chaves Moura**. O ecossistema consolida **Estatística Aplicada, Estatística Computacional, Simulação Estocástica, Machine Learning, Análise Espacial e Visualização Interativa** em uma experiência web imersiva de altíssimo padrão estético e rigor acadêmico-profissional.

Desenvolvido sob medida (*Vanilla Web Stack*) em um elegante tema *Dark/Gold Mode* (Azul Noturno Profundo `#0A1428` e Dourado Metálico `#D7B56D`), a plataforma unifica 5 estudos de caso quantitativos de alta densidade técnica, notebooks reproduzíveis, artigos teóricos formatados com renderização matemática $\LaTeX$ em tempo real e relatórios técnicos em PDF compilados sob o selo editorial **DOCHMO Analytics**.

---

## 🚀 Atalhos Rápidos

* 🌐 **[Acesse o Portfólio Ao Vivo (Cloudflare Pages)](https://douglas-moura-portfolio.pages.dev)**
* 📄 **[Baixe o Curriculum Vitae Atualizado (PDF)](./assets/Douglas_Moura___Curriculum_Vitae.pdf)**
* 🏆 **[Explore a Galeria Interativa de Certificações](https://douglas-moura-portfolio.pages.dev/certificacoes.html)**

---

## 📸 Demonstração da Interface

![Preview da Interface DOCHMO Portfolio](assets/img/preview.jpg)

*Interface da aplicação web DOCHMO.*

---

## ⚡ Engenharia de Interface & Arquitetura Web

Para proporcionar uma navegação fluida, esteticamente marcante e com desempenho computacional otimizado no lado do cliente (sem a sobrecarga de frameworks JS invasivos), a arquitetura do ecossistema web foi projetada em torno de quatro pilares fundamentais:

### 1. Vanilla Web Core & Design System Customizado
* **Estabilidade & Desempenho Nativo:** Estruturação semântica em **HTML5** e estilização em **CSS3** estruturado via CSS Grid, Flexbox e variáveis globais (*Custom Properties*).
* **Paleta de Cores Institucional:** Identidade visual inspirada na sobriedade de publicações científicas e consultoria quantitativa, combinando Azul Noturno Profundo (`#0A1428`), Dourado Metálico (`#D7B56D`), Grafite Escuro e realces luminosos.
* **Tipografia Editorial:** Harmonização entre a fonte serifada *Playfair Display* (para títulos institucionais e equações) e *Inter* (para leitura técnica e tabelas de dados).

### 2. Motor de Animação e Micro-Interações (GSAP & ScrollTrigger)
* **Scroll-Driven Storytelling:** Utilização do ecossistema **GSAP (GreenSock)** e plugin **ScrollTrigger** para orquestrar revelações encadeadas, parallax sutil em seções de destaque e entrada suave de cartões de projetos.
* **Custom Cursor Magnético:** Cursor duplo interativo desenvolvido em JavaScript nativo com interpolação linear (*lerp smoothing*) que reage dinamicamente ao passar por botões, links e cards interativos.
* **Hero Particle Canvas:** Motor gráfico em HTML5 Canvas 2D renderizando uma malha vetorial de partículas em movimento continuo no plano de fundo da seção inicial.

```javascript
/* Trecho do motor de interpolação do cursor magnético (interactions.js) */
function animateCursor() {
  rx = lerp(rx, mx, 0.14);
  ry = lerp(ry, my, 0.14);
  ring.style.left = `${rx}px`;
  ring.style.top = `${ry}px`;
  dot.style.left = `${mx}px`;
  dot.style.top = `${my}px`;
  requestAnimationFrame(animateCursor);
}
```

### 3. Visualização de Dados & Motor Gráfico Embarcado (Plotly.js & MathJax 3)
* **Dashboards Interativos no Client-Side:** Embarcamento nativo de gráficos tridimensionais, mapas coropléticos espaciais, diagramas de intervenção e séries temporais gerados em **Python** e **R** e convertidos para **Plotly.js**.
* **Renderização Teórica $\LaTeX$:** Integração da biblioteca **MathJax 3** com suporte a macros customizadas, permitindo a exibição impecável de densidades de probabilidade, matrizes e equações diferenciais nas páginas de artigos teóricos.

### 4. Infraestrutura Edge, SEO Avançado & Segurança
* **Cloudflare Pages CDN:** Hospedagem global de alta disponibilidade com distribuição na camada Edge para latência ultrabaixa.
* **Cabeçalhos HTTP de Segurança (`_headers`):** Diretivas personalizadas de Content Security Policy (CSP), proteção contra ataques de *clickjacking* (`X-Frame-Options: DENY`), HTTP Strict Transport Security (HSTS) e regras estritas de *Cache-Control* para recursos estáticos.
* **Otimização SEO & Performance:** Meta tags Open Graph completas, suporte a favicons em múltiplos tamanhos, verificação do Google Search Console e carregamento diferido (*lazy loading*) das métricas do Google Analytics 4.

---

## ⚛️ Fundamentação Teórica & Estudos de Caso em Destaque

O portfólio unifica 5 investigações quantitativas completas, conectando o rigor teóricofísico/matemático à aplicação prática de Machine Learning e Econometria:

---

### 1. ⚛️ Modelo de Ising 2D: Simulação Estocástica e Fenômenos Críticos
* **Página Interativa:** [`case_ising_2d.html`](case_ising_2d.html) | **Streamlit App:** [douglasmoura-ising-2d.streamlit.app](https://douglasmoura-ising-2d.streamlit.app/)
* **Relatório Técnico:** [`Relatorio_Modelo_Ising_2D.pdf`](projetos_arquivos/modelo_ising_2d_metropolis/Relatorio_Modelo_Ising_2D.pdf)

Estudo da transição de fase ferromagnética e comportamentos coletivos em uma rede quadrada $n \times n$ de spins ($\sigma_i \in \{-1, +1\}$), governada pela Hamiltoniana:

$$H(\sigma) = -J \sum_{\langle i,j \rangle} \sigma_i \sigma_j - h \sum_i \sigma_i$$

* **Solução Exata de Onsager (1944):** Ponto crítico exato no limite termodinâmico dado por $\beta_c = \frac{\ln(1+\sqrt{2})}{2J} \approx 0{,}4407$, correspondendo à temperatura crítica $T_c \approx 2{,}269 \frac{J}{k_B}$.
* **Engenharia de Performance (Python + Numba JIT):** Motor estocástico de **Metropolis-Hastings** compilado via LLVM nativo (`@njit`), atingindo milhões de atualizações de spin por segundo. Renderização gráfica vetorizada em $O(1)$ mapeando a matriz de spins diretamente para um tensor RGB uint8 via NumPy.
* **Análise Termodinâmica:** Simulação de grandezas observáveis (Magnetização espontânea $M$, Suscetibilidade magnética $\chi$ e Calor específico $C$) e discussão da divergência do tempo de autocorrelação (*Critical Slowing Down*).

---

### 2. 📈 Modelagem e Previsão da Produção de Petróleo no Brasil (Versão 2.0)
* **Página Interativa:** [`case_series_temporais_v2.html`](case_series_temporais_v2.html) | **Relatório Técnico:** [`Modelagem_Previsao_Petroleo_Brasil.pdf`](projetos_arquivos/relatorio_dochmo_series_temporais_v2.0/Modelagem_Previsao_Petroleo_Brasil.pdf)

Estudo econométrico sobre a série histórica mensal de produção de petróleo no Brasil (dados ANP de **Janeiro/1997 a Dezembro/2025**, totalizando **348 observações**).

* **Modelagem Clássica & Intervenção:** Ajuste de modelos $\mathrm{SARIMA}(p,d,q)(P,D,Q)_{12}$ acoplados à análise de intervenção de Box-Tiao com detecção automática de quebras estruturais (Bai-Perron). Classificação de choques históricos em *Additive Outliers* (Crise do Apagão 2001: $-9{,}62\%$; Pandemia COVID-19: $-7{,}80\%$) e *Level Shifts* (Rodadas da Cessão Onerosa 2019: $+19{,}7\%$).
* **Análise Espectral & Fourier:** Decomposição no domínio da frequência via Transformada de Fourier, confirmando a sazonalidade determinística de alta complexidade no limite de Nyquist ($K=6$).
* **Validação Cruzada Preditiva:** Competição entre modelos estatísticos (SARIMA, Holt-Winters, ARIMAX) e de Machine Learning (Prophet, TBATS, NNAR) sob esquemas de **Holdout Estático ($h=36$ meses)** e **Rolling-Origin ($h=12$ meses)**.

#### Resultados Preditivos (Holdout Estático $h=36$ meses - 2023 a 2025):

| Modelo | MAE ($m^3$) | RMSE ($m^3$) | MAPE (%) | MASE | U-Theil |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Holt-Winters** | **830.657** | **1.008.788** | **4,742%** | **1,350** | **1,260** |
| `auto.arima` (c/ deriva) | 922.925 | 1.127.748 | 5,254% | 1,500 | 1,409 |
| ARIMA + Fourier (parc.) | 1.000.498 | 1.229.305 | 5,684% | 1,626 | 1,535 |
| ARIMAX (5 intervenções) | 1.082.475 | 1.334.219 | 6,121% | 1,759 | 1,666 |
| Prophet | 1.489.120 | 1.765.812 | 8,412% | 2,420 | 2,150 |
| Naive Sazonal | 2.376.508 | 2.651.313 | 13,646% | 3,861 | 3,312 |

* **Diagnóstico de Risco:** Demonstração da falha de calibração empírica dos intervalos de incerteza em modelos *Black-Box* (Prophet cobriu apenas 47,2% dos dados reais no IC 95%), provando a superioridade da calibração paramétrica de modelos estatísticos para planejamento de longo prazo.

---

### 3. 🗺️ Análise Espacial do IPS Brasil (Geoprocessamento & Autocorrelação)
* **Página Interativa:** [`case_ips_brasil.html`](case_ips_brasil.html) | **Relatório Técnico:** [`Análise_Espacial_IPS.pdf`](projetos_arquivos/realatorio_analise_espacial/An%C3%A1lise_Espacial_IPS.pdf)

Investigação socioterritorial da distribuição do Índice de Progresso Social nos mais de **5.500 municípios brasileiros** (dados 2024-2025).

* **Pipeline Espacial em Python:** Migração e otimização de rotinas de geoprocessamento em R (`sf`, `geobr`) para a pilha espacial em Python (`GeoPandas`, `PySAL`, `pandas`).
* **Tratamento de Outliers (Boxmap):** Aplicação da regra de limites de Tukey em dados espaciais para mitigar distorções visuais provocadas por municípios de grande extensão territorial.
* **Autocorrelação Espacial (Moran's I):** Identificação de *clusters* espaciais de alta e baixa vulnerabilidade social via indicador estatístico de autocorrelação local (LISA boxmaps).

---

### 4. 👨🏽‍🏫 EEGs em Regressão Beta para Dados Longitudinais
* **Página Interativa:** [`case_eegs_reg_beta.html`](case_eegs_reg_beta.html) | **Relatório Técnico:** [`EEGs_Regressão_Beta_com_Medidas_Repetidas.pdf`](projetos_arquivos/eegs_reg_beta_medidas_repetidas/EEGs_Regress%C3%A3o_Beta_com_Medidas_Repetidas.pdf)
* **Orientação Acadêmica:** Prof. Dr. Juvêncio Santos Nobre (Universidade Federal do Ceará — UFC)

Pesquisa estatística teórica focada na modelagem de variáveis resposta restritas ao intervalo contínuo $(0,1)$ (taxas, proporções e índices) sob estruturas de medidas repetidas ao longo do tempo.

* **Reparametrização da Distribuição Beta:** Expressão em termos da média $\mu \in (0,1)$ e parâmetro de precisão/dispersão $\phi > 0$:

$$f(y; \mu, \phi) = \frac{\Gamma(\phi)}{\Gamma(\mu\phi)\Gamma((1-\mu)\phi)} y^{\mu\phi-1} (1-y)^{(1-\mu)\phi-1}, \quad \mathbb{E}[Y] = \mu, \quad \mathbb{V}[Y] = \frac{\mu(1-\mu)}{1+\phi}$$

* **Equações de Estimação Generalizadas (EEGs / GEE):** Formulação de estimadores consistentes para os parâmetros de regressão sem a necessidade de especificar completamente a distribuição conjunta multivariada, utilizando matrizes de correlação de trabalho (Independente, Equicorrelacionada, AR(1) e Não-estruturada).
* **Modelagem Conjunta da Média e Dispersão:** Especificação de ligantes duplos ($\text{logit}(\mu_i) = \mathbf{x}_i^T \boldsymbol{\beta}$ e $\ln(\phi_i) = \mathbf{z}_i^T \boldsymbol{\gamma}$).

---

### 5. 🚢 Machine Learning no Dataset Titanic (Ensembles & Análise Preditiva)
* **Página Interativa:** [`case_titanic.html`](case_titanic.html) | **Diretório:** [`projetos_arquivos/Titanic/`](projetos_arquivos/Titanic/)

Pipeline preditivo completo de classificação binária de sobrevivência aplicado ao clássico dataset do Titanic.

* **Feature Engineering Avançado:** Extração de títulos honoríficos a partir dos nomes dos passageiros, agrupação de tamanho de família (`FamilySize = SibSp + Parch + 1`), binagem de tarifas (`FareBin`) e imputação iterativa de idades faltantes baseada em agrupamento categórico.
* **Competição de Modelos:** Comparativo rigoroso entre algoritmos lineares e baseados em árvores de decisão (*Bagging* e *Boosting*).

#### Métricas de Desempenho nos Dados de Teste:

| Modelo | Acurácia | Precisão | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Random Forest (Bagging)** | **82,68%** | 81,16% | **75,68%** | **78,32%** | 89,31% |
| **Logistic Regression** | 82,12% | 78,38% | 78,38% | 78,38% | 89,29% |
| **XGBoost (Boosting)** | 82,12% | **83,87%** | 70,27% | 76,47% | **91,02%** |

* **Interpretabilidade (Feature Importance):** Confirmação estatística do impacto dominante da variável de gênero e do título extraído, refletindo o protocolo social de resgate histórico ("mulheres e crianças primeiro").

---

## 📊 Resumo dos Estudos de Caso & Entregáveis

| Estudo de Caso | Domínio Quantitativo | Ferramentas & Pilha | Relatórios PDF & Artefatos Compilados |
| :--- | :--- | :--- | :--- |
| ⚛️ **Modelo de Ising 2D** | Simulação Estocástica & Física Estatística | Python, Numba JIT, Streamlit, R, LaTeX | [`Relatorio_Modelo_Ising_2D.pdf`](projetos_arquivos/modelo_ising_2d_metropolis/Relatorio_Modelo_Ising_2D.pdf) |
| 📈 **Previsão de Petróleo V2.0** | Econometria & Séries Temporais | R, SARIMA, Holt-Winters, Prophet, ARIMAX | [`Modelagem_Previsao_Petroleo_Brasil.pdf`](projetos_arquivos/relatorio_dochmo_series_temporais_v2.0/Modelagem_Previsao_Petroleo_Brasil.pdf) |
| 🗺️ **Análise Espacial IPS** | Geoprocessamento & Autocorrelação | Python, GeoPandas, PySAL, Plotly Mapbox | [`Análise_Espacial_IPS.pdf`](projetos_arquivos/realatorio_analise_espacial/An%C3%A1lise_Espacial_IPS.pdf) |
| 👨🏽‍🏫 **EEGs & Regressão Beta** | Estatística Teórica & Longitudinal | R, EEGs/GEE, Distribuição Beta, LaTeX | [`EEGs_Regressão_Beta_com_Medidas_Repetidas.pdf`](projetos_arquivos/eegs_reg_beta_medidas_repetidas/EEGs_Regress%C3%A3o_Beta_com_Medidas_Repetidas.pdf) |
| 🚢 **Machine Learning Titanic** | Aprendizado de Máquina & EDA | Python, XGBoost, Scikit-Learn, Plotly | Dashboards HTML interativos & Notebooks |

---

## 📂 Estrutura do Repositório

O repositório está organizado de forma modular e transparente, separando as páginas web da aplicação, bibliotecas de estilo, scripts de interação e documentos técnicos compilados:

```text
site_dochmo/
├── README.md                            # Documentação principal do repositório (esta página)
├── _headers                             # Cabeçalhos HTTP de segurança e cache para Cloudflare Pages
├── index.html                           # Landing page oficial do portfólio DOCHMO
├── case_ising_2d.html                   # Página do Case: Modelo de Ising 2D
├── case_series_temporais_v2.html        # Página do Case: Previsão da Produção de Petróleo (V2.0)
├── case_series_temporais.html           # Página do Case: Previsão da Produção de Petróleo (V1.0)
├── case_ips_brasil.html                 # Página do Case: Análise Espacial do IPS Brasil
├── case_eegs_reg_beta.html              # Página do Case: EEGs em Regressão Beta Longitudinal
├── case_titanic.html                    # Página do Case: Machine Learning no Titanic
├── certificacoes.html                   # Galeria interativa de certificações profissionais
├── assets/                              # Recursos estáticos da aplicação
│   ├── Douglas_Moura___Curriculum_Vitae.pdf # Currículo profissional em PDF
│   ├── css/                             # Estilos CSS modularizados
│   │   ├── animations.css               # Animações de revelação e keyframes
│   │   ├── base.css                     # Variáveis globais, reset e escala tipográfica
│   │   ├── components.css               # Cards, botões, navegação e formulários
│   │   ├── preloader.css                # Estilização da tela de carregamento
│   │   └── style.min.css                # Folha de estilo minificada consolidada
│   ├── js/                              # Scripts da aplicação
│   │   ├── interactions.js              # Cursor magnético, GSAP ScrollTrigger e canvas
│   │   └── preloader.js                 # Gerenciador de inicialização do DOM
│   ├── img/                             # Favicons, logos e imagens institucionais
│   │   ├── favicon.png                  # Ícone de aba do navegador
│   │   ├── logo_dochmo.png              # Logotipo oficial DOCHMO
│   │   ├── preview.jpg                  # Banner de exibição Open Graph
│   │   └── fotos/                       # Registros fotográficos do autor
│   ├── video/                           # Recursos de mídia auxiliares
│   └── certificados/                    # Imagens dos certificados de certificacoes.html
└── projetos_arquivos/                   # Artefatos compilados, relatórios PDF e gráficos Plotly
    ├── modelo_ising_2d_metropolis/      # PDF do relatório do Modelo de Ising 2D
    ├── relatorio_dochmo_series_temporais_v2.0/ # PDF, dados e scripts do Estudo de Séries Temporais V2.0
    ├── realatorio_analise_espacial/     # PDF, datasets e gráficos HTML do IPS Brasil
    ├── eegs_reg_beta_medidas_repetidas/ # PDF do artigo e slides de apresentação de Regressão Beta
    ├── Titanic/                         # Gráficos interativos HTML do estudo Titanic
    └── relatorio_final_series_temporais/# PDF da versão 1.0 do relatório de Séries Temporais
```

---

## 💻 Como Executar e Visualizar Localmente

### Pré-requisitos
Para visualizar a aplicação em sua máquina local exatamente como é servida na Web, basta utilizar qualquer servidor web estático simples.

### 1. Clonar o Repositório
```bash
git clone https://github.com/douglascmoura/site_dochmo.git
cd site_dochmo
```

### 2. Inicializar um Servidor Local

#### Opção A: Utilizando Python (Nativo)
```bash
# Executa um servidor HTTP local na porta 8000
python -m http.server 8000
```
Em seguida, abra o seu navegador e acesse: `http://localhost:8000`

#### Opção B: Utilizando Node.js (`serve` ou `live-server`)
```bash
npx serve .
```

#### Opção C: VS Code Live Server
Caso utilize o VS Code, basta clicar com o botão direito no arquivo `index.html` e selecionar **"Open with Live Server"**.

---

## ✍🏽 Autor

<table align="center">
  <tr>
    <td align="center" width="150px">
      <img src="assets/img/fotos/foto_douglas_github.png" width="110" alt="Douglas Moura"/><br />
      <sub><b>Douglas Chaves Moura</b></sub>
    </td>
    <td>
      <p>Estatístico, pesquisador e cientista de dados idealizador do ecossistema <b>DOCHMO</b>. Atuando no desenvolvimento de soluções quantitativas avançadas, estatística computacional, simulação estocástica de fenômenos complexos, econometria e engenharia de visualização de dados de alta performance.</p>
      <p align="left">
        <a href="https://github.com/douglascmoura"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/></a>
        <a href="https://www.linkedin.com/in/douglas-chaves-moura/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
        <a href="mailto:douglascmoura21@gmail.com"><img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/></a>
        <a href="https://douglas-moura-portfolio.pages.dev/"><img src="https://img.shields.io/badge/Website-0A1630?style=for-the-badge&logo=googlepubsub&logoColor=white" alt="Website"/></a>
      </p>
    </td>
  </tr>
</table>

<p align="right"><a href="#topo">🔼 Voltar ao topo</a></p>
