from colorthief import ColorThief
import json

cor = 'cabare.png'
data = dict()
nome = ''


def findpant(r,g,b):
    with open('pantone.json','r+') as file:
        file_data = json.load(file)
    maxr = r+64
    minr = r-64
    maxg = g+64
    ming = g-64
    maxb = b+64
    minb = b-64
    if maxr > 255:
        maxr = 255
    if minr < 0:
        minr = 0
    if maxg > 255:
        maxg = 255
    if ming < 0:
        ming = 0
    if  maxb > 255:
        maxb  = 255
    if minb < 0:
        minb = 0
    for red in range(minr, maxr):
        for green in range(ming, maxg):
            for blue in range(minb, maxb):
                hexa = f'{red:02x}{green:02x}{blue:02x}'
                if f"#{hexa}" in file_data['corespantone']:
                    pantone = file_data['corespantone'][f"#{hexa}"]
                    return pantone
                else:
                    continue
                    
# formats name variabledef formatnome(cor):
def formatnome(cor):
    tempnome = cor.replace(' ', '_')
    tempnome = tempnome.replace('á','a').replace('ã','a').replace('â','a')
    tempnome = tempnome.replace('é', 'e').replace('ê','e')
    tempnome = tempnome.replace('í','i')
    tempnome = tempnome.replace('õ','o').replace('ô', 'o').replace('ó','o')
    nome = tempnome.replace('ç','c').replace('ú','u').replace('=','-')
    return nome

nome = formatnome(cor)

local = cor.find('.')
nome = cor[0:local]

ct = ColorThief(cor)
dominant_color = ct.get_color(quality=1)
color = dominant_color

data['nome'] = nome
data['rgb'] = color[0], color[1], color[2]
hexa = f'{color[0]:02x}{color[1]:02x}{color[2]:02x}'
data['hexadecimal'] = f"#{hexa}"
r = int(color[0])
g = int(color[1])
b = int(color[2])

pant = findpant(r,g,b)
data['pantone'] = pant
data['fornecedores'] = 'coral'
# fornecedor

def write_json(new_data, filename='coral.json'):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["corescoral"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
write_json(data)


print(data)
