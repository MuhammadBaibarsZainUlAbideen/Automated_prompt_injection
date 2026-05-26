import os
import sqlite3
import random
import hashlib

# Use the same database filename as before
DB_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mydatabase1.db")

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    """Initializes the Users table if it doesn't exist."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            account_number INTEGER UNIQUE,
            balance REAL
        )
        """)
        conn.commit()

def register_user(username, password, initial_balance=1000.0):
    """
    Registers a new user. Generates a unique 8-digit account number.
    Returns the user info dictionary if successful, or raises a ValueError if the username is taken.
    """
    init_db()
    with get_connection() as conn:
        cur = conn.cursor()
        # Check if username exists
        cur.execute("SELECT id FROM Users WHERE username = ?", (username,))
        if cur.fetchone():
            raise ValueError(f"Username '{username}' is already taken.")
        
        # Generate a unique 8-digit account number
        while True:
            account_number = random.randint(10000000, 99999999)
            cur.execute("SELECT id FROM Users WHERE account_number = ?", (account_number,))
            if not cur.fetchone():
                break
        
        # Convert password to MD5 hash
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        
        cur.execute("""
            INSERT INTO Users (username, password, account_number, balance)
            VALUES (?, ?, ?, ?)
            """, (username, hashed_password, account_number, initial_balance)
        )
        conn.commit()
        
        return {
            "username": username,
            "account_number": account_number,
            "balance": initial_balance
        }

def authenticate_user(username, password):
    """
    Checks username and password.
    Returns a dictionary of user details (username, account_number, balance) if successful, else None.
    """
    init_db()
    with get_connection() as conn:
        cur = conn.cursor()
        # Convert input password to MD5 hash for comparison
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        
        cur.execute("""
            SELECT username, account_number, balance 
            FROM Users 
            WHERE username = ? AND password = ?
        """, (username, hashed_password))
        row = cur.fetchone()
        if row:
            return {
                "username": row[0],
                "account_number": row[1],
                "balance": row[2]
            }
    return None

def get_user_by_username(username):
    """Fetches user details by username."""
    init_db()
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT username, account_number, balance 
            FROM Users 
            WHERE username = ?
        """, (username,))
        row = cur.fetchone()
        if row:
            return {
                "username": row[0],
                "account_number": row[1],
                "balance": row[2]
            }
    return None

def get_balance(account_number):
    """Fetches account balance by account number."""
    init_db()
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT balance FROM Users WHERE account_number = ?", (account_number,))
        row = cur.fetchone()
        return row[0] if row else None

def get_all_users_raw():
    """Retrieves all user records, including passwords, for vulnerability testing/debugging."""
    init_db()
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, username, password, account_number, balance FROM Users")
        rows = cur.fetchall()
        return [
            {
                "id": r[0],
                "username": r[1],
                "password": r[2],
                "account_number": r[3],
                "balance": r[4]
            }
            for r in rows
        ]

