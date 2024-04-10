import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Execute each SQL statement separately
sql_queries = [
    """CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fname TEXT NOT NULL,
        lname TEXT NOT NULL,
        gender TEXT CHECK(gender IN ('male', 'female', 'none')) NOT NULL,
        nationality TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );""",
    """CREATE TABLE records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        label TEXT NOT NULL,
        year INTEGER NOT NULL,
        condition TEXT NOT NULL,
        cost NUMERIC(10, 2) NOT NULL,
        year_of_purchase INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );"""
]

for query in sql_queries:
    cursor.execute(query)

# Commit changes and close connection
conn.commit()
conn.close()