import streamlit as st
from user import login_user, register_user
from transaction import submit_transaction, fetch_transactions
from forecast import forecast_spending
from recommender import generate_recommendations
from budget import compare_budget_vs_actual
from database import create_tables

# Initialize database tables
create_tables()

# --- Page Config ---
st.set_page_config(page_title="WiseBudget", layout="wide")

# --- App Header ---
st.title("💸 WiseBudget: Personal Finance Assistant")
st.markdown("Securely manage your expenses, forecast future spending, and receive personalized financial tips.")

# --- Sidebar Navigation ---
menu = ["Login", "Register", "Dashboard"]
choice = st.sidebar.selectbox("Navigation", menu)

# --- User Session Storage ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

# --- Registration Page ---
if choice == "Register":
    st.subheader("Create New Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        register_user(username, password)
        st.success("Account created successfully. Please log in.")

# --- Login Page ---
elif choice == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid username or password.")

# --- Dashboard ---
elif choice == "Dashboard" and st.session_state.logged_in:
    st.success(f"Logged in as: {st.session_state.username}")
    tab1, tab2, tab3, tab4 = st.tabs(["💾 Add Transaction", "📊 Budget Dashboard", "🔮 Forecast", "🎯 Recommendations"])

    with tab1:
        st.subheader("Add Transaction")
        category = st.selectbox("Category", ["Income", "Needs", "Wants", "Savings"])
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        if st.button("Submit Transaction"):
            submit_transaction(st.session_state.username, category, amount)
            st.success("Transaction added!")

    with tab2:
        st.subheader("Budget Overview")
        data = fetch_transactions(st.session_state.username)
        if data is not None and not data.empty:
            compare_budget_vs_actual(data)
        else:
            st.info("No transaction data found.")

    with tab3:
        st.subheader("Forecast Future Spending")
        if data is not None and not data.empty:
            forecast_spending(data)
        else:
            st.warning("Forecasting requires transaction data.")

    with tab4:
        st.subheader("Recommendations")
        if data is not None and not data.empty:
            tips = generate_recommendations(data)
            for tip in tips:
                st.info(f"💡 {tip}")
        else:
            st.warning("No transactions to analyze.")

# --- If not logged in ---
elif choice == "Dashboard":
    st.warning("Please log in to access the dashboard.")
