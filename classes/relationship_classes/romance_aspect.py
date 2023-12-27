from ..utils import *

class Romance():
    def __init__(self, relationship, personA, personB, friendshiplevel=0) -> None:
        self.relationship = relationship
        self.personA = personA
        self.personB = personB

        self.influence_love(friendshiplevel)

    def influence_love(self, friendship):
        pass

    def evolve(self):
        return {
            'change' : False
        }
