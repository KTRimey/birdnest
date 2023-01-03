"""Initialize database of NDZ violators with 'schema.sql'."""

import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()
