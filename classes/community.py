from typing import Any
import numpy as np
import json
import shutil
import os
from mesa import Agent, Model
from mesa.time import StagedActivation
from .utils import *
from .city_classes import City, Institutions
from .community_classes import Factions, CommunityEvents
from .person_classes import Naming, Body
from .person import Person
from .relationship import Relationship
from .tests import run_tests

def set_globals(health_stats, aesthetic_seed, names, society):
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
        Body.all_disabilities = health_stats['physical_disabilities']
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


class Community(Model):
    def __init__(self, society, seed, health_stats, aesthetic_seed, 
                 community, institutions, names, testing=True, year=1200) -> None:
        super().__init__(self)
        set_globals(health_stats, aesthetic_seed, names, society)
        self.ids = 10000
        self.schedule = StagedActivation(self, ["people", "relationships", "houses", "post_processing"], True)
        self.year = year
        self.people = {}
        self.homes = {}
        self.relationships = {}

        # init the various community components
        self.city = City(self, seed, community)
        self.factions = Factions(community)
        self.institutions = Institutions(institutions)
        self.manager = CommunityEvents(society)
        self.init_community(society, aesthetic_seed, health_stats)
        if testing:
            run_tests(self)

    """
    INIT FUNCTIONS
    """
    def init_community(self, society, aesthetic_seed, health_stats):
        # test = Person(self.get_id(), self, 2, {}, {}, 'r', 20, True)
        # self.add_person(test)        
        for _ in range(4):
            self.make_couple()

    def make_couple(self):
        man = Person(self.get_id(), self, self.year, 2, {}, {}, 'm', 25, True )
        woman = Person(self.get_id(), self, self.year, 2, {}, {}, 'f', 22, True)
        self.add_person(man)
        self.add_person(woman)
        marriage = Relationship(self.get_id(), self, man.description(),
                                woman.description(), 'arranged marriage')
        self.add_relationship(marriage)

    """
    INPUT FUNCTIONS
    """
    def add_person(self, person : Agent):
        self.people[person.unique_id] = person
        self.schedule.add(person)

    def add_home(self, home : Agent):
        self.homes[home.unique_id] = home
        self.schedule.add(home)

    def add_person_to_home(self, house_key, person_key):
        person_info = self.people[person_key]
        self.homes[house_key].add_person(person_info)

    def add_relationship(self, relat : Agent):
        self.relationships[relat.unique_id] = relat 
        self.schedule.add(relat)

    def birth_child(self, key_father, key_mother):
        father = self.get_person(key_father)
        mother = self.get_person(key_mother)
        unique_id = self.get_id()
        child = Person(unique_id, self, self.year, father['income class'], mother, 
                       father, age=0)
        self.add_person(child)
        return child.description()

    
    """
    MESSAGE FUNCTIONS
    """
    def message_person(self, key, msg):
        self.people[key].receive_message(msg)

    def message_home(self, key, msg):
        self.homes[key].receive_message(msg)

    def message_relationship(self, key, msg):
        self.relationships[key].receive_message(msg)

    """
    SIMULATION FUNCTIONS
    """
    def step(self):
        self.schedule.step()

    def run(self, years, output=False):
        for _ in range(years):
            if output:
                pass
                # print(self.year)
            self.step()
            self.year += 1 
        print("SIMULATION STATS")
        print(f"- {years} years")
        print(f"- {len(self.people)} people")
        print(f"- {len(self.relationships)} relationships")
        print(f"- {len(self.homes)} homes")
        print(f'- {self.schedule.get_agent_count()} active agents')
        # self.city.stats(True)

    """
    OUTPUT FUNCTIONS
    """
    def get_person(self, key):
        return self.people[key].description()
    
    def get_person_short(self, key):
        return self.people[key].whoisthis()
    
    def get_home(self, key):
        return self.homes[key].info()
    
    def get_relationship(self, key):
        return self.relationships[key].status()

    def get_year(self):
        return self.year
    
    def get_id(self):
        self.ids += 1
        return self.ids - 1

    def get_people(self):
        return [p.description() for p in self.people.values()]
    
    def get_homes(self):
        return [h.info() for h in self.homes.values()]

    def relationships(self):
        return [r.status() for r in self.relationships.values()]

    def json_output(self):
        """
        Output all agent info into json files. Deletes all previous files.
        """
        # remove existing generation to start fresh (so save communities you like!!)
        if os.path.exists('output/people_json'):
            shutil.rmtree('output/people_json')
        os.mkdir('output/people_json')

        for key, p in self.people.items():
            with open(f"output/people_json/{key}.json", 'w') as output:
                json.dump({f'{key}' : p.description()}, output)

        if not os.path.exists('output/homes_json'):
            os.mkdir('output/homes_json')
        for key, h in self.homes.items():
            with open(f"output/homes_json/{key}.json", 'w') as output:
                json.dump({key : h.info()}, output)

        if not os.path.exists('output/relationships_json'):
            os.mkdir('output/relationships_json')
        for key, r in self.relationships.items():
            with open(f"output/relationships_json/{key}.json", 'w') as output:
                json.dump({key : r.status()}, output)

        # useful tool when json dump gives errors:
        # print_dict_types(self.homes[2].info())
        

