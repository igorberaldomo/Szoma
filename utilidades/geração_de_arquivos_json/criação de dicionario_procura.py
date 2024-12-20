import sqlalchemy
import os
import pandas as pd
import json
from sqlalchemy import MetaData
from sqlalchemy.dialects.mysql import DATETIME as DATE
from dotenv import load_dotenv
from utilidades.método_de_conecção_local import método_de_conecção_local
load_dotenv()
newdict = dict()


engine = método_de_conecção_local()
# esse método é usado depois de ser inseridos os dados no banco de dados, para criar o json que ser usado pelo front-end para procurar as cores quando somente um nome for digitado, depois de criadoo json ele tem que ser movido para a pasta procura

search_string = f"SELECT nome , id FROM suvinil"
resultset = pd.read_sql(search_string, engine)
resultset = resultset.to_dict(orient='records')

for i in range(len(resultset)):
        nome = resultset[i]['nome']
        id1 = int(resultset[i]['id'])
        newdict[nome] = id1
print(newdict)
with open ('search_dict.json', 'r+') as file:
   search = json.load(file)
   search['suvinil'].append(newdict)
   file.seek(0)
   json.dump(search, file)

search_string = f"SELECT nome , id FROM coral"
resultset = pd.read_sql(search_string, engine)
resultset = resultset.to_dict(orient='records')
newdict.clear()
print(newdict)

for i in range(len(resultset)):
        nome = resultset[i]['nome']
        id1 = int(resultset[i]['id'])
        newdict[nome] = id1
print(newdict)

with open ('search_dict.json', 'r+') as file:
   search = json.load(file)
   search['coral'].append(newdict)
   file.seek(0)
   json.dump(search, file)


search_string = f"SELECT nome , id FROM sherwin_willians"
resultset = pd.read_sql(search_string, engine)
resultset = resultset.to_dict(orient='records')
newdict.clear()
print(newdict)

for i in range(len(resultset)):
        nome = resultset[i]['nome']
        id1 = int(resultset[i]['id'])
        newdict[nome] = id1
print(newdict)

with open ('search/search_dict.json', 'r+') as file:
   search = json.load(file)
   search["sherwin-willians"].append(newdict)
   file.seek(0)
   json.dump(search, file)
   
search_string = f"SELECT nome , id FROM anjo"
resultset = pd.read_sql(search_string, engine)
resultset = resultset.to_dict(orient='records')
newdict.clear()
print(newdict)

for i in range(len(resultset)):
        nome = resultset[i]['nome']
        id1 = int(resultset[i]['id'])
        newdict[nome] = id1
print(newdict)

with open ('search/search_dict.json', 'r+') as file:
   search = json.load(file)
   search["anjo"].append(newdict)
   file.seek(0)
   json.dump(search, file)