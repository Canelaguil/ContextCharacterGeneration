from ..utils import *

class HomoSociologicus():
    def __init__(self, person, community, born_like, personality, income_class, 
                 age=0, disabilities=[]) -> None:

        self.person = person 
        self.personality = personality
        self.community = community
        self.person_key = person.unique_id
        self.income_class = income_class
        self.set_expression_of_expressions(born_like)
        self.tasks = MessageInbox(self)
        self.ideal_no_friends = int(self.personality['outgoing'] * HomoSociologicus.no_friends)

        # needs
        if age == 0:
            self.independent = False
            self.needs_care = True
            self.taken_care_of = True
            self.caretaker = True
        else:
            self.independent = True
            self.needs_care = disabilities != []
            self.taken_care_of = False
            self.caretaker = False

        # flags set
        self.flags = set()
        
    def set_expression_of_expressions(self, born_like):
        """
        How much do they actually express of their gender & sexuality?
        TODO: factor in perosnality?
        """
        # init variables relating to this
        self.sex = born_like['sex']
        self.sexuality_label = born_like['sexuality label']
        self.sexuality = born_like['sexuality']
        self.romantic_interest = born_like['romantic interest']
        self.sex_interest = born_like['sex interest']
        self.gender_expression = born_like['gender expression']

        # gender
        loc = 0.5 * self.gender_expression
        scale = 0.5 * (self.gender_expression - loc)
        self.gender_expression_expression = normal_in_range(loc, scale, 
                                                            self.gender_expression)
        # sexuality
        # TODO: modify with lawfulness
        loc2 = 0.6 * self.sexuality
        scale2 = 0.4 * (self.sexuality - loc2)
        self.sexuality_expression = normal_in_range(loc2, scale2, self.sexuality)

    """
    EVOLVE
    """
    def evolve(self, age, record, relationship_status):
        # check for disabilities
        if 'new_disability' in record['health']['health']:
            look_at_me_now = self.community.get_person(self.person_key)
            addr = look_at_me_now['home']['unique id']
            self.need_care(addr)

        # filter for age
        # print(self.independent_age)
        if age < self.independent_age:
            self.childhood(age, record)
        else:
            if age == self.independent_age:
                self.become_adult()
            self.adulthood(age, record)

            # marriage wish
            # TODO : check for existing relationships
            if not relationship_status['married'] and rand() < self.marriage_wish():
                it = {
                    'topic' : 'marriage', 
                    'motivation' : 'convention', 
                    'sex' : self.sex,
                    'age' : age,
                    'faction' : self.person.faction,
                    'source' : self.person_key, 
                    'income class' : self.income_class,
                    'personality' : self.personality,
                    'situation' : self.homo_sociologicus(),
                }
                self.community.express_intention(it)

        # return current state
        return {
                'independent' : self.independent, 
                'needs_care' : self.needs_care,
                'taken_care_of' : self.taken_care_of, 
                'caretaker' : self.caretaker, 
            }
    
    def situation_change(self, update, age):
        change = update['topic']
        if change == 'now caretaker':
            self.caretaker = True
            self.flags.add('caretaker')
        elif change == 'not caretaker':
            self.caretaker = False
        elif change == 'new caretaker':
            self.taken_care_of = True
        elif change == 'neglected':
            if age != 0:
                self.taken_care_of = False
                self.flags.add('neglected')
        elif change == 'need care':
            self.need_care = True
        elif change == 'not enough income':
            self.flags.add('starving')
        else:
            log_error('Did not recognize that homsoc update.', update)

    def trigger(self, trigger):
        if trigger == 'faction upheaval':
            ...
        
    """
    UTILS
    """
    def become_adult(self):
        look_at_me_now = self.community.get_person(self.person_key)
        if look_at_me_now['genetics']['disabilities'] == []:
            addr = look_at_me_now['home']['unique id']
            self.i_dont_need_care(addr)
            # print('discharged')

        # notify network of adulthood
        adult_msg = {
            'topic' : 'newly adult',
            'source' : self.person_key
        }
        self.person.network.message_relationships(adult_msg)

    def need_care(self, home_key : int):
        self.needs_care = True
        msg = {
            'topic' : 'new care dependant',
            'key' : self.person_key
        }
        self.community.message_home(home_key, msg)

    def i_dont_need_care(self, home_key : int):
        self.needs_care = False
        self.taken_care_of = False
        msg = {
            'topic' : 'remove care dependant',
            'key' : self.person_key
        }
        self.community.message_home(home_key, msg)

    def go_find_job(self, age):
        # change to message?
        self.person.occupation.find_job(age)   

    def find_friend(self, age):
        it = {
            'topic' : 'friendship', 
            'sex' : self.sex,
            'age' : age,
            'source' : self.person_key, 
            'income class' : self.income_class,
            'personality' : self.personality,
            'situation' : self.homo_sociologicus(),
            'adress' : self.person.home
        }
        # print(it)
        self.community.express_intention(it) 

    """
    INFO
    """
    def homo_sociologicus(self):
        return {
            'means' : {
                'independent' : self.independent, 
                'taken_care_of' : self.taken_care_of, 
                'caretaker' : self.caretaker, 
                'needs_care' : self.needs_care, 
                'flags' : list(self.flags)
            },
            'expression'  : {
                'sexuality expression' : self.sexuality_expression,
                'gender expression expression' : self.gender_expression_expression,
            }
        }


"""
Homo sociologicus classes
"""
class WomanMA(HomoSociologicus):
    def __init__(self, person, community, born_like, whoami, income_class,
                 age=0, disabilities=[]) -> None:
        super().__init__(person, community, born_like, whoami, income_class,
                         age, disabilities)
        self.independent_age = 16 #HomoSociologicus.marriage_age_women

    def marriage_wish(self):
        look_at_me_now = self.community.get_person(self.person_key)
        return 0.7
        # independent :  70 / 1 , 90 / 0
        # sexuality : 95 / straigth, 85 / bisexual , 50 / gay
        # romance : 95 / 1, 85 / 0
        # lawful : 99 / 1, 50 / 0

    def childhood(self, age, record):
        self.needs_care = True
        if age == 3:
            self.find_friend(age)
        elif age > 4:
            if rand() < 0.8:
                self.find_friend(age)

    def adulthood(self, age, record):
        # motivate to go for independence
        if not record['occupation']['has job']:
            if rand() < 0.05:
                self.go_find_job(age)
        else:
            if record['occupation']['income'] > 0.8:
                self.independent = True
            else:
                self.independent = False

        # if not enough friends 
        friends = self.person.network.get_friends()
        if len(friends) < self.ideal_no_friends:
            self.find_friend(age)

class ManMA(HomoSociologicus):
    def __init__(self, person, community, born_like, whoami, income_class,
                 age=0, disabilities=[]) -> None:
        super().__init__(person, community, born_like, whoami, income_class,
                         age, disabilities)
        self.independent_age = 16 #HomoSociologicus.marriage_age_men

    def marriage_wish(self):
        """
        This would have been a good place for a more nuanced chance (influenced)
        """
        look_at_me_now = self.community.get_person(self.person_key)
        personality = look_at_me_now['personality']
        if self.independent:
            if self.sexuality_expression < 0.85:
                return 0.8
            else:
                return 0.5
        else:
            return 0.3
        pos_mods, neg_mods, vals = [], [], []

        # independent :  90 / 1 , 20 / 0
        pos_mods.append(0.9)
        neg_mods.append(0.2)
        vals.append(int(self.independent))

        # sexuality : 20 / 1, 90 / 0
        pos_mods.append(0.2)
        neg_mods.append(0.9)
        vals.append(self.sexuality_expression)

        # romance : 95 / 1, 20 / 0
        pos_mods.append(0.95)
        neg_mods.append(0.2)
        vals.append(self.romantic_interest)

        # lawful : 99 / 0, 20 / 1 
        pos_mods.append(0.95)
        neg_mods.append(0.2)
        vals.append(self.personality['lawful-chaotic'])

        try:
            ch = get_modified_chance(0.5, pos_mods, neg_mods, vals)
            print(rand() < ch)
            print(ch)
        except:
            ch = get_modified_chance(0.5, pos_mods, neg_mods, vals)
            print(ch)
            print(pos_mods)
            print(neg_mods)
            print(vals)
        return ch

    def childhood(self, age, record):
        self.needs_care = True        
        if age == 3:
            self.find_friend(age)
        elif age > 4:
            if rand() < 0.8:
                self.find_friend(age)

    def adulthood(self, age, record):
        # motivate to go for independence
        if not record['occupation']['has job']:
            if rand() < 0.5:
                self.go_find_job(age)
        else:
            if record['occupation']['income'] > 0.8:
                self.independent = True
            else:
                self.independent = False

        # if not enough friends 
        friends = self.person.network.get_friends()
        if len(friends) < self.ideal_no_friends:
            self.find_friend(age)

class Neutral(HomoSociologicus):
    def __init__(self, person, community, born_like, whoami, income_class,
                 age=0, disabilities=[]) -> None:
        super().__init__(person, community, born_like, whoami, income_class,
                         age, disabilities)
        self.independent_age = 16 #HomoSociologicus.male_for_indepenence

    
    def childhood(self, age, record):
        if age == 3:
            self.find_friend(age)
        elif age > 4:
            if rand() < 0.5:
                self.find_friend(age)

    def adulthood(self, age, record):
        ...

