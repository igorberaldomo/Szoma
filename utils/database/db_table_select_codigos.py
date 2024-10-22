import os, json
import pandas as pd
import sqlalchemy
from flask import Flask, request

def select_códigos(codigo):
    search_string = f"SELECT * FROM suvinil WHERE pantone_código = '{codigo}'"
    resultset = pd.read_sql(search_string, engine)
    if resultset.empty:
        search_string = f"SELECT * FROM suvinil where pantone_código like ':codigo'"
        resultset = pd.read_sql(search_string, engine, params={"codigo": codigo})
    return resultset