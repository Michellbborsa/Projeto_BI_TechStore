
import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

# =====================================
# PROJETO BI - TECHSTORE
# DASHBOARD PRINCIPAL
# =====================================

# Configuração da página
st.set_page_config(
    page_title="TechStore | Dashboard BI",
    page_icon="📊",
    layout="wide"
)
# =====================================
# IDENTIDADE VISUAL - TECHSTORE
# =====================================

st.markdown("""
<style>

.stApp {
    background-color: #0B1120;
    color: #FFFFFF;
}

[[data-testid="stMetric"] {
    background: linear-gradient(145deg, #17243A, #1E3150);
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #2B4568;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    transition: all 0.3s ease;
}

[data-testid="stMetric"]:hover {
    border: 1px solid #38BDF8;
    transform: translateY(-3px);
}

[data-testid="stMetricLabel"] {
    color: #A8B8D0;
}

[data-testid="stMetricValue"] {
    color: #38BDF8;
}

h1, h2, h3 {
    color: #FFFFFF;
}

</style>
""", unsafe_allow_html=True)

# Caminho do banco de dados
PASTA_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_BANCO = PASTA_PROJETO / "dados" / "techstore.db"
# =====================================
# FILTRO DE PERÍODO
# =====================================

st.sidebar.header("🔎 Filtros")

periodo = st.sidebar.selectbox(
    "Selecione o período:",
    ["Todo o período", "2025", "2026"]
)

# Filtro de categoria
categorias = [
    "Todas as categorias",
    "Acessorios",
    "Audio",
    "Celulares",
    "Eletronicos",
    "Fotografia",
    "Games",
    "Informatica",
    "Redes",
    "Televisores",
    "Wearables"
]

categoria_selecionada = st.sidebar.selectbox(
    "Selecione a categoria:",
    categorias
)

# Filtro de estado
estados = [
    "Todos os estados",
    "BA",
    "DF",
    "GO",
    "MG",
    "PR",
    "RJ",
    "SP"
]

estado_selecionado = st.sidebar.selectbox(
    "Selecione o estado:",
    estados
)


# Título

st.markdown("""
<div style="background: linear-gradient(90deg, #17243A, #1E3A5F); padding: 30px; border-radius: 15px; border-left: 6px solid #38BDF8; margin-bottom: 25px;">
    <h1 style="color: #38BDF8; margin-bottom: 5px;">TECHSTORE BI</h1>
    <h3 style="color: #FFFFFF; margin-top: 0;">Plataforma de Inteligência de Negócios</h3>
    <p style="color: #A8B8D0; margin-bottom: 0;">Análise de vendas, faturamento, lucratividade e desempenho comercial.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### Análise de desempenho comercial")

# =====================================
# FORMATAÇÃO DE MOEDA BRASILEIRA
# =====================================

def formatar_moeda(valor):
    valor_formatado = f"{valor:,.2f}"
    valor_formatado = valor_formatado.replace(",", "X")
    valor_formatado = valor_formatado.replace(".", ",")
    valor_formatado = valor_formatado.replace("X", ".")
    return f"R$ {valor_formatado}"

# Função para consultar o banco


def consultar_dados(sql, parametros=()):

    # Filtros aplicados às vendas
    condicoes = []

    if periodo == "2025":
        condicoes.append(
            "data_venda >= '2025-01-01' AND data_venda < '2026-01-01'"
        )

    elif periodo == "2026":
        condicoes.append(
            "data_venda >= '2026-01-01' AND data_venda < '2027-01-01'"
        )

    # Filtro de categoria
    if categoria_selecionada != "Todas as categorias":
        condicoes.append(
            f"categoria = '{categoria_selecionada}'"
        )

    # Filtro de estado
    if estado_selecionado != "Todos os estados":
        condicoes.append(
            f"estado = '{estado_selecionado}'"
        )

    # Aplicar filtros nas consultas de vendas
    if condicoes:
        filtro = " AND ".join(condicoes)

        sql = sql.replace(
            "vw_vendas_detalhadas",
            f"(SELECT * FROM vw_vendas_detalhadas WHERE {filtro}) AS vw_vendas_detalhadas"
        )

    # Filtro de período na consulta mensal
    if periodo == "2025":
        sql = sql.replace(
            "vw_resumo_mensal",
            """(
                SELECT * FROM vw_resumo_mensal
                WHERE mes >= '2025-01' AND mes < '2026-01'
            )"""
        )

    elif periodo == "2026":
        sql = sql.replace(
            "vw_resumo_mensal",
            """(
                SELECT * FROM vw_resumo_mensal
                WHERE mes >= '2026-01' AND mes < '2027-01'
            )"""
        )

    conexao = sqlite3.connect(CAMINHO_BANCO)

    dados = pd.read_sql_query(
        sql,
        conexao,
        params=parametros
    )

    conexao.close()

    return dados



# Indicadores principais
sql_indicadores = """
SELECT
    ROUND(SUM(faturamento_realizado), 2) AS faturamento,
    ROUND(SUM(lucro_bruto), 2) AS lucro,
    COUNT(DISTINCT id_venda) AS vendas,
    COUNT(DISTINCT cliente) AS clientes
FROM vw_vendas_detalhadas;
"""

indicadores = consultar_dados(sql_indicadores)

faturamento = indicadores["faturamento"].iloc[0]
lucro = indicadores["lucro"].iloc[0]
vendas = indicadores["vendas"].iloc[0]
clientes = indicadores["clientes"].iloc[0]

# Exibir indicadores em quatro cartões
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Faturamento Total",
    formatar_moeda(faturamento)
)

col2.metric(
    "📈 Lucro Total",
    formatar_moeda(lucro)
)

col3.metric(
    "🛒 Total de Vendas",
    f"{vendas:,}"
)

col4.metric(
    "👥 Total de Clientes",
    f"{clientes:,}"
)

st.divider()

st.divider()



# =====================================
# GRÁFICOS 1 E 2 - INDICADORES MENSAIS
# =====================================

coluna1, coluna2 = st.columns(2)

with coluna1:
    st.subheader("📈 Faturamento Mensal")

    sql_faturamento_mensal = """
SELECT
    substr(data_venda, 1, 7) AS mes,
    ROUND(SUM(faturamento_realizado), 2) AS faturamento
FROM vw_vendas_detalhadas
GROUP BY substr(data_venda, 1, 7)
ORDER BY mes;
"""

    df_faturamento = consultar_dados(sql_faturamento_mensal)

    st.line_chart(
    df_faturamento,
    x="mes",
    y="faturamento",
    color="#38BDF8",
    height=350
    )

with coluna2:
    st.subheader("💰 Lucro Mensal")

    sql_lucro_mensal = """
SELECT
    substr(data_venda, 1, 7) AS mes,
    ROUND(SUM(lucro_bruto), 2) AS lucro
FROM vw_vendas_detalhadas
GROUP BY substr(data_venda, 1, 7)
ORDER BY mes;
"""

    df_lucro = consultar_dados(sql_lucro_mensal)

    st.line_chart(
        df_lucro,
        x="mes",
        y="lucro"
    )



# =====================================
# GRÁFICOS 3 E 4 - CATEGORIAS E PRODUTOS
# =====================================

coluna3, coluna4 = st.columns(2)

with coluna3:
    st.subheader("📦 Faturamento por Categoria")

    sql_categoria = """
    SELECT
        categoria,
        ROUND(SUM(faturamento_realizado), 2) AS faturamento
    FROM vw_vendas_detalhadas
    GROUP BY categoria
    ORDER BY faturamento DESC;
    """

    df_categoria = consultar_dados(sql_categoria)

    st.bar_chart(
        df_categoria,
        x="categoria",
        y="faturamento"
    )

with coluna4:
    st.subheader("🏆 Top 10 Produtos Mais Vendidos")

    sql_produtos = """
    SELECT
        produto,
        SUM(quantidade) AS quantidade
    FROM vw_vendas_detalhadas
    WHERE status = 'Concluida'
    GROUP BY produto
    ORDER BY quantidade DESC
    LIMIT 10;
    """

    df_produtos = consultar_dados(sql_produtos)

    st.bar_chart(
        df_produtos,
        x="produto",
        y="quantidade"
    )

# =====================================
# GRÁFICOS 5 E 6 - VENDEDORES E ESTADOS
# =====================================

coluna5, coluna6 = st.columns(2)

with coluna5:
    st.subheader("👨‍💼 Desempenho dos Vendedores")

    sql_vendedores = """
    SELECT
        vendedor,
        ROUND(SUM(faturamento_realizado), 2) AS faturamento
    FROM vw_vendas_detalhadas
    WHERE status = 'Concluida'
    GROUP BY vendedor
    ORDER BY faturamento DESC;
    """

    df_vendedores = consultar_dados(sql_vendedores)

    st.bar_chart(
        df_vendedores,
        x="vendedor",
        y="faturamento"
    )

with coluna6:
    st.subheader("🗺️ Faturamento por Estado")

    sql_estados = """
    SELECT
        estado,
        ROUND(SUM(faturamento_realizado), 2) AS faturamento
    FROM vw_vendas_detalhadas
    GROUP BY estado
    ORDER BY faturamento DESC;
    """

    df_estados = consultar_dados(sql_estados)

    st.bar_chart(
        df_estados,
        x="estado",
        y="faturamento"
    )

# =====================================
# GRÁFICOS 7 E 8 - STATUS E CLIENTES
# =====================================

coluna7, coluna8 = st.columns(2)

with coluna7:
    st.subheader("📊 Vendas por Status")

    sql_status = """
    SELECT
        status,
        COUNT(DISTINCT id_venda) AS quantidade_vendas
    FROM vw_vendas_detalhadas
    GROUP BY status
    ORDER BY quantidade_vendas DESC;
    """

    df_status = consultar_dados(sql_status)

    st.bar_chart(
        df_status,
        x="status",
        y="quantidade_vendas"
    )

with coluna8:
    st.subheader("🥇 Top 10 Clientes")

    sql_clientes = """
    SELECT
        cliente,
        ROUND(SUM(faturamento_realizado), 2) AS faturamento
    FROM vw_vendas_detalhadas
    WHERE status = 'Concluida'
    GROUP BY cliente
    ORDER BY faturamento DESC
    LIMIT 10;
    """

    df_clientes = consultar_dados(sql_clientes)

    st.bar_chart(
        df_clientes,
        x="cliente",
        y="faturamento"
    )