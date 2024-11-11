import sqlalchemy
import os
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

def db_table_select_all_fornecedores():
    # DATABASE_URL = st.secrets["DATABASE_URL"]
    DATABASE_URL = os.getenv("AWS_URL")
    engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
    resultset  = pd.read_sql('SELECT * FROM fornecedores ', engine)
    print(resultset)


