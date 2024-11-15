import json

def search_name_for_id(nome):
    with open("search/search_dict.json", "r") as file:
        nome  = f'"{nome}"'
        search_dict = json.load(file)
        select_id = 0
        for keys in search_dict["quickSearch"][0].keys():
            for nome in values[k]:
                if searchFor in nome:
                    return keys
        for keys in search_dict["suvinil"][0].keys():
            for nome in values[k]:
                if searchFor in nome:
                    return keys
        for keys in search_dict["coral"][0].keys():
            for nome in values[k]:
                if searchFor in nome:
                    return keys
        for keys in search_dict["sherwin-willians"][0].keys():
            for nome in values[k]:
                if searchFor in nome:
                    return keys
        print(select_id)
    return select_id
