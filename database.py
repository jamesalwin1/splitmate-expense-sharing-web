import sqlite3

def get_connection():
    conn = sqlite3.connect("data.db")
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        payer TEXT,
        amount REAL,
        description TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS splits(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        expense_id INTEGER,
        person TEXT,
        share REAL
    )
    """)

    conn.commit()
    conn.close()