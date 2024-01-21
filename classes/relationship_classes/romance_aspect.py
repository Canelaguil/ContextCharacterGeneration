from ..utils import *

# TODO: ROMANCE RELATIONSHIP
class LoveIsAStateMachine():
    def __init__(self, romance, subject : dict, love_object : dict, can_marry=True, 
                 can_break_up=True, start='nothing') -> None:
        """
        TODO: young love
        """
        self.romance = romance
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
        self.can_break_up = can_break_up
        
        # just avoiding pedophilia as much as possible here
        if age_match(subject['age'], love_object['age']) < 0.8:
            self.can_love = False
            

        if start == 'generate':
            self.init_arranged()
        else:
            self.state = start 

    def init_arranged(self):
        if self.can_love:
            self.state = 'infatuation'
        else:
            self.state = 'loveless'

    """
    CORE FUNCTIONS
    """
    def turn(self, marriage_restraint, solid_love_restraint):
        self.marriage_restraint = marriage_restraint
        self.solid_love_restraint = solid_love_restraint

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
    
    def start_relationship(self, taken):        
        if self.can_marry and not taken: # if not already married or no marriage rights
            self.can_break_up = False
        else:
            self.can_break_up = True
    
    def end_relationship(self):
        self.state = 'nothing'

    def receive_declaration(self, status : dict):
        """
        INPUT: current relationship status
        """
        if not self.can_love:
            return False
        taken = status['taken']
        rng = rand()
        if self.state == 'nothing' and not taken: 
            if rng < 0.02 and self.can_love:
                self.state = 'infatuation'
                self.start_relationship(taken)
                return True
            return False
        elif self.state == 'crush':
            if not taken:
                if rng < 0.7:
                    self.state = 'infatuation'
                    self.start_relationship(taken)
                    return True
            else:
                if rng < 0.2:
                    self.state = 'infatuation'
                    self.start_relationship(taken)
                    return True
            return False
        elif self.state == 'in love':
            if not taken:
                if rng < 0.95:
                    self.state = 'honeymoon'
                    self.start_relationship(taken)
                    return True
            else:
                if rng < 0.5:
                    self.state = 'honeymoon'
                    self.start_relationship(taken)
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
        taken = self.romance.model.get_relationship_status_person(self.subject['key'])['taken']
        rng = rand()
        if not taken:
            if rng < 0.33:
                return 'nothing'
            elif rng < 0.66:
                return 'in love'
            else:
                return 'crush'
        else:
            if rng < 0.5:
                return 'nothing'
            elif rng < 0.7: # 20 % chance of properly falling in love while taken
                return 'in love'
            else:
                return 'crush'


    def in_love(self):
        rng = rand()
        taken = self.romance.model.get_relationship_status_person(self.subject['key'])['taken']
        if rng < 0.5:
            return 'in love'
        elif rng < 0.8 and not self.marriage_restraint:
            if self.romance.declaration(self.subject['key']):
                print(self.subject['key'])
                self.start_relationship(taken)
                # print(self.subject)
                return 'honeymoon phase'
            else:
                rng2 = rand()
                if rng2 < 0.2:
                    return 'crush'
                else: 
                    return 'nothing'
                
        else:
            return 'nothing'

    """
    RELATIONSHIP PHASES
    """
    def infatuation(self):
        rng = rand()
        if rng < 0.2:
            return 'out of love'
        elif rng < 0.5 and not self.solid_love_restraint:
            return 'solid love'
        else:
            return 'infatuation'

    def loveless(self):
        rng = rand()
        if rng < 0.01 and self.can_love:
            return 'infatuation'
        return 'loveless'

    def honeymoon_phase(self):
        rng = rand()
        if rng < 0.05:
            return 'out of love'
        elif rng < 0.35 and not self.solid_love_restraint:
            return 'solid love'
        else:
            return 'honeymoon phase'
    
    def out_of_love(self):
        rng = rand()
        if self.can_break_up:
            if rng < 0.5:
                return 'out of love'
            elif rng < 0.98:
                print(f"{self.subject['key']} wants to break up")
                # self.romance.break_up(self.subject['key'])
                # return 'nothing'
        else:
            if rng < 0.95:
                return 'out of love'
        return 'infatuation'

    def solid_love(self):
        rng = rand()
        if rng < 0.98 and not self.solid_love_restraint:
            return 'solid love'
        else:
            return 'out of love'

class Romance():
    """
    Represents Romance aspect of Relationship
    """
    def __init__(self, relationship, model, personA : dict, personB : dict, initA='nothing',
                  initB='nothing') -> None:
        self.relationship = relationship
        self.model = model
        
        # check if couple would potentially be able to marry / break up
        if Romance.equal_rights or (personA['sex'] != personB['sex']):
            can_marry = True
            can_break_up = Romance.can_divorce
        else:
            can_marry = False
            can_break_up = True

        # init state machines
        self.state_machineA = LoveIsAStateMachine(self, personA, personB, can_marry, 
                                                  can_break_up, initA)
        self.state_machineB = LoveIsAStateMachine(self, personB, personA, can_marry, 
                                                  can_break_up, initB)
        
        self.machines = {
            personA['key'] : self.state_machineA,
            personB['key'] : self.state_machineB
        }

    def declaration(self, receiver):
        """
        Declare love
        """
        status = self.model.get_relationship_status_person(receiver)
        response = self.machines[receiver].receive_declaration(status)
        msg = {
            'topic' : 'declaration', 
            'result' : 'accepted' if response else 'rejected', 
            'target' : receiver
        }
        self.relationship.update_people(msg)
        return response

    def break_up(self, origin):
        """
        Break up relationship
        """
        for p in self.machines.items():
            p.break_up()

    def get_states(self):
        """
        Returns love states of the pair
        """
        return {
            'state A' : self.state_machineA.state,
            'state B' : self.state_machineB.state,
        }
    
    def get_state(self, source):
        """
        Returns love state of [source]
        """
        return self.machines[source].state

    def evolve(self, friendship_state, adults):
        """
        Evolve romantic relationship through state machine and its conditions,
        and report back any change
        """
        # Check if people are old enough to enter a relationship / marriage
        if adults != [True, True]:
            age_restraint = True
        else:
            age_restraint = False

        # check if people are friends enough to have a solid love relationship
        if friendship_state['score'] < 1:
            solid_love_restraint = True
        else:
            solid_love_restraint = False
        changeA = self.state_machineA.turn(age_restraint, solid_love_restraint)
        changeB = self.state_machineB.turn(age_restraint, solid_love_restraint)
        change = True if changeA or changeB else False
        return {
            'change' : change,
            'change A' : changeA,
            'state A' : self.state_machineA.state,
            'change B' : changeB,
            'state B' : self.state_machineB.state,
        }
