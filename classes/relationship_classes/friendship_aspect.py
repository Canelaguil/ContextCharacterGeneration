from ..utils import *
# from math import power

class Friendship():
    """
    Represents the friendship aspect of a relationship
    """
    def __init__(self, relationship, personA : dict, personB : dict, family : bool, seed=0.6) -> None:
        self.relationship = relationship
        self.family = family # True if related, NOT couples
        self.affectionA = 0
        self.affectionB = 0
        self.compatibility = 0.5
        self.score, self.label = self.init_relation(seed)
        self.determine_compatibility(personA, personB)
        self.label_history = [self.label]
        self.start = seed

    def init_relation(self, seed):
        """
        Start relationship with provided seed
        """
        score = seed
        label = self.get_label(seed)
        return score, label

    def get_label(self, value):
        """
        Attributes label to friendship score
        """
        if value < 0.2:
            return 'enemy'
        elif value < 0.5:
            return 'disliked'
        elif value < 1:
            return 'indifferent'
        elif value < 1.3:
            return 'friend'
        elif value < 1.51:
            return 'good friend'
        else:
            fatal_error('incorrect value', value)

    def determine_compatibility(self, personA, personB):
        """
        Determine compatibility between two people
        """
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
        Yearly check to see if something changes in the relationship. The chance
        of something happening depends on the relationship label, whether the
        event is positive or not on the compatibility

        NOTE: Proximity score may still be implemented
        """
        # chance of something happening
        if self.label == 'enemy':
            something_chance = 0.05
        elif self.label == 'disliked':
            something_chance = 0.15
        elif self.label == 'indifferent':
            something_chance = 0.1
        elif self.label == 'friend':
            something_chance = 0.15
        elif self.label == 'good friend':
            something_chance = 0.05

        # # chance of something happening
        # something_chance = self.score * 0.2 + (0.2 ** proximity_score)
        something_happens = True if rand() < something_chance else False
        report = {'change' : False, 'label change' : False}

        # something happens
        if something_happens:
            # set up report
            report['change'] = True
            report['old score'] = self.score
            report['old label'] = self.label

            # choose the event kind
            events = [1, 0.5, 0.25, 0.1]
            event_label = ['explosive', 'major', 'medium', 'minor']
            p = [0.025, 0.175, 0.3, 0.5]
            posneg = 1 if rand() < self.compatibility else -1
            e = rand_choice(events, p) 
            e_label = event_label[events.index(e)]
            report['event label'] = f"{e_label} event"

            # actually change all of this
            self.score = fair_mod(self.score, e * posneg, 1.5)
            self.label = self.get_label(self.score)
            report['label change'] = report['old score'] != self.label

            # if label changed, record it in history
            if report['label change']:
                self.label_history.append(self.label)
       
        report['label'] = self.label
        report['score'] = self.score
        return report
    
    def get_status(self) -> dict:
        """
        Returns current relationship status
        """
        return {
            'label' : self.label,
            'score' : self.score,
            'history' : self.label_history
        }

    def trajectory(self) -> dict:
        """
        Returns relationship trajectory from start to finish
        """
        return {
            'start' : self.start,
            'current' : self.score,
            'label' : self.label
        }


            



