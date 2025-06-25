import streamlit as st
from database import engine
from auth import hash_password, check_password
import pandas as pd
from sqlalchemy import text

# Page title
st.set_page_config(page_title="WiseBudget", page_icon="💸")

st.title("💸 WiseBudget - Login Portal")

# Page selection
page = st.sidebar.selectbox("Choose a page", ["Login", "Register"])

# DB connection
def run_query(query, params=None):
    with engine.connect() as conn:
        return conn.execute(text(query), params or {}).fetchall()

def execute_query(query, params=None):
    with engine.begin() as conn:
        conn.execute(text(query), params or {})

# Register page
if page == "Register":
    st.subheader("📝 Create an Account")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if password != confirm:
            st.error("Passwords do not match.")
        else:
            hashed_pw = hash_password(password)
            try:
                execute_query(
                    "INSERT INTO users (email, username, password) VALUES (:email, :username, :password)",
                    {"email": email, "username": username, "password": hashed_pw},
                )
                st.success("Account created! You can now log in.")
            except Exception as e:
                st.error(f"Registration failed: {e}")

# Login page
elif page == "Login":
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        result = run_query(
            "SELECT password FROM users WHERE username = :username",
            {"username": username},
        )
        if result:
            stored_hash = result[0][0]
            if check_password(password, stored_hash):
                st.success(f"Welcome, {username}!")
                st.balloons()
            else:
                st.error("Incorrect password.")
        else:
            st.error("User not found.")
