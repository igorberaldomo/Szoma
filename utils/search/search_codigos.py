from utils.conect_to_engine_developer import conect_to_engine_developer
from utils.conect_to_engine_production import conect_to_engine_production
import pandas as pd

# engine = conect_to_engine_developer()
engine = conect_to_engine_production()
def select_códigos(codigo, fornecedores):
    seach_string = ""
    if fornecedores != "todos":
        search_string = (
            f"SELECT * from {fornecedores} WHERE pantone_código = '{codigo}'"
        )
    else:
        search_string = f"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil WHERE pantone_código = '{codigo}' union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral WHERE pantone_código = '{codigo}' "
    resultset = pd.read_sql(search_string, engine)
    return resultset