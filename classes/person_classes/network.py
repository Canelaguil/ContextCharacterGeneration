from ..utils import *

class Network():
    def __init__(self, person, community, mother, father, parents={}) -> None:
        self.community = community
        self.person = person
        self.person_key = person.unique_id
        self.mother = mother
        self.father = father
        self.children = []
        self.adopted_children = []
        self.relationships = {} # relationship key : other person key

    def add_relationship(self, relationship_key, people):
        # instead of popping this, because I fear python var copies
        other = people[0] if people[0] != self.person_key else people[1]
        self.relationships[relationship_key] = other

    def add_child(self, child_key, kind='birth'):
        if kind == 'birth' : 
            self.children.append(child_key)
        else:
            self.adopted_children.append(child_key)

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
            'children' : self.get_child_descriptions(),
            'relationships' : self.relationships
        }
    