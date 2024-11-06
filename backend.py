import os, json
import pandas as pd
import sqlalchemy
from flask import Flask, request

DATABASE_URL = os.getenv("DATABASE_URL")
engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
lista_complementos = []


def generate_pandas_table(segundo_query, primeiro_query):
    lista_pandas = []

    def getting_data():
        queries = {
            "suvinil": primeiro_query,
            "coral": segundo_query,
        }
        dataframes = {}

        def convert_to_float(value):
            value = str(value).replace(",", "")  # Substituir vírgula por ponto
            try:
                return float(value)
            except ValueError:
                return None

        for table_name, query in queries.items():
            try:
                df = pd.read_sql(query, engine)
                if table_name in ["suvinil", "coral"]:
                    df["fornecedores"] = df["fornecedores"].astype(str)
                    df["hexadecimal"] = df["hexadecimal"].astype(str)
                    df["nome"] = df["nome"].astype(str)
                    df["pantone_código"] = df["pantone_código"].astype(str)
                    df["red"] = df["red"].astype(int)
                    df["green"] = df["green"].astype(int)
                    df["blue"] = df["blue"].astype(int)
                dataframes[table_name] = df
            except Exception as e:
                print(f"Erro ao processar a tabela {table_name}: {e}")
            return dataframes

    table = getting_data()
    # print(table)


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
                primeira = f"SELECT * from {fornecedores} WHERE red >= {menor_valor_de_menor} AND red <= {maior_valor_de_menor} AND green >= {menor_valor_de_maior} AND green <= {maior_valor_de_maior} AND blue >= {menor_valor_de_meio} AND blue <={maior_valor_de_meio} "
                segunda = f"SELECT * from {fornecedores} WHERE red >= {menor_valor_de_maior} AND red <={maior_valor_de_maior} AND green >= {menor_valor_de_meio} AND green <= {maior_valor_de_meio} AND blue >= {menor_valor_de_menor} AND blue <= {maior_valor_de_menor} "
            else:
                primeira = f"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil WHERE red >= {menor_valor_de_menor} AND red <= {maior_valor_de_menor} AND green >= {menor_valor_de_maior} AND green <= {maior_valor_de_maior} AND blue >= {menor_valor_de_meio} AND blue <={maior_valor_de_meio} union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral WHERE red >= {menor_valor_de_menor} AND red <= {maior_valor_de_menor} AND green >= {menor_valor_de_maior} AND green <= {maior_valor_de_maior} AND blue >= {menor_valor_de_meio} AND blue <={maior_valor_de_meio}"

                segunda = f"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil WHERE red >= {menor_valor_de_maior} AND red <={maior_valor_de_maior} AND green >= {menor_valor_de_meio} AND green <= {maior_valor_de_meio} AND blue >= {menor_valor_de_menor} AND blue <= {maior_valor_de_menor} union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral WHERE red >= {menor_valor_de_maior} AND red <={maior_valor_de_maior} AND green >= {menor_valor_de_meio} AND green <= {maior_valor_de_meio} AND blue >= {menor_valor_de_menor} AND blue <= {maior_valor_de_menor} "

        resultado1 = pd.read_sql(primeira, engine)
        resultado2 = pd.read_sql(segunda, engine)

        generate_pandas_table(primeira, segunda)

        
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
                    menor_distancia_2 = x
                    distancia = distancia_atual
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


def select_hexadecimal(hexadecimal, fornecedores):
    seach_string = ""

    if fornecedores != "todos":
        search_string = f"SELECT * from {fornecedores} WHERE hexadecimal = '{hexadecimal}' or pantone_hex = '{hexadecimal}' "
    else:
        search_string = f"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil WHERE hexadecimal = '{hexadecimal}' or pantone_hex = '{hexadecimal}' union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral WHERE hexadecimal = '{hexadecimal}' or pantone_hex = '{hexadecimal}' "

    resultset = pd.read_sql(search_string, engine)
    return resultset


def select_códigos(codigo, fornecedores):
    seach_string = ""
    if fornecedores != "todos":
        search_string = (
            f"SELECT * from {fornecedores} WHERE pantone_código = '{codigo}'"
        )
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
