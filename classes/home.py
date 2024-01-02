from mesa import Agent, Model
from .utils import *
# from .city_classes import StreetSection # Dit kan nog problemen opleveren

class Home(Agent):
    def __init__(self, key: str, unique_id: int, model: Model, income_class: int, 
                 section) -> None:
        # Init
        super().__init__(unique_id, model)
        self.key = key
        self.income_class = income_class # (number, class_name)
        self.section = section
        self.tasks = MessageInbox(self)
        self.log = Log(self.model)
        self.income_reports = []
        self.person_percentage = Home.person_income_percentage[income_class[0]]

        # Location variables
        self.registered = False
        self.neighborhood, self.street = None, None

        # Inhabitants
        self.no_inhabitants = 0
        self.inhabitants = []
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
        income = self.process_income_reports()
        income_needed = self.no_inhabitants * self.person_percentage
        if income_needed > income:
            self.not_enough_income()
            log = {
                'topic' : 'not enough income',
                'income' : income,
                'income needed' : round(income_needed, 3),
                'no inhabitants' : self.no_inhabitants
            }
            self.log.add_log(log)

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
            msg = self.tasks.get()

    """
    UPDATE FUNCTIONS 
    """
    def add_person(self, person_info): 
        self.no_inhabitants += 1
        self.inhabitants.append(person_info['key'])
        move_notice = {
            'topic' : 'new home',
            'home' : self.address()
        }
        ic = {
            'report' : {
                'income' : person_info['occupation']['income']
            }
        }
        self.model.message_person(person_info['key'], move_notice)
        self.income_reports.append(ic)

    def remove_person(self, person_info):
        if person_info['key'] in self.inhabitants:
            # print('here')
            self.no_inhabitants -= 1
            self.inhabitants.remove(person_info['key'])
        else:
            print('home remove error')

    def receive_message(self, msg):
        if msg['topic'] == 'income report':
            self.income_reports.append(msg)
        else:
            self.tasks.add(msg)
    """
    UTILS
    """
    def process_income_reports(self):
        income = 0
        for ic in self.income_reports: 
            income += ic['report']['income']
        self.income_reports = []
        return income
    
    def not_enough_income(self):
        ...

    """
    INFO FUNCTIONS 
    """
    def is_empty(self): 
        if self.no_inhabitants == 0:
            return True
        else:
            return False
        
    def get_inhabitants(self):
        my_people = {}
        for i in self.inhabitants:
            my_people[i] = self.model.get_person_summary(i)
        return my_people
    
    def address(self):
        return {
            'income class' : self.income_class[0], 
            'income class label' : self.income_class[1],
            'section' : self.section.key, 
            'street' : self.street, 
            'neighborhood' : self.neighborhood,
            'unique id' : self.unique_id,
        }
        
    def info(self):
        return {
            'income class' : self.income_class[0], 
            'income class label' : self.income_class[1],
            'section' : self.section.key, 
            'street' : self.street, 
            'neighborhood' : self.neighborhood, 
            'key' : self.key, 
            'unique id' : self.unique_id,
            'no inhabitants' : self.no_inhabitants,
            'inhabitants' : self.get_inhabitants(),
            'log' : self.log.get_logs()
        }
 