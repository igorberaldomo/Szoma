
from utils.conect_to_engine_production import conect_to_engine_production
import pandas as pd
import streamlit as st


engine = conect_to_engine_production()
def select_códigos(codigo, tabela):
    resultset = []
    for index, row in tabela.iterrows():
            if row['pantone_código'] == codigo:
                st.write(row)
                resultset.append(row)
    return resultset[0]