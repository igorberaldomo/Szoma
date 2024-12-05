from utilidades.método_de_conecção_produção import método_de_conecção_produção
import pandas as pd


engine = método_de_conecção_produção()
def select_id(request_id, nome, fornecedores):
    # metodo para procurar as tabelas pelo id
    if fornecedores != "todos":
        seach_string = f"Select * from {fornecedores} WHERE id = {request_id}"
        resultset = pd.read_sql(seach_string, engine)
    else:
        seach_string = f"Select * from suvinil WHERE id = {request_id} "
        search_string_2 = f"Select * from coral WHERE id = {request_id}"
        search_string_3 = f"Select * from sherwin-willians WHERE id = {request_id}"
        resultset_1 = pd.read_sql(seach_string, engine)
        resultset_2 = pd.read_sql(search_string_2, engine)
        resultset_3 = pd.read_sql(search_string_3, engine)
        if nome in resultset_1["nome"].values:
            resultset = resultset_1
        elif nome in resultset_2["nome"].values:
            resultset = resultset_2
        else:
            resultset = resultset_3
    return resultset