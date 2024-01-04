from ..utils import *

class Network():
    def __init__(self, person, community, mother, father, parents={}) -> None:
        self.community = community
        self.person = person
        self.person_key = person.unique_id
        self.mother = mother
        self.father = father
        self.siblings = []
        self.children = []
        self.relationship_types = {}
        self.adopted_children = []
        self.relationships = {} # relationship key : other person key

    def unravel(self):
        """
        Person dies, network ends and relationships & people are notified
        """
        about_me = self.community.get_person_short(self.person_key)
        relation_message = {
            'topic' : 'person died', 
            'person' : about_me
        }
        for l in self.relationship_types.values():
            # for children subcategories
            if isinstance(l, dict):
                for _, l2 in l.items():
                    for r in l2:
                        self.community.message_relationship(r, relation_message)
            else:
                for r in l:
                    print(r)
                    self.community.message_relationship(r, relation_message)

    """
    RELATIONSHIP MANAGEMENT
    """
    def add_relationship(self, update):
        label = update['label']
        if label not in self.relationship_types:
            self.relationship_types[label] = []
        self.relationship_types[label].append(update['key'])

    def process_parent_child(self, notice, age, kind='birth'):
        if age == 0: # meaning, these are their parents
            label = 'parent'
        else: # they are the parents
            label = 'child'

            # also add to list of children to keep track of
            try:
                # has to be done like this because of python var referencing
                child = notice['people'][0] if notice['people'][0] != self.person_key else notice['people'][1]
                self.children.append(child)
            except:
                log_error('cannot find child' ,notice)

        if label not in self.relationship_types:
            self.relationship_types[label] = {}
        if kind not in self.relationship_types[label]:
            self.relationship_types[label][kind] = []
        self.relationship_types[label][kind].append(notice['key'])

        # if isinstance(child, dict):
        #     child_key = child['child key']
        #     log_error('I received a message instead of a key', child)
        # else:
        #     child_key = child
        # if 'child' not in self.relationship_types:
        #     self.relationship_types['child'] = []
        # self.relationship_types['child'].append(child_key)
        # if kind == 'birth' : 
        #     self.children.append(child_key)
        # else:
        #     self.adopted_children.append(child_key)

    def add_sibling(self, sibling_key, kind='full'):
        """
        TODO : half siblings & adopted
        """
        if sibling_key in self.siblings:
            print(sibling_key)
        self.siblings.append(sibling_key)

    def init_siblings(self, list_of_siblings):
        """
        Add list of existing siblings
        """
        for s in list_of_siblings:
            self.siblings.append(s)

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
        for child_key in self.children:
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
            # 'siblings' : self.siblings,
            'children' : self.get_child_descriptions(),
            # 'relationships' : self.relationships,
            ** self.relationship_types
        }
    