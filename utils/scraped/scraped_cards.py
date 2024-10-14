
#  essa era uma função para adicionar card em html estilizados pelo streamlit, o problema é que a função st.html não esta alocando height de acordo com o tamanho dos componentes
def scrapedcards(data):
    c= 0
    # outro método
    while c < len(data)-1:
        nome = str(data[c]['nome'])
        hexa = str(data[c]['hexadecimal'])
        pantone_name = str(data[c]['pantone_name'])
        pantone_hex = str(data[c]['pantone_hex'])
        st.html("<style>.container { width: 100%; height: 200px; position: absolute; display: flex; flex-direction: row; justify-content: space-between; background-color: gray; } .fornecedor { width: 300px; height: 200px; background-color: " + hexa + ";padding: 5px;border-radius: 10px; }.pantone {width: 300px;height: 200px;background-color: " + pantone_hex + ";border-radius: 10px;}</style><div class='container'><div class='fornecedor'>"+nome+"</div><div class='pantone'>"+pantone_name+"</div></div>")
    c+=1