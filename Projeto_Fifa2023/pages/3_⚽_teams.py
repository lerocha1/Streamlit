import streamlit as st
import matplotlib.pyplot as plt


st.set_page_config(
    layout= "wide",
    page_title="FIFA 23 - Teams",
    page_icon="⚽",
)

df_data = st.session_state["data"]
st.title("FIFA 23 - Teams")

clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)


df_filtered = df_data[(df_data["Club"] == club)].set_index("Name")
st.image(df_filtered.iloc[0]["Club Logo"])

st.markdown(f"## {club}")



columms = ["Age", "Photo", "Flag", "Overall", "Value(£)", "Wage(£)", "Joined", "Height(cm.)",
           "Weight(lbs.)", "Contract Valid Until", "Release Clause(£)" ]

st.dataframe(df_filtered[columms], 
             column_config={
                 "Overall": st.column_config.ProgressColumn(
                     "Overall", format="%d", min_value=0, max_value=100,
                 ),
                 "Photo": st.column_config.ImageColumn(
                     width=100,
                 ),
                 "Flag": st.column_config.ImageColumn(
                     width=100,
                 ),
                 "Wage(£)": st.column_config.ProgressColumn(
                     "Weeklu Wage", format="£%f", min_value=0, max_value=df_filtered["Wage(£)"].max(),

                 ),
                 "Contract Valid Until": st.column_config.NumberColumn(
                     "Contract Valid Until", format="%d"
                 )

             })
# Calcula a média do atributo "Overall" do time
media_overall = df_filtered["Overall"].mean()
media_value = df_filtered["Value(£)"].mean()
valor_mercado = df_filtered["Release Clause(£)"].sum()


st.subheader("Gráfico do Overall por Jogado")
# Plota um gráfico de linhas com a evolução do atributo "Overall" ao longo do tempo
st.line_chart(df_filtered["Overall"])

# Exibe a média na tela
col1, col2, col3 = st.columns(3)
col1.markdown(f"Média Overral do time: **{media_overall:.2f}**")
col2.markdown(f"Media do Valor de Mercado jogadores: **£{media_value:.2f}**",)
col3.markdown(f"Total Venda Todos Jogadores: **{valor_mercado:.2f}**")

st.divider()
# Calcula a média de idade dos jogadores
# Calcula a média de idade dos jogadores
media_idade = df_filtered["Age"].mean()

plt.figure(figsize=(8, 4))
# Plota o histograma da idade dos jogadores
plt.hist(df_filtered["Age"], bins=30, color="orange", edgecolor="black")

# Adiciona uma linha vertical representando a média de idade
plt.axvline(media_idade, color='red', linestyle='dashed', linewidth=1, label=f'Média: {media_idade:.2f}')

plt.xlabel("Idade")
plt.ylabel("Frequência")
plt.title("Histograma de Frequência por Idade dos Jogadores")
plt.legend()
plt.show()

#Ignora Warnings decorrente da plotagem
st.set_option('deprecation.showPyplotGlobalUse', False)

st.pyplot()