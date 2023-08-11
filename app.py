from faker import Faker
import pandas as pd
import random
import streamlit as st
import base64

# Gerar dados fictícios

fake = Faker()

# Pessoas
pessoas_data = [{"ID": i, "Nome": fake.name(), "Localidade": fake.city()} for i in range(100)]
pessoas_df = pd.DataFrame(pessoas_data)

# Produtos
tipos_produto = ["Eletrônico", "Mobília", "Alimento"]
produtos_data = [{"ID": i, "Nome": fake.bs(), "Tipo": random.choice(tipos_produto), "Preço Unitário": random.randint(10, 1000)} for i in range(50)]
produtos_df = pd.DataFrame(produtos_data)

# Vendas
vendas_data = [{"ID da Venda": i, "ID da Pessoa": random.randint(0, 99), "ID do Produto": random.randint(0, 49), "Quantidade": random.randint(1, 10), "Data": fake.date()} for i in range(200)]
vendas_df = pd.DataFrame(vendas_data)

# Mesclagem dos DataFrames para trazer informações adicionais
vendas_df = vendas_df.merge(pessoas_df, left_on="ID da Pessoa", right_on="ID", suffixes=('', '_Pessoa'))
vendas_df = vendas_df.merge(produtos_df, left_on="ID do Produto", right_on="ID", suffixes=('', '_Produto'))

# Calcular o valor total das vendas
vendas_df["Valor Total"] = vendas_df["Quantidade"] * vendas_df["Preço Unitário"]

# Função para gerar um link de download para um CSV
def create_download_link(df, filename="data.csv"):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">Clique aqui para baixar o arquivo CSV</a>'

# Obter localidades que possuem ao menos uma venda
localidades_com_vendas = pessoas_df[pessoas_df['ID'].isin(vendas_df['ID da Pessoa'])]['Localidade'].unique()


# Aplicação Streamlit

# Sidebar para seleção de filtros
st.sidebar.title('Filtros')
opcao = st.sidebar.selectbox('Escolha uma opção:', ['Vendas por Localidade', 'Vendas por Tipo de Produto', 'Vendas por Período de Data'])

# Filtro para Vendas por Localidade
if opcao == 'Vendas por Localidade':
    localidade = st.sidebar.selectbox('Escolha a localidade:', localidades_com_vendas)
    resultado_df = vendas_df[vendas_df['Localidade'] == localidade][['Nome', 'Nome_Produto', 'Quantidade', 'Data', 'Valor Total']]
    st.table(resultado_df)

# Filtro para Vendas por Tipo de Produto
elif opcao == 'Vendas por Tipo de Produto':
    tipo_produto = st.sidebar.selectbox('Escolha o tipo de produto:', produtos_df['Tipo'].unique())
    resultado_df = vendas_df[vendas_df['Tipo'] == tipo_produto][['Nome', 'Nome_Produto', 'Quantidade', 'Data', 'Valor Total']]
    st.table(resultado_df)

# Filtro para Vendas por Período de Data
elif opcao == 'Vendas por Período de Data':
    data_inicial = st.sidebar.date_input('Data Inicial')
    data_final = st.sidebar.date_input('Data Final')
    resultado_df = vendas_df[(vendas_df['Data'] >= str(data_inicial)) & (vendas_df['Data'] <= str(data_final))][['Nome', 'Nome_Produto', 'Quantidade', 'Data', 'Valor Total']]
    st.table(resultado_df)

# Adicionando link para download na sidebar
st.sidebar.markdown(create_download_link(resultado_df), unsafe_allow_html=True)