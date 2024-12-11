
from utils.conection.production_connection import production_connection
import pandas as pd

engine = production_connection()
def search_hexadecimal(hexadecimal, tabela):
    st.write(hexadecimal)
    resultset = dict()
    for index, row in tabela.iterrows():
        if row['hexadecimal'] == hexadecimal or row['pantone_hex'] == hexadecimal:
            resultset = {'nome': row['nome'], 'red': row['red'], 'green': row['green'], 'blue': row['blue'], 'ncs': row['ncs'], 'codigo_suvinil': row['codigo_suvinil'], 'hexadecimal': row['hexadecimal'], 'pantone_código': row['pantone_código'], 'pantone_name': row['pantone_name'], 'pantone_hex': row['pantone_hex'], 'fornecedores': row['fornecedores']}
            break
    resultset = {k:[v] for k,v in resultset.items()}     
    resultset_df = pd.DataFrame(resultset)
    return resultset_df