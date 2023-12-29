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

            # sex life variables
            self.max_sex_life = max(personA['born this way']['sex interest'], 
                                    personB['born this way']['sex interest'])
            self.min_sex_life = min(personA['born this way']['sex interest'], 
                                    personB['born this way']['sex interest'])
            self.current_sex_life = round((self.max_sex_life + self.min_sex_life) / 2, 3)
            self.drive_compatibility = 1 - round(self.max_sex_life - self.min_sex_life, 3)
            
        def conceive(self):
            """
            TODO: actually do something with the fertility scores
            """
            if not self.can_conceive or not self.is_sexual:
                return False
            
            chance_modifier = 1
            
            # update known age
            self.mother_age += 1
            if self.mother_age > 50:
                self.can_conceive = False
                return False
            elif self.mother_age > 41:
                chance = 0.01
            elif self.mother_age > 36:
                chance = 0.2
            elif self.mother_age > 25:
                chance = 0.35
            elif self.mother_age > 14:
                chance = 0.45
            else:
                chance = 0.
            updated_chance = chance * self.fertility * chance_modifier
            # print(f'mother: {self.mother_age}, chance: {updated_chance}')
            if rand() < updated_chance:
                return True
            return False
            
        def evolve(self):
            """
            Reasoning: the tendencies in relationships to have less sex as time 
            progresses, as well as the tendency to have better sex as time progresses
            and two partners know each other better, cancel each other out, thus
            not 
            """
            report = {'change' : False}
            if not self.is_sexual:
                if self.sexuality_compatible:
                    if rand() < 0.001 * self.drive_compatibility:
                        self.is_sexual = True

            # chance of something changing
            something_chance = ...

            return {
                'change' : False
            }
            
        def get_parents(self):
            return self.mother, self.father

