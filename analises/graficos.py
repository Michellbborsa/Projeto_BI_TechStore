
import sqlite3
import matplotlib.pyplot as plt

# Conectar ao banco de dados
conexao = sqlite3.connect("dados/techstore.db")

# Consultar faturamento mensal
sql = """
SELECT
    mes,
    ROUND(faturamento, 2) AS faturamento
FROM vw_resumo_mensal
ORDER BY mes;
"""

# Executar consulta
dados = conexao.execute(sql).fetchall()

# Fechar conexão
conexao.close()

# Separar os resultados
meses = [linha[0] for linha in dados]
faturamento = [linha[1] for linha in dados]

# Criar gráfico
plt.figure(figsize=(12, 6))

plt.plot(
    meses,
    faturamento,
    marker="o",
    linewidth=2
)

plt.title("Faturamento Mensal - TechStore")
plt.xlabel("Mês")
plt.ylabel("Faturamento (R$)")

plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()

# Exibir gráfico
plt.show()

# =====================================
# GRÁFICO 2 - LUCRO MENSAL
# =====================================

# Consultar os dados de lucro
conexao = sqlite3.connect("dados/techstore.db")

sql_lucro = """
SELECT
    mes,
    ROUND(lucro, 2) AS lucro
FROM vw_resumo_mensal
ORDER BY mes;
"""

dados_lucro = conexao.execute(sql_lucro).fetchall()

conexao.close()

# Separar os dados
meses_lucro = [linha[0] for linha in dados_lucro]
lucro = [linha[1] for linha in dados_lucro]

# Criar gráfico
plt.figure(figsize=(12, 6))

plt.plot(
    meses_lucro,
    lucro,
    marker="o",
    linewidth=2
)

plt.title("Lucro Mensal - TechStore")
plt.xlabel("Mês")
plt.ylabel("Lucro (R$)")

plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.show()

# =====================================
# GRÁFICO 3 - FATURAMENTO POR CATEGORIA
# =====================================

# Conectar ao banco
conexao = sqlite3.connect("dados/techstore.db")

# Consulta SQL
sql_categorias = """
SELECT
    categoria,
    ROUND(SUM(faturamento_realizado), 2) AS faturamento
FROM vw_vendas_detalhadas
GROUP BY categoria
ORDER BY faturamento DESC;
"""

# Executar consulta
dados_categorias = conexao.execute(sql_categorias).fetchall()

# Fechar conexão
conexao.close()

# Separar os dados
categorias = [linha[0] for linha in dados_categorias]
valores = [linha[1] for linha in dados_categorias]

# Criar gráfico de barras
plt.figure(figsize=(10, 6))

plt.bar(categorias, valores)

plt.title("Faturamento por Categoria - TechStore")
plt.xlabel("Categoria")
plt.ylabel("Faturamento (R$)")

plt.xticks(rotation=30)
plt.grid(axis="y")

plt.tight_layout()
plt.show()

# =====================================
# GRÁFICO 4 - TOP 10 PRODUTOS
# =====================================

# Conectar ao banco
conexao = sqlite3.connect("dados/techstore.db")

# Consulta SQL
sql_produtos = """
SELECT
    produto,
    SUM(quantidade) AS unidades_vendidas,
    ROUND(SUM(faturamento_realizado), 2) AS faturamento
FROM vw_vendas_detalhadas
WHERE status = 'Concluida'
GROUP BY produto
ORDER BY faturamento DESC
LIMIT 10;
"""

# Executar consulta
dados_produtos = conexao.execute(sql_produtos).fetchall()

# Fechar conexão
conexao.close()

# Separar os dados
produtos = [linha[0] for linha in dados_produtos]
valores_produtos = [linha[2] for linha in dados_produtos]

# Criar gráfico horizontal
plt.figure(figsize=(12, 7))

plt.barh(produtos[::-1], valores_produtos[::-1])

plt.title("Top 10 Produtos por Faturamento - TechStore")
plt.xlabel("Faturamento (R$)")
plt.ylabel("Produtos")

plt.grid(axis="x")
plt.tight_layout()
plt.show()

# =====================================
# GRÁFICO 5 - DESEMPENHO DOS VENDEDORES
# =====================================

# Conectar ao banco
conexao = sqlite3.connect("dados/techstore.db")

# Consulta SQL
sql_vendedores = """
SELECT
    vendedor,
    COUNT(DISTINCT id_venda) AS vendas_realizadas,
    ROUND(SUM(faturamento_realizado), 2) AS faturamento
FROM vw_vendas_detalhadas
WHERE status = 'Concluida'
GROUP BY vendedor
ORDER BY faturamento DESC;
"""

# Executar consulta
dados_vendedores = conexao.execute(sql_vendedores).fetchall()

# Fechar conexão
conexao.close()

# Separar os dados
vendedores = [linha[0] for linha in dados_vendedores]
faturamento_vendedores = [linha[2] for linha in dados_vendedores]

# Criar gráfico
plt.figure(figsize=(10, 6))

plt.bar(vendedores, faturamento_vendedores)

plt.title("Desempenho dos Vendedores - TechStore")
plt.xlabel("Vendedores")
plt.ylabel("Faturamento (R$)")

plt.xticks(rotation=30)
plt.grid(axis="y")
plt.tight_layout()
plt.show()

# =====================================
# GRÁFICO 6 - FATURAMENTO POR ESTADO
# =====================================

# Conectar ao banco
conexao = sqlite3.connect("dados/techstore.db")

# Consulta SQL
sql_estados = """
SELECT
    estado,
    ROUND(SUM(faturamento_realizado), 2) AS faturamento
FROM vw_vendas_detalhadas
GROUP BY estado
ORDER BY faturamento DESC;
"""

# Executar consulta
dados_estados = conexao.execute(sql_estados).fetchall()

# Fechar conexão
conexao.close()

# Separar os dados
estados = [linha[0] for linha in dados_estados]
faturamento_estados = [linha[1] for linha in dados_estados]

# Criar gráfico
plt.figure(figsize=(10, 6))

plt.bar(estados, faturamento_estados)

plt.title("Faturamento por Estado - TechStore")
plt.xlabel("Estados")
plt.ylabel("Faturamento (R$)")

plt.xticks(rotation=30)
plt.grid(axis="y")
plt.tight_layout()
plt.show()

# =====================================
# GRÁFICO 7 - VENDAS POR STATUS
# =====================================

# Conectar ao banco
conexao = sqlite3.connect("dados/techstore.db")

# Consulta SQL
sql_status = """
SELECT
    status,
    COUNT(DISTINCT id_venda) AS quantidade_vendas
FROM vw_vendas_detalhadas
GROUP BY status
ORDER BY quantidade_vendas DESC;
"""

# Executar consulta
dados_status = conexao.execute(sql_status).fetchall()

# Fechar conexão
conexao.close()

# Separar os dados
status = [linha[0] for linha in dados_status]
quantidades = [linha[1] for linha in dados_status]

# Criar gráfico
plt.figure(figsize=(9, 6))

plt.bar(status, quantidades)

plt.title("Quantidade de Vendas por Status - TechStore")
plt.xlabel("Status das Vendas")
plt.ylabel("Quantidade de Vendas")

plt.grid(axis="y")
plt.tight_layout()
plt.show()

# =====================================
# GRÁFICO 8 - TOP 10 CLIENTES
# =====================================

# Conectar ao banco
conexao = sqlite3.connect("dados/techstore.db")

# Consulta SQL
sql_clientes = """
SELECT
    cliente,
    COUNT(DISTINCT id_venda) AS quantidade_compras,
    ROUND(SUM(faturamento_realizado), 2) AS faturamento
FROM vw_vendas_detalhadas
WHERE status = 'Concluida'
GROUP BY cliente
ORDER BY faturamento DESC
LIMIT 10;
"""

# Executar consulta
dados_clientes = conexao.execute(sql_clientes).fetchall()

# Fechar conexão
conexao.close()

# Separar os dados
clientes = [linha[0] for linha in dados_clientes]
faturamento_clientes = [linha[2] for linha in dados_clientes]

# Criar gráfico horizontal
plt.figure(figsize=(12, 7))

plt.barh(clientes[::-1], faturamento_clientes[::-1])

plt.title("Top 10 Clientes por Faturamento - TechStore")
plt.xlabel("Faturamento (R$)")
plt.ylabel("Clientes")

plt.grid(axis="x")
plt.tight_layout()
plt.show()
