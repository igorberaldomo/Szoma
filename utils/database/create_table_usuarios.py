import sqlalchemy
import os
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy import MetaData
from dotenv import load_dotenv
from sqlalchemy.dialects.mysql import DATETIME as DATE
load_dotenv()

# rode isso para criar o esqueleto da tabela usuarios
    # DATABASE_URL = st.secrets["AWS_URL"]
DATABASE_URL = os.getenv("AWS_URL")
engine = sqlalchemy.create_engine( DATABASE_URL , pool_size=5, max_overflow=10)

table_name = 'usuarios'
metadata_obj = MetaData()

my_table = Table(
    table_name,
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('nome', String(50)),
    Column('empresa',String(20)),
    Column('email', String(50)),
    Column('senha', String(50)),
    Column('CREATED_AT', DATE),
    Column('UPDATED_AT', DATE),
    Column('DELETED_AT', DATE),
    mysql_charset='utf8mb4',
)

metadata_obj.create_all(engine)