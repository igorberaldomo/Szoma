
from utils.conect_to_engine_production import conect_to_engine_production
import pandas as pd
import streamlit as st


engine = conect_to_engine_production()
def select_códigos(codigo, tabela):
    for index, row in tabela[fornecedores].iterrows():
            if row['pantone_código'] == codigo:
                resultset = row
    resultset = tabela[tabela['pantone_código'] == codigo]
    return resultset