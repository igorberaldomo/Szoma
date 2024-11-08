# devido a limitação do st.button esse código não pode ser transferido na integra

def findrgb(upload,procura,opcao_fornecedores,tipo_de_palheta):
    if  procura is not None and upload is not None :
        if upload is not None:
            st.session_state.cliked = True
            ct = colorthief.ColorThief(upload)
            cor = ct.get_color(quality=1)
            response = requests.post("http://localhost:5555/suvinil/",json=cor)
            data = response.json()
            return data
        else:
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