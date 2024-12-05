def procurar_o_codigo_para_obter_a_id(codigo, tabela):
    with open("procura/dicionário_procura_codigo_id.json", "r") as file:
        search_dict = json.load(file)
        codigo_id = -1
        resultset = list()
        # procura no json o id da cor que bate com o codigo digitado assim como a tabela que ela pertence
        if codigo_id == -1:
            for keys in search_dict["quickSearch"][0]:
                if codigo in keys:
                    codigo_id = search_dict["quickSearch"][0][codigo]
                    tabela_escolida = tabela["coral"]      
        if codigo_id == -1 :
            for keys in search_dict["suvinil"][0]:
                if codigo in keys:
                    codigo_id = search_dict["suvinil"][0][codigo]
                    tabela_escolida = tabela["suvinil"]   
        if codigo_id == -1:
            for keys in search_dict["sherwin-willians"][0]:
                if codigo in keys:
                    codigo_id = search_dict["sherwin-willians"][0][codigo]
                    tabela_escolida = tabela["sherwin-willians"]   
        if codigo_id == -1:
            for keys in search_dict["anjo"][0]:
                if codigo in keys:
                    codigo_id = search_dict["anjo"][0][codigo]
                    tabela_escolida = tabela["anjo"]   
        if codigo_id == -1:
            for keys in search_dict["coral"][0]:
                if codigo in keys:
                    codigo_id = search_dict["coral"][0][codigo]
                    tabela_escolida = tabela["coral"]   
        # o metodo iloc mantem a posição original da tabela, nós precisamos que ele esteja na posição 0 para para executar as procuras, então desfazemos as posições pegamos os dados e refazemos a tabela
        resultset = tabela_escolida.iloc[[codigo_id]]
        resultset = resultset.to_dict(orient='records')
        resultset = {k:[v] for k,v in resultset[0].items()}
        resultset_df = pd.DataFrame(resultset)
        return resultset
