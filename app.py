import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from utils import graphs
from utils import widgets

# --- Configuraçoes ---
st.set_page_config(layout='wide',page_title="Dashboard Restaurantes",page_icon="🏠")


# --- Carregamento dos dados ---
@st.cache_data
def load_data():
    try:
        data = pd.read_csv("assets/Sales-Data-Analysis.csv")
        df = pd.DataFrame(data)
        
        # --- Limpeza e Preparação dos Dados ---
        # Converte a coluna 'Date' para o formato datetime
        df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")

        # Remove espaços em branco adicionais.
        for col in df.select_dtypes(include=['object']).columns:
            # 1. Substitui múltiplos espaços (incluindo no meio) por um único espaço.
            df[col] = df[col].str.replace(r'\s+', ' ', regex=True)
            # 2. Remove quaisquer espaços que possam ter sobrado no início ou no fim.
            df[col] = df[col].str.strip()

        return df
    except FileNotFoundError:
        st.error("Arquivo 'Sales-Data-Analysis.csv' não encontrado.")
        st.stop()


df = load_data()

# --- App ---

# --- BARRA LATERAL COM WIDGETS DE FILTRO ---
data_inicio, data_fim, tipo_compra, gerente = widgets.make_sidebar(df)

# --- APLICAÇÃO DOS FILTROS NO DATAFRAME ---
df_filtrado = df[
    (df["Date"] >= pd.to_datetime(data_inicio)) & (df["Date"] <= pd.to_datetime(data_fim))
]

if tipo_compra != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Purchase Type"] == tipo_compra]

if gerente != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Manager"] == gerente]

# --- APP ---
st.title("Análise de Vendas de Restaurantes")
st.markdown("Verifique as estatísticas do seu restaurante favorito.")
st.markdown("---")

# Verifica se o dataframe filtrado não está vazio antes de renderizar os gráficos
if not df_filtrado.empty:
    st.header("Qual é o produto mais vendido?")
    graphs.best_sellers(df_filtrado)

    st.header("Qual cidade gera mais receita para o restaurante?")
    st.write("Aqui vamos descobrir qual das franquias gera mais receita para o grupo dono do restaurante.")
    graphs.city_profit(df_filtrado)

    st.header("Qual a forma de pagamento mais utilizada?")
    graphs.payment_method(df_filtrado)
else:
    st.warning("Nenhum dado encontrado para os filtros selecionados. Por favor, ajuste as opções.")

