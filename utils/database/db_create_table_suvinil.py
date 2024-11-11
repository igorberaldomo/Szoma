import sqlalchemy
import os
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy import MetaData
from dotenv import load_dotenv
load_dotenv()

# rode isso para criar o esqueleto da tabela suvinil

# DATABASE_URL = st.secrets["DATABASE_URL"]
DATABASE_URL = os.getenv("AWS_URL")
engine = sqlalchemy.create_engine( DATABASE_URL , pool_size=5, max_overflow=10)

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
