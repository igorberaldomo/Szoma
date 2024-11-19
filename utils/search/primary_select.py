from utils.conect_to_engine_production import conect_to_engine_production
import pandas as pd


engine = conect_to_engine_production()
def primary_select(red, green, blue, tabela):
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
    resultset = tabela[(tabela['red'] >= minred) & (tabela['red'] <= maxred) & (tabela['green'] >= mingreen) & (tabela['green'] <= maxgreen) & (tabela['blue'] >= minblue) & (tabela['blue'] <= maxblue)]
    if resultset.empty:
        return []
    else:
        return resultset