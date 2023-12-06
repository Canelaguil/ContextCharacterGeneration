import numpy as np
from mesa import Agent, Model
from city_classes import City, Institutions
from community_classes import Factions


class Community(Model):
    def __init__(self, society, population_seed, health_stats, aesthetic_seed, 
                 community, institutions) -> None:
        # information for other classes
        # self.config = {
        #     'health' : health_stats,
        #     'aesthetics' : aesthetic_seed,
        #     # 'community' : community,
        #     # 'institutions' : institutions
        # }
        self.city = City(population_seed, community)
        self.factions = Factions(community)
        self.institutions = Institutions(institutions)

        self.init_community(society, aesthetic_seed, health_stats)

    def init_community(self, society, aesthetic_seed, health_stats):
        pass

    def run(self, years, output=True):
        pass

    def json_output(self):
        pass
