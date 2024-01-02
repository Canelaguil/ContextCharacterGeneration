from ..utils import *

class HomoSociologicus():
    def __init__(self, person, community, born_like, personality, income_class) -> None:

        self.person = person 
        self.personality = personality
        self.community = community
        self.person_key = person.unique_id
        self.income_class = income_class
        self.set_expression_of_expressions(born_like)
        self.tasks = MessageInbox(self)

        # needs
        self.independent = False
        self.needs_care = False
        self.taken_care_of = False
        self.caretaker = False
        
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
            self.needs_care = True

        # filter for age
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

    """
    UTILS
    """
    def become_adult(self):
        look_at_me_now = self.community.get_person(self.person_key)
        if look_at_me_now['genetics']['disabilities'] != []:
            self.needs_care = True
        else:
            self.needs_care = False

    def go_find_job(self, age):
        # change to message?
        self.person.occupation.find_job(age)

    

    """
    INFO
    """
    def homo_sociologicus(self):
        return {
            'means' : {
                'independent' : self.independent, 
                'taken_care_of' : self.taken_care_of, 
                'caretaker' : self.caretaker, 
                'needs_care' : self.needs_care
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
    def __init__(self, person, community, born_like, whoami, income_class) -> None:
        super().__init__(person, community, born_like, whoami, income_class)
        self.independent_age = HomoSociologicus.female_for_indepenence

    def marriage_wish(self):
        look_at_me_now = self.community.get_person(self.person_key)
        return 0.3
        # independent :  70 / 1 , 90 / 0
        # sexuality : 95 / straigth, 85 / bisexual , 50 / gay
        # romance : 95 / 1, 85 / 0
        # lawful : 99 / 1, 50 / 0

    def childhood(self, age, record):
        self.needs_care = True

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

class ManMA(HomoSociologicus):
    def __init__(self, person, community, born_like, whoami, income_class) -> None:
        super().__init__(person, community, born_like, whoami, income_class)
        self.independent_age = HomoSociologicus.male_for_indepenence

    def marriage_wish(self):
        # look_at_me_now = self.community.get_person(self.person_key)
        # personality = look_at_me_now['personality']
        return 0.15
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

        
        

class Neutral(HomoSociologicus):
    def __init__(self, person, community, born_like, whoami, income_class) -> None:
        super().__init__(person, community, born_like, whoami, income_class)
        self.independent_age = HomoSociologicus.male_for_indepenence

    
    def childhood(self, age, record):
        ...

    def adulthood(self, age, record):
        ...

