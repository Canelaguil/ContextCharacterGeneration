from mesa import Model
from ..relationship import Relationship

class FullPlatonic(Relationship):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)