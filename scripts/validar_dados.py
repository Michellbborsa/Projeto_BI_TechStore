 
import csv
from pathlib import Path
from datetime import date
from collections import Counter

# ==========================================
# PROJETO BI - TECHSTORE
# VALIDACAO DA QUALIDADE DOS DADOS
# ==========================================

PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_DADOS = PASTA_PROJETO / "dados"

resultados = []


def carregar_csv(nome):
    caminho = PASTA_DADOS / nome

    if not caminho.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {caminho}"
        )

    with open(caminho, "r", encoding="utf-8-sig", newline="") as arquivo:
        return list(csv.DictReader(arquivo))


def verificar(descricao, condicao, detalhe=""):
    status = "APROVADO" if condicao else "REPROVADO"
    resultados.append(condicao)

    print(f"[{status}] {descricao}")

    if detalhe:
        print(f"          {detalhe}")


def validar_id_unico(registros, campo):
    ids = [registro[campo] for registro in registros]
    return len(ids) == len(set(ids))


def executar_validacao():

    print("\n======================================")
    print(" VALIDACAO DOS DADOS - TECHSTORE")
    print("======================================\n")

    clientes = carregar_csv("clientes.csv")
    produtos = carregar_csv("produtos.csv")
    vendedores = carregar_csv("vendedores.csv")
    vendas = carregar_csv("vendas.csv")
    itens = carregar_csv("itens_venda.csv")

    # --------------------------------------
    # 1. QUANTIDADE DE REGISTROS
    # --------------------------------------

    print("\n1. QUANTIDADE DE REGISTROS")

    verificar(
        "Quantidade de clientes",
        len(clientes) == 1000,
        f"Encontrados: {len(clientes)}"
    )

    verificar(
        "Quantidade de produtos",
        len(produtos) == 30,
        f"Encontrados: {len(produtos)}"
    )

    verificar(
        "Quantidade de vendedores",
        len(vendedores) == 10,
        f"Encontrados: {len(vendedores)}"
    )

    verificar(
        "Quantidade de vendas",
        len(vendas) == 5000,
        f"Encontradas: {len(vendas)}"
    )

    verificar(
        "Existencia de itens de venda",
        len(itens) >= len(vendas),
        f"Encontrados: {len(itens)}"
    )

    # --------------------------------------
    # 2. CAMPOS VAZIOS
    # --------------------------------------

    print("\n2. VERIFICACAO DE CAMPOS VAZIOS")

    tabelas = {
        "Clientes": clientes,
        "Produtos": produtos,
        "Vendedores": vendedores,
        "Vendas": vendas,
        "Itens": itens
    }

    for nome, registros in tabelas.items():

        vazios = sum(
            1
            for registro in registros
            for valor in registro.values()
            if valor is None or valor.strip() == ""
        )

        verificar(
            f"Campos vazios - {nome}",
            vazios == 0,
            f"Total de campos vazios: {vazios}"
        )

    # --------------------------------------
    # 3. IDS DUPLICADOS
    # --------------------------------------

    print("\n3. VERIFICACAO DE DUPLICIDADES")

    chaves = [
        (clientes, "id_cliente"),
        (produtos, "id_produto"),
        (vendedores, "id_vendedor"),
        (vendas, "id_venda"),
        (itens, "id_item")
    ]

    for registros, campo in chaves:

        verificar(
            f"IDs unicos - {campo}",
            validar_id_unico(registros, campo)
        )

    # --------------------------------------
    # 4. INTEGRIDADE REFERENCIAL
    # --------------------------------------

    print("\n4. INTEGRIDADE REFERENCIAL")

    ids_clientes = {r["id_cliente"] for r in clientes}
    ids_produtos = {r["id_produto"] for r in produtos}
    ids_vendedores = {r["id_vendedor"] for r in vendedores}
    ids_vendas = {r["id_venda"] for r in vendas}

    verificar(
        "Clientes das vendas cadastrados",
        all(r["id_cliente"] in ids_clientes for r in vendas)
    )

    verificar(
        "Vendedores das vendas cadastrados",
        all(r["id_vendedor"] in ids_vendedores for r in vendas)
    )

    verificar(
        "Vendas dos itens cadastradas",
        all(r["id_venda"] in ids_vendas for r in itens)
    )

    verificar(
        "Produtos dos itens cadastrados",
        all(r["id_produto"] in ids_produtos for r in itens)
    )

    # --------------------------------------
    # 5. VALIDACAO DOS VALORES
    # --------------------------------------

    print("\n5. VALIDACAO DOS VALORES")

    produtos_por_id = {
        r["id_produto"]: r for r in produtos
    }

    verificar(
        "Precos dos produtos positivos",
        all(float(r["preco"]) > 0 for r in produtos)
    )

    verificar(
        "Custos dos produtos positivos",
        all(float(r["custo"]) > 0 for r in produtos)
    )

    verificar(
        "Custos inferiores aos precos",
        all(
            float(r["custo"]) < float(r["preco"])
            for r in produtos
        )
    )

    verificar(
        "Quantidades dos itens positivas",
        all(int(r["quantidade"]) > 0 for r in itens)
    )

    verificar(
        "Precos dos itens positivos",
        all(float(r["preco_unitario"]) > 0 for r in itens)
    )

    # --------------------------------------
    # 6. VALIDACAO DAS DATAS
    # --------------------------------------

    print("\n6. VALIDACAO DAS DATAS")

    datas = []

    try:
        datas = [
            date.fromisoformat(r["data_venda"])
            for r in vendas
        ]

        verificar(
            "Todas as datas sao validas",
            len(datas) == len(vendas)
        )

        verificar(
            "Datas dentro do periodo esperado",
            all(
                date(2025, 1, 1) <= d <= date(2026, 10, 31)
                for d in datas
            )
        )

    except ValueError:
        verificar("Datas validas", False)

    # --------------------------------------
    # 7. STATUS DAS VENDAS
    # --------------------------------------

    print("\n7. VALIDACAO DOS STATUS")

    status_permitidos = {
        "Concluida",
        "Cancelada",
        "Pendente"
    }

    verificar(
        "Status permitidos",
        all(r["status"] in status_permitidos for r in vendas)
    )

    # --------------------------------------
    # 8. QUANTIDADE DE ITENS POR VENDA
    # --------------------------------------

    print("\n8. ITENS POR VENDA")

    contagem_itens = Counter(
        r["id_venda"] for r in itens
    )

    verificar(
        "Todas as vendas possuem de 1 a 4 itens",
        all(
            1 <= contagem_itens[r["id_venda"]] <= 4
            for r in vendas
        )
    )

    # --------------------------------------
    # 9. CONSISTENCIA DOS PRODUTOS
    # --------------------------------------

    print("\n9. CONSISTENCIA DOS PRODUTOS")

    verificar(
        "Preco dos itens igual ao preco cadastrado",
        all(
            float(r["preco_unitario"])
            == float(produtos_por_id[r["id_produto"]]["preco"])
            for r in itens
        )
    )

    pares = [
        (r["id_venda"], r["id_produto"])
        for r in itens
    ]

    verificar(
        "Sem produtos repetidos na mesma venda",
        len(pares) == len(set(pares))
    )

    # --------------------------------------
    # 10. RESULTADO FINAL
    # --------------------------------------

    aprovados = sum(resultados)
    reprovados = len(resultados) - aprovados

    print("\n======================================")
    print(" RESULTADO FINAL DA VALIDACAO")
    print("======================================")

    print(f"Verificacoes realizadas: {len(resultados)}")
    print(f"Aprovadas: {aprovados}")
    print(f"Reprovadas: {reprovados}")

    if reprovados == 0:
        print("\nTODAS AS VALIDACOES FORAM APROVADAS!")
    else:
        print("\nATENCAO: EXISTEM PROBLEMAS NOS DADOS.")

    print("======================================\n")


if __name__ == "__main__":
    executar_validacao()
