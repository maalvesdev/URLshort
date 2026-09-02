import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS urls (
        short_code TEXT PRIMARY KEY,
        original_url TEXT NOT NULL,
        expires_at INTEGER
    )
''')

connection.commit()
connection.close()
print("New database created with expiration support!")