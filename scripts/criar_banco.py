
import sqlite3
import csv
from pathlib import Path

# ==========================================
# PROJETO BI - TECHSTORE
# CRIACAO DO BANCO DE DADOS
# ==========================================

PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_DADOS = PASTA_PROJETO / "dados"
PASTA_TRATADOS = PASTA_DADOS / "tratados"

CAMINHO_BANCO = PASTA_DADOS / "techstore.db"


def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def carregar_csv(nome):
    caminho = PASTA_TRATADOS / nome

    if not caminho.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {caminho}"
        )

    with open(caminho, "r", encoding="utf-8-sig", newline="") as arquivo:
        return list(csv.DictReader(arquivo))


def criar_tabelas(conexao):

    cursor = conexao.cursor()

    print("\nCRIANDO AS TABELAS...")

    cursor.executescript("""
        DROP VIEW IF EXISTS vw_resumo_mensal;
        DROP VIEW IF EXISTS vw_vendas_detalhadas;

        DROP TABLE IF EXISTS itens_venda;
        DROP TABLE IF EXISTS vendas;
        DROP TABLE IF EXISTS vendedores;
        DROP TABLE IF EXISTS produtos;
        DROP TABLE IF EXISTS clientes;

        CREATE TABLE clientes (
            id_cliente INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            cidade TEXT NOT NULL,
            estado TEXT NOT NULL
        );

        CREATE TABLE produtos (
            id_produto INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            preco REAL NOT NULL CHECK(preco > 0),
            custo REAL NOT NULL CHECK(custo > 0 AND custo < preco)
        );

        CREATE TABLE vendedores (
            id_vendedor INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            regiao TEXT NOT NULL
        );

        CREATE TABLE vendas (
            id_venda INTEGER PRIMARY KEY,
            id_cliente INTEGER NOT NULL,
            id_vendedor INTEGER NOT NULL,
            data_venda TEXT NOT NULL,
            status TEXT NOT NULL CHECK(
                status IN ('Concluida', 'Cancelada', 'Pendente')
            ),

            FOREIGN KEY (id_cliente)
                REFERENCES clientes(id_cliente),

            FOREIGN KEY (id_vendedor)
                REFERENCES vendedores(id_vendedor)
        );

        CREATE TABLE itens_venda (
            id_item INTEGER PRIMARY KEY,
            id_venda INTEGER NOT NULL,
            id_produto INTEGER NOT NULL,
            quantidade INTEGER NOT NULL CHECK(quantidade > 0),
            preco_unitario REAL NOT NULL CHECK(preco_unitario > 0),

            FOREIGN KEY (id_venda)
                REFERENCES vendas(id_venda),

            FOREIGN KEY (id_produto)
                REFERENCES produtos(id_produto),

            UNIQUE(id_venda, id_produto)
        );

        CREATE INDEX idx_vendas_data
        ON vendas(data_venda);

        CREATE INDEX idx_vendas_cliente
        ON vendas(id_cliente);

        CREATE INDEX idx_vendas_vendedor
        ON vendas(id_vendedor);

        CREATE INDEX idx_itens_venda
        ON itens_venda(id_venda);
    """)

    print("Tabelas e indices criados!")


def inserir_dados(conexao):

    cursor = conexao.cursor()

    print("\nIMPORTANDO OS DADOS...")

    clientes = carregar_csv("clientes_tratados.csv")
    produtos = carregar_csv("produtos_tratados.csv")
    vendedores = carregar_csv("vendedores_tratados.csv")
    vendas = carregar_csv("vendas_tratadas.csv")
    itens = carregar_csv("itens_tratados.csv")

    cursor.executemany("""
        INSERT INTO clientes
        (id_cliente, nome, cidade, estado)
        VALUES (?, ?, ?, ?)
    """, [
        (
            int(r["id_cliente"]),
            r["nome"],
            r["cidade"],
            r["estado"]
        )
        for r in clientes
    ])

    cursor.executemany("""
        INSERT INTO produtos
        (id_produto, nome, categoria, preco, custo)
        VALUES (?, ?, ?, ?, ?)
    """, [
        (
            int(r["id_produto"]),
            r["nome"],
            r["categoria"],
            float(r["preco"]),
            float(r["custo"])
        )
        for r in produtos
    ])

    cursor.executemany("""
        INSERT INTO vendedores
        (id_vendedor, nome, regiao)
        VALUES (?, ?, ?)
    """, [
        (
            int(r["id_vendedor"]),
            r["nome"],
            r["regiao"]
        )
        for r in vendedores
    ])

    cursor.executemany("""
        INSERT INTO vendas
        (id_venda, id_cliente, id_vendedor, data_venda, status)
        VALUES (?, ?, ?, ?, ?)
    """, [
        (
            int(r["id_venda"]),
            int(r["id_cliente"]),
            int(r["id_vendedor"]),
            r["data_venda"][:10],
            r["status"]
        )
        for r in vendas
    ])

    cursor.executemany("""
        INSERT INTO itens_venda
        (id_item, id_venda, id_produto, quantidade, preco_unitario)
        VALUES (?, ?, ?, ?, ?)
    """, [
        (
            int(r["id_item"]),
            int(r["id_venda"]),
            int(r["id_produto"]),
            int(r["quantidade"]),
            float(r["preco_unitario"])
        )
        for r in itens
    ])

    print("Clientes importados:", len(clientes))
    print("Produtos importados:", len(produtos))
    print("Vendedores importados:", len(vendedores))
    print("Vendas importadas:", len(vendas))
    print("Itens importados:", len(itens))


def criar_views(conexao):

    print("\nCRIANDO CONSULTAS SALVAS...")

    conexao.executescript("""
        CREATE VIEW vw_vendas_detalhadas AS

        SELECT
            v.id_venda,
            v.data_venda,
            v.status,
            c.nome AS cliente,
            c.cidade,
            c.estado,
            vd.nome AS vendedor,
            p.nome AS produto,
            p.categoria,
            i.quantidade,
            i.preco_unitario,

            (i.quantidade * i.preco_unitario)
                AS valor_item,

            (i.quantidade * p.custo)
                AS custo_item,

            CASE
                WHEN v.status = 'Concluida'
                THEN i.quantidade * i.preco_unitario
                ELSE 0
            END AS faturamento_realizado,

            CASE
                WHEN v.status = 'Concluida'
                THEN i.quantidade * (i.preco_unitario - p.custo)
                ELSE 0
            END AS lucro_bruto

        FROM itens_venda i

        INNER JOIN vendas v
            ON i.id_venda = v.id_venda

        INNER JOIN clientes c
            ON v.id_cliente = c.id_cliente

        INNER JOIN vendedores vd
            ON v.id_vendedor = vd.id_vendedor

        INNER JOIN produtos p
            ON i.id_produto = p.id_produto;


        CREATE VIEW vw_resumo_mensal AS

        SELECT
            substr(data_venda, 1, 7) AS mes,

            COUNT(DISTINCT id_venda) AS quantidade_vendas,

            SUM(faturamento_realizado) AS faturamento,

            SUM(lucro_bruto) AS lucro

        FROM vw_vendas_detalhadas

        GROUP BY substr(data_venda, 1, 7);
    """)

    print("Views criadas com sucesso!")


def verificar_banco(conexao):

    cursor = conexao.cursor()

    print("\nVALIDANDO O BANCO DE DADOS...")

    tabelas = [
        "clientes",
        "produtos",
        "vendedores",
        "vendas",
        "itens_venda"
    ]

    for tabela in tabelas:

        quantidade = cursor.execute(
            f"SELECT COUNT(*) FROM {tabela}"
        ).fetchone()[0]

        print(f"{tabela}: {quantidade} registros")

    erros = cursor.execute(
        "PRAGMA foreign_key_check"
    ).fetchall()

    print("\nVerificacao de chaves estrangeiras:")

    if erros:
        print("ERRO: Foram encontrados relacionamentos invalidos.")
        for erro in erros:
            print(erro)
        raise ValueError("Banco possui erros de integridade.")

    print("Nenhum erro de integridade encontrado!")

    faturamento = cursor.execute("""
        SELECT SUM(faturamento_realizado)
        FROM vw_vendas_detalhadas
    """).fetchone()[0]

    lucro = cursor.execute("""
        SELECT SUM(lucro_bruto)
        FROM vw_vendas_detalhadas
    """).fetchone()[0]

    print(f"\nFaturamento: R$ {faturamento:,.2f}")
    print(f"Lucro bruto: R$ {lucro:,.2f}")


def executar():

    print("\n===================================")
    print("BANCO DE DADOS TECHSTORE")
    print("===================================")

    conexao = conectar()

    try:
        with conexao:
            criar_tabelas(conexao)
            inserir_dados(conexao)
            criar_views(conexao)
            verificar_banco(conexao)

        print("\n===================================")
        print("BANCO CRIADO COM SUCESSO!")
        print("===================================")
        print(f"Local: {CAMINHO_BANCO}")

    except Exception:
        print("\nERRO AO CRIAR O BANCO DE DADOS.")
        raise

    finally:
        conexao.close()


if __name__ == "__main__":
    executar()
