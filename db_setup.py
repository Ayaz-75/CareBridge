import sqlite3

DATABASE = 'carebridge.db'

conn = sqlite3.connect(DATABASE)

# Create tables
conn.execute('''CREATE TABLE scenarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL
)''')

conn.execute('''CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scenario_id INTEGER NOT NULL,
    feedback TEXT NOT NULL,
    improvement TEXT NOT NULL,
    FOREIGN KEY (scenario_id) REFERENCES scenarios (id)
)''')

conn.close()
print("Database setup completed.")
