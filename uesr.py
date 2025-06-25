from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine, select
from security import hash_password, verify_password
from database import engine

metadata = MetaData()

users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True, nullable=False),
    Column("password", String, nullable=False)
)

metadata.create_all(engine)

def register_user(username, password):
    hashed = hash_password(password)
    with engine.begin() as conn:
        result = conn.execute(select(users).where(users.c.username == username))
        if result.fetchone():
            return False  # Username already exists
        conn.execute(users.insert().values(username=username, password=hashed))
        return True

def authenticate_user(username, password):
    with engine.begin() as conn:
        result = conn.execute(select(users).where(users.c.username == username)).fetchone()
        if result and verify_password(password, result.password):
            return result.id
    return None
