import sqlalchemy
import streamlit as st

def conect_to_engine_production():
    DATABASE_URL = st.secrets["AWS_URL"]
    engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
    return engine