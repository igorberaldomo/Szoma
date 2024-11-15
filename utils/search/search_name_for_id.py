import json

def search_name_for_id(nome, fornecedores):
    with open("search/search_dict.json", "r") as file:
        search_dict = json.load(file)
        name_id = -1
        if name_id == -1:
            for keys in search_dict["quickSearch"][0]:
                    if nome in keys:
                        name_id = search_dict["quickSearch"][0][""+nome+""]
                        fornecedores = 'coral'               
        elif name_id == -1:
            for keys in search_dict["suvinil"][0]:
                    if nome in keys:
                        name_id = search_dict["suvinil"][0][""+nome+""]
                        fornecedores = 'suvinil'
        elif name_id == -1:
            for keys in search_dict["sherwin-willians"][0]:
                if nome in keys:
                    name_id = search_dict["sherwin-willians"][0][""+nome+""]
                    fornecedores = 'sherwin-willians'
        elif name_id == -1:
            for keys in search_dict["coral"][0]:
                if nome in keys:
                    name_id = search_dict["coral"][0][""+nome+""]
                    fornecedores = 'coral'
        else:
            break
    if fornecedores == 'sherwin-willians':
        fornecedores = "sherwin_willians"
    if fornecedores != "todos":
        seach_string = f"Select * from {fornecedores} WHERE id = {name_id}"
        resultset = pd.read_sql(seach_string, engine)
    else:
        seach_string = f"Select * from suvinil WHERE id = {name_id} "
        search_string_2 = f"Select * from coral WHERE id = {name_id}"
        search_string_3 = f"Select * from sherwin_willians WHERE id = {name_id}"
        resultset_1 = pd.read_sql(seach_string, engine)
        resultset_2 = pd.read_sql(search_string_2, engine)
        resultset_3 = pd.read_sql(search_string_3, engine)
        if nome in resultset_1["nome"].values:
            resultset = resultset_1
        elif nome in resultset_2["nome"].values:
            resultset = resultset_2
        else:
            resultset = resultset_3
    return resultset
