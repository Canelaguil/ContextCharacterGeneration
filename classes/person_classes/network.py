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
        for l in self.relationship_types.values():
            for r in l:
                # person_message = {
                #     'topic' : 'person died',
                #     # 'label' : r.label, 
                #     'person' : about_me
                # }
                # self.community.message_person(p, person_message)
                relation_message = {
                    'topic' : 'person died', 
                    'person' : about_me
                }
                # if self.community.year != 1200:
                print(r)
                self.community.message_relationship(r, relation_message)

        # for s in self.siblings:
        #     sib_message = {
        #         'topic' : 'person died', 
        #         'person' : about_me,
        #         'label' : 'sibling'
        #     }
        #     self.community.message_person(s, sib_message)

    """
    RELATIONSHIP MANAGEMENT
    """
    def add_relationship(self, update):
        # instead of popping this, because I fear python var copies
        # other = update[0] if update[0] != self.person_key else update[1]
        # self.relationships[relationship_key] = other
        # print(update)
        label = update['label']
        if label not in self.relationship_types:
            self.relationship_types[label] = []
        self.relationship_types[label].append(update['key'])
        # print(self.relationship_types)

    def add_child(self, child_key, kind='birth'):
        if 'child' not in self.relationship_types:
            self.relationship_types['child'] = []
        self.relationship_types['child'].append(child_key)
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
        child_summary = {'birth' : {}, 'adopted' : {}}
        for child_key in self.children:
            child = self.community.get_person_short(child_key)
            child_summary['birth'][child_key] = child
        for child_key in self.adopted_children:
            child = self.community.get_person_short(child_key)
            child_summary['adopted'][child_key] = child
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
            # 'children' : self.get_child_descriptions(),
            # 'relationships' : self.relationships,
            ** self.relationship_types
        }
    