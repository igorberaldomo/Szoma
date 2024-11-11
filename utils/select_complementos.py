import os, json
import pandas as pd
import sqlalchemy
from utils.conect_to_engine_developer import conect_to_engine_developer
from utils.conect_to_engine_production import conect_to_engine_production
from utils.create_pandas_table import generate_pandas_table
from utils.filter_lines import filter_lines

# engine = conect_to_engine_developer()
engine = conect_to_engine_production()

def select_complementos(red, green, blue, palheta, fornecedores):
    lista_complementos = []
    if palheta == "triade":
        lista_complementos.clear()
        desvio_maior = 80
        desvio_menor = 70
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
        primeira_maior = ""
        segunda_maior = ""
        if maior == red:
            if fornecedores != "todos":
                primeira = f"SELECT * from {fornecedores} WHERE red >= {menor_valor_de_menor} AND red <= {maior_valor_de_menor} AND green >= {menor_valor_de_maior} AND green <= {maior_valor_de_maior} AND blue >= {menor_valor_de_meio} AND blue <={maior_valor_de_meio} "


                segunda = f"SELECT * from {fornecedores} WHERE red >= {menor_valor_de_meio} AND red <={maior_valor_de_meio} AND green >= {menor_valor_de_menor} AND green <= {maior_valor_de_menor} AND blue >= {menor_valor_de_maior} AND blue <= {maior_valor_de_maior} "

            else:
                primeira = f"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores FROM suvinil WHERE red >= {menor_valor_de_menor} AND red <= {maior_valor_de_menor} AND green >= {menor_valor_de_maior} AND green <= {maior_valor_de_maior} AND blue >= {menor_valor_de_meio} AND blue <={maior_valor_de_meio} union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores FROM coral WHERE red >= {menor_valor_de_menor} AND red <= {maior_valor_de_menor} AND green >= {menor_valor_de_maior} AND green <= {maior_valor_de_maior} AND blue >= {menor_valor_de_meio} AND blue <={maior_valor_de_meio}"
                segunda = f"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores FROM suvinil WHERE red >= {menor_valor_de_meio} AND red <= {maior_valor_de_meio} AND green >= {menor_valor_de_menor} AND green <= {maior_valor_de_menor} AND blue >= {menor_valor_de_maior} AND blue <={maior_valor_de_maior} union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores FROM coral WHERE red >= {menor_valor_de_meio} AND red <= {maior_valor_de_meio} AND green >= {menor_valor_de_menor} AND green <= {maior_valor_de_menor} AND blue >= {menor_valor_de_maior} AND blue <={maior_valor_de_maior}" 

        if maior == green:
            if fornecedores != "todos":
                primeira = f"SELECT * from {fornecedores} WHERE red >={menor_valor_de_meio} AND red <={maior_valor_de_meio} AND green >= {menor_valor_de_menor} AND green <= {maior_valor_de_menor} AND blue >= {menor_valor_de_maior} AND blue <= {maior_valor_de_maior} "

                segunda = f"SELECT * from {fornecedores} WHERE red >= {menor_valor_de_maior} AND red <= {maior_valor_de_maior} AND green >= {menor_valor_de_meio} AND green <= {maior_valor_de_meio} AND blue >= {menor_valor_de_menor} AND blue <={maior_valor_de_menor} "
            else:
                primeira = f"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil WHERE red >={menor_valor_de_meio} AND red <={maior_valor_de_meio} AND green >= {menor_valor_de_menor} AND green <= {maior_valor_de_menor} AND blue >= {menor_valor_de_maior} AND blue <= {maior_valor_de_maior} union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral WHERE red >={menor_valor_de_meio} AND red <={maior_valor_de_meio} AND green >= {menor_valor_de_menor} AND green <= {maior_valor_de_menor} AND blue >= {menor_valor_de_maior} AND blue <= {maior_valor_de_maior} "

                segunda = f"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil WHERE red >= {menor_valor_de_maior} AND red <= {maior_valor_de_maior} AND green >= {menor_valor_de_meio} AND green <= {maior_valor_de_meio} AND blue >= {menor_valor_de_menor} AND blue <={maior_valor_de_menor} union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral WHERE red >= {menor_valor_de_maior} AND red <= {maior_valor_de_maior} AND green >= {menor_valor_de_meio} AND green <= {maior_valor_de_meio} AND blue >= {menor_valor_de_menor} AND blue <={maior_valor_de_menor}"

        if maior == blue:
            if fornecedores != "todos":
                primeira = f"SELECT * from {fornecedores} WHERE red >= {menor_valor_de_meio} AND red <= {maior_valor_de_meio} AND green >= {menor_valor_de_maior} AND green <= {maior_valor_de_maior} AND blue >= {menor_valor_de_menor} AND blue <={maior_valor_de_menor} "
                segunda = f"SELECT * from {fornecedores} WHERE red >= {menor_valor_de_maior} AND red <={maior_valor_de_maior} AND green >= {menor_valor_de_meio} AND green <= {maior_valor_de_meio} AND blue >= {menor_valor_de_menor} AND blue <= {maior_valor_de_menor} "
            else:
                primeira = f"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil WHERE red >= {menor_valor_de_meio} AND red <= {maior_valor_de_meio} AND green >= {menor_valor_de_maior} AND green <= {maior_valor_de_maior} AND blue >= {menor_valor_de_menor} AND blue <={maior_valor_de_menor} union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral WHERE red >= {menor_valor_de_meio} AND red <= {maior_valor_de_meio} AND green >= {menor_valor_de_maior} AND green <= {maior_valor_de_maior} AND blue >= {menor_valor_de_menor} AND blue <={maior_valor_de_menor}"

                segunda = f"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil WHERE red >= {menor_valor_de_maior} AND red <={maior_valor_de_maior} AND green >= {menor_valor_de_menor} AND green <= {maior_valor_de_menor} AND blue >= {menor_valor_de_meio} AND blue <= {maior_valor_de_meio} union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral WHERE red >= {menor_valor_de_maior} AND red <={maior_valor_de_maior} AND green >= {menor_valor_de_menor} AND green <= {maior_valor_de_menor} AND blue >= {menor_valor_de_meio} AND blue <= {maior_valor_de_meio} "

        resultado1 = pd.read_sql(primeira, engine)
        resultado2 = pd.read_sql(segunda, engine)

        # generate_pandas_table(primeira, segunda)
        if maior == red:
            primeira_maior = "green"
            segunda_maior = "blue"

        if maior == green:
            primeira_maior = "blue"
            segunda_maior = "red"

        if maior == blue:
            segunda_maior = "green"
            primeira_maior = "red"

        
        if resultado1.empty and resultado2.empty:
            complemento1 = False
            complemento2 = False
        elif resultado1.empty:
            complemento1 = False
        elif resultado2.empty:
            complemento2 = False
        else:
            print(" ")
        resultado1 = resultado1.to_dict(orient="records")
        resultado2 = resultado2.to_dict(orient="records")

        c = 0
        x = 0
        distancia_1 = 0
        distancia_2 = 0
        menor_distancia_1 = 0
        menor_distancia_2 = 0
        print(primeira_maior)
        while c < len(resultado1):
            atual_red = resultado1[c]["red"] - red
            atual_green = resultado1[c]["green"] - green
            atual_blue = resultado1[c]["blue"] - blue

            if atual_red < 0:
                atual_red = atual_red * -1
            if atual_green < 0:
                atual_green = atual_green * -1
            if atual_blue < 0:
                atual_blue = atual_blue * -1

            distancia_atual = atual_red + atual_green + atual_blue

            if c == 0 or distancia_atual < distancia_1:
                if distancia_atual != 0:
                    if primeira_maior == "red":
                        if atual_red > atual_blue and atual_red > atual_green:
                            menor_distancia_1 = c
                            distancia_1 = distancia_atual
                    if primeira_maior == "green":
                        if atual_green > atual_blue and atual_green > atual_red:
                            menor_distancia_1 = c
                            distancia_1 = distancia_atual
                    if primeira_maior == "blue":
                        if atual_blue > atual_green and atual_blue > atual_red:
                            menor_distancia_1 = c
                            distancia_1 = distancia_atual
            c += 1
        print(segunda_maior)
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
            if c == 0 or distancia_atual < distancia_2:
                if distancia_atual != 0:
                    if segunda_maior == "red":
                        if atual_red > atual_blue and atual_red > atual_green:
                            menor_distancia_2 = x
                            distancia_2 = distancia_atual
                    if segunda_maior == "green":
                        if atual_green > atual_blue and atual_green > atual_red:
                            menor_distancia_2 = x
                            distancia_2 = distancia_atual
                    if segunda_maior == "blue":
                        if atual_blue > atual_green and atual_blue > atual_red:
                            menor_distancia_2 = x
                            distancia_2 = distancia_atual
            x += 1
        
        resultado1 = filter_lines(resultado1)
        resultado2 = filter_lines(resultado2)
        if complemento1 == True and complemento2 == True:
            lista_complementos.append(resultado1[menor_distancia_1])
            lista_complementos.append(resultado2[menor_distancia_2])
        elif complemento1 == False:
            lista_complementos.append(resultado2[menor_distancia_2])
        elif complemento2 == False:
            lista_complementos.append(resultado1[menor_distancia_1])
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
        intermediaria = ""
        complementar = ""

        if fornecedores != "todos":
            intermediaria = f"SELECT * from {fornecedores} WHERE red >= {cr_inter_min} AND red <= {cr_inter_max} AND green >= {cg_inter_min} AND green <= {cg_inter_max} AND blue >= {cb_inter_min} AND blue <= {cb_inter_max} "

            complementar = f"SELECT * from {fornecedores} WHERE red >= {cr_min} AND red <= {cr_max} AND green >= {cg_min} AND green <= {cg_max} AND blue >= {cb_min} AND blue <= {cb_max} "
        else:
            intermediaria = f"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil WHERE red >= {cr_inter_min} AND red <= {cr_inter_max} AND green >= {cg_inter_min} AND green <= {cg_inter_max} AND blue >= {cb_inter_min} AND blue <= {cb_inter_max} union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral WHERE red >= {cr_inter_min} AND red <= {cr_inter_max} AND green >= {cg_inter_min} AND green <= {cg_inter_max} AND blue >= {cb_inter_min} AND blue <= {cb_inter_max}"

            complementar = f"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil WHERE red >= {cr_min} AND red <= {cr_max} AND green >= {cg_min} AND green <= {cg_max} AND blue >= {cb_min} AND blue <= {cb_max} union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral WHERE red >= {cr_min} AND red <= {cr_max} AND green >= {cg_min} AND green <= {cg_max} AND blue >= {cb_min} AND blue <= {cb_max}"
        
        resultado1 = pd.read_sql(intermediaria, engine)
        resultado2 = pd.read_sql(complementar, engine)

        if resultado1.empty and resultado2.empty:
            complemento1 = False
            complemento2 = False
        elif resultado1.empty:
            complemento1 = False
        elif resultado2.empty:
            complemento2 = False
        else:
            print(" ")
        resultado1 = resultado1.to_dict(orient="records")
        resultado2 = resultado2.to_dict(orient="records")
        c = 0
        x = 0
        menor_distancia_1 = 0
        menor_distancia_2 = 0

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

        while x < len(resultado2):
            atual_red = resultado2[x]["red"] - cr
            atual_green = resultado2[x]["green"] - cg
            atual_blue = resultado2[x]["blue"] - cb

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
        print(resultado1[menor_distancia_1], complemento1)
        print(resultado2[menor_distancia_2], complemento2)
        if complemento1 == True and complemento2 == True:
            lista_complementos.append(resultado1[menor_distancia_1])
            lista_complementos.append(resultado2[menor_distancia_2])
        elif complemento1 == False:
            lista_complementos.append(resultado2[menor_distancia_2])
        elif complemento2 == False:
            lista_complementos.append(resultado1[menor_distancia_1])
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
        if blue == menor_analoga and green == maior_analoga or blue == maior_analoga and green == menor_analoga:
            meio_analoga = red
        if red == maior_analoga and blue == menor_analoga or red == menor_analoga and blue == maior_analoga:
            meio_analoga = green
        if red == maior_analoga and green == menor_analoga or red == menor_analoga and green == maior_analoga:
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

        primeira = ""
        segunda = ""
        primeira_menor = ""
        segunda_menor = ""

        if maior_analoga == red:
            if fornecedores != "todos":
                primeira = f"SELECT * from {fornecedores} WHERE red >= {menor_valor_de_maior_analoga} AND red <= {maior_valor_de_maior_analoga} AND green >= {menor_valor_de_meio_analoga} AND green <= {maior_valor_de_meio_analoga} AND blue >= {menor_valor_de_menor_analoga} AND blue <={maior_valor_de_menor_analoga} "
                segunda = f"SELECT * from {fornecedores} WHERE red >= {menor_valor_de_maior_analoga} AND red <={maior_valor_de_maior_analoga} AND green >= {menor_valor_de_menor_analoga} AND green <= {maior_valor_de_menor_analoga} AND blue >= {menor_valor_de_meio_analoga} AND blue <= {maior_valor_de_meio_analoga} "
            else:
                primeira = f"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil WHERE red >= {menor_valor_de_maior_analoga} AND red <= {maior_valor_de_maior_analoga} AND green >= {menor_valor_de_meio_analoga} AND green <= {maior_valor_de_meio_analoga} AND blue >= {menor_valor_de_menor_analoga} AND blue <={maior_valor_de_menor_analoga} union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral WHERE red >= {menor_valor_de_maior_analoga} AND red <= {maior_valor_de_maior_analoga} AND green >= {menor_valor_de_meio_analoga} AND green <= {maior_valor_de_meio_analoga} AND blue >= {menor_valor_de_menor_analoga} AND blue <={maior_valor_de_menor_analoga}"
                
                segunda = f"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil WHERE red >= {menor_valor_de_maior_analoga} AND red <={maior_valor_de_maior_analoga} AND green >= {menor_valor_de_menor_analoga} AND green <= {maior_valor_de_menor_analoga} AND blue >= {menor_valor_de_meio_analoga} AND blue <= {maior_valor_de_meio_analoga} union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral WHERE red >= {menor_valor_de_maior_analoga} AND red <={maior_valor_de_maior_analoga} AND green >= {menor_valor_de_menor_analoga} AND green <= {maior_valor_de_menor_analoga} AND blue >= {menor_valor_de_meio_analoga} AND blue <= {maior_valor_de_meio_analoga} "

        if maior_analoga == green:
            if fornecedores != "todos":
                primeira = f"SELECT * from {fornecedores} WHERE red >={menor_valor_de_meio_analoga} AND red <={maior_valor_de_meio_analoga} AND green >= {menor_valor_de_maior_analoga} AND green <= {maior_valor_de_maior_analoga} AND blue >= {menor_valor_de_menor_analoga} AND blue <= {maior_valor_de_menor_analoga} "
                segunda = f"SELECT * from {fornecedores} WHERE red >={menor_valor_de_menor_analoga} AND red <={maior_valor_de_menor_analoga} AND green >= {menor_valor_de_maior_analoga} AND green <= {maior_valor_de_maior_analoga} AND blue >= {menor_valor_de_meio_analoga} AND blue <= {maior_valor_de_meio_analoga} "
            else:
                primeira = f"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil WHERE red >={menor_valor_de_meio_analoga} AND red <={maior_valor_de_meio_analoga} AND green >= {menor_valor_de_maior_analoga} AND green <= {maior_valor_de_maior_analoga} AND blue >= {menor_valor_de_menor_analoga} AND blue <= {maior_valor_de_menor_analoga} union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral WHERE red >={menor_valor_de_meio_analoga} AND red <={maior_valor_de_meio_analoga} AND green >= {menor_valor_de_maior_analoga} AND green <= {maior_valor_de_maior_analoga} AND blue >= {menor_valor_de_menor_analoga} AND blue <= {maior_valor_de_menor_analoga}"
                segunda = f"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil WHERE red >={menor_valor_de_menor_analoga} AND red <={maior_valor_de_menor_analoga} AND green >= {menor_valor_de_maior_analoga} AND green <= {maior_valor_de_maior_analoga} AND blue >= {menor_valor_de_meio_analoga} AND blue <= {maior_valor_de_meio_analoga} union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral WHERE red >={menor_valor_de_menor_analoga} AND red <={maior_valor_de_menor_analoga} AND green >= {menor_valor_de_maior_analoga} AND green <= {maior_valor_de_maior_analoga} AND blue >= {menor_valor_de_meio_analoga} AND blue <= {maior_valor_de_meio_analoga} "

        if maior_analoga == blue:
            if fornecedores != "todos":
                primeira = f"SELECT * from {fornecedores} WHERE red >= {menor_valor_de_menor_analoga} AND red <= {maior_valor_de_menor_analoga} AND green >= {menor_valor_de_meio_analoga} AND green <= {maior_valor_de_meio_analoga} AND blue >= {menor_valor_de_maior_analoga} AND blue <={maior_valor_de_maior_analoga} "
                segunda = f"SELECT * from {fornecedores} WHERE red >= {menor_valor_de_meio_analoga} AND red <= {maior_valor_de_meio_analoga} AND green >= {menor_valor_de_menor_analoga} AND green <= {maior_valor_de_menor_analoga} AND blue >= {menor_valor_de_maior_analoga} AND blue <={maior_valor_de_maior_analoga} "
            else:
                primeira = f"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil WHERE red >= {menor_valor_de_menor_analoga} AND red <= {maior_valor_de_menor_analoga}  AND green >= {menor_valor_de_meio_analoga} AND green <= {maior_valor_de_meio_analoga} AND blue >= {menor_valor_de_maior_analoga} AND blue <={maior_valor_de_maior_analoga} union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral WHERE red >= {menor_valor_de_menor_analoga} AND red <= {maior_valor_de_menor_analoga} AND green >= {menor_valor_de_meio_analoga} AND green <= {maior_valor_de_meio_analoga} AND blue >= {menor_valor_de_maior_analoga} AND blue <={maior_valor_de_maior_analoga} "
                segunda = f"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil WHERE red >= {menor_valor_de_meio_analoga} AND red <= {maior_valor_de_meio_analoga} AND green >= {menor_valor_de_menor_analoga} AND green <= {maior_valor_de_menor_analoga} AND blue >= {menor_valor_de_maior_analoga} AND blue <={maior_valor_de_maior_analoga} union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral WHERE red >= {menor_valor_de_meio_analoga} AND red <= {maior_valor_de_meio_analoga} AND green >= {menor_valor_de_menor_analoga} AND green <= {maior_valor_de_menor_analoga} AND blue >= {menor_valor_de_maior_analoga} AND blue <={maior_valor_de_maior_analoga}"
        
        if maior_analoga == red:
            primeira_menor = "blue"
            segunda_menor = "green"
        if maior_analoga == green:
            primeira_menor = "blue"
            segunda_menor = "red"
        if maior_analoga == blue:
            primeira_menor = "red"
            segunda_menor = "green"
            
        
        resultado1 = pd.read_sql(primeira, engine)
        resultado2 = pd.read_sql(segunda, engine)
        if resultado1.empty and resultado2.empty:
            complemento1 = False
            complemento2 = False
        elif resultado1.empty:
            complemento1 = False
        elif resultado2.empty:
            complemento2 = False
        resultado1 = resultado1.to_dict(orient="records")
        resultado2 = resultado2.to_dict(orient="records")

        c = 0
        x = 0
        menor_distancia_1 = 0
        menor_distancia_2 = 0

        while c < len(resultado1):
            atual_red = resultado1[c]["red"] - red
            atual_green = resultado1[c]["green"] - green
            atual_blue = resultado1[c]["blue"] - blue

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
                        if atual_red < atual_blue and atual_red < atual_green:
                            menor_distancia_1 = c
                            distancia = distancia_atual
                    if primeira_menor == "green":
                        if atual_green < atual_blue and atual_green < atual_red:
                            menor_distancia_1 = c
                            distancia = distancia_atual
                    if primeira_menor == "blue":
                        if atual_blue < atual_green and atual_blue < atual_red:
                            menor_distancia_1 = c
                            distancia = distancia_atual
            c += 1

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
                        if atual_red < atual_blue and atual_red < atual_green:
                            menor_distancia_2 = x
                            distancia = distancia_atual
                    if segunda_menor == "green":
                        if atual_green < atual_blue and atual_green < atual_red:
                            menor_distancia_2 = x
                            distancia = distancia_atual
                    if segunda_menor == "blue":
                        if atual_blue < atual_green and atual_blue < atual_red:
                            menor_distancia_2 = x
                            distancia = distancia_atual
            x += 1

        if complemento1 == True and complemento2 == True:
            lista_complementos.append(resultado1[menor_distancia_1])
            lista_complementos.append(resultado2[menor_distancia_2])
        elif complemento1 == False:
            lista_complementos.append(resultado2[menor_distancia_2])
        elif complemento2 == False:
            lista_complementos.append(resultado1[menor_distancia_1])
        elif complemento1 == False and complemento2 == False:
            return []
        return lista_complementos
    else:
        err = "Complemento indisponível"
        print(err)
        return err