import streamlit as st
import pandas as pd
import plotly.express as px

# --- NOVA FUNÇÃO PARA RENDERIZAR A SIDEBAR E RETORNAR OS FILTROS ---
def make_sidebar(df):
    """
    Renderiza a barra lateral com os filtros e retorna os valores selecionados.

    Args:
        df (pd.DataFrame): O DataFrame completo para extrair as opções dos filtros.

    Returns:
        tuple: Uma tupla contendo os valores selecionados de cada filtro.
               (data_inicio, data_fim, tipo_compra_selecionado, gerente_selecionado)
    """
    st.sidebar.header("Filtros Globais")

    # WIDGET 1: Filtro por Período (Data)
    data_inicio = st.sidebar.date_input(
        "Data de Início",
        value=df["Date"].min(),
        min_value=df["Date"].min(),
        max_value=df["Date"].max()
    )
    data_fim = st.sidebar.date_input(
        "Data de Fim",
        value=df["Date"].max(),
        min_value=df["Date"].min(),
        max_value=df["Date"].max()
    )

    # WIDGET 2: Filtro por Tipo de Compra
    tipos_compra = ["Todos"] + df["Purchase Type"].unique().tolist()
    tipo_compra_selecionado = st.sidebar.radio(
        "Tipo de Compra",
        options=tipos_compra
    )

    # WIDGET 3: Filtro por Gerente
    gerentes = ["Todos"] + df["Manager"].unique().tolist()
    gerente_selecionado = st.sidebar.selectbox(
        "Gerente",
        options=gerentes
    )
    
    # Retorna os valores selecionados para serem usados no script principal
    return data_inicio, data_fim, tipo_compra_selecionado, gerente_selecionado

