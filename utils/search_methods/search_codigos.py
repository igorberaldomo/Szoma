
from utils.conection.production_connection import production_connection
import pandas as pd
import streamlit as st


engine = production_connection()
def search_codigos(codigo, tabela):
    results = dict()
    for index, linhas in tabela.iterrows():
        if linhas['pantone_código'] == codigo:
            results = {'nome': linhas['nome'], 'red': linhas['red'], 'green': linhas['green'], 'blue': linhas['blue'], 'ncs': linhas['ncs'], 'codigo_suvinil': linhas['codigo_suvinil'], 'hexadecimal': linhas['hexadecimal'], 'pantone_código': linhas['pantone_código'], 'pantone_name': linhas['pantone_name'], 'pantone_hex': linhas['pantone_hex'], 'fornecedores': linhas['fornecedores']}
            break
    results = {k:[v] for k,v in results.items()}     
    resultset_df = pd.DataFrame(results)
    return resultset_df