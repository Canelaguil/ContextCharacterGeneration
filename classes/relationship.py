from .utils import *
from mesa import Agent, Model
from .relationship_classes import *
from copy import deepcopy

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
        self.ages = [personA['age'], personB['age']]
        self.adults = [True if a > 16 else False for a in self.ages ]
        self.proximity_score = 1 # for testing
        self.children = []
        self.adopted_children = []
        self.tasks = MessageInbox(self)
        self.logs = Log(model)

        # don't allow for romance or sexual angle (w/ family e.g.)
        self.platonic_only = platonic_only

        if label == 'spouse':
            self.arranged_marriage_init()
        elif label in ['parentchild', 'sibling', 'half-sibling', 
                       'grandparentchild', 'aunclenibling', 'cousin']:
            self.family_init()
        elif label == 'friend':
            self.friendship_init()
            label = 'unrelated' # categorize under unrelated
        else:
            self.platonic_init()
        
        self.label = label
        notify_people_msg = {
            'topic' : 'new relationship',
            'key' : self.unique_id, 
            'people' : [self.personA['key'], self.personB['key']], 
            'people names' : [self.personA['full name'], self.personB['full name']],
            'people ages' : self.ages,
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
        friendship_seed = normal_in_range(1.1, 0.2, 1.5)
        self.friendship_aspect = Friendship(self, self.personA, self.personB, 
                                            False, friendship_seed)

        self.sexual_aspect = BirdsAndBees(self, self.personA, self.personB, True)
        self.romance_aspect = Romance(self, self.model, self.personA, self.personB, 
                                      'generate', 'generate')

    def friendship_init(self):
        friendship_seed = normal_in_range(1.1, 0.1, 1.5)
        self.friendship_aspect = Friendship(self, self.personA, self.personB, 
                                            False, friendship_seed)
        self.sexual_aspect = BirdsAndBees(self, self.personA, self.personB, False)
        self.romance_aspect = Romance(self, self.model, self.personA, self.personB)

    def platonic_init(self):
        friendship_seed = normal_in_range(0.7, 0.2, 1.5)
        self.friendship_aspect = Friendship(self, self.personA, self.personB, 
                                            False, friendship_seed)

    def family_init(self):
        friendship_seed = normal_in_range(1, 0.2, 1.5)
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
            people_involved = deepcopy(self.keys)
            people_involved.remove(context['person']['key'])
            
            # if relationship, update relationship status
            relationship_msg = {
                'key' : self.unique_id, 
            }
            if self.label == 'spouse':
                relationship_msg['topic'] = 'unmarried'
                self.model.message_person(people_involved[0], relationship_msg)
            elif self.label == 'partner':
                relationship_msg['topic'] = 'single'
                self.model.message_person(people_involved[0], relationship_msg)

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
                'friendship label' : self.friendship_aspect.label,
                'label' : descriptor
            }
            if not self.platonic_only:
                death_note['love state'] = self.romance_aspect.get_state(people_involved[0])
            self.model.message_person(people_involved[0], death_note)
            
        else:
            self.end_cause = end_cause
        
        self.active = False

    def update_label(self, new_label):
        label_hierarchy = [
            'sibling',
            'half-sibling',
            'aunclenibling', 
            'parentchild',
            'grandparentchild', 
            'greatgrandparentchild', 
            'spouse',
            'partner', 
            'unrelated'
        ]
        if label_hierarchy.index(new_label) < label_hierarchy.index(self.label):
            print(new_label)
            print(self.unique_id)
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

        if report['friendship']['label change']:
            # update people on new friendship change
            friend_update = {
                'topic' : 'update', 
                'update' : 'new friendship label', 
                'relationship label' : self.label,
                'friendship label' : friend_report['label'], 
                'relationship' : self.unique_id
            }
            self.update_people(friend_update)
       
        change = report['friendship']['change']
        if not self.platonic_only:
            romance_report = self.romance_aspect.evolve(friend_report, self.adults)
            sexual_report = self.sexual_aspect.evolve(romance_report)
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
                        'friendship label' : friend_report['label'], 
                        'relationship' : self.unique_id
                    }
                    self.model.message_person(self.keys[0], update)
                else:
                    update = {
                        'topic' : 'feelings change', 
                        'target' : self.keys[0],
                        'target name' : self.personA['full name'],
                        'state' : romance_report['state B'],                        
                        'friendship label' : friend_report['label'], 
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
        task = self.tasks.get()
        while task != None:
            topic = task['topic']
            if topic == 'person died':
                self.end('person died', {'person' : task['person'], 'cause' : task['cause']})
            if topic == 'newly adult':
                source = task['source']
                self.adult[self.people.index(source)] = True
            task = self.tasks.get()
        
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
    def get_update(self):
        about_us = {
            'friendship' : self.friendship_aspect.get_status()
        }
        if not self.platonic_only:
            about_us['romance'] = self.romance_aspect.get_states()
            about_us['sex'] = self.sexual_aspect.get_status()
        return about_us

    def status(self):
        # return woman first if woman in relationship
        if self.personA['sex'] == 'f':
            people = [self.personA['key'], self.personB['key']]
        else:
            people = [self.personB['key'], self.personA['key']]

        return {
            'active' : self.active,
            'duration' : [self.start_year, self.end_year],
            'ages at init' : self.ages,
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
    
