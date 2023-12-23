from ..utils import *

class Memory:
    def __init__(self, person, model) -> None:
        self.person = person
        self.model = model
        self.events = {}
        self.health_records = {}
        self.health_prev_year = {}

    def add_record(self, record, selective = True):
        # health record
        if selective:
            if record['health'] == self.health_prev_year:
                return
        self.health_records[self.model.year] = record['health']
        self.health_prev_year = record['health']

    def add_event(self, event):
        if self.model.year not in self.events:
            self.events[self.model.year] = []
        self.events[self.model.year].append(event)

    def summary(self):
        records = {
            'health' : self.health_records
        }
        return records