from mesa import Agent, Model
from .utils import *
# from .city_classes import StreetSection # Dit kan nog problemen opleveren

class Home(Agent):
    def __init__(self, key: str, unique_id: int, model: Model, income_class: int, section) -> None:
        # Init
        super().__init__(unique_id, model)
        self.key = key
        self.income_class = income_class # (number, class_name)
        self.section = section
        self.tasks = MessageInbox(self)

        # Location variables
        self.registered = False
        self.neighborhood, self.street = None, None

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
        if self.section == None:
            print(self.street, self.income_class)
        self.section_key = self.section.key
        self.registered = True

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
        msg = self.tasks.get()
        while msg != None:
            task = msg['topic']
            if task == 'new person':
                self.add_person(msg)
            elif task == 'person died':
                self.remove_person(msg)
            elif task == 'person moved':
                self.remove_person(msg)
            task = self.tasks.get()

    """
    UPDATE FUNCTIONS 
    """
    def add_person(self, person_info): 
        self.no_inhabitants += 1
        self.inhabitants.append(person_info['key'])
        move_notice = {
            'topic' : 'new home',
            'home' : self.info()
        }
        self.model.message_person(person_info['key'], move_notice)

    def remove_person(self, person_info):
        self.no_inhabitants -= 1
        self.inhabitants.remove(person_info['key'])

    def receive_message(self, msg):
        self.tasks.add(msg)

    """
    INFO FUNCTIONS 
    """
    def is_empty(self): 
        if self.no_inhabitants == 0:
            return True
        else:
            return False
        
    def info(self):
        return {
            'income class' : self.income_class[0], 
            'income class label' : self.income_class[1],
            'section' : self.section.key, 
            'street' : self.street, 
            'neighborhood' : self.neighborhood, 
            'key' : self.key, 
            'unique id' : self.unique_id,
        }
    
