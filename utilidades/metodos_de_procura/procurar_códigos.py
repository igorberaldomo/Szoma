
from utilidades.método_de_conecção_produção import método_de_conecção_produção
import pandas as pd
import streamlit as st


engine = método_de_conecção_produção()
def procurar_códigos(codigo, tabela):
    resultados = dict()
    for index, linhas in tabela.iterrows():
        if linhas['pantone_código'] == codigo:
            resultados = {'nome': linhas['nome'], 'red': linhas['red'], 'green': linhas['green'], 'blue': linhas['blue'], 'ncs': linhas['ncs'], 'codigo_suvinil': linhas['codigo_suvinil'], 'hexadecimal': linhas['hexadecimal'], 'pantone_código': linhas['pantone_código'], 'pantone_name': linhas['pantone_name'], 'pantone_hex': linhas['pantone_hex'], 'fornecedores': linhas['fornecedores']}
            break
    resultados = {k:[v] for k,v in resultados.items()}     
    resultset_df = pd.DataFrame(resultados)
    return resultset_df