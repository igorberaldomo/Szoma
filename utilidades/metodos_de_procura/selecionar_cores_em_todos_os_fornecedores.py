import streamlit as st

def selecionar_cores_em_todos_os_fornecedores(red, green,blue,tabela):
    lista_cores_final = []
    desvio = 5
    tem_resultados = False
    minimo_vermelho = red - desvio
    maximo_vermelho = red + desvio
    minimo_verde = green - desvio
    maximo_verde = green + desvio
    minimo_azul = blue - desvio
    maximo_azul = blue + desvio

    if minimo_vermelho < 0:
        minimo_vermelho = 0
    if maximo_vermelho > 255:
        maximo_vermelho = 255
    if minimo_verde < 0:
        minimo_verde = 0
    if maximo_verde > 255:
        maximo_verde = 255
    if minimo_azul < 0:
        minimo_azul = 0
    if maximo_azul > 255:
        maximo_azul = 255
    
    resultados = list()
    suvinil = tabela["suvinil"]
    # busca na tabela suvinil
    for index,row in suvinil.iterrows():
        if row['red'] >= minimo_vermelho and row['red'] <= maximo_vermelho and row['green'] >= minimo_verde and row['green'] <= maximo_verde and row['blue'] >= minimo_azul and row['blue'] <= maximo_azul: 
            resultados.append({"nome": row['nome'],"hexadecimal":row['hexadecimal'],"fornecedores":row['fornecedores'], "red":row["red"], "green":row["green"], "blue":row["blue"]})
            
    # busca na tabela coral
    coral = tabela["coral"]
    for index,row in coral.iterrows():
        if row['red'] >= minimo_vermelho and row['red'] <= maximo_vermelho and row['green'] >= minimo_verde and row['green'] <= maximo_verde and row['blue'] >= minimo_azul and row['blue'] <= maximo_azul:
            resultados.append({"nome": row['nome'],"hexadecimal":row['hexadecimal'],"fornecedores":row['fornecedores'], "red":row["red"], "green":row["green"], "blue":row["blue"]})

     # busca na tabela anjo

    anjo = tabela["anjo"]
    for index,row in anjo.iterrows():
        if row['red'] >= minimo_vermelho and row['red'] <= maximo_vermelho and row['green'] >= minimo_verde and row['green'] <= maximo_verde and row['blue'] >= minimo_azul and row['blue'] <= maximo_azul:
            resultados.append({"nome": row['nome'],"hexadecimal":row['hexadecimal'],"fornecedores":row['fornecedores'], "red":row["red"], "green":row["green"], "blue":row["blue"]})
    # busca na tabela sherwin-willians
    sherwin_willians = tabela["sherwin-willians"]
    for index,row in sherwin_willians.iterrows():
        if row['red'] >= minimo_vermelho and row['red'] <= maximo_vermelho and row['green'] >= minimo_verde and row['green'] <= maximo_verde and row['blue'] >= minimo_azul and row['blue'] <= maximo_azul: 
            resultados.append({"nome": row['nome'],"hexadecimal":row['hexadecimal'],"fornecedores":row['fornecedores'], "red":row["red"], "green":row["green"], "blue":row["blue"]})   
    if len(resultados) == 0:
        tem_resultados = False
    else:
        tem_resultados = True
    
    c = 0
    for c in range(len(resultados)):
        lista_cores_final.append(resultados)
        c += 1
    return lista_cores_final