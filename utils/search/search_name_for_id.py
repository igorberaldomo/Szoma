import json

def search_name_for_id(nome):
    with open("search/search_dict.json", "r") as file:
        nome  = f'"{nome}"'
        search_dict = json.load(file)
        select_id = 0
        for local in search_dict["quickSearch"][0].keys():
            for keys in search_dict["quickSearch"][local]:
                if nome in keys:
                    return keys[nome]
      
        print(select_id)
    return select_id
