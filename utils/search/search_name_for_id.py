import json
import pandas as pd
import sqlalchemy
import streamlit as st
from utils.conect_to_engine_production import conect_to_engine_production

engine = conect_to_engine_production()

def search_name_for_id(nome, tabela):
    with open("search/search_dict.json", "r") as file:
        search_dict = json.load(file)
        name_id = -1
        resultset = list()
        # procura no json o id da cor que bate com o nome digitado assim como a tabela que ela pertence
        if name_id == -1:
            for keys in search_dict["quickSearch"][0]:
                if nome in keys:
                    name_id = search_dict["quickSearch"][0][nome]
                    tabela_escolida = tabela["coral"]      
        if name_id == -1:
            for keys in search_dict["suvinil"][0]:
                if nome in keys:
                    name_id = search_dict["suvinil"][0][nome]
                    tabela_escolida = tabela["suvinil"]   
        if name_id == -1:
            for keys in search_dict["sherwin-willians"][0]:
                if nome in keys:
                    name_id = search_dict["sherwin-willians"][0][nome]
                    tabela_escolida = tabela["sherwin-willians"]   
        if name_id == -1:
            for keys in search_dict["anjo"][0]:
                if nome in keys:
                    name_id = search_dict["anjo"][0][nome]
                    tabela_escolida = tabela["anjo"]   
        if name_id == -1:
            for keys in search_dict["coral"][0]:
                if nome in keys:
                    name_id = search_dict["coral"][0][nome]
                    tabela_escolida = tabela["coral"]   
        # seleciona a tabela de acordo com o id encontrado
        tabela = tabela_escolida.to_json(orient="records")
        c= 0
        for c in range(len(tabela)):
            if c == name_id:
                resultset.append(tabela[c])
            c+=1
            st.write(resultset[0])
        return resultset[0]
