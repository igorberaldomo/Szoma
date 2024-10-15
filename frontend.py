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
    else:
        st.text('Por favor coloque uma imagem para verificar a cor')

def findname():
     if nomecor is not None:
        st.session_state.cliked = True
        name = {"nome":nomecor}
        response = requests.post("http://localhost:5555/names/",json=name)
        print(response)
        return response
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
nomecor = st.text_input('Qual é o nome da cor que deseja verificar?')
button = st.button('Verificar', on_click=findrgb)
button2 = st.button('Verificar nome', on_click=findname)
receivesuvinil()



