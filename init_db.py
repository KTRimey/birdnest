"""
Script to initialize SQLite database of NDZ violators in 'database.db'
and exectute 'schema.sql' to create drone table with specified schema.
"""

import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()
