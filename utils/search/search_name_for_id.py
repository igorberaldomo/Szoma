import json

def search_name_for_id(nome):
    with open("search/search_dict.json", "r") as file:
        search_dict = json.load(file)
        name_id = -1
        if name_id == -1:
            for keys in search_dict["quickSearch"][0]:
                    if nome in keys:
                        name_id = search_dict["quickSearch"][0][""+nome+""]
        elif name_id == -1:
            for keys in search_dict["suvinil"][0]:
                    if nome in keys:
                        name_id = search_dict["suvinil"][0][""+nome+""]
        elif name_id == -1:
            for keys in search_dict["sherwin-willians"][0]:
                if nome in keys:
                    name_id = search_dict["sherwin-willians"][0][""+nome+""]
        elif name_id == -1:
            for keys in search_dict["coral"][0]:
                if nome in keys:
                    name_id = search_dict["coral"][0][""+nome+""]
        else:
            break

