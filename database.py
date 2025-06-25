import os
import streamlit as st
from sqlalchemy import create_engine

# Load database credentials from Streamlit secrets or env
DB_USER = os.getenv("DB_USER") or st.secrets["DB_USER"]
DB_PASSWORD = os.getenv("DB_PASSWORD") or st.secrets["DB_PASSWORD"]
DB_HOST = os.getenv("DB_HOST") or st.secrets["DB_HOST"]
DB_PORT = os.getenv("DB_PORT") or st.secrets["DB_PORT"]
DB_NAME = os.getenv("DB_NAME") or st.secrets["DB_NAME"]

# Add SSL requirement for Streamlit Cloud
DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"
)

# Create SQLAlchemy engine with pre-ping
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
