import streamlit as st
import webbrowser
import pandas as pd
from datetime import datetime

if "data" not in st.session_state:
    df_data = pd.read_csv(r"D:\Educação\Asimov\Dev AI_comPython\Streamlit\Projeto_Fifa2023\dataset\CLEAN_FIFA23_official_data.csv", index_col=0) #Carrega dataset
    df_data = df_data[df_data["Contract Valid Until"] >= datetime.today().year] #filtra por contratos ativos maiores igual a 2024 ou now!
    df_data = df_data[df_data["Value(£)"] > 0] #filtra por jogadores com valor maior que 0
    df_data = df_data.sort_values(by="Overall", ascending=False) #ordenal por overall do maior para o menor
    st.session_state["data"] = df_data
# Contract Valid Until
st.set_page_config(
    layout= "wide",
    page_title="FIFA 23",
    page_icon="🏆",
)

#criando alguns textos em nosso home!

st.markdown("# OFFICIAL FIFA23 DATASET OFICIAL⚽")
st.markdown("### Dataset de jogadores de futebol de 2017 a 2023")

st.sidebar.image("https://pbs.twimg.com/media/FXBGCIrXgAAbwKe?format=jpg&name=large", width=250)
st.sidebar.markdown("Desenvolvido por [LRCorp](https://lrcorp.com.br/)")
# st.image("https://pbs.twimg.com/media/FXBGCIrXgAAbwKe?format=jpg&name=large", width=300)


btn = st.button("Acesse os dados no kaggle")
if btn:
    webbrowser.open_new_tab("https://www.kaggle.com/datasets/kevwesophia/fifa23-official-datasetclean-data")


st.markdown(f"""
    O conjunto de dados de jogadores de futebol de 2017 a 2023 fornece informações abrangentes sobre jogadores de futebol profissionais. 
    O conjunto de dados contém uma ampla gama de atributos, incluindo dados demográficos dos jogadores, características físicas, estatísticas de jogo,
    detalhes de contratos e afiliações de clubes. Com mais de **17.000** registros, este conjunto de dados oferece um recurso valioso para analistas de futebol, 
    pesquisadores e entusiastas interessados em explorar vários aspectos do mundo do futebol, pois permite estudar atributos de jogadores, métricas de desempenho, 
    avaliação de mercado, análise de clubes, posicionamento de jogadores e desenvolvimento do jogador ao longo do tempo.

    ## Sobre Kaggle
            
    O Kaggle uma plataforma para aprendizado de ciência de dados. É também uma comunidade, a maior da internet, para assuntos relacionados com Data Science.
    Hoje, contém mais de 536 mil membros ativos, com novas entradas todos os dias. O Kaggle se destaca por ser uma comunidade, mas também por apresentar competições premiadas, o que profissionaliza um pouco as práticas no site.
    Em geral, apresenta tutoriais, competições, rankings, cursos, dicas, fóruns, datasets e muito mais. É um grande site com uma variedade de informações para quem precisa mergulhar de cabeça nesse mundo.             
            """)