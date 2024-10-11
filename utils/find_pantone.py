def findpant(r,g,b):
    with open('pantone.json','r+') as file:
        file_data = json.load(file)
    maxr = r+32
    minr = r-32
    maxg = g+32
    ming = g-32
    maxb = b+32
    minb = b-32
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
                    if f"#{hexa}" in file_data:
                        pantone = file_data[f"#{hexa}"]
                        print(file_data[f"#{hexa}"])
                        return pantone
                        break
                    else:
                        continue
