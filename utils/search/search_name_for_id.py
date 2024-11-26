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
        fornecedores = ""
        resultset = dict()
        # procura no json o id da cor que bate com o nome digitado assim como a tabela que ela pertence
        if name_id == -1:
            for keys in search_dict["quickSearch"][0]:
                if nome in keys:
                    name_id = search_dict["quickSearch"][0][""+nome+""]
                    fornecedores = 'coral'               
        if name_id == -1:
            for keys in search_dict["suvinil"][0]:
                if nome in keys:
                    name_id = search_dict["suvinil"][0][""+nome+""]
                    fornecedores = 'suvinil'
        if name_id == -1:
            for keys in search_dict["sherwin-willians"][0]:
                if nome in keys:
                    name_id = search_dict["sherwin-willians"][0][""+nome+""]
                    fornecedores = 'sherwin-willians'
        if name_id == -1:
            for keys in search_dict["anjo"][0]:
                if nome in keys:
                    name_id = search_dict["anjo"][0][""+nome+""]
                    fornecedores = 'anjo'
        if name_id == -1:
            for keys in search_dict["coral"][0]:
                if nome in keys:
                    name_id = search_dict["coral"][0][""+nome+""]
                    fornecedores = 'coral'
        # seleciona a tabela de acordo com o id encontrado
        tabela = tabela[fornecedores].to_json(orient="index")
        st.write(tabela['0'])
        c = 0
        for c in range(len(tabela)):
            if tabela[c]['name'] == name_id:
                resultset = {row['nome'], row['red'], row['green'], row['blue'], row['ncs'], row['codigo_suvinil'], row['hexadecimal'], row['pantone_código'], row['pantone_name'], row['pantone_hex'], row['fornecedores']}
                break
            c += 1
        resultset = {k:[v] for k,v in resultset.items()}
        resultset = pd.DataFrame(resultset)
        return resultset
