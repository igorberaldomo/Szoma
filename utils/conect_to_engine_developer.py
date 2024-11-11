import os, sqlalchemy

def conect_to_engine_developer():
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
    return engine