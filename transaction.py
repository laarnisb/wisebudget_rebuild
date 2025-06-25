from sqlalchemy import Table, Column, Integer, String, Float, Date, MetaData, select
from database import engine
from security import encrypt_data, decrypt_data

metadata = MetaData()

# Define the transactions table
transactions = Table(
    "transactions", metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, nullable=False),
    Column("date", String, nullable=False),
    Column("category", String, nullable=False),
    Column("amount", String, nullable=False),  # Stored as encrypted string
    Column("description", String, nullable=True)
)

metadata.create_all(engine)

# Submit a new transaction with encrypted amount
def submit_transaction(user_id, date, category, amount, description):
    encrypted_amount = encrypt_data(str(amount))
    with engine.begin() as conn:
        conn.execute(transactions.insert().values(
            user_id=user_id,
            date=date,
            category=category,
            amount=encrypted_amount,
            description=description
        ))

# Fetch and decrypt all transactions for a user
def fetch_transactions(user_id):
    with engine.begin() as conn:
        result = conn.execute(
            select(transactions).where(transactions.c.user_id == user_id)
        ).fetchall()

    # Decrypt amount field
    return [
        {
            "date": row.date,
            "category": row.category,
            "amount": float(decrypt_data(row.amount)),
            "description": row.description
        }
        for row in result
    ]
