from colorthief import ColorThief
import json


data = dict()
lista_hexa = list()

def por_acentos(nome):
    with open("lista_acentos_suvinil.json", "r+") as acentos:
        acentosdata = json.load(acentos)
        x = 0 # contador do acento
        while x < len(acentosdata["checklist"]):
            if acentosdata["checklist"][x]["modificado"] in nome:
                nome = nome.replace(
                    acentosdata["checklist"][x]["modificado"],
                    acentosdata["checklist"][x]["original"],
                )
            x+=1
        nome = nome.replace("_", " ")
        print(nome)
    return nome


def write_json(new_data, filename="suvinil2.json"):
    with open(filename, "r+") as file:
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["coressuvinil"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)

def findpant(r, g, b):
    with open("pantone/pantone.json", "r+") as file:
        file_data = json.load(file)
    maxr = r + 32
    minr = r - 32
    maxg = g + 32
    ming = g - 32
    maxb = b + 32
    minb = b - 32
    if maxr > 255:
        maxr = 255
    if minr < 0:
        minr = 0
    if maxg > 255:
        maxg = 255
    if ming < 0:
        ming = 0
    if maxb > 255:
        maxb = 255
    if minb < 0:
        minb = 0
    for red in range(minr, maxr):
        for green in range(ming, maxg):
            for blue in range(minb, maxb):
                hexa = f"{red:02x}{green:02x}{blue:02x}"
                if f"#{hexa}" in file_data["corespantone"]:
                    lista_hexa.append(hexa)
                else:
                    continue            
    c = 0
    while c < len(lista_hexa):
        vermelho = int(lista_hexa[c][0:2], 16)
        verde = int(lista_hexa[c][2:4], 16)
        azul = int(lista_hexa[c][4:6], 16)
        diferença_vermelho = r - vermelho
        diferença_verde = g - verde
        diferença_azul = b - azul
        if diferença_vermelho < 0:
            diferença_vermelho = diferença_vermelho * -1
        if diferença_verde < 0:
            diferença_verde = diferença_verde * -1
        if diferença_azul < 0:
            diferença_azul = diferença_azul * -1
        total = diferença_vermelho + diferença_verde + diferença_azul
        if c == 0:
            pant = lista_hexa[0]
            menor_total = total
        if total < menor_total:
            menor_total = total
            pant = lista_hexa[c]
        c += 1
    return pant

with open("suvinil/suvinil.json", "r+") as file:
    suvinildata = json.load(file)
    c = 0 # posição do dicionário
    while c < len(suvinildata["coressuvinil"]):
        tempnome = suvinildata["coressuvinil"][c]["nome"]
        data["nome"] = por_acentos(tempnome)
        red = suvinildata["coressuvinil"][c]["rgb"][0]
        green = suvinildata["coressuvinil"][c]["rgb"][1]
        blue = suvinildata["coressuvinil"][c]["rgb"][2]
        print(red, green, blue)
        data["rgb"] = (red, green, blue)
        data["ncs"] = suvinildata["coressuvinil"][c]["ncs"]
        data["codigo_suvinil"] = suvinildata["coressuvinil"][c]["codigo"]
        hexa = f"{red:02x}{green:02x}{blue:02x}"
        data["hexadecimal"] = f"#{hexa}"
        pant = findpant(red, green, blue)
        with open("pantone/pantone.json", "r+") as pantone:
            file_data = json.load(pantone)
        data["pantone"] = file_data["corespantone"][f"#{pant}"]
        data["fornecedores"] = "suvinil"
        write_json(data)
        c += 1
      





