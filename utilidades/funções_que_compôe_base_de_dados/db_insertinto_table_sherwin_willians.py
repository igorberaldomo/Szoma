import sqlalchemy
import os
import json
import datetime
from sqlalchemy import insert
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy import MetaData
from sqlalchemy.dialects.mysql import DATETIME as DATE


# rode isso para criar o esqueleto da tabela padrao_cores e inserir os dados

def db_table_insertinto_Sherwin_Willians():
    DATABASE_URL = os.getenv("AWS_URL")
    engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
    
    nome_tabela = 'sherwin_willians'
    metadata_obj = MetaData()

    my_table = Table(
        nome_tabela,
        metadata_obj,
        Column('id', Integer, primary_key=True),
        Column('nome', String(50)),
        Column('red', Integer),
        Column('green', Integer),
        Column('blue', Integer),
        Column('hexadecimal', String(7)),
        Column('pantone_código', String(8)),
        Column('pantone_name', String(20)),
        Column('pantone_hex', String(7)),
        Column('fornecedores', String(20)),
        Column('CREATED_AT', String(40)),
        Column('UPDATED_AT', String(40)),
        Column('DELETED_AT', String(40)),

        mysql_charset='utf8mb4',
    )

    metadata_obj.create_all(engine)

    with open('sherwin/sherwin-willians.json','r+') as file:
        file_data = json.load(file)
        c = 0
        while c < len(file_data["cores-sherwin-willians"]):
 
            nome = str(file_data["cores-sherwin-willians"][c]['nome'])
            red = int(file_data["cores-sherwin-willians"][c]['rgb'][0])
            green= int(file_data["cores-sherwin-willians"][c]['rgb'][1])
            blue = int(file_data["cores-sherwin-willians"][c]['rgb'][2])
            hexadecimal = str(file_data["cores-sherwin-willians"][c]['hexadecimal'])
            pantone_código = str(file_data["cores-sherwin-willians"][c]['pantone']['codigo'])
            pantone_name = str(file_data["cores-sherwin-willians"][c]['pantone']['name'])
            pantone_hex = str(file_data["cores-sherwin-willians"][c]['pantone']['hex'])
            fornecedores = str(file_data["cores-sherwin-willians"][c]['fornecedor'])
            created_at = datetime.datetime.now()
            updated_at = datetime.datetime.now()
            deleted_at = 0
            
            stmt = insert(my_table).values(nome = nome, red = red, green = green, blue = blue, hexadecimal = hexadecimal, pantone_código = pantone_código, pantone_name = pantone_name, pantone_hex = pantone_hex, fornecedores = fornecedores, CREATED_AT = created_at, UPDATED_AT = updated_at, DELETED_AT = deleted_at)
            compiled = stmt.compile()
            print(compiled.params)
            
            with engine.connect() as conn:
                result = conn.execute(stmt)
                print(c)
                conn.commit()
            c+=1
db_table_insertinto_Sherwin_Willians()