import os, json
import pandas as pd
import sqlalchemy
import streamlit as st
from flask import Flask, request
from utils.select_complementos import select_complementos
from utils.conect_to_engine import conect_to_engine
from utils.create_pandas_table import generate_pandas_table


engine = conect_to_engine()


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


@app.route("/colors/", methods=["GET", "POST"])
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


@app.route("/complementos/", methods=["POST", "GET"])
def getComplementos():
    if request.method == "POST":
        complementos = request.get_json()
        print(complementos)
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
