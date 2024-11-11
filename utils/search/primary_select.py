from utils.conect_to_engine_developer import conect_to_engine_developer
from utils.conect_to_engine_production import conect_to_engine_production
import pandas as pd

# engine = conect_to_engine_developer()
engine = conect_to_engine_production()
def primary_select(red, green, blue, fornecedores):
    distancia = 18
    maxred = red + distancia
    minred = red - distancia
    maxgreen = green + distancia
    mingreen = green - distancia
    maxblue = blue + distancia
    minblue = blue - distancia
    if maxred > 255:
        maxred = 255
    if minred < 0:
        minred = 0
    if maxgreen > 255:
        maxgreen = 255
    if mingreen < 0:
        mingreen = 0
    if maxblue > 255:
        maxblue = 255
    if minblue < 0:
        minblue = 0

    seach_string = ""
    if fornecedores != "todos":
        search_string = f"SELECT hexadecimal, fornecedores,nome, pantone_código,red,green,blue from {fornecedores} WHERE red >= {minred} AND  red <= {maxred} AND green >= {mingreen} AND green <= {maxgreen} AND blue >= {minblue} AND blue <= {maxblue}"
    elif fornecedores == "todos":
        search_string = f"SELECT hexadecimal, fornecedores,nome, pantone_código,red,green,blue from suvinil WHERE red >= {minred} AND  red <= {maxred} AND green >= {mingreen} AND green <= {maxgreen} AND blue >= {minblue} AND blue <= {maxblue} union SELECT hexadecimal, fornecedores,nome, pantone_código,red,green,blue from coral WHERE red >= {minred} AND  red <= {maxred} AND green >= {mingreen} AND green <= {maxgreen} AND blue >= {minblue} AND blue <= {maxblue}"
    resultset = pd.read_sql(search_string, engine)
    if resultset.empty:
        return []
    else:
        return resultset