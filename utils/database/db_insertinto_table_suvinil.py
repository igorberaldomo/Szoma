import sqlalchemy
import os
import json
import datetime
from sqlalchemy import insert
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy import MetaData
from dotenv import load_dotenv
load_dotenv()

# rode isso para criar o esqueleto da tabela suvinil e inserir os dados

def db_table_insertinto_suvinil():
    # DATABASE_URL = st.secrets["DATABASE_URL"]
    DATABASE_URL = os.getenv("AWS_URL")
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
        Column('ncs',String(10)),
        Column('codigo_suvinil',String(5)),
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

    with open('./suvinil/suvinil.json','r+') as file:
        file_data = json.load(file)
        c = 0
        while c < len(file_data['coressuvinil']):
 
            nome = str(file_data['coressuvinil'][c]['nome'])
            red = int(file_data['coressuvinil'][c]['rgb'][0])
            green= int(file_data['coressuvinil'][c]['rgb'][1])
            blue = int(file_data['coressuvinil'][c]['rgb'][2])
            ncs = str(file_data['coressuvinil'][c]['ncs']) 
            codigo_suvinil = str(file_data['coressuvinil'][c]['codigo_suvinil'])
            hexadecimal = str(file_data['coressuvinil'][c]['hexadecimal'])
            pantone_código = str(file_data['coressuvinil'][c]['pantone']['codigo'])
            pantone_name = str(file_data['coressuvinil'][c]['pantone']['name'])
            pantone_hex = str(file_data['coressuvinil'][c]['pantone']['hex'])
            fornecedores = str(file_data['coressuvinil'][c]['fornecedores'])
            created_at = datetime.datetime.now()
            updated_at = datetime.datetime.now()
            deleted_at = 0
            
            stmt = insert(my_table).values(nome = nome, red = red, green = green, blue = blue, ncs = ncs, codigo_suvinil = codigo_suvinil, hexadecimal = hexadecimal, pantone_código = pantone_código, pantone_name = pantone_name, pantone_hex = pantone_hex, fornecedores = fornecedores, CREATED_AT = created_at, UPDATED_AT = updated_at, DELETED_AT = deleted_at)
            compiled = stmt.compile()
            print(compiled.params)
            
            with engine.connect() as conn:
                result = conn.execute(stmt)
                print(c)
                conn.commit()
            c+=1
db_table_insertinto_suvinil()