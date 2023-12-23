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
        self.living_children = []
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

    """
    PHASES / STEPS
    """
    def people(self):
        return       

    def relationships(self): 
        friend_report = self.friendship_aspect.evolve()
        romance_report = self.romance_aspect.evolve()
        sexual_report = self.sexual_aspect.evolve()
        if self.sexual_aspect.conceive():
            self.add_child_birth()
        
    def houses(self):
        return

    def post_processing(self):
        return
    
    """
    UTILS
    """
    def add_child_birth(self):
        # this is the only place where the specific sex of the partners matters within this class
        mother, father = self.sexual_aspect.get_parents()
        child = self.model.birth_child(father, mother)
        self.add_child(child, 'birth')

    def add_child(self, child, kind='birth'):
        """
        Add child, either through birth or adoption
        """        
        self.children.append(child['key'])
        self.living_children.append(child['key'])

        # notify parents they've had a child
        msg = {
            'topic' : 'new child',
            'child name' : child['name'],
            'child sex' : child['sex'], 
            'child key' : child['key'], 
            'addition type' : kind
        }
        self.update_people(msg)

    def update_people(self, msg):
        self.model.message_person(self.personA['key'], msg)
        self.model.message_person(self.personB['key'], msg)

    def status(self):
        return {
            'no children' : len(self.children),
            'no adopted children' : len(self.adopted_children)
        }
    
    def receive_message(self, task):
        self.tasks.add(task)
    
