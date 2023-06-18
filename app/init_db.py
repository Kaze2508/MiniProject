import sqlite3
from datetime import datetime

# Create a new SQLite database file
conn = sqlite3.connect('database.db')

# Create a cursor object
c = conn.cursor()

# Create the data table
c.execute('''CREATE TABLE IF NOT EXISTS data
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              timestamp TEXT NOT NULL,
              temperature REAL NOT NULL,
              humidity REAL NOT NULL)''')

# Insert some data into the table
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
temperature = 25.5
humidity = 60.2
c.execute("INSERT INTO data (timestamp, temperature, humidity) VALUES (?,?,?)", (timestamp, temperature, humidity))

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()
