def search_name_for_id(nome):
    with open ("search/search_dict.json", "r") as file:
        search_dict = json.load(file)
        print (search_dict)
        if nome in search_dict:
             return search_dict[nome]
        else:
            return None