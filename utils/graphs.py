import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

def best_sellers(df):
    best_sellers = df.groupby('Product')['Quantity'].sum().sort_values(ascending=False).reset_index()

    # slider limita números de itens mostrados
    max_items = len(best_sellers)
    default_top = min(10, max_items)
    top_n = st.slider("Mostrar top N produtos", min_value=1, max_value=max_items, value=default_top)
    best_sellers = best_sellers.head(top_n)

    fig = px.bar(
        best_sellers,
        x="Product",
        y="Quantity",
        color="Product",
        text="Quantity",
        category_orders={"Product": best_sellers["Product"].tolist()},
        color_discrete_sequence=px.colors.sequential.Viridis,
        labels={"Product": "Produto", "Quantity": "Quantidade"},
        title="Produtos Mais Vendidos por Quantidade",
        template="plotly_white",
        height=520,
    )

    fig.update_traces(texttemplate="%{text:.0f}", textposition="outside", showlegend=False)
    fig.update_yaxes(tickformat=",d")
    fig.update_layout(
        xaxis_tickangle=-45,
        margin=dict(t=90, b=160, l=40, r=20),
        uniformtext_minsize=8,
        uniformtext_mode="hide",
    )

    st.plotly_chart(fig, use_container_width=True)


def city_profit(df):
    df['Receita'] = df['Price'] * df['Quantity']

    receita_produto = df.groupby('City')['Receita'].sum().sort_values(ascending=False).reset_index()

    max_items = len(receita_produto)
    default_top = min(10, max_items)
    top_n = st.slider("Mostrar top N cidades", min_value=1, max_value=max_items, value=default_top)
    receita_produto = receita_produto.head(top_n)

    fig = px.bar(
        receita_produto,
        x="City",
        y="Receita",
        color="City",
        text="Receita",  # mostra os números nas barras
        category_orders={"City": receita_produto["City"].tolist()},  # mantém a ordem decrescente
        color_discrete_sequence=px.colors.sequential.Viridis,
        labels={"City": "Cidade", "Receita": "Receita"},
        title="Faturamento por Cidade",
        template="plotly_white",
        height=520,
    )

    # formatação: mostrar valores com separador de milhares e 2 casas, posicionados fora das barras
    fig.update_traces(texttemplate="R$ %{text:,.2f}", textposition="outside", showlegend=False)

    # eixo y com prefixo de moeda e formato numérico
    fig.update_yaxes(tickprefix="R$ ", tickformat=",.2f")

    # layout final (rotaciona ticks, margens)
    fig.update_layout(
        xaxis_tickangle=-45,
        margin=dict(t=90, b=160, l=40, r=20),
        uniformtext_minsize=8,
        uniformtext_mode="hide",
    )

    st.plotly_chart(fig, use_container_width=True)


def payment_method(df):
    pagamento = df['Payment Method'].value_counts().reset_index()

    max_items = len(pagamento)
    top_n = st.slider("Mostrar top N formas de pagamento", min_value=1, max_value=max_items, value=max_items)
    pagamento = pagamento.head(top_n)

    # gráfico de barras horizontal
    fig = px.bar(
    pagamento,
    x="count",
    y="Payment Method",
    orientation="h",
    color="Payment Method",                     # colore por método (pode remover se preferir cor única)
    text="count",                               # mostra números nas barras
    category_orders={"Payment Method": pagamento["Payment Method"].tolist()},  # mantém a ordem decrescente
    color_discrete_sequence=px.colors.sequential.Viridis,
    labels={"count": "Vezes usada", "Payment Method": "Forma de Pagamento"},
    title="Vendas por forma de pagamento",
    template="plotly_white",
    height=480,
    )

    # formatação dos textos e eixos
    fig.update_traces(texttemplate="%{text:.0f}", textposition="outside", showlegend=False)
    fig.update_xaxes(tickformat=",d")  # formata como inteiro com separador de milhares
    fig.update_layout(margin=dict(t=80, b=60, l=200, r=40))  # aumenta margem esquerda para rótulos longos

    # renderiza no Streamlit
    st.plotly_chart(fig, use_container_width=True)
