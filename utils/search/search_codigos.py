
from utils.conect_to_engine_production import conect_to_engine_production
import pandas as pd
import streamlit as st


engine = conect_to_engine_production()
def select_códigos(codigo, tabela):
    for index, row in tabela.iterrows():
            if row['pantone_código'] == codigo:
                st.write(row)
                resultset = row
    for index, row in resultset.iterrows():
        if index == 0:
            resultset = row
    return resultset

# dct = {'nome': resultset[posição]['nome'], 'red': resultset[posição]['red'], 'green': resultset[posição]['green'], 'blue': resultset[posição]['blue'], 'ncs': resultset[posição]['ncs'], 'codigo_suvinil': resultset[posição]['codigo_suvinil'], 'hexadecimal': resultset[posição]['hexadecimal'], 'pantone_código': resultset[posição]['pantone_código'], 'pantone_name': resultset[posição]['pantone_name'], 'pantone_hex': resultset[posição]['pantone_hex'], 'fornecedores': resultset[posição]['fornecedores']} 
                # dct = {k:[v] for k,v in dct.items()}     
                # resultset_df = pd.DataFrame(dct)