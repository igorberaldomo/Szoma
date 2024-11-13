import pandas as pd
import sqlalchemy
import os
from dotenv import load_dotenv
from utils.conect_to_engine_developer import conect_to_engine_developer


engine = conect_to_engine_developer()


def getting_data():
    queries = {
        "suvinil": "SELECT hexadecimal, fornecedores,nome, pantone_código,red,green,blue FROM suvinil",
        "coral": "SELECT hexadecimal, fornecedores,nome, pantone_código,red,green,blue  FROM coral",

    }
    dataframes = {}
    def convert_to_float(value):
        value = str(value).replace(',', '')  # Substituir vírgula por ponto
        try:
            return float(value)
        except ValueError:
            return None

    for table_name, query in queries.items():
        try:
            df = pd.read_sql(query, engine)
            if table_name in ['suvinil', 'coral']:
                df['fornecedores'] = df['fornecedores'].astype(str)
                df['hexadecimal'] = df['hexadecimal'].astype(str)
                df['nome']  = df['nome'].astype(str)
                df['pantone_código'] = df['pantone_código'].astype(str)
                df['red'] = df['red'].astype(int)
                df['green'] = df['green'].astype(int)
                df['blue'] = df['blue'].astype(int)    
            dataframes[table_name] = df
        except Exception as e:
            print(f"Erro ao processar a tabela {table_name}: {e}")
    return dataframes
table = getting_data()

final_df = pd.merge(table['suvinil'], table['coral'], on='hexadecimal', how='outer')
print(final_df)