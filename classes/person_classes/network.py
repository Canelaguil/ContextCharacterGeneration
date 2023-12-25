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
        self.adopted_children = []
        self.relationships = {} # relationship key : other person key

    def unravel(self):
        """
        Person dies, network ends and relationships & people are notified
        """
        about_me = self.community.get_person_short(self.person_key)
        for r, p in self.relationships.items():
            person_message = {
                'topic' : 'person died', 
                'person' : about_me
            }
            self.community.message_person(p, person_message)
            relation_message = {
                'topic' : 'person died', 
                'person' : about_me
            }
            self.community.message_relationship(r, relation_message)

        for s in self.siblings:
            sib_message = {
                'topic' : 'sibling died', 
                'person' : about_me
            }
            self.community.message_person(s, sib_message)

    """
    RELATIONSHIP MANAGEMENT
    """
    def add_relationship(self, relationship_key, people):
        # instead of popping this, because I fear python var copies
        other = people[0] if people[0] != self.person_key else people[1]
        self.relationships[relationship_key] = other

    def add_child(self, child_key, kind='birth'):
        if kind == 'birth' : 
            self.children.append(child_key)
        else:
            self.adopted_children.append(child_key)

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
            'siblings' : self.siblings,
            'children' : self.get_child_descriptions(),
            'relationships' : self.relationships
        }
    