Projeto BI – TechStore

Sobre o projeto

Este projeto tem como objetivo desenvolver uma solução de Business Intelligence (BI) para analisar os dados de vendas da empresa fictícia TechStore.

Foram utilizadas consultas SQL, Python e SQLite para extrair informações, gerar indicadores e desenvolver um dashboard interativo para apoiar a tomada de decisões.

Objetivos

Analisar o faturamento total da empresa.

Identificar o lucro total.

Analisar o faturamento mensal.

Identificar os produtos mais vendidos.

Avaliar o desempenho dos vendedores.

Analisar as categorias de produtos.

Identificar os estados com maior faturamento.

Analisar a situação das vendas.

Identificar os clientes com maior faturamento.

Desenvolver um dashboard interativo para visualização dos resultados.

Tecnologias utilizadas

Python

SQL

SQLite

Pandas

Matplotlib

Streamlit

Visual Studio Code

Git e GitHub

Estrutura do projeto

Projeto_BI/
│
├── .venv/
│
├── analises/
│   └── graficos.py
│
├── dados/
│   ├── tratados/
│   ├── clientes.csv
│   ├── itens_venda.csv
│   ├── produtos.csv
│   ├── techstore.db
│   ├── vendas.csv
│   └── vendedores.csv
│
├── dashboard/
│   └── app.py
│
├── documentacao/
│
├── scripts/
│   ├── consultas_sql.py
│   ├── criar_banco.py
│   ├── etl.py
│   ├── gerar_dados.py
│   └── validar_dados.py
│
└── README.md

Consultas SQL desenvolvidas

O projeto possui nove análises principais:

Faturamento total.

Lucro total.

Faturamento mensal.

Produtos mais vendidos.

Desempenho dos vendedores.

Faturamento por categoria.

Faturamento por estado.

Vendas por status.

Clientes com maior faturamento.

Dashboard interativo

O dashboard foi desenvolvido utilizando Streamlit e apresenta:

Indicadores de faturamento, lucro, vendas e clientes.

Gráficos de análise comercial.

Filtro por período.

Filtro por categoria.

Filtro por estado.

Atualização dos resultados conforme os filtros selecionados.

Como executar o projeto

1. Abrir o projeto

Abra a pasta Projeto_BI no Visual Studio Code.

2. Ativar o ambiente virtual

No terminal do VS Code, execute:

.\.venv\Scripts\Activate.ps1

3. Instalar as bibliotecas

python -m pip install pandas matplotlib streamlit

4. Executar as consultas SQL

python scripts/consultas_sql.py

5. Gerar os gráficos

python analises/graficos.py

6. Executar o dashboard

python -m streamlit run dashboard/app.py

O Streamlit abrirá o dashboard no navegador, normalmente no endereço:

http://localhost:8501

Resultados obtidos

A análise dos dados apresentou os seguintes resultados:

Faturamento total: R$ 47.914.220,00.

Lucro total: R$ 16.297.255,00.

Categoria com maior faturamento: Informática.

Estado com maior faturamento: São Paulo (SP).

Produto com maior faturamento: Notebook Gamer.

Vendedor com maior faturamento: Vendedor 1.

Cliente com maior faturamento: Gabriel Almeida.

Conclusão

O projeto TechStore BI permitiu transformar dados de vendas em informações relevantes para a análise do desempenho comercial da empresa.

Por meio das consultas SQL, dos gráficos e do dashboard interativo, foi possível identificar indicadores importantes, acompanhar resultados e analisar o comportamento das vendas por período, categoria e estado.

A solução demonstra como ferramentas de análise de dados e Business Intelligence podem auxiliar empresas na interpretação de informações e na tomada de decisões estratégicas.