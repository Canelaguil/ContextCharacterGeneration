from ..utils import *

def get_other(my_key, update):
    # has to be done like this because of python var referencing
    return update['people'][0] if update['people'][0] != my_key else update['people'][1]

class Network():
    def __init__(self, person, community, mother, father) -> None:
        self.community = community
        self.person = person
        self.person_key = person.unique_id
        self.mother = mother
        self.father = father
        self.siblings = []
        self.children_keys = []
        self.relationship_types = {}

    def unravel(self, cause=''):
        """
        Person dies, network ends and relationships & people are notified
        """
        about_me = self.community.get_person_short(self.person_key)
        relation_message = {
            'topic' : 'person died', 
            'person' : about_me,
            'cause' : cause
        }
        self.message_relationships(relation_message)

    """
    RELATIONSHIP MANAGEMENT
    """
    def add_relationship(self, update):
        label = update['label']
        if label not in self.relationship_types:
            self.relationship_types[label] = []
        self.relationship_types[label].append(update['key'])

        if label == 'spouse':
            self.new_marriage(update)

    def process_parent_child(self, notice, my_age, kind='birth', grand=False):        
        if my_age == 0: # meaning, this person is the child and the other is a parent
            label = 'parent' if not grand else 'grandparent'
            if label not in self.relationship_types:
                self.relationship_types[label] = []
            self.relationship_types[label].append(notice['key'])
        else: # this person is the parent
            label = 'child' if not grand else 'grandchild'

            # also add to list of children to keep track of
            try:
                # has to be done like this because of python var referencing
                child = get_other(self.person_key, notice) #notice['people'][0] if notice['people'][0] != self.person_key else notice['people'][1]
                self.children_keys.append(child)
            except:
                log_error('cannot find child', notice)

            # add to relationships
            if label not in self.relationship_types:
                self.relationship_types[label] = {}
            if kind not in self.relationship_types[label]:
                self.relationship_types[label][kind] = []
            self.relationship_types[label][kind].append(notice['key'])

            # introduce to rest of the family
            if label == 'child':
                # introduce to children (full siblings have already been introduced by relationship)
                self.introduce_children(child, 'half-sibling')

                # introduce to parents if they have them
                if self.mother != {} or self.mother == None: # check if firstgen
                    self.introduce_parents(child)
            elif label == 'grandchild':
                # introduce to children as family
                self.introduce_children(child, 'aunclenibling')

                # introduce to parents if they have them
                if self.mother != {} or self.mother == None: # check if firstgen
                    self.introduce_parents(child, 'greatgrandparentchild')

    def process_other_family(self, notice):
        my_index = notice['people'].index(self.person_key)
        # if notice['people ages'] == [1, 1]:
        #     print(notice)
        # print(notice['people ages'])
        if notice['label'] == 'aunclenibling':
            if my_index == 0:
                label = 'nibling'
                self.introduce_children(notice['people'][1], 'cousin')
            else:
                label = 'auncle'
        elif notice['label'] == 'greatgrandparentchild':
            # print(self.person_key)
            if notice['people ages'][my_index] > notice['people ages'][int(not my_index)]:
                print('my_index')
                label = 'greatgrandchild'
            else:
                label = 'greatgrandparent'

        # if notice['people ages'][my_index] > notice['people ages'][int(not my_index)]: # if I'm the supposedly older person here
        #     if notice['label'] == 'aunclenibling':
        #         label = 'nibling'

        #         # introduce my own children
        #         other = get_other(self.person_key, notice)
        #         self.introduce_children(other, 'cousin')
        #     elif notice['label'] == 'greatgrandparentchild':
        #         print(my_index)
        #         label = 'greatgrandchild'
        #     else:
        #         log_error('we dont have this label yet', notice)
        # else: # if I'm the supposedly younger person here
        #     if notice['label'] == 'aunclenibling':
        #         label = 'auncle'
        #     elif notice['label'] == 'greatgrandparentchild':
        #         label = 'greatgrandparent'
        #     else:
        #         log_error('we dont have this label yet', notice)
        # add to network
        notice['label'] = label
        self.add_relationship(notice)

    def introduce_children(self, new_child, label):
        """
        
        """
        # label = 'half-sibling' if not family else 'family'
        for ch in self.children_keys:
            if not self.community.we_know_each_other(ch, new_child):
                self.community.create_relationship(ch, new_child, label, True)
                # log_error('half siblings', self.community.create_relationship(ch, new_child, 'half-sibling', True))

    def introduce_parents(self, new_person, label='grandparentchild', platonic_only=True):
        other_key = new_person
        # update parents to check if they're alive
        self.mother = self.community.get_person(self.mother['key'])
        self.father = self.community.get_person(self.father['key'])

        # create relationship if alive
        if self.mother['alive']:
            self.community.create_relationship(self.mother['key'], other_key, label, platonic_only)
        if self.father['alive']:
            self.community.create_relationship(self.father['key'], other_key, label, platonic_only)

    """
    UTILS 
    """
    def new_marriage(self, update):
        msg = {
            'topic' : 'update',
            'update' : 'parent married',
            'parent' : self.person_key,
            'new partner' : get_other(self.person_key, update)
        }
        self.message_children(msg)

    def message_children(self, msg):
        for ch in self.children_keys:
            self.community.message_person(ch, msg)

    def message_relationships(self, msg): 
        for l in self.relationship_types.values():
            # for children subcategories
            if isinstance(l, dict):
                for _, l2 in l.items():
                    for r in l2:
                        self.community.message_relationship(r, msg)
            else:
                for r in l:
                    self.community.message_relationship(r, msg)
    """
    INFO FUNCTIONS
    """
    def get_parents(self):
        if self.mother != {}:
            return {
                'mother' : f"{self.mother['name']} ({self.mother['key']})",
                'father' : f"{self.father['name']} ({self.father['key']})",
            }
        else:
            return 'firstgen'
    
    def get_child_descriptions(self):
        child_summary = {}
        for child_key in self.children_keys:
            child = self.community.get_person_short(child_key)
            child_summary[child_key] = child
        return child_summary
    
    def get_friends(self):
        friends = []
        is_friend = lambda x : True if x['friendship']['score'] >= 1 else False
        for l in self.relationship_types.values():
            # for children subcategories
            if isinstance(l, dict):
                for r, l2 in l.items():
                    for r in l2:
                        info = self.community.get_relationship_info(r)
                        if is_friend(info):
                            friends.append(r)
            else:
                for r in l:
                    info = self.community.get_relationship_info(r)
                    if is_friend(info):
                            friends.append(r)
        return friends

    def get_enemies(self):
        enemies = []
        is_enemy = lambda x : True if x['friendship']['score'] <= 0.5 else False
        for l in self.relationship_types.values():
            # for children subcategories
            if isinstance(l, dict):
                for r, l2 in l.items():
                    for r in l2:
                        info = self.community.get_relationship_info(r)
                        if is_enemy(info):
                            enemies.append(r)
            else:
                for r in l:
                    info = self.community.get_relationship_info(r)
                    if is_enemy(info):
                            enemies.append(r)
        return enemies

    def get_relationships(self):
        rs = {}
        for k, p in self.relationships.items():
            other = self.community.get_person_short(p)
            rs[k] = other

    def links(self):
        return {
            'parents' : self.get_parents(),
            'children' : self.get_child_descriptions(),
            'relationship keys': self.relationship_types
        }
    