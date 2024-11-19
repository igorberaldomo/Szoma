
from utils.conect_to_engine_production import conect_to_engine_production
import pandas as pd


engine = conect_to_engine_production()
def select_hexadecimal(hexadecimal, tabela):
    resultset = tabela[tabela['hexadecimal'] == hexadecimal or tabela['pantone_hex'] == hexadecimal]
    return resultset