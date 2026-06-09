# Sistema de Identificacao de Clientes com Risco de Cancelamento

Projeto de aprendizado supervisionado para prever o **churn** de clientes de
uma empresa de telecomunicacoes. A solucao compara quatro algoritmos de
classificacao e combina suas previsoes em um comite de classificadores por
votacao suave.

> O comite apresentou o melhor equilibrio entre precisao e recall, atingindo
> **F1-score de 0,6205**, acima de todos os modelos individuais avaliados.

## Sobre o projeto

Empresas que oferecem servicos recorrentes precisam identificar clientes com
risco de cancelamento para direcionar acoes de retencao. Este projeto utiliza
dados demograficos, contratuais, financeiros e de servicos para classificar se
um cliente provavelmente cancelara ou permanecera com a empresa.

A solucao implementa um pipeline completo de machine learning:

1. Analise exploratoria dos dados;
2. Tratamento de valores ausentes;
3. Codificacao de variaveis categoricas;
4. Padronizacao de variaveis numericas;
5. Separacao estratificada entre treino e teste;
6. Treinamento de classificadores individuais;
7. Construcao de um comite por votacao suave;
8. Avaliacao e comparacao dos resultados.

## Base de dados

Foi utilizada a base publica
[Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn).

| Caracteristica | Descricao |
|---|---|
| Registros | 7.043 clientes |
| Colunas originais | 21 |
| Variavel alvo | `Churn` (`Yes` ou `No`) |
| Classe positiva | Cliente que cancelou o servico |
| Clientes com churn | 1.869 |
| Clientes sem churn | 5.174 |

As features incluem tempo como cliente, tipo de contrato, forma de pagamento,
servicos contratados, cobranca mensal e cobranca total.

## Tecnologias utilizadas

- Python
- Jupyter Notebook
- Pandas e NumPy
- Matplotlib e Seaborn
- Scikit-learn

## Pre-processamento

O pre-processamento foi implementado com `Pipeline` e `ColumnTransformer`,
garantindo que as transformacoes sejam ajustadas somente com os dados de
treino e evitando vazamento de dados.

- Conversao da coluna `TotalCharges` para formato numerico;
- Imputacao de 11 valores ausentes pela mediana;
- Remocao de `customerID`, por ser apenas um identificador;
- One-hot encoding das variaveis categoricas;
- Padronizacao das variaveis numericas;
- Divisao estratificada em 80% para treino e 20% para teste.

Apos o pre-processamento, os dados passaram de 19 para 45 features e ficaram
sem valores ausentes.

## Modelos avaliados

Foram treinados quatro classificadores individuais:

- **KNN:** classificacao baseada nos clientes mais proximos;
- **Naive Bayes:** modelo probabilistico gaussiano;
- **SVM:** separacao das classes utilizando kernel RBF;
- **Arvore de Decisao:** classificacao baseada em regras sucessivas.

O **comite de classificadores** combina os quatro modelos por votacao suave.
Cada classificador calcula probabilidades para as classes, e a decisao final e
baseada na media dessas probabilidades.

## Resultados

| Modelo | Acuracia | Precisao | Recall | F1-score |
|---|---:|---:|---:|---:|
| **Comite** | 0,7743 | 0,5603 | 0,6952 | **0,6205** |
| Naive Bayes | 0,6948 | 0,4589 | **0,8369** | 0,5928 |
| KNN | 0,7779 | 0,5822 | 0,5775 | 0,5799 |
| Arvore de Decisao | **0,7970** | **0,6679** | 0,4679 | 0,5503 |
| SVM | 0,7935 | 0,6627 | 0,4519 | 0,5374 |

Como a base possui classes desbalanceadas, o **F1-score** foi adotado como
principal criterio de comparacao.

### Principais conclusoes

- O Naive Bayes apresentou o maior recall e identificou a maior quantidade de
  clientes que realmente cancelaram;
- A Arvore de Decisao obteve a maior acuracia, mas deixou de identificar muitos
  clientes com churn;
- O comite obteve o maior F1-score, apresentando o melhor equilibrio geral
  entre precisao e recall;
- Uma acuracia elevada, isoladamente, nao garante que o modelo seja adequado
  para identificar clientes em risco.

## Estrutura do repositorio

```text
A3-IA/
|-- data/
|   `-- WA_Fn-UseC_-Telco-Customer-Churn.csv
|-- notebooks/
|   |-- 01_eda_preprocessamento.ipynb
|   `-- 02_modelagem_comite.ipynb
|-- reports/
|   |-- Relatorio_Projeto_A3_Comite_Classificadores.pdf
|   `-- Roteiro_Explicacao_Projeto_A3.pdf
|-- requirements.txt
`-- README.md
```

> O CSV esta configurado no `.gitignore`. Para executar o projeto apos clonar
> o repositorio, baixe a base no Kaggle e coloque o arquivo
> `WA_Fn-UseC_-Telco-Customer-Churn.csv` dentro da pasta `data/`.

## Como executar

### 1. Clone o repositorio

```bash
git clone https://github.com/GustavoFernandesS/previsao-churn-comite-classificadores.git
cd previsao-churn-comite-classificadores
```

### 2. Crie e ative um ambiente virtual

No Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No Linux ou macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependencias

```bash
pip install -r requirements.txt
```

### 4. Execute os notebooks

Abra os notebooks no VS Code ou Jupyter e execute-os nesta ordem:

1. `notebooks/01_eda_preprocessamento.ipynb`
2. `notebooks/02_modelagem_comite.ipynb`

No primeiro notebook, o resultado final esperado e:

```text
Formato transformado do treino: (5634, 45)
Formato transformado do teste: (1409, 45)
Valores ausentes apos o pre-processamento: 0
```

No segundo notebook, o resultado final esperado e:

```text
Melhor modelo individual pelo F1-score: Naive Bayes
F1-score do melhor individual: 0.5928
F1-score do comite: 0.6205
O comite apresentou melhora sobre o melhor modelo individual.
```

## Possiveis melhorias

- Aplicar validacao cruzada;
- Realizar busca automatizada de hiperparametros;
- Testar pesos diferentes para os classificadores do comite;
- Avaliar tecnicas de balanceamento de classes;
- Ajustar o limiar de classificacao;
- Adicionar metricas como ROC-AUC e curva precisao-recall;
- Investigar a importancia e a interpretabilidade das features.

## Autor

**Gustavo Fernandes Borrelly dos Santos**

Projeto desenvolvido para a disciplina de Inteligencia Artificial da
Universidade Sao Judas Tadeu.
