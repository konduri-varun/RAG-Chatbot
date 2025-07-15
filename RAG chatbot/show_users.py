import sqlite3


def show_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password FROM users")
    rows = cursor.fetchall()
    conn.close()

    print("Registered Users:")
    for row in rows:
        print(f"ID: {row[0]}, Username: {row[1]}, Hashed Password: {row[2]}")

if __name__ == "__main__":
    show_users()
