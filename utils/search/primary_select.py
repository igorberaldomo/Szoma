from utils.conect_to_engine_production import conect_to_engine_production
import pandas as pd
import json


engine = conect_to_engine_production()
def primary_select(red, green, blue, tabela):
    # distancia define o limite de busca para cima e para baixo
    distancia = 18
    # min e max é os maiores e menores valores que um atributo pode ter
    maxred = red + distancia
    minred = red - distancia
    maxgreen = green + distancia
    mingreen = green - distancia
    maxblue = blue + distancia
    minblue = blue - distancia
    # garanta que os valores estao entre 0 e 255 (limites do rgb)
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
    # aplica a procura na tabela
    resultset = tabela[(tabela['red'] >= minred) & (tabela['red'] <= maxred) & (tabela['green'] >= mingreen) & (tabela['green'] <= maxgreen) & (tabela['blue'] >= minblue) & (tabela['blue'] <= maxblue)]
    c = 0
    menor_diferência = 0
    posição = 0
    resultset = resultset.to_dict(orient="records")
    for c in range(len(resultset)):
        r = resultset[c]['red']
        g = resultset[c]['green']
        b = resultset[c]['blue']
        diferença = abs(red - r) + abs(green - g) + abs(blue - b)
        if c == 0:
            menor_diferência = diferença
            posição = c
        if diferença < menor_diferência:
            menor_diferência = diferença
            posição = c
        if menor_diferência == 0:
            posição = c
        c+= 1
        dct = {'nome': resultset[posição]['nome'], 'red': resultset[posição]['red'], 'green': resultset[posição]['green'], 'blue': resultset[posição]['blue'], 'ncs': resultset[posição]['ncs'], 'codigo_suvinil': resultset[posição]['codigo_suvinil'], 'hexadecimal': resultset[posição]['hexadecimal'], 'pantone_código': resultset[posição]['pantone_código'], 'pantone_name': resultset[posição]['pantone_name'], 'pantone_hex': resultset[posição]['pantone_hex'], 'fornecedores': resultset[posição]['fornecedores']} 
        dct = {k:[v] for k,v in dct.items()}     
        resultset_df = pd.DataFrame(dct)
    return resultset_df