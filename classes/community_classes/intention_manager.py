from ..utils import * 
from mesa import Agent, Model

class Intention_Manager(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)

    """
    Intention management
    """
    def receive_intention(self, person, intention):
        pass

    """
    PHASES
    """
    def people(self):
        pass

    def relationships(self):
        pass

    def houses(self):
        pass

    def post_processing(self):
        pass

    """
    INFO FUNCTIONS
    """



