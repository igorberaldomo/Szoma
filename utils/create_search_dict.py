import sqlalchemy
import os
import pandas as pd
import json
from sqlalchemy import MetaData
from sqlalchemy.dialects.mysql import DATETIME as DATE
from dotenv import load_dotenv
load_dotenv()
newdict = dict()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=5, max_overflow=10)

search_string = f"SELECT nome , id FROM suvinil"
resultset = pd.read_sql(search_string, engine)
resultset = resultset.to_dict(orient='records')

for i in range(len(resultset)):
        nome = resultset[i]['nome']
        id1 = int(resultset[i]['id'])
        newdict[nome] = id1
print(newdict)
with open ('search_dict.json', 'w+') as file:
    json.dump(newdict, file)