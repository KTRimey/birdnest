import sqlite3
import requests
import logging
import xml.etree.ElementTree as ET
from dateutil import parser
from datetime import datetime, timezone
import time
import math

NEST_POSITION = (250000, 250000)
NO_FLY_RADIUS = 100000


def get_snapshot():
    """fetch drones snapshot"""

    url = 'https://assignments.reaktor.com/birdnest/drones'
    response = requests.get(url, headers={'accept': 'application/xml'})
    response.raise_for_status()

    return response.text


def get_pilot(serial_number):
    """fetch pilot info for violating drone"""

    url = f'https://assignments.reaktor.com/birdnest/pilots/{serial_number}'
    response = requests.get(url, headers={'accept': 'application/json'})
    if response.status_code == 404:
        return {'firstName': None, 'lastName': None, 'phoneNumber': None, 'email': None}
    response.raise_for_status()

    return response.json()


def update(connection, snapshot):
    """update database of violating drones based on snapshot"""
    cur = connection.cursor()

    root = ET.fromstring(snapshot)
    last_seen = root[1].get('snapshotTimestamp')

    for drone in root.iter('drone'):
        drone_id = drone.find('serialNumber').text
        is_known = cur.execute(
            "SELECT drone_id FROM drone WHERE drone_id=?", (drone_id,)).fetchone()
        if is_known:
            # known violator last seen by equipment
            cur.execute(
                "UPDATE drone SET last_seen=? WHERE drone_id=?", (last_seen, drone_id))

        position = float(drone.find('positionX').text), float(
            drone.find('positionY').text)
        distance = math.dist(position, NEST_POSITION)
        if distance <= NO_FLY_RADIUS:
            # drone is in violation

            if not is_known:
                # new violator
                pilot = get_pilot(drone_id)
                name = pilot['firstName'] + " " + pilot['lastName']
                violator = (drone_id, distance, last_seen, name,
                            pilot['phoneNumber'], pilot['email'])
                cur.execute(
                    "INSERT INTO drone VALUES(?, ?, ?, ?, ?, ?)", violator)
            else:
                # known violator
                prev_closest = cur.execute(
                    "SELECT closest_approach FROM drone WHERE drone_id=?", (drone_id,)).fetchone()
                if distance < prev_closest[0]:
                    # closest confirmed distance to the nest
                    cur.execute(
                        "UPDATE drone SET closest_approach=? WHERE drone_id=?", (distance, drone_id))

    violators = cur.execute("SELECT drone_id, last_seen FROM drone").fetchall()
    for drone_id, last_seen in violators:
        time_since = (datetime.now(timezone.utc) - parser.parse(last_seen))
        if time_since.total_seconds() >= 600:
            cur.execute("DELETE FROM drone WHERE drone_id=?", (drone_id,))

    connection.commit()


def update_periodically(connection, period=2):
    """execute update task every 2 seconds"""
    while True:
        start_time = time.time()
        try:
            update(connection, get_snapshot())
        except Exception as e:
            logging.exception(e)
            continue

        elapsed_time = time.time() - start_time

        if elapsed_time < period:
            time.sleep(period - elapsed_time)


if __name__ == "__main__":
    connection = sqlite3.connect('database.db')
    try:
        update_periodically(connection)
    finally:
        connection.close()
