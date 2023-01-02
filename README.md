Run:

- `python init_db.py` to create SQLite table
- `python updater.py` to launch database updater task
- `flask run` to start flask server at http://127.0.0.1:5000
- `npm start` in react-app directory to start react app at http://localhost:3000/

Look at database with `sqlite3`, `.open 'database.db'` and, e.g. `SELECT full_name FROM drone;` or `SELECT MIN(last_seen) FROM drone;`
