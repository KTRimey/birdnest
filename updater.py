""" updater.py

This script contains the task for making periodic calls to fetch snapshots 
from the 'birdnest' drone monitoring service and populate the database of 
recent NDZ violators with information served from the /report endpoint of 
the Flask server in 'app.py'.

The file contains the following functions:
    * update_periodically - fetches snapshot and executes update every 2 seconds
    * update - update 'drone' table in database based on snapshot
    * get_snapshot - fetches and parses the xml snapshot
    * get_pilot - fetches pilot information for a particular drone
    * clear_expired - deletes the records of expired violators

Pilot information is only fetched for drones who have violated the NDZ perimeter.
For each violator, a record is kept of when they were last seen, pilot information, and 
their closest violation of the NDZ.
Information on violators is kept for 10 minutes since their drone was last seen anywhere.

"""

import sqlite3
import requests
import logging
import xml.etree.ElementTree as ET
from dateutil import parser
from datetime import timedelta
import time
import math

EXPIRATION = timedelta(seconds=600)
NEST_POSITION = (250000, 250000)
NO_FLY_RADIUS = 100000


def get_snapshot():
    """fetch and parse drones snapshot"""

    url = 'https://assignments.reaktor.com/birdnest/drones'
    response = requests.get(url, headers={'accept': 'application/xml'})
    response.raise_for_status()

    root = ET.fromstring(response.text)
    timestamp = root[1].get('snapshotTimestamp')

    drone_distances = {}
    for drone in root.iter('drone'):
        drone_id = drone.find('serialNumber').text
        position = float(drone.find('positionX').text), float(
            drone.find('positionY').text)
        drone_distances[drone_id] = math.dist(position, NEST_POSITION)

    return (parser.parse(timestamp), drone_distances)


def get_pilot(serial_number):
    """fetch pilot info for violating drone"""

    url = f'https://assignments.reaktor.com/birdnest/pilots/{serial_number}'
    response = requests.get(url, headers={'accept': 'application/json'})
    if response.status_code == 404:
        return {}
    response.raise_for_status()

    return response.json()


def update(con, timestamp, drone_distances):
    """update database of violating drones based on snapshot"""

    known_violators = set(id for id, in con.execute(
        "SELECT drone_id FROM drone").fetchall())

    pilot_information = {}
    for drone_id, distance_from_nest in drone_distances.items():
        # fetch pilot information for violating, unknown drones
        if distance_from_nest <= NO_FLY_RADIUS and drone_id not in known_violators:
            pilot_information[drone_id] = get_pilot(drone_id)

    for drone_id, distance_from_nest in drone_distances.items():
        if drone_id in known_violators:
            # update time last seen
            con.execute(
                "UPDATE drone SET last_seen=? WHERE drone_id=?", (timestamp, drone_id))

        if distance_from_nest <= NO_FLY_RADIUS:
            # drone is in violation
            if drone_id not in known_violators:
                # create record for new drone
                pilot = pilot_information.get(drone_id)
                violator = (drone_id, distance_from_nest, timestamp, pilot.get('firstName'), pilot.get('lastName'),
                            pilot.get('phoneNumber'), pilot.get('email'))
                con.execute(
                    "INSERT INTO drone VALUES(?, ?, ?, ?, ?, ?, ?)", violator)
            else:
                # update closest approach
                closest, = con.execute(
                    "SELECT closest_approach FROM drone WHERE drone_id=?", (drone_id,)).fetchone()
                if distance_from_nest < closest:
                    con.execute(
                        "UPDATE drone SET closest_approach=? WHERE drone_id=?", (distance_from_nest, drone_id))


def clear_expired(con, latest_snapshot_timestamp):
    """delete record of violator if the drone has not been seen for some time"""

    violators = con.execute("SELECT drone_id, last_seen FROM drone").fetchall()

    for drone_id, last_seen in violators:
        time_since = (latest_snapshot_timestamp - parser.parse(last_seen))
        if time_since >= EXPIRATION:
            con.execute("DELETE FROM drone WHERE drone_id=?", (drone_id,))


def update_periodically(connection, period=2):
    """execute update task every 2 seconds"""
    while True:
        start_time = time.time()
        try:
            with connection:
                timestamp, drone_distances = get_snapshot()
                update(connection, timestamp, drone_distances)
                clear_expired(connection, timestamp)
        except Exception as e:
            logging.exception(e)

        elapsed_time = time.time() - start_time
        if elapsed_time < period:
            time.sleep(period - elapsed_time)


if __name__ == '__main__':
    connection = sqlite3.connect('database.db')
    try:
        update_periodically(connection)
    finally:
        connection.close()
