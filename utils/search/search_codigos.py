
from utils.conect_to_engine_production import conect_to_engine_production
import pandas as pd


engine = conect_to_engine_production()
def select_códigos(codigo, tabela):
    st.write(tabela)
    resultset = tabela[tabela['pantone_código'] == codigo]
    return resultset