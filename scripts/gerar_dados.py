
import csv
import random
from datetime import date, timedelta
from pathlib import Path

# ==========================================
# PROJETO: BUSINESS INTELLIGENCE - TECHSTORE
# GERADOR AUTOMATICO DE BASE DE DADOS
# ==========================================

random.seed(42)

# Local onde os arquivos CSV serao salvos
PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_DADOS = PASTA_PROJETO / "dados"
PASTA_DADOS.mkdir(exist_ok=True)


def salvar_csv(nome_arquivo, colunas, registros):
    """Salva uma lista de registros em um arquivo CSV."""
    caminho = PASTA_DADOS / nome_arquivo

    with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        escritor.writerows(registros)

    print(f"Arquivo gerado: {caminho.name} ({len(registros)} registros)")


# ==========================================
# 1. CADASTRO DE CLIENTES
# ==========================================

nomes = [
    "Ana", "Joao", "Maria", "Pedro", "Lucas",
    "Julia", "Carlos", "Mariana", "Gabriel", "Beatriz",
    "Rafael", "Camila", "Felipe", "Larissa", "Bruno"
]

sobrenomes = [
    "Silva", "Santos", "Oliveira", "Souza", "Costa",
    "Pereira", "Rodrigues", "Almeida", "Lima", "Ferreira"
]

cidades = [
    ("Uberlandia", "MG"),
    ("Sao Paulo", "SP"),
    ("Belo Horizonte", "MG"),
    ("Goiania", "GO"),
    ("Brasilia", "DF"),
    ("Campinas", "SP"),
    ("Curitiba", "PR"),
    ("Rio de Janeiro", "RJ"),
    ("Salvador", "BA"),
    ("Ribeirao Preto", "SP")
]

clientes = []

for i in range(1, 1001):
    cidade, estado = random.choice(cidades)

    clientes.append({
        "id_cliente": i,
        "nome": f"{random.choice(nomes)} {random.choice(sobrenomes)}",
        "cidade": cidade,
        "estado": estado
    })


# ==========================================
# 2. CADASTRO DE PRODUTOS
# ==========================================

catalogo = [
    ("Smartphone", "Celulares", 2500, 1400),
    ("Notebook", "Informatica", 4200, 2900),
    ("Tablet", "Informatica", 1800, 1100),
    ("Smart TV", "Televisores", 3200, 2200),
    ("Fone Bluetooth", "Acessorios", 250, 100),
    ("Mouse Gamer", "Acessorios", 180, 70),
    ("Teclado Mecanico", "Acessorios", 350, 160),
    ("Monitor", "Informatica", 1200, 750),
    ("Smartwatch", "Wearables", 900, 500),
    ("Caixa de Som", "Audio", 450, 230),
    ("Headset", "Audio", 380, 190),
    ("Webcam", "Acessorios", 300, 150),
    ("Impressora", "Informatica", 950, 600),
    ("Console", "Games", 3800, 2800),
    ("Controle Gamer", "Games", 400, 220),
    ("Camera Digital", "Fotografia", 2100, 1400),
    ("Roteador", "Redes", 280, 130),
    ("SSD 1TB", "Informatica", 550, 300),
    ("HD Externo", "Informatica", 420, 240),
    ("Microfone", "Audio", 600, 320),
    ("Carregador", "Acessorios", 120, 45),
    ("Cabo HDMI", "Acessorios", 60, 20),
    ("Power Bank", "Acessorios", 180, 80),
    ("Projetor", "Eletronicos", 2500, 1700),
    ("Drone", "Eletronicos", 4500, 3100),
    ("Placa de Video", "Informatica", 3500, 2500),
    ("Processador", "Informatica", 1800, 1200),
    ("Memoria RAM", "Informatica", 450, 250),
    ("Notebook Gamer", "Informatica", 6500, 4700),
    ("Smart Speaker", "Audio", 500, 280)
]

produtos = []

for i, produto in enumerate(catalogo, start=1):
    nome, categoria, preco, custo = produto

    produtos.append({
        "id_produto": i,
        "nome": nome,
        "categoria": categoria,
        "preco": preco,
        "custo": custo
    })


# ==========================================
# 3. CADASTRO DE VENDEDORES
# ==========================================

vendedores = []

for i in range(1, 11):
    vendedores.append({
        "id_vendedor": i,
        "nome": f"Vendedor {i}",
        "regiao": random.choice([
            "Sudeste", "Sul", "Centro-Oeste",
            "Norte", "Nordeste"
        ])
    })


# ==========================================
# 4. GERACAO DE VENDAS
# ==========================================

vendas = []
itens_venda = []

data_inicial = date(2025, 1, 1)
data_final = date(2026, 10, 31)

intervalo_dias = (data_final - data_inicial).days

for id_venda in range(1, 5001):

    data_venda = data_inicial + timedelta(
        days=random.randint(0, intervalo_dias)
    )

    status = random.choices(
        ["Concluida", "Cancelada", "Pendente"],
        weights=[85, 10, 5],
        k=1
    )[0]

    vendas.append({
        "id_venda": id_venda,
        "id_cliente": random.randint(1, 1000),
        "id_vendedor": random.randint(1, 10),
        "data_venda": data_venda.isoformat(),
        "status": status
    })

    quantidade_itens = random.randint(1, 4)

    produtos_escolhidos = random.sample(
        produtos, quantidade_itens
    )

    for produto in produtos_escolhidos:
        itens_venda.append({
            "id_item": len(itens_venda) + 1,
            "id_venda": id_venda,
            "id_produto": produto["id_produto"],
            "quantidade": random.randint(1, 5),
            "preco_unitario": produto["preco"]
        })


# ==========================================
# 5. SALVAR TODOS OS ARQUIVOS
# ==========================================

print("\nINICIANDO GERACAO DA BASE DE DADOS...\n")

salvar_csv(
    "clientes.csv",
    ["id_cliente", "nome", "cidade", "estado"],
    clientes
)

salvar_csv(
    "produtos.csv",
    ["id_produto", "nome", "categoria", "preco", "custo"],
    produtos
)

salvar_csv(
    "vendedores.csv",
    ["id_vendedor", "nome", "regiao"],
    vendedores
)

salvar_csv(
    "vendas.csv",
    ["id_venda", "id_cliente", "id_vendedor", "data_venda", "status"],
    vendas
)

salvar_csv(
    "itens_venda.csv",
    ["id_item", "id_venda", "id_produto", "quantidade", "preco_unitario"],
    itens_venda
)

print("\n===================================")
print("BASE DE DADOS GERADA COM SUCESSO!")
print("===================================")
print(f"Clientes: {len(clientes)}")
print(f"Produtos: {len(produtos)}")
print(f"Vendedores: {len(vendedores)}")
print(f"Vendas: {len(vendas)}")
print(f"Itens de venda: {len(itens_venda)}")
print(f"\nArquivos salvos em: {PASTA_DADOS}")
