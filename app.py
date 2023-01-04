"""Flask-based API server."""

from flask import Flask, send_from_directory, send_file, redirect, url_for
from flask import g
import sqlite3

app = Flask(__name__, static_folder='react-app/build/static')


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


@app.route('/api/report')
def violator_report():
    con = get_db()
    report = con.execute(
        'SELECT * FROM drone ORDER BY closest_approach_time DESC').fetchall()
    return report


#
# The following are only needed for production.
#

@app.route('/app/<path:path>')
def send_app(path):
    return send_from_directory('react-app/build', path)


@app.route('/app/')
def send_index():
    return send_file('react-app/build/index.html')


@app.route('/favicon.ico')
def send_favicon():
    return send_file('react-app/build/favicon.ico')


@app.route('/')
def redirect_from_root():
    return redirect(url_for('send_index'))
