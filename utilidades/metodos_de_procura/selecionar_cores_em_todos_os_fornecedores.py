
def selecionar_cores_em_todos_os_fornecedores(red, green,blue,suvinil):
    lista_cores_final = []
    desvio = 30
    tem_resultados = False
    minimo_vermelho = red - desvio
    maximo_vermelho = red + desvio
    minimo_verde = green - desvio
    maximo_verde = green + desvio
    minimo_azul = blue - desvio
    maximo_azul = blue + desvio

    if minimo_vermelho < 0:
        minimo_vermelho = 0
    if maximo_vermelho > 255:
        maximo_vermelho = 255
    if minimo_verde < 0:
        minimo_verde = 0
    if maximo_verde > 255:
        maximo_verde = 255
    if minimo_azul < 0:
        minimo_azul = 0
    if maximo_azul > 255:
        maximo_azul = 255
    
    resultados = list
    suvinil = tabela["suvinil"]
    # busca na tabela suvinil
    c = 0
    for c in range(len(suvinil)):
        if suvinil[c]['red'] >= minimo_vermelho and suvinil[c]['red'] <= maximo_vermelho and suvinil[c]['green'] >= minimo_verde and suvinil[c]['green'] <= maximo_verde and suvinil[c]['blue'] >= minimo_azul and suvinil[c]['blue'] <= maximo_azul: 
            st.write(suvinil[c])
            resultados.append(suvinil[c])
        c += 1
    # busca na tabela coral
    c = 0
    coral = tabela["coral"]
    for c in range(len(coral)):
        if coral[c]['red'] >= minimo_vermelho and coral[c]['red'] <= maximo_vermelho and coral[c]['green'] >= minimo_verde and coral[c]['green'] <= maximo_verde and coral[c]['blue'] >= minimo_azul and coral[c]['blue'] <= maximo_azul:
            st.write(suvinil[c])
            resultados.append(coral[c])
        c += 1

     # busca na tabela anjo
    c = 0
    anjo = tabela["anjo"]
    for c in range(len(anjo)):
        if anjo[c]['red'] >= minimo_vermelho and anjo[c]['red'] <= maximo_vermelho and anjo[c]['green'] >= minimo_verde and anjo[c]['green'] <= maximo_verde and anjo[c]['blue'] >= minimo_azul and anjo[c]['blue'] <= maximo_azul: 
            st.write(suvinil[c])
            resultados.append(anjo[c])
        c += 1
    # busca na tabela sherwin-willians
    c = 0
    sherwin_willians = tabela["sherwin-willians"]
    for c in range(len(anjo)):
        if sherwin_willians[c]['red'] >= minimo_vermelho and sherwin_willians[c]['red'] <= maximo_vermelho and sherwin_willians[c]['green'] >= minimo_verde and sherwin_willians[c]['green'] <= maximo_verde and sherwin_willians[c]['blue'] >= minimo_azul and sherwin_willians[c]['blue'] <= maximo_azul: 
            st.write(suvinil[c])
            resultados.append(sherwin_willians[c])
        c += 1
    
    if len(resultados) == 0:
        tem_resultados = False
    else:
        tem_resultados = True
    
    c = 0
    for c in range(len(resultados)):
        lista_cores_final.append(resultados[c])
        c += 1
    st.write(lista_cores_final)
    return lista_cores_final