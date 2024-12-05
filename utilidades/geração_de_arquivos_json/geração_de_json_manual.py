from colorthief import ColorThief
import json


fornecedores = 'anjo'
def encontrar_rgb(hexadecimal):
    hexadecimal = hexadecimal.replace('#', '')
    r = int(hexadecimal[0:2], 16)
    g = int(hexadecimal[2:4], 16)
    b = int(hexadecimal[4:6], 16)
    return r,g,b

with open ("sherwin-williams.json", "r+") as file:
    file_data = json.load(file)
    c = 0
    while c < len(file_data):
        nome = file_data[c]['name']

        # ncs = '8301-Y97R'
        # código_suvinil = 'm167'
        red,green,blue = encontrar_rgb(file_data[c]['hex'])

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

        # nome = formatnome(nome)


        data['nome'] = nome
        data['rgb'] = red,green,blue
        # data['ncs'] = ncs.upper()
        # data['codigo_suvinil'] = código_suvinil.upper()
        # hexa = f'{red:02x}{green:02x}{blue:02x}'
        data['hexadecimal'] = file_data[c]['hex']
        def findpant(r,g,b):
            with open('pantone/pantone.json','r+') as file:
                file_data = json.load(file)
            nearest_pantone = list() 
            maxr = r+30
            minr = r-30
            maxg = g+30
            ming = g-30
            maxb = b+30
            minb = b-30
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
                            nearest_pantone.append(file_data['corespantone'][f"#{hexa}"])
                        else:
                            continue
            c = 0
            pantone = {}
            min_dif = 0
            print(nearest_pantone[c]['hex'])
            for c in range(len(nearest_pantone)):
                hexadecimal = nearest_pantone[c]['hex']
                h = hexadecimal.lstrip('#')
                red_hex, green_hex, blue_hex = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
                
                dif_red = red_hex - red
                dif_green = green_hex - green
                dif_blue = blue_hex - blue
                
                if dif_red < 0:
                    dif_red = dif_red * -1
                if dif_green < 0:
                    dif_green = dif_green * -1
                if dif_blue < 0:
                    dif_blue = dif_blue * -1
                    
                total_dif = dif_red + dif_green + dif_blue
                if c == 0 :
                    min_dif = total_dif
                    pantone = nearest_pantone[c]
                if total_dif < min_dif:
                    min_dif = total_dif
                    pantone = nearest_pantone[c]
                c += 1
            return pantone
                                
        pant = findpant(red, green, blue)
        data['pantone'] = pant
        data['fornecedor'] = fornecedores 


        def write_json(new_data, filename='sherwin-willians_2.json'):
            with open(filename,'r+') as file:
                file_data = json.load(file)
                # Join new_data with file_data inside emp_details
                file_data["cores-sherwin-willians"].append(new_data)
                # Sets file's current position at offset.
                file.seek(0)
                # convert back to json.
                json.dump(file_data, file, indent = 4)
        write_json(data)
        c += 1
print(data)
