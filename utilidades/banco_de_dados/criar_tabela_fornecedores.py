import sqlalchemy
import os
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy import MetaData
from sqlalchemy.dialects.mysql import DATETIME as DATE
from dotenv import load_dotenv
load_dotenv()

# rode isso para criar o esqueleto da tabela fornecedores
# para linkar fornecedores com padrão_cores use Alter table fornecedores add constraint padrão_id Foreign KEY (padrão_id) references padrao_cores(id)

# DATABASE_URL = st.secrets["DATABASE_URL"]
DATABASE_URL = os.getenv("AWS_URL")
engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=5, max_overflow=10)

nome_tabela = 'fornecedores'
metadata_obj = MetaData()

my_table = Table(
    nome_tabela,
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('nome', String(50)),
    Column('padrão_id', Integer), 
    Column('email', String(50)),
    Column('CREATED_AT', DATE),
    Column('UPDATED_AT', DATE),
    Column('DELETED_AT', DATE),
    mysql_charset='utf8mb4',
)


metadata_obj.create_all(engine)