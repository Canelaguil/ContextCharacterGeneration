from ..utils import *

def get_other(my_key, update):
    # has to be done like this because of python var referencing
    return update['people'][0] if update['people'][0] != my_key else update['people'][1]

class Network():
    def __init__(self, person, community, mother, father, parents={}) -> None:
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
        for l in self.relationship_types.values():
            # for children subcategories
            if isinstance(l, dict):
                for _, l2 in l.items():
                    for r in l2:
                        self.community.message_relationship(r, relation_message)
            else:
                for r in l:
                    self.community.message_relationship(r, relation_message)

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

    def process_parent_child(self, notice, age, kind='birth'):
        if age == 0: # meaning, these are their parents
            label = 'parent'
            if label not in self.relationship_types:
                self.relationship_types[label] = []
            self.relationship_types[label].append(notice['key'])
        else: # they are the parent
            label = 'child'

            # also add to list of children to keep track of
            try:
                # has to be done like this because of python var referencing
                child = get_other(self.person_key, notice) #notice['people'][0] if notice['people'][0] != self.person_key else notice['people'][1]
                self.children_keys.append(child)
            except:
                log_error('cannot find child', notice)

            if label not in self.relationship_types:
                self.relationship_types[label] = {}
            if kind not in self.relationship_types[label]:
                self.relationship_types[label][kind] = []
            self.relationship_types[label][kind].append(notice['key'])

            self.introduce_children(child)

    def introduce_children(self, new_child):
        """
        
        """
        for ch in self.children_keys:
            if not self.community.we_know_each_other(ch, new_child):
                self.community.create_relationship(ch, new_child, 'half-sibling', True)
                # log_error('half siblings', self.community.create_relationship(ch, new_child, 'half-sibling', True))

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
    