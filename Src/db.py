import sqlite3
import os

file_name = "mydatabase1.db"


def tables():
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


def InsertingData(username, password):
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO Users (username, password)
    VALUES (?, ?)
    """, (username, password))

    conn.commit()
    conn.close()


def getting_username_password():
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()

    cur.execute("SELECT * FROM Users")
    data = cur.fetchall()

    conn.close()

    return data
def delting_eveything():
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()
    cur.execute("DELETE FROM Users")
    conn.commit()
    # conn.close()




