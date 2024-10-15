from colorthief import ColorThief
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import numpy as np
import pandas as pd
import requests
import json

st.markdown("""
<style>
.st-emotion-cache-yfhhig.ef3psqc5{
visibility:hidden
}

</style>
""", unsafe_allow_html=True)

RGB_SCALE = 255
CMYK_SCALE = 100


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
    if procura is not None and upload is None and procura[0] not in '0123456789#':
        st.session_state.cliked = True
        name = {"nome":procura}
        response = requests.post("http://localhost:5555/names/",json=name)
        return response
    if procura is not None and upload is None and procura[0] in '0123456789#':
        st.session_state.cliked = True
        if procura[0] == '#':
            procura = {"hexadecimal":procura}
        else:
            procura = {"pantone": procura}
        response = requests.post("http://localhost:5555/procura/",json=name)
        return response
    else:
        st.text('Por favor coloque uma imagem para verificar a cor')

     
def receivesuvinil():
    response = requests.get("http://localhost:5555/suvinil/")
    data = response.json()
    cores_df = pd.DataFrame(data).filter(['id','nome','red','green','blue','hexadecimal','pantone_código','pantone_name','pantone_hex','fornecedores'])  
    st.dataframe(cores_df)
    container = st.container()
    c,y,m,k = rgb_to_cmyk(data[0]['red'],data[0]['green'],data[0]['blue'])
    c1,y1,m1,k1 = rgb_to_cmyk(data[1]['red'],data[1]['green'],data[1]['blue'])
    c2,y2,m2,k2 = rgb_to_cmyk(data[2]['red'],data[2]['green'],data[2]['blue'])
    with container:
        script = "<div style='display: flex; flex-direction: row; justify-content: space-around; margin: 0px; padding:0px'> <div style='background-color: white ; width: 220px; height: 400px;border-radius: 10px; padding: 10px'><div id='container' style='background-color: {}; width: 200px; height: 200px; '></div><p style='color:black; margin: 0px; padding:0px'>{}: {}</p><p style='color:black;margin: 0px; padding:0px;'>pantone: {}</p><p style='color:black;margin: 0px; padding:0px'>rgb: {},{},{} </p><p style='color:black;margin: 0px; padding:0px'>cyan: {:.2f}<br>yellow: {:.2f}<br>magenta: {:.2f}<br>key: {:.2f} </p></div><div style='background-color: white ; width: 220px; height: 400px;border-radius: 10px; padding: 10px'><div id='container' style='background-color: {}; width: 200px; height: 200px; '></div><p style='color:black; margin: 0px; padding:0px'>{}: {}</p><p style='color:black;margin: 0px; padding:0px;'>pantone: {}</p><p style='color:black;margin: 0px; padding:0px'>rgb: {},{},{} </p><p style='color:black;margin: 0px; padding:0px'>cyan: {:.2f}<br>yellow: {:.2f}<br>magenta: {:.2f}<br>key: {:.2f} </p></div><div style='background-color: white ; width: 220px; height: 400px;border-radius: 10px; padding: 10px'><div id='container' style='background-color: {}; width: 200px; height: 200px; '></div><p style='color:black; margin: 0px; padding:0px'>{}: {}</p><p style='color:black;margin: 0px; padding:0px;'>pantone: {}</p><p style='color:black;margin: 0px; padding:0px'>rgb: {},{},{} </p><p style='color:black;margin: 0px; padding:0px'>cyan: {:.2f}<br>yellow: {:.2f}<br>magenta: {:.2f}<br>key: {:.2f} </p></div></div>".format(data[0]['hexadecimal'], data[0]['fornecedores'], data[0]['nome'],data[0] ['pantone_name'],data[0]['red'],data[0]['green'],data[0]['blue'],float(c),float(m),float(y),float(k),data[1]['hexadecimal'], data[1]['fornecedores'], data[1]['nome'],data[1] ['pantone_name'],data[1]['red'],data[1]['green'],data[1]['blue'],float(c1),float(m1),float(y1),float(k1),data[2]['hexadecimal'], data[2]['fornecedores'], data[2]['nome'],data[2] ['pantone_name'],data[2]['red'],data[2]['green'],data[2]['blue'],float(c2),float(m2),float(y2),float(k2))
        st.markdown(script, unsafe_allow_html=True)

 
st.title('Find me')
st.subheader('Onde você acha sua cor')
st.markdown('---')
upload = st.file_uploader('dê upload na imagem abaixo para verificar a cor', type=['png','jpg','jpeg'])
select = st.selectbox('Em que categoria você quer procurar?', options=('todos', 'suvinil'))
procura = st.text_input('Digite o nome da cor, o código pantone ou o hexadecimal(#000000):')
button = st.button('Procurar', on_click=findrgb)

receivesuvinil()



