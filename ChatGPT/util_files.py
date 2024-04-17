import streamlit as st

from pathlib import Path
import re
from unidecode import unidecode
import pickle

#Cria pasta mensagens, caso n!ão exita!
PASTA_CONFIGURACOES = Path(__file__).parent / "configuracoes"
PASTA_CONFIGURACOES.mkdir(exist_ok=True)
PASTA_MENSAGENS = Path(__file__).parent / "mensagens"
PASTA_MENSAGENS.mkdir(exist_ok=True)
CACHE_DESCONVERTE = {}


def desconverte_nome_mensagem(nome_arquivo):
    if not nome_arquivo in CACHE_DESCONVERTE:
        nome_mensagem = ler_mensagem_po_nome_arquivo(nome_arquivo, key="nome_mensagem")
        CACHE_DESCONVERTE[nome_arquivo] = nome_mensagem
    return CACHE_DESCONVERTE[nome_arquivo]


def converte_nome_mensagem(nome_mensagem):
    nome_arquivo = unidecode(nome_mensagem)
    nome_arquivo = re.sub("\W+","",nome_arquivo).lower()
    return nome_arquivo

def salvar_mensagens(mensagens):
    if len(mensagens) == 0:
        return False
    nome_mensagem = retorna_nome_da_mensagem(mensagens)
    nome_arquivo = converte_nome_mensagem(nome_mensagem)
    arquivo_salvar = {'nome_mensagem': nome_mensagem,
                      'nome_arquivo': nome_arquivo,
                      'mensagem': mensagens}
    with open(PASTA_MENSAGENS / nome_arquivo, 'wb') as f:
        pickle.dump(arquivo_salvar, f)

    return True

def listar_conversas():
    conversas = list(PASTA_MENSAGENS.glob("*"))
    conversas = sorted(conversas, key=lambda item: item.stat().st_mtime_ns, reverse=True)
    return [c.stem for c in conversas]

def ler_mensagem_po_nome_arquivo(nome_arquivo, key="mensagem"):
    with open(PASTA_MENSAGENS / nome_arquivo, "rb") as f:
        mensagens = pickle.load(f)
    return mensagens[key]

def ler_mensagens(mensagens, key = "mensagem"):
    if len(mensagens) == 0:
        return []
    nome_mensagem = retorna_nome_da_mensagem(mensagens)
    nome_arquivo = converte_nome_mensagem(nome_mensagem)
    with open (PASTA_MENSAGENS / nome_arquivo, "rb") as f:
        mensagens = pickle.load(f)
    return mensagens[key]

def retorna_nome_da_mensagem(mensagens):
    nome_mensagem = ''
    for mensagem in mensagens:
        if mensagem['role'] == 'user':
            nome_mensagem = mensagem['content'][:30]
            break
    return nome_mensagem