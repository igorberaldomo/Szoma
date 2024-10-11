def formatnome(cor):
    ponto = cor.find('.')
    sliceposition = slice(0, ponto, 1)
    tempnome = (cor[sliceposition]).replace('_', ' ')
    tempnome = tempnome.replace('á','a').replace('ã','a').replace('â','a')
    tempnome = tempnome.replace('é', 'e').replace('ê','e')
    tempnome = tempnome.replace('í','i')
    tempnome = tempnome.replace('õ','o').replace('ô', 'o').replace('ó','o')
    nome = tempnome.replace('ç','c').replace('ú','u')
    return nome