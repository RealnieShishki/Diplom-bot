import sqlite3


conn = sqlite3.connect('zakazy.db')

cursor = conn.cursor()

query = "SELECT * FROM telegram_data"
cursor.execute(query)

data = cursor.fetchall()

conn.close()

for row in data:
    print(row)