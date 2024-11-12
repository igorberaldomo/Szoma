import sqlalchemy
import streamlit as st
from sqlalchemy import create_engine

def conect_to_engine_production():
    DATABASE_URL = st.secrets["AWS_URL"]
    engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
    return engin