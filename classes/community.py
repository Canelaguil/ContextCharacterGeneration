import numpy as np
import mesa
from city_classes import City
from community_classes import *


class Community(mesa.Model):
    def __init__(self, simulation, population_seed, health_stats, aesthetic_seed, 
                 community, institutions) -> None:
        self.steps = simulation['number_of_years']
        self.terminal_output = simulation['simulation_output']
        self.json_output = simulation['json_output']

        # information for other classes
        self.config = {
            'health' : health_stats,
            'aesthetics' : aesthetic_seed,
            'community' : community,
            'institutions' : institutions
        }

        self.city = City()