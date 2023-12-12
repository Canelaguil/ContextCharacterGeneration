from mesa import Agent, Model
# from .city_classes import Section # Dit kan nog problemen opleveren

class Home(Agent):
    def __init__(self, key: str, unique_id: int, model: Model, income_class: int, section) -> None:
        # Init
        super().__init__(unique_id, model)
        self.key = key
        self.income_class = income_class # (number, class_name)
        self.section = section

        # Location variables
        self.registered = False
        self.neighborhood, self.street, self.section = None, None, None

        # Inhabitants
        self.no_inhabitants = 0
        self.inhabitants = []
        self.breadwinners = []
        self.caretakers = []
        self.care_dependants = []

    def register(self, neighborhood: str, street: str):
        """
        Registers a house in its location. 
        """
        self.neighborhood = neighborhood
        self.street = street
        self.registered = True

    def step(self):
        print(f"Hi, I'm {self.unique_id}")

    """
    UPDATE FUNCTIONS 
    """
    def add_person(self, person_key): 
        pass

    """
    INFO FUNCTIONS 
    """
    def is_empty(self): 
        if self.no_inhabitants == 0:
            return True
        else:
            return False
    
