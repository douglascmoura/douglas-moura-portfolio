# 📄 EEGs em Modelos de Regressão Beta para Dados Longitudinais

Este repositório contém o relatório teórico desenvolvido para a disciplina de **Análise de Dados Longitudinais (CC0300)**, ofertada pelo Departamento de Estatística e Matemática Aplicada (DEMA) da **Universidade Federal do Ceará (UFC)**, sob a orientação do Prof. Dr. Juvêncio Santos Nobre.

---

## 🎯 Resumo do Trabalho

Estudos longitudinais (medidas repetidas) impõem o desafio analítico de lidar com a correlação intrínseca entre observações de um mesmo indivíduo ao longo do tempo. Quando a variável resposta assume valores contínuos e restritos ao intervalo $(0,1)$ --- como taxas, proporções e índices ---, a regressão clássica se torna inadequada.

Este relatório explora de forma aprofundada a aplicação das **Equações de Estimação Generalizadas (EEGs)**, propostas originalmente por Liang e Zeger (1986), no contexto dos **Modelos de Regressão Beta** (Ferrari e Cribari-Neto, 2004). O trabalho documenta não apenas a modelagem do parâmetro de posição (média), mas também a **modelagem conjunta da média e da dispersão (precisão)**, permitindo capturar a heterogeneidade e a dependência temporal dos dados.

## 📚 Tópicos Abordados no Relatório

O documento PDF detalha o arcabouço matemático e estatístico dos seguintes temas:
1. **Distribuição e Regressão Beta:** Parametrizações, função de verossimilhança, e matriz de Informação de Fisher.
2. **Equações de Estimação Generalizadas (EEGs):** Estruturas de covariância de trabalho (Independência, AR-1, Não Estruturada) e matriz sanduíche.
3. **Modelagem Conjunta (EEGs aplicadas à Regressão Beta):** Estimação iterativa de parâmetros de posição ($\beta$), precisão ($\gamma$) e correlação ($\alpha$).
4. **Análise de Diagnóstico para Medidas Repetidas:** Pontos de alavanca (matriz de projeção), pontos aberrantes (resíduos padronizados) e pontos influentes (Distância de Cook).
5. **Seleção de Modelos:** Uso dos critérios de informação $QIC$ e $QIC_s$.
6. **Influência Local:** Avaliação da sensibilidade do modelo sob diferentes esquemas de perturbação (ponderação de casos, resposta, covariáveis e precisão).

---

## 🛠️ Ferramentas Utilizadas

A redação e a formatação matemática de alto nível deste documento foram construídas utilizando o ecossistema LaTeX.

![LaTeX](https://img.shields.io/badge/latex-%23008080.svg?style=for-the-badge&logo=latex&logoColor=white)
![Overleaf](https://img.shields.io/badge/Overleaf-47A141?style=for-the-badge&logo=overleaf&logoColor=white)

---

## 📂 Estrutura do Repositório

Como este é um repositório focado em documentação teórica e metodológica, a estrutura foi simplificada para facilitar o acesso:

```text
├── graphics/           # Pasta contendo os gráficos utilizados
├── EEGs_Regressão_Beta_com_Medidas_Repetidas.pdf  # Versão final do documento compilado para leitura
├── Slides_de_Apresentação # Versão de apresentação do trabalho
├── referencias.bib     # Biblioteca de referências
└── README.md           # Este arquivo
```

---

## 🚀 Para Visualizar os Resultados

👉 **[Clique aqui para ler o Relatório Técnico Completo (PDF)](./EEGs_Regressão_Beta_com_Medidas_Repetidas.pdf)**

👉 **[Clique aqui para ver a Apresentação em Slides (BEAMER)](./Slides_de_Apresentação.pdf)**