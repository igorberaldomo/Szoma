from utilidades.conecções.método_de_conecção_produção import método_de_conecção_produção

import pandas as pd



engine = método_de_conecção_produção()
def tabela_pandas(segundo_query, primeiro_query):
    #  essa função pega os dados e gera um pandas dataframe para uso futuro
    lista_pandas = []

    def getting_data():
        queries = {
            "suvinil": primeiro_query,
            "coral": segundo_query,
        }
        dataframes = {}

        def convert_to_float(value):
            # substitui vírgula por ponto
            value = str(value).replace(",", "")  # Substituir vírgula por ponto
            try:
                return float(value)
            except ValueError:
                return None

        for table_name, query in queries.items():
            try:
                df = pd.read_sql(query, engine)
                if table_name in ["suvinil", "coral"]:
                    df["fornecedores"] = df["fornecedores"].astype(str)
                    df["hexadecimal"] = df["hexadecimal"].astype(str)
                    df["nome"] = df["nome"].astype(str)
                    df["pantone_código"] = df["pantone_código"].astype(str)
                    df["red"] = df["red"].astype(int)
                    df["green"] = df["green"].astype(int)
                    df["blue"] = df["blue"].astype(int)
                dataframes[table_name] = df
            except Exception as e:
                print(f"Erro ao processar a tabela {table_name}: {e}")
            return dataframes

    table = getting_data()
    print(table)