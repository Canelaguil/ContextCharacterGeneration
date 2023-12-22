
class Network():
    def __init__(self, person, mother, father, parents={}) -> None:
        self.person = person
        self.mother = mother
        self.father = father

    def get_parents(self):
        if self.mother != {}:
            return {
                'mother' : f"{self.mother['name']} ({self.mother['key']})",
                'father' : f"{self.father['name']} ({self.father['key']})",
            }
        else:
            return 'firstgen'
        
    def links(self):
        return {
            'parents' : self.get_parents()
        }
    