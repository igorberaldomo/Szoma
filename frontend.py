import streamlit as st
import pandas as pd
import numpy as np
import time
from colorthief import ColorThief
from utils.rgb_to_cmyk import rgb_to_cmyk
from utils.select_complementos import select_complementos
from utils.search.search_hexadecimal import select_hexadecimal
from utils.search.search_codigos import select_códigos
from utils.search.search_name_for_id import search_name_for_id
from utils.search.primary_select import primary_select
from utils.conect_to_engine_production import conect_to_engine_production



# Inicializar o estado da sessão
if "resultados" not in st.session_state:
    st.session_state.resultados = []
if "complementos" not in st.session_state:
    st.session_state.complementos = []
if "tables" not in st.session_state:
    st.session_state.tables = []

# Estilização personalizada
st.markdown("""
<style>
.st-emotion-cache-yfhhig.ef3psqc5{
visibility:hidden
}
.stMainMenu.st-emotion-cache-hwawmg.e16jpq800{
    visibility:hidden
}
</style>
""", unsafe_allow_html=True)

# Funções para processar as entradas do usuário

@st.cache_data
def getting_data():
    engine = conect_to_engine_production()
    queries = {
    "suvinil": "SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil",
    "coral": "SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral",
    # dentro so search parameters note que está escrito sherwin_wilians em vez de sherwin-willians, está correto o SQL não faz busca com o caractere '-' então foi substituido de propósito por '_'
    "sherwin-willians": "SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from sherwin_willians",
    "anjo": "SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from anjo",
    "todos":"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil UNION SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral UNION SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from sherwin_willians union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from anjo"
    }
    
    dataframes ={}    
    
    def convert_to_float(value):
        value = str(value).replace(',', '')  # Substituir vírgula por ponto
        try:
            return float(value)
        except ValueError:
            return None
    
    for table_name, query in queries.items():
        try:
            df = pd.read_sql(query, engine)
        except Exception as e:
            print(f"Erro ao processar a tabela {table_name}: {e}")
            continue
        
        try:
            if table_name in ['suvinil', 'coral', 'sherwin-willians', 'anjo', 'todos']:
                df['fornecedores'] = df['fornecedores'].astype(str)
                df['hexadecimal'] = df['hexadecimal'].astype(str)
                df['nome']  = df['nome'].astype(str)
                df['ncs'] = df['ncs'].astype(str)
                df['codigo_suvinil'] = df['codigo_suvinil'].astype(str)
                df['pantone_código'] = df['pantone_código'].astype(str)
                df['red'] = df['red'].astype(int)
                df['green'] = df['green'].astype(int)
                df['blue'] = df['blue'].astype(int)    
            dataframes[table_name] = df.copy(deep=True)
        except Exception as e:
            print(f"Erro ao processar a tabela {table_name}: {e}")
    return dataframes
# para acessar tabela use table['nome_da_tabela']
tables = getting_data()
st.session_state.tables = tables


def findrgb():
    st.session_state.resultados = []
    if procura or upload:
        if upload is not None:
            ct = ColorThief(upload)
            cor = ct.get_color(quality=1)
            red, green, blue = cor
            fornecedores = opcao_fornecedores
            tabela = st.session_state.tables
            tabela = tabela[fornecedores]
            response_df = primary_select(red, green, blue, tabela)
            st.session_state.resultados = response_df
        elif procura is not None:
            fornecedores = opcao_fornecedores
            if procura[0].isalpha():
                nome = procura
                # para essa função os fornecedores serão determinados dentro da função sendo necessário passar todas as tabelas
                tabela = st.session_state.tables
                response_df = search_name_for_id(nome, tabela)
                st.session_state.resultados = response_df
            if procura[0].isnumeric():
                codigo = procura
                tabela = st.session_state.tables
                tabela = tabela[fornecedores]
                response_df = select_códigos(codigo, tabela)
                st.session_state.resultados = response_df
            if procura[0] == '#':
                hexadecimal = procura
                tabela = st.session_state.tables
                tabela = tabela[fornecedores]
                response_df = select_hexadecimal(hexadecimal, tabela)
                st.session_state.resultados = response_df
    else:
        st.text('Por favor, insira uma imagem ou um valor para procurar a cor')


def receivecolors():
    if len(st.session_state.resultados) > 0:
        data = st.session_state.resultados
        cores_df = pd.DataFrame(data)
        container = st.container()
        st.toast('Carregando...')
        time.sleep(1.5)
        data_df = pd.DataFrame(data, index=[0])
        data = data_df.to_dict(orient='records')
        tabela = st.session_state.tables
        fornecedores = opcao_fornecedores
        st.write(data)
        try:
            # Processar a cor principal
            cor_principal = data[0]
            red, green, blue = cor_principal['red'], cor_principal['green'], cor_principal['blue']
            c, m, y, k = rgb_to_cmyk(red, green, blue)
            fornecedores = cor_principal['fornecedores']
            nome = cor_principal['nome']
            hexadecimal = cor_principal['hexadecimal']
            pantone_codigo = cor_principal['pantone_código']

            # Calcular complementos
            tabela = tabela[fornecedores]
            complementos = select_complementos(red, green, blue, tipo_de_palheta, tabela)
            st.session_state.complementos = complementos

            # Processar complementos
            complemento1 = complementos[0]
            redc1, greenc1, bluec1 = complemento1['red'], complemento1['green'], complemento1['blue']
            cc1, mc1, yc1, kc1 = rgb_to_cmyk(redc1, greenc1, bluec1)
            fornecedoresc1 = complemento1['fornecedores']
            nomec1 = complemento1['nome']
            hexadecimalc1 = complemento1['hexadecimal']
            pantone_codigoc1 = complemento1['pantone_código']

            complemento2 = complementos[1]
            redc2, greenc2, bluec2 = complemento2['red'], complemento2['green'], complemento2['blue']
            cc2, mc2, yc2, kc2 = rgb_to_cmyk(redc2, greenc2, bluec2)
            fornecedoresc2 = complemento2['fornecedores']
            nomec2 = complemento2['nome']
            hexadecimalc2 = complemento2['hexadecimal']
            pantone_codigoc2 = complemento2['pantone_código']
            # renderizar complementos
            with container:
                script = ("<div style='display: flex; flex-direction: row; justify-content: space-around; margin: 0px; padding:0px;width: 700px ;margin: 0px auto; height: 450px;'>"
                          "<div style='background-color: white ; width: 660px; height: 450px; padding: 10px;box-shadow: 2px 2px 2px 1.5px rgba(0, 0, 0, 0.25);border-radius: 10px 0px 0px 10px;'>"
                          "<div><h5 style='margin: 0px; padding:0px; color:black;'><strong>Cor principal:</strong></h5>"
                          "<div id='container' style='background-color: {}; width: 200px; height: 200px;'></div>"
                          "<p style='color:black; margin: 0px; padding:0px'>{}: {}</p>"
                          "<p style='color:black;margin: 0px; padding:0px;'>Pantone: {}</p>"
                          "<p style='color:black;margin: 0px; padding:0px'>RGB: {},{},{} </p>"
                          "<p style='color:black;margin: 0px; padding:0px'>Cyan: {:.2f}<br>Magenta: {:.2f}<br>Yellow: {:.2f}<br>Key: {:.2f}</p>"
                          "</div></div>"
                          "<div style='background-color: white ; width: 660px; height: 450px; padding: 10px;"
                          "box-shadow: 2px 2px 2px 1.5px rgba(0, 0, 0, 0.25);'>"
                          "<div><h5 style='color:black;margin: 0px; padding:0px'>Cor secundária 1:</h5>"
                          "<div id='container' style='background-color: {}; width: 200px; height: 200px;'></div>"
                          "<p style='color:black; margin: 0px; padding:0px'>{}: {}</p>"
                          "<p style='color:black;margin: 0px; padding:0px;'>Pantone: {}</p>"
                          "<p style='color:black;margin: 0px; padding:0px'>RGB: {},{},{} </p>"
                          "<p style='color:black;margin: 0px; padding:0px'>Cyan: {:.2f}<br>Magenta: {:.2f}<br>Yellow: {:.2f}<br>Key: {:.2f}</p>"
                          "</div></div>"
                          "<div style='background-color: white ; width: 660px; height: 450px; padding: 10px;"
                          "box-shadow: 2px 2px 2px 1.5px rgba(0, 0, 0, 0.25);border-radius: 0px 10px 10px 0px;'>"
                          "<div><h5 style='margin: 0px; padding:0px; color:black;'>Cor secundária 2:</h5>"
                          "<div id='container' style='background-color: {}; width: 200px; height: 200px;'></div>"
                          "<p style='color:black; margin: 0px; padding:0px'>{}: {}</p>"
                          "<p style='color:black;margin: 0px; padding:0px;'>Pantone: {}</p>"
                          "<p style='color:black;margin: 0px; padding:0px'>RGB: {},{},{} </p>"
                          "<p style='color:black;margin: 0px; padding:0px'>Cyan: {:.2f}<br>Magenta: {:.2f}<br>Yellow: {:.2f}<br>Key: {:.2f}</p>"
                          "</div></div></div>").format(
                    hexadecimal, fornecedores, nome, pantone_codigo, red, green, blue, c, m, y, k,
                    hexadecimalc1, fornecedoresc1, nomec1, pantone_codigoc1, redc1, greenc1, bluec1, cc1, mc1, yc1, kc1,
                    hexadecimalc2, fornecedoresc2, nomec2, pantone_codigoc2, redc2, greenc2, bluec2, cc2, mc2, yc2, kc2)
                st.markdown(script, unsafe_allow_html=True)
        except Exception as e:
            st.write("Nenhuma cor encontrada")
            st.write(f"Erro: {e}")
    else:
        st.write("Nenhuma cor encontrada")

# Interface do usuário
st.title('Find Me')
st.subheader('Onde você acha sua cor')
upload = st.file_uploader('Faça upload de uma imagem para verificar a cor', type=['png', 'jpg', 'jpeg'])
opcao_fornecedores = st.selectbox('Em que categoria você quer procurar?', options=('todos', 'coral', 'suvinil', 'sherwin-willians','anjo'))
tipo_de_palheta = st.selectbox('Quais opções de palheta você está procurando?', options=('triade', 'complementar', 'análoga'))
procura = st.text_input('Digite o nome da cor, o código Pantone (00-0000) ou o hexadecimal (#000000):')

button = st.button('Procurar', on_click=findrgb)

receivecolors()
