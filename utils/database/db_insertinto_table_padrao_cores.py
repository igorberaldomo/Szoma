import sqlalchemy
import os
import json
import datetime
from sqlalchemy import insert
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy import MetaData
from sqlalchemy.dialects.mysql import DATETIME as DATE
from dotenv import load_dotenv
load_dotenv()

# rode isso para criar o esqueleto da tabela padrao_cores e inserir os dados

def db_table_insertinto_padrao_cores():
    # DATABASE_URL = st.secrets["DATABASE_URL"]
    DATABASE_URL = os.getenv("AWS_URL")
    engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
    
    nome_tabela = 'padrao_cores'
    metadata_obj = MetaData()

    my_table = Table(
        nome_tabela,
        metadata_obj,
        Column('id', Integer, primary_key=True),
        Column('padrão', String(50)),
        Column('CREATED_AT', DATE ),
        Column('UPDATED_AT', DATE),
        Column('DELETED_AT', DATE),
        mysql_charset='utf8mb4',
    )

    metadata_obj.create_all(engine)

    with open('padrão/padrao_cores.json','r+') as file:  
        file_data = json.load(file)
        c = 0
        while c < len(file_data['padrão']):
            
            given_id = int(file_data['padrão'][c]['id'])
            padrão = str(file_data['padrão'][c]['padrão'])
            data = datetime.datetime.now()

            stmt = insert(my_table).values( id = given_id, padrão = padrão, CREATED_AT = data)
            compiled = stmt.compile()
            print(compiled.params)
            
            with engine.connect() as conn:
                result = conn.execute(stmt)
                print(c)
                conn.commit()
            c+=1
db_table_insertinto_padrao_cores()