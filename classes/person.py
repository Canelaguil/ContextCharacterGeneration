import numpy as np
from mesa import Agent, Model
from .home import Home
from .utils import *
from .person_classes import *

class Person(Agent):
    def __init__(self, unique_id: int, model: Model, birth_year : int, 
                 income_class : int, faction : str, parent_info={}, sex='r',  
                 age=0, first_gen=False) -> None:
        super().__init__(unique_id, model)
        self.community = model
        self.birth_year = birth_year
        if age != 0:
            self.birth_year -= age
        self.born_this_way(sex)

        self.income_class = income_class
        self.parent_key = parent_info if first_gen else parent_info['key']
        self.home = None
        self.age = age
        self.alive = True
        self.first_gen = first_gen
        self.faction = faction
        self.romantic_relationship_status = {
            'taken' : False if not first_gen else True,
            'married' : False if not first_gen else True,
            'relationships' : []
        }

        # Init submodules 
        self.messages = MessageInbox(self)
        self.memory = Memory(self, self.model) 
        self.memory.add_event({'topic' : 'birth', 'year' : self.birth_year})
        self.personality = Personality(self)
        if self.first_gen:
            self.names = Naming(self.sex, '', '', '', True)
            self.body = Body(self, {}, {}, True)
            self.network = Network(self, self.model, {}, {})
        else:
            self.init_essentials_legacy(parent_info)

        self.occupation = Occupation(self, self.model, self.income_class, 
                                     self.personality.get_personality())
        if self.sex == 'f':
            self.homsoc = WomanMA(self, self.model, self.get_homsoc_attributes(), 
                                  self.personality.get_personality(), 
                                  self.income_class, age, self.body.disabilities)
        elif self.sex == 'm':
            self.homsoc = ManMA(self, self.model, self.get_homsoc_attributes(), 
                                  self.personality.get_personality(), 
                                  self.income_class, age, self.body.disabilities)
            if self.age > Occupation.adult_age:
                self.occupation.find_job(self.age)  
        else: 
            self.homsoc = Neutral(self, self.model, self.get_homsoc_attributes(), 
                                  self.personality.get_personality(), 
                                  self.income_class, age, self.body.disabilities)
            
        self.mark_for_death = False # am I gonna die this year?

    
    def init_essentials_legacy(self, parent_info): 
        """
        Init submodules for all people with parents (=not first gen)
        """
        # get parent info 
        mother_key, father_key = parent_info['people']
        mother = self.community.get_person(mother_key)
        father = self.community.get_person(father_key)
        surnames = [father['surname'], mother['surname']]
        self.names = Naming(self.sex, father['name'], mother['name'], 
                            surnames)
        self.body = Body(self, father['genetics'], mother['genetics'])
        self.network = Network(self, self.model, mother, father)

    def born_this_way(self, sex):
        """
        Define sex, gender & sexuality
        """
        # sex
        if sex == 'r': self.sex = 'm' if rand() < Person.bio_mf_ratio else 'f'
        else: self.sex = sex

        # sexuality
        # primary sexuality is the label, secondary the "place on the spectrum"
        self.primary_sexuality = rand_choice(['straight', 'bi', 'gay'], 
                                             p=[0.8, 0.1, 0.1])
        
        loc, scale = {'straight' : (0.05, 0.05), 
                      'bi' : (0.5, 0.1), 
                      'gay' : (0.9, 0.05)}[self.primary_sexuality]
        self.secondary_sexuality = normal_in_range(loc, scale)
        self.romance_interest = normal_in_range(0.7, 0.15)
        self.sex_interest = normal_in_range(0.7, 0.15)

        # gender expression
        # the assumption here is that knowing you're not straight makes you more 
        # open to the possiblity you might not be cis either
        if self.primary_sexuality == 'straight' : 
            loc2, scale2 = (0.1, 0.1)
        else:
            loc2, scale2 = (0.3, 0.2)
        self.gender_expression = normal_in_range(loc2, scale2) # 0 = 1-1 with sex

    def die(self, cause=''):
        self.alive = False
        self.network.unravel(cause)
        if cause == '':
            cause = self.body.death_cause
        i_died = {
            'topic' : 'person died', 
            'key' : self.unique_id,
            'cause' : cause
        }
        if self.home != None:
            self.community.message_home(self.home['unique id'], i_died)
        self.community.report_death(self.unique_id)
        self.memory.add_event({
            'topic' : 'death',
            'cause' : cause
        })

    """
    PHASES / STEPS
    """
    def people(self):
        if not self.alive: 
            return        
        self.age += 1

        # health update
        health_report = self.body.yearly_step(self.age)
        if health_report['death']:
            self.mark_for_death = True

        # job update
        occupation_report = self.occupation.evolve(self.age)
        home_msg ={
            'topic' : 'income report',
            'sender' : self.unique_id,
            'report' : occupation_report
        }
        if self.home != None:
            self.community.message_home(self.home['unique id'], home_msg)
        else:
            log_error('no home', self.description())

        record = {
            'health' : health_report,
            'occupation' : occupation_report
        }

        homsoc_report = self.homsoc.evolve(self.age, record, self.romantic_relationship_status)
        record['homsoc'] = homsoc_report
        self.memory.add_record(record)

    def lovedeathbirth(self): 
        if self.mark_for_death:
            self.die(self.body.death_cause)
    
    def houses(self):
        return

    def post_processing(self):
        msg = self.messages.get()
        while msg != None:
            topic = msg['topic']
            if topic == 'new relationship':
                self.relationship_processing(msg)
            elif topic in ['relationship change', 'unmarried', 'single']: # relationship label
                self.update_relationship_status(msg)
                # TODO: notify network
                self.memory.add_event(msg)
            elif topic == 'feelings change':
                self.memory.add_event(msg)
            elif topic == 'person died': 
                self.memory.add_event(msg)
                if msg['friendship label'] in ['friend', 'good friend']:
                    personality_effect = self.personality.trigger('grief')
                    if personality_effect['change']:
                        self.memory.add_event(personality_effect)
            elif topic == 'not enough income':
                self.body.trigger('starving')
                self.homsoc.situation_change(msg, self.age)
                self.memory.add_event(msg)
            elif topic == 'get a job':
                self.occupation.find_job(self.age)
            elif topic == 'job notice':
                self.memory.add_event(msg)
            # elif topic == 'die':
            #     self.mark_for_death = True
            elif topic in ['now caretaker', 'not caretaker', 'new caretaker', 
                           'neglected', 'need care']:
                self.homsoc.situation_change(msg, self.age)
                if self.age != 0:
                    self.memory.add_event(msg)
            elif topic == 'update':
                self.memory.add_event(msg)
            else:
                log_error('person received unrecognized message', msg)
            msg = self.messages.get()

    """
    UTIL FUNCTIONS
    """        
    def receive_message(self, msg):
        if not self.alive:
            return
        if msg['topic'] == 'event':
            self.process_event(msg)
            return
        self.messages.add(msg)

    def relationship_processing(self, msg):
        if msg['label'] == 'parentchild':
            self.network.process_parent_child(msg, self.age)
            if self.sex == 'f' :
                self.body.trigger('childbirth')
        elif msg['label'] == 'grandparentchild':
            self.network.process_parent_child(msg, self.age, 'birth', True)
        elif msg['label'] in ['aunclenibling', 'greatgrandparentchild']:
            # if msg['label'] == 'greatgrandparentchild':                
            #     print(self.unique_id)
            self.network.process_other_family(msg)
        else:
            self.update_relationship_status(msg) 
            self.network.add_relationship(msg)

        # if self.age != 0: # skip memories for family new relationships
        self.memory.add_event(msg)

    def move(self, home_info):
        self.home = home_info

    def update_relationship_status(self, info):
        # end relationship 
        if info['topic'] in ['unmarried', 'single']:
            # TODO : account for cheating
            self.romantic_relationship_status['married'] = False
            self.romantic_relationship_status['taken'] = False
            return

        # start relationship
        self.romantic_relationship_status['taken'] = info['committed']
        if info['label'] == 'spouse':
            self.romantic_relationship_status['married'] = True
        if info['label']  in ['spouse', 'partner']:
            self.romantic_relationship_status['relationships'].append(info['key'])

    def process_event(self, info):
        self.memory.add_event(info)
        event = info['event']
        if event in ['famine', 'plague']:
            self.body.trigger(event)
            personality_effect = self.personality.trigger('trauma')
            if personality_effect['change']:
                self.memory.add_event(personality_effect)
        elif event == 'war':
            if self.sex == 'm' and self.age > Body.adult_age:
                self.body.trigger(event)
            personality_effect = self.personality.trigger('trauma')
            if personality_effect['change']:
                self.memory.add_event(personality_effect)
        elif event == 'faction upheaval':
            ...


    """
    INFO FUNCTIONS
    """

    def get_homsoc_attributes(self):
        return {
            'sexuality label' : self.primary_sexuality,
            'sexuality' : self.secondary_sexuality, 
            'romantic interest' : self.romance_interest,
            'sex interest' : self.sex_interest, 
            'gender expression' : self.gender_expression,
            'sex' : self.sex,
        }
    
    def get_relationship_status(self):
        return self.romantic_relationship_status
    
    def in_short(self):
        return {
            'name' : self.names.full(),
            'age' : self.age
        }
    
    def whoisthis(self):
        """
        Short summary for descriptive purposes
        """
        return {
            'key' : self.unique_id, 
            'name' : self.names.full(),
            'age' : self.age,
            'alive' : self.alive,
            'sex' : self.sex, 
            'parents' : self.network.get_parents()
        }

    def description(self, final=False) -> dict:
        """
        Long description for json objects
        """
        me = {
            'alive' : self.alive,
            'name' : self.names.first_name(),
            'surname' : self.names.last_name(),
            'full name' : self.names.full(),
            'born this way' : self.get_homsoc_attributes(),
            'age' : self.age,
            'birth year' : self.birth_year,
            'sex' : self.sex,
            'faction' : self.faction,
            'income class' : self.income_class, 
            'personality' : self.personality.get_personality(),
            'attitude' : self.personality.get_attitude(),
            'homsoc' : self.homsoc.homo_sociologicus(),
            'network' : self.network.links(),
            'occupation' : self.occupation.resume(),
            'genetics' : self.body.pass_gens(), 
            'memory' : self.memory.summary(),
            'key' : self.unique_id,
            'home' : self.home, 
            'relationship status' : self.get_relationship_status()
        }
        if final:
            me['friends'] = self.network.get_friends()
            me['enemies'] = self.network.get_enemies()
        return me
    

