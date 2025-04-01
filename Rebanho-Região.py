import requests
import pandas as pd

# URL da API
url = "https://apisidra.ibge.gov.br/values/t/3939/n2/all/v/all/p/all/c79/2670"

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
    df = pd.DataFrame(data_list)

    # Convertendo valores numéricos corretamente (se a coluna existir)
    if "Valor" in df.columns:  # Confirme o nome correto no JSON
        df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")

    # Exibir as 5 primeiras linhas do DataFrame
    print(df.head())

else:
    print(f"Erro na requisição: {response.status_code}")


# Selecionar e calcular a variação percentual dentro de cada Grande Região
df_selecionado = (
    df[["Valor", "Grande Região", "Ano"]]
    .rename(columns={"Grande Região": "Região"})
    .sort_values(["Região", "Ano"])
    .assign(
        variacao_percentual=lambda x: x.groupby("Região")["Valor"].pct_change() * 100
    )
)

import matplotlib.pyplot as plt
import seaborn as sns

# Criando a figura
fig, ax = plt.subplots(figsize=(12, 8))  # Apenas um gráfico

# Gráfico: Valor de cabeças do rebanho por ano e por Grande Região
sns.lineplot(
    data=df_selecionado, 
    x="Ano", 
    y=df_selecionado["Valor"] / 1_000_000, 
    hue="Região", 
    marker="o", 
    palette="tab10", 
    ax=ax
)

# Configurações do gráfico
ax.set_title("Efetivo Bovino por Ano e Região (em milhões)", fontsize=14)
ax.set_xlabel("Ano", fontsize=12)
ax.set_ylabel("Número de Cabeças (Milhões)", fontsize=12)
ax.grid(True, linestyle="--", color="gray", alpha=0.3)
ax.tick_params(axis="x", rotation=90)
ax.legend(title="Região")

# Exibir o gráfico
plt.show()


# Gráfico de barras
# Filtrando apenas os dados do ano de 2023 e ordenando em ordem decrescente
df_2023 = df_selecionado[df_selecionado["Ano"] == "2023"].sort_values("Valor", ascending=False)

# Criando a figura
fig, ax = plt.subplots(figsize=(10, 6))

# Criando o gráfico de barras
barplot = sns.barplot(
    data=df_2023, 
    x="Região", 
    y=df_2023["Valor"] / 1_000_000,  # Convertendo para milhões
    palette="inferno", 
    ax=ax,
    order=df_2023["Região"]
)

# Adicionando os valores no topo das barras
for bar in barplot.containers:
    ax.bar_label(bar, fmt="%.1f", fontsize=12, padding=0)

# Configurações do gráfico
ax.set_title("Efetivo bovino por região", fontsize=18, fontweight="bold", fontname="Fira Code")
plt.suptitle("Número de cabeças bovinas em 2023 (em milhões)", fontsize=14, color="gray", fontname="Fira Code")
ax.set_xlabel("")
ax.set_ylabel("")  # Corrigido para remover o rótulo do eixo Y
ax.set_yticks([])  # Remove os ticks do eixo Y
ax.set_yticklabels([])  # Remove os valores do eixo Y

# Ajustando a posição do figtext para que seja visível
plt.figtext(0.5, 0.01, "Dados: IBGE (2025) | Elaboração: @italo.m.m", 
            ha="center", fontsize=10, color="gray", fontname="Fira Code")

# Exibir o gráfico
plt.show()


# Exibir o gráfico interativo
fig.show()


import plotly.express as px
import webbrowser

# Criando o gráfico interativo com Plotly
fig = px.line(
    df_selecionado, 
    x="Ano", 
    y=df_selecionado["Valor"] / 1_000_000, 
    color="Região", 
    markers=True, 
    title="Efetivo Bovino por Ano e Região (em milhões)",
    labels={"Ano": "Ano", "y": "Número de Cabeças (Milhões)", "Região": "Região"},
    template="plotly_white"
)

# Salvar o gráfico como um arquivo HTML
file_path = ".vscode\\Image\\grafico_interativo.html"
fig.write_html(file_path)

# Abrir no Google Chrome
webbrowser.get("chrome").open(file_path)




import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Definir a ordem desejada para as regiões
ordem_regioes = ["Centro-Oeste", "Norte", "Sudeste", "Nordeste", "Sul"]

# Garantir que a variável Região tenha a ordem definida
df_selecionado["Região"] = pd.Categorical(df_selecionado["Região"], categories=ordem_regioes, ordered=True)

# Definir paleta de cores única
cores = sns.color_palette("inferno", n_colors=len(ordem_regioes))

# Criando a figura com dois subplots empilhados
fig, axes = plt.subplots(2, 1, figsize=(12, 12), sharex=False)

# --- Gráfico 1: Linha (Evolução do efetivo bovino por ano e região) ---
sns.lineplot(
    data=df_selecionado, 
    x="Ano", 
    y=df_selecionado["Valor"] / 1_000_000, 
    hue="Região", 
    marker="o", 
    palette=cores,  # Aplicando as cores na ordem correta
    ax=axes[0]
)

# Configurações do gráfico de linha
axes[0].set_title("Comportamento do efetivo bovino por ano e região", fontsize=14, fontweight="bold", fontname="Fira Code")
axes[0].set_xlabel("")
axes[0].set_ylabel("Número de Cabeças (Milhões)", fontsize=12)
axes[0].grid(True, linestyle="--", color="gray", alpha=0.3)
axes[0].tick_params(axis="x", rotation=90)
axes[0].legend(title="Região", loc="best")  # Mantém a ordem da legenda correta

# --- Gráfico 2: Barras (Efetivo bovino por região em 2023) ---
df_2023 = df_selecionado[df_selecionado["Ano"] == "2023"].sort_values("Valor", ascending=False)

barplot = sns.barplot(
    data=df_2023, 
    x="Região", 
    y=df_2023["Valor"] / 1_000_000,  
    palette=cores,  # Aplicando as mesmas cores
    ax=axes[1],
    order=ordem_regioes  # Garantindo a ordem correta das barras
)

# Adicionando os valores no topo das barras
for bar in barplot.containers:
    axes[1].bar_label(bar, fmt="%.1f", fontsize=12, padding=3)

# Configurações do gráfico de barras
axes[1].set_title("Efetivo bovino por região (2023)", fontsize=14, fontweight="bold", fontname="Fira Code")
axes[1].set_xlabel("")
axes[1].set_ylabel("")
axes[1].set_yticks([])
axes[1].set_yticklabels([])

# Ajustando a posição do figtext
plt.figtext(0, 0, "Dados: IBGE (2025) | Elaboração: @italo.m.m", ha="left", fontsize=10, color="black", fontname="Fira Code")

# Ajuste do layout para evitar sobreposição
plt.tight_layout()

# Salvar a imagem em alta qualidade
plt.savefig('.vscode\\Image\\Rebanho-Região.png', dpi=300, bbox_inches='tight')

# Exibir os gráficos
plt.show()