from ..utils import *

class HomoSociologicus():
    def __init__(self, person, born_like, whoami, income_class) -> None:

        self.person = person 
        self.whoami = whoami
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

    def evolve(self, age, record):
        if age < self.independent_age:
            self.childhood(age, record)
        else:
            self.adulthood(age, record)
        return {
                'independent' : self.independent, 
                'taken_care_of' : self.taken_care_of, 
                'caretaker' : self.caretaker, 
                'needs_care' : self.needs_care
            }

    def go_find_job(self, age):
        # change to message?
        self.person.occupation.find_job(age)

"""
Homo sociologicus classes
"""
class WomanMA(HomoSociologicus):
    def __init__(self, person, born_like, whoami, income_class) -> None:
        super().__init__(person, born_like, whoami, income_class)
        self.independent_age = HomoSociologicus.female_for_indepenence

    def childhood(self, age, record):
        ...

    def adulthood(self, age, record):
        ...

class ManMA(HomoSociologicus):
    def __init__(self, person, born_like, whoami, income_class) -> None:
        super().__init__(person, born_like, whoami, income_class)
        self.independent_age = HomoSociologicus.male_for_indepenence

    def childhood(self, age, record):
        ...

    def adulthood(self, age, record):
        if not record['occupation']['has job']:
            if rand() < 0.5:
                self.go_find_job(age)
        else:
            # this could be more efficient
            if record['occupation']['income'] > 0.8:
                self.independent = True
            else:
                self.independent = False

class Neutral(HomoSociologicus):
    def __init__(self, person, born_like, whoami, income_class) -> None:
        super().__init__(person, born_like, whoami, income_class)
        self.independent_age = HomoSociologicus.male_for_indepenence

    
    def childhood(self, age, record):
        ...

    def adulthood(self, age, record):
        ...

