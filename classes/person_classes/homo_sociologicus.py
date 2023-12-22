from ..utils import *

class HomoSociologicus():
    def __init__(self, person, born_like, personality) -> None:

        self.person = person        
        self.set_expression_of_expressions(personality, born_like)
        self.tasks = MessageInbox(self)
        
    def set_expression_of_expressions(self, personality, born_like):
        """
        How much do they actually express of their gender & sexuality?
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
                'independent' : True, 
                'taken_care_of' : True, 
                'caretaker' : True, 
                'needs_care' : False
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
    def __init__(self, person, born_like, personality) -> None:
        super().__init__(person, born_like, personality)

class ManMA(HomoSociologicus):
    def __init__(self, person, born_like, personality) -> None:
        super().__init__(person, born_like, personality)

class Neutral(HomoSociologicus):
    def __init__(self, person, born_like, personality) -> None:
        super().__init__(person, born_like, personality)
