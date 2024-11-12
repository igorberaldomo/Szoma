
import os
import json
import pandas as pd
import sqlalchemy
import streamlit as st
from utils.select_complementos import select_complementos
from utils.conect_to_engine_developer import conect_to_engine_developer
from utils.create_pandas_table import generate_pandas_table
from utils.search.search_hexadecimal import select_hexadecimal
from utils.search.search_codigos import select_códigos
from utils.search.search_id import select_id
from utils.search.search_name_for_id import search_name_for_id
from utils.search.primary_select import primary_select

# Inicializa a conexão com o banco de dados
engine = conect_to_engine_developer()

def get_colors(cor, fornecedores):
    """
    Encontra cores baseadas em valores RGB.

    Parâmetros:
    - cor: lista ou tupla contendo (red, green, blue)
    - fornecedores: string indicando o fornecedor ou categoria

    Retorna:
    - response: lista de dicionários com informações das cores
    """
    red, green, blue = cor
    response_df = primary_select(red, green, blue, fornecedores)
    response = response_df.to_dict(orient="records")
    return response

def get_names(nome, fornecedores):
    """
    Encontra cores baseadas no nome.

    Parâmetros:
    - nome: string com o nome da cor
    - fornecedores: string indicando o fornecedor ou categoria

    Retorna:
    - response: lista de dicionários com informações das cores
    """
    request_id = search_name_for_id(nome)
    if request_id is None:
        return []
    response_df = select_id(request_id, nome, fornecedores)
    response = response_df.to_dict(orient="records")
    return response

def get_codigos(codigo, fornecedores):
    """
    Encontra cores baseadas no código Pantone.

    Parâmetros:
    - codigo: string com o código Pantone
    - fornecedores: string indicando o fornecedor ou categoria

    Retorna:
    - response: lista de dicionários com informações das cores
    """
    response_df = select_códigos(codigo, fornecedores)
    response = response_df.to_dict(orient="records")
    return response

def get_hex(hexadecimal, fornecedores):
    """
    Encontra cores baseadas no código hexadecimal.

    Parâmetros:
    - hexadecimal: string com o código hexadecimal (por exemplo, '#FF5733')
    - fornecedores: string indicando o fornecedor ou categoria

    Retorna:
    - response: lista de dicionários com informações das cores
    """
    response_df = select_hexadecimal(hexadecimal, fornecedores)
    response = response_df.to_dict(orient="records")
    return response

def get_complementos(red, green, blue, palheta, fornecedores):
    """
    Encontra cores complementares baseadas em valores RGB e tipo de paleta.

    Parâmetros:
    - red: inteiro (0-255)
    - green: inteiro (0-255)
    - blue: inteiro (0-255)
    - palheta: string indicando o tipo de paleta ('triade', 'complementar', 'análoga')
    - fornecedores: string indicando o fornecedor ou categoria

    Retorna:
    - response: lista de dicionários com informações das cores complementares
    """
    response_df = select_complementos(red, green, blue, palheta, fornecedores)
    response = response_df.to_dict(orient="records")
    return response

# Exemplo de uso das funções:

if __name__ == "__backend__":
    # Exemplo para encontrar cores por RGB
    cor_rgb = (255, 0, 0)  # Vermelho
    fornecedores = 'todos'
    cores_encontradas = get_colors(cor_rgb, fornecedores)
    print("Cores encontradas por RGB:")
    print(cores_encontradas)

    # Exemplo para encontrar cores por nome
    nome_cor = 'Azul'
    cores_por_nome = get_names(nome_cor, fornecedores)
    print("\nCores encontradas por nome:")
    print(cores_por_nome)

    # Exemplo para encontrar cores por código Pantone
    codigo_pantone = '19-4052'
    cores_por_codigo = get_codigos(codigo_pantone, fornecedores)
    print("\nCores encontradas por código Pantone:")
    print(cores_por_codigo)

    # Exemplo para encontrar cores por hexadecimal
    hexadecimal = '#FFFFFF'
    cores_por_hex = get_hex(hexadecimal, fornecedores)
    print("\nCores encontradas por hexadecimal:")
    print(cores_por_hex)

    # Exemplo para encontrar cores complementares
    red, green, blue = 255, 0, 0  # Vermelho
    palheta = 'complementar'
    cores_complementares = get_complementos(red, green, blue, palheta, fornecedores)
    print("\nCores complementares encontradas:")
    print(cores_complementares)

