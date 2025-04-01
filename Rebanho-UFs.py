import requests
import pandas as pd

# URL da API
url = "https://apisidra.ibge.gov.br/values/t/3939/n3/all/u/y/v/all/p/last%201/c79/2670"

# Requisição GET
response = requests.get(url)

# Verificando o status da requisição
if response.status_code == 200:
    # Convertendo para JSON
    data_json = response.json()
    
    # O primeiro item contém os nomes das colunas
    colunas = list(data_json[0].values())

    # Criando lista de dicionários a partir dos dados (ignorando o primeiro item)
    data_list = [dict(zip(colunas, item.values())) for item in data_json[1:]]

    # Criando DataFrame
    df_uf = pd.DataFrame(data_list)

    # Convertendo valores numéricos corretamente (se a coluna existir)
    if "Valor" in df_uf.columns:  # Confirme o nome correto no JSON
        df_uf["Valor"] = pd.to_numeric(df_uf["Valor"], errors="coerce")

    # Exibir as 5 primeiras linhas do DataFrame
    print(df_uf.head())

else:
    print(f"Erro na requisição: {response.status_code}")

df_uf1 = df_uf[["Valor", "Unidade da Federação"]]

# Calcular percentual de participação de cada UF
df_uf1["Percentual"] = (df_uf1["Valor"] / df_uf1["Valor"].sum() * 100).round(2)