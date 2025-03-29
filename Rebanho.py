import requests
import pandas as pd

# URL da API
url = "https://apisidra.ibge.gov.br/values/t/3939/n1/all/v/all/p/all/c79/2670"

# Requisição GET
response = requests.get(url)

# Verificando o status
if response.status_code == 200:
    # Convertendo para JSON
    data_json = response.json()
    
    # Criando uma lista para armazenar os dados estruturados
    data_list = []
    
    # A primeira linha do JSON contém metadados (nomes das colunas)
    colunas = data_json[0]
    
    # Iterar sobre os dados a partir do índice 1 (ignorando os metadados)
    for item in data_json[1:]:
        data_list.append(item)
    
    # Convertendo para DataFrame
    df = pd.DataFrame(data_list)
    
    # Renomeando colunas para facilitar a leitura
    df.rename(columns={
        "NC": "territorio",
        "NN": "nome_territorio",
        "V": "variavel",
        "D1C": "periodo",
        "D1N": "ano",
        "D2C": "classificacao",
        "D2N": "descricao_classificacao",
        "D3C": "categoria",
        "D3N": "descricao_categoria",
        "MC": "unidade_medida",
        "MN": "descricao_unidade",
        "V": "valor"
    }, inplace=True)

    # Convertendo valores numéricos corretamente
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")

    # Exibir as 5 primeiras linhas do DataFrame
    print(df.head())
    
else:
    print(f"Erro na requisição: {response.status_code}")

df[["valor", "categoria"]].rename(columns={"categoria": "ano"})

# Selecionar e renomear
df_selecionado = (
    df[["valor", "categoria"]]
    .rename(columns={"categoria": "ano"})
    .sort_values("ano")
    .assign(
        variacao_percentual=lambda x: (x["valor"].pct_change() * 100).round(2)
    )
)

import matplotlib.pyplot as plt
import seaborn as sns

# Selecionar e renomear os dados para análise
df_selecionado = (
    df[["valor", "categoria"]]
    .rename(columns={"categoria": "ano"})
    .sort_values("ano")
    .assign(
        variacao_percentual=lambda x: (x["valor"].pct_change() * 100).round(2)
    )
)

# Criando os gráficos
fig, axes = plt.subplots(2, 1, figsize=(10, 12))
#fig, axes = plt.subplots(1, 2, figsize=(18, 6))  # Agora 1 linha e 2 colunas

# Gráfico 1: Valor de cabeças do rebanho por ano (dividido por 1 milhão para facilitar a leitura)
sns.lineplot(data=df_selecionado, x="ano", y=df_selecionado["valor"] / 1_000_000, marker="o", color="g", ax=axes[0])
axes[0].set_title("Efetivo Bovino por Ano (em milhões)", fontsize=14)
axes[0].set_xlabel("Ano", fontsize=12)
axes[0].set_ylabel("Número de Cabeças (Milhões)", fontsize=12)
axes[0].grid(True, linestyle='--', color='gray', alpha=0.3)
axes[0].tick_params(axis='x', rotation=90)

# Gráfico 2: Variação Percentual Anual
sns.lineplot(data=df_selecionado, x="ano", y="variacao_percentual", marker="o", color="b", ax=axes[1])
axes[1].set_title("Variação Percentual Anual", fontsize=14)
axes[1].set_xlabel("Ano", fontsize=12)
axes[1].set_ylabel("Percentual (%)", fontsize=12)
axes[1].axhline(0, color="red", linestyle="-", linewidth=1)
axes[1].grid(True, linestyle='--', color='gray', alpha=0.3)
axes[1].tick_params(axis='x', rotation=90)

# Salvar a imagem em alta qualidade
plt.savefig('.vscode\\Image\\Rebanho-Variação.png', dpi=300, bbox_inches='tight')

# Exibindo os gráficos
plt.tight_layout()
plt.show()