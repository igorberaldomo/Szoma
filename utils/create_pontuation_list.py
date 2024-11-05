import json
sem_acento = "vinicola"
acento = "vinícola"

data = dict()
data['modificado'] = sem_acento
data['original'] = acento

print(data)
def create_pontuation_list(data):
    with open("lista_acentos_suvinil.json", "r+") as lista_acentos:
        lista = json.load(lista_acentos)
        
        lista['checklist'].append(data)
        
        lista_acentos.seek(0)
        json.dump(lista, lista_acentos)
        
create_pontuation_list(data)

