import sqlite3

print("Connecting to compost.db...")
conn = sqlite3.connect('compost.db')
cursor = conn.cursor()

print("Creating table compost_logs...")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS compost_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        weight REAL NOT NULL,
        location TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()
print("Table created successfully!")
