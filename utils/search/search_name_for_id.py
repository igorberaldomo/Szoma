def search_name_for_id(nome):
    with open("search/search_dict.json", "r") as file:
        search_dict = json.load(file)
        select_id = None
        if nome in search_dict["quickSearch"][0]:
            select_id = search_dict["quickSearch"][0][nome]
        if nome in search_dict["suvinil"][0]:
            select_id = search_dict["suvinil"][0][nome]
        if nome in search_dict["coral"][0]:
            select_id = search_dict["coral"][0][nome]
        print(select_id)
    return select_id
