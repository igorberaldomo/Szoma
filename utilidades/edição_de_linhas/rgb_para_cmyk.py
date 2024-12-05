def rgb_para_cmyk(r, g, b):
    escala_RGB = 255
    excala_cmyk = 100
    if (r, g, b) == (0, 0, 0):
        # black
        return 0, 0, 0, excala_cmyk

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / escala_RGB
    m = 1 - g / escala_RGB
    y = 1 - b / escala_RGB

    # extract out k [0, 1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    # rescale to the range [0,excala_cmyk]
    return c * excala_cmyk, m * excala_cmyk, y * excala_cmyk, k * excala_cmyk
