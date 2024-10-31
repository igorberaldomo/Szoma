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


# rode isso para criar o esqueleto da tabela coral
def db_table_insertinto_coral():
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = sqlalchemy.create_engine( DATABASE_URL , pool_size=5, max_overflow=10)

    nome_tabela ='coral'
    metadata_obj = MetaData()

    my_table = Table(
        nome_tabela,
        metadata_obj,
        Column('id', Integer,primary_key=True),
        Column('nome', String(50)),
        Column('red', Integer),
        Column('green', Integer),
        Column('blue', Integer),
        Column('hexadecimal', String(7)),
        Column('pantone_código', String(8)),
        Column('pantone_name', String(20)),
        Column('pantone_hex', String(7)),
        Column('fornecedores', String(20)),
        mysql_charset='utf8mb4',
    )

    metadata_obj.create_all(engine)
    with open('coral/coral.json','r+') as file:  
        file_data = json.load(file)
        c = 0
        while c < len(file_data['corescoral']):
            given_id = c+1
            nome = str(file_data['corescoral'][c]['nome'])
            r = file_data['corescoral'][c]['rgb'][0]
            g = file_data['corescoral'][c]['rgb'][1]
            b = file_data['corescoral'][c]['rgb'][2]
            hexadecimal = file_data['corescoral'][c]['hexadecimal']
            pantone = file_data['corescoral'][c]['pantone']['codigo']
            pantone_name = file_data['corescoral'][c]['pantone']['name']
            pantone_hex = file_data['corescoral'][c]['pantone']['hex']
            fornecedores = file_data['corescoral'][c]['fornecedores']


            stmt = insert(my_table).values( id = given_id,nome = nome, red = r, green = g, blue = b, hexadecimal = hexadecimal, pantone_código = pantone, pantone_name = pantone_name, pantone_hex = pantone_hex, fornecedores = fornecedores)
            compiled = stmt.compile()
            
            with engine.connect() as conn:
                result = conn.execute(stmt)
                conn.commit()
            c+=1
db_table_insertinto_coral()