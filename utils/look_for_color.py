def lookforcolor(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    distancia = 36
    maxred = red + distancia
    minred = red - distancia
    maxgreen = green + distancia
    mingreen = green - distancia
    maxblue = blue + distancia
    minblue = blue - distancia
    if maxred > 255:
        maxred = 255
    if minred < 0:
        minred = 0
    if maxgreen > 255:
        maxgreen = 255
    if mingreen < 0:
        mingreen = 0
    if maxblue > 255:
        maxblue = 255
    if minblue < 0:
        minblue = 0
    for red in range(minred, maxred):
        for green in range(mingreen, maxgreen):
            for blue in range(minblue, maxblue):
                hexa = f'{red:02x}{green:02x}{blue:02x}'
                print(f"#{hexa}")