import os, json
import pandas as pd
import sqlalchemy
from flask import Flask, request

DATABASE_URL = os.getenv("DATABASE_URL")
engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
lista_complementos = []


def select_complementos(red, green, blue, palheta):
    if palheta == "triade":
        lista_complementos.clear()
        desvio_maior = 60
        desvio_menor = 10
        maior = max(red, green, blue)
        menor = min(red, green, blue)
        meio = 0
        complemento1 = True
        complemento2 = True
        if red != maior and red != menor :
            meio = red
        if green != maior and green != menor:
            meio = green
        if blue != maior and blue != menor:
            meio = blue

        menor_valor_do_meio = meio - desvio_maior
        maior_valor_do_meio = meio + desvio_maior
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
        if maior_valor_do_meio < 0:
            maior_valor_do_meio = 0
        if menor_valor_do_meio > 255:
            menor_valor_do_meio = 255
        if maior == red:
            primeira = f"SELECT * FROM suvinil WHERE red >= {menor_valor_de_menor} AND red <= {maior_valor_de_menor} AND green >= {menor_valor_de_maior} AND green <= {maior_valor_de_maior} AND blue >= {menor_valor_do_meio} AND blue <={maior_valor_do_meio} "
            segunda = f"SELECT * FROM suvinil WHERE red >= {menor_valor_do_meio} AND red <={maior_valor_do_meio} AND green >= {menor_valor_de_menor} AND green <= {maior_valor_de_menor} AND blue >= {menor_valor_de_maior} AND blue <= {maior_valor_de_maior} "
            
        if maior == green:
            primeira = f"SELECT * FROM suvinil WHERE red >={menor_valor_do_meio} AND red <={maior_valor_do_meio} AND green >= {menor_valor_de_menor} AND green <= {maior_valor_de_menor} AND blue >= {menor_valor_de_maior} AND blue <= {maior_valor_de_maior} "
            segunda = f"SELECT * FROM suvinil WHERE red >= {menor_valor_de_maior} AND red <= {maior_valor_de_maior} AND green >= {menor_valor_do_meio} AND green <= {maior_valor_do_meio} AND blue >= {menor_valor_de_menor} AND blue <={maior_valor_de_menor} "
            
        if maior == blue:
            primeira = f"SELECT * FROM suvinil WHERE red >= {menor_valor_de_menor} AND red <= {maior_valor_de_menor} AND green >= {menor_valor_de_maior} AND green <= {maior_valor_de_maior} AND blue >= {menor_valor_do_meio} AND blue <={maior_valor_do_meio} "
            segunda = f"SELECT * FROM suvinil WHERE red >= {menor_valor_de_maior} AND red <={maior_valor_de_maior} AND green >= {menor_valor_do_meio} AND green <= {maior_valor_do_meio} AND blue >= {menor_valor_de_menor} AND blue <= {maior_valor_de_menor} "
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
            atual_red = (resultado1[c]['red'] - red)
            if atual_red < 0:
                atual_red = atual_red * -1
            atual_green = (resultado1[c]['green'] - green)
            if atual_green < 0:
                atual_green = atual_green * -1
            atual_blue = (resultado1[c]['blue'] - blue)
            if atual_blue < 0:
                atual_blue = atual_blue * -1
            distancia_atual =  atual_red + atual_green + atual_blue
            if c == 0 or distancia_atual < distancia:
                menor_distancia_1 = c
                distancia = distancia_atual

        while x < len(resultado2):
            atual_red = (resultado2[x]['red'] - red)
            if atual_red < 0:
                atual_red = atual_red * -1
            atual_green = (resultado2[x]['green'] - green)
            if atual_green < 0:
                atual_green = atual_green * -1
            atual_blue = (resultado2[x]['blue'] - blue)
            if atual_blue < 0:
                atual_blue = atual_blue * -1
            distancia_atual =  atual_red + atual_green + atual_blue
            if c == 0 or distancia_atual < distancia:
                menor_distancia_2 = x
                distancia = distancia_atual
                
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
        if palheta == "complementar":
            desvio_complementar = 30
            cr = 255 - red
            cg = 255 - green
            cb = 255 - blue
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
            cr_inter= (cr + red)/2
            cg_inter = (cg + green)/2
            cb_inter = (cb + blue)/2
            cr_inter_max = cr_inter + desvio_complementar
            cr_inter_min = cr_inter - desvio_complementar
            cg_inter_max = cg_inter + desvio_complementar
            cg_inter_min = cg_inter - desvio_complementar
            cb_inter_max = cb_inter + desvio_complementar
            cb_inter_min = cb_inter - desvio_complementar

            
                
            intermediaria = f"SELECT * FROM suvinil WHERE red >= {cr_inter_min} AND red <= {cr_inter_max} AND green >= {cg_inter_min} AND green <= {cg_inter_max} AND blue >= {cb_inter_min} AND blue <= {cb_inter_max} "
            complementar = f"SELECT * FROM suvinil WHERE red >= {cr_min} AND red <= {cr_max} AND green >= {cg_min} AND green <= {cg_max} AND blue >= {cb_min} AND blue <= {cb_max} "
            resultado1 = pd.read_sql(intermediaria, engine)
            resultado2 = pd.read_sql(complementar, engine)

            resultado1 = resultado1.to_dict(orient="records")
            resultado2 = resultado2.to_dict(orient="records")
            c = 0
            x = 0
            menor_distancia_1 = 0
            menor_distancia_2 = 0
            
            while c < len(resultado1):
                atual_red = (resultado1[c]['red'] - cr_inter)
                if atual_red < 0:
                    atual_red = atual_red * -1
                atual_green = (resultado1[c]['green'] - cg_inter)
                if atual_green < 0:
                    atual_green = atual_green * -1
                atual_blue = (resultado1[c]['blue'] - cb_inter)
                if atual_blue < 0:
                    atual_blue = atual_blue * -1
                distancia_atual =  atual_red + atual_green + atual_blue
                if c == 0 or distancia_atual < distancia:
                    menor_distancia_1 = c
                    distancia = distancia_atual

            while x < len(resultado2):
                atual_red = (resultado2[x]['red'] - cr)
                if atual_red < 0:
                    atual_red = atual_red * -1
                atual_green = (resultado2[x]['green'] - cg)
                if atual_green < 0:
                    atual_green = atual_green * -1
                atual_blue = (resultado2[x]['blue'] - cb)
                if atual_blue < 0:
                    atual_blue = atual_blue * -1
                distancia_atual =  atual_red + atual_green + atual_blue
                if c == 0 or distancia_atual < distancia:
                    menor_distancia_2 = x
                    distancia = distancia_atual
                    
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
            
        if palheta == "análoga":
            lista_complementos.clear()
            desvio_maior = 30
            desvio_menor = 10
            maior = max(red, green, blue)
            menor = min(red, green, blue)
            meio = 0
            if red != maior and red != menor :
                meio = red
            if green != maior and green != menor:
                meio = green
            if blue != maior and blue != menor:
                meio = blue
            meio += 60
            menor_valor_de_meio = meio - desvio_maior
            maior_valor_de_meio = meio + desvio_maior
            menor_valor_de_maior = maior - desvio_menor
            maior_valor_de_maior = maior + desvio_menor
            menor_valor_de_menor = menor - desvio_menor
            maior_valor_de_menor = menor + desvio_menor


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
            
            if maior == red:
                primeira = f"SELECT * FROM suvinil WHERE red >= {menor_valor_de_maior} AND red <= {maior_valor_de_maior} AND green >= {menor_valor_de_meio} AND green <= {maior_valor_de_meio} AND blue >= {menor_valor_do_menor} AND blue <={maior_valor_do_menor} "
                segunda = f"SELECT * FROM suvinil WHERE red >= {menor_valor_do_maior} AND red <={maior_valor_do_maior} AND green >= {menor_valor_de_menor} AND green <= {maior_valor_de_menor} AND blue >= {menor_valor_de_meio} AND blue <= {maior_valor_de_meio} "
                
            if maior == green:
                primeira = f"SELECT * FROM suvinil WHERE red >={menor_valor_do_meio} AND red <={maior_valor_do_meio} AND green >= {menor_valor_de_maior} AND green <= {maior_valor_de_maior} AND blue >= {menor_valor_de_menor} AND blue <= {maior_valor_de_menor} "
                segunda = f"SELECT * FROM suvinil WHERE red >={menor_valor_do_menor} AND red <={maior_valor_do_menor} AND green >= {menor_valor_de_maior} AND green <= {maior_valor_de_maior} AND blue >= {menor_valor_de_meio} AND blue <= {maior_valor_de_meio} " 
               
            if maior == blue:
                primeira = f"SELECT * FROM suvinil WHERE red >= {menor_valor_de_menor} AND red <= {maior_valor_de_menor} AND green >= {menor_valor_de_meio} AND green <= {maior_valor_de_meio} AND blue >= {menor_valor_do_maior} AND blue <={maior_valor_do_maior} "
                segunda = f"SELECT * FROM suvinil WHERE red >= {menor_valor_de_meio} AND red <= {maior_valor_de_meio} AND green >= {menor_valor_de_menor} AND green <= {maior_valor_de_menor} AND blue >= {menor_valor_do_maior} AND blue <={maior_valor_do_maior} "
                
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
            atual_red = (resultado1[c]['red'] - red)
            if atual_red < 0:
                atual_red = atual_red * -1
            atual_green = (resultado1[c]['green'] - green)
            if atual_green < 0:
                atual_green = atual_green * -1
            atual_blue = (resultado1[c]['blue'] - blue)
            if atual_blue < 0:
                atual_blue = atual_blue * -1
            distancia_atual =  atual_red + atual_green + atual_blue
            if c == 0 or distancia_atual < distancia:
                menor_distancia_1 = c
                distancia = distancia_atual

        while x < len(resultado2):
            atual_red = (resultado2[x]['red'] - red)
            if atual_red < 0:
                atual_red = atual_red * -1
            atual_green = (resultado2[x]['green'] - green)
            if atual_green < 0:
                atual_green = atual_green * -1
            atual_blue = (resultado2[x]['blue'] - blue)
            if atual_blue < 0:
                atual_blue = atual_blue * -1
            distancia_atual =  atual_red + atual_green + atual_blue
            if c == 0 or distancia_atual < distancia:
                menor_distancia_2 = x
                distancia = distancia_atual
                
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
            
def select_hexadecimal(hexadecimal):
    search_string = f"SELECT * FROM suvinil WHERE hexadecimal = '{hexadecimal}' or pantone_hex = '{hexadecimal}' "
    resultset = pd.read_sql(search_string, engine)
    if resultset.empty:
        search_string = f"SELECT * FROM suvinil where hexadecimal like ':hexadecimal' or pantone_hex like ':hexadecimal' "
        resultset = pd.read_sql(
            search_string, engine, params={"hexadecimal": hexadecimal}
        )
    return resultset


def select_códigos(codigo):
    search_string = f"SELECT * FROM suvinil WHERE pantone_código = '{codigo}'"
    resultset = pd.read_sql(search_string, engine)
    if resultset.empty:
        search_string = f"SELECT * FROM suvinil where pantone_código like ':codigo'"
        resultset = pd.read_sql(search_string, engine, params={"codigo": codigo})
    return resultset


def select_names(nome):
    search_string = (
        f"SELECT * FROM suvinil WHERE nome = '{nome}' or pantone_name = '{nome}' "
    )
    resultset = pd.read_sql(search_string, engine)
    if resultset.empty:
        search_string = f"SELECT * FROM suvinil where nome like ':nome' or pantone_name like ':nome' "
        resultset = pd.read_sql(search_string, engine, params={"nome": nome})
    return resultset

def search_name_for_id(nome):
    with open ("search/search_dict.json", "r") as file:
        search_dict = json.load(file)
        print (search_dict)
        if nome in search_dict:
             return search_dict[nome]
        else:
            return None

def primary_select(red, green, blue):
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
    search_string = f"SELECT * FROM suvinil WHERE red >= {minred} AND  red <= {maxred} AND green >= {mingreen} AND green <= {maxgreen} AND blue >= {minblue} AND blue <= {maxblue} "
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


@app.route("/suvinil/<int:red>/<int:green>/<int:blue>", methods=["GET", "POST"])
def getsuvinilColors():
    if request.method == "POST":
        rgb = request.get_json()
        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]
        temp = primary_select(red, green, blue)
        response = temp.to_dict(orient="records")
        c = 0
        while c < len(response):
            lastQuery.append(response[c])
            c += 1
        with open("response.json", "w+") as file:
            json.dump(lastQuery, file)
            lastQuery.clear()
        return response
    if request.method == "GET":
        with open("response.json", "r") as file:
            response = json.load(file)
            return response


@app.route("/names/<string:nome>", methods=["POST"])
def getNames():
    if request.method == "POST":
        nomecor = request.get_json()
        nome = nomecor["nome"]
        response = select_names(nome)
        response = response.to_dict(orient="records")
        with open("response.json", "w+") as file:
            json.dump(response, file)
        return response


@app.route("/codigos/<string:codigo>", methods=["POST"])
def getProcura():
    if request.method == "POST":
        codigo_cor = request.get_json()
        codigo = codigo_cor["codigo"]
        response = select_códigos(codigo)
        response = response.to_dict(orient="records")
        with open("response.json", "w+") as file:
            json.dump(response, file)
        return response


@app.route("/hex/<string:hexadecimal>", methods=["POST"])
def getHex():
    if request.method == "POST":
        codigo_cor = request.get_json()
        hexadecimal = codigo_cor["headecimal"]
        response = select_hexadecimal(hexadecimal)
        response = response.to_dict(orient="records")
        with open("response.json", "w+") as file:
            json.dump(response, file)
        return response


@app.route("/complementos/<int:red>/<int:green>/<int:blue>/<string:palheta>", methods=["POST","GET"])
def getComplementos():
    if request.method == "POST":
        complementos = request.get_json()
        red = complementos["red"]
        green = complementos["green"]
        blue = complementos["blue"]
        palheta = complementos["palheta"]
        lista = select_complementos(red, green, blue, palheta)
        c = 0
        while c < len(lista):
            lastQuery.append(lista[c])
            c += 1
        with open("complementos.json", "w+") as file:
            json.dump(lastQuery, file)
            lastQuery.clear()
        return lastQuery
    if request.method == "GET":
        with open("complementos.json", "r") as file:
            response = json.load(file)
            return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)
