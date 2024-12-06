import json
import pandas as pd
import sqlalchemy
import streamlit as st
from utilidades.conecções.método_de_conecção_produção import método_de_conecção_produção

engine = método_de_conecção_produção()


def procurar_o_nome_para_obter_a_id(nome, tabela):
    with open("procura/dicionário_procura_nome_id.json", "r") as file:
        search_dict = json.load(file)
        nome_id= -1
        resultset = list()
        # procura no json o id da cor que bate com o nome digitado assim como a tabela que ela pertence
        if nome_id == -1:
            for keys in search_dict["quickSearch"][0]:
                if nome in keys:
                    nome_id = search_dict["quickSearch"][0][nome]
                    tabela_escolida = tabela["coral"]
        if nome_id == -1:
            for keys in search_dict["suvinil"][0]:
                if nome in keys:
                    nome_id = search_dict["suvinil"][0][nome]
                    tabela_escolida = tabela["suvinil"]
        if nome_id == -1:
            for keys in search_dict["sherwin-willians"][0]:
                if nome in keys:
                    nome_id = search_dict["sherwin-willians"][0][nome]
                    tabela_escolida = tabela["sherwin-willians"]
        if nome_id == -1:
            for keys in search_dict["anjo"][0]:
                if nome in keys:
                    nome_id = search_dict["anjo"][0][nome]
                    tabela_escolida = tabela["anjo"]
        if nome_id == -1:
            for keys in search_dict["coral"][0]:
                if nome in keys:
                    nome_id = search_dict["coral"][0][nome]
                    tabela_escolida = tabela["coral"]
        # o metodo iloc mantem a posição original da tabela, nós precisamos que ele esteja na posição 0 para para executar as procuras, então desfazemos as posições pegamos os dados e refazemos a tabela
        resultset = tabela_escolida.iloc[[nome_id]]
        resultset = resultset.to_dict(orient="records")
        resultset = {k: [v] for k, v in resultset[0].items()}
        resultset_df = pd.DataFrame(resultset)
        return resultset
