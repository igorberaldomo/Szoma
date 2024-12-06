import json
import pandas as pd
import sqlalchemy
import streamlit as st
from utilidades.conecções.método_de_conecção_produção import método_de_conecção_produção

engine = método_de_conecção_produção()

def procurar_o_codigo_para_obter_a_id(codigo, tabela):
    with open("procura/dicionário_procura_codigo_id.json", "r") as file:
        search_dict = json.load(file)
        codigo_id = -1
        resultset = list()
        # procura no json o id da cor que bate com o codigo digitado assim como a tabela que ela pertence   
        if codigo_id == -1:
            for keys in search_dict["suvinil"][0]:
                if codigo in keys:
                    codigo_id = search_dict["suvinil"][0][codigo]
                    tabela_escolida = tabela["suvinil"]
                    resultset.append(tabela_escolida.iloc[[codigo_id]])
                    codigo_id = -1
        if codigo_id == -1:
            for keys in search_dict["sherwin-willians"][0]:
                if codigo in keys:
                    codigo_id = search_dict["sherwin-willians"][0][codigo]
                    tabela_escolida = tabela["sherwin-willians"]
                    resultset.append(tabela_escolida.iloc[[codigo_id]])
                    codigo_id = -1 
        if codigo_id == -1:
            for keys in search_dict["anjo"][0]:
                if codigo in keys:
                    codigo_id = search_dict["anjo"][0][codigo]
                    tabela_escolida = tabela["anjo"]
                    resultset.append(tabela_escolida.iloc[[codigo_id]])
                    codigo_id = -1   
        if codigo_id == -1:
            for keys in search_dict["coral"][0]:
                if codigo in keys:
                    codigo_id = search_dict["coral"][0][codigo]
                    tabela_escolida = tabela["coral"]
                    resultset.append(tabela_escolida.iloc[[codigo_id]])
                    codigo_id = -1 
        # o metodo iloc mantem a posição original da tabela, nós precisamos que ele esteja na posição 0 para para executar as procuras, então desfazemos as posições pegamos os dados e refazemos a tabela
        c = 0
        st.write(resultset)
        for c in range(len(resultset[0])):
            resultset = resultset[0][c].to_dict(orient='records')
            resultset = {k:[v] for k,v in resultset[0].items()}
            resultset_df = pd.DataFrame(resultset)
            st.write(resultset)
            c+=1
        return resultset
