import numpy as np
from mesa import Agent, Model
from .home import Home
from numpy import random
from .person_classes import Personality, Naming, Body, Network, WomanMA, ManMA, Neutral

class Person(Agent):
    def __init__(self, unique_id: int, model: Model, income_class : int, 
                 mother: dict = {} , father: dict = {}, sex='r', age=0, 
                 first_gen=False) -> None:
        super().__init__(unique_id, model)
        if sex == 'r': self.sex = 'm' if random.random() < Person.bio_mf_ratio else 'f'
        else: self.sex = sex
        self.income_class = income_class
        self.age = age

        if first_gen:
            self.names = Naming(self.sex, '', '', '', True)
            self.body = Body({}, {}, True)
        else:
            surnames = [father['surname'], mother['surname']]
            self.names = Naming(self.sex, father['name'], mother['name'], surnames)
            self.body = Body(father['genetics'], mother['genetics'])

        self.personality = Personality()
        self.network = Network()

        if self.sex == 'f':
            self.homsoc = WomanMA()
        elif self.sex == 'm':
            self.homsoc = ManMA()  
        else: 
            self.homsoc = Neutral()     
        
    def step(self):
        pass

    def description(self):
        me = {
            'name' : self.names.name,
            'surname' : self.names.surname,
            'sex' : self.sex,
            'income class' : self.income_class, 
            'full_name' : self.names.full(),
            'genetics' : self.body.pass_gens(), 
            'personality' : self.personality.get_personality(),

        }
        return me

    
