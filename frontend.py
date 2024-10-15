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
    
    
st.title('Find me')
st.subheader('Onde você acha sua cor')
st.markdown('---')
upload = st.file_uploader('dê upload na imagem abaixo para verificar a cor', type=['png','jpg','jpeg'])
select = st.selectbox('Em que categoria você quer procurar?', options=('todos', 'suvinil'))
procura = st.text_input('Digite o nome da cor, o código pantone ou o hexadecimal(#000000):')
button = st.button('Procurar', on_click=findrgb)

receivesuvinil()



