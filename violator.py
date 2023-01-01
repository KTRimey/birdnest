from json import JSONEncoder


class Violator:
    def __init__(self, closest_approach, last_seen, name=None, phone=None, email=None):
        self.closest_approach = closest_approach
        self.last_seen = last_seen
        self.name = name
        self.phone = phone
        self.email = email

    def set_closest_approach(self, closest_approach):
        self.closest_approach = closest_approach

    def set_last_seen(self, last_seen):
        self.last_seen = last_seen

    def get_closest_approach(self):
        return self.closest_approach

    def get_last_seen(self):
        return self.last_seen


class ViolatorEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
