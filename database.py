import sqlite3
from sqlalchemy import create_engine, MetaData

# SQLite DB path
DATABASE_URL = "sqlite:///wisebudget.db"

# SQLAlchemy Engine and Metadata
engine = create_engine(DATABASE_URL, echo=False)
metadata = MetaData()

def create_tables():
    with engine.connect() as connection:
        connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """)
        connection.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            category TEXT NOT NULL,
            amount TEXT NOT NULL,  -- AES encrypted
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)