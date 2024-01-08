from typing import Any
import numpy as np
import json
import shutil
import os
from mesa import Agent, Model
from mesa.time import StagedActivation
from .utils import *
from .city_classes import *
from .community_classes import *
from .person_classes import *
from .person import Person
from .home import Home
from .relationship import Relationship
from .relationship_classes import Romance
from .tests import run_tests

def set_globals(health_stats, aesthetic_seed, names, society, community):
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
        HomoSociologicus.male_for_indepenence = society['male_meant_for_independence']
        HomoSociologicus.female_for_indepenence = society['female_meant_for_independence']
        Occupation.adult_age = society['male_meant_for_independence']
        Home.person_income_percentage = community['class_person_household_percentage']
        
        # relationships
        Person.can_divorce = society['divorce']
        Person.can_marry = society['marriage']
        Person.equal_rights = society['same_sex_marriage']
        Person.adult_age_women = society['marriage_age_women']
        Person.adult_age_men = society['marriage_age_men']
        Body.adult_age = society['marriage_age_men']
        Romance.can_divorce = society['divorce']
        Romance.can_marry = society['marriage']
        Romance.equal_rights = society['same_sex_marriage']
        HomoSociologicus.marriage_age_women = society['marriage_age_women']
        HomoSociologicus.marriage_age_men = society['marriage_age_men']


class Community(Model):
    def __init__(self, society, seed, health_stats, aesthetic_seed, 
                 community, institutions, names, testing=True, year=1200) -> None:
        super().__init__(self)
        set_globals(health_stats, aesthetic_seed, names, society, community)

        # stat trackers
        self.ids = 10000 # TODO : find consistent system?
        self.births = 0
        self.male_births, self.female_births = 0, 0
        self.deaths = 0
        self.marriages = 0
        self.people_alive = 0

        self.schedule = StagedActivation(self, ["people", "lovedeathbirth", "houses", 
                                                "post_processing"], True)
        self.year = year
        self.people = {}
        self.homes = {}
        self.relationships = {}
        self.whoknowswho = {} # person_key : [list of acquaintances]

        # init the various community components
        self.city = City(self, seed, community)
        self.factions = Factions(community)
        self.institutions = Institutions(institutions)
        self.community_events = CommunityEvents(self, community)
        self.intention_manager = Intention_Manager(0, self)
        self.init_community(society, seed)

        if testing:
            run_tests(self)

    """
    INIT FUNCTIONS
    """
    def init_community(self, society, seed):
        for hk, h in self.homes.items():
            if rand() < seed['percentage_inhabited_houses']: 
                income_class = h.income_class
                m, w = self.make_couple(income_class, h.address())
                self.add_person_to_home(hk, m)
                self.add_person_to_home(hk, w)

    def make_couple(self, income_class, home_address):
        max_age = Body.old_age # Person.adult_age_men + int((Body.old_age - Person.adult_age_men) * 0.6)
        man_age = rand_int(max_age, Person.adult_age_men)
        faction = self.factions.assign_faction()
        man = Person(self.get_id(), self, self.year, income_class, faction,'firstgen', 
                     'm', man_age, True )
        woman_age = rand_int(man_age, Person.adult_age_women)
        woman = Person(self.get_id(), self, self.year, income_class, faction, 'firstgen',
                       'f', woman_age, True)
        self.add_person(man)
        self.add_person(woman)
        marriage = Relationship(self.get_id(), self, man.description(),
                                woman.description(), 'spouse')
        marriage.set_home(home_address['unique id'])
        self.add_relationship(marriage)
        return (man.unique_id, woman.unique_id)

    """
    INPUT FUNCTIONS
    """
    def add_person(self, person : Agent):
        self.people_alive += 1
        # everyone knows themselves
        if not person.unique_id in self.whoknowswho:
            self.whoknowswho[person.unique_id] = []
        self.whoknowswho[person.unique_id].append(person.unique_id)
        self.people[person.unique_id] = person
        self.schedule.add(person)

    def add_home(self, home : Agent):
        self.homes[home.unique_id] = home
        self.schedule.add(home)

    def add_person_to_home(self, house_key, person_key):
        person_info = self.people[person_key].description()
        self.homes[house_key].add_person(person_info)

    def move_person_to_home(self, house_key, person_key):
        person_info = self.people[person_key].description()
        try:
            if person_info['home'] != None: # like for newborns
                old_home = person_info['home']['unique id']
                self.homes[old_home].remove_person(person_info)
        except:
            log_error('could not move person', [house_key, person_info])
        self.homes[house_key].add_person(person_info)
        house_info = self.homes[house_key].address()
        self.people[person_key].move(house_info)

    def add_relationship(self, relat : Agent):
        a, b = relat.keys
        if not a in self.whoknowswho:
            self.whoknowswho[a] = []
        if not b in self.whoknowswho:
            self.whoknowswho[b] = []
        self.whoknowswho[a].append(b)
        self.whoknowswho[b].append(a)
        self.relationships[relat.unique_id] = relat 
        self.schedule.add(relat)

    def marry(self, keyA, keyB, type='spouse'):
        self.marriages += 1
        personA = self.get_person(keyA)
        personB = self.get_person(keyB)
        marriage = Relationship(self.get_id(), self, personA, personB, type)
        self.add_relationship(marriage)

        # TODO : could be moved to community events?
        # add spouse to house of other spouse (MA inclination for moving in with husband)
        husband = personA if personA['sex'] == 'm' else personB
        wife = personA if personA['sex'] == 'f' else personB

        ch = rand()
        if (husband['home'] != None and ch < 0.8) or wife['home'] == None :
            couple_home = husband['home']
            try:
                if wife['home']['unique id'] == None:
                    return
            except:
                beautify_print(wife)
                fatal_error(wife['home'])
            care_dependants = self.homes[wife['home']['unique id']].get_my_children(wife)
            self.move_person_to_home(couple_home['unique id'], wife['key'])
        elif wife['home'] != None:
            couple_home = wife['home']
            try:
                if husband['home']['unique id'] == None:
                    return
            except:
                beautify_print(husband)
                fatal_error(husband['home'])
            care_dependants = self.homes[husband['home']['unique id']].get_my_children(husband)

            self.move_person_to_home(couple_home['unique id'], husband['key'])
        else:
            log_error('no home found in couple', [keyA, keyB])
            # if either or both of the houses are not available (because person died this year, eg)
            return
        
        marriage.set_home(couple_home['unique id'])
        for person in care_dependants:
            self.move_person_to_home(couple_home['unique id'], person)

    def create_relationship(self, personA_key, personB_key, label, 
                            platonic_only=False):
        personA = self.get_person(personA_key)
        personB = self.get_person(personB_key)
        u_id = self.get_id()
        r = Relationship(u_id, self, personA, personB, label, platonic_only)
        self.add_relationship(r)
        return u_id

    def express_intention(self, intention):
        self.intention_manager.receive_intention(intention)

    def birth_child(self, relationship_key, income_class, faction):
        self.births += 1
        parent_info = self.get_relationship(relationship_key)
        unique_id = self.get_id()
        child = Person(unique_id, self, self.year, income_class, faction, 
                       parent_info)
        if child.sex == 'f':
            self.female_births += 1
        else:
            self.male_births += 1
        self.add_person(child)
        return child.description()
    
    def report_death(self, key):
        self.people_alive -= 1
        self.deaths += 1
        self.schedule.remove(self.people[key])

    
    """
    MESSAGE FUNCTIONS
    """
    def message_person(self, key, msg):
        self.people[key].receive_message(msg)

    def message_all_living_people(self, msg):
        for key, p in self.people.items():
            if p.alive:
                self.message_person(key, msg)

    def message_home(self, key, msg):
        self.homes[key].receive_message(msg)

    def message_relationship(self, key, msg):
        try:
            self.relationships[key].receive_message(msg)
        except:
            print('in relationship messaging')
            print(f"key: {key}")
            fatal_error(msg)

    """
    SIMULATION FUNCTIONS
    """
    def step(self):
        # check if a historical event happens this year
        happenings = self.community_events.something_happens(self.year)
        if happenings != []:
            print(f"Events in {self.year}: {happenings}.")

        self.schedule.step()

    def run(self, years, output=False):
        # add intention manager to schedule (unique ID=0)
        self.schedule.add(self.intention_manager)

        # run simulation
        for _ in range(years):
            self.step()
            if output:
                print(f"~{self.year}~")
                print(f"Currently {self.people_alive} are alive in the city.\nStats this year:")
                print(f"births : {self.male_births + self.female_births}")
                print(f"deaths : {self.deaths}")
                print(f"marriages : {self.marriages}")
                print('------------------------')
            # record stats and reset
            self.intention_manager.receive_stats(self.male_births, self.female_births, 
                                                    self.deaths, self.marriages, self.people_alive)
            self.year += 1 
            self.births = 0
            self.deaths = 0
            self.female_births, self.male_births = 0, 0
            self.marriages = 0
        print("SIMULATION STATS")
        print(f"- {years} years")
        print(f"- {len(self.people)} people")
        print(f"- {len(self.relationships)} relationships")
        print(f"- {len(self.homes)} homes")
        print(f'- {self.schedule.get_agent_count()} active agents')
        global errors
        if errors != {}:
            print("Errors were logged in output/errors.json")
        # self.city.stats(True)

    """
    OUTPUT FUNCTIONS
    """
    def get_person(self, key):
        return self.people[key].description()
    
    def get_person_short(self, key):
        return self.people[key].whoisthis()
    
    def get_person_summary(self, key): 
        return self.people[key].in_short()
    
    def get_home(self, key):
        return self.homes[key].info()
    
    def get_relationship(self, key):
        return self.relationships[key].status()
    
    def get_relationship_status_person(self, key):
        return self.people[key].get_relationship_status()
    
    def we_know_each_other(self, keyA, keyB):
        if keyA not in self.whoknowswho:
            log_error('knows no one', keyA)
            return False
        return keyB in self.whoknowswho[keyA]

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
        print('Creating output files...')
        # remove existing generation to start fresh (so save communities you like!!)
        if os.path.exists('output/people_json'):
            shutil.rmtree('output/people_json')
        os.mkdir('output/people_json')
        if os.path.exists('output/relationships_json'):
            shutil.rmtree('output/relationships_json')
        os.mkdir('output/relationships_json')

        for key, p in self.people.items():
            with open(f"output/people_json/{key}.json", 'w') as output:
                json.dump({f'{key}' : p.description()}, output, indent=2, separators=(',', ': '))

        if not os.path.exists('output/homes_json'):
            os.mkdir('output/homes_json')
        for key, h in self.homes.items():
            with open(f"output/homes_json/{key}.json", 'w') as output:
                json.dump({key : h.info()}, output, indent=2, separators=(',', ': '))

        if not os.path.exists('output/relationships_json'):
            os.mkdir('output/relationships_json')
        for key, r in self.relationships.items():
            with open(f"output/relationships_json/{key}.json", 'w') as output:
                json.dump({key : r.status()}, output, indent=2, separators=(',', ': '))

        with open('output/stats.json', 'w') as output:
            dems = self.intention_manager.demographics()
            json.dump(dems, output)

        global errors
        if errors != {}:
            output_errors()
        print('Done!')

        # useful tool when json dump gives errors:
        # print_dict_types(self.homes[2].info())
