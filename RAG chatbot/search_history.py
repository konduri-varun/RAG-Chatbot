# search_history.py
import sqlite3
from datetime import datetime

import streamlit as st

DB_PATH = "users.db"

import sqlite3


def upgrade_search_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE search ADD COLUMN answer TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    conn.commit()
    conn.close()

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
    upgrade_search_table()

# ----------- Store Search -----------
def store_search_query(username, query, answer):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO search (username, query, answer) VALUES (?, ?, ?)", (username, query, answer))
    conn.commit()
    conn.close()


# ----------- Get History for User -----------
def get_user_history(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, query, answer, timestamp FROM search WHERE username = ? ORDER BY timestamp DESC", (username,))
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
        st.subheader("💬 Your Previous Chat History")

        history = get_user_history(st.session_state.username)
        if history:
            with st.expander("🕘 View / Clear Chat History"):
                for _id, query, answer, ts in history[:10]:
                    with st.chat_message("user"):
                        st.markdown(f"**You:** {query}")
                    with st.chat_message("assistant"):
                        st.markdown(f"**Bot:** {answer}")

                if st.button("🗑️ Clear History"):
                    clear_user_history(st.session_state.username)
                    st.success("History cleared. Please refresh.")
        else:
            st.info("No chat history yet.")

