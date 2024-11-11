import os, json
import pandas as pd
import sqlalchemy
from flask import Flask, request

DATABASE_URL = os.getenv("AWS_URL")
engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=5, max_overflow=10)

def select_names(nome):
    search_string = (
        f"SELECT * FROM suvinil WHERE nome = '{nome}' or pantone_name = '{nome}' "
    )
    resultset = pd.read_sql(search_string, engine)
    if resultset.empty:
        search_string = f"SELECT * FROM suvinil where nome like ':nome' or pantone_name like ':nome' "
        resultset = pd.read_sql(search_string, engine, params={"nome": nome})
    return resultset
