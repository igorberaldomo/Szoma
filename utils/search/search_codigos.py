
from utils.conect_to_engine_production import conect_to_engine_production
import pandas as pd
import streamlit as st


engine = conect_to_engine_production()
def select_códigos(codigo, tabela):
    resultset = dict()
    for index, row in tabela.iterrows():
        if row['pantone_código'] == codigo:
            resultset = {'nome': row['nome'], 'red': row['red'], 'green': row['green'], 'blue': row['blue'], 'ncs': row['ncs'], 'codigo_suvinil': row['codigo_suvinil'], 'hexadecimal': row['hexadecimal'], 'pantone_código': row['pantone_código'], 'pantone_name': row['pantone_name'], 'pantone_hex': row['pantone_hex'], 'fornecedores': row['fornecedores']}
            break
    resultset = {k:[v] for k,v in resultset.items()}     
    resultset_df = pd.DataFrame(resultset)
    return resultset_df