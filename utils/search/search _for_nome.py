from utils.conect_to_engine import conect_to_engine_developer

engine = conect_to_engine_developer()
def select_names(nome, fornecedores):
    seach_string = ""
    if fornecedores != "todos":
        search_string = f"SELECT * from {fornecedores} WHERE nome = '{nome}' or pantone_name = '{nome}' "
    else:
        search_string = f"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil WHERE nome = '{nome}' or pantone_name = '{nome}' union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral WHERE nome = '{nome}' or pantone_name = '{nome}' "

    resultset = pd.read_sql(search_string, engine)
    return resultset