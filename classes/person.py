import numpy as np
from mesa import Agent, Model
from .home import Home
from .utils import *
from .person_classes import *

class Person(Agent):
    def __init__(self, unique_id: int, model: Model, income_class : int, 
                 mother: dict = {} , father: dict = {}, sex='r', age=0, 
                 first_gen=False) -> None:
        super().__init__(unique_id, model)
        self.community = model
        if sex == 'r': self.sex = 'm' if rand() < Person.bio_mf_ratio else 'f'
        else: self.sex = sex
        self.income_class = income_class
        self.age = age
        self.alive = True

        if first_gen:
            self.names = Naming(self.sex, '', '', '', True)
            self.body = Body(self, {}, {}, True)
        else:
            surnames = [father['surname'], mother['surname']]
            self.names = Naming(self.sex, father['name'], mother['name'], surnames)
            self.body = Body(self, father['genetics'], mother['genetics'])

        self.personality = Personality(self)
        self.network = Network(self)
        self.occupation = Occupation(self, self.income_class)

        if self.sex == 'f':
            self.homsoc = WomanMA(self)
        elif self.sex == 'm':
            self.homsoc = ManMA(self)  
        else: 
            self.homsoc = Neutral(self)

        self.messages = MessageInbox(self)    
        
    """
    PHASES / STEPS
    """
    def people(self):
        self.age += 1
        # print(f"Hi I'm {self.names.full()} and I'm {self.age} years old.")

    def relationships(self): 
        return
    
    def houses(self):
        return

    def post_processing(self):
        return

    """
    UTIL FUNCTIONS
    """        
    def receive_message(self, message):
        self.messages.add(message)

    def description(self) -> dict:
        me = {
            'alive' : self.alive,
            'name' : self.names.first_name(),
            'surname' : self.names.last_name(),
            'full_name' : self.names.full(),
            'sex' : self.sex,
            'age' : self.age,
            'income class' : self.income_class, 
            'personality' : self.personality.get_personality(),
            'homsoc' : self.homsoc.homo_sociologicus(),
            'network' : self.network.links(),
            'occupation' : self.occupation.resume(),
            'genetics' : self.body.pass_gens(), 
        }
        return me

