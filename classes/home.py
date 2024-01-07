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
        self.inhabitant_tracking = []
        self.inhabitants = []
        self.people_to_add_this_round = []
        self.people_to_remove_this_round = []
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
        if self.no_inhabitants == 0:
            return
        msg = self.tasks.get()
        while msg != None:
            task = msg['topic']
            if task == 'new person':
                self.add_person(msg)
            elif task == 'person died':
                self.remove_person(msg)
            elif task == 'person moved':
                self.remove_person(msg)
            elif task == 'new care dependant':
                self.add_care_dependant(msg['key'])
            elif task == 'remove care dependant':
                self.remove_care_dependants(msg['key'])
            else:
                log_error('did not recognize home task', msg)
            msg = self.tasks.get()
        
        self.income = self.process_income_reports()
        self.income_needed = self.no_inhabitants * self.person_percentage
        if self.income_needed > self.income:
            self.not_enough_income()
            log = {
                'topic' : 'not enough income',
                'income' : self.income,
                'income needed' : round(self.income_needed, 3),
                'no inhabitants' : self.no_inhabitants,
                'inhabitants' : self.inhabitants
            }
            self.log.add_log(log)
            
        
        if self.care_dependants != [] and self.caretakers == []:
            log = {
                'topic' : 'needs new caretaker', 
                'care dependants' : self.care_dependants,
                'caretakers' : self.caretakers,
                'inhabitants' : self.inhabitants,
                'income' : self.income,
                'income needed' : round(self.income_needed, 3),
            }
            self.log.add_log(log)
            self.find_caretaker()

    def post_processing(self):
        

        self.inhabitant_tracking.append((self.no_inhabitants, self.inhabitants))
        # for p in self.people_to_add_this_round:
        #     self.add_person(p)
        # for p2 in self.people_to_remove_this_round:
        #     self.remove_person(p2)

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

        if person_info['age'] < 14:
            self.add_care_dependant(person_info['key'])

    def remove_person(self, person_info):
        if person_info['key'] in self.inhabitants:
            # print('here')
            self.no_inhabitants -= 1
            self.inhabitants.remove(person_info['key'])
            if person_info['key'] in self.care_dependants:
                self.care_dependants.remove(person_info['key'])
            elif person_info['key'] in self.caretakers:
                self.caretakers.remove(person_info['key'])
        else:
            log_error('home remove error', {'person' : person_info, 'house' : self.address()})

    def add_care_dependant(self, key):
        if key not in self.care_dependants:
            if key not in self.inhabitants:
                log_error('I dont even go here', [key, self.unique_id])
                return
            self.care_dependants.append(key)

    def remove_care_dependants(self, key):
        if key in self.care_dependants:
            if key not in self.inhabitants:
                log_error('I dont even go here', [key, self.unique_id])
                return
            self.care_dependants.remove(key)
            # print('removed')

        # if there are caretakers
        if self.care_dependants == [] and self.caretakers != []:
            msg = {
                'topic' : 'not caretaker'
            }
            self.model.message_person(self.caretakers[0], msg)
            self.caretakers = []

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
        msg = {
            'topic' : 'not enough income',
            'income' : self.income,
            'inhabitants' : self.inhabitants
        }
        self.notify_inhabitants(msg)

    def set_people_to_work(self, income_needed):
        # check if people are eligible to work & not working, and set to work
        best_candidate = None
        max_age = 10
        best_age = 10 # minimum working age...
        best_sex = 'f'
        for i in self.inhabitants:
            option = False
            candidate = self.model.get_person(i)
            # if candidate already employed
            if candidate['occupation']['has job']:
                break

            if candidate['sex'] == 'm' and best_sex == 'f' and candidate['age'] > 10:
                option = True            
            
            if candidate['age'] > best_age:
                option = True

            if candidate['age'] > max_age:
                max_age = candidate['age']

            if option:
                best_candidate = i
                best_age = candidate['age']
                best_sex = candidate['sex']

        if max_age < 16:
            # this does not really seem to be a problem often, so for now will not be further remedied
            log_error('no adults', self.info())
        # if all people are already employed or not eligible for employment: find house for them
        if best_candidate != None:
            msg = {
                'topic' : 'get a job'
            }
            self.model.message_person(best_candidate, msg)
        else:
            log_error('no possible worker', self.info())

    def find_caretaker(self):
        # check if people are eligible to work & not working, and set to work
        best_candidate = None
        best_age = 8 # minimum caretaking age...
        best_sex = 'm'
        for i in self.inhabitants:
            option = False
            candidate = self.model.get_person(i)

            # if candidate already employed
            if candidate['occupation']['has job']:
                break

            if candidate['sex'] == 'f' and best_sex == 'm' and candidate['age'] > 10:
                option = True            
            
            if candidate['age'] > best_age:
                option = True

            if option:
                best_candidate = i
                best_age = candidate['age']
                best_sex = candidate['sex']
                # beautify_print(candidate)


        if best_candidate != None:
            # notify caretaker
            msg = {
                'topic' : 'now caretaker',
                'care dependants' : self.care_dependants
            }
            self.model.message_person(best_candidate, msg)

            # notify care dependants
            msg2 = {
                'topic' : 'new caretaker',
                'person' : best_candidate
            }
            self.notify_care_dependants(msg2)
            self.caretakers.append(best_candidate)
        else:
            # can we assume there'd be enough income to provide alternative childcare?
            if (self.income - self.income_needed) >= (len(self.care_dependants) * 0.05):
                msg = {
                    'topic' : 'neglected',
                }
                self.notify_care_dependants(msg)
                # log_error('no possible caretaker', self.info())
                # if self.income_class[0] > 2:                    
                #     print(self.care_dependants)

    """
    INFO FUNCTIONS 
    """
    def get_my_children(self, person_info):
        """
        Get all children of person living in the house (used eg when a parent moves
        in with a new spouse).
        """
        children = []
        for key, child in person_info['network']['children'].items():
            if key in self.inhabitants:
                if child['age'] < 18:
                    children.append(key)
                # TODO: check if care dependant
        return children
        

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
    
    def notify_inhabitants(self, msg):
        for i in self.inhabitants:
            self.model.message_person(i, msg)

    def notify_care_dependants(self, msg):
        for i in self.care_dependants:
            self.model.message_person(i, msg)
    
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
            'inhabitant history' : self.inhabitant_tracking,
            'inhabitants' : self.get_inhabitants(),
            'caretakers' : self.caretakers,
            'care dependants' : self.care_dependants,
            'log' : self.log.get_logs()
        }
 