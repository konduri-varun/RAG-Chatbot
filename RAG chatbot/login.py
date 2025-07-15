# login.py
import sqlite3

import bcrypt
import streamlit as st


# ---------- Database Setup ----------
def create_connection():
    return sqlite3.connect("users.db")

def create_users_table():
    conn = create_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = create_connection()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        st.success("✅ User registered successfully.")
    except sqlite3.IntegrityError:
        st.error("❌ Username already exists.")
    conn.close()

def login_user(username, password):
    conn = create_connection()
    cursor = conn.execute("SELECT password FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row and bcrypt.checkpw(password.encode(), row[0]):
        return True
    return False

# ---------- Streamlit App ----------
st.set_page_config("Login", page_icon="🔐")
st.title("🔐 Secure Login")

create_users_table()

menu = st.sidebar.radio("Select", ["Login", "Register"])

if menu == "Register":
    st.subheader("👤 Create Account")
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type='password')
    if st.button("Register"):
        if new_user and new_pass:
            register_user(new_user, new_pass)
        else:
            st.warning("Please fill both fields.")

elif menu == "Login":
    st.subheader("🔑 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful. Redirecting...")
            st.switch_page("pages/main.py")
        else:
            st.error("Incorrect username or password.")
