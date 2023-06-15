import sqlite3

# Create a new SQLite database file
conn = sqlite3.connect('database.db')

# Create a cursor object
c = conn.cursor()

# Create the data table
c.execute('''CREATE TABLE data
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              topic TEXT NOT NULL,
              payload TEXT NOT NULL)''')

# Insert some data into the table
c.execute("INSERT INTO data (topic, payload) VALUES (?,?)", ('topic1', 'payload1'))
c.execute("INSERT INTO data (topic, payload) VALUES (?,?)", ('topic2', 'payload2'))
c.execute("INSERT INTO data (topic, payload) VALUES (?,?)", ('topic3', 'payload3'))

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()