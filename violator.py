from json import JSONEncoder


class Violator:
    def __init__(self, closest_approach, last_seen, name=None, phone=None, email=None):
        self.closest_approach = closest_approach
        self.last_seen = last_seen
        self.name = name
        self.phone = phone
        self.email = email


class ViolatorEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
