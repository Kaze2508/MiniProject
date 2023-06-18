import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS data
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            sensor_data REAL NOT NULL,
            sensor_type TEXT NOT NULL,
            humidity REAL)''')

conn.commit()

conn.close()