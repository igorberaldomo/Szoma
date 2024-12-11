from utils.conection.production_connection import production_connection

engine = production_connection()

def search_table_for_name(nome, fornecedores):
    # metodo para procurar as tabelas pelo nome
    if fornecedores == 'sherwin-willians':
        fornecedores = 'sherwin_willians'
    seach_string = ""
    if fornecedores != "todos":
        search_string = f"SELECT * from {fornecedores} WHERE nome = '{nome}' or pantone_name = '{nome}' "
    else:
        search_string = f"SELECT nome,red,green,blue,ncs,codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from suvinil WHERE nome = '{nome}' or pantone_name = '{nome}' union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from coral WHERE nome = '{nome}' or pantone_name = '{nome}' union SELECT nome,red,green,blue,null as ncs,null as codigo_suvinil,hexadecimal,pantone_código,pantone_name,pantone_hex,fornecedores from sherwin-willians WHERE nome = '{nome}' or pantone_name = '{nome}' "

    resultset = pd.read_sql(search_string, engine)
    return resultset