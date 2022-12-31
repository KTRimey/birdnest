import json


class Violator:

    def __init__(self, last_seen, closest_approach, name=None, phone=None, email=None):
        self.last_seen = last_seen
        self.closest_approach = closest_approach
        self.name = name
        self.phone = phone
        self.email = email
