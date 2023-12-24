import numpy as np
from mesa import Agent, Model
from .home import Home
from .utils import *
from .person_classes import *

class Person(Agent):
    def __init__(self, unique_id: int, model: Model, birth_year : int, income_class : int,
                 mother: dict = {} , father: dict = {}, siblings=[], sex='r', age=0, 
                 first_gen=False) -> None:
        super().__init__(unique_id, model)
        self.community = model
        self.birth_year = birth_year
        if age != 0:
            self.birth_year -= age
        self.born_this_way(sex)
        self.income_class = income_class
        self.home = None
        self.age = age
        self.alive = True
        self.first_gen = first_gen

        if self.first_gen:
            self.names = Naming(self.sex, '', '', '', True)
            self.body = Body(self, {}, {}, True)
        else:
            surnames = [father['surname'], mother['surname']]
            self.names = Naming(self.sex, father['name'], mother['name'], 
                                surnames)
            self.body = Body(self, father['genetics'], mother['genetics'])

        self.personality = Personality(self)
        self.network = Network(self, model, mother, father)
        # if not self.first_gen:
        #     self.network.siblings = siblings
        self.occupation = Occupation(self, self.income_class)

        if self.sex == 'f':
            self.homsoc = WomanMA(self, self.get_homsoc_attributes(), 
                                  self.personality.get_personality())
        elif self.sex == 'm':
            self.homsoc = ManMA(self, self.get_homsoc_attributes(), 
                                  self.personality.get_personality())  
        else: 
            self.homsoc = Neutral(self, self.get_homsoc_attributes(), 
                                  self.personality.get_personality())

        self.messages = MessageInbox(self)
        self.memory = Memory(self, self.model) 
    
    def born_this_way(self, sex):
        """
        Define sex, gender & sexuality
        """
        # sex
        if sex == 'r': self.sex = 'm' if rand() < Person.bio_mf_ratio else 'f'
        else: self.sex = sex

        # sexuality
        # primary sexuality is the label, secondary the "place on the spectrum"
        self.primary_sexuality = rand_choice(['straight', 'bi', 'gay'], 
                                             p=[0.8, 0.1, 0.1])
        
        loc, scale = {'straight' : (0.05, 0.05), 
                      'bi' : (0.5, 0.1), 
                      'gay' : (0.9, 0.05)}[self.primary_sexuality]
        self.secondary_sexuality = normal_in_range(loc, scale)
        self.romance_interest = normal_in_range(0.7, 0.15)
        self.sex_interest = normal_in_range(0.7, 0.15)

        # gender expression
        # the assumption here is that knowing you're not straight makes you more 
        # open to the possiblity you might not be cis either
        if self.primary_sexuality == 'straight' : 
            loc2, scale2 = (0.1, 0.1)
        else:
            loc2, scale2 = (0.3, 0.2)
        self.gender_expression = normal_in_range(loc2, scale2) # 0 = 1-1 with sex

    def die(self):
        self.alive = False
        self.network.unravel()
        self.community.report_death(self.unique_id)

    """
    PHASES / STEPS
    """
    def people(self):
        if self.alive:
            self.age += 1

            # health update
            health_report = self.body.yearly_step(self.age)
            if health_report['death']:
                self.die()


            record = {
                'health' : health_report,
            }

            self.memory.add_record(record)
            # if not self.first_gen:
                # print(f"Hi I'm {self.names.full()} and I'm {self.age} years old.")

    def relationships(self): 
        return
    
    def houses(self):
        return

    def post_processing(self):
        msg = self.messages.get()
        while msg != None:
            topic = msg['topic']
            if topic == 'new child':
                self.network.add_child(msg['child key'], msg['kind'])
                self.memory.add_event(msg)
                if self.sex == 'f' : # add child to mother's home
                    self.community.add_person_to_home(self.home['unique id'], 
                                                      msg['child key'])
            elif topic == 'new relationship': 
                self.network.add_relationship(msg['key'], msg['people'])
                self.memory.add_event(msg)
            elif topic == 'new sibling': 
                self.network.add_sibling(msg['child key'], msg['kind'])
                self.memory.add_event(msg)
            elif topic == 'person died':
                self.memory.add_event(msg)
            elif topic == 'new home': 
                self.move(msg['home'])
            msg = self.messages.get()

    """
    UTIL FUNCTIONS
    """        
    def receive_message(self, msg):
        if self.alive:
            self.messages.add(msg)
        else:
            # if person not alive, add only certain info and add directly
            posthumous_info = ['new sibling']
            topic = msg['topic']
            if topic in posthumous_info:         
                if topic == 'new sibling' :    
                    self.network.add_sibling(msg['child key'], msg['kind'])

    def move(self, home_info):
        self.home = home_info

    """
    INFO FUNCTIONS
    """

    def get_homsoc_attributes(self):
        return {
            'sexuality label' : self.primary_sexuality,
            'sexuality' : self.secondary_sexuality, 
            'romantic interest' : self.romance_interest,
            'sex interest' : self.sex_interest, 
            'gender expression' : self.gender_expression,
            'sex' : self.sex,
        }
    
    def whoisthis(self):
        """
        Short summary for descriptive purposes
        """
        return {
            'key' : self.unique_id, 
            'name' : self.names.full(),
            'age' : self.age,
            'alive' : self.alive,
            'sex' : self.sex, 
            'parents' : self.network.get_parents()
        }

    def description(self) -> dict:
        """
        Long description for json objects
        """
        me = {
            'alive' : self.alive,
            'name' : self.names.first_name(),
            'surname' : self.names.last_name(),
            'full_name' : self.names.full(),
            'born this way' : self.get_homsoc_attributes(),
            'age' : self.age,
            'birth year' : self.birth_year,
            'sex' : self.sex,
            'income class' : self.income_class, 
            'personality' : self.personality.get_personality(),
            'attitude' : self.personality.get_attitude(),
            'homsoc' : self.homsoc.homo_sociologicus(),
            'network' : self.network.links(),
            'occupation' : self.occupation.resume(),
            'genetics' : self.body.pass_gens(), 
            'memory' : self.memory.summary(),
            'key' : self.unique_id,
            'home' : self.home
        }
        return me
    

