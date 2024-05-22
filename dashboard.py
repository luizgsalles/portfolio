import os
import pandas as pd
import numpy as np
from datetime import datetime

import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import altair as altair

# from urllib.parse import quote




colunas = [
            'Nome do Destinatário'
            , 'Canal de Vendas'
            , 'UF'
            , 'Nota Fiscal'
            , 'Transportadora'
            , 'Data Despacho'
            , 'Status Transportador'
            , 'Data do último status'
            , 'Previsão Entrega Cliente Original'
            , 'Situação'
            , 'Previsão Entrega Transp. Original'
            , 'Situação Transp.'
            , 'Custo Frete'
            , 'Preço Frete'
            , 'MicroStatus'
            , 'Valor da Nota'
           ]


# url = "https://docs.google.com/spreadsheets/d/1TA6yqJcuLXqoTAXy41jz7DZ5C6Y29PKM/edit?usp=drive_link&ouid=115090895786622954210&rtpof=true&sd=true/Pendências_2024-05-22.xlsx"
# escaped_url = quote(url, safe=':/')
# df = pd.read_excel(escaped_url, engine='openpyxl', usecols=colunas)

df = pd.read_excel('Pendências_2024-05-22.xlsx', engine='openpyxl', usecols=colunas)

# url_raw = 'https://github.com/luizgsalles/portfolio/blob/90fb5d96c69779c11f4460c6faa7da09f7221a27/Pend%C3%AAncias_2024-05-22.xlsx'
# df = pd.read_excel(url_raw, engine='openpyxl', usecols=colunas)


########################################################################################################################
########################################################################################################################

# Configurar o layout da página para "wide"
st.set_page_config(layout="wide")

########################################################################################################################
########################################################################################################################

## TÍTULO DASHBOARD
st.markdown("<h1 style='text-align: center; color:#0037A7;'>DASHBOARD - CONTROLE DE PENDÊNCIAS</h1>", unsafe_allow_html=True)


########################################################################################################################
########################################################################################################################

## GRÁFICOS:

transp_vc = df['Transportadora'].value_counts().reset_index()
transp_vc.columns = ['Transportadora', 'Contagem']
status_vc = df['Status Transportador'].value_counts().reset_index()
status_vc.columns = ['Status Transportador', 'Contagem']
market_vc = df['Canal de Vendas'].value_counts().reset_index()
market_vc.columns = ['Canal de Vendas', 'Contagem']


# Função para criar gráficos de barras
def create_bar_chart(data, x_col, y_col, title, x_label, y_label):
    fig, ax = plt.subplots(figsize=(5, 4))  # Ajustar o tamanho do gráfico
    ax.bar(data[x_col]
           , data[y_col]
           , color=['#0037A7']
          )
    ax.set_title(title
                 , fontsize=10
                 , fontweight='bold'
                )
    ax.set_xlabel(x_label
                  , fontsize=8
                 )
    ax.set_ylabel(y_label
                  , fontsize=8
                 )
    ax.set_xticklabels(data[x_col]
                       , rotation=45
                       , ha='right'
                       , fontsize=8
                      )
    ax.set_yticklabels(ax.get_yticks()
                       , fontsize=8
                      )
    ax.grid(True
            , which='both'
            , linestyle='--'
            , linewidth=0.5
           )
    
    return fig

# Criar gráficos de barras
fig_transp = create_bar_chart(transp_vc, 'Transportadora'
                              , 'Contagem'
                              , 'Contagem por Transportadora'
                              , 'Transportadora'
                              , 'Contagem'
                             )
fig_status = create_bar_chart(status_vc, 'Status Transportador'
                              , 'Contagem'
                              , 'Contagem por Status do Transportador'
                              , 'Status Transportador'
                              , 'Contagem'
                             )
fig_market = create_bar_chart(market_vc, 'Canal de Vendas'
                              , 'Contagem'
                              , 'Contagem por Canal de Vendas'
                              , 'Canal de Vendas'
                              , 'Contagem'
                             )

# Exibir gráficos no Streamlit
st.title('Análise de Transportadoras, Status e Canais de Vendas')

col1, col2, col3 = st.columns(3)

with col1:
    st.pyplot(fig_transp)

with col2:
    st.pyplot(fig_status)

with col3:
    st.pyplot(fig_market)

########################################################################################################################
########################################################################################################################

## MENU LATERAL:

# FILTROS - MENU LATERAL:
st.sidebar.header("Filtros da Tabela:")

########################################################################################################################

market = sorted(df['Canal de Vendas'].dropna().unique())

## Filtro de Marketplace:
mkt = st.sidebar.multiselect('Selecione os Marketplaces:'
                             , options=market
                             , default=market[0]
                             , help="Escolha uma ou mais opções disponíveis."
                          )

########################################################################################################################

transp = sorted(df['Transportadora'].dropna().unique())

## Filtro de Transportadora:
transportadora = st.sidebar.multiselect('Selecione a Transportadora:'
                                        , options=transp
                                        , default=transp[0]
                                        , help="Escolha uma ou mais opções disponíveis."
                                       )

########################################################################################################################

stts = sorted(df['Status Transportador'].dropna().unique())

## Filtro de Status:
status = st.sidebar.multiselect('Selecione o Status:'
                                        , options=stts
                                        , default=stts
                                        , help="Escolha uma ou mais opções disponíveis."
                                       )

########################################################################################################################

# Filtrar os dados com base na seleção do usuário
df_filtered = df[(df['Canal de Vendas'].isin(mkt)) &
                 (df['Transportadora'].isin(transportadora)) &
                 (df['Status Transportador'].isin(status))
                ]

########################################################################################################################
########################################################################################################################

## TABELA:

# Mostrar o dataframe:
st.subheader('Dados Filtrados', )
st.dataframe(df_filtered, use_container_width=True)

########################################################################################################################