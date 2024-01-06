from ..utils import *

class CommunityEvents():
    def __init__(self, model, community) -> None:
        self.events = community['community_events']
        self.event_distr = community['community_events_distr']
        self.factions = community['faction_names']
        self.model = model
    
    def trigger(self, event=None, param=None):
        # choose random event if none specified
        if event == None or event not in self.events:
            event = rand_choice(self.events, self.event_distr)

        # execute event
        if event == 'plague': 
            self.plague()
        elif event == 'faction upheaval': 
            self.faction_upheaval(param)
        elif event == 'war':
            self.war()
        elif event == 'famine': 
            self.famine()
        return event

    def plague(self):
        announcement = {
            'topic' : 'event',
            'event' : 'plague'
        }
        self.announce(announcement)
    
    def faction_upheaval(self, faction=None):
        if faction == None:
            f = rand_choice(self.factions)
        announcement = {
            'topic' : 'event',
            'event' : 'faction upheaval',
            'faction' : f
        }
        self.announce(announcement)

    def war(self):
        announcement = {
            'topic' : 'event',
            'event' : 'war'
        }
        self.announce(announcement)


    def famine(self):
        announcement = {
            'topic' : 'event',
            'event' : 'famine'
        }
        self.announce(announcement)

    def announce(self, announcement):
        ...