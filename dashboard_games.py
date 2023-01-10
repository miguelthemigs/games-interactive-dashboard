import pandas as pd
import streamlit as st
import plotly_express as px


st.set_page_config(page_title="Estatística dos Vídeo Games",
                   page_icon=":video_game:", # this is an emoji
                   layout="wide", # how the content will be displayed in the screen
                   ) 

@st.cache 
def pega_excel():
    df = pd.read_csv("C:\\Users\\migro\\Desktop\\Programming\\interactive_dash\\Video_Games.csv")
    return df

df = pega_excel()

# --- TITLE ---
st.title(":video_game: Video Games Dashboard")
st.text("Planilha:")
st.markdown("##")

# --- FILTROS ---
st.sidebar.title("Filtros")

genero = st.sidebar.multiselect(
    "Escolha o genero do jogo:",
    options=df["Genre"].unique(),
    default=df["Genre"].unique()
)

plataforma = st.sidebar.multiselect(
    "Escolha a plataforma do jogo:",
    options=df["Platform"].unique(),
    default=df["Platform"].unique()
)

df_filtrado = df.query( # consulta o data frame
    "Genre == @genero & Platform == @plataforma"
)

st.dataframe(df_filtrado) # coloca o data frame na tela


# --- GRAFICO DE VENDAS POR ANO
vendas_por_ano = df_filtrado.groupby(["Year_of_Release"]).sum()[["Global_Sales"]]
vendas_por_ano = vendas_por_ano.drop(vendas_por_ano.tail(2).index,axis=0)
media_vendas_anuais = vendas_por_ano.values.mean()

st.subheader(f"Média de Vendas Anuais:")
st.subheader(f"{round(media_vendas_anuais, 2)} bi $")
st.markdown("---")

# colunas 
left_column, right_column = st.columns(2)

plot_vendas_por_ano = px.bar(
    vendas_por_ano,
    x=vendas_por_ano.index,
    y="Global_Sales",
    title="Vendas de Jogos Anuais (bi)$",
    template="plotly_white"
)
with left_column:
    st.plotly_chart(plot_vendas_por_ano)

# --- GRAFICO DE DISTRIBUICAO POR JOGO --- 
genre_platform = pd.crosstab(df_filtrado["Genre"], df_filtrado["Platform"]).T
genre_platform = pd.DataFrame(genre_platform.sum(axis=0))
genre_platform["Total"] = genre_platform.values

plot_distribuicao = px.pie(
    genre_platform,
    values="Total",
    names=genre_platform.index,
    title="Distribuição de Gêneros dos Jogos",
    color_discrete_sequence=px.colors.sequential.RdBu
)
with right_column:
    st.plotly_chart(plot_distribuicao)
    
# --- HIDE STUFF --- 
#Main Menu {visibility: hidden;}
hide = """
    <style>
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide, unsafe_allow_html=True)