from utils.conect_to_engine_developer import conect_to_engine_developer
from utils.conect_to_engine_production import conect_to_engine_production
import pandas as pd

# engine = conect_to_engine_developer()
engine = conect_to_engine_production()
def select_id(request_id, nome, fornecedores):
    if fornecedores != "todos":
        seach_string = f"Select * from {fornecedores} WHERE id = {request_id}"
        resultset = pd.read_sql(seach_string, engine)
    else:
        seach_string = f"Select * from suvinil WHERE id = {request_id} "
        search_string_2 = f"Select * from coral WHERE id = {request_id}"
        resultset_1 = pd.read_sql(seach_string, engine)
        resultset_2 = pd.read_sql(search_string_2, engine)
        if nome in resultset_1["nome"].values:
            resultset = resultset_1
        else:
            resultset = resultset_2
    return resultset