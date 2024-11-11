import colorthief
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import numpy as np
import pandas as pd
import requests
import json
import time
from utils.rgb_to_cmyk import rgb_to_cmyk

if "count" not in st.session_state:
    st.session_state.count = '0'
                
st.markdown("""
<style>
.st-emotion-cache-yfhhig.ef3psqc5{
visibility:hidden
}

</style>
""", unsafe_allow_html=True)
query = True

def findrgb():
    if  procura is not None or upload is not None:
        if upload is not None:
            st.session_state.cliked = True
            ct = colorthief.ColorThief(upload)
            cor = ct.get_color(quality=1)
            json_procura = {'cor': cor,'fornecedores':opcao_fornecedores}
            response = requests.post("https://findme-backend.streamlit.app:5555/colors/",json=json_procura)
        elif procura != '':
            if procura[0].isalpha():
                st.session_state.cliked = True
                nome = {"nome":procura, "fornecedores":opcao_fornecedores}
                response = requests.post("https://findme-backend.streamlit.app:5555/names/",json=nome)
            elif procura[0].isnumeric():
                codigo = {"codigo":procura, "fornecedores":opcao_fornecedores}
                response = requests.post("https://findme-backend.streamlit.app:5555/codigos/",json=codigo)
            elif procura[0] == '#':
                hexa = {"hexadecimal":procura, "fornecedores":opcao_fornecedores}
                response = requests.post("https://findme-backend.streamlit.app:5555/hex/",json=hexa)
            return response
    else:
        st.text('Por favor coloque uma imagem para verificar a cor')

     
def receivecolors():
    response = requests.get("https://findme-backend.streamlit.app:5555/colors/",headers={'Content-Type': 'application/json',"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'})
    data = response.json()
    cores_df = pd.DataFrame(data).filter(['id','nome','red','green','blue','hexadecimal','pantone_código','pantone_name','pantone_hex','fornecedores']) 
    container = st.container()
    st.toast('loading...')
    time.sleep(1.5)
    try:

        hexadecimal,fornecedores = (data[0]['hexadecimal']), data[0]['fornecedores']
        nome,pantone_codigo = data[0]['nome'],data[0] ['pantone_código']
        red,green,blue = data[0]['red'],data[0]['green'],data[0]['blue']
        c,y,m,k = rgb_to_cmyk(data[0]['red'],data[0]['green'],data[0]['blue'])

        response_complementos = requests.post("https://findme-backend.streamlit.app:5555/complementos/",json={'red': red, 'green': green, 'blue': blue,"palheta":tipo_de_palheta,'fornecedores':opcao_fornecedores}) 
        complementos = requests.get("https://findme-backend.streamlit.app:5555/complementos/",headers={'Content-Type': 'application/json'})
        complementos = complementos.json()
        hexadecimalc1,fornecedoresc1 = (complementos[0]['hexadecimal']), complementos[0]['fornecedores']
        nomec1,pantone_codigoc1 = complementos[0]['nome'],complementos[0]['pantone_código']
        redc1,greenc1,bluec1 =complementos[0]['red'],complementos[0]['green'],complementos[0]['blue']
        cc1,yc1,mc1,kc1 = rgb_to_cmyk(complementos[0]['red'],complementos[0]['green'],complementos[0]['blue'])

        hexadecimalc2,fornecedoresc2 = (complementos[1]['hexadecimal']), complementos[1]['fornecedores']
        nomec2,pantone_codigoc2 = complementos[1]['nome'],complementos[1]['pantone_código']
        redc2,greenc2,bluec2 = complementos[1]['red'],complementos[1]['green'],complementos[1]['blue']
        cc2,yc2,mc2,kc2 = rgb_to_cmyk(complementos[1]['red'],complementos[1]['green'],complementos[1]['blue'])
            
        
        with container:

            script = ("<div style='display: flex; flex-direction: row; justify-content: space-around; margin: 0px; padding:0px;width: 700px ;margin: 0px auto; height: 450px;'><div style='background-color: white ; width: 660px; height: 420px;; padding: 10px;box-shadow: 2px 2px 2px 1.5px rgba(0, 0, 0, 0.25);border-radius: 10px 0px 0px 10px; '><div><h5 style='margin: 0px; padding:0px; color:black;'><strong>Cor principal: </strong></h5><div id='container' style='background-color: {}; width: 200px; height: 200px; '></div><p style='color:black; margin: 0px; padding:0px'>{}: {}</p> <p style='color:black;margin: 0px; padding:0px;'>pantone: {}</p><p style='color:black;margin: 0px; padding:0px'>rgb: {},{},{} </p><p style='color:black;margin: 0px; padding:0px'>cyan: {:.2f}<br>yellow: {:.2f}<br>magenta: {:.2f}<br>key:{:.2f}</p></div></div><div style='background-color: white ; width: 660px; height: 420px; padding: 10px;box-shadow: 2px 2px 2px 1.5px rgba(0, 0, 0, 0.25);'><div><h5 style='color:black;margin: 0px; padding:0px'>Cor secundária 1: </h5><div id='container' style='background-color: {}; width: 200px; height: 200px; '></div><p style='color:black; margin: 0px; padding:0px'>{}: {}</p><p style='color:black;margin: 0px; padding:0px;'>pantone: {}</p><p style='color:black;margin: 0px; padding:0px'>rgb: {},{},{} </p><p style='color:black;margin: 0px; padding:0px'>cyan: {:.2f}<br>yellow: {:.2f}<br>magenta: {:.2f}<br>key:{:.2f}</p></div></div><div style='background-color: white ; width: 660px; height: 420px; padding: 10px;box-shadow: 2px 2px 2px 1.5px rgba(0, 0, 0, 0.25);border-radius: 0px 10px 10px 0px;'><div><h5 style='margin: 0px; padding:0px; color:black;'>Cor secundária 2: </h5><div id='container' style='background-color: {}; width: 200px; height: 200px; '></div><p style='color:black; margin: 0px; padding:0px'>{}: {}</p><p style='color:black;margin: 0px; padding:0px;'>pantone: {}</p><p style='color:black;margin: 0px; padding:0px'>rgb: {},{},{} </p><p style='color:black;margin: 0px; padding:0px'>cyan: {:.2f} <br>yellow: {:.2f}<br>magenta: {:.2f}<br>key:{:.2f}</p></div></div></div>").format(hexadecimal,fornecedores,nome,pantone_codigo,red,green,blue,float(c),float(m),float(y),float(k),hexadecimalc1,fornecedoresc1,nomec1,pantone_codigoc1,redc1,greenc1,bluec1,float(cc1),float(mc1),float(yc1),float(kc1),hexadecimalc2,fornecedoresc2,nomec2,pantone_codigoc2,redc2,greenc2,bluec2,float(cc2),float(mc2),float(yc2),float(kc2))
            st.markdown(script, unsafe_allow_html=True)
    except:
        st.write("Nenhuma cor encontrada")

st.title('Find me')
st.subheader('Onde você acha sua cor')
upload = st.file_uploader('dê upload na imagem abaixo para verificar a cor', type=['png','jpg','jpeg'])
opcao_fornecedores = st.selectbox('Em que categoria você quer procurar?', options=('todos', 'coral','suvinil'))
tipo_de_palheta =st.selectbox('quais opções de palheta você está procurando?', options=('triade','complementar','análoga' ))
procura = st.text_input('Digite o nome da cor, o código pantone(00-0000) ou o hexadecimal(#000000):')

button = st.button('Procurar', on_click=findrgb)

receivecolors()


