from ..utils import *

class Personality():
    def __init__(self, person) -> None:
        self.person = person
        # personality
        self.lawfulchaotic = normal_in_range(0.5, 0.4)
        self.nicenasty = normal_in_range(0.5, 0.4)
        self.honestfalse = normal_in_range(0.5, 0.4)

        # attitude
        self.dream = normal_in_range(0.4, 0.2)
        self.outgoing = normal_in_range(0.5, 0.2)

    def influence_lc(self, chance, modifier):
        if rand() < chance:
            self.lawfulchaotic = fair_mod(self.lawfulchaotic, modifier, 1, 3)
            return True
        return False

    def influence_nn(self, chance, modifier):
        if rand() < chance:
            self.nicenasty = fair_mod(self.nicenasty, modifier, 1, 3)
            return True
        return False   
        
    def influence_hf(self, chance, modifier):
        if rand() < chance:
            self.honestfalse = fair_mod(self.honestfalse, modifier, 1, 3)
            return True
        return False
    
    def get_trait(self, trait):
        return {
            'lc': self.lawfulchaotic,
            'nn': self.nicenasty,
            'hf': self.honestfalse, 
            'dream' : self.dream
        }[trait]

    def get_personality(self, core = False):
        if core:
            return [self.lawfulchaotic, self.nicenasty, self.honestfalse]
        p = {
            'lawful-chaotic': self.lawfulchaotic,
            'nice-nasty': self.nicenasty,
            'honest-false': self.honestfalse, 
        }
        return p
    
    def get_attitude(self):
        a = {
            'outgoing' : self.outgoing,
            'dream' : self.dream,
        }
        return a
    