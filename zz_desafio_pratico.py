# ==============================================================================
# MÓDULO 02 - SEMANA 10 | AULA 03: DESAFIO PRÁTICO (B3)
# Roteiro simplificado e direto, alinhado ao nível iniciante da semana.
# ==============================================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard Financeiro B3", page_icon="📈", layout="wide")

# Título da aplicação
st.title("📈 Dashboard de Ações B3 - Desafio Prático")


# ------------------------------------------------------------------------------
# Passo 1: Leitura dos dados com Cache (@st.cache_data)
# ------------------------------------------------------------------------------
@st.cache_data
def carregar_dados(caminho):
    df = pd.read_csv(caminho)
    df["data"] = pd.to_datetime(df["data"])  # Converte a coluna para formato de data
    return df


df = carregar_dados("dados_b3_reais.csv")

# ------------------------------------------------------------------------------
# Passo 2: Filtros na Barra Lateral (st.sidebar)
# ------------------------------------------------------------------------------
st.sidebar.header("⚙️ Filtros")

# Filtro de Ações (multiselect para escolher uma ou mais ações)
tickers_disponiveis = sorted(df["ticker"].unique())
tickers_selecionados = st.sidebar.multiselect(
    label="Selecione as Ações:",
    options=tickers_disponiveis,
    default=tickers_disponiveis[:2],  # Seleciona as duas primeiras por padrão
)

# Filtro de Intervalo de Datas
datas = df["data"].dt.date
data_min = datas.min()
data_max = datas.max()

intervalo_datas = st.sidebar.date_input(
    label="Selecione o Período:",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max,
)

# Aplicando os filtros no DataFrame
df_filtrado = df.copy()

# 1. Filtra as ações escolhidas
if tickers_selecionados:
    df_filtrado = df_filtrado[df_filtrado["ticker"].isin(tickers_selecionados)]

# 2. Filtra o período de datas (quando início e fim estiverem selecionados)
if len(intervalo_datas) == 2:
    data_inicio, data_fim = intervalo_datas
    df_filtrado = df_filtrado[
        (df_filtrado["data"].dt.date >= data_inicio)
        & (df_filtrado["data"].dt.date <= data_fim)
    ]

# ------------------------------------------------------------------------------
# Passo 3: Indicadores em Colunas (st.columns e st.metric)
# ------------------------------------------------------------------------------
st.subheader("📌 Indicadores Principais (KPIs)")
col1, col2, col3 = st.columns(3)

# Cálculos simples
if not df_filtrado.empty:
    ultimo_preco = df_filtrado["preco_fechamento"].iloc[-1]
    preco_medio = df_filtrado["preco_fechamento"].mean()
    volume_total = df_filtrado["volume"].sum()
else:
    ultimo_preco, preco_medio, volume_total = 0, 0, 0

with col1:
    st.metric("Último Preço (R$)", f"R$ {ultimo_preco:.2f}")

with col2:
    st.metric("Preço Médio (R$)", f"R$ {preco_medio:.2f}")

with col3:
    st.metric("Volume Negociado", f"{volume_total:,.0f}".replace(",", "."))

st.divider()

# ------------------------------------------------------------------------------
# Passo 4: Visualizações em Abas (st.tabs) - Plotly e Matplotlib
# ------------------------------------------------------------------------------
aba_plotly, aba_matplotlib = st.tabs(
    [
        "📈 Evolução do Preço (Plotly Interativo)",
        "📊 Distribuição de Preço (Matplotlib Estático)",
    ]
)

# Aba 1: Gráfico de Linha do Plotly
with aba_plotly:
    st.subheader("Evolução Temporal do Preço de Fechamento")
    if not df_filtrado.empty:
        fig_plotly = px.line(
            df_filtrado,
            x="data",
            y="preco_fechamento",
            color="ticker",
            title="Preço de Fechamento ao Longo do Tempo",
            labels={"preco_fechamento": "Preço (R$)", "data": "Data"},
        )
        st.plotly_chart(fig_plotly, use_container_width=True)
    else:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")

# Aba 2: Histograma do Matplotlib
with aba_matplotlib:
    st.subheader("Distribuição Geral dos Preços de Fechamento")
    if not df_filtrado.empty:
        fig_mpl, ax = plt.subplots(figsize=(10, 4))
        ax.hist(
            df_filtrado["preco_fechamento"], bins=20, color="#2E86C1", edgecolor="black"
        )
        ax.set_title("Histograma de Preço de Fechamento")
        ax.set_xlabel("Preço (R$)")
        ax.set_ylabel("Frequência")
        st.pyplot(fig_mpl)
    else:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")

# ------------------------------------------------------------------------------
# Passo 5: Base Detalhada no Expander (st.expander)
# ------------------------------------------------------------------------------
with st.expander("📄 Visualizar Tabela de Dados Filtrados"):
    st.write(f"Exibindo **{len(df_filtrado)}** registros:")
    st.dataframe(df_filtrado, use_container_width=True)
