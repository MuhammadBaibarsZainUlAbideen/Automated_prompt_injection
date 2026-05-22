import sqlite3

file_name = "mydatabase1.db"

#TABLE INITIALIZATION FUNCTION

def get_connection():
    conn = sqlite3.connect(file_name)
    return conn

def init_db():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            account_number INTEGER,
            balance REAL
        )
        """)
    conn.commit()


#INSERTING DATA INTO TABLES FUNCTIONS

def add_user(username, password, account_number, balance=0.0):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO Users (username, password, account_number, balance)
            VALUES (?, ?, ?, ?)
            """, (username, password, account_number, balance)
        )
        conn.commit()


#GETTING DATA FROM TABLES FUNCTIONS

def get_user_by_username(username):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, username, account_number, balance FROM Users WHERE username = ?", (username,))
    data = cur.fetchone()
    return data

def get_user_by_account_number(account_number):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, username, account_number, balance FROM Users WHERE account_number = ?", (account_number,))
    data = cur.fetchone()
    return data

def get_balance(account_number):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT balance FROM Users WHERE account_number = ?", (account_number,))
    data = cur.fetchone()
    return data[0] if data else None