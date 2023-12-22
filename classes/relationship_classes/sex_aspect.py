from ..utils import *

class BirdsAndBees():
        def __init__(self, relationship, personA : dict, personB : dict, sexualRelationship) -> None:
            self.relationship = relationship

            # nature of sexual relationship
            self.is_sexual = sexualRelationship
            self.sex_degree = (personA['born this way']['sex interest'] + personB['born this way']['sex interest']) / 2
            self.sexuality_compatible = sexuality_match(personA['sex'], personB['sex'],
                                                        personA['born this way']['sexuality label'],
                                                        personB['born this way']['sexuality label'])
            self.sexuality_score = sexuality_match(personA['sex'], personB['sex'],
                                                    personA['born this way']['sexuality'],
                                                    personB['born this way']['sexuality'], 
                                                    'score')
            
            # conception variables
            if personA['sex'] != personB['sex']:
                self.can_conceive = True         
                if personB['sex'] == 'm':
                    self.mother = personA['key']
                    self.father = personB['key']
                    self.mother_age = personA['age']
                else:
                    self.mother = personB['key']
                    self.father = personA['key']
                    self.mother_age = personB['age']
                self.fertility = min(personA['genetics']['fertility'], 
                                     personB['genetics']['fertility'])

            else:
                self.can_conceive = False
            
        def init_types(self, type='arranged'):
             ...

        def conceive(self):
            """
            TODO: actually do something with the fertility scores
            """
            if not self.can_conceive or not self.is_sexual:
                return False
            
            # update known age
            self.mother_age += 1

            if self.mother_age > 41:
                chance = 0.03
            elif self.mother_age > 36:
                chance = 0.3
            elif self.mother_age > 25:
                chance = 0.5
            elif self.mother_age > 14:
                chance = 0.6
            else:
                chance = 0.

            if rand() < chance * self.fertility:
                return True
            return False
            
        def evolve(self):
            """
            TODO : implement happiness with current sexual relationship
            """
            if not self.is_sexual:
                return False
            
        def get_parents(self):
            return self.mother, self.father

