from utilidades.conecções.método_de_conecção_produção import método_de_conecção_produção
import streamlit as st
import pandas as pd
import json

engine = método_de_conecção_produção()
def selecionar_cor_principal(red, green, blue, tabela):
    try:
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
        resultset = resultset.to_dict(orient='index')
        menor_diferência = 0
        posição = 0
        for key, value in resultset.items(): 
            r = resultset[key]['red']
            g = resultset[key]['green']
            b = resultset[key]['blue']
            diferença = abs(red - r) + abs(green - g) + abs(blue - b)
            if key == 0:
                menor_diferência = diferença
                posição = key
            if diferença < menor_diferência:
                menor_diferência = diferença
                posição = key
            if menor_diferência == 0:
                posição = key
            key += 1
        dct = {'nome': resultset[posição]['nome'], 'red': resultset[posição]['red'], 'green': resultset[posição]['green'], 'blue': resultset[posição]['blue'], 'ncs': resultset[posição]['ncs'], 'codigo_suvinil': resultset[posição]['codigo_suvinil'], 'hexadecimal': resultset[posição]['hexadecimal'], 'pantone_código': resultset[posição]['pantone_código'], 'pantone_name': resultset[posição]['pantone_name'], 'pantone_hex': resultset[posição]['pantone_hex'], 'fornecedores': resultset[posição]['fornecedores']} 
        dct = {k:[v] for k,v in dct.items()}     
        resultset = pd.DataFrame(dct)
        return resultset
    except:
        return 