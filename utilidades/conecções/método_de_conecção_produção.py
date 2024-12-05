import sqlalchemy
import streamlit as st
import os
import pymysql


def método_de_conecção_produção():
    DATABASE_URL = st.secrets["AWS_URL"]
    engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
    return engine

