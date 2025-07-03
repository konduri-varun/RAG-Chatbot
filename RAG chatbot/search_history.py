# search_history.py
import sqlite3
from datetime import datetime

import streamlit as st

DB_PATH = "users.db"

import sqlite3


def initialize_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            query TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# ----------- Store Search -----------
def store_search_query(username, query):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO search (username, query) VALUES (?, ?)", (username, query))
    conn.commit()
    conn.close()

# ----------- Get History for User -----------
def get_user_history(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, query, timestamp FROM search WHERE username = ? ORDER BY timestamp DESC", (username,))
    history = cursor.fetchall()
    conn.close()
    return history

# ----------- Delete History for User -----------
def clear_user_history(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM search WHERE username = ?", (username,))
    conn.commit()
    conn.close()

# ----------- Display History -----------
def display_user_history():
    if "username" in st.session_state:
        st.markdown("---")
        st.subheader("🕘 Your Search History")
        history = get_user_history(st.session_state.username)
        if history:
            with st.expander("View / Clear History"):
                for _id, query, ts in history[:10]:
                    st.markdown(f"- {ts.split('.')[0]}: `{query}`")
                if st.button("🗑️ Clear History"):
                    clear_user_history(st.session_state.username)
                    st.success("History cleared. Please refresh to update.")
        else:
            st.info("No search history yet.")
