from ..utils import *

class BirdsAndBees():
        """
        Directs conception and sex life progression
        """
        def __init__(self, relationship, personA : dict, personB : dict, 
                     sexualRelationship : bool) -> None:
            self.relationship = relationship
            self.personA = personA
            self.personB = personB
            
            # nature of sexual relationship
            self.is_sexual = sexualRelationship
            if sexualRelationship:
                self.make_sexual()
            
            self.sexuality_compatible = sexuality_match(self.personA['sex'], self.personB['sex'],
                                                        self.personA['born this way']['sexuality label'],
                                                        self.personB['born this way']['sexuality label'])
            self.sexuality_score = sexuality_match(self.personA['sex'], self.personB['sex'],
                                                    self.personA['born this way']['sexuality'],
                                                    self.personB['born this way']['sexuality'], 
                                                    'score')
            
            # conception variables
            if self.personA['sex'] != self.personB['sex']:
                self.can_conceive = True         
                if self.personB['sex'] == 'm':
                    self.mother = self.personA['key']
                    self.father = self.personB['key']
                    self.mother_age = self.personA['age']
                else:
                    self.mother = self.personB['key']
                    self.father = self.personA['key']
                    self.mother_age = self.personB['age']
                self.fertility = min(self.personA['genetics']['fertility'], 
                                     self.personB['genetics']['fertility'])

            else:
                self.can_conceive = False

            
            
        def make_sexual(self):
            """
            Determine nature of sexual relationship
            """
            # sex life variables
            self.is_sexual = True
            self.sex_degree = (self.personA['born this way']['sex interest'] + self.personB['born this way']['sex interest']) / 2
            self.max_sex_life = max(self.personA['born this way']['sex interest'], 
                                    self.personB['born this way']['sex interest'])
            self.min_sex_life = min(self.personA['born this way']['sex interest'], 
                                    self.personB['born this way']['sex interest'])
            self.current_sex_life = round((self.max_sex_life + self.min_sex_life) / 2, 3)
            self.drive_compatibility = 1 - round(self.max_sex_life - self.min_sex_life, 3)

        def conceive(self, chance_modifier = 1):
            """
            Chance of conception based on age and fertility score
            """
            if not self.can_conceive or not self.is_sexual:
                return False
            
            # update known age
            self.mother_age += 1
            if self.mother_age > 50:
                self.can_conceive = False
                return False
            elif self.mother_age > 41:
                chance = 0.1
            elif self.mother_age > 36:
                chance = 0.3
            elif self.mother_age > 25:
                chance = 0.6
            elif self.mother_age > 15:
                chance = 0.7
            else:
                chance = 0.
            updated_chance = chance * self.fertility * chance_modifier
            # print(f'mother: {self.mother_age}, chance: {updated_chance}')
            if rand() < updated_chance:
                return True
            return False
            
        def evolve(self, romance_report):
            """
            Reasoning: the tendencies in relationships to have less sex as time 
            progresses, as well as the tendency to have better sex as time progresses
            and two partners know each other better, cancel each other out, thus
            not 
            """
            report = {'change' : False}
            if not self.is_sexual: 
                # ch = rand()
                # # chance of one night stand
                # if (romance_report['state A'] != 'nothing' or romance_report['state B']) and ch < 0.1:
                #     self.one_time_thing = True
                # else:
                #     return report
                return report
                
            # chance of something changing
            something_chance = 0.2 * (1-self.drive_compatibility)
            if rand() < something_chance:
                loc = self.min_sex_life
                scale = (self.max_sex_life - self.min_sex_life) / 2
                old_sex = self.sex_degree
                self.sex_degree = normal_in_range(loc, scale, round_dec=3)
                report['change'] = True
                report['value change'] = self.sex_degree - old_sex
            report['sex degree'] = self.sex_degree

            return report
    
        def get_status(self): 
            return {
                'sexual' : self.is_sexual
            }
        
        def get_parents(self):
            return self.mother, self.father

