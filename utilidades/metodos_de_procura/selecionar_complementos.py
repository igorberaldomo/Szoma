import os, json
import pandas as pd
import sqlalchemy
import streamlit as st
from utilidades.conecções.método_de_conecção_local import método_de_conecção_local
from utilidades.conecções.método_de_conecção_produção import método_de_conecção_produção
from utilidades.exemplos.tabela_pandas import tabela_pandas
from utilidades.edição_de_linhas.filtrar_linhas_necessárias import filtrar_linhas_necessárias


# engine = método_de_conecção_local()
engine = método_de_conecção_produção()


def selecionar_complementos(red, green, blue, palheta, tabela):
    lista_complementos = []
    if palheta == "triade":
        lista_complementos.clear()
        # seleciona os desvios
        desvio_maior = 30
        desvio_menor = 20
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
        primeira = list()
        segunda = list()
        # cores como branco preto ou cinza, mais especificamente aquelas cores que tem dois ou mais valores rgb iguais, não adequados para serem buscados por filtros complementares, pois o filtro precisa que os valores sejam diferentes para gerarem cores complementares
        difRB = red - blue
        difRG = red - green
        difGB = green - blue
        
        if difRB < 0:
            difRB = difRB * -1
        if difRG < 0:
            difRG = difRG * -1
        if difGB < 0:
            difGB = difGB * -1
        # se a diferença entre as cores for menor ou igual a 3, ela tem dois ou mais valores próximos o suficiente para causar que duas cores do complemento sejam iguais
        if difRB < 3 and difRG < 3 and difGB < 3:
            # como precisamos de cores diferentes para os complementos 
            if red > 128 or green > 128 or blue > 128:
                maior_valor  = [maior_valor_de_menor, maior_valor_de_maior, maior_valor_de_meio]
                maior_valor.sort()
                # para mais facil leitura leiase com base no maior valor rgb da triade , os limites são entre o 0 e -20, entre -20 e -40 e entre -40 e -60
                maior_valor_de_maior = maior_valor[2]
                menor_valor_de_maior = maior_valor[2] -20
                maior_valor_de_meio = maior_valor[2] - 20
                menor_valor_de_meio = maior_valor[2] - 40
                maior_valor_de_menor = maior_valor[2] - 40
                menor_valor_de_menor = maior_valor[2] - 60
            if red < 128 or green < 128 or blue < 128:
                # para mais facil leitura leiase com base no menor valor rgb da triade, os limites são entre o 0 e +20, entre +20 e +40 e entre +40 e +60
                menor_valor  = [maior_valor_de_menor, maior_valor_de_maior, maior_valor_de_meio]
                menor_valor.sort()
                maior_valor_de_maior = menor_valor[0]
                menor_valor_de_maior = menor_valor[0] + 20
                maior_valor_de_meio = menor_valor[0] + 20
                menor_valor_de_meio = menor_valor[0] + 40
                maior_valor_de_menor = menor_valor[0] + 40
                menor_valor_de_menor = menor_valor[0] + 60

            
        # qual das cores complementares da triade tem seu maior valor entre red, green e blue isso vai ser utilizado para filtrar os complementos no futuro para encontrar complementos proporcionais
        tabela = tabela.to_dict(orient='index')
        if maior == red:
            primeira_maior = "green"
            segunda_maior = "blue"
            c = 0
            for c in range(len(tabela)):
                if tabela[c]['red'] >= menor_valor_de_menor and tabela[c]['red'] <= maior_valor_de_menor and tabela[c]['green'] >= menor_valor_de_maior and tabela[c]['green'] <= maior_valor_de_maior and tabela[c]['blue'] >= menor_valor_de_meio and tabela[c]['blue'] <= maior_valor_de_meio: 
                    primeira.append(tabela[c])
                c += 1
            
            x = 0
            for x in range(len(tabela)):
                if tabela[x]['red'] >= menor_valor_de_meio and tabela[x]['red'] <= maior_valor_de_meio and tabela[x]['green'] >= menor_valor_de_menor and tabela[x]['green'] <= maior_valor_de_menor and tabela[x]['blue'] >= menor_valor_de_maior and tabela[x]['blue'] <= maior_valor_de_maior:
                    segunda.append(tabela[x])
                x += 1
        
        if maior == green:
            primeira_maior = "blue"
            segunda_maior = "red"
            c = 0
            for c in range(len(tabela)):
                if tabela[c]['red'] >= menor_valor_de_meio and tabela[c]['red'] <= maior_valor_de_meio and tabela[c]['green'] >= menor_valor_de_menor and tabela[c]['green'] <= maior_valor_de_menor and tabela[c]['blue'] >= menor_valor_de_maior and tabela[c]['blue'] <= maior_valor_de_maior:
                    primeira.append(tabela[c])
                c += 1
            
            x = 0
            for x in range(len(tabela)):
                if tabela[x]['red'] >= menor_valor_de_maior and tabela[x]['red'] <= maior_valor_de_maior and tabela[x]['green'] >= menor_valor_de_meio and tabela[x]['green'] <= maior_valor_de_meio and tabela[x]['blue'] >= menor_valor_de_menor and tabela[x]['blue'] <= maior_valor_de_menor:
                    segunda.append(tabela[x])
                x += 1
                
        if maior == blue:
            segunda_maior = "green"
            primeira_maior = "red"
            c = 0
            for c in range(len(tabela)):
                if tabela[c]['red'] >= menor_valor_de_meio and tabela[c]['red'] <= maior_valor_de_meio and tabela[c]['green'] >= menor_valor_de_maior and tabela[c]['green'] <= maior_valor_de_maior and tabela[c]['blue'] >= menor_valor_de_menor and tabela[c]['blue'] <= maior_valor_de_menor: 
                    primeira.append(tabela[c])
                c += 1

            x = 0
            for x in range(len(tabela)):
                if tabela[x]['red'] >= menor_valor_de_maior and tabela[x]['red'] <= maior_valor_de_maior and tabela[x]['green'] >= menor_valor_de_meio and tabela[x]['green'] <= maior_valor_de_meio and tabela[x]['blue'] >= menor_valor_de_menor and tabela[x]['blue'] <= maior_valor_de_menor:
                    segunda.append(tabela[x])
                x += 1 
                
        resultado1 = primeira
        resultado2 = segunda
        
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
                    # garante cores diferentes para cores secundárias pŕoximas
                     if resultado2[x]["red"] != resultado1[menor_distancia_1]["red"] and resultado2[x]["green"] != resultado1[menor_distancia_1]["green"] and resultado2[x]["blue"] != resultado1[menor_distancia_1]["blue"]:
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

        # filtra as linhas necessárias 
        resultado1 = filtrar_linhas_necessárias(resultado1)
        resultado2 = filtrar_linhas_necessárias(resultado2)
        
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
        
    
        intermediaria = list()
        complementar = list()
        
        tabela = tabela.to_dict(orient='index')
        # recebe a informação das tabelas
        c = 0
        for c in range(len(tabela)):
            if tabela[c]['red'] >= cr_inter_min and tabela[c]['red'] <= cr_inter_max and tabela[c]['green'] >= cg_inter_min and tabela[c]['green'] <= cr_inter_max and tabela[c]['blue'] >= cb_inter_min and tabela[c]['blue'] <= cb_inter_max:
                intermediaria.append(tabela[c])
            c += 1
            
        x = 0
        for x in range(len(tabela)):
            if tabela[x]['red'] >= cr_min and tabela[x]['red'] <= cr_max and tabela[x]['green'] >= cg_min and tabela[x]['green'] <= cg_max and tabela[x]['blue'] >= cb_min and tabela[x]['blue'] <= cb_max:
                complementar.append(tabela[x])
            x += 1 
        
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
        
        # filtra as linhas necessárias  
        resultado1 = filtrar_linhas_necessárias(resultado1)
        resultado2 = filtrar_linhas_necessárias(resultado2)
        
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
        desvio_maior_analoga = 40
        desvio_menor_analoga = 30
        # assume que os complementos existem
        complemento1 = True
        complemento2 = True
        # encontra maior, meio e menor
        valores = [red, green, blue]
        valores.sort()
        maior_analoga = valores[2]
        meio_analoga = valores[1]
        menor_analoga = valores[0]

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
        primeira = list()
        segunda = list()
        
        # será usado para pegar os complementos de acordo com a proporção
        primeira_menor = ""
        segunda_menor = ""
        
 
        tabela = tabela.to_dict(orient='index')
        if maior_analoga == red:
            primeira_menor = "blue"
            segunda_menor = "green"
            c = 0
            for c in range(len(tabela)):
                if tabela[c]['red'] >= menor_valor_de_maior_analoga and tabela[c]['red'] <= maior_valor_de_maior_analoga and tabela[c]['green'] >= menor_valor_de_meio_analoga and tabela[c]['green'] <= maior_valor_de_meio_analoga and tabela[c]['blue'] >= menor_valor_de_menor_analoga and tabela[c]['blue'] <= maior_valor_de_menor_analoga:
                    primeira.append(tabela[c])
                c += 1
                
            x = 0
            for x in range(len(tabela)):
                if tabela[x]['red'] >= menor_valor_de_maior_analoga and tabela[x]['red'] <= maior_valor_de_maior_analoga and tabela[x]['green'] >= menor_valor_de_menor_analoga and tabela[x]['green'] <= maior_valor_de_menor_analoga and tabela[x]['blue'] >= menor_valor_de_meio_analoga and tabela[x]['blue'] <= maior_valor_de_meio_analoga:
                    segunda.append(tabela[x])
                x += 1

        if maior_analoga == green:
            primeira_menor = "blue"
            segunda_menor = "red"
            c = 0
            for c in range(len(tabela)):
                if tabela[c]['red'] >= menor_valor_de_meio_analoga and tabela[c]['red'] <= maior_valor_de_meio_analoga and tabela[c]['green'] >= menor_valor_de_maior_analoga and tabela[c]['green'] <= maior_valor_de_maior_analoga and tabela[c]['blue'] >= menor_valor_de_menor_analoga and tabela[c]['blue'] <= maior_valor_de_menor_analoga:
                    primeira.append(tabela[c])
                c += 1
                
            x = 0
            for x in range(len(tabela)):
                if tabela[x]['red'] >= menor_valor_de_menor_analoga and tabela[x]['red'] <= maior_valor_de_menor_analoga and tabela[x]['green'] >= menor_valor_de_maior_analoga and tabela[x]['green'] <= maior_valor_de_maior_analoga and tabela[x]['blue'] >= menor_valor_de_meio_analoga and tabela[x]['blue'] <= maior_valor_de_meio_analoga:
                    segunda.append(tabela[x])
                x += 1
                
        if maior_analoga == blue:
            primeira_menor = "red"
            segunda_menor = "green"
            c = 0
            for c in range(len(tabela)):
                if tabela[c]['red'] >= menor_valor_de_menor_analoga and tabela[c]['red'] <= maior_valor_de_menor_analoga and tabela[c]['green'] >= menor_valor_de_meio_analoga and tabela[c]['green'] <= maior_valor_de_meio_analoga and tabela[c]['blue'] >= menor_valor_de_maior_analoga and tabela[c]['blue'] <= maior_valor_de_maior_analoga:
                    primeira.append(tabela[c])
                c += 1
                
            x = 0
            for x in range(len(tabela)):
                if tabela[x]['red'] >= menor_valor_de_meio_analoga and tabela[x]['red'] <= maior_valor_de_meio_analoga and tabela[x]['green'] >= menor_valor_de_menor_analoga and tabela[x]['green'] <= maior_valor_de_menor_analoga and tabela[x]['blue'] >= menor_valor_de_maior_analoga and tabela[x]['blue'] <= maior_valor_de_maior_analoga:
                    segunda.append(tabela[x])
                x += 1


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
                    # verifica se o resultado selecionado nao e igual ao primeiro
                    if resultado2[x]["red"] != resultado1[menor_distancia_1]["red"] and resultado2[x]["green"] != resultado1[menor_distancia_1]["green"] and resultado2[x]["blue"] != resultado1[menor_distancia_1]["blue"]:
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
            
        # filtra as linhas necessárias  
        resultado1 = filtrar_linhas_necessárias(resultado1)
        resultado2 = filtrar_linhas_necessárias(resultado2)
        
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