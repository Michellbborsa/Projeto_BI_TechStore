
import pandas as pd
from pathlib import Path

# ==========================================
# PROJETO BI - TECHSTORE
# PROCESSO ETL
# ==========================================

PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_DADOS = PASTA_PROJETO / "dados"
PASTA_TRATADOS = PASTA_DADOS / "tratados"

PASTA_TRATADOS.mkdir(parents=True, exist_ok=True)


def carregar_csv(nome):
    caminho = PASTA_DADOS / nome

    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {caminho}")

    return pd.read_csv(caminho, encoding="utf-8-sig")


def verificar_chaves(df, coluna, nome):
    if df[coluna].isna().any():
        raise ValueError(f"Existem IDs vazios em {nome}.")

    if df[coluna].duplicated().any():
        raise ValueError(f"Existem IDs duplicados em {nome}.")


def salvar_csv(df, nome):
    caminho = PASTA_TRATADOS / nome
    df.to_csv(caminho, index=False, encoding="utf-8-sig")
    print(f"Arquivo tratado salvo: {nome}")


def executar_etl():

    print("\n===================================")
    print("INICIANDO PROCESSO ETL - TECHSTORE")
    print("===================================\n")

    # --------------------------------------
    # 1. EXTRACAO
    # --------------------------------------

    print("1. EXTRAINDO OS DADOS...")

    clientes = carregar_csv("clientes.csv")
    produtos = carregar_csv("produtos.csv")
    vendedores = carregar_csv("vendedores.csv")
    vendas = carregar_csv("vendas.csv")
    itens = carregar_csv("itens_venda.csv")

    tabelas = {
        "clientes": clientes,
        "produtos": produtos,
        "vendedores": vendedores,
        "vendas": vendas,
        "itens": itens
    }

    for nome, df in tabelas.items():
        print(f"{nome}: {len(df)} registros")

    # --------------------------------------
    # 2. TRANSFORMACAO
    # --------------------------------------

    print("\n2. TRANSFORMANDO OS DADOS...")

    # Remover espacos desnecessarios dos textos
    for df in tabelas.values():
        colunas_texto = df.select_dtypes(
    include=["object", "str"]
).columns

        for coluna in colunas_texto:
            df[coluna] = df[coluna].str.strip()

    # Verificar chaves primarias
    verificar_chaves(clientes, "id_cliente", "clientes")
    verificar_chaves(produtos, "id_produto", "produtos")
    verificar_chaves(vendedores, "id_vendedor", "vendedores")
    verificar_chaves(vendas, "id_venda", "vendas")
    verificar_chaves(itens, "id_item", "itens")

    # Tratar tipos numericos
    produtos["preco"] = pd.to_numeric(
        produtos["preco"], errors="coerce"
    )

    produtos["custo"] = pd.to_numeric(
        produtos["custo"], errors="coerce"
    )

    itens["quantidade"] = pd.to_numeric(
        itens["quantidade"], errors="coerce"
    )

    itens["preco_unitario"] = pd.to_numeric(
        itens["preco_unitario"], errors="coerce"
    )

    # Validar valores numericos
    colunas_numericas = [
        produtos["preco"],
        produtos["custo"],
        itens["quantidade"],
        itens["preco_unitario"]
    ]

    if any(coluna.isna().any() for coluna in colunas_numericas):
        raise ValueError("Existem valores numericos invalidos.")

    if any((coluna <= 0).any() for coluna in colunas_numericas):
        raise ValueError("Existem valores menores ou iguais a zero.")

    if (produtos["custo"] >= produtos["preco"]).any():
        raise ValueError("Existem produtos com custo maior ou igual ao preco.")

    # Converter datas
    vendas["data_venda"] = pd.to_datetime(
        vendas["data_venda"], errors="coerce"
    )

    if vendas["data_venda"].isna().any():
        raise ValueError("Existem datas invalidas.")

    # Validar status
    status_permitidos = {
        "Concluida", "Cancelada", "Pendente"
    }

    if not vendas["status"].isin(status_permitidos).all():
        raise ValueError("Existem status de vendas invalidos.")

    # Verificar relacionamentos
    if not vendas["id_cliente"].isin(clientes["id_cliente"]).all():
        raise ValueError("Venda com cliente inexistente.")

    if not vendas["id_vendedor"].isin(vendedores["id_vendedor"]).all():
        raise ValueError("Venda com vendedor inexistente.")

    if not itens["id_venda"].isin(vendas["id_venda"]).all():
        raise ValueError("Item com venda inexistente.")

    if not itens["id_produto"].isin(produtos["id_produto"]).all():
        raise ValueError("Item com produto inexistente.")

    # --------------------------------------
    # 3. INTEGRACAO DAS TABELAS
    # --------------------------------------

    print("\n3. INTEGRANDO AS TABELAS...")

    fato_vendas = itens.merge(
        vendas,
        on="id_venda",
        how="left",
        validate="many_to_one"
    )

    fato_vendas = fato_vendas.merge(
        produtos,
        on="id_produto",
        how="left",
        validate="many_to_one",
        suffixes=("_item", "_produto")
    )

    # --------------------------------------
    # 4. CALCULO DOS INDICADORES
    # --------------------------------------

    print("\n4. CALCULANDO OS INDICADORES...")

    fato_vendas["valor_bruto_item"] = (
        fato_vendas["quantidade"]
        * fato_vendas["preco_unitario"]
    )

    fato_vendas["custo_total_item"] = (
        fato_vendas["quantidade"]
        * fato_vendas["custo"]
    )

    vendas_concluidas = (
        fato_vendas["status"] == "Concluida"
    )

    fato_vendas["faturamento_realizado"] = (
        fato_vendas["valor_bruto_item"]
        .where(vendas_concluidas, 0)
    )

    fato_vendas["custo_realizado"] = (
        fato_vendas["custo_total_item"]
        .where(vendas_concluidas, 0)
    )

    fato_vendas["lucro_bruto"] = (
        fato_vendas["faturamento_realizado"]
        - fato_vendas["custo_realizado"]
    )

    fato_vendas["mes"] = (
        fato_vendas["data_venda"].dt.to_period("M").astype(str)
    )

    # --------------------------------------
    # 5. RESUMO MENSAL
    # --------------------------------------

    print("\n5. GERANDO RESUMO MENSAL...")

    resumo_mensal = (
        fato_vendas
        .groupby("mes")
        .agg(
            quantidade_vendas=("id_venda", "nunique"),
            quantidade_itens=("quantidade", "sum"),
            faturamento=("faturamento_realizado", "sum"),
            custo=("custo_realizado", "sum"),
            lucro=("lucro_bruto", "sum")
        )
        .reset_index()
    )

    # --------------------------------------
    # 6. CARGA DOS DADOS TRATADOS
    # --------------------------------------

    print("\n6. SALVANDO OS DADOS TRATADOS...")

    # Preservar os arquivos originais
    for nome, df in [
        ("clientes_tratados.csv", clientes),
        ("produtos_tratados.csv", produtos),
        ("vendedores_tratados.csv", vendedores),
        ("vendas_tratadas.csv", vendas),
        ("itens_tratados.csv", itens)
    ]:
        salvar_csv(df, nome)

    fato_saida = fato_vendas.copy()
    fato_saida["data_venda"] = (
        fato_saida["data_venda"].dt.strftime("%Y-%m-%d")
    )

    salvar_csv(fato_saida, "fato_vendas.csv")
    salvar_csv(resumo_mensal, "resumo_mensal.csv")

    # --------------------------------------
    # 7. RESULTADO FINAL
    # --------------------------------------

    faturamento = fato_vendas["faturamento_realizado"].sum()
    lucro = fato_vendas["lucro_bruto"].sum()

    print("\n===================================")
    print("PROCESSO ETL CONCLUIDO!")
    print("===================================")

    print(f"Registros integrados: {len(fato_vendas)}")
    print(f"Faturamento realizado: R$ {faturamento:,.2f}")
    print(f"Lucro bruto: R$ {lucro:,.2f}")

    print(f"\nArquivos salvos em: {PASTA_TRATADOS}")


if __name__ == "__main__":
    executar_etl()
