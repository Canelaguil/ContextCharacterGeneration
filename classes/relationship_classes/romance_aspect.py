from ..utils import *

class LoveIsAStateMachine():
    def __init__(self, relationship, subject, love_object, can_marry=True, start='nothing') -> None:
        self.relationship = relationship
        self.subject = subject
        self.object = love_object

        # can the subject love the object?
        if self.subject['born this way']['sexuality label'] == 'gay':
            if self.object['sex'] == self.subject['sex']:
                self.can_love = True
            else:
                self.can_love = False
        elif self.subject['born this way']['sexuality label'] == 'straight':
            if self.object['sex'] != self.subject['sex']:
                self.can_love = True
            else:
                self.can_love = False 
        else:
            self.can_love = True # lucky bisexuals
        self.can_marry = can_marry
        self.state = start 

    def turn(self, marriage_age_restraint=False, love_restraint=False):
        self.marriage_age_restraint = marriage_age_restraint
        self.love_restraint = love_restraint

        old_state = self.state
        # pre-relationship phases
        if self.state == 'nothing':
            self.state = self.nothing()
        elif self.state == 'crush':
            self.state = self.crush()
        elif self.state == 'in love':
            self.state = self.in_love()

        # relationship phases
        elif self.state == 'infatuation': 
            self.state = self.infatuation()
        elif self.state == 'honeymoon phase':
            self.state = self.honeymoon_phase()
        elif self.state == 'loveless':
            self.state = self.loveless()
        elif self.state == 'out of love':
            self.state = self.out_of_love()
        elif self.state == 'solid love':
            self.state = self.solid_love()

        if old_state != self.state:
            return True
        return False
    
    def start_relationship(self):        
        if self.can_marry:
            self.can_break_up = False
        else:
            self.can_break_up = True
    
    def receive_declaration(self, status={}):
        """
        INPUT: current relationship status
        """
        rng = rand()
        if self.state == 'nothing': 
            if rng < 0.02 and self.can_love:
                self.state = 'infatuation'
                self.start_relationship()
                return True
            return False
        elif self.state == 'crush':
            if rng < 0.7:
                self.state = 'infatuation'
                self.start_relationship()
                return True
            return False
        elif self.state == 'in love':
            if rng < 0.95:
                self.state = 'honeymoon'
                self.start_relationship()
                return True
            return False
        return False
    
    """
    PRE-RELATIONSHIP PHASES 
    """
    def nothing(self):
        if not self.can_love:
            return 'nothing'
        if rand() < 0.005:
            return 'crush'
        return 'nothing'

    def crush(self):
        rng = rand()
        if rng < 0.33:
            return 'nothing'
        elif rng < 0.66:
            return 'in love'
        else:
            return 'crush'

    def in_love(self):
        rng = rand()
        if rng < 0.5:
            return 'in love'
        elif rng < 0.7:
            return 'nothing'
        else:
            if self.relationship.declaration(self.subject['key']):
                self.start_relationship()
                return 'honeymoon phase'
            else:
                rng2 = rand()
                if rng2 < 0.2:
                    return 'crush'
                else: 
                    return 'nothing'

    """
    RELATIONSHIP PHASES
    """
    def infatuation(self):
        rng = rand()
        if rng < 0.2:
            return 'out of love'
        elif rng < 0.7:
            return 'infatuation'
        else:
            return 'solid love'

    def loveless(self):
        rng = rand()
        if rng < 0.01 and self.can_love:
            return 'infatuation'
        return 'loveless'

    def honeymoon_phase(self):
        rng = rand()
        if rng < 0.05:
            return 'out of love'
        elif rng < 0.7:
            return 'honeymoon phase'
        else:
            return 'solid love'
    
    def out_of_love(self):
        rng = rand()
        if self.can_break_up:
            if rng < 0.5:
                return 'out of love'
            elif rng < 0.98:
                self.relationship.break_up(self.subject['key'])
                return 'nothing'
        else:
            if rng < 0.95:
                return 'out of love'
        return 'solid love'

    def solid_love(self):
        rng = rand()
        if rng < 0.95:
            return 'solid love'
        else:
            return 'out of love'


class Romance():
    def __init__(self, relationship, personA, personB, friendshiplevel=0) -> None:
        self.relationship = relationship
        self.personA = personA
        self.personB = personB
        
        self.influence_love(friendshiplevel)

    def influence_love(self, friendship):
        pass

    def declaration(self, origin):
        pass

    def break_up(self, origin):
        pass

    def evolve(self):

        return {
            'change' : False
        }
