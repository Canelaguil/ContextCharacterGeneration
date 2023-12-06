import mesa
from mesa import Agent, Model

class Relationship(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)