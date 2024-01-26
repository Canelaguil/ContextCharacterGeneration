from ..utils import *

def random_trait():
    return rand_choice(['lawful-chaotic', 'nice-nasty', 'honest-false'])

class Personality():
    """
    Represents the personality and attitude of Person
    """
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
        """
        Influence a trait through fair modification 
        """
        if rand() < chance:
            if trait in self.personality:
                self.personality[trait] = fair_mod(self.personality[trait], modifier, 1, 3)
                return True
            elif trait in self.attitude:
                self.attitude[trait] = fair_mod(self.attitude[trait], modifier, 1, 3)
                return True
        return False
    
    def trigger(self, trigger, params = None):
        """
        Receive & process personality triggers
        """
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
        elif trigger == 'neglect': 
            ch = 0.5
            trait = 'outgoing'
            mod = - 0.3 # relative to pre-existing outgoing
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
        """
        Returns specific trait
        """
        if trait in self.personality:
            return self.personality[trait]
        elif trait in self.attitude:
            return self.attitude[trait]
        else:
            fatal_error(f'wrong trait request: {trait}')

    def get_personality(self, core = False):
        """
        Returns personality & attitude
        Core specifies whether just the personality has to be returned
        as a vector.
        """
        if core:
            return list(self.personality.values())
        return {
            ** self.personality,
            ** self.attitude
        }
    
    