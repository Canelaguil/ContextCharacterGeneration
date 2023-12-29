from ..utils import *
# from math import power

class Friendship():
    def __init__(self, relationship, personA : dict, personB : dict, family : bool, seed=0) -> None:
        """
        family : related, NOT couples
        """
        self.relationship = relationship
        self.family = family
        self.affectionA = 0
        self.affectionB = 0
        self.compatibility = 0.5
        self.score = seed
        self.determine_compatibility(personA, personB)
        self.start = seed

    def determine_compatibility(self, personA, personB):
        pA, pB = personA['personality'], personB['personality']
        personality_similarity = get_vector_distance(pA, pB)
        self.compatibility = 1 - personality_similarity
        return self.compatibility
        # mA, mB = personA['homsoc']['means'], ['homsoc']['means']
        # life_similarity = get_vector_distance(mA, mB)
        # iA, iB = personA['homsoc']['expression'], ['homsoc']['expression']
        # identity_similarity = get_vector_distance(iA, iB)
        # age_closeness = age_match(personA['age'], personB['age'])
        
    def evolve(self, proximity_score):
        """
        Every year there is a chance of something happening
        """
        # chance of something happening
        something_chance = self.score * 0.2 + (0.2 ** proximity_score)
        something_happens = True if rand() < something_chance else False
        report = {'change' : False, 'value_change' : 0.}

        # something happens
        if something_happens:
            scale = 0.2
            loc = self.compatibility * 0.4 - 0.2
            modifier = normal_in_range(loc, scale, 0.25, -0.25)
            old_score = self.score
            self.score = fair_mod(self.score, modifier)
            report['change'] = True
            report['value_change'] = round(self.score - old_score, 3)

        report['new score'] = self.score
        return report
    
    def trajectory(self):
        return {
            'start' : self.start,
            'current' : self.score
        }


            



