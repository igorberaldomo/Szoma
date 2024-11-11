from utils.conect_to_engine_developer import conect_to_engine_developer
from utils.conect_to_engine_production import conect_to_engine_production
import pandas as pd

# engine = conect_to_engine_developer()
engine = conect_to_engine_production()
def select_hexadecimal(hexadecimal, fornecedores):
    seach_string = ""

    if fornecedores != "todos":
        search_string = f"SELECT * from {fornecedores} WHERE hexadecimal = '{hexadecimal}' or pantone_hex = '{hexadecimal}' "
    else:
        search_string = f"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil WHERE hexadecimal = '{hexadecimal}' or pantone_hex = '{hexadecimal}' union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral WHERE hexadecimal = '{hexadecimal}' or pantone_hex = '{hexadecimal}' "

    resultset = pd.read_sql(search_string, engine)
    return resultset