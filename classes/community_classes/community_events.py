from ..utils import *

class CommunityEvents():
    """
    Makes community events happen either at random or as planned
    """
    def __init__(self, model, community) -> None:
        self.events = community['community_events']
        self.event_distr = community['community_events_distr']
        self.yearly_chance = community['comunnity_events_yearly_chance']
        self.factions = community['faction_names']
        self.model = model

        # save years in which events will happen for sure
        self.fixed_events = {}
        for i, e in enumerate(self.events):
            for y in community['community_fixed_events'][i]: 
                if y not in self.fixed_events:
                    self.fixed_events[y] = []
                self.fixed_events[y].append(e)
    
    def trigger(self, event=None, param=None):
        """
        Trigger specific community happening
        """
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

    def dictated_history(self, year):
        """
        Check for the dictated events this year
        """
        self.year = year
        if year in self.fixed_events:
            return self.fixed_events[year]
        return []
    
    def something_happens(self, year):
        """
        Yearly evolve step: check if something is meant to happen, have something
        happen by chance (might be double!)
        """
        self.year = year
        # if something is meant to happen this year, make it happen
        history_book = self.dictated_history(year)
        if history_book != []:
            for e in history_book:
                self.trigger(e)
        # check for chance of something random happening (this could also be an else statement)
        if rand() < self.yearly_chance:
            event = self.trigger()

            # avoid same event happening twice in a year (not necessary)
            if event not in history_book:
                history_book.append(event)
        return history_book
        

    """
    THE EVENTS
    """

    def plague(self):
        """
        Announce plague to community
        """
        announcement = {
            'topic' : 'event',
            'event' : 'plague', 
            'year' : self.year
        }
        self.announce(announcement)
    
    def faction_upheaval(self, faction=None):
        """
        Announce faction upheaval to community
        """
        if faction == None:
            f = rand_choice(self.factions)
        announcement = {
            'topic' : 'event',
            'event' : 'faction upheaval',
            'faction' : f, 
            'year' : self.year
        }
        self.announce(announcement)

    def war(self):
        """
        Announce war to community
        """
        announcement = {
            'topic' : 'event',
            'event' : 'war', 
            'year' : self.year
        }
        self.announce(announcement)

    def famine(self):
        """
        Announce famine to community
        """
        announcement = {
            'topic' : 'event',
            'event' : 'famine', 
            'year' : self.year
        }
        self.announce(announcement)

    def announce(self, announcement):
        """
        Announce the current disaster to community
        """
        self.model.message_all_living_people(announcement)
        