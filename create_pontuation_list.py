import json
sem_acento = "energetica"
acento = "energética"

# maré precisa ser feito depois a mão
data = dict()
data['modificado'] = sem_acento
data['original'] = acento

print(data)
def create_pontuation_list(data):
    with open("lista_acentos_coral.json", "r+") as lista_acentos:
        lista = json.load(lista_acentos)
        
        lista['checklist'].append(data)
        
        lista_acentos.seek(0)
        json.dump(lista, lista_acentos)
        
create_pontuation_list(data)

