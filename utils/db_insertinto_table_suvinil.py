import sqlalchemy
import os
import json
from sqlalchemy import insert
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy import MetaData
from dotenv import load_dotenv

load_dotenv()


def db_table_insertinto_suvinil():
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
    
    nome_tabela ='suvinil'
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

    with open('./suvinil/suvenil.json','r+') as file:
        file_data = json.load(file)
        c = 0
        while c < len(file_data['coressuvinil']):
 
            nome = str(file_data['coressuvinil'][c]['nome'])
            red = int(file_data['coressuvinil'][c]['rgb'][0])
            green= int(file_data['coressuvinil'][c]['rgb'][1])
            blue = int(file_data['coressuvinil'][c]['rgb'][2])
            hexadecimal = str(file_data['coressuvinil'][c]['hexadecimal'])
            pantone_código = str(file_data['coressuvinil'][c]['pantone']['codigo'])
            pantone_name = str(file_data['coressuvinil'][c]['pantone']['name'])
            pantone_hex = str(file_data['coressuvinil'][c]['pantone']['hex'])
            fornecedores = str(file_data['coressuvinil'][c]['loja'])
            
            
            stmt = insert(my_table).values(nome = nome, red = red, green = green, blue = blue, hexadecimal = hexadecimal, pantone_código = pantone_código, pantone_name = pantone_name, pantone_hex = pantone_hex, fornecedores = fornecedores)
            compiled = stmt.compile()
            print(compiled.params)
            
            with engine.connect() as conn:
                result = conn.execute(stmt)
                print(c)
                conn.commit()
            c+=1
db_table_insertinto_suvinil()