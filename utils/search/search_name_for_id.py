import json

def search_name_for_id(nome):
    with open("search/search_dict.json", "r") as file:
        nome  = f'"{nome}"'
        search_dict = json.load(file)
        select_id = 0
        if nome in search_dict[0]["quickSearch"][0]:
            select_id = search_dict["quickSearch"][0][nome]
        elif nome in search_dict[0]["suvinil"][0]:
            select_id = search_dict["suvinil"][0][nome]
        elif nome in search_dict[0]["coral"][0]:
            select_id = search_dict["coral"][0][nome]
        elif nome in search_dict[0]["sherwin-willians"][0]:
            select_id = search_dict["sherwin-willians"][0][nome]
        else:
            err = "Nenhuma cor encontrada"
            return err
        print(select_id)
    return select_id
