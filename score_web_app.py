# Importando bibliotecas
# import streamlit as st
import pickle
import joblib
# import gzip
from PIL import Image

# Importando algoritmo
from sklearn.ensemble import RandomForestClassifier

# Orientação inicial
st.markdown('*_Observação: para mais informações, navegue pelas páginas_*')

#Indicando do que se trata a web app
foto = Image.open('bruno.carloto (2).png')
st.sidebar.image(foto, use_column_width=True)
st.sidebar.subheader('Bruno Rodrigues Carloto')
st.sidebar.markdown('Analista de dados')
st.sidebar.markdown('#### Projeto de modelagem')
st.sidebar.markdown("Em breve novas informações sobre o projeto")
st.sidebar.markdown('Feito por : Bruno Rodrigues Carloto')

st.sidebar.markdown("Redes Sociais :")
st.sidebar.markdown("- [Linkedin](https://www.linkedin.com/in/bruno-rodrigues-carloto)")
st.sidebar.markdown("- [Medium](https://medium.com/@brc-deep-analytics)")
st.sidebar.markdown("- [Mercadados](https://brunnocarlotosjob.wixsite.com/mercadados)")



st.header('Seja bem-vindo ao Good Bank')
st.subheader('Financiamento Jovem')
st.markdown(' ')
st.markdown(' ')

# Definição da taxa de juros
juro = 1.12 

# Solicitação de nome
usuario = st.text_input('Me informe seu nome para uma melhor experiência')
st.markdown('')

# Buscando mais informações
idade = st.number_input('Me informe sua idade', 18, 120) # idade
renda = st.number_input('Me informe sua renda', 500.0) # Renda
opcoes_moradia = ['Própria', 'Hipoteca', 'Aluguel', 'Outro'] # Opções de condição de posse de moradia
moradia = st.selectbox('Em que tipo de residência você mora?', opcoes_moradia) # Seleção de condição de posse de moradia
opcoes_objetivo = ['Empreendimento', 'Educação', 'Vestuário/Entretenimento', 'Saúde', 'Reforma', 'Quitar outra dívida'] # Opção objetivo financiamento
objetivo_financiamento = st.selectbox('Em que o financiamento ajudaria você?', opcoes_objetivo) # Seleção da opção de financiamento
financiamento = st.number_input('Qual valor de financiamento você precisa?', 500.0, 10000.00) # Seleção de valor de financiamento
parcela = st.radio('Em quantas vezes você quer pagar o empréstimo?', (1, 2, 3, 4, 5, 6, 12)) # Seleção de quantidades de parcelas
mensalidade = (round(((financiamento/parcela)) * juro,2)) # Cálculo do juros sobre a mensalidade

# Operação do modelo
modelo_RFC = joblib.load('modelo_RFC_v4.joblib')
    
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
    output = 0
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
  output = 0  

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
  else:
    output = 6
  
  return output

# Processamento das informações fornecidas
condicao_moradia = conversao_opcao_moradia(moradia)
objetivo = conversao_objetivo_financiamento(objetivo_financiamento)
percentual_comprometimento = (financiamento/renda)
if percentual_comprometimento > 1.0:
    percentual_comprometimento_tratada = 1.0
else:
    percentual_comprometimento_tratada = percentual_comprometimento
juro = juro
risco_credito = classificacao_risco(renda, percentual_comprometimento_tratada)

# Ordenando variáveis preditoras
X_final = [[percentual_comprometimento, renda, risco_credito, condicao_moradia, juro, financiamento, objetivo]]

# Predição
score_final = modelo_RFC.predict_proba(X_final) * 1000
# Tratamento
if(score_final[0][0] == 1000.0).any():
    score_final_tratado = int(999.0)
elif (score_final[0][0] == 0.0).any():
    score_final_tratado = int(2.0)
elif (score_final[0][0] == 1.0).any():
    score_final_tratado = int(2.0)
else:
    score_final_tratado = str(int(score_final[0][0]))

# Regras
if idade > 40:
    st.write('''
    Este programa é destinado para um perfil mais jovem.

    Mas não se preocupe! Temos um programa especialmente para você:''')
    texto_do_link = "Programa Para Todos"
    st.markdown("- [Empréstimo Pessoal Para Todos](https://fintech-classifier-machine-learning.streamlit.app/)")

else:

    # Condicional para pagamento à vista
    if parcela == 1:
        if st.button("Ver Resultado"):
            # O código dentro deste bloco será executado quando o botão for clicado.
            if score_final[0][0] < 400:
                st.write(usuario,', este é seu score:')
                st.markdown(score_final_tratado)
                st.markdown('''Infelizmente, você não foi aprovado em nossa política de crédito.
                            Mas não fique triste! Temos outra solução para você. Que tal tentar nossa outra modalidade de crédito?''')
                st.markdown("- [Empréstimo Pessoal Para Todos](https://fintech-classifier-machine-learning.streamlit.app/)")
            else:
                st.write(usuario,', este é seu score:')
                st.markdown(score_final_tratado)
                st.markdown('Valor à vista do empréstimo: R$ {}. Pagamento só para daqui a três meses.'.format(mensalidade))

                if st.button("Eu quero!"):
                    st.markdown('Transferência realizada!')
        
    # Condicional para pagamento em mais de 1 vez
    else:
        if st.button("Ver Resultado"):
            # O código dentro deste bloco será executado quando o botão for clicado.
            if score_final[0][0] < 400:
                st.write(usuario,', este é seu score:')
                st.markdown(score_final_tratado)
                st.markdown('''Infelizmente, você não foi aprovado em nossa política de crédito.
                            Mas não fique triste! Temos outra solução para você. Que tal tentar nossa outra modalidade de crédito?''')
                st.markdown("- [Empréstimo Pessoal Para Todos](https://fintech-classifier-machine-learning.streamlit.app/)")
            else:
                st.write(usuario,', este é seu score:')
                st.markdown(score_final_tratado)
                st.markdown('Valor da mensalidade do empréstimo: R$ {}. A primeira só daqui a três meses.'.format(mensalidade))

                if st.button("Eu quero!"):
                    st.markdown('Transferência realizada!')
