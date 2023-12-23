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
        self.health_records[self.model.get_year()] = record['health']
        self.health_prev_year = record['health']

    def add_event(self, event):
        yr = self.model.get_year()
        if yr not in self.events:
            self.events[yr] = []
        self.events[yr].append(event)

    def summary(self):
        records = {
            'health' : self.health_records,
            'events' : self.events
        }
        return records