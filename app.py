from flask import Flask
import threading
import requests
import xml.etree.ElementTree as ET
import time
import math
import json

from violator import Violator, ViolatorEncoder

violators = {}


def get_snapshot(session):
    """fetch drones snapshot"""

    url = 'https://assignments.reaktor.com/birdnest/drones'
    response = session.get(url, headers={'accept': 'application/xml'})
    response.raise_for_status()

    return response.text


def get_pilot(serial_number):
    """fetch pilot info for violating drone"""

    url = f'https://assignments.reaktor.com/birdnest/pilots/{serial_number}'
    response = requests.get(url, headers={'accept': 'application/json'})
    response.raise_for_status()

    return response.json()


def update(snapshot):
    """update violators index based on snapshot"""

    root = ET.fromstring(snapshot)
    last_seen = root[1].get('snapshotTimestamp')

    for drone in root.iter('drone'):
        position = float(drone.find('positionX').text), float(
            drone.find('positionY').text)
        if math.dist(position, (250000, 250000)) <= 100000:
            # drone is a violator
            drone_id = drone.find('serialNumber').text
            pilot = get_pilot(drone_id)
            pilot_id = pilot['pilotId']

            if pilot_id not in violators:
                # new violator
                name = pilot['firstName'] + " " + pilot['lastName']
                phone = pilot['phoneNumber']
                email = pilot['email']

                violators[pilot_id] = Violator(
                    last_seen, position, name, phone, email)
            else:
                # known violator
                violators[pilot_id].closest_approach = position
                violators[pilot_id].last_seen = last_seen


def update_periodically(period=2):
    """execute update task every 2 seconds"""

    session = requests.Session()

    while True:
        start_time = time.time()
        update(get_snapshot(session))
        end_time = time.time()

        if end_time - start_time < period:
            time.sleep(period - (end_time - start_time))


app = Flask(__name__)


@app.before_first_request
def before_first_request():
    t = threading.Thread(target=update_periodically)
    t.start()


@app.route("/")
def report_violators():
    return json.dumps(violators, cls=ViolatorEncoder)
