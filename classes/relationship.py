from .utils import *
from mesa import Agent, Model

class Relationship(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)

    """
    PHASES / STEPS
    """
    def people(self):
        return        

    def relationships(self): 
        return
    
    def houses(self):
        return

    def post_processing(self):
        return
    
    """
    UTILS
    """

    def status(self):
        return {
            
        }
    
    def receive_message(self, msg):
        return
    
