from ..utils import *

def random_trait():
    return rand_choice(['lawful-chaotic', 'nice-nasty', 'honest-false'])

class Personality():
    def __init__(self, person) -> None:
        self.person = person
        # personality
        self.personality = {
            'lawful-chaotic': normal_in_range(0.5, 0.3),
            'nice-nasty': normal_in_range(0.5, 0.3),
            'honest-false': normal_in_range(0.5, 0.3), 
        }

        # attitude
        self.attitude = {
            'dream' : normal_in_range(0.4, 0.2),
            'outgoing' : normal_in_range(0.6, 0.2),
        }
    
    def influence_trait(self, trait, chance, modifier):
        if rand() < chance:
            self.personality[trait] = fair_mod(self.personality[trait], modifier, 1, 3)
            return True
        return False

    def trigger(self, trigger, params = None):
        if trigger == 'grief':
            ch = 0.2 * (1 - self.attitude['dream']) # bigger chance if dreamer
            trait = random_trait()
            mod = normal_in_range(0., 0.1, 0.5, -0.5)
            change = self.influence_trait(trait, ch, mod)
        elif trigger == 'trauma':
            ch = 0.2 * (1 - self.attitude['dream']) # bigger chance if dreamer
            trait = random_trait()
            mod = normal_in_range(0., 0.1, 0.5, -0.5)
            change = self.influence_trait(trait, ch, mod)

        return {
            'topic' : 'personality change',
            'change' : change,
            'trait' : trait,
            'trigger' : trigger,
            'mod' : mod
        }

    """
    INFO FUNCTIONS
    """
    def get_trait(self, trait):
        return self.personality[trait]

    def get_personality(self, core = False):
        if core:
            return list(self.personality.values())
        return {
            ** self.personality,
            ** self.attitude
        }
    
    def get_attitude(self):
        return self.attitude
    