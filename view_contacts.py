import sqlite3

# Connect to the same database
conn = sqlite3.connect("contact.db")
c = conn.cursor()

# Get everything from the contacts table
c.execute("SELECT id, name, email, message, created_at FROM contacts")
rows = c.fetchall()

conn.close()

# Print results
for row in rows:
    print(row)
