from flask import Flask
import json

app = Flask(__name__)


@app.route('/report')
def violator_report():
    return json.dumps()
