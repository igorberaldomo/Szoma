import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from streamlit_cropper import st_cropper
from PIL import Image as image2
from PIL import ImageEnhance
from colorthief import ColorThief
from utils.editing.rgb_para_cmyk import rgb_para_cmyk
from utils.search_methods.select_complements import select_complements
from utils.search_methods.search_hexadecimal import search_hexadecimal
from utils.search_methods.search_codigos import search_codigos
from utils.search_methods.search_nome_to_find_id import search_nome_to_find_id
from utils.search_methods.search_codigo_to_find_id import search_codigo_to_find_id
from utils.search_methods.search_hexadecimal_to_find_id import search_hexadecimal_to_find_id
from utils.search_methods.select_first_color import select_first_color
from utils.search_methods.select_colors_in_all_suppliers import select_colors_in_all_suppliers
from utils.conection.production_connection import production_connection


# Inicializar o estado da sessão
if "resultados" not in st.session_state:
    st.session_state.resultados = []
if "complementos" not in st.session_state:
    st.session_state.complementos = []
if "tables" not in st.session_state:
    st.session_state.tables = []
if "cor" not in st.session_state:
    st.session_state.cor = '#ffffff'
    

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
def cache_data():
    engine = production_connection()
    searchs = {
    "suvinil": "SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil",
    "coral": "SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral",
    # dentro so metodos_de_args parameters note que está escrito sherwin_wilians em vez de sherwin-willians, está correto o SQL não faz busca com o caractere '-' então foi substituido de propósito por '_'
    "sherwin-willians": "SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from sherwin_willians",
    "anjo": "SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from anjo",
    "todos":"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil UNION SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral UNION SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from sherwin_willians union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from anjo"
    }
    
    dataframes ={}    
    
    def converter_str_para_float(value):
        value = str(value).replace(',', '')  # Substituir vírgula por ponto
        try:
            return float(value)
        except ValueError:
            return None
    
    for table_name, args in searchs.items():
        try:
            df = pd.read_sql(args, engine)
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
tables = cache_data()

st.session_state.tables = tables

def encontrar_cor_similar(caminho_para_imagem, args,opção_fornecedores):
    # esse métodos parecem com aqueles no encontrar rgb mas os métodos abaixo são maiores em escopo não necessitando do nome dos fornecedores
    if args is not None:
        if args[0].isalpha():
            nome = args
            # para essa função os fornecedores serão determinados dentro da função sendo necessário passar todas as tabelas
            tabela = st.session_state.tables
            resultados = search_nome_to_find_id(nome,tabela)
            st.session_state.resultados = resultados
        elif args[0].isnumeric():
            codigo = args
            tabela = st.session_state.tables
            if opção_fornecedores == "todos":
                resultados = search_codigo_to_find_id(codigo, tabela)
            else:
                tabela = tabela[opção_fornecedores]
                resultados = search_codigos(codigo, tabela)
            st.session_state.resultados = resultados
        elif args[0] == '#':
            hexadecimal = args
            tabela = st.session_state.tables
            if opção_fornecedores == "todos":
                resultados = search_hexadecimal_to_find_id(hexadecimal, tabela)
            else:
                tabela = tabela[opção_fornecedores]
                resultados = search_hexadecimal(hexadecimal, tabela)
            st.session_state.resultados = resultados
    elif caminho_para_imagem is not None:
        ct = ColorThief(caminho_para_imagem)
        cor = ct.get_color(quality=1)
        red, green, blue = cor
        fornecedores = opção_fornecedores
        tabela = st.session_state.tables
        tabela = tabela[fornecedores]
        dataframe_da_resposta = select_first_color(red, green, blue, tabela)
        st.session_state.resultados = dataframe_da_resposta
    else:
        st.write('Não foi colocado uma imagem ou um valor para argsr a cor')
      
def mudar_cor_da_caixa():
    if st.session_state.cor == '#ffffff':
        st.session_state.cor = '#000000'
    else:
        st.session_state.cor = '#ffffff'

def find_rgb_value(args, upload, camera ,opção_fornecedores,filtros):

    st.session_state.resultados = []
    if args or upload or camera:
        if upload is not None:
            ct = ColorThief(upload)
            cor = ct.get_color(quality=1)
            red, green, blue = cor
            if filtros =="Luz Quente":
                red = red + 16
                green = green + 16
                blue = blue + 48

            fornecedores = opção_fornecedores

            tabela = st.session_state.tables
            tabela = tabela[fornecedores]
            dataframe_da_resposta = select_first_color(red, green, blue, tabela)
            if dataframe_da_resposta.empty:
                st.text('Erro imagem desfocada, selecione outra imagem')
            else:
                st.session_state.resultados = dataframe_da_resposta
        elif camera is not None:
            ct = ColorThief(camera)
            cor = ct.get_color(quality=1)
            red, green, blue = cor
            if filtros == "Luz Quente": # luz quente muda os tons em vermelho e verde por 
                red = red + 16
                green = green + 16
                blue = blue + 48

            fornecedores = opção_fornecedores

            tabela = st.session_state.tables
            tabela = tabela[fornecedores]
            dataframe_da_resposta = select_first_color(red, green, blue, tabela)
            if dataframe_da_resposta.empty:
                st.text('Erro imagem desfocada, tire outra foto')
            else:
                st.session_state.resultados = dataframe_da_resposta
        elif args is not None:
            fornecedores = opção_fornecedores
            if args[0].isalpha():
                nome = args
                # para essa função os fornecedores serão determinados dentro da função sendo necessário passar todas as tabelas
                tabela = st.session_state.tables
                dataframe_da_resposta = search_nome_to_find_id(nome, tabela)
                st.session_state.resultados = dataframe_da_resposta
            if args[0].isnumeric():
                codigo = args
                tabela = st.session_state.tables
                tabela = tabela[fornecedores]
                dataframe_da_resposta = search_codigos(codigo, tabela)
                st.session_state.resultados = dataframe_da_resposta
            if args[0] == '#':
                hexadecimal = args
                tabela = st.session_state.tables
                tabela = tabela[fornecedores]
                dataframe_da_resposta = search_hexadecimal(hexadecimal, tabela)
                st.session_state.resultados = dataframe_da_resposta
    else:
        st.text('Por favor, insira uma imagem ou um valor para argsr a cor')

def show_similar_colors():
    if len(st.session_state.resultados) >0:
            data = st.session_state.resultados
            container = st.container()
            st.toast('Carregando...')
            time.sleep(1.5)
            data_df = pd.DataFrame(data, index=[0])
            data = data_df.to_dict(orient='records')
            tabela = st.session_state.tables
            hexadecimal = data[0]['hexadecimal']
            nome, fornecedor = data[0]['nome'], data[0]['fornecedores']
            red, green, blue = data[0]['red'], data[0]['green'], data[0]['blue']
            if red > 155 or green > 155 or blue > 155:
                textcolor = '#000000'
            else:
                textcolor = '#ffffff'
            cores = select_colors_in_all_suppliers
            (red, green,blue,tabela)
            cores = cores[0]
            red1, green1, blue1 = cores[0]['red'], cores[0]['green'], cores[0]['blue']
            hexadecimal1 = cores[0]['hexadecimal']
            nome1, fornecedor1 = cores[0]['nome'], cores[0]['fornecedores']
            if red1 > 155 or green1 > 155 or blue1 > 155:
                textcolor1 = '#000000'
            else:
                textcolor1 = '#ffffff'
            red2, green2, blue2 = cores[1]['red'], cores[1]['green'], cores[1]['blue']
            hexadecimal2 = cores[1]['hexadecimal']
            nome2, fornecedor2 = cores[1]['nome'], cores[1]['fornecedores']
            if red2 > 155 or green2 > 155 or blue2 > 155:
                textcolor2 = '#000000'
            else:
                textcolor2 = '#ffffff'  
            red3, green3, blue3 = cores[2]['red'], cores[2]['green'], cores[2]['blue']
            hexadecimal3 = cores[2]['hexadecimal']
            nome3, fornecedor3 = cores[2]['nome'], cores[2]['fornecedores']
            if red3 > 155 or green3 > 155 or blue3 > 155:
                textcolor3 = '#000000'
            else:
                textcolor3 = '#ffffff'
            red4, green4, blue4 = cores[3]['red'], cores[3]['green'], cores[3]['blue']
            hexadecimal4 = cores[3]['hexadecimal']
            nome4, fornecedor4 = cores[3]['nome'], cores[3]['fornecedores']
            if red4 > 155 or green4 > 155 or blue4 > 155:
                textcolor4 = '#000000'
            else:
                textcolor4 = '#ffffff'
            red5, green5, blue5 = cores[4]['red'], cores[4]['green'], cores[4]['blue']
            hexadecimal5 = cores[4]['hexadecimal']
            nome5, fornecedor5 = cores[4]['nome'], cores[4]['fornecedores']
            if red5 > 155 or green5 > 155 or blue5 > 155:
                textcolor5 = '#000000'
            else:
                textcolor5 = '#ffffff'
            red6, green6, blue6 = cores[5]['red'], cores[5]['green'], cores[5]['blue']
            hexadecimal6 = cores[5]['hexadecimal']
            nome6, fornecedor6 = cores[5]['nome'], cores[5]['fornecedores']
            if red6 > 155 or green6 > 155 or blue6 > 155:
                textcolor6 = '#000000'
            else:
                textcolor6 = '#ffffff'
            try:              
                
                with container:
                    script = (
                        "<div style='height: 400px; width: 700px; background-color:green display:flex; flex-direction: row'>"
                            "<p style='padding: 10px '>Cor Principal</p>"
                            "<div style='background-color: {} ; height: 80px; width: 200px; padding: 0px; margin: 05px 0px 0px 0px;'>"
                                 "<p style='padding: 55px 0px 0px 05px; font-size: 16px; color: {};'>{}:{}</p>"
                            "</div>"
                            "<div style='height: 300px; width: 500px;  padding: 0px; margin:-140px 10px 0px 280px; display: flex; flex-direction: column;'>"
                                "<div style=' height: 90px; width: 500px; padding: 0px; margin: 10px 0px 0px 05px; display: flex; flex-direction: row; justify-content: space-around'>"
                                    "<div style='background-color: {} ; height: 80px; width: 230px; padding: 0px; margin: 05px 0px 0px 0px;'>"
                                        "<p style='padding: 55px 0px 0px 05px; font-size: 16px; color: {};'>{}:{}</p>"
                                    "</div>"
                                    "<div style='background-color: {} ; height: 80px; width: 230px; padding: 0px; margin: 05px 0px 0px 0px;'>"
                                        "<p style='padding: 55px 0px 0px 05px; font-size: 16px; color: {};'>{}:{}</p>"
                                    "</div>"
                                "</div>"
                                "<div style=' height: 90px; width: 500px; padding: 0px; margin: 10px 0px 0px 05px; display: flex; flex-direction: row; justify-content: space-around'>"
                                    "<div style='background-color: {} ; height: 80px; width: 230px; padding: 0px; margin: 05px 0px 0px 0px;'>"
                                        "<p style='padding: 55px 0px 0px 05px; font-size: 16px; color: {};'>{}:{}</p>"
                                    "</div>"
                                    "<div style='background-color: {} ; height: 80px; width: 230px; padding: 0px; margin: 05px 0px 0px 0px;'>"
                                        "<p style='padding: 55px 0px 0px 05px; font-size: 16px; color: {};'>{}:{}</p>"
                                    "</div>"
                                "</div>"
                                "<div style=' height: 90px; width: 500px; padding: 0px; margin: 10px 0px 0px 05px; display: flex; flex-direction: row ; justify-content: space-around'>"
                                    "<div style='background-color: {} ; height: 80px; width: 230px; padding: 0px; margin: 05px 0px 0px 0px;'>"
                                        "<p style='padding: 55px 0px 0px 05px; font-size: 16px; color: {};'>{}:{}</p>"
                                    "</div>"
                                    "<div style='background-color: {} ; height: 80px; width: 230px; padding: 0px; margin: 05px 0px 0px 0px;'>"
                                        "<p style='padding: 55px 0px 0px 05px; font-size: 16px; color: {};'>{}:{}</p>"
                                    "</div>"
                                "</div>"
                            "</div>"
                        "</div>").format(hexadecimal,textcolor,fornecedor,nome,hexadecimal1,textcolor1,fornecedor1,nome1, hexadecimal2,textcolor2,fornecedor2,nome2,hexadecimal3,textcolor3,fornecedor3,nome3, hexadecimal4,textcolor4,fornecedor4,nome4, hexadecimal5,textcolor5,fornecedor5,nome5,hexadecimal6,textcolor6,fornecedor6,nome6)
                st.markdown(script, unsafe_allow_html=True)
            except Exception as e:
                st.write("erro cores não encontradas")
                
                

def receivecolors():
    if len(st.session_state.resultados) >0:
        data = st.session_state.resultados
        container = st.container()
        st.toast('Carregando...')
        time.sleep(1.5)
        data_df = pd.DataFrame(data, index=[0])
        data = data_df.to_dict(orient='records')
        tabela = st.session_state.tables
        fornecedores = opção_fornecedores
        try:
            # Processar a cor principal
            cor_principal = data[0]
            red, green, blue = cor_principal['red'], cor_principal['green'], cor_principal['blue']
            c, m, y, k = rgb_para_cmyk(red, green, blue)
            fornecedores = cor_principal['fornecedores']
            nome = cor_principal['nome']
            hexadecimal = cor_principal['hexadecimal']
            pantone_codigo = cor_principal['pantone_código']
            ncs = cor_principal['ncs']
            # Calcular complementos
            tabela = tabela[fornecedores]
            complementos = select_complements(red, green, blue, tipo_de_paleta, tabela)
            st.session_state.complementos = complementos

            # Processar complementos
            complemento1 = complementos[0]
            redc1, greenc1, bluec1 = complemento1['red'], complemento1['green'], complemento1['blue']
            cc1, mc1, yc1, kc1 = rgb_para_cmyk(redc1, greenc1, bluec1)
            fornecedoresc1 = complemento1['fornecedores']
            nomec1 = complemento1['nome']
            hexadecimalc1 = complemento1['hexadecimal']
            pantone_codigoc1 = complemento1['pantone_código']
            ncs1 = complemento1['ncs']

            complemento2 = complementos[1]
            redc2, greenc2, bluec2 = complemento2['red'], complemento2['green'], complemento2['blue']
            cc2, mc2, yc2, kc2 = rgb_para_cmyk(redc2, greenc2, bluec2)
            fornecedoresc2 = complemento2['fornecedores']
            nomec2 = complemento2['nome']
            hexadecimalc2 = complemento2['hexadecimal']
            pantone_codigoc2 = complemento2['pantone_código']
            ncs2 = complemento2['ncs']
            # renderizar complementos
            with container:
                script = ("<div style='display: flex; flex-direction: row; justify-content: space-around; margin: 0px; padding:0px;width: 700px ;margin: 0px auto; height: 480px;'>"
                        "<div style='background-color: white ; width: 660px; height: 480px; padding: 10px;box-shadow: 2px 2px 2px 1.5px rgba(0, 0, 0, 0.25);border-radius: 10px 0px 0px 10px;'>"
                        "<div><h5 style='margin: 0px; padding:0px; color:black;'><strong>Cor principal:</strong></h5>"
                        "<div id='container' style='background-color: {}; width: 200px; height: 200px;'></div>"
                        "<p style='color:black; margin: 0px; padding:0px'>{}: {}</p>"
                        "<p style='color:black;margin: 0px; padding:0px;'>Pantone: {}</p>"
                        "<p style='color:black;margin: 0px; padding:0px'>NCS: {}</p>"
                        "<p style='color:black;margin: 0px; padding:0px'>RGB: {},{},{} </p>"
                        "<p style='color:black;margin: 0px; padding:0px'>Cyan: {:.2f}<br>Magenta: {:.2f}<br>Yellow: {:.2f}<br>Key: {:.2f}</p>"
                        "</div></div>"
                        "<div style='background-color: white ; width: 660px; height: 480px; padding: 10px;"
                        "box-shadow: 2px 2px 2px 1.5px rgba(0, 0, 0, 0.25);'>"
                        "<div><h5 style='color:black;margin: 0px; padding:0px'>Cor secundária 1:</h5>"
                        "<div id='container' style='background-color: {}; width: 200px; height: 200px;'></div>"
                        "<p style='color:black; margin: 0px; padding:0px'>{}: {}</p>"
                        "<p style='color:black;margin: 0px; padding:0px;'>Pantone: {}</p>"
                        "<p style='color:black;margin: 0px; padding:0px'>NCS: {}</p>"
                        "<p style='color:black;margin: 0px; padding:0px'>RGB: {},{},{} </p>"
                        "<p style='color:black;margin: 0px; padding:0px'>Cyan: {:.2f}<br>Magenta: {:.2f}<br>Yellow: {:.2f}<br>Key: {:.2f}</p>"
                        "</div></div>"
                        "<div style='background-color: white ; width: 660px; height: 480px; padding: 10px;"
                        "box-shadow: 2px 2px 2px 1.5px rgba(0, 0, 0, 0.25);border-radius: 0px 10px 10px 0px;'>"
                        "<div><h5 style='margin: 0px; padding:0px; color:black;'>Cor secundária 2:</h5>"
                        "<div id='container' style='background-color: {}; width: 200px; height: 200px;'></div>"
                        "<p style='color:black; margin: 0px; padding:0px'>{}: {}</p>"
                        "<p style='color:black;margin: 0px; padding:0px;'>Pantone: {}</p>"
                        "<p style='color:black;margin: 0px; padding:0px'>NCS: {}</p>"
                        "<p style='color:black;margin: 0px; padding:0px'>RGB: {},{},{} </p>"
                        "<p style='color:black;margin: 0px; padding:0px'>Cyan: {:.2f}<br>Magenta: {:.2f}<br>Yellow: {:.2f}<br>Key: {:.2f}</p>"
                        "</div></div></div>").format(
                    hexadecimal, fornecedores, nome, pantone_codigo, ncs, red, green, blue, c, m, y, k,
                    hexadecimalc1, fornecedoresc1, nomec1, pantone_codigoc1,ncs1, redc1, greenc1, bluec1, cc1, mc1, yc1, kc1,
                    hexadecimalc2, fornecedoresc2, nomec2, pantone_codigoc2,ncs2, redc2, greenc2, bluec2, cc2, mc2, yc2, kc2)
                st.markdown(script, unsafe_allow_html=True)
        except Exception as e:

            st.write("Nenhuma cor encontrada")



# Interface do usuário
st.title('Find Me')
st.subheader('Onde você acha sua cor')

with st.expander("Tire sua foto"):
    camera = st.camera_input(label = "Use a camera para capturar a cor ")
img_file = st.file_uploader(label = "Carregue uma imagem", type=['png', 'jpg', 'jpeg'], accept_multiple_files=False)
realtime_update = True


aspect_choice = "1:1"
aspect_dict = {
    "1:1": (1, 1), 
    "16:9": (16, 9),
    "4:3": (4, 3),
    "2:3": (2, 3),
    "Nenhum": None
}
aspect_ratio = aspect_dict[aspect_choice]

modo = st.selectbox('Modo', options=("Args de Paletas","Comparação de Marcas"))
if modo == "Args de Paletas":
    opção_fornecedores = st.selectbox('Marcas de tinta', options=('todos', 'coral', 'suvinil', 'sherwin-willians','anjo'))
    tipo_de_paleta = st.selectbox('Paletas', options=('triade', 'complementar', 'análoga'))
    filtros = st.selectbox('Filtros', options=("Luz Fria","Luz Neutra","Luz Quente"))
    args = st.text_input('Digite o nome da cor, o código Pantone (00-0000) ou o hexadecimal (#000000):')
    iluminação = st.slider('Iluminação', min_value=0.0, max_value=1.0, value=1.0, step=0.1)
    change_color = st.button("Alterar cor da caixa" , on_click=mudar_cor_da_caixa)
    box_color = st.session_state.cor

    # luz quente 2700, luz neutra 4000, luz fria 6500, luz fria é branca
    if img_file:
            img = image2.open(img_file)   
            # Get a cropped image from the frontend
            cropped_img = st_cropper(img, realtime_update=realtime_update, box_color=box_color,
                                        aspect_ratio=aspect_ratio)    
            # Manipulate cropped image at will
            st.write("Prévia")

            _ = cropped_img.thumbnail((150,150))
            st.image(cropped_img)
            if cropped_img:
                enhancer = ImageEnhance.Brightness(cropped_img)
                enhancer.enhance(iluminação).save("image/cropped.png")    

                find_rgb_value(args, "image/cropped.png", camera, opção_fornecedores,filtros)


    elif camera:
            foto = image2.open(camera)
            if not realtime_update:
                st.write("Clique duas vezes para cortar a imagem")
            # Get a cropped image from the frontend
            edited_foto = st_cropper(foto, realtime_update=realtime_update, box_color=box_color,
                                        aspect_ratio=aspect_ratio)    
            # Manipulate cropped image at will
            st.write("Prévia")
            _ = edited_foto.thumbnail((150,150))
            st.image(edited_foto)
            if edited_foto:
                enhancer = ImageEnhance.Brightness(edited_foto)
                enhancer.enhance(iluminação).save("image/cropped.png")

                find_rgb_value(args, img_file, "image/cropped.png", opção_fornecedores,filtros)
    elif args:
        tabela = st.session_state.tables 
        st.write(tabela['todos'])
        find_rgb_value(args, None, None, opção_fornecedores,filtros)

    receivecolors()
    
    
if modo == "Comparação de Marcas":
    fornecedores = st.selectbox('Marcas de tinta', options=('todos', 'coral', 'suvinil', 'sherwin-willians','anjo'))
    argsr_marcas = st.text_input('Digite o nome da cor, o código Pantone (00-0000) ou o hexadecimal (#000000):')
    realtime_update = True

    aspect_choice = "1:1"
    aspect_dict = {
        "1:1": (1, 1), 
        "16:9": (16, 9),
        "4:3": (4, 3),
        "2:3": (2, 3),
        "Nenhum": None
    }
    aspect_ratio = aspect_dict[aspect_choice]
    iluminação = st.slider('Iluminação', min_value=0.0, max_value=1.0, value=1.0, step=0.1)
    change_color_button = st.button("Alterar cor da caixa" , on_click=mudar_cor_da_caixa)
    box_color = st.session_state.cor
    if img_file:
            img = image2.open(img_file)
            cropped_img = st_cropper(img, realtime_update=realtime_update, box_color=box_color,
                                        aspect_ratio=aspect_ratio)           

            st.write("Prévia")
            _ = cropped_img.thumbnail((150,150))
            st.image(cropped_img)
            if cropped_img:
                enhancer = ImageEnhance.Brightness(cropped_img)
                enhancer.enhance(iluminação).save("image/cropped.png")
                encontrar_cor_similar("image/cropped.png", None, fornecedores)

    elif argsr_marcas:
            encontrar_cor_similar(None, argsr_marcas, fornecedores)
    show_similar_colors()
