import pandas as pd
import streamlit as st

def get_all_entries(red, green,blue,tabela,menor_valor_de_menor, maior_valor_de_menor,menor_valor_de_maior,maior_valor_de_maior,menor_valor_de_meio,maior_valor_de_meio):
    if maior == red:
            primeira_maior = "green"
            segunda_maior = "blue"
            for index, row in tabela.iterrows():
                if row['red'] >= menor_valor_de_menor:
                    if row['red'] <= maior_valor_de_menor:
                        if row['green'] >= menor_valor_de_maior:
                            if row['green'] <= maior_valor_de_maior: 
                                if row['blue'] >= menor_valor_de_meio:
                                    if row['blue'] <= maior_valor_de_meio:
                                        primeira = {'nome': row['nome'], 'red': row['red'], 'green': row['green'], 'blue': row['blue'], 'ncs': row['ncs'], 'codigo_suvinil': row['codigo_suvinil'], 'hexadecimal': row['hexadecimal'], 'pantone_código': row['pantone_código'], 'pantone_name': row['pantone_name'], 'pantone_hex': row['pantone_hex'], 'fornecedores': row['fornecedores']}
                                        primeira = {k:[v] for k,v in primeira.items()}     
                                        primeira = pd.DataFrame(primeira)
            
            for index, row in tabela.iterrows():
                if tabela['red'] >= menor_valor_de_meio:
                    if tabela['red'] <= maior_valor_de_meio:
                        if tabela['green'] >= menor_valor_de_menor:
                            if tabela['green'] <= maior_valor_de_menor:
                                if tabela['blue'] >= menor_valor_de_maior:
                                    if tabela['blue'] <= maior_valor_de_maior:
                                        segunda = {'nome': row['nome'], 'red': row['red'], 'green': row['green'], 'blue': row['blue'], 'ncs': row['ncs'], 'codigo_suvinil': row['codigo_suvinil'], 'hexadecimal': row['hexadecimal'], 'pantone_código': row['pantone_código'], 'pantone_name': row['pantone_name'], 'pantone_hex': row['pantone_hex'], 'fornecedores': row['fornecedores']}
                                        segunda = {k:[v] for k,v in segunda.items()}     
                                        segunda = pd.DataFrame(segunda)
        
    if maior == green:
        primeira_maior = "blue"
        segunda_maior = "red"
        for index, row in tabela.iterrows():
            if tabela['red'] >= menor_valor_de_meio:
                if tabela['red'] <= maior_valor_de_meio: 
                    if tabela['green'] >= menor_valor_de_menor:
                        if tabela['green'] <= maior_valor_de_menor:
                            if tabela['blue'] >= menor_valor_de_maior:
                                if tabela['blue'] <= maior_valor_de_maior:
                                    primeira = {'nome': row['nome'], 'red': row['red'], 'green': row['green'], 'blue': row['blue'], 'ncs': row['ncs'], 'codigo_suvinil': row['codigo_suvinil'], 'hexadecimal': row['hexadecimal'], 'pantone_código': row['pantone_código'], 'pantone_name': row['pantone_name'], 'pantone_hex': row['pantone_hex'], 'fornecedores': row['fornecedores']}
                                    primeira = {k:[v] for k,v in primeira.items()}     
                                    primeira = pd.DataFrame(primeira)
        
        for index, row in tabela.iterrows():
            if tabela['red'] >= menor_valor_de_maior:
                if tabela['red'] <= maior_valor_de_maior:
                    if tabela['green'] >= menor_valor_de_meio:
                        if tabela['green'] <= maior_valor_de_meio:
                            if tabela['blue'] >= menor_valor_de_menor:
                                if tabela['blue'] <= maior_valor_de_menor: 
                                    segunda = {'nome': row['nome'], 'red': row['red'], 'green': row['green'], 'blue': row['blue'], 'ncs': row['ncs'], 'codigo_suvinil': row['codigo_suvinil'], 'hexadecimal': row['hexadecimal'], 'pantone_código': row['pantone_código'], 'pantone_name': row['pantone_name'], 'pantone_hex': row['pantone_hex'], 'fornecedores': row['fornecedores']}
                                    segunda = {k:[v] for k,v in segunda.items()}     
                                    segunda = pd.DataFrame(segunda)
    if maior == blue:
        segunda_maior = "green"
        primeira_maior = "red"
        for index, row in tabela.iterrows():
            if tabela['red'] >= menor_valor_de_meio:
                if tabela['red'] <= maior_valor_de_meio:
                    if tabela['green'] >= menor_valor_de_maior:
                        if tabela['green'] <= maior_valor_de_maior:
                            if tabela['blue'] >= menor_valor_de_menor:
                                if tabela['blue'] <= maior_valor_de_menor:
                                    primeira = {'nome': row['nome'], 'red': row['red'], 'green': row['green'], 'blue': row['blue'], 'ncs': row['ncs'], 'codigo_suvinil': row['codigo_suvinil'], 'hexadecimal': row['hexadecimal'], 'pantone_código': row['pantone_código'], 'pantone_name': row['pantone_name'], 'pantone_hex': row['pantone_hex'], 'fornecedores': row['fornecedores']}
                                    primeira = {k:[v] for k,v in primeira.items()}     
                                    primeira = pd.DataFrame(primeira)
                                        
        for index, row in tabela.iterrows():
            if tabela['red'] >= menor_valor_de_maior:
                if tabela['red'] <= maior_valor_de_maior:
                    if tabela['green'] >= menor_valor_de_meio:
                        if tabela['green'] <= maior_valor_de_meio:
                            if tabela['blue'] >= menor_valor_de_menor:
                                if tabela['blue'] <= maior_valor_de_menor:
                                    segunda = {'nome': row['nome'], 'red': row['red'], 'green': row['green'], 'blue': row['blue'], 'ncs': row['ncs'], 'codigo_suvinil': row['codigo_suvinil'], 'hexadecimal': row['hexadecimal'], 'pantone_código': row['pantone_código'], 'pantone_name': row['pantone_name'], 'pantone_hex': row['pantone_hex'], 'fornecedores': row['fornecedores']}
                                    segunda = {k:[v] for k,v in segunda.items()}     
                                    segunda = pd.DataFrame(segunda)

    return primeira, segunda, primeira_maior, segunda_maior