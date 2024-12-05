import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from streamlit_cropper import st_cropper
from PIL import Image as image2
from PIL import ImageEnhance
from colorthief import ColorThief
from utilidades.edição_de_linhas.rgb_para_cmyk import rgb_para_cmyk
from utilidades.metodos_de_procura.selecionar_complementos import selecionar_complementos
from utilidades.metodos_de_procura.procurar_hexadecimal import procurar_hexadecimal
from utilidades.metodos_de_procura.procurar_códigos import procurar_códigos
from utilidades.metodos_de_procura.procurar_o_nome_para_obter_a_id import procurar_o_nome_para_obter_a_id
from utilidades.metodos_de_procura.selecionar_cor_principal import selecionar_cor_principal
from utilidades.conecções.método_de_conecção_produção import método_de_conecção_produção



# Inicializar o estado da sessão
if "resultados" not in st.session_state:
    st.session_state.resultados = []
if "complementos" not in st.session_state:
    st.session_state.complementos = []
if "tabelas" not in st.session_state:
    st.session_state.tabelas = []
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
def buscar_dados_do_banco():
    engine = método_de_conecção_produção()
    procuras = {
    "suvinil": "SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil",
    "coral": "SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral",
    # dentro so metodos_de_procura parameters note que está escrito sherwin_wilians em vez de sherwin-willians, está correto o SQL não faz busca com o caractere '-' então foi substituido de propósito por '_'
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
    
    for nome_tabela, procura in procuras.items():
        try:
            df = pd.read_sql(procura, engine)
        except Exception as e:
            print(f"Erro ao processar a tabela {nome_tabela}: {e}")
            continue
        
        try:
            if nome_tabela in ['suvinil', 'coral', 'sherwin-willians', 'anjo', 'todos']:
                df['fornecedores'] = df['fornecedores'].astype(str)
                df['hexadecimal'] = df['hexadecimal'].astype(str)
                df['nome']  = df['nome'].astype(str)
                df['ncs'] = df['ncs'].astype(str)
                df['codigo_suvinil'] = df['codigo_suvinil'].astype(str)
                df['pantone_código'] = df['pantone_código'].astype(str)
                df['red'] = df['red'].astype(int)
                df['green'] = df['green'].astype(int)
                df['blue'] = df['blue'].astype(int)    
            dataframes[nome_tabela] = df.copy(deep=True)
        except Exception as e:
            print(f"Erro ao processar a tabela {nome_tabela}: {e}")
    return dataframes
# para acessar tabela use table['nome_da_tabela']
tabelas = buscar_dados_do_banco()
st.session_state.tabelas = tabelas 

def encontrar_cor_similar(caminho_para_imagem, procura):
    if procura is not None:
        fornecedores = opcao_fornecedores
        if procura[0].isalpha():
            nome = procura
            # para essa função os fornecedores serão determinados dentro da função sendo necessário passar todas as tabelas
            tabela = st.session_state.tabelas
            resultados = procurar_o_nome_para_obter_a_id(nome,tabela)
            st.session_state.resultados = resultados
        if procura[0].isnumeric():
            codigo = procura
            tabela = st.session_state.tabelas

        if procura[0] == '#':
            hexadecimal = procura
            tabela = st.session_state.tabelas
    elif caminho_para_imagem is not None:
        ct = ColorThief(caminho_para_imagem)
        cor = ct.get_color(quality=1)
        red, green, blue = cor
        fornecedores = opcao_fornecedores
        tabela = st.session_state.tabelas
        tabela = tabela[fornecedores]
        dataframe_da_resposta = selecionar_cor_principal(red, green, blue, tabela)
        st.session_state.resultados = dataframe_da_resposta
    else:
        st.write('Não foi colocado uma imagem ou um valor para procurar a cor')
        
def mudar_cor_da_caixa():
    if st.session_state.cor == '#ffffff':
        st.session_state.cor = '#000000'
    else:
        st.session_state.cor = '#ffffff'

def encontrar_valor_rgb(procura,upload,camera ,opcao_fornecedores):
    st.session_state.resultados = []
    if procura or upload or camera:
        if upload is not None:
            ct = ColorThief(upload)
            cor = ct.get_color(quality=1)
            red, green, blue = cor
            st.write(red,green,blue)
            fornecedores = opcao_fornecedores
            tabela = st.session_state.tabelas
            tabela = tabela[fornecedores]
            dataframe_da_resposta = selecionar_cor_principal(red, green, blue, tabela)
            if dataframe_da_resposta.empty:
                st.text('Erro imagem desfocada, selecione outra imagem')
            else:
                st.session_state.resultados = dataframe_da_resposta
        elif camera is not None:
            ct = ColorThief(camera)
            cor = ct.get_color(quality=1)
            red, green, blue = cor
            fornecedores = opcao_fornecedores
            tabela = st.session_state.tabelas
            tabela = tabela[fornecedores]
            dataframe_da_resposta = selecionar_cor_principal(red, green, blue, tabela)
            if dataframe_da_resposta.empty:
                st.text('Erro imagem desfocada, tire outra foto')
            else:
                st.session_state.resultados = dataframe_da_resposta
    elif procura is not None:
        fornecedores = opcao_fornecedores
        if procura[0].isalpha():
            nome = procura
            # para essa função os fornecedores serão determinados dentro da função sendo necessário passar todas as tabelas
            tabela = st.session_state.tabelas
            dataframe_da_resposta = procurar_o_nome_para_obter_a_id(nome, tabela)
            st.session_state.resultados = dataframe_da_resposta
        if procura[0].isnumeric():
            codigo = procura
            tabela = st.session_state.tabelas
            tabela = tabela[fornecedores]
            dataframe_da_resposta = procurar_códigos(codigo, tabela)
            st.session_state.resultados = dataframe_da_resposta
        if procura[0] == '#':
            hexadecimal = procura
            tabela = st.session_state.tabelas
            tabela = tabela[fornecedores]
            dataframe_da_resposta = procurar_hexadecimal(hexadecimal, tabela)
            st.session_state.resultados = dataframe_da_resposta
    else:
        st.text('Por favor, insira uma imagem ou um valor para procurar a cor')


            
def receivecolors(modo):
    if modo == 'Procura de palhetas':
        if len(st.session_state.resultados) > 0:
            data = st.session_state.resultados
            cores_df = pd.DataFrame(data)
            container = st.container()
            st.toast('Carregando...')
            time.sleep(1.5)
            data_df = pd.DataFrame(data, index=[0])
            data = data_df.to_dict(orient='records')
            tabela = st.session_state.tabelas
            fornecedores = opcao_fornecedores
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
                complementos = select_complementos(red, green, blue, tipo_de_palheta, tabela)
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
                st.write(f"Erro: {e}")
        else:
            st.write("Nenhuma cor encontrada")
    elif modo == "Comparação de Marcas":
            if len(st.session_state.resultados) > 0:
                data = st.session_state.resultados
                cores_df = pd.DataFrame(data)
                container = st.container()
                st.toast('Carregando...')
                time.sleep(1.5)
                data_df = pd.DataFrame(data, index=[0])
                data = data_df.to_dict(orient='records')
                tabela = st.session_state.tabelas
                fornecedores = opcao_fornecedores
            


# Interface do usuário
st.title('Find Me')
st.subheader('Onde você acha sua cor')
with st.container():
    camera = st.camera_input(label = "Use a camera para capturar a cor ou carregue uma imagem abaixo")
    img_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], accept_multiple_files=False)
realtime_update = True
change_color = st.button("Alterar cor da caixa" , on_click=mudar_cor_da_caixa)
box_color = st.session_state.cor
aspect_choice = "1:1"
aspect_dict = {
    "1:1": (1, 1),
    "16:9": (16, 9),
    "4:3": (4, 3),
    "2:3": (2, 3),
    "Nenhum": None
}
aspect_ratio = aspect_dict[aspect_choice]

modo = st.selectbox('Modo', options=("Procura de Palhetas","Comparação de Marcas"))
if modo == "Procura de Palhetas":
    opcao_fornecedores = st.selectbox('Marcas de tinta', options=('todos', 'coral', 'suvinil', 'sherwin-willians','anjo'))
    tipo_de_palheta = st.selectbox('Palhetas', options=('triade', 'complementar', 'análoga'))
    procura = st.text_input('Digite o nome da cor, o código Pantone (00-0000) ou o hexadecimal (#000000):')
    filtros = st.selectbox('Filtros', options=("luz quente", "luz neutra", "luz fria"))
    iluminação = st.slider('Iluminação', min_value=0.0, max_value=1.0, value=1.0, step=0.1)
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
                    
                encontrar_valor_rgb(procura, "image/cropped.png", camera, opcao_fornecedores)

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
                encontrar_valor_rgb(procura, img_file, "image/cropped.png", opcao_fornecedores)
    elif procura:
            encontrar_valor_rgb(procura, None, None, opcao_fornecedores)
if modo == "Comparação de Marcas":
    procura = st.text_input('Digite o nome da cor, o código Pantone (00-0000) ou o hexadecimal (#000000):')
    iluminação = st.slider('Iluminação', min_value=0.0, max_value=1.0, value=1.0, step=0.1)
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
                encontrar_cor_similar("image/cropped.png", procura )
receivecolors(modo)
