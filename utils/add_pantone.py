from colorthief import ColorThief
import json
data_with_pantone = list()
new_data = dict()
def findpant(r,g,b):
    with open('pantone.json','r+') as file2:
        pantone_file_data = json.load(file2)
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
                    if f"#{hexa}" in pantone_file_data['corespantone']:
                        pantone = pantone_file_data['corespantone'][f"#{hexa}"]  
                        return  pantone
                        break
       
    
def write_json(new_data, filename='suvenil_with_pantone.json'):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["coressuvinil"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
        
with open('suvenil.json', 'r') as file:
    filedata = json.load(file)
    c = 0
    while c < len(filedata['coressuvinil'][0]):
        new_data['nome'] = filedata['coressuvinil'][0][c]['nome']
        new_data['rgb'] = filedata['coressuvinil'][0][c]['rgb']
        new_data['ncs'] = filedata['coressuvinil'][0][c]['ncs']
        new_data['codigo'] = filedata['coressuvinil'][0][c]['codigo_suvinil']
        new_data['hexadecimal'] = filedata['coressuvinil'][0][c]['hexadecimal']
        r = filedata['coressuvinil'][0][c]['rgb'][0]
        g = filedata['coressuvinil'][0][c]['rgb'][1]
        b = filedata['coressuvinil'][0][c]['rgb'][2]
        new_data['pantone'] = findpant(r,g,b)
        new_data['fornecedores'] = filedata['coressuvinil'][0][c]['loja']
        write_json(new_data)
        c+=1
        



        



