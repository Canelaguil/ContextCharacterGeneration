from ..utils import *

class Memory:
    def __init__(self, person, model):
        self.person = person
        self.model = model
        self.events = {}
        self.health_records = {}
        self.occupation_records = {}
        self.homsoc_records = {}

        # in order to only record changes (occupation changes yearly, so not tracked)
        self.health_prev_year = {}
        self.homsoc_prev_year = {}

    def add_record(self, record : dict):
        """
        Saves reports from support classes as records as opposed to
        events. Only save records if something changed
        """
        y = self.model.get_year()
        
        if record['health'] != self.health_prev_year:
            self.health_records[y] = record['health']
            self.health_prev_year = record['health']

        if record['homsoc'] != self.homsoc_prev_year:
            self.homsoc_records[y] = record['homsoc']
            self.homsoc_prev_year = record['homsoc']

        self.occupation_records[y] = record['occupation']

    def add_event(self, event : dict):
        """
        Adds event to memory
        """
        yr = self.model.get_year()
        if yr not in self.events:
            self.events[yr] = []
        self.events[yr].append(event)

    def summary(self):
        """
        Overview of records
        """
        records = {
            'health' : self.health_records,
            'homsoc' : self.homsoc_records,
            'ocupation' : self.occupation_records,
            'events' : self.events
        }
        return records
    
