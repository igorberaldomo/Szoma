import os, json
import pandas as pd
import sqlalchemy
import streamlit as st
from flask import Flask, request
from utils.select_complementos import select_complementos
from utils.conect_to_engine_developer import conect_to_engine_developer
from utils.conect_to_engine_production import conect_to_engine_production
from utils.create_pandas_table import generate_pandas_table
from utils.search.search_hexadecimal import select_hexadecimal
from utils.search.search_codigos import select_códigos
from utils.search.search_id import select_id
from utils.search.search_name_for_id import search_name_for_id
from utils.search.primary_select import primary_select


engine = conect_to_engine_developer()


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
