import sqlite3

DATABASE = 'carebridge.db'

conn = sqlite3.connect(DATABASE)

# Insert sample scenarios
scenarios = [
    ('A patient is refusing medication. How would you approach this situation?'),
    ('A colleague is showing signs of burnout. How can you address this?'),
    ('A patient’s family is asking for updates beyond what is allowed. What would you do?')
]

conn.executemany('INSERT INTO scenarios (text) VALUES (?)', [(s,) for s in scenarios])

conn.commit()
conn.close()
print("Sample data populated.")
