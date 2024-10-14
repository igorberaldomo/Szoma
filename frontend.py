from colorthief import ColorThief
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import numpy as np
import pandas as pd
import requests


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

def receivesuvinil():
    response = requests.get("http://localhost:5555/suvinil/")
    data = response.json()
    cores_df = pd.DataFrame(data).filter(['id','nome','red','green','blue','hexadecimal','pantone_código','pantone_name','pantone_hex','fornecedores'])
    
    st.text(data)
    st.dataframe(cores_df)
    row1 =st.columns(2)
    row2 =st.columns(2)
    row3 =st.columns(2)
    row4 =st.columns(2)
    row5 =st.columns(2)
    st.markdown("""
        <style>
 
        .st-emotion-cache-1apb2ab.e1f1d6gn0{
            background-color: red;
        }
        </style>
        """, unsafe_allow_html=True)
    c=0
    while c < len(data):
        for col in row1+row2+row3+row4+row5:
            if col == row1[0] or col == row2[0] or col == row3[0] or col == row4[0] or col == row5[0]:
                tile = col.container(height=200)
                tile.write(f'{data[c]["nome"]}',key='main'+str(c))
            else:
                tile = col.container(height=200)
                tile.write(f'{data[c]["pantone_name"]}',key='pant'+str(c))
                c+=1
    
    
st.title('Find me')
st.subheader('Onde você acha sua cor')
st.markdown('---')
upload = st.file_uploader('dê upload na imagem abaixo para verificar a cor', type=['png','jpg','jpeg'])
select = st.selectbox('Em que categoria você quer procurar?', options=('todos', 'suvinil'), 
)
button = st.button('Verificar', on_click=findrgb)
receivesuvinil()




            # [{'blue': 60, 'fornecedores': 'suvenil', 'green': 44, 'hexadecimal': '#ac2c3c', 'id': 109, 'nome': 'cereja', 'pantone_código': '19-1559', 'pantone_hex': '#9d202f', 'pantone_name': 'scarlet-sage', 'red': 172},
            # {'blue': 60, 'fornecedores': 'suvenil', 'green': 52, 'hexadecimal': '#84343c', 'id': 152, 'nome': 'desejo', 'pantone_código': '19-1338', 'pantone_hex': '#743332', 'pantone_name': 'russet-brown', 'red': 132},
            # {'blue': 60, 'fornecedores': 'suvenil', 'green': 44, 'hexadecimal': '#ac2c3c', 'id': 317, 'nome': 'paixao inspiradora', 'pantone_código': '19-1559', 'pantone_hex': '#9d202f', 'pantone_name': 'scarlet-sage', 'red': 172},
            # {'blue': 44, 'fornecedores': 'suvenil', 'green': 36, 'hexadecimal': '#c4242c', 'id': 453, 'nome': 'valentino', 'pantone_código': '18-1551', 'pantone_hex': '#b4262a', 'pantone_name': 'aura-orange', 'red': 196}]