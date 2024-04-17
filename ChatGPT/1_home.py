import streamlit as st
from dotenv import load_dotenv, find_dotenv

from pathlib import Path
from util_files import *
from util_openai import retorna_resposta_modelo


# #Carrega o arquivo .env
# load_dotenv(find_dotenv())
# #Carrega o arquivo .env com a chave da API
# openai_key = os.getenv("OPENAI_API_KEY")
# Insira sua chave de API da OpenAI aqui
# api_key = openai_key

def tab_conversas(tab):
    tab.button("➕ Nova Conversa", on_click=seleciona_conversa, args=("",), use_container_width = True)
    tab.markdown("")
    conversas =listar_conversas()
    for nome_arquivo in conversas:
        nome_mensagem = desconverte_nome_mensagem(nome_arquivo).capitalize()
        if len(nome_mensagem) >= 30:
            nome_mensagem = nome_mensagem[:30] + "..."
        tab.button(nome_mensagem,on_click=seleciona_conversa, args=(nome_arquivo,),
                   disabled=nome_arquivo==st.session_state["conversa_atual"], use_container_width = True)

def seleciona_conversa(nome_arquivo):
    if nome_arquivo == "":
        st.session_state.mensagens = []
    else:
        mensagem = ler_mensagem_po_nome_arquivo(nome_arquivo)
        st.session_state.mensagens = mensagem
    st.session_state.conversa_atual = nome_arquivo

#Salvamento e Leitura da chave da API

def salva_chave(chave):
    with open(PASTA_CONFIGURACOES / "chave.", "wb") as f:
        pickle.dump(chave, f)

def le_chave():
    if (PASTA_CONFIGURACOES / "chave").exists():
        with open(PASTA_CONFIGURACOES / "chave", "rb")as f:
            return pickle.load(f)
    else:
        return ""
       
# Paginas*************************************************************************
def inicializcao():
    if not "mensagens" in st.session_state:
        st.session_state.mensagens = []
    if not "conversa_atual" in st.session_state:
        st.session_state.conversa_atual = ""
    if not "modelo" in st.session_state :
        st.session_state.modelo = "gpt-3.5-turbo"
    if not "api_key" in st.session_state:
        st.session_state.api_key = le_chave()

def tab_configuracoes(tab):
    modelo_escolhido = tab.selectbox("Selecione o modelo",
                  ["gpt-3.5-turbo", "gpt-4"])
    st.session_state["modelo"] = modelo_escolhido

    chave = tab.text_input("Adicione sua api Key",value=st.session_state["api_key"])

    if chave != st.session_state["api_key"]:
        st.session_state["api_key"] = chave
        salva_chave(chave)
        tab.success("Chave salva com sucesso!")

def pagina_principal():

    if not "mensagens" in st.session_state:
        st.session_state.mensagens = []

    mensagens = st.session_state["mensagens"]
    # Exibe o cabeçalho
    st.header("🤖 LRcorp ChatBot", divider=True)

    # Exibe a resposta do modelo
    for mensagem in mensagens:
        chat = st.chat_message(mensagem["role"])
        chat.markdown(mensagem["content"])

    prompt = st.chat_input("Fale com o chat")
    if prompt:
        if st.session_state["api_key"] == "":
            st.error("Adicione uma chave válida de api na aba de configurações")
        else:
            nova_mensagem = {"role": "user", 
                             "content": prompt}
            chat = st.chat_message(nova_mensagem["role"])
            chat.markdown(nova_mensagem["content"])
            mensagens.append(nova_mensagem)

            chat = st.chat_message('assistant')
            placeholder = chat.empty()
            placeholder.markdown("▌")
            resposta_completa = ''
            respostas = retorna_resposta_modelo(mensagens,
                                                st.session_state['api_key'],
                                                modelo=st.session_state['modelo'],
                                                stream=True)
        
        for resposta in respostas:
            resposta_completa += resposta.choices[0].delta.get("content", " ")
            placeholder.markdown(resposta_completa + "▌")
        placeholder.markdown(resposta_completa)
        nova_mensagem = {"role": "assistant", "content": resposta_completa}
        mensagens.append(nova_mensagem)

        st.session_state["mensagens"] = mensagens
        salvar_mensagens(mensagens)    

def main():
    inicializcao()
    pagina_principal()
    tab1, tab2, tab3 =st.sidebar.tabs(["Conversas","|","Configurações"])
    tab_conversas(tab1)
    tab_configuracoes(tab3)
    

if __name__ == "__main__":
    main()
