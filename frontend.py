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


def add():
    number = st.session_state.count
    newvalue= int(number) + 3
    st.session_state.count = str(newvalue)
    
def subtract():
    number = st.session_state.count
    newvalue= int(number) - 3
    st.session_state.count = str(newvalue)
    
def pickcard():
    return st.session_state.count

def update(updated):
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
        posição = pickcard()
        card = (int(posição))
        if (card +1) +3 > len(data):
            card = len(data) -3
            update(card)
        if card <0:
            card = 0
            update(card)

        
        if len(data) >= 0 and len(data)-1 <=1:
            hexadecimal,fornecedores = (data[card]['hexadecimal']), data[card]['fornecedores']
            nome,pantone_codigo = data[card]['nome'],data[card] ['pantone_código']
            red,green,blue = data[card]['red'],data[card]['green'],data[card]['blue']
            c,y,m,k = rgb_to_cmyk(data[card]['red'],data[card]['green'],data[card]['blue'])
            complementos = requests.post("http://localhost:5555/complementos/",json={'red': red, 'green': green, 'blue': blue,"palheta":tipo_de_palheta })
            st.write(complementos)
            
            with container:
                script = ("<div style='display: flex; flex-direction: row; justify-content: space-around; margin: 0px; padding:0px;width: 700px ;margin: 0px auto; height: 450px;'><div style='background-color: white ; width: 220px; height: 400px;border-radius: 10px; padding: 10px;box-shadow: 2px 2px 2px 1.5px rgba(0, 0, 0, 0.25); margin: 5px;'><div id='container' style='background-color:{}; width: 200px; height: 200px; '></div> <p style='color:black; margin: 0px; padding:0px'>{}: {}</p><p style='color:black;margin: 0px; padding:0px;'>pantone: {}</p> <p style='color:black;margin: 0px; padding:0px'>rgb: {},{},{} </p> <p style='color:black;margin: 0px; padding:0px'>cyan: {:.2f} <br>yellow: {:.2f} <br>magenta: {:.2f} <br>key:{:.2f} </p> </div></div>").format(hexadecimal,fornecedores,nome,pantone_codigo,red,green,blue,float(c),float(m),float(y),float(k))
                st.markdown(script, unsafe_allow_html=True)

        else:
            # pega os dados em variáveis
            hexadecimal,fornecedores = (data[card]['hexadecimal']), data[card]['fornecedores']
            nome,pantone_codigo = data[card]['nome'],data[card] ['pantone_código']
            red,green,blue = data[card]['red'],data[card]['green'],data[card]['blue']
            c,y,m,k = rgb_to_cmyk(data[card]['red'],data[card]['green'],data[card]['blue'])
            hexadecimal1,fornecedores1 = (data[card+1]['hexadecimal']), data[card+1]['fornecedores']
            nome1,pantone_codigo1 = data[card+1]['nome'],data[card+1] ['pantone_código']
            red1,green1,blue1 = data[card+1]['red'],data[card+1]['green'],data[card+1]['blue']
            c1,y1,m1,k1 = rgb_to_cmyk(data[card+1]['red'],data[card+1]['green'],data[card+1]['blue'])
            hexadecimal2,fornecedores2 = (data[card+2]['hexadecimal']), data[card+2]['fornecedores']
            nome2,pantone_codigo2 = data[card+2]['nome'],data[card+2]['pantone_código']
            red2,green2,blue2 = data[card+2]['red'],data[card+2]['green'],data[card+2]['blue']
            c2,y2,m2,k2 = rgb_to_cmyk(data[card+2]['red'],data[card+2]['green'],data[card+2]['blue'])
        
            with container:
                st.button('anterior', key='anterior', on_click=subtract)
                script = ("<div style='display: flex; flex-direction: row; justify-content: space-around; margin: 0px; padding:0px;width: 700px ;margin: 0px auto; height: 450px;'><div style='background-color: white ; width: 220px; height: 400px;border-radius: 10px; padding: 10px;box-shadow: 2px 2px 2px 1.5px rgba(0, 0, 0, 0.25); margin: 5px;'><div id='container' style='background-color: {}; width: 200px; height: 200px; '></div> <p style='color:black; margin: 0px; padding:0px'>{}: {}</p><p style='color:black;margin: 0px; padding:0px;'>pantone: {}</p> <p style='color:black;margin: 0px; padding:0px'>rgb: {},{},{} </p> <p style='color:black;margin: 0px; padding:0px'>cyan: {:.2f} <br>yellow: {:.2f} <br>magenta: {:.2f} <br>key:{:.2f} </p> </div><div style='background-color: white ; width: 220px; height: 400px;border-radius: 10px; padding: 10px;box-shadow: 2px 2px 2px 1.5px rgba(0, 0, 0, 0.25); margin: 5px;'> <div id='container' style='background-color: {}; width: 200px; height: 200px; '></div> <p style='color:black; margin: 0px; padding:0px'>{}: {}</p> <p style='color:black;margin: 0px; padding:0px;'>pantone: {}</p> <p style='color:black;margin: 0px; padding:0px'>rgb: {},{},{} </p> <p style='color:black;margin: 0px; padding:0px'>cyan: {:.2f} <br>yellow: {:.2f} <br>magenta: {:.2f} <br>key:{:.2f} </p> </div><div style='background-color: white ; width: 220px; height: 400px;border-radius: 10px; padding: 10px;box-shadow: 2px 2px 2px 1.5px rgba(0, 0, 0, 0.25); margin: 5px;'> <div id='container' style='background-color: {}; width: 200px; height: 200px; '></div> <p style='color:black; margin: 0px; padding:0px'>{}: {}</p> <p style='color:black;margin: 0px; padding:0px;'>pantone: {}</p> <p style='color:black;margin: 0px; padding:0px'>rgb: {},{},{} </p> <p style='color:black;margin: 0px; padding:0px'>cyan: {:.2f} <br>yellow: {:.2f}<br>magenta: {:.2f}<br>key:{:.2f} </p> </div></div>").format(hexadecimal,fornecedores,nome,pantone_codigo,red,green,blue,float(c),float(m),float(y),float(k),hexadecimal1,fornecedores1,nome1,pantone_codigo1,red1,green1,blue1,float(c1),float(m1),float(y1),float(k1),hexadecimal2,fornecedores2,nome2,pantone_codigo2,red2,green2,blue2,float(c2),float(m2),float(y2),float(k2))
                st.markdown(script, unsafe_allow_html=True)
                st.button('proximo', key='proximo', on_click=add)
 
st.title('Find me')
st.subheader('Onde você acha sua cor',divider='rainbow')
upload = st.file_uploader('dê upload na imagem abaixo para verificar a cor', type=['png','jpg','jpeg'])
select = st.selectbox('Em que categoria você quer procurar?', options=('todos', 'suvinil'))
tipo_de_palheta =st.selectbox('quais opções de palheta você está procurando?', options=('complementar','análoga', 'triade'))
procura = st.text_input('Digite o nome da cor, o código pantone(00-0000) ou o hexadecimal(#000000):')
button = st.button('Procurar', on_click=findrgb)

receivesuvinil()



