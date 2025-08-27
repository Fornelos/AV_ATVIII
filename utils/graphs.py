import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

def best_sellers(df):
    best_sellers = df.groupby('Product')['Quantity'].sum().sort_values(ascending=False).reset_index()

    # slider limita números de itens mostrados
    max_items = len(best_sellers)
    default_top = min(10, max_items)
    top_n = st.slider(label='',min_value=1, max_value=max_items, value=default_top,key='produto')
    st.write(f'Mostrar top {top_n} produtos:')
    best_sellers = best_sellers.head(top_n)

    fig = px.bar(
        best_sellers,
        x="Product",
        y="Quantity",
        color="Product",
        text="Quantity",
        category_orders={"Product": best_sellers["Product"].tolist()},
        color_discrete_sequence=px.colors.sequential.Plasma,
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


def city_treemap(df):
    import streamlit as st
    import pandas as pd
    import plotly.express as px

    df = df.copy()
    df['Receita'] = df['Price'] * df['Quantity']

    receita_produto = (
        df.groupby("City", as_index=False)["Receita"]
          .sum()
          .sort_values("Receita", ascending=False)
    )

    max_items = len(receita_produto)
    default_top = min(20, max_items)  # treemap tolera mais categorias
    top_n = st.slider("Mostrar top N cidades (treemap)", min_value=1, max_value=max_items, value=default_top, key='treemap_cidade')
    receita_top = receita_produto.head(top_n)

    fig = px.treemap(
        receita_top,
        path=["City"],
        values="Receita",
        color="Receita",
        color_continuous_scale=px.colors.sequential.Plasma,
        title="Faturamento por Cidade — Treemap",
        template="plotly_white",
        height=620,
    )

    # mostra label e valor formatado
    fig.data[0].texttemplate = "%{label}<br>R$ %{value:,.2f}"
    fig.update_traces(root_color="lightgrey")

    st.plotly_chart(fig, use_container_width=True)


def payment_method(df):
    pagamento = df['Payment Method'].value_counts().reset_index()

    max_items = len(pagamento)
    min_itens = len(pagamento) - len(pagamento)
    top_n = st.slider(label='', min_value=min_itens, max_value=max_items, value=max_items,key='pagamento')
    st.write(f'Mostrar top {top_n} formas de pagamento:')
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
    color_discrete_sequence=px.colors.sequential.Plasma,
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
