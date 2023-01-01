import requests
import xml.etree.ElementTree as ET
from dateutil import parser
from datetime import datetime, timezone
import time
import math

from violator import Violator


def get_snapshot(session):
    """fetch drones snapshot, return xml"""

    url = 'https://assignments.reaktor.com/birdnest/drones'
    response = session.get(url, headers={'accept': 'application/xml'})
    response.raise_for_status()

    return response.text


def get_pilot(serial_number):
    """fetch pilot info for violating drone, return json"""

    url = f'https://assignments.reaktor.com/birdnest/pilots/{serial_number}'
    response = requests.get(url, headers={'accept': 'application/json'})
    response.raise_for_status()

    return response.json()


def update(violators, snapshot):
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
                    position, last_seen, name, phone, email)
            else:
                # known violator
                violators[pilot_id].set_closest_approach(position)
                violators[pilot_id].set_last_seen(last_seen)

    for pilot_id in list(violators):
        last_seen = violators[pilot_id].get_last_seen()
        time_since = (datetime.now(timezone.utc) - parser.parse(last_seen))
        if time_since.total_seconds() >= 600:
            del violators[pilot_id]


def update_periodically(report, period=2):
    """execute update task every 2 seconds"""

    session = requests.Session()

    while True:
        start_time = time.time()
        snapshot = get_snapshot(session)
        with report.lock:
            update(report.violators, snapshot)
        end_time = time.time()

        if end_time - start_time < period:
            time.sleep(period - (end_time - start_time))
