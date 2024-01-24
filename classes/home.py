from mesa import Agent, Model
import copy
from .utils import *

# TODO INTRODUCRE PEOPLE TO EACH OTHER
class Home(Agent):
    """
    Agent representing a home: keeps track of its inhabitants, caretakers and
    income. 
    """
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
        self.people_to_remove = []
        self.people_to_add = []
        self.caretakers = []
        self.care_dependants = []

    def register(self, neighborhood: str, street: str):
        """
        Registers a house in its location. 
        """
        self.neighborhood = neighborhood
        self.street = street
        if self.section == None:
            fatal_error(self.street, self.income_class)
        self.section_key = self.section.key
        self.registered = True

    """
    PHASES / STEPS
    """
    def people(self):
        return
    
    def lovedeathbirth(self): 
        return
    
    def houses(self):
        """
        - Add / remove people
        - Process other messages
        - Set people to work if needed
        - Find new caretaker if needed
        """
        self.no_inhabitants = len(self.inhabitants)
        if self.no_inhabitants == 0:
            return  
        
        # remove and add people
        for p in self.people_to_add:
            self.add_person(p)
        for p2 in self.people_to_remove:
            self.remove_person(p2)

        if self.no_inhabitants == 0:
            return

        msg = self.tasks.get()
        while msg != None:
            task = msg['topic']
            if task == 'new care dependant':
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
                'inhabitants' : copy.deepcopy(self.inhabitants)
            }
            self.log.add_log(log)
            
        
        if self.care_dependants != [] and self.caretakers == []:
            log = {
                'topic' : 'needs new caretaker', 
                'care dependants' : copy.deepcopy(self.care_dependants),
                'caretakers' : copy.deepcopy(self.caretakers),
                'inhabitants' : copy.deepcopy(self.inhabitants),
                'income' : self.income,
                'income needed' : round(self.income_needed, 3),
            }
            self.log.add_log(log)
            self.find_caretaker()

        self.inhabitant_tracking.append((self.no_inhabitants, copy.deepcopy(self.inhabitants), copy.deepcopy(self.care_dependants)))

    def post_processing(self):              
        self.people_to_remove = []
        self.people_to_add = []

    """
    UPDATE FUNCTIONS 
    """
    def add_person(self, person_info : dict): 
        """
        Add person to home
        """
        # self.no_inhabitants += 1
        if person_info['key'] in self.inhabitants:
            log_error('perosn already in home', person_info)
        self.inhabitants.append(person_info['key'])
        # move_notice = {
        #     'topic' : 'new home',
        #     'home' : self.address()
        # }
        ic = {
            'report' : {
                'income' : person_info['occupation']['income']
            }
        }
        self.income_reports.append(ic) # add income report for this cycle
        
        # self.model.message_person(person_info['key'], move_notice)
        self.no_inhabitants = len(self.inhabitants)

        if person_info['age'] < Home.adult_age and person_info['key'] not in self.care_dependants:
            self.add_care_dependant(person_info['key'])

    def remove_person(self, person_info : dict):
        """
        Remove person from home
        """
        if person_info['key'] in self.inhabitants:
            # self.no_inhabitants -= 1
            # print(self.inhabitants)
            self.inhabitants.remove(person_info['key'])
            # if self.inhabitants == []:
            #     print('-----------------------')
            if person_info['key'] in self.care_dependants:
                self.care_dependants.remove(person_info['key'])
            elif person_info['key'] in self.caretakers:
                self.caretakers.remove(person_info['key'])
            self.no_inhabitants = len(self.inhabitants)
        else:            
            log_error('home remove error', {'person' : person_info, 
                                            'house' : self.address(), 
                                            'year' : self.model.get_year()})

    def add_care_dependant(self, key):
        """
        Add care dependant to home
        """
        if key not in self.care_dependants:
            if key not in self.inhabitants:
                log_error('I dont even go here', [key, self.unique_id])
                return
            self.care_dependants.append(key)

    def remove_care_dependants(self, key):
        """
        Remove care dependant from home
        """
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
        """
        Receive message, and process income reports and +/- inhabitant messages
        immediately. 
        """
        topic = msg['topic']
        if topic == 'income report':
            self.income_reports.append(msg)
        elif topic in ['person died', 'person moved']:
            self.people_to_remove.append(msg)
        elif topic in ['new person']:
            self.people_to_add.append(msg)
        else:
            self.tasks.add(msg)

    """
    UTILS
    """
    def process_income_reports(self):
        """
        Calculate income based on the received income reports. 
        """
        income = 0
        for ic in self.income_reports: 
            income += ic['report']['income']
        self.income_reports = []
        return income
    
    def not_enough_income(self):
        """
        Notify inhabitants not enough income was earned this cycle to support 
        them all. 
        """
        msg = {
            'topic' : 'not enough income',
            'income' : self.income,
            'inhabitants' : self.inhabitants
        }
        self.notify_inhabitants(msg)

    def set_people_to_work(self, income_needed):
        """
        Find new person to work. Preference is given to unemployed older men. 

        TODO: Don't just find one, but estimate how many are needed based on 
        the missing income
        """
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
        """
        Find new caretaker in the house. Preference is giving to unemployed older
        women.
        """
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

    """
    INFO FUNCTIONS 
    """
    def get_my_children(self, person_info):
        """
        Returns the ID's of all children of a person living in the house 
        (used eg when a parent moves in with a new spouse).
        """
        children = []
        for key, child in person_info['network']['children'].items():
            if key in self.inhabitants:
                if child['age'] < 18:
                    children.append(key)
                # TODO: check if care dependant regardless of being child
        return children
        
    def is_empty(self) -> bool: 
        if self.no_inhabitants == 0:
            return True
        return False
        
    def get_inhabitants(self):
        """
        Generate quick overview of current inhabitants
        """
        my_people = {}
        for i in self.inhabitants:
            my_people[i] = self.model.get_person_summary(i)
        return my_people
    
    """
    UTILS
    """
    def notify_inhabitants(self, msg):
        """
        Send message to all inhabitants
        """
        for i in self.inhabitants:
            self.model.message_person(i, msg)

    def notify_care_dependants(self, msg):
        """
        Send message to all care dependants
        """
        for i in self.care_dependants:
            self.model.message_person(i, msg)

    """
    OUTPUT FUNCTIONS
    """
    
    def address(self):
        """
        Short output without danger of recursive requests to other agent's info.
        """
        return {
            'income class' : self.income_class[0], 
            'income class label' : self.income_class[1],
            'section' : self.section.key, 
            'street' : self.street, 
            'neighborhood' : self.neighborhood,
            'unique id' : self.unique_id,
        }
        
    def info(self):
        """
        Long output, used for .json file.
        """
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
 