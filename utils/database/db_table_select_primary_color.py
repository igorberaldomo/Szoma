import os, json
import pandas as pd
import sqlalchemy
from flask import Flask, request

DATABASE_URL = os.getenv("AWS_URL")
engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
def primary_select(red, green, blue):
    distancia = 18
    maxred = red + distancia
    minred = red - distancia
    maxgreen = green + distancia
    mingreen = green - distancia
    maxblue = blue + distancia
    minblue = blue - distancia
    if maxred > 255:
        maxred = 255
    if minred < 0:
        minred = 0
    if maxgreen > 255:
        maxgreen = 255
    if mingreen < 0:
        mingreen = 0
    if maxblue > 255:
        maxblue = 255
    if minblue < 0:
        minblue = 0
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
    search_string = f"SELECT * FROM suvinil WHERE red >= {minred} AND  red <= {maxred} AND green >= {mingreen} AND green <= {maxgreen} AND blue >= {minblue} AND blue <= {maxblue} "
    resultset = pd.read_sql(search_string, engine)
    if resultset.empty:
        return []
    else:
        return resultset