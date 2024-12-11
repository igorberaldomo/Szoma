import json
import pandas as pd
import sqlalchemy
import streamlit as st
from utils.conection.production_connection import production_connection

engine = production_connection()

def search_nome_to_find_id(nome, tabela):
    with open("procura/dicionário_procura_nome_id.json", "r") as file:
        search_dict = json.load(file)
        nome_id= -1
        resultset = list()
        # procura no json o id da cor que bate com o nome digitado assim como a tabela que ela pertence
        if nome_id == -1:
            for keys in search_dict["quickSearch"][0]:
                if nome.capitalize() in keys:
                    nome = search_dict["quickSearch"][0]
                    nome_id = search_dict["quickSearch"][0]
                    tabela_escolida = tabela["coral"]
        if nome_id == -1:
            for keys in search_dict["suvinil"][0]:
                if nome.capitalize() in keys:
                    nome = search_dict["quickSearch"][0]
                    nome_id = search_dict["suvinil"][0]
                    tabela_escolida = tabela["suvinil"]
        if nome_id == -1:
            for keys in search_dict["sherwin-willians"][0]:
                if nome.capitalize() in keys:
                    nome = search_dict["quickSearch"][0]
                    nome_id = search_dict["sherwin-willians"][0]
                    tabela_escolida = tabela["sherwin-willians"]
        if nome_id == -1:
            for keys in search_dict["anjo"][0]:
                if nome.capitalize() in keys:
                    nome = search_dict["quickSearch"][0]
                    nome_id = search_dict["anjo"][0]
                    tabela_escolida = tabela["anjo"]
        if nome_id == -1:
            for keys in search_dict["coral"][0]:
                if nome.capitalize() in keys:
                    nome = search_dict["quickSearch"][0]
                    nome_id = search_dict["coral"][0]
                    tabela_escolida = tabela["coral"]
        # o metodo iloc mantem a posição original da tabela, nós precisamos que ele esteja na posição 0 para para executar as procuras, então desfazemos as posições pegamos os dados e refazemos a tabela
        resultset = tabela_escolida[nome_id]
        st.write(resultset)
        resultset = resultset.to_dict(orient="records")
        resultset = {k: [v] for k, v in resultset[0].items()}

        resultset_df = pd.DataFrame(resultset)
        return resultset
