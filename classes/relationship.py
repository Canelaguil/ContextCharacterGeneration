from .utils import *
from mesa import Agent, Model
from .relationship_classes import *

class Relationship(Agent):
    def __init__(self, unique_id: int, model: Model, personA : dict, 
                 personB : dict, label : str, platonic_only=False) -> None:
        super().__init__(unique_id, model)
        self.active = True
        self.start_year = self.model.get_year()
        self.end_year = 0
        self.personA = personA
        self.personB = personB
        self.keys = [personA['key'], personB['key']]
        self.proximity_score = 1 # for testing
        self.children = []
        self.adopted_children = []
        self.tasks = MessageInbox(self)
        self.logs = Log(model)

        if not isinstance(personA, dict):            
            print('sdfsf')
            fatal_error(personA)

        # don't allow for romance or sexual angle (w/ family e.g.)
        self.platonic_only = platonic_only

        if label == 'spouse':
            self.arranged_marriage_init()
        elif label in ['parentchild', 'sibling', 'half-sibling']:
            self.family_init()
        else:
            self.platonic_init()
        
        self.label = label
        notify_people_msg = {
            'topic' : 'new relationship',
            'key' : self.unique_id, 
            'people' : [self.personA['key'], self.personB['key']], 
            'people names' : [self.personA['full name'], self.personB['full name']],
            'label' : self.label,
            'committed' : True if self.label in ['spouse', 'partner'] else False
        }
        self.update_people(notify_people_msg)
        self.end_cause = 'still active' # updated when relationship ends

    def arranged_marriage_init(self):
        """
        Arrange marriage for first_gen couples. Disregards the platonic_only 
        parameter.
        """
        # print('arrangingggg')
        friendship_seed = normal_in_range(0.7, 0.3)
        self.friendship_aspect = Friendship(self, self.personA, self.personB, 
                                            False, friendship_seed)

        self.sexual_aspect = BirdsAndBees(self, self.personA, self.personB, True)
        # self.sexual_aspect.init_types('arranged')
        if rand() < self.friendship_aspect.compatibility:
            initA = 'solid love'
            initB = 'solid love'
        else:
            initA = 'infatuation'
            initB = 'infatuation' if rand() < 0.5 else 'out of love'
        self.romance_aspect = Romance(self, self.model, self.personA, self.personB, 
                                      initA, initB)

    def platonic_init(self):
        friendship_seed = normal_in_range(0.7, 0.3)
        self.friendship_aspect = Friendship(self, self.personA, self.personB, 
                                            False, friendship_seed)

    def family_init(self):
        friendship_seed = normal_in_range(0.7, 0.3)
        self.friendship_aspect = Friendship(self, self.personA, self.personB, 
                                            True, friendship_seed)

    def set_home(self, house_key):
        self.common_home = house_key

    """
    CHANGE RELATIONSHIP STATE
    """
    def romance_change(self, new_label):
        self.update_label(new_label)
        if new_label in ['spouse', 'partner']:
            taken = True
        else: taken = False

        notify_people_msg = {
            'topic' : 'relationship change', 
            'label' : new_label,
            'people' : [self.personA['key'], self.personB['key']], 
            'key' : self.unique_id,
            'committed' : taken,
        }
        self.update_people(notify_people_msg)

    def end(self, end_cause, context={}):
        # if relationship already done for
        if not self.active:
            return
        
        if end_cause == 'person died':
            self.end_year = self.model.get_year()
            self.end_cause = f"{context['person']['name']} died"
            self.keys.remove(context['person']['key'])
            
            # if relationship, update relationship status
            relationship_msg = {
                'key' : self.unique_id, 
            }
            if self.label == 'spouse':
                relationship_msg['topic'] = 'unmarried'
                self.model.message_person(self.keys[0], relationship_msg)
            elif self.label == 'partner':
                relationship_msg['topic'] = 'single'
                self.model.message_person(self.keys[0], relationship_msg)

            # Determine whether it was a child or a parent to the survior
            if self.label == 'parentchild':
                if self.personA['key'] == context['person']['key']:
                    # this uses the ages at creation but that's fine
                    if self.personA['age'] < self.personB['age']:
                        descriptor = 'child'
                    else:
                        descriptor = 'parent'
                elif self.personB['key'] == context['person']['key']:
                    if self.personA['age'] < self.personB['age']:
                        descriptor = 'parent'
                    else:
                        descriptor = 'child'
                else:
                    log_error('finding parentchild', [self.personA, self.personB, context])
                    descriptor = self.label
            else:
                descriptor = self.label

            death_note = {
                'topic' : 'person died',
                'person' : context['person'],
                'cause' : context['cause'],
                'label' : descriptor
            }
            self.model.message_person(self.keys[0], death_note)
            
        else:
            self.end_cause = end_cause
        
        self.active = False

    def update_label(self, new_label):
        label_hierarchy = [
            'sibling',
            'half-sibling',
            'parentchild',
            'spouse',
            'partner', 
            'friend', 
            'acquaintance'
        ]
        if label_hierarchy.index(new_label) < label_hierarchy.index(self.label):
            self.label = new_label

    """
    PHASES / STEPS
    """
    def people(self):
        if not self.active:
            return
        change = False
        friend_report = self.friendship_aspect.evolve(self.proximity_score)
        report = {
            'friendship' : friend_report,
        }
        change = report['friendship']['change']
        if not self.platonic_only:
            romance_report = self.romance_aspect.evolve()
            sexual_report = self.sexual_aspect.evolve()
            conceived = self.sexual_aspect.conceive()
            if conceived:
                self.add_child_birth()
                change = True
            if romance_report['change']:
                change = True

                # notify person that their feelings changed
                if romance_report['change A']:
                    update = {
                        'topic' : 'feelings change', 
                        'target' : self.keys[1],
                        'target name' : self.personB['full name'],
                        'state' : romance_report['state A'],
                        'relationship' : self.unique_id
                    }
                    self.model.message_person(self.keys[0], update)
                else:
                    update = {
                        'topic' : 'feelings change', 
                        'target' : self.keys[0],
                        'target name' : self.personA['full name'],
                        'state' : romance_report['state B'],
                        'relationship' : self.unique_id
                    }
                    self.model.message_person(self.keys[1], update)
            if sexual_report['change']:
                change = True

            # merge reports
            report = {** report, ** {
                'romance' : romance_report,
                'sex'  : sexual_report, 
                'conceived' : conceived
            }}
        if change:
            self.logs.add_log(report)       

    def lovedeathbirth(self): 
        return
        
    def houses(self):
        task = self.tasks.get()
        while task != None:
            topic = task['topic']
            if topic == 'person died':
                self.end('person died', {'person' : task['person'], 'cause' : task['cause']})
            task = self.tasks.get()

    def post_processing(self):
        return
    
    """
    UTILS
    """
    def add_child_birth(self):
        income_class = self.personA['income class']
        child = self.model.birth_child(self.unique_id, income_class, self.personA['faction'])
        self.add_child(child, 'birth')

    def add_child(self, child, kind='birth'):
        """
        Add child, either through birth or adoption
        """
        for parent in self.keys:
            self.model.create_relationship(parent, child['key'], 'parentchild', True)

        for sibling in self.children: 
            try:
                if not self.model.we_know_each_other(sibling, child['key']):
                    self.model.create_relationship(sibling, child['key'], 'sibling', True)
            except:
                print(sibling)
                print(child['key'])
                fatal_error('failed to notify siblings', [sibling, child, self.unique_id])

        if kind == 'birth':
            self.children.append(child['key'])
        else: 
            self.adopted_children.append(child['key'])

        try:
            self.model.move_person_to_home(self.common_home, child['key'])
        except:
            print('Could not move child in')
            print(child)
            fatal_error(self.common_home)


    """
    MESSAGING FUNCTIONS
    """
    def receive_message(self, task):
        self.tasks.add(task)

    def update_people(self, msg):
        self.model.message_person(self.personA['key'], msg)
        self.model.message_person(self.personB['key'], msg)

    def update_children(self, msg):
        for child in self.children:
            self.model.message_person(child, msg)
        for a_child in self.adopted_children:
            self.model.message_person(a_child, msg)

    """
    INFO FUNCTIONS
    """
    def update(self):
        about_us = {
            'friendship' : self.friendship_aspect.score
        }
        if not self.platonic_only:
            about_us['romantic state']

    def status(self):
        # return woman first if woman in relationship
        if self.personA['sex'] == 'f':
            people = [self.personA['key'], self.personB['key']]
        else:
            people = [self.personB['key'], self.personA['key']]

        return {
            'active' : self.active,
            'duration' : [self.start_year, self.end_year],
            'label' : self.label,
            'compatibility' : self.friendship_aspect.determine_compatibility(self.personA, self.personB),
            'platonic only' : self.platonic_only,
            'people' : people,
            'no birth children' : len(self.children),
            'birth children' : self.children,
            'no adopted children' : len(self.adopted_children), 
            'adopted children' : self.adopted_children,
            'end cause': self.end_cause, 
            'key' : self.unique_id, 
            'logs' : self.logs.get_logs(), 
            'friendship trajectory' : self.friendship_aspect.trajectory()
        }
    
