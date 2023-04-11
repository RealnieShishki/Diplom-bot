import sqlite3

conn = sqlite3.connect('zakazy.db')


conn.execute('''CREATE TABLE IF NOT EXISTS telegram_data
             (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
             NAME TEXT NOT NULL,
             CONTACTS TEXT NOT NULL,
             WORK_TYPE TEXT NOT NULL,
             TRANSPORT TEXT NOT NULL);''')

conn.commit()

conn.close()
