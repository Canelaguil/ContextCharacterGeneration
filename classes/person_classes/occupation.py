from ..utils import *

def job_volatility(lawful : bool, honest : bool):
    """
    Returns scale for normal distribution change of occupation income.
    """
    scale = 0.05
    if not lawful: 
        scale += 0.1
    if not honest:
        scale += 0.15
    return scale

def income_adjusted_for_age(age, income, previously_employed=False):
    """
    Either take a portion from the full income or adjust previous income to raise 
    because of age.
    """
    if not previously_employed:
        return round((age / Occupation.adult_age) * income, 3)
    return round(income + (2 / Occupation.adult_age), 3)


class Occupation():
    def __init__(self, person, income_class, personality, lawful=None, honest=None, 
                 hereditary=False) -> None:
        self.person = person
        self.personality = personality
        self.has_job = False
        self.income_class = income_class
        self.income = 0
        self.all_incomes = []
        self.hereditary = hereditary # not implemented
        self.job = {
            'lawful' : lawful, # fluctuation of income
            'honest' : honest # fluctuation of job security
        }

    def find_job(self, age):
        # determine the kind of job
        if rand() < self.personality['lawful-chaotic'] :
            lawful = True
        else: lawful = False
        if rand() < self.personality['honest-false']:
            honest = True
        else: honest = False

        self.job = {
            'lawful' : lawful,
            'honest' : honest
        }

        # determine income
        scale = job_volatility(lawful, honest)
        if self.has_job and self.income != 0:
            self.income = normal_in_range(self.income, scale, 1.5, 0.5)
        else:
            self.income = normal_in_range(1, scale, 1.5, 0.5)
            if age < Occupation.adult_age:
                self.income = income_adjusted_for_age(age, self.income)
        self.has_job = True
        self.all_incomes.append(self.income)
        return self.income
    
    def evolve(self, age):
        if self.has_job:
            scale = job_volatility(**self.job)
            if age < Occupation.adult_age:
                self.income += income_adjusted_for_age(age, self.income, True)
            self.income = normal_in_range(self.income, scale, 1.5, 0)
            self.all_incomes.append(self.income)
        return {
            'has job' : self.has_job,
            'income' : self.income, 
        }
        
    def resume(self):
        resume =  {
            'has job' : self.has_job,
            'income class' : self.income_class, 
            'income' : self.income,
            'all_incomes' : self.all_incomes,
        }
        if self.has_job:
            resume['job'] = self.job
        return resume