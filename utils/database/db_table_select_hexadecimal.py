import os, json
import pandas as pd
import sqlalchemy
from flask import Flask, request

def select_hexadecimal(hexadecimal):
    search_string = f"SELECT * FROM suvinil WHERE hexadecimal = '{hexadecimal}' or pantone_hex = '{hexadecimal}' "
    resultset = pd.read_sql(search_string, engine)
    if resultset.empty:
        search_string = f"SELECT * FROM suvinil where hexadecimal like ':hexadecimal' or pantone_hex like ':hexadecimal' "
        resultset = pd.read_sql(
            search_string, engine, params={"hexadecimal": hexadecimal}
        )
    return resultset