from .utils import *
from mesa import Agent, Model
from .relationship_classes import *

class Relationship(Agent):
    def __init__(self, unique_id: int, model: Model, personA : dict, 
                 personB : dict, init_type : str, platonic_only=False) -> None:
        super().__init__(unique_id, model)
        self.personA = personA
        self.personB = personB
        self.keys = [personA['key'], personB['key']]
        self.active = True
        self.children = []
        self.adopted_children = []
        self.tasks = MessageInbox(self)

        # don't allow for romance or sexual angle 
        self.platonic_only = platonic_only

        if init_type == 'arranged marriage':
            self.arrange_marriage()
        else:
            self.platonic()

        notify_people_msg = {
            'topic' : 'new relationship',
            'key' : self.unique_id, 
            'people' : [self.personA['key'], self.personB['key']]
        }
        self.update_people(notify_people_msg)
        self.end_cause = 'still active' # updated when relationship ends

    def arrange_marriage(self):
        """
        Arrange marriage for first_gen couples. Disregards the platonic_only 
        parameter.
        """
        friendship_seed = normal_in_range(0.7, 0.3)
        self.friendship_aspect = Friendship(self, self.personA, self.personB, 
                                     False, friendship_seed)

        self.sexual_aspect = BirdsAndBees(self, self.personA, self.personB, True)
        self.sexual_aspect.init_types('arranged')

        self.romance_aspect = Romance(self, self.personA, self.personB, 
                                      friendship_seed)

    def platonic(self):
        pass

    def end(self, cause, context={}):
        self.active = False
        if cause == 'person died':
            self.end_cause = f"{context['person']['name']} died"
        else:
            self.end_casue = cause

    """
    PHASES / STEPS
    """
    def people(self):
        return       

    def relationships(self): 
        if self.active:
            friend_report = self.friendship_aspect.evolve()
            romance_report = self.romance_aspect.evolve()
            sexual_report = self.sexual_aspect.evolve()
            conceived = self.sexual_aspect.conceive()
            if conceived:
                self.add_child_birth()

            report = {
                'friendship' : friend_report,
                'romance' : romance_report,
                'sex'  : sexual_report, 
                'conceived' : conceived
            }
            return report
        
    def houses(self):
        return

    def post_processing(self):
        task = self.tasks.get()
        while task != None:
            topic = task['topic']
            if topic == 'person died':
                self.end(task['topic'], {'person' : task['person']})
            task = self.tasks.get()
    
    """
    UTILS
    """
    def add_child_birth(self):
        income_class = self.personA['income class']
        child = self.model.birth_child(self.unique_id, income_class)
        self.add_child(child, 'birth')

    def add_child(self, child, kind='birth'):
        """
        Add child, either through birth or adoption
        """        
        # notify parents and other children
        msg = {
            'topic' : 'new child',
            'child name' : child['name'],
            'child sex' : child['sex'], 
            'child key' : child['key'], 
            'kind' : kind
        }
        self.update_people(msg)
        msg2 = { # new message necessary to avoid errors
            'topic' : 'new sibling',
            'child name' : child['name'],
            'child sex' : child['sex'], 
            'child key' : child['key'], 
            'kind' : kind
        }
        self.update_children(msg2)

        self.children.append(child['key'])

    def update_people(self, msg):
        self.model.message_person(self.personA['key'], msg)
        self.model.message_person(self.personB['key'], msg)

    def update_children(self, msg):
        for child in self.children:
            self.model.message_person(child, msg)
        for a_child in self.adopted_children:
            self.model.message_person(a_child, msg)

    def status(self):
        # return woman first if woman in relationship
        if self.personA['sex'] == 'f':
            people = [self.personA['key'], self.personB['key']]
        else:
            people = [self.personB['key'], self.personA['key']]

        return {
            'active' : self.active,
            'people' : people,
            'no birth children' : len(self.children),
            'birth children' : self.children,
            'no adopted children' : len(self.adopted_children), 
            'adopted children' : self.adopted_children,
            'end cause': self.end_cause, 
            'key' : self.unique_id
        }
    
    def receive_message(self, task):
        self.tasks.add(task)

