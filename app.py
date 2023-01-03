from flask import Flask
from flask import g
import sqlite3

app = Flask(__name__)


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database.db')
    db.row_factory = make_dicts
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/report')
def violator_report():
    con = get_db()
    report = con.execute(
        'SELECT * FROM drone ORDER BY last_seen DESC').fetchall()
    return report
