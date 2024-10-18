from colorthief import ColorThief
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import numpy as np
import pandas as pd
import requests
import json



if "count" not in st.session_state:
    st.session_state.count = '0'
                
st.markdown("""
<style>
.st-emotion-cache-yfhhig.ef3psqc5{
visibility:hidden
}

</style>
""", unsafe_allow_html=True)

RGB_SCALE = 255
CMYK_SCALE = 100
query = True


def add_count():
    number = st.session_state.count
    newvalue= int(number) + 3
    st.session_state.count = str(newvalue)
    
def subtract_count():
    number = st.session_state.count
    newvalue= int(number) - 3
    st.session_state.count = str(newvalue)
    
def select_count():
    return st.session_state.count

def update_counter(updated):
    number = st.session_state.count
    newvalue= updated
    st.session_state.count = str(newvalue)
def rgb_to_cmyk(r, g, b):
    if (r, g, b) == (0, 0, 0):
        # black
        return 0, 0, 0, CMYK_SCALE

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / RGB_SCALE
    m = 1 - g / RGB_SCALE
    y = 1 - b / RGB_SCALE

    # extract out k [0, 1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    # rescale to the range [0,CMYK_SCALE]
    return c * CMYK_SCALE, m * CMYK_SCALE, y * CMYK_SCALE, k * CMYK_SCALE

def findrgb():
    if upload is not None:
        st.session_state.cliked = True
        ct = ColorThief(upload)
        cor = ct.get_color(quality=1)
        response = requests.post("http://localhost:5555/suvinil/",json=cor)
        data = response.json()
        return data
    if procura is not None and upload is None :
        if procura[0].isalpha():
            st.session_state.cliked = True
            name = {"nome":procura}
            response = requests.post("http://localhost:5555/names/",json=name)
        if procura[0].isnumeric():
            codigo = {"codigo":procura}
            response = requests.post("http://localhost:5555/codigos/",json=codigo)
        if procura[0] == '#':
            hexa = {"hexadecimal":procura}
            response = requests.post("http://localhost:5555/hex/",json=hexa)
        return response
    else:
        st.text('Por favor coloque uma imagem para verificar a cor')

     
def receivesuvinil():
    response = requests.get("http://localhost:5555/suvinil/")
    data = response.json()
    cores_df = pd.DataFrame(data).filter(['id','nome','red','green','blue','hexadecimal','pantone_código','pantone_name','pantone_hex','fornecedores']) 
    container = st.container()
    
    if data is not None:
        # seleciona o numero do index
        posição = select_count()
        card = (int(posição))
        if (card +1) +3 > len(data):
            card = len(data) -3
            update_counter(card)
        if card < 0:
            card = 0
            update_counter(card)
        
        if len(data) > 0 :
            hexadecimal,fornecedores = (data[card]['hexadecimal']), data[card]['fornecedores']
            nome,pantone_codigo = data[card]['nome'],data[card] ['pantone_código']
            red,green,blue = data[card]['red'],data[card]['green'],data[card]['blue']
            c,y,m,k = rgb_to_cmyk(data[card]['red'],data[card]['green'],data[card]['blue'])
            response_complementos = requests.post("http://localhost:5555/complementos/",json={'red': red, 'green': green, 'blue': blue,"palheta":tipo_de_palheta })
            complementos = requests.get("http://localhost:5555/complementos/")
            complementos = complementos.json()
            hexadecimalc1,fornecedoresc1 = (complementos[0][0]['hexadecimal']), complementos[0][0]['fornecedores']
            nomec1,pantone_codigoc1 = complementos[0][0]['nome'],complementos[0][0]['pantone_código']
            redc1,greenc1,bluec1 =complementos[0][0]['red'],complementos[0][0]['green'],complementos[0][0]['blue']
            cc1,yc1,mc1,kc1 = rgb_to_cmyk(complementos[0][0]['red'],complementos[0][0]['green'],complementos[0][0]['blue'])

            hexadecimalc2,fornecedoresc2 = (complementos[1][0]['hexadecimal']), complementos[1][0]['fornecedores']
            nomec2,pantone_codigoc2 = complementos[1][0]['nome'],complementos[1][0] ['pantone_código']
            redc2,greenc2,bluec2 = complementos[1][0]['red'],complementos[1][0]['green'],complementos[1][0]['blue']
            cc2,yc2,mc2,kc2 = rgb_to_cmyk(complementos[1][0]['red'],complementos[1][0]['green'],complementos[1][0]['blue'])
                
            
            
            with container:
                # st.button('anterior', key='anterior', on_click=subtract_count)
                # st.button('proximo', key='proximo', on_click=add_count)
                script = ("<div style='display: flex; flex-direction: row; justify-content: space-around; margin: 0px; padding:0px;width: 700px ;margin: 0px auto; height: 450px;'><div style='background-color: white ; width: 660px; height: 420px;; padding: 10px;box-shadow: 2px 2px 2px 1.5px rgba(0, 0, 0, 0.25);border-radius: 10px 0px 0px 10px; '><div><h5 style='margin: 0px; padding:0px; color:black;'><strong>Cor principal: </strong></h5><div id='container' style='background-color: {}; width: 200px; height: 200px; '></div><p style='color:black; margin: 0px; padding:0px'>{}: {}</p> <p style='color:black;margin: 0px; padding:0px;'>pantone: {}</p><p style='color:black;margin: 0px; padding:0px'>rgb: {},{},{} </p><p style='color:black;margin: 0px; padding:0px'>cyan: {:.2f}<br>yellow: {:.2f}<br>magenta: {:.2f}<br>key:{:.2f}</p></div></div><div style='background-color: white ; width: 660px; height: 420px; padding: 10px;box-shadow: 2px 2px 2px 1.5px rgba(0, 0, 0, 0.25);'><div><h5 style='color:black;margin: 0px; padding:0px'>Cor secundária 1: </h5><div id='container' style='background-color: {}; width: 200px; height: 200px; '></div><p style='color:black; margin: 0px; padding:0px'>{}: {}</p><p style='color:black;margin: 0px; padding:0px;'>pantone: {}</p><p style='color:black;margin: 0px; padding:0px'>rgb: {},{},{} </p><p style='color:black;margin: 0px; padding:0px'>cyan: {:.2f}<br>yellow: {:.2f}<br>magenta: {:.2f}<br>key:{:.2f}</p></div></div><div style='background-color: white ; width: 660px; height: 420px; padding: 10px;box-shadow: 2px 2px 2px 1.5px rgba(0, 0, 0, 0.25);border-radius: 0px 10px 10px 0px;'><div><h5 style='margin: 0px; padding:0px; color:black;'>Cor secundária 2: </h5><div id='container' style='background-color: {}; width: 200px; height: 200px; '></div><p style='color:black; margin: 0px; padding:0px'>{}: {}</p><p style='color:black;margin: 0px; padding:0px;'>pantone: {}</p><p style='color:black;margin: 0px; padding:0px'>rgb: {},{},{} </p><p style='color:black;margin: 0px; padding:0px'>cyan: {:.2f} <br>yellow: {:.2f}<br>magenta: {:.2f}<br>key:{:.2f}</p></div></div></div>").format(hexadecimal,fornecedores,nome,pantone_codigo,red,green,blue,float(c),float(m),float(y),float(k),hexadecimalc1,fornecedoresc1,nomec1,pantone_codigoc1,redc1,greenc1,bluec1,float(cc1),float(mc1),float(yc1),float(kc1),hexadecimalc2,fornecedoresc2,nomec2,pantone_codigoc2,redc2,greenc2,bluec2,float(cc2),float(mc2),float(yc2),float(kc2))
                st.markdown(script, unsafe_allow_html=True)
        else:
            st.write("Nenhuma cor encontrada")
st.title('Find me')
st.subheader('Onde você acha sua cor')
upload = st.file_uploader('dê upload na imagem abaixo para verificar a cor', type=['png','jpg','jpeg'])
select = st.selectbox('Em que categoria você quer procurar?', options=('todos', 'suvinil'))
tipo_de_palheta =st.selectbox('quais opções de palheta você está procurando?', options=('triade','complementar','análoga' ))
procura = st.text_input('Digite o nome da cor, o código pantone(00-0000) ou o hexadecimal(#000000):')
button = st.button('Procurar', on_click=findrgb)

receivesuvinil()



