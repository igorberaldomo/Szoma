def filtrar_linhas_necessárias(table):
    data = []
    i = 0
    for i in range(len(table)):
        data.append(
            {
                "nome": table[i]["nome"],
                "hexadecimal": table[i]["hexadecimal"],
                "fornecedores": table[i]["fornecedores"],
                "pantone_código": table[i]["pantone_código"],
                "pantone_name": table[i]["pantone_name"],
                "pantone_hexadecimal": table[i]["pantone_hex"],
                "ncs": table[i]["ncs"],
                "red": table[i]["red"],
                "green": table[i]["green"],
                "blue": table[i]["blue"],
            }
        )
        i += 1
    return data