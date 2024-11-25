import os, json
import pandas as pd
import sqlalchemy
import streamlit as st
from utils.conect_to_engine_developer import conect_to_engine_developer
from utils.conect_to_engine_production import conect_to_engine_production
from utils.create_pandas_table import generate_pandas_table
from utils.get_all_entries import get_all_entries
from utils.filter_lines import filter_lines


# engine = conect_to_engine_developer()
engine = conect_to_engine_production()


def select_complementos(red, green, blue, palheta, tabela):
    lista_complementos = []
    if palheta == "triade":
        lista_complementos.clear()
        # seleciona os desvios
        desvio_maior = 60
        desvio_menor = 80
        # seleciona os maiores e menores valores
        valores = [red, green, blue]
        valores.sort()
        maior = valores[2]
        meio = valores[1]
        menor = valores[0]
        
        # coloca o default dos complementos como true
        complemento1 = True
        complemento2 = True

        # pega os limites da procura
        menor_valor_de_meio = meio - desvio_maior
        maior_valor_de_meio = meio + desvio_maior
        menor_valor_de_menor = menor - desvio_menor
        maior_valor_de_menor = menor + desvio_menor
        menor_valor_de_maior = maior - desvio_menor
        maior_valor_de_maior = maior + desvio_menor

        # garante que os limites da procura estao entre 0 e 255 (limites do rgb)
        if menor_valor_de_maior < 0:
            menor_valor_de_maior = 0
        if maior_valor_de_maior > 255:
            maior_valor_de_maior = 255
        if menor_valor_de_menor < 0:
            menor_valor_de_menor = 0
        if maior_valor_de_menor > 255:
            maior_valor_de_menor = 255
        if menor_valor_de_meio < 0:
            menor_valor_de_meio = 0
        if maior_valor_de_meio > 255:
            maior_valor_de_meio = 255

        # a primeira cor da triade a segunda cor da triade
        primeira = ""
        segunda = ""
        
        # qual das cores complementares da triade tem seu maior valor entre red, green e blue isso vai ser utilizado para filtrar os complementos no futuro para encontrar complementos proporcionais
        
        primeira, segunda, primeira_maior ,segunda_maior = get_all_entries(red, green, blue, tabela, menor_valor_de_menor, maior_valor_de_menor, menor_valor_de_maior, maior_valor_de_maior, menor_valor_de_meio, maior_valor_de_meio)

        st.write('segunda')
        
        # confirma se os complementos foram encontrados
        if len(resultado1) == 0 & len(resultado2) == 0:
            complemento1 = False
            complemento2 = False
        elif len(resultado1) == 0:
            complemento1 = False
        elif len(resultado2) == 0:
            complemento2 = False
        else:
            print(" ")
            
        # converte para dicionário

        c = 0
        x = 0
        distancia_1 = 0
        distancia_2 = 0
        menor_distancia_1 = 0
        menor_distancia_2 = 0

        while c < len(resultado1):
            # calcula a diferença entre os valores dentro da primeira cor da tríade
            atual_red = resultado1[c]["red"] - red
            atual_green = resultado1[c]["green"] - green
            atual_blue = resultado1[c]["blue"] - blue

            # transforma os valores negativos em positivos
            if atual_red < 0:
                atual_red = atual_red * -1
            if atual_green < 0:
                atual_green = atual_green * -1
            if atual_blue < 0:
                atual_blue = atual_blue * -1
            
            # calcula a diferença entre os valores dentro da primeira cor da tríade e a cor ideal
            distancia_atual = atual_red + atual_green + atual_blue

            # verifica qual e a menor diferença
            if c == 0 or distancia_atual < distancia_1:
                if distancia_atual != 0:
                    # usa a primeira maior para garantir que a cor selecionada seja proporcional
                    if primeira_maior == "red":
                        if atual_red > atual_blue & atual_red > atual_green:
                            menor_distancia_1 = c
                            distancia_1 = distancia_atual
                    if primeira_maior == "green":
                        if atual_green > atual_blue & atual_green > atual_red:
                            menor_distancia_1 = c
                            distancia_1 = distancia_atual
                    if primeira_maior == "blue":
                        if atual_blue > atual_green & atual_blue > atual_red:
                            menor_distancia_1 = c
                            distancia_1 = distancia_atual
                # pega a cor ideal
                elif distancia_atual == 0:
                    menor_distancia_1 = c
                    distancia_1 = distancia_atual
                    break
            c += 1
        while x < len(resultado2):
            # calcula a diferença entre os valores dentro da primeira cor da tríade
            atual_red = resultado2[x]["red"] - red
            atual_green = resultado2[x]["green"] - green
            atual_blue = resultado2[x]["blue"] - blue
            
            # transforma os valores negativos em positivos
            if atual_red < 0:
                atual_red = atual_red * -1
            if atual_green < 0:
                atual_green = atual_green * -1
            if atual_blue < 0:
                atual_blue = atual_blue * -1
            
            # calcula a diferença entre os valores dentro da primeira cor da tríade e a cor ideal
            distancia_atual = atual_red + atual_green + atual_blue
            if c == 0 or distancia_atual < distancia_2:
                if distancia_atual != 0:
                    # usa a primeira maior para garantir que a cor selecionada seja proporcional
                    if segunda_maior == "red":
                        if atual_red > atual_blue & atual_red > atual_green:
                            menor_distancia_2 = x
                            distancia_2 = distancia_atual
                    if segunda_maior == "green":
                        if atual_green > atual_blue & atual_green > atual_red:
                            menor_distancia_2 = x
                            distancia_2 = distancia_atual
                    if segunda_maior == "blue":
                        if atual_blue > atual_green & atual_blue > atual_red:
                            menor_distancia_2 = x
                            distancia_2 = distancia_atual
                # pega a cor ideal
                elif distancia_atual == 0:
                    menor_distancia_2 = x
                    distancia_2 = distancia_atual
                    break
            x += 1

        # a testar 
        resultado1 = filter_lines(resultado1)
        resultado2 = filter_lines(resultado2)
        
        # adiciona as cores mais perto da cor ideal que seguem o padrão nas listas
        if complemento1 == True & complemento2 == True:
            lista_complementos.append(resultado1[menor_distancia_1])
            lista_complementos.append(resultado2[menor_distancia_2])
        elif complemento1 == False:
            lista_complementos.append(resultado2[menor_distancia_2])
        elif complemento2 == False:
            lista_complementos.append(resultado1[menor_distancia_1])
        elif complemento1 == False & complemento2 == False:
            return []
        # retorna as cores 
        return lista_complementos
    elif palheta == "complementar":
        lista_complementos.clear()
        # seleciona o desvio
        desvio_complementar = 60
        # calcula o complementar
        cr = 255 - red
        cg = 255 - green
        cb = 255 - blue
        # assume que o complemento existe
        complemento1 = True
        complemento2 = True
        # calcula os limites do complemento
        cr_max = cr + desvio_complementar
        cr_min = cr - desvio_complementar
        cg_max = cg + desvio_complementar
        cg_min = cg - desvio_complementar
        cb_max = cb + desvio_complementar
        cb_min = cb - desvio_complementar
        # garante que os limites estejam entre 0 e 255
        if cr_max > 255:
            cr_max = 255
        if cr_min < 0:
            cr_min = 0
        if cg_max > 255:
            cg_max = 255
        if cg_min < 0:
            cg_min = 0
        if cb_max > 255:
            cb_max = 255
        if cb_min < 0:
            cb_min = 0

        # calcula o complemento intermediario
        cr_inter = (cr + red) / 2
        cg_inter = (cg + green) / 2
        cb_inter = (cb + blue) / 2

        # calcula os limites do complemento intermediario
        cr_inter_max = cr_inter + desvio_complementar
        cr_inter_min = cr_inter - desvio_complementar
        cg_inter_max = cg_inter + desvio_complementar
        cg_inter_min = cg_inter - desvio_complementar
        cb_inter_max = cb_inter + desvio_complementar
        cb_inter_min = cb_inter - desvio_complementar
        
        # aredonda os limites
        cr_inter_max = int(cr_inter_max).__round__()
        cr_inter_min = int(cr_inter_min).__round__()
        cg_inter_max = int(cg_inter_max).__round__()
        cg_inter_min = int(cg_inter_min).__round__()
        cb_inter_max = int(cb_inter_max).__round__()
        cb_inter_min = int(cb_inter_min).__round__()
        
        # recebe a informação das tabelas
        intermediaria = tabela[(tabela['red'] >= cr_inter_min) & (tabela['red'] <= cr_inter_max) & (tabela['green'] >= cg_inter_min) & (tabela['green'] <= cg_inter_max) & (tabela['blue'] >= cb_inter_min) & (tabela['blue'] <= cb_inter_max)]
        
        complementar = tabela[(tabela['red'] >= cr_min) & (tabela['red'] <= cr_max) & (tabela['green'] >= cg_min) & (tabela['green'] <= cg_max) & (tabela['blue'] >= cb_min) & (tabela['blue'] <= cb_max)]
        
        
        resultado1 = intermediaria
        resultado2 = complementar
        
        # verifica se as tabelas estao vazias
        if len(resultado1) == 0 & len(resultado2) == 0:
            complemento1 = False
            complemento2 = False
        elif len(resultado1) == 0:
            complemento1 = False
        elif len(resultado2) == 0:
            complemento2 = False
        else:
            print(" ")
            
        # transforma as tabelas em dicionarios
        
        c = 0
        x = 0
        menor_distancia_1 = 0
        menor_distancia_2 = 0
        distancia = 0
        # encontra o intermediario mais perto do ideal
        while c < len(resultado1):
            atual_red = resultado1[c]["red"] - cr_inter
            atual_green = resultado1[c]["green"] - cg_inter
            atual_blue = resultado1[c]["blue"] - cb_inter

            if atual_red < 0:
                atual_red = atual_red * -1
            if atual_green < 0:
                atual_green = atual_green * -1
            if atual_blue < 0:
                atual_blue = atual_blue * -1

            distancia_atual = atual_red + atual_green + atual_blue
            if c == 0 or distancia_atual < distancia:
                if distancia_atual != 0:
                    menor_distancia_1 = c
                    distancia = distancia_atual
            c += 1
            
        
        distancia = 0
        # encontra o complementar mais perto do ideal
        while x < len(resultado2):
            atual_red = resultado2[x]["red"] - cr
            atual_green = resultado2[x]["green"] - cg
            atual_blue = resultado2[x]["blue"] - cb

            # garante que os valores nao sejam negativos
            if atual_red < 0:
                atual_red = atual_red * -1
            if atual_green < 0:
                atual_green = atual_green * -1
            if atual_blue < 0:
                atual_blue = atual_blue * -1
            # calcula a distancia entre o numero atual e o ideal
            distancia_atual = atual_red + atual_green + atual_blue
            if c == 0 or distancia_atual < distancia:
                # garante que não irá ter duas cores iguais
                if distancia_atual != 0 & resultado2[x]['red'] != resultado1[menor_distancia_1]['red'] & resultado2[x]['green'] != resultado1[menor_distancia_1]['green'] & resultado2[x]['blue'] != resultado1[menor_distancia_1]['blue']:
                    menor_distancia_2 = x
                    distancia = distancia_atual
            x += 1
        # coloca a cor na lista
        if complemento1 == True & complemento2 == True:
            lista_complementos.append(resultado1[menor_distancia_1])
            lista_complementos.append(resultado2[menor_distancia_2])
        elif complemento1 == False:
            lista_complementos.append(resultado2[menor_distancia_2])
        elif complemento2 == False:
            lista_complementos.append(resultado1[menor_distancia_1])
        elif complemento1 == False & complemento2 == False:
            return []

        return lista_complementos

    elif palheta == "análoga":
        lista_complementos.clear()
        # seleciona os desvios
        desvio_maior_analoga = 80
        desvio_menor_analoga = 60
        # assume que os complementos existem
        complemento1 = True
        complemento2 = True
        # encontra maior e menor
        maior_analoga = max(red, green, blue)
        menor_analoga = min(red, green, blue)
        meio_analoga = 0
        # encontra o meio
        if blue == menor_analoga & green == maior_analoga or blue == maior_analoga & green == menor_analoga:
            meio_analoga = red
        if red == maior_analoga & blue == menor_analoga or red == menor_analoga & blue == maior_analoga:
            meio_analoga = green
        if red == maior_analoga & green == menor_analoga or red == menor_analoga & green == maior_analoga:
            meio_analoga = blue

        # pega os limites da procura
        menor_valor_de_maior_analoga = maior_analoga - desvio_menor_analoga
        maior_valor_de_maior_analoga = maior_analoga + desvio_menor_analoga
        menor_valor_de_menor_analoga = menor_analoga - desvio_menor_analoga
        maior_valor_de_menor_analoga = menor_analoga + desvio_menor_analoga
        menor_valor_de_meio_analoga = meio_analoga - desvio_maior_analoga
        maior_valor_de_meio_analoga = meio_analoga + desvio_maior_analoga

        # garante que os valores estejam dentro dos limites
        if menor_valor_de_maior_analoga < 0:
            menor_valor_de_maior_analoga = 0
        if maior_valor_de_maior_analoga > 255:
            maior_valor_de_maior_analoga = 255
        if menor_valor_de_menor_analoga < 0:
            menor_valor_de_menor_analoga = 0
        if maior_valor_de_menor_analoga > 255:
            maior_valor_de_menor_analoga = 255
        if menor_valor_de_meio_analoga < 0:
            menor_valor_de_meio_analoga = 0
        if maior_valor_de_meio_analoga > 255:
            maior_valor_de_meio_analoga = 255

        # aonde a procura vai ser armazenada
        primeira = ""
        segunda = ""
        
        # será usado para pegar os complementos de acordo com a proporção
        primeira_menor = ""
        segunda_menor = ""

        if maior_analoga == red:
            primeira_menor = "blue"
            segunda_menor = "green"
            
            primeira = tabela[(tabela['red'] >= menor_valor_de_maior_analoga) & (tabela['red'] <= maior_valor_de_maior_analoga) & (tabela['green'] >= menor_valor_de_meio_analoga) & (tabela['green'] <= maior_valor_de_meio_analoga) & (tabela['blue'] >= menor_valor_de_menor_analoga) & (tabela['blue'] <= maior_valor_de_menor_analoga)]

            segunda = tabela[(tabela['red'] >= menor_valor_de_maior_analoga) & (tabela['red'] <= maior_valor_de_maior_analoga) & (tabela['green'] >= menor_valor_de_menor_analoga) & (tabela['green'] <= maior_valor_de_menor_analoga) & (tabela['blue'] >= menor_valor_de_meio_analoga) & (tabela['blue'] <= maior_valor_de_meio_analoga)]

        if maior_analoga == green:
            primeira_menor = "blue"
            segunda_menor = "red"
            primeira = tabela[(tabela['red'] >= menor_valor_de_meio_analoga) & (tabela['red'] <= maior_valor_de_meio_analoga) & (tabela['green'] >= menor_valor_de_maior_analoga) & (tabela['green'] <= maior_valor_de_maior_analoga) & (tabela['blue'] >= menor_valor_de_menor_analoga) & (tabela['blue'] <= maior_valor_de_menor_analoga)]
            
            
            segunda = tabela[(tabela['red'] >= menor_valor_de_menor_analoga) & (tabela['red'] <= maior_valor_de_menor_analoga) & (tabela['green'] >= menor_valor_de_maior_analoga) & (tabela['green'] <= maior_valor_de_maior_analoga) & (tabela['blue'] >= menor_valor_de_meio_analoga) & (tabela['blue'] <= maior_valor_de_meio_analoga)]

        if maior_analoga == blue:
            primeira_menor = "red"
            segunda_menor = "green"
            primeira = tabela[(tabela['red'] >= menor_valor_de_menor_analoga) & (tabela['red'] <= maior_valor_de_menor_analoga) & (tabela['green'] >= menor_valor_de_meio_analoga) & (tabela['green'] <= maior_valor_de_meio_analoga) & (tabela['blue'] >= menor_valor_de_maior_analoga) & (tabela['blue'] <= maior_valor_de_maior_analoga)]
            
            
            segunda = tabela[(tabela['red'] >= menor_valor_de_meio_analoga) & (tabela['red'] <= maior_valor_de_meio_analoga) & (tabela['green'] >= menor_valor_de_menor_analoga) & (tabela['green'] <= maior_valor_de_menor_analoga) & (tabela['blue'] >= menor_valor_de_maior_analoga) & (tabela['blue'] <= maior_valor_de_maior_analoga)]

        resultado1 = primeira
        resultado2 = segunda
        
        # verifica se os complementos não estao vazios
        if len(resultado1) == 0 & len(resultado2) == 0:
            complemento1 = False
            complemento2 = False
        elif len(resultado1) == 0:
            complemento1 = False
        elif len(resultado2) == 0:
            complemento2 = False
    
        c = 0
        x = 0
        menor_distancia_1 = 0
        menor_distancia_2 = 0
        distancia = 0
        # pega o complemento mais perto do ideal
        while c < len(resultado1):
            atual_red = resultado1[c]["red"] - red
            atual_green = resultado1[c]["green"] - green
            atual_blue = resultado1[c]["blue"] - blue
            distancia = 0
            if atual_red < 0:
                atual_red = atual_red * -1
            if atual_green < 0:
                atual_green = atual_green * -1
            if atual_blue < 0:
                atual_blue = atual_blue * -1

            distancia_atual = atual_red + atual_green + atual_blue
            if c == 0 or distancia_atual < distancia:
                if distancia_atual != 0:
                    if primeira_menor == "red":
                        if atual_red < atual_blue & atual_red < atual_green:
                            menor_distancia_1 = c
                            distancia = distancia_atual
                    if primeira_menor == "green":
                        if atual_green < atual_blue & atual_green < atual_red:
                            menor_distancia_1 = c
                            distancia = distancia_atual
                    if primeira_menor == "blue":
                        if atual_blue < atual_green & atual_blue < atual_red:
                            menor_distancia_1 = c
                            distancia = distancia_atual
                elif distancia_atual == 0:
                    menor_distancia_1 = c
                    distancia = distancia_atual
                    break
            c += 1

        distancia = 0
        while x < len(resultado2):
            atual_red = resultado2[x]["red"] - red
            atual_green = resultado2[x]["green"] - green
            atual_blue = resultado2[x]["blue"] - blue
            if atual_red < 0:
                atual_red = atual_red * -1
            if atual_green < 0:
                atual_green = atual_green * -1
            if atual_blue < 0:
                atual_blue = atual_blue * -1

            distancia_atual = atual_red + atual_green + atual_blue
            if c == 0 or distancia_atual < distancia:
                if distancia_atual != 0:
                    if segunda_menor == "red":
                        if atual_red < atual_blue & atual_red < atual_green:
                            menor_distancia_2 = x
                            distancia = distancia_atual
                    if segunda_menor == "green":
                        if atual_green < atual_blue & atual_green < atual_red:
                            menor_distancia_2 = x
                            distancia = distancia_atual
                    if segunda_menor == "blue":
                        if atual_blue < atual_green & atual_blue < atual_red:
                            menor_distancia_2 = x
                            distancia = distancia_atual
                elif distancia_atual == 0:
                    menor_distancia_1 = c
                    distancia = distancia_atual
                    break
            x += 1
        # coloca na lista de complementos
        if complemento1 == True & complemento2 == True:
            lista_complementos.append(resultado1[menor_distancia_1])
            lista_complementos.append(resultado2[menor_distancia_2])
        elif complemento1 == False:
            lista_complementos.append(resultado2[menor_distancia_2])
        elif complemento2 == False:
            lista_complementos.append(resultado1[menor_distancia_1])
        elif complemento1 == False & complemento2 == False:
            return []
        return lista_complementos
    else:
        err = "Complemento indisponível"
        print(err)
        return err