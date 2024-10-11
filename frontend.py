from colorthief import ColorThief
import streamlit as st
import numpy as np
import pandas as pd
import requests


st.markdown("""
<style>
.st-emotion-cache-yfhhig.ef3psqc5{
visibility:hidden
}
stVerticalBlock.st-emotion-cache-1n76uvr.e1f1d6gn2{
    width: 900px;
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

def receivesuvinil():
    response = requests.get("http://localhost:5555/suvinil/")
    data = response.json()
    st.text(data[0]['id'])
    cores_df = pd.DataFrame(data).filter(['id','nome','red','green','blue','hexadecimal','pantone_código','pantone_name','pantone_hex','fornecedores'])
    st.text('Cores encontradas:')
    st.dataframe(cores_df)
    c= 0
    while c < 3:
        st.html("""
                <style>
                .container {
                    width: 100%;
                    height: 200px;
                    position: ;
                    justify-content: space-between;
                }
                .fornecedor {
                    width: 300px;
                    height: 200px;
                    background-color:""" + {} + """;
                    padding: 5px;
                }
                .pantone {
                    width: 300px;
                    height: 200px;
                    background-color:""" + {} + """;
                }
                </style>
                <div class='container'>
                    <div class='fornecedor'></div>
                    <div class='pantone'></div>
                </div>""")
        c+=1
    
    
st.title('Find me')
st.subheader('Onde você acha sua cor')
st.markdown('---')
upload = st.file_uploader('dê upload na imagem abaixo para verificar a cor', type=['png','jpg','jpeg'])
select = st.selectbox('Em que categoria você quer procurar?', options=('todos', 'suvinil'), 
)
btn = st.button('procura', on_click=findrgb)
receivesuvinil()


