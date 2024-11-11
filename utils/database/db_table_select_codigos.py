import os, json
import pandas as pd
import sqlalchemy
from flask import Flask, request


def select_códigos(codigo):
    DATABASE_URL = os.getenv("AWS_URL")
    engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
    search_string = f"SELECT * FROM suvinil WHERE pantone_código = '{codigo}'"
    resultset = pd.read_sql(search_string, engine)
    if resultset.empty:
        search_string = f"SELECT * FROM suvinil where pantone_código like ':codigo'"
        resultset = pd.read_sql(search_string, engine, params={"codigo": codigo})
    return resultset