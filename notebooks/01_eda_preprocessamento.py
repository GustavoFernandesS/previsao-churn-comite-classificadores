# %% [markdown]
# # Projeto A3 - Analise exploratoria e pre-processamento
#
# **Problema:** prever se um cliente de telecomunicacoes cancelara o servico.
#
# **Target:** `Churn`, onde `Yes` indica cancelamento e `No` indica permanencia.
#
# Nesta etapa, vamos conhecer a base, corrigir problemas nos dados e preparar
# conjuntos de treino e teste. A modelagem sera feita na proxima etapa.

# %%
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

sns.set_theme(style="whitegrid")
RANDOM_STATE = 42

# %% [markdown]
# ## 1. Carregamento dos dados
#
# O caminho abaixo funciona ao executar o notebook tanto na raiz do projeto
# quanto dentro da pasta `notebooks`.

# %%
possiveis_caminhos = [
    Path("../data/WA_Fn-UseC_-Telco-Customer-Churn.csv"),
    Path("data/WA_Fn-UseC_-Telco-Customer-Churn.csv"),
]

caminho_dados = next((p for p in possiveis_caminhos if p.exists()), None)
if caminho_dados is None:
    raise FileNotFoundError("Arquivo CSV nao encontrado na pasta data.")

df = pd.read_csv(caminho_dados)
print(f"Dimensoes da base: {df.shape[0]} linhas e {df.shape[1]} colunas")
df.head()

# %% [markdown]
# Cada linha representa um cliente. As features descrevem perfil, servicos
# contratados, forma de pagamento e valores cobrados.

# %%
df.info()

# %%
df.describe(include="all").T

# %% [markdown]
# ## 2. Verificacao da qualidade dos dados
#
# `TotalCharges` deveria ser numerica, mas foi carregada como texto porque
# possui espacos vazios. Esses espacos serao convertidos em valores ausentes.

# %%
print("Linhas duplicadas:", df.duplicated().sum())
print("Valores ausentes antes da conversao:", df.isna().sum().sum())
print("Espacos vazios em TotalCharges:", df["TotalCharges"].str.strip().eq("").sum())

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

print("Valores ausentes depois da conversao:")
df.isna().sum()[df.isna().sum() > 0]

# %% [markdown]
# Os valores ausentes de `TotalCharges` serao preenchidos pela mediana dentro
# do pipeline. Isso evita usar informacoes do conjunto de teste durante o
# treinamento.

# %% [markdown]
# ## 3. Analise do target
#
# A base possui mais clientes que permaneceram do que clientes que cancelaram.
# Portanto, alem da acuracia, sera importante avaliar recall e F1-score.

# %%
contagem_churn = df["Churn"].value_counts()
percentual_churn = df["Churn"].value_counts(normalize=True).mul(100).round(2)

pd.DataFrame({"Quantidade": contagem_churn, "Percentual": percentual_churn})

# %%
ax = sns.countplot(data=df, x="Churn", hue="Churn", palette="Set2", legend=False)
ax.set(title="Distribuicao do target Churn", xlabel="Cancelou?", ylabel="Clientes")
plt.show()

# %% [markdown]
# ## 4. Relacao das features com churn
#
# Os graficos abaixo ajudam a identificar perfis com maior proporcao de
# cancelamento. A altura representa a taxa media de churn em cada categoria.

# %%
df_eda = df.copy()
df_eda["ChurnNumerico"] = df_eda["Churn"].map({"No": 0, "Yes": 1})

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.barplot(data=df_eda, x="Contract", y="ChurnNumerico", ax=axes[0], errorbar=None)
sns.barplot(
    data=df_eda,
    x="InternetService",
    y="ChurnNumerico",
    ax=axes[1],
    errorbar=None,
)
axes[0].set(title="Taxa de churn por contrato", ylabel="Taxa de churn", xlabel="")
axes[1].set(title="Taxa de churn por internet", ylabel="Taxa de churn", xlabel="")
plt.tight_layout()
plt.show()

# %%
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.boxplot(data=df, x="Churn", y="tenure", ax=axes[0], hue="Churn", legend=False)
sns.boxplot(
    data=df,
    x="Churn",
    y="MonthlyCharges",
    ax=axes[1],
    hue="Churn",
    legend=False,
)
axes[0].set(title="Tempo como cliente por churn", xlabel="Cancelou?")
axes[1].set(title="Cobranca mensal por churn", xlabel="Cancelou?")
plt.tight_layout()
plt.show()

# %% [markdown]
# **Interpretacao inicial:** clientes com contrato mensal, menor tempo de
# permanencia e determinadas modalidades de internet aparentam apresentar
# maior risco de churn. Essa observacao devera ser confirmada pelos modelos.

# %% [markdown]
# ## 5. Separacao entre features e target
#
# `customerID` e apenas um identificador e nao ajuda a explicar o churn.
# O target e transformado em 0 e 1 para uso pelos classificadores.

# %%
X = df.drop(columns=["customerID", "Churn"])
y = df["Churn"].map({"No": 0, "Yes": 1})

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=y,
)

print("Treino:", X_train.shape, "| Teste:", X_test.shape)
print("\nProporcao de churn no treino:")
print(y_train.value_counts(normalize=True).round(3))
print("\nProporcao de churn no teste:")
print(y_test.value_counts(normalize=True).round(3))

# %% [markdown]
# A separacao estratificada preserva aproximadamente a mesma proporcao de
# churn nos conjuntos de treino e teste.

# %% [markdown]
# ## 6. Pipeline de pre-processamento
#
# - Features numericas: valores ausentes preenchidos pela mediana e
#   padronizacao com `StandardScaler`.
# - Features categoricas: valor mais frequente para ausentes e codificacao
#   one-hot.
#
# O pipeline sera ajustado apenas durante o treinamento de cada modelo.

# %%
colunas_numericas = X.select_dtypes(include=np.number).columns.tolist()
colunas_categoricas = X.select_dtypes(exclude=np.number).columns.tolist()

pipeline_numerico = Pipeline(
    steps=[
        ("imputacao", SimpleImputer(strategy="median")),
        ("padronizacao", StandardScaler()),
    ]
)

pipeline_categorico = Pipeline(
    steps=[
        ("imputacao", SimpleImputer(strategy="most_frequent")),
        ("one_hot", OneHotEncoder(handle_unknown="ignore")),
    ]
)

preprocessador = ColumnTransformer(
    transformers=[
        ("numerico", pipeline_numerico, colunas_numericas),
        ("categorico", pipeline_categorico, colunas_categoricas),
    ]
)

print("Colunas numericas:", colunas_numericas)
print("Quantidade de colunas categoricas:", len(colunas_categoricas))

# %% [markdown]
# ## 7. Verificacao do pre-processamento
#
# Esta transformacao e feita somente para verificar o resultado. Na etapa de
# modelagem, o `preprocessador` sera combinado com cada classificador em um
# unico pipeline.

# %%
X_train_transformado = preprocessador.fit_transform(X_train)
X_test_transformado = preprocessador.transform(X_test)

print("Formato original do treino:", X_train.shape)
print("Formato transformado do treino:", X_train_transformado.shape)
print("Formato transformado do teste:", X_test_transformado.shape)
print("Valores ausentes apos o pre-processamento:", np.isnan(X_train_transformado.data).sum())

# %% [markdown]
# ## Conclusao da etapa
#
# A base foi analisada e preparada para modelagem. Corrigimos `TotalCharges`,
# removemos o identificador, separamos treino e teste de forma estratificada e
# criamos um pipeline reutilizavel de pre-processamento.
#
# **Proxima etapa:** treinar e avaliar KNN, Naive Bayes, SVM e Arvore de
# Decisao, seguidos pelo comite de classificadores.
