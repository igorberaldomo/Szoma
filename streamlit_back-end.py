import os, json
import pandas as pd
import sqlalchemy
import streamlit as st
from flask import Flask, request
def load_coral():
    with open("coral/coral.json", "r") as file:
        coral = json.load(file)
        coral = coral["corescoral"]
        return coral
def load_suvinil():
    with open("suvinil/suvinil.json", "r") as file:
        suvinil = json.load(file)
        suvinil = suvinil["coressuvinil"]
        return suvinil
    
coral = load_coral()
suvinil = load_suvinil()

def filter_lines(table):
    data = []
    i = 0
    for i in range(len(table)):
        data.append(
            {
                "nome": table[i]["nome"],
                "hexadecimal": table[i]["hexadecimal"],
                "fornecedores": table[i]["fornecedores"],
                "pantone_código": table[i]["pantone_código"],
                "red": table[i]["red"],
                "green": table[i]["green"],
                "blue": table[i]["blue"],
            }
        )
        i += 1
    return data


def select_complementos(red, green, blue, palheta, fornecedores):
    if palheta == "triade":
        lista_complementos.clear()
        desvio_maior = 70
        desvio_menor = 80
        maior = max(red, green, blue)
        menor = min(red, green, blue)
        meio = 0
        complemento1 = True
        complemento2 = True
        if red != maior and red != menor:
            meio = red
        if green != maior and green != menor:
            meio = green
        if blue != maior and blue != menor:
            meio = blue

        menor_valor_de_meio = meio - desvio_maior
        maior_valor_de_meio = meio + desvio_maior
        menor_valor_de_menor = menor - desvio_menor
        maior_valor_de_menor = menor + desvio_menor
        menor_valor_de_maior = maior - desvio_menor
        maior_valor_de_maior = maior + desvio_menor

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

        primeira = ""
        segunda = ""

        lista_de_complementos_1 = []
        lista_de_complementos_2 = []
        if maior == red:
            if fornecedores != "todos":
                if fornecedores == "suvinil":
                    posição = 0
                    while posição < len(suvinil):
                        if suvinil[posição]["red"] >= menor_valor_de_menor and suvinil[posição]["red"] <= maior_valor_de_menor and suvinil[posição]["green"] >= menor_valor_de_maior and suvinil[posição]["green"] <= maior_valor_de_maior and suvinil[posição]["blue"] >= menor_valor_de_meio and suvinil[posição]["blue"] <= maior_valor_de_meio:
                            lista_de_complementos_1.append(suvinil[posição])

                        if suvinil[posição]["red"] >= menor_valor_de_meio and suvinil[posição]["red"] <= maior_valor_de_meio and suvinil[posição]["green"] >= menor_valor_de_menor and suvinil[posição]["green"] <= maior_valor_de_menor and suvinil[posição]["blue"] >= menor_valor_de_maior and suvinil[posição]["blue"] <= maior_valor_de_maior:
                            lista_de_complementos_2.append(suvinil[posição])
                        posição += 1
                if fornecedores == "coral":
                    posição = 0
                    while posição < len(coral):
                        if coral[posição]["red"] >= menor_valor_de_menor and coral[posição]["red"] <= maior_valor_de_menor and coral[posição]["green"] >= menor_valor_de_maior and coral[posição]["green"] <= maior_valor_de_maior and coral[posição]["blue"] >= menor_valor_de_meio and coral[posição]["blue"] <= maior_valor_de_meio:
                            lista_de_complementos_1.append(coral[posição])

                        if coral[posição]["red"] >= menor_valor_de_meio and coral[posição]["red"] <= maior_valor_de_meio and coral[posição]["green"] >= menor_valor_de_menor and coral[posição]["green"] <= maior_valor_de_menor and coral[posição]["blue"] >= menor_valor_de_maior and coral[posição]["blue"] <= maior_valor_de_maior:
                            lista_de_complementos_2.append(coral[posição])
                        posição += 1
            else:
                posição = 0
                while posição < len(suvinil):
                    if suvinil[posição]["red"] >= menor_valor_de_menor and suvinil[posição]["red"] <= maior_valor_de_menor and suvinil[posição]["green"] >= menor_valor_de_maior and suvinil[posição]["green"] <= maior_valor_de_maior and suvinil[posição]["blue"] >= menor_valor_de_meio and suvinil[posição]["blue"] <= maior_valor_de_meio:
                        lista_de_complementos_1.append(suvinil[posição])
                    if coral[posição]["red"] >= menor_valor_de_menor and coral[posição]["red"] <= maior_valor_de_menor and coral[posição]["green"] >= menor_valor_de_maior and coral[posição]["green"] <= maior_valor_de_maior and coral[posição]["blue"] >= menor_valor_de_meio and coral[posição]["blue"] <= maior_valor_de_meio:
                            lista_de_complementos_1.append(coral[posição])

                    if suvinil[posição]["red"] >= menor_valor_de_meio and suvinil[posição]["red"] <= maior_valor_de_meio and suvinil[posição]["green"] >= menor_valor_de_menor and suvinil[posição]["green"] <= maior_valor_de_menor and suvinil[posição]["blue"] >= menor_valor_de_maior and suvinil[posição]["blue"] <= maior_valor_de_maior:
                        lista_de_complementos_2.append(suvinil[posição])
                    if coral[posição]["red"] >= menor_valor_de_meio and coral[posição]["red"] <= maior_valor_de_meio and coral[posição]["green"] >= menor_valor_de_menor and coral[posição]["green"] <= maior_valor_de_menor and coral[posição]["blue"] >= menor_valor_de_maior and coral[posição]["blue"] <= maior_valor_de_maior:
                            lista_de_complementos_2.append(coral[posição])
                    posição += 1

        if maior == green:
            if fornecedores != "todos":
                if fornecedores == "suvinil":
                    posição = 0
                    while posição < len(suvinil):
                        if suvinil[posição]["red"] >= menor_valor_de_meio and suvinil[posição]["red"] <= maior_valor_de_meio and suvinil[posição]["green"] >= menor_valor_de_menor and suvinil[posição]["green"] <= maior_valor_de_menor and suvinil[posição]["blue"] >= menor_valor_de_maior and suvinil[posição]["blue"] <= maior_valor_de_maior:
                            lista_de_complementos_1.append(suvinil[posição])

                        if suvinil[posição]["red"] >= menor_valor_de_maior and suvinil[posição]["red"] <= maior_valor_de_maior and suvinil[posição]["green"] >= menor_valor_de_meio and suvinil[posição]["green"] <= maior_valor_de_meio and suvinil[posição]["blue"] >= menor_valor_de_menor and suvinil[posição]["blue"] <= maior_valor_de_menor:
                            lista_de_complementos_2.append(suvinil[posição])
                        posição += 1
                if fornecedores == "coral":
                    posição = 0
                    while posição < len(coral):
                        if coral[posição]["red"] >= menor_valor_de_meio and coral[posição]["red"] <= maior_valor_de_meio and coral[posição]["green"] >= menor_valor_de_menor and coral[posição]["green"] <= maior_valor_de_menor and coral[posição]["blue"] >= menor_valor_de_maior and coral[posição]["blue"] <= maior_valor_de_maior:
                            lista_de_complementos_1.append(coral[posição])

                        if coral[posição]["red"] >= menor_valor_de_maior and coral[posição]["red"] <= maior_valor_de_maior and coral[posição]["green"] >= menor_valor_de_meio and coral[posição]["green"] <= maior_valor_de_meio and coral[posição]["blue"] >= menor_valor_de_menor and coral[posição]["blue"] <= maior_valor_de_menor:
                            lista_de_complementos_2.append(coral[posição])
                        posição += 1
            else:
                posição = 0
                while posição < len(suvinil):
                    if suvinil[posição]["red"] >= menor_valor_de_meio and suvinil[posição]["red"] <= maior_valor_de_meio and suvinil[posição]["green"] >= menor_valor_de_menor and suvinil[posição]["green"] <= maior_valor_de_menor and suvinil[posição]["blue"] >= menor_valor_de_maior and suvinil[posição]["blue"] <= maior_valor_de_maior:
                        lista_de_complementos_1.append(suvinil[posição])
                    if coral[posição]["red"] >= menor_valor_de_meio and coral[posição]["red"] <= maior_valor_de_meio and coral[posição]["green"] >= menor_valor_de_menor and coral[posição]["green"] <= maior_valor_de_menor and coral[posição]["blue"] >= menor_valor_de_maior and coral[posição]["blue"] <= maior_valor_de_maior:
                            lista_de_complementos_1.append(coral[posição])


                    if suvinil[posição]["red"] >= menor_valor_de_maior and suvinil[posição]["red"] <= maior_valor_de_maior and suvinil[posição]["green"] >= menor_valor_de_meio and suvinil[posição]["green"] <= maior_valor_de_meio and suvinil[posição]["blue"] >= menor_valor_de_menor and suvinil[posição]["blue"] <= maior_valor_de_menor:
                        lista_de_complementos_2.append(suvinil[posição])
                    if coral[posição]["red"] >= menor_valor_de_maior and coral[posição]["red"] <= maior_valor_de_maior and coral[posição]["green"] >= menor_valor_de_meio and coral[posição]["green"] <= maior_valor_de_meio and coral[posição]["blue"] >= menor_valor_de_menor and coral[posição]["blue"] <= maior_valor_de_menor:
                            lista_de_complementos_2.append(coral[posição])
                    posição += 1

        if maior == blue:
            if fornecedores != "todos":
                if fornecedores == "suvinil":
                    posição = 0
                    while posição < len(suvinil):
                        if suvinil[posição]["red"] >= menor_valor_de_menor and suvinil[posição]["red"] <= maior_valor_de_menor and suvinil[posição]["green"] >= menor_valor_de_maior and suvinil[posição]["green"] <= maior_valor_de_maior and suvinil[posição]["blue"] >= menor_valor_de_meio and suvinil[posição]["blue"] <= maior_valor_de_meio:
                            lista_de_complementos_1.append(suvinil[posição])

                        if suvinil[posição]["red"] >= menor_valor_de_maior and suvinil[posição]["red"] <= maior_valor_de_maior and suvinil[posição]["green"] >= menor_valor_de_meio and suvinil[posição]["green"] <= maior_valor_de_meio and suvinil[posição]["blue"] >= menor_valor_de_menor and suvinil[posição]["blue"] <= maior_valor_de_menor:
                            lista_de_complementos_2.append(suvinil[posição])
                        posição += 1
                if fornecedores == "coral":
                    posição = 0
                    while posição < len(coral):
                        if coral[posição]["red"] >= menor_valor_de_menor and coral[posição]["red"] <= maior_valor_de_menor and coral[posição]["green"] >= menor_valor_de_maior and coral[posição]["green"] <= maior_valor_de_maior and coral[posição]["blue"] >= menor_valor_de_meio and coral[posição]["blue"] <= maior_valor_de_meio:
                            lista_de_complementos_1.append(coral[posição])

                        if coral[posição]["red"] >= menor_valor_de_maior and coral[posição]["red"] <= maior_valor_de_maior and coral[posição]["green"] >= menor_valor_de_meio and coral[posição]["green"] <= maior_valor_de_meio and coral[posição]["blue"] >= menor_valor_de_menor and coral[posição]["blue"] <= maior_valor_de_menor:
                            lista_de_complementos_2.append(coral[posição])
                        posição += 1

            else:
                posição = 0
                while posição < len(suvinil):
                    if suvinil[posição]["red"] >= menor_valor_de_menor and suvinil[posição]["red"] <= maior_valor_de_menor and suvinil[posição]["green"] >= menor_valor_de_maior and suvinil[posição]["green"] <= maior_valor_de_maior and suvinil[posição]["blue"] >= menor_valor_de_meio and suvinil[posição]["blue"] <= maior_valor_de_meio:
                        lista_de_complementos_1.append(suvinil[posição])
                    if coral[posição]["red"] >= menor_valor_de_menor and coral[posição]["red"] <= maior_valor_de_menor and coral[posição]["green"] >= menor_valor_de_maior and coral[posição]["green"] <= maior_valor_de_maior and coral[posição]["blue"] >= menor_valor_de_meio and coral[posição]["blue"] <= maior_valor_de_meio:
                        lista_de_complementos_1.append(coral[posição])

                    if suvinil[posição]["red"] >= menor_valor_de_maior and suvinil[posição]["red"] <= maior_valor_de_maior and suvinil[posição]["green"] >= menor_valor_de_meio and suvinil[posição]["green"] <= maior_valor_de_meio and suvinil[posição]["blue"] >= menor_valor_de_menor and suvinil[posição]["blue"] <= maior_valor_de_menor:
                        lista_de_complementos_2.append(suvinil[posição])
                    if coral[posição]["red"] >= menor_valor_de_maior and coral[posição]["red"] <= maior_valor_de_maior and coral[posição]["green"] >= menor_valor_de_meio and coral[posição]["green"] <= maior_valor_de_meio and coral[posição]["blue"] >= menor_valor_de_menor and coral[posição]["blue"] <= maior_valor_de_menor:
                            lista_de_complementos_2.append(coral[posição])
                    posição += 1

        generate_pandas_table(lista_de_complementos_1, lista_de_complementos_2)

        if lista_de_complementos_1.empty and lista_de_complementos_2.empty:
            complemento1 = False
            complemento2 = False
        elif lista_de_complementos_1.empty:
            complemento1 = False
        elif lista_de_complementos_2.empty:
            complemento2 = False
        else:
            print(" ")
 

        c = 0
        x = 0
        menor_distancia_1 = 0
        menor_distancia_2 = 0
        while c < len(lista_de_complementos_1):
            atual_red = lista_de_complementos_1[c]["red"] - red
            atual_green = lista_de_complementos_1[c]["green"] - green
            atual_blue = lista_de_complementos_1[c]["blue"] - blue

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

        while x < len(lista_de_complementos_2):
            atual_red = lista_de_complementos_2[x]["red"] - red
            atual_green = lista_de_complementos_2[x]["green"] - green
            atual_blue = lista_de_complementos_2[x]["blue"] - blue

            if atual_red < 0:
                atual_red = atual_red * -1
            if atual_green < 0:
                atual_green = atual_green * -1
            if atual_blue < 0:
                atual_blue = atual_blue * -1

            distancia_atual = atual_red + atual_green + atual_blue
            if c == 0 or distancia_atual < distancia:
                if distancia_atual != 0:
                    menor_distancia_2 = x
                    distancia = distancia_atual
            x += 1

        lista_de_complementos_1 = filter_lines(lista_de_complementos_1)
        lista_de_complementos_2 = filter_lines(lista_de_complementos_2)

        if complemento1 == True and complemento2 == True:
            lista_complementos.append(lista_de_complementos_1[menor_distancia_1])
            lista_complementos.append(lista_de_complementos_2[menor_distancia_2])
        elif complemento1 == False:
            lista_complementos.append(lista_de_complementos_2[menor_distancia_2])
        elif complemento2 == False:
            lista_complementos.append(lista_de_complementos_1[menor_distancia_1])
        elif complemento1 == False and complemento2 == False:
            return []
        return lista_complementos
    elif palheta == "complementar":
        lista_complementos.clear()
        desvio_complementar = 60
        cr = 255 - red
        cg = 255 - green
        cb = 255 - blue
        complemento1 = True
        complemento2 = True
        cr_max = cr + desvio_complementar
        cr_min = cr - desvio_complementar
        cg_max = cg + desvio_complementar
        cg_min = cg - desvio_complementar
        cb_max = cb + desvio_complementar
        cb_min = cb - desvio_complementar
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

        cr_inter = (cr + red) / 2
        cg_inter = (cg + green) / 2
        cb_inter = (cb + blue) / 2

        cr_inter_max = cr_inter + desvio_complementar
        cr_inter_min = cr_inter - desvio_complementar
        cg_inter_max = cg_inter + desvio_complementar
        cg_inter_min = cg_inter - desvio_complementar
        cb_inter_max = cb_inter + desvio_complementar
        cb_inter_min = cb_inter - desvio_complementar

        cr_inter_max = int(cr_inter_max).__round__()
        cr_inter_min = int(cr_inter_min).__round__()
        cg_inter_max = int(cg_inter_max).__round__()
        cg_inter_min = int(cg_inter_min).__round__()
        cb_inter_max = int(cb_inter_max).__round__()
        cb_inter_min = int(cb_inter_min).__round__()
        intermediaria = []
        complementar = []

        if fornecedores != "todos":
            if fornecedores == "suvinil":
                    posição = 0
                    while posição < len(suvinil):
                        if suvinil[posição]["red"] >= cr_inter_min and suvinil[posição]["red"] <= cr_inter_max and suvinil[posição]["green"] >= cg_inter_min and suvinil[posição]["green"] <= cg_inter_max and suvinil[posição]["blue"] >= cb_inter_min and suvinil[posição]["blue"] <= cb_inter_max:
                            intermediaria.append(suvinil[posição])

                        if suvinil[posição]["red"] >= cr_min and suvinil[posição]["red"] <= cr_max and suvinil[posição]["green"] >= cg_inter_min and suvinil[posição]["green"] <= cg_max and suvinil[posição]["blue"] >= cb_inter_min and suvinil[posição]["blue"] <= cb_inter_max:
                            complementar.append(suvinil[posição])
                        posição += 1
            if fornecedores == "coral":
                posição = 0
                while posição < len(coral):
                    if coral[posição]["red"] >= cr_inter_min and coral[posição]["red"] <= cr_inter_max and coral[posição]["green"] >= cg_inter_min and coral[posição]["green"] <= cg_inter_max and coral[posição]["blue"] >= cb_inter_min and coral[posição]["blue"] <= cb_inter_max:
                        intermediaria.append(coral[posição])

                    if coral[posição]["red"] >= cr_min and coral[posição]["red"] <= cr_max and coral[posição]["green"] >= cg_min and coral[posição]["green"] <= cg_max and coral[posição]["blue"] >= cb_min and coral[posição]["blue"] <= cb_max:
                        complementar.append(coral[posição])
                    posição += 1
        else:
            posição = 0
            while posição < len(suvinil):
                if suvinil[posição]["red"] >= cr_inter_min and suvinil[posição]["red"] <= cr_inter_max and suvinil[posição]["green"] >= cg_inter_min and suvinil[posição]["green"] <= cg_inter_max and suvinil[posição]["blue"] >= cb_inter_min and suvinil[posição]["blue"] <= cb_inter_max:
                    intermediaria.append(suvinil[posição])
                if coral[posição]["red"] >= cr_inter_min and coral[posição]["red"] <= cr_inter_max and coral[posição]["green"] >= cg_inter_min and coral[posição]["green"] <= cg_inter_max and coral[posição]["blue"] >= cb_inter_min and coral[posição]["blue"] <= cb_inter_max:
                    intermediaria.append(coral[posição])

                if suvinil[posição]["red"] >= cr_min and suvinil[posição]["red"] <= cr_max and suvinil[posição]["green"] >= cg_inter_min and suvinil[posição]["green"] <= cg_max and suvinil[posição]["blue"] >= cb_inter_min and suvinil[posição]["blue"] <= cb_inter_max:
                    complementar.append(suvinil[posição])
                if coral[posição]["red"] >= cr_min and coral[posição]["red"] <= cr_max and coral[posição]["green"] >= cg_min and coral[posição]["green"] <= cg_max and coral[posição]["blue"] >= cb_min and coral[posição]["blue"] <= cb_max:
                    complementar.append(coral[posição])
                posição += 1

        if lista_de_complementos_1.empty and lista_de_complementos_2.empty:
            complemento1 = False
            complemento2 = False
        elif lista_de_complementos_1.empty:
            complemento1 = False
        elif lista_de_complementos_2.empty:
            complemento2 = False
        else:
            print(" ")
        
        c = 0
        x = 0
        menor_distancia_1 = 0
        menor_distancia_2 = 0

        while c < len(intermediaria):
            atual_red = intermediaria[c]["red"] - cr_inter
            atual_green = intermediaria[c]["green"] - cg_inter
            atual_blue = intermediaria[c]["blue"] - cb_inter

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

        while x < len(complementar):
            atual_red = complementar[x]["red"] - cr
            atual_green = complementar[x]["green"] - cg
            atual_blue = complementar[x]["blue"] - cb

            if atual_red < 0:
                atual_red = atual_red * -1
            if atual_green < 0:
                atual_green = atual_green * -1
            if atual_blue < 0:
                atual_blue = atual_blue * -1

            distancia_atual = atual_red + atual_green + atual_blue
            if c == 0 or distancia_atual < distancia:
                if distancia_atual != 0:
                    menor_distancia_2 = x
                    distancia = distancia_atual
            x += 1


        if complemento1 == True and complemento2 == True:
            lista_complementos.append(intermediaria[menor_distancia_1])
            lista_complementos.append(complementar[menor_distancia_2])
        elif complemento1 == False:
            lista_complementos.append(complementar[menor_distancia_2])
        elif complemento2 == False:
            lista_complementos.append(intermediaria[menor_distancia_1])
        elif complemento1 == False and complemento2 == False:
            return []

        return lista_complementos

    elif palheta == "análoga":
        lista_complementos.clear()
        desvio_maior_analoga = 80
        desvio_menor_analoga = 60
        complemento1 = True
        complemento2 = True
        maior_analoga = max(red, green, blue)
        menor_analoga = min(red, green, blue)
        meio_analoga = 0
        if (
            blue == menor_analoga
            and green == maior_analoga
            or blue == maior_analoga
            and green == menor_analoga
        ):
            meio_analoga = red
        if (
            red == maior_analoga
            and blue == menor_analoga
            or red == menor_analoga
            and blue == maior_analoga
        ):
            meio_analoga = green
        if (
            red == maior_analoga
            and green == menor_analoga
            or red == menor_analoga
            and green == maior_analoga
        ):
            meio_analoga = blue

        menor_valor_de_maior_analoga = maior_analoga - desvio_menor_analoga
        maior_valor_de_maior_analoga = maior_analoga + desvio_menor_analoga
        menor_valor_de_menor_analoga = menor_analoga - desvio_menor_analoga
        maior_valor_de_menor_analoga = menor_analoga + desvio_menor_analoga
        menor_valor_de_meio_analoga = meio_analoga - desvio_maior_analoga
        maior_valor_de_meio_analoga = meio_analoga + desvio_maior_analoga

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
        primeira_analoga = []
        segunda_analoga = []

        if maior_analoga == red:
            if fornecedores != "todos":
                if fornecedores == "suvinil":
                    posição = 0
                    while posição < len(suvinil):
                        if suvinil[posição]["red"] >= menor_valor_de_maior_analoga and suvinil[posição]["red"] <= maior_valor_de_maior_analoga and suvinil[posição]["green"] >= menor_valor_de_meio_analoga and suvinil[posição]["green"] <= maior_valor_de_meio_analoga and suvinil[posição]["blue"] >= menor_valor_de_menor_analoga and suvinil[posição]["blue"] <= maior_valor_de_menor_analoga:
                            primeira_analoga.append(suvinil[posição])

                        if suvinil[posição]["red"] >= menor_valor_de_maior_analoga and suvinil[posição]["red"] <= maior_valor_de_maior_analoga and suvinil[posição]["green"] >= menor_valor_de_menor_analoga and suvinil[posição]["green"] <= maior_valor_de_menor_analoga and suvinil[posição]["blue"] >= menor_valor_de_meio_analoga and suvinil[posição]["blue"] <= maior_valor_de_meio_analoga:
                            segunda_analoga.append(suvinil[posição])
                        posição += 1
                if fornecedores == "coral":
                    posição = 0
                    while posição < len(coral):
                        if coral[posição]["red"] >= menor_valor_de_maior_analoga and coral[posição]["red"] <= maior_valor_de_maior_analoga and coral[posição]["green"] >= menor_valor_de_meio_analoga and coral[posição]["green"] <= maior_valor_de_meio_analoga and coral[posição]["blue"] >= menor_valor_de_menor_analoga and coral[posição]["blue"] <= maior_valor_de_menor_analoga:
                            primeira_analoga.append(coral[posição])

                        if coral[posição]["red"] >= menor_valor_de_maior_analoga and coral[posição]["red"] <= maior_valor_de_maior_analoga and coral[posição]["green"] >= menor_valor_de_menor_analoga and coral[posição]["green"] <= maior_valor_de_menor_analoga and coral[posição]["blue"] >= menor_valor_de_meio_analoga and coral[posição]["blue"] <= maior_valor_de_meio_analoga:
                            segunda_analoga.append(coral[posição])
                        posição += 1
            else:
                posição = 0
                while posição < len(suvinil):
                    if suvinil[posição]["red"] >= menor_valor_de_maior_analoga and suvinil[posição]["red"] <= maior_valor_de_maior_analoga and suvinil[posição]["green"] >= menor_valor_de_meio_analoga and suvinil[posição]["green"] <= maior_valor_de_meio_analoga and suvinil[posição]["blue"] >= menor_valor_de_menor_analoga and suvinil[posição]["blue"] <= maior_valor_de_menor_analoga:
                        primeira_analoga.append(suvinil[posição])
                    if coral[posição]["red"] >= menor_valor_de_maior_analoga and coral[posição]["red"] <= maior_valor_de_maior_analoga and coral[posição]["green"] >= menor_valor_de_meio_analoga and coral[posição]["green"] <= maior_valor_de_meio_analoga and coral[posição]["blue"] >= menor_valor_de_menor_analoga and coral[posição]["blue"] <= maior_valor_de_menor_analoga:
                        primeira_analoga.append(coral[posição])

                    if suvinil[posição]["red"] >= menor_valor_de_maior_analoga and suvinil[posição]["red"] <= maior_valor_de_maior_analoga and suvinil[posição]["green"] >= menor_valor_de_menor_analoga and suvinil[posição]["green"] <= maior_valor_de_menor_analoga and suvinil[posição]["blue"] >= menor_valor_de_meio_analoga and suvinil[posição]["blue"] <= maior_valor_de_meio_analoga:
                        segunda_analoga.append(suvinil[posição])
                    if coral[posição]["red"] >= menor_valor_de_maior_analoga and coral[posição]["red"] <= maior_valor_de_maior_analoga and coral[posição]["green"] >= menor_valor_de_menor_analoga and coral[posição]["green"] <= maior_valor_de_menor_analoga and coral[posição]["blue"] >= menor_valor_de_meio_analoga and coral[posição]["blue"] <= maior_valor_de_meio_analoga:
                        segunda_analoga.append(coral[posição])
                    posição += 1

        if maior_analoga == green:
            if fornecedores != "todos":
                if fornecedores == "suvinil":
                    posição = 0
                    while posição < len(suvinil):
                        if suvinil[posição]["red"] >= menor_valor_de_meio_analoga and suvinil[posição]["red"] <= maior_valor_de_meio_analoga and suvinil[posição]["green"] >= menor_valor_de_maior_analoga and suvinil[posição]["green"] <= maior_valor_de_maior_analoga and suvinil[posição]["blue"] >= menor_valor_de_menor_analoga and suvinil[posição]["blue"] <= maior_valor_de_menor_analoga:
                            primeira_analoga.append(suvinil[posição])

                        if suvinil[posição]["red"] >= menor_valor_de_menor_analoga and suvinil[posição]["red"] <= maior_valor_de_menor_analoga and suvinil[posição]["green"] >= menor_valor_de_maior_analoga and suvinil[posição]["green"] <= maior_valor_de_maior_analoga and suvinil[posição]["blue"] >= menor_valor_de_meio_analoga and suvinil[posição]["blue"] <= maior_valor_de_meio_analoga:
                            segunda_analoga.append(suvinil[posição])
                        posição += 1
                if fornecedores == "coral":
                    posição = 0
                    while posição < len(coral):
                        if coral[posição]["red"] >= menor_valor_de_meio_analoga and coral[posição]["red"] <= maior_valor_de_meio_analoga and coral[posição]["green"] >= menor_valor_de_maior_analoga and coral[posição]["green"] <= maior_valor_de_maior_analoga and coral[posição]["blue"] >= menor_valor_de_menor_analoga and coral[posição]["blue"] <= maior_valor_de_menor_analoga:
                            primeira_analoga.append(coral[posição])

                        if coral[posição]["red"] >= menor_valor_de_menor_analoga and coral[posição]["red"] <= maior_valor_de_menor_analoga and coral[posição]["green"] >= menor_valor_de_maior_analoga and coral[posição]["green"] <= maior_valor_de_maior_analoga and coral[posição]["blue"] >= menor_valor_de_meio_analoga and coral[posição]["blue"] <= maior_valor_de_meio_analoga:
                            segunda_analoga.append(coral[posição])
                        posição += 1
            else:
                posição = 0
                while posição < len(suvinil):
                    if suvinil[posição]["red"] >= menor_valor_de_meio_analoga and suvinil[posição]["red"] <= maior_valor_de_meio_analoga and suvinil[posição]["green"] >= menor_valor_de_maior_analoga and suvinil[posição]["green"] <= maior_valor_de_maior_analoga and suvinil[posição]["blue"] >= menor_valor_de_menor_analoga and suvinil[posição]["blue"] <= maior_valor_de_menor_analoga:
                        primeira_analoga.append(suvinil[posição])
                    if suvinil[posição]["red"] >= menor_valor_de_menor_analoga and suvinil[posição]["red"] <= maior_valor_de_menor_analoga and suvinil[posição]["green"] >= menor_valor_de_maior_analoga and suvinil[posição]["green"] <= maior_valor_de_maior_analoga and suvinil[posição]["blue"] >= menor_valor_de_meio_analoga and suvinil[posição]["blue"] <= maior_valor_de_meio_analoga:
                        segunda_analoga.append(suvinil[posição])
                    posição += 1
                    
                posição = 0        
                while posicao < len(coral):        
                    if coral[posição]["red"] >= menor_valor_de_meio_analoga and coral[posição]["red"] <= maior_valor_de_meio_analoga and coral[posição]["green"] >= menor_valor_de_maior_analoga and coral[posição]["green"] <= maior_valor_de_maior_analoga and coral[posição]["blue"] >= menor_valor_de_menor_analoga and coral[posição]["blue"] <= maior_valor_de_menor_analoga:
                        primeira_analoga.append(coral[posição])

                    if coral[posição]["red"] >= menor_valor_de_menor_analoga and coral[posição]["red"] <= maior_valor_de_menor_analoga and coral[posição]["green"] >= menor_valor_de_maior_analoga and coral[posição]["green"] <= maior_valor_de_maior_analoga and coral[posição]["blue"] >= menor_valor_de_meio_analoga and coral[posição]["blue"] <= maior_valor_de_meio_analoga:
                        segunda_analoga.append(coral[posição])
                    posição += 1

        if maior_analoga == blue:
            if fornecedores != "todos":
                if fornecedores == "suvinil":
                    posição = 0
                    while posição < len(suvinil):
                        if suvinil[posição]["red"] >= menor_valor_de_menor_analoga and suvinil[posição]["red"] <= maior_valor_de_menor_analoga and suvinil[posição]["green"] >= menor_valor_de_meio_analoga and suvinil[posição]["green"] <= maior_valor_de_meio_analoga and suvinil[posição]["blue"] >= menor_valor_de_maior_analoga and suvinil[posição]["blue"] <= maior_valor_de_maior_analoga:
                            primeira_analoga.append(suvinil[posição])

                        if suvinil[posição]["red"] >= menor_valor_de_meio_analoga and suvinil[posição]["red"] <= maior_valor_de_meio_analoga and suvinil[posição]["green"] >= menor_valor_de_menor_analoga and suvinil[posição]["green"] <= maior_valor_de_menor_analoga and suvinil[posição]["blue"] >= menor_valor_de_maior_analoga and suvinil[posição]["blue"] <= maior_valor_de_maior_analoga:
                            segunda_analoga.append(suvinil[posição])
                        posição += 1
                if fornecedores == "coral":
                    posição = 0
                    while posição < len(coral):
                        if coral[posição]["red"] >= menor_valor_de_menor_analoga and coral[posição]["red"] <= maior_valor_de_menor_analoga and coral[posição]["green"] >= menor_valor_de_meio_analoga and coral[posição]["green"] <= maior_valor_de_meio_analoga and coral[posição]["blue"] >= menor_valor_de_maior_analoga and coral[posição]["blue"] <= maior_valor_de_maior_analoga:
                            primeira_analoga.append(coral[posição])

                        if coral[posição]["red"] >= menor_valor_de_meio_analoga and coral[posição]["red"] <= maior_valor_de_meio_analoga and coral[posição]["green"] >= menor_valor_de_menor_analoga and coral[posição]["green"] <= maior_valor_de_menor_analoga and coral[posição]["blue"] >= menor_valor_de_maior_analoga and coral[posição]["blue"] <= maior_valor_de_maior_analoga:
                            segunda_analoga.append(coral[posição])
                        posição += 1
            else:
                posição = 0
                while posição < len(suvinil):
                    if suvinil[posição]["red"] >= menor_valor_de_menor_analoga and suvinil[posição]["red"] <= maior_valor_de_menor_analoga and suvinil[posição]["green"] >= menor_valor_de_meio_analoga and suvinil[posição]["green"] <= maior_valor_de_meio_analoga and suvinil[posição]["blue"] >= menor_valor_de_maior_analoga and suvinil[posição]["blue"] <= maior_valor_de_maior_analoga:
                        primeira_analoga.append(suvinil[posição])
                    if suvinil[posição]["red"] >= menor_valor_de_meio_analoga and suvinil[posição]["red"] <= maior_valor_de_meio_analoga and suvinil[posição]["green"] >= menor_valor_de_menor_analoga and suvinil[posição]["green"] <= maior_valor_de_menor_analoga and suvinil[posição]["blue"] >= menor_valor_de_maior_analoga and suvinil[posição]["blue"] <= maior_valor_de_maior_analoga:
                        segunda_analoga.append(suvinil[posição])
                    posição += 1
                    
                posição = 0
                while posição < len(suvinil):      
                    if coral[posição]["red"] >= menor_valor_de_menor_analoga and coral[posição]["red"] <= maior_valor_de_menor_analoga and coral[posição]["green"] >= menor_valor_de_meio_analoga and coral[posição]["green"] <= maior_valor_de_meio_analoga and coral[posição]["blue"] >= menor_valor_de_maior_analoga and coral[posição]["blue"] <= maior_valor_de_maior_analoga:
                        primeira_analoga_analoga.append(coral[posição])
                    if coral[posição]["red"] >= menor_valor_de_meio_analoga and coral[posição]["red"] <= maior_valor_de_meio_analoga and coral[posição]["green"] >= menor_valor_de_menor_analoga and coral[posição]["green"] <= maior_valor_de_menor_analoga and coral[posição]["blue"] >= menor_valor_de_maior_analoga and coral[posição]["blue"] <= maior_valor_de_maior_analoga:
                        segunda_analoga.append(coral[posição])
                    posição += 1

        if primeira_analoga.empty and segunda_analoga.empty:
            complemento1 = False
            complemento2 = False
        elif primeira_analoga.empty:
            complemento1 = False
        elif segunda_analoga.empty:
            complemento2 = False

        c = 0
        x = 0
        menor_distancia_1 = 0
        menor_distancia_2 = 0

        while c < len(primeira_analoga):
            atual_red = primeira_analoga[c]["red"] - red
            atual_green = primeira_analoga[c]["green"] - green
            atual_blue = primeira_analoga[c]["blue"] - blue

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

        while x < len(segunda_analoga):
            atual_red = segunda_analoga[x]["red"] - red
            atual_green = segunda_analoga[x]["green"] - green
            atual_blue = segunda_analoga[x]["blue"] - blue
            if atual_red < 0:
                atual_red = atual_red * -1
            if atual_green < 0:
                atual_green = atual_green * -1
            if atual_blue < 0:
                atual_blue = atual_blue * -1

            distancia_atual = atual_red + atual_green + atual_blue
            if c == 0 or distancia_atual < distancia:
                if distancia_atual != 0:
                    menor_distancia_2 = x
                    distancia = distancia_atual
            x += 1

        if complemento1 == True and complemento2 == True:
            lista_complementos.append(primeira_analoga[menor_distancia_1])
            lista_complementos.append(segunda_analoga[menor_distancia_2])
        elif complemento1 == False:
            lista_complementos.append(segunda_analoga[menor_distancia_2])
        elif complemento2 == False:
            lista_complementos.append(primeira_analoga[menor_distancia_1])
        elif complemento1 == False and complemento2 == False:
            return []
        return lista_complementos
    else:
        err = "Complemento indisponível"
        print(err)
        return err


def select_hexadecimal(hexadecimal, fornecedores):
    hexadecimal_list = []
    hexadecimal_list.clear()
    
    if fornecedores != "todos":
        if fornecedores == "suvinil":
            posição = 0
            for posição in range(len(suvinil["coressuvinil"])):
                if suvinil["hexadecimal"] == hexadecimal or suvinil["pantone"]["hex"] == hexadecimal:
                    hexadecimal_list.append(suvinil[posição])
                posição += 1
        if fornecedores == "coral":
            posição = 0
            for posição in range(len(coral["corescoral"])):
                if coral["hexadecimal"] == hexadecimal or coral["pantone"]["hex"] == hexadecimal:
                    hexadecimal_list.append(coral[posição])
                posição += 1
    else:
        posição = 0
        for posição in range(len(suvinil["coressuvinil"])):
            if suvinil["hexadecimal"] == hexadecimal or suvinil["pantone"]["hex"] == hexadecimal:
                hexadecimal_list.append(suvinil[posição])
            posição += 1
        posição = 0
        for posição in range(len(coral["corescoral"])):
            if coral["hexadecimal"] == hexadecimal or coral["pantone"]["hex"] == hexadecimal:
                    hexadecimal_list.append(coral[posição])
            posição += 1

    resultset = pd.read_sql(search_string, engine)
    return resultset


def select_códigos(codigo, fornecedores):
    codigo_list = []
    codigo_list.clear()
    
    if fornecedores != "todos":
        if fornecedores == "suvinil":
            posição = 0
            for posição in range(len(suvinil["coressuvinil"])):
                if suvinil["pantone"]["codigo"] == codigo:
                    codigo_list.append(suvinil)
                posição += 1
                
        if fornecedores == "coral":
            posição = 0
            for posição in range(len(coral["corescoral"])):
                if coral["pantone"]["codigo"] == codigo:
                    codigo_list.append(coral)
                posição += 1
                
    else:
        search_string = f"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil WHERE pantone_código = '{codigo}' union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral WHERE pantone_código = '{codigo}' "
    resultset = pd.read_sql(search_string, engine)
    return resultset


def select_id(request_id, nome, fornecedores):
    if fornecedores != "todos":
        seach_string = f"Select * from {fornecedores} WHERE id = {request_id}"
        resultset = pd.read_sql(seach_string, engine)
    else:
        seach_string = f"Select * from suvinil WHERE id = {request_id} "
        search_string_2 = f"Select * from coral WHERE id = {request_id}"
        resultset_1 = pd.read_sql(seach_string, engine)
        resultset_2 = pd.read_sql(search_string_2, engine)
        if nome in resultset_1["nome"].values:
            resultset = resultset_1
        else:
            resultset = resultset_2
    return resultset


def search_name_for_id(nome):
    with open("search/search_dict.json", "r") as file:
        search_dict = json.load(file)
        select_id = None
        if nome in search_dict["quickSearch"][0]:
            select_id = search_dict["quickSearch"][0][nome]
        if nome in search_dict["suvinil"][0]:
            select_id = search_dict["suvinil"][0][nome]
        if nome in search_dict["coral"][0]:
            select_id = search_dict["coral"][0][nome]
        print(select_id)
    return select_id


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
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
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


app = Flask(__name__)
lastQuery = list()


@app.route("/", methods=["GET"])
def infopage():
    return "<h1>Colors API</h1><p>This api will request a picture or RGB, and will return a product (paint, tiles, fabrics) </p> "


@app.route("/suvinil/", methods=["GET", "POST"])
def getsuvinilColors():
    if request.method == "POST":
        req = request.get_json()
        red = req["cor"][0]
        green = req["cor"][1]
        blue = req["cor"][2]
        response = primary_select(red, green, blue, req["fornecedores"])
        response = response.to_dict(orient="records")
        c = 0
        while c < len(response):
            lastQuery.append(response[c])
            c += 1
        with open("response/response.json", "w+") as file:
            json.dump(lastQuery, file)
            lastQuery.clear()

        return response
    if request.method == "GET":
        with open("response/response.json", "r") as file:
            response = json.load(file)
            return response


@app.route("/names/", methods=["POST"])
def getNames():
    if request.method == "POST":
        req = request.get_json()
        nome = req["nome"]
        fornecedores = req["fornecedores"]
        request_id = search_name_for_id(nome)
        response = select_id(request_id, nome, fornecedores)
        response = response.to_dict(orient="records")
        with open("response/response.json", "w+") as file:
            json.dump(response, file)
        return response


@app.route("/codigos/", methods=["POST"])
def getProcura():
    if request.method == "POST":
        codigo_cor = request.get_json()
        codigo = codigo_cor["codigo"]
        fornecedores = codigo_cor["fornecedores"]
        response = select_códigos(codigo, fornecedores)
        response = response.to_dict(orient="records")
        with open("response/response.json", "w+") as file:
            json.dump(response, file)
        return response


@app.route("/hex/", methods=["POST"])
def getHex():
    if request.method == "POST":
        codigo_cor = request.get_json()
        hexadecimal = codigo_cor["headecimal"]
        fornecedores = codigo_cor["fornecedores"]
        response = select_hexadecimal(hexadecimal, fornecedores)
        response = response.to_dict(orient="records")
        with open("response/response.json", "w+") as file:
            json.dump(response, file)
        return response


@app.route("/complementos/", methods=["GET", "POST"])
def getComplementos():
    if request.method == "POST":
        complementos = request.get_json()
        red = complementos["red"]
        green = complementos["green"]
        blue = complementos["blue"]
        palheta = complementos["palheta"]
        fornecedores = complementos["fornecedores"]
        lista = select_complementos(red, green, blue, palheta, fornecedores)
        c = 0
        while c < len(lista):
            lastQuery.append(lista[c])
            c += 1
        with open("complementos/complementos.json", "w+") as file:
            json.dump(lastQuery, file)
            lastQuery.clear()
        return lastQuery
    if request.method == "GET":
        with open("complementos/complementos.json", "r") as file:
            response = json.load(file)
            return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)
