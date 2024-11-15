import json

def search_name_for_id(nome):
    with open("search/search_dict.json", "r") as file:
        search_dict = json.load(file)
        for keys in search_dict["quickSearch"][0]:
            if nome in keys:
                return search_dict["quickSearch"][0]["amarelo"]
        for keys in search_dict["suvinil"][0]:
            if nome in keys:
                return search_dict["suvinil"][0][""+nome+""]
        for keys in search_dict["sherwin-willians"][0]:
            if nome in keys:
                return search_dict["sherwin-willians"][0][""+nome+""]
        for keys in search_dict["coral"][0]:
            if nome in keys:
                return search_dict["coral"][0][""+nome+""]

