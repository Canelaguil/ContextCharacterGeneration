from typing import Any
import numpy as np
from mesa import Agent, Model
from mesa.time import StagedActivation
from .city_classes import City, Institutions
from .community_classes import Factions, CommunityEvents
from .person_classes import Naming, Body
from .person import Person
from .relationship import Relationship
from .tests import run_tests


class Community(Model):
    def __init__(self, society, seed, health_stats, aesthetic_seed, 
                 community, institutions, names, testing=True) -> None:
        super().__init__(self)
        self.schedule = StagedActivation(self, ["people", "relationships", "houses"])

        # init the various community components
        self.city = City(self, seed, community)
        self.factions = Factions(community)
        self.institutions = Institutions(institutions)
        self.manager = CommunityEvents(society)
        
        self.set_globals(health_stats, aesthetic_seed, names, society)
        self.init_community(society, aesthetic_seed, health_stats)
        if testing:
            run_tests(self)

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
        Body.average_health = health_stats['average_health']
        Body.health_care_modifier = health_stats['health_care_modifier']
        Body.child_mortality = health_stats['child_mortality']
        Body.disability_ch = health_stats['physical_disability_chance']
        Body.disability_distr = health_stats['physical_disabilities_distribution']
        Body.disability_impact = health_stats['physical_disabilities_health_impact']
        Body.disabilities = health_stats['physical_disabilities']
        Body.old_age = health_stats['old_age']

        # aesthetics
        Body.skin_distr = aesthetic_seed['skin_color_distribution']
        Body.no_skins = len(Body.skin_distr)
        Body.skins = list(range(Body.no_skins))
        Body.hair_colors = aesthetic_seed['hair_colors']
        Body.no_hairs = len(Body.hair_colors)
        Body.hair_type_seed = aesthetic_seed['hair_type_seed']
        Body.dark_hair_distr = np.array(aesthetic_seed['dark_skin_hair_color_distribution'])
        Body.light_hair_distr = np.array(aesthetic_seed['light_skin_hair_color_distribution'])
        Body.eye_colors = aesthetic_seed['eye_colors']
        Body.dark_eye_distr = aesthetic_seed['dark_skin_eye_color_distribution']
        Body.light_eye_distr = aesthetic_seed['light_skin_eye_color_distribution']
    
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
