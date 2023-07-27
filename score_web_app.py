# Importando bibliotecas
import streamlit as st
import pandas as pd
import pickle

# Importando algoritmo
from sklearn.ensemble import RandomForestClassifier

st.markdown('*_Observação: para mais informações, navegue pelas páginas_*')

juro = 1.12 #Juro ao ano

usuario = st.text_input('Me informe seu nome para termos uma melhor experiência')
st.markdown('')

idade = st.number_input('Me informe sua idade', 18)
renda = st.number_input('Me informe sua renda')
opcoes_moradia = ['Própria', 'Hipoteca', 'Aluguel', 'Outro']
moradia = st.selectbox('Em que tipo de residência você mora?', opcoes_moradia)
opcoes_objetivo = ['Empreendimento', 'Educação', 'Vestuário/Entretenimento', 'Saúde', 'Reforma', 'Quitar outra dívida']
objetivo_financiamento = st.selectbox('Em que o financiamento ajudaria você?', opcoes_objetivo)
financiamento = st.number_input('Qual valor de financiamento você precisa?', 0.0, 10000.00)
parcela = st.radio('Em quantas vezes você quer pagar o empréstimo?', (1, 2, 3, 4, 5, 6, 12)
mensalidade = (round(((emprestimo/parcela)) * juro,2))
if parcela == 1:
    st.write('Valor à vista se o empréstimo for aprovado: R$ {} por mês'.format(mensalidade))
else:
    st.write('Se o empréstimo for aprovado, a mensalidade fica de R$ {} por mês'.format(mensalidade))

# Modelo
with open('modelo_RFC.pkl', 'rb') as f:
    modelo_RFC = pickle.load(f)

def classificacao_risco(renda, percentual_comprometimento):
    
    risco = 1
    
    if renda <= 2000 and percentual_comprometimento <= 0.3:
        risco = 1
    elif renda <= 2000 and percentual_comprometimento <= 0.5:
        risco = 3
    elif renda <= 2000 and percentual_comprometimento <= 1.0:
        risco = 7
    elif renda <= 5000 and percentual_comprometimento <= 0.3:
        risco = 1
    elif renda <= 5000 and percentual_comprometimento <= 0.5:
        risco = 2
    elif renda <= 5000 and percentual_comprometimento <= 0.1:
        risco = 6
    elif renda <= 10000 and percentual_comprometimento <= 0.3:
        risco = 1
    elif renda <= 10000 and percentual_comprometimento <= 0.5:
        risco = 1
    elif renda <= 10000 and percentual_comprometimento <= 1.0:
        risco = 5
    elif renda > 10000 and percentual_comprometimento <= 0.3:
        risco = 1
    elif renda > 10000 and percentual_comprometimento <= 0.5:
        risco = 1
    elif renda > 10000 and percentual_comprometimento <= 1.0:
        risco = 4

    return risco

def conversao_opcao_moradia(opcao):
  if opcao == 'Própria':
    output = 1
  elif opcao == 'Hipoteca':
    output = 2
  elif opcao == 'Aluguel':
    output = 3
  elif opcao == 'Outro':
    output 3
  return output

def conversao_objetivo_financiamento(opcao):
  if opcao == 'Empreendimento':
    output = 1
  elif opcao == 'Educação':
    output = 2
  elif opcao == 'Vestuário/Entretenimento':
    output = 3
  elif opcao == 'Saúde':
    output = 4
  elif opcao == 'Reforma':
    output = 5
  elif opcao == 'Quita outra dívida':
    output = 6
  return output

# Backend
condicao_moradia = conversao_opcao_moradia(moradia)
objetivo = conversao_objetivo_financiamento(objetivo_financiamento)
percentual_comprometimento = (financiamento/renda)
juro = juro
risco_credito = classificacao_risco(renda, percentual_comprometimento)

X_final = [[percentual_comprometimento, renda, risco_credito, condicao_moradia, juro, financiamento, objetivo]]

score_final = modelo_RFC.predict_proba(X_final) * 1000

st.write(score_final)



