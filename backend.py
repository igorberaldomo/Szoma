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
        maior = max(red, green, blue)
        menor = min(red, green, blue)
        if red != maior and red != menor :
            meio = red
        if green != maior and green != menor:
            meio = green
        if blue != maior and blue != menor:
            meio = blue

        menor_valor_do_meio = meio - 60
        maior_valor_do_meio = meio + 60
        menor_valor_de_menor = menor - 30
        maior_valor_de_menor = menor + 20
        menor_valor_de_maior = maior - 20
        maior_valor_de_maior = maior + 20

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
            resultado1 = pd.read_sql(primeira, engine)
            resultado2 = pd.read_sql(segunda, engine)
            print(resultado1, resultado2)
            lista_complementos.append(resultado1)
            lista_complementos.append(resultado2)
            return lista_complementos
        if maior == green:
            print('green')
            primeira = f"SELECT * FROM suvinil WHERE red >={menor_valor_do_meio} AND red <={maior_valor_do_meio} AND green >= {menor_valor_de_menor} AND green <= {maior_valor_de_menor} AND blue >= {menor_valor_de_maior} AND blue <= {maior_valor_de_maior} "
            segunda = f"SELECT * FROM suvinil WHERE red >= {menor_valor_de_maior} AND red <= {maior_valor_de_maior} AND green >= {menor_valor_do_meio} AND green <= {maior_valor_do_meio} AND blue >= {menor_valor_de_menor} AND blue <={maior_valor_de_menor} "
            resultado1 = pd.read_sql(primeira, engine)
            resultado2 = pd.read_sql(segunda, engine)
            lista_complementos.append(resultado1)
            lista_complementos.append(resultado2)
            return lista_complementos
        if maior == blue:
            print('blue')
            primeira = f"SELECT * FROM suvinil WHERE red >= {menor_valor_de_menor} AND red <= {maior_valor_de_menor} AND green >= {menor_valor_de_maior} AND green <= {maior_valor_de_maior} AND blue >= {menor_valor_do_meio} AND blue <={maior_valor_do_meio} "
            segunda = f"SELECT * FROM suvinil WHERE red >= {menor_valor_de_maior} AND red <={maior_valor_de_maior} AND green >= {menor_valor_do_meio} AND green <= {maior_valor_do_meio} AND blue >= {menor_valor_de_menor} AND blue <= {maior_valor_de_menor} "
            resultado1 = pd.read_sql(primeira, engine)
            resultado2 = pd.read_sql(segunda, engine)
            lista_complementos.append(resultado1)
            lista_complementos.append(resultado2)
            return lista_complementos
        #  ainda falta aqui palheta complementar e análoga

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

    return resultset


app = Flask(__name__)
lastQuery = list()


@app.route("/", methods=["GET"])
def infopage():
    return "<h1>Colors API</h1><p>This api will request a picture or RGB, and will return a product (paint, tiles, fabrics) </p> "


@app.route("/suvinil/", methods=["GET", "POST"])
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


@app.route("/names/", methods=["POST"])
def getNames():
    if request.method == "POST":
        nomecor = request.get_json()
        nome = nomecor["nome"]
        response = select_names(nome)
        response = response.to_dict(orient="records")
        with open("response.json", "w+") as file:
            json.dump(response, file)
        return response


@app.route("/codigos/", methods=["POST"])
def getProcura():
    if request.method == "POST":
        codigo_cor = request.get_json()
        codigo = codigo_cor["codigo"]
        response = select_códigos(codigo)
        response = response.to_dict(orient="records")
        with open("response.json", "w+") as file:
            json.dump(response, file)
        return response


@app.route("/hex/", methods=["POST"])
def getHex():
    if request.method == "POST":
        codigo_cor = request.get_json()
        hexadecimal = codigo_cor["headecimal"]
        response = select_hexadecimal(hexadecimal)
        response = response.to_dict(orient="records")
        with open("response.json", "w+") as file:
            json.dump(response, file)
        return response


@app.route("/complementos/", methods=["POST"])
def getComplementos():
    if request.method == "POST":
        complementos = request.get_json()
        red = complementos["red"]
        green = complementos["green"]
        blue = complementos["blue"]
        palheta = complementos["palheta"]
        lista = select_complementos(red, green, blue, palheta)
        print(lista)
        with open("complementos.json", "w+") as file:
            json.dump(lastQuery, file)
            lastQuery.clear()
        return lastQuery



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)
