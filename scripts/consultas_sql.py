
import sqlite3
from pathlib import Path

# ==========================================
# PROJETO BI - TECHSTORE
# CONSULTAS SQL
# ==========================================

PASTA_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_BANCO = PASTA_PROJETO / "dados" / "techstore.db"


def executar_consulta(titulo, sql):

    conexao = sqlite3.connect(CAMINHO_BANCO)

    print("\n" + "=" * 60)
    print(titulo)
    print("=" * 60)

    cursor = conexao.cursor()
    cursor.execute(sql)

    colunas = [item[0] for item in cursor.description]

    print(" | ".join(colunas))
    print("-" * 60)

    for linha in cursor.fetchall():
        print(" | ".join(
            str(valor) for valor in linha
        ))

    conexao.close()


# 1. FATURAMENTO TOTAL

sql_faturamento = """
SELECT
    ROUND(SUM(faturamento_realizado), 2) AS faturamento_total
FROM vw_vendas_detalhadas;
"""


# 2. LUCRO TOTAL

sql_lucro = """
SELECT
    ROUND(SUM(lucro_bruto), 2) AS lucro_total
FROM vw_vendas_detalhadas;
"""


# 3. FATURAMENTO MENSAL

sql_mensal = """
SELECT
    mes,
    ROUND(faturamento, 2) AS faturamento,
    ROUND(lucro, 2) AS lucro
FROM vw_resumo_mensal
ORDER BY mes;
"""


# 4. TOP 10 PRODUTOS

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


# 5. DESEMPENHO DOS VENDEDORES

sql_vendedores = """
SELECT
    vendedor,
    COUNT(DISTINCT id_venda) AS vendas_realizadas,
    ROUND(SUM(faturamento_realizado), 2) AS faturamento,
    ROUND(SUM(lucro_bruto), 2) AS lucro
FROM vw_vendas_detalhadas
WHERE status = 'Concluida'
GROUP BY vendedor
ORDER BY faturamento DESC;
"""
# 6. FATURAMENTO POR CATEGORIA
sql_categorias = """
SELECT
    categoria,
    ROUND(SUM(faturamento_realizado), 2) AS faturamento,
    ROUND(SUM(lucro_bruto), 2) AS lucro
FROM vw_vendas_detalhadas
GROUP BY categoria
ORDER BY faturamento DESC;
"""


# 7. FATURAMENTO POR ESTADO
sql_estados = """
SELECT
    estado,
    ROUND(SUM(faturamento_realizado), 2) AS faturamento
FROM vw_vendas_detalhadas
GROUP BY estado
ORDER BY faturamento DESC;
"""


# 8. VENDAS POR STATUS
sql_status = """
SELECT
    status,
    COUNT(DISTINCT id_venda) AS quantidade_vendas
FROM vw_vendas_detalhadas
GROUP BY status
ORDER BY quantidade_vendas DESC;
"""


# 9. TOP 10 CLIENTES
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

if __name__ == "__main__":

  if __name__ == "__main__":

    executar_consulta("1. FATURAMENTO TOTAL", sql_faturamento)

    executar_consulta("2. LUCRO TOTAL", sql_lucro)

    executar_consulta("3. FATURAMENTO MENSAL", sql_mensal)

    executar_consulta("4. TOP 10 PRODUTOS", sql_produtos)

    executar_consulta("5. DESEMPENHO DOS VENDEDORES", sql_vendedores)

    executar_consulta("6. FATURAMENTO POR CATEGORIA", sql_categorias)

    executar_consulta("7. FATURAMENTO POR ESTADO", sql_estados)

    executar_consulta("8. VENDAS POR STATUS", sql_status)

    executar_consulta("9. TOP 10 CLIENTES", sql_clientes)
    
    


