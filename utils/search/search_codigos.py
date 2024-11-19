
from utils.conect_to_engine_production import conect_to_engine_production
import pandas as pd


engine = conect_to_engine_production()
def select_códigos(codigo, fornecedores, tabela):
    resultset = tabela[fornecedores][tabela[fornecedores]['pantone_código'] == codigo]
    return resultset