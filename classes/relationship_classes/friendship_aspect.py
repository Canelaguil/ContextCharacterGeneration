from ..utils import *

class Friendship():
    def __init__(self, relationship, personA : dict, personB : dict, family : bool, seed=0) -> None:
        """
        family : related, NOT couples
        """
        self.relationship = relationship
        self.level = seed
        self.family = family
        self.affectionA = 0
        self.affectionB = 0
        self.compatibility = 0.5
        # self.determine_compatibility(personA, personB)

    def determine_compatibility(self, personA, personB):
        pA, pB = personA['personality'], personB['personality']
        personality_similarity = get_vector_distance(pA, pB)
        mA, mB = personA['homsoc']['means'], ['homsoc']['means']
        life_similarity = get_vector_distance(mA, mB)
        iA, iB = personA['homsoc']['expression'], ['homsoc']['expression']
        identity_similarity = get_vector_distance(iA, iB)
        age_closeness = age_match(personA['age'], personB['age'])
        
    
    def evolve(self):
        pass


