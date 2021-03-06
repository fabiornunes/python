# -*- coding: utf-8 -*-
"""Exemplo Geração de Regras apriori.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nGH5yk8kSb7AASYZcKrIfOSlLlCVNu-z
"""

import pandas as pd
from pandas import read_csv
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

#Realiza a leitura do csv contendo uma amostra reduzida dos dados do dataset titanic
dataset = read_csv('https://telescopeinstorage.blob.core.windows.net/datasets/titanic-apriori.csv', sep=';' , engine='python')
dataset.head()

#obtem quatidade de linhas e colunas

qtdlinhas = dataset.shape[0]
qtdcols = dataset.shape[1]

print(qtdlinhas)
print(qtdcols)

#converte o dataset em lista de transações

transacoes = []
for i in range(0, qtdlinhas):
    linhaTransacao = []
    for j in range(0, qtdcols):        
        linhaTransacao.append(str(dataset.values[i,j]))
    
    transacoes.append(linhaTransacao)
print(transacoes)

te = TransactionEncoder()

#Coloca em memórias as trasações e interpreta a quantidade de colunas que serão geradas durante o processamento
te.fit(transacoes)

#O objeto TransactionEncoder faz a conversão das transações em uma matriz binária onde cada linha da matriz representa uma transação
matriz_transacoes = te.transform(transacoes)
matriz_transacoes

print(te.columns_)

#Cria um dataframe auxiliar com a matriz binária (passo te.transform(transacoes)) de transações e as colunas obtidas (passo te.fit(transacoes))
dfAuxiliar = pd.DataFrame(matriz_transacoes, columns=te.columns_)

dfAuxiliar.head()

#Obtêm os itemsets mais frequentes com um suporte mínimo igual a 0.01. O paramêtro use_colnames significa que vamos usar os nomes das colunas do DataFrame dfAuxiliar 
#para construir as regras de Associação
itemsets_freq = apriori(dfAuxiliar, min_support=0.01, use_colnames=True)
itemsets_freq

itemsets_freq

#Algumas métricas:
#- support(A->C) = support(A+C) [aka 'support'], range: [0, 1]
#- confidence(A->C) = support(A+C) / support(A), range: [0, 1]
#- lift(A->C) = confidence(A->C) / support(C), range: [0, inf]
#- leverage(A->C) = support(A->C) - support(A)*support(C), range: [-1, 1]
#- conviction = [1 - support(C)] / [1 - confidence(A->C)],

#Obtêm as regras de associação a partir dos itemsets mais frequêntes
regras = association_rules(itemsets_freq, metric="confidence", min_threshold=0.4)

#Ordena as Regras por confiança
regrasOrdenadas = regras.sort_values('confidence' , ascending=False)

#mantém apenas as colunas que vamos utilizar 
regrasOrdenadas = regrasOrdenadas[['antecedents', 'consequents', 'support', 'confidence']]
regrasOrdenadas.head(100)

regras_sobreviventes =  regrasOrdenadas[regrasOrdenadas['consequents'] == {'Yes'}]
#OU
subset_sobrevivou = {'Yes'}
regras_sobreviventes =  regrasOrdenadas[  regrasOrdenadas['consequents'].apply(lambda x: subset_sobrevivou.issubset(x))]

regras_sobreviventes

regras_naoSobreviventes =  regrasOrdenadas[regrasOrdenadas['consequents'] == {'No'}]
regras_naoSobreviventes

subset_Mulheres = {'Female'}
regras_mulheres = regrasOrdenadas[  regrasOrdenadas['antecedents'].apply(lambda x: subset_Mulheres.issubset(x))]
regras_mulheres

subset_YesNo = {'Yes', 'No'}
regras_YesNo = regrasOrdenadas[regrasOrdenadas['consequents'].apply(lambda x: len(subset_YesNo.intersection(x)) > 0 )]
regras_YesNo

#Concatena as regras relacionadas dos sobreviventes e não-sobreviventes para análise única
regrasGeral =  pd.concat([regras_sobreviventes,regras_naoSobreviventes])

regrasGeral = regrasGeral.sort_values('confidence' , ascending=False)

regrasGeral