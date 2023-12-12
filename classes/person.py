import numpy as np
from mesa import Agent, Model
from .home import Home
from .person_classes import Personality, Naming

class Person(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)
        self.names = Naming('m', 'Jack', 'Femke', '', True)

    def step(self):
        pass

