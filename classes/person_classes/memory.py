from ..utils import *

class Memory:
    def __init__(self, person, model) -> None:
        self.person = person
        self.model = model
        self.records = {}
        self.prev_year = {}

    def add_record(self, record, selective = True):
        if selective:
            if record == self.prev_year:
                return
        self.records[self.model.year] = record
        self.prev_year = record

    def summary(self):
        return self.records