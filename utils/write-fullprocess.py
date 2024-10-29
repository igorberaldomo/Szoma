from colorthief import ColorThief
import json

nome = 'carvão'
ncs = '8301-Y97R'
código_suvinil = 'm167'
red = 77
green = 74
blue = 73

data = dict()
# function to add to JSON

# formats name variable
def formatnome(cor):
    tempnome = cor.replace(' ', '_')
    tempnome = tempnome.replace('á','a').replace('ã','a').replace('â','a')
    tempnome = tempnome.replace('é', 'e').replace('ê','e')
    tempnome = tempnome.replace('í','i')
    tempnome = tempnome.replace('õ','o').replace('ô', 'o').replace('ó','o')
    nome = tempnome.replace('ç','c').replace('ú','u').replace('=','-')
    return nome

nome = formatnome(nome)


data['nome'] = nome
data['rgb'] = red,green,blue
data['ncs'] = ncs.upper()
data['codigo_suvinil'] = código_suvinil.upper()
hexa = f'{red:02x}{green:02x}{blue:02x}'
data['hexadecimal'] = f"#{hexa}"
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
                
pant = findpant(red, green, blue)
data['pantone'] = pant
data['loja'] = 'suvenil'
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
