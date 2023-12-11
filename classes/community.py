from typing import Any
import numpy as np
from mesa import Agent, Model
from mesa.time import StagedActivation
from .city_classes import City, Institutions
from .community_classes import Factions, CommunityEvents
from .person_classes import Naming
from .person import Person
from .relationship import Relationship


class Community(Model):
    def __init__(self, society, seed, health_stats, aesthetic_seed, 
                 community, institutions, names) -> None:
        super().__init__(self)
        self.schedule = StagedActivation(self, ["people", "relationships", "houses"])

        # init the various community components
        self.city = City(self, seed, community)
        self.factions = Factions(community)
        self.institutions = Institutions(institutions)
        self.manager = CommunityEvents(society)
        
        self.set_globals(health_stats, aesthetic_seed, names, society)

        test = Person(3, self)

        self.init_community(society, aesthetic_seed, health_stats)

    """
    INIT FUNCTIONS
    """
    def set_globals(self, health_stats, aesthetic_seed, names, society):
        # names
        Naming.surnames = names[2]
        Naming.female_names = names[1]
        Naming.male_names = names[0]
        Naming.system = society['name_system']

        # health
        Person.bio_mf_ratio = health_stats['bio_male_female_ratio']
        Person.average_health = health_stats['average_health']
        Person.health_care_modifier = health_stats['health_care_modifier']
        Person.child_mortality = health_stats['child_mortality']
        Person.disability_ch = health_stats['physical_disability_chance']
        Person.disability_distr = health_stats['physical_disabilities_distribution']
        Person.disability_impact = health_stats['physical_disabilities_health_impact']
        Person.disabilities = health_stats['physical_disabilities']
        Person.old_age = health_stats['old_age']

        # aesthetics
        Person.skin_distr = aesthetic_seed['skin_color_distribution']
        Person.hair_colors = aesthetic_seed['hair_colors']
        Person.dark_hair_distr = aesthetic_seed['dark_skin_hair_color_distribution']
        Person.light_hair_distr = aesthetic_seed['light_skin_hair_color_distribution']
        Person.eye_colors = aesthetic_seed['eye_colors']
        Person.dark_eye_distr = aesthetic_seed['dark_skin_eye_color_distribution']
        Person.light_eye_distr = aesthetic_seed['light_skin_eye_color_distribution']
    
        # people
        Person.male_for_indepenence = society['male_meant_for_independence']
        Person.female_for_indepenence = society['female_meant_for_independence']

        # relationships
        Person.can_divorce = society['divorce']
        Person.can_marry = society['marriage']
        Person.equal_rights = society['same_sex_marriage']
        Person.marriage_age_women = society['marriage_age_women']
        Person.marriage_age_men = society['marriage_age_men']
        Relationship.can_divorce = society['divorce']
        Relationship.can_marry = society['marriage']
        Relationship.equal_rights = society['same_sex_marriage']
        Relationship.marriage_age_women = society['marriage_age_women']
        Relationship.marriage_age_men = society['marriage_age_men']

    def init_community(self, society, aesthetic_seed, health_stats):
        pass

    """
    SIMULATION FUNCTIONS
    """
    def step(self):
        pass

    def run(self, years, output=True):
        pass

    """
    OUTPUT FUNCTIONS
    """
    def json_output(self):
        pass
