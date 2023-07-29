# Importando bibliotecas
import streamlit as st
import pickle
import joblib
import gzip

# Importando algoritmo
from sklearn.ensemble import RandomForestClassifier

# Orientação inicial
st.markdown('*_Observação: para mais informações, navegue pelas páginas_*')

# Definição da taxa de juros
juro = 1.12 

# Solicitação de nome
usuario = st.text_input('Me informe seu nome para termos uma melhor experiência')
st.markdown('')

# Buscando mais informações
idade = st.number_input('Me informe sua idade', 18) # idade
renda = st.number_input('Me informe sua renda', 500.0) # Renda
opcoes_moradia = ['Própria', 'Hipoteca', 'Aluguel', 'Outro'] # Opções de condição de posse de moradia
moradia = st.selectbox('Em que tipo de residência você mora?', opcoes_moradia) # Seleção de condição de posse de moradia
opcoes_objetivo = ['Empreendimento', 'Educação', 'Vestuário/Entretenimento', 'Saúde', 'Reforma', 'Quitar outra dívida'] # Opção objetivo financiamento
objetivo_financiamento = st.selectbox('Em que o financiamento ajudaria você?', opcoes_objetivo) # Seleção da opção de financiamento
financiamento = st.number_input('Qual valor de financiamento você precisa?', 500.0, 10000.00) # Seleção de valor de financiamento
parcela = st.radio('Em quantas vezes você quer pagar o empréstimo?', (1, 2, 3, 4, 5, 6, 12)) # Seleção de quantidades de parcelas
mensalidade = (round(((financiamento/parcela)) * juro,2)) # Cálculo do juros sobre a mensalidade

# Operação do modelo
modelo_RFC = joblib.load('modelo_RFC_v2.joblib')
    
def classificacao_risco(renda, percentual_comprometimento):
    
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
    output = 4
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

# Processamento das informações fornecidas
condicao_moradia = conversao_opcao_moradia(moradia)
objetivo = conversao_objetivo_financiamento(objetivo_financiamento)
percentual_comprometimento = (financiamento/renda)
juro = juro
risco_credito = classificacao_risco(renda, percentual_comprometimento)

# Ordenando variáveis preditoras
X_final = [[percentual_comprometimento, renda, risco_credito, condicao_moradia, juro, financiamento, objetivo]]

# Predição
score_final = modelo_RFC.predict_proba(X_final) * 1000

# Condicional para pagamento à vista
if parcela == 1:
    st.write('Valor à vista se o empréstimo for aprovado: R$ {} por mês'.format(mensalidade))
    st.markdown(f'**<h1 style = color: green >Score</h1>:**')
    st.markdown(f"**<h1>{score_final[0][0]}</h1>**")
    
# Condicional para pagamento em mais de 1 vez
else:
    st.write('Se o empréstimo for aprovado, a mensalidade fica de R$ {} por mês'.format(mensalidade))
    st.markdown(f'**<h1 style = color: green >Score</h1>:**')
    st.markdown(f"**<h1>{score_final[0][0]}</h1>**")
