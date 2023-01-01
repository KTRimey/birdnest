from flask import Flask
import threading
import json

from updater import update_periodically
from violator import ViolatorEncoder


class Violators:
    """pilots who have violated no-fly-zone in past 10 minutes"""

    def __init__(self):
        self.violators = {}
        self.lock = threading.Lock()


report = Violators()

app = Flask(__name__)


@app.before_first_request
def before_first_request():
    t = threading.Thread(target=update_periodically, args=(report,))
    t.start()


@app.route('/report')
def violator_report():
    with report.lock:
        return json.dumps(report.violators, cls=ViolatorEncoder)
