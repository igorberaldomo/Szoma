import os, sqlalchemy
from sqlalchemy import create_engine
import pymysql


def conect_to_engine_developer():
    DATABASE_URL = os.getenv("AWS_URL")
    engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
    return engine