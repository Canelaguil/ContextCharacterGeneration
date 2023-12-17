
class Occupation():
    def __init__(self, person, income_class, lawful=None, honest=None, hereditary=False) -> None:
        self.person = person
        self.lawful = lawful # fluctuation of income
        self.honest = honest # fluctuation of job security
        self.income_class = income_class # income class security
        self.hereditary = hereditary
        
    def resume(self):
        return {
            'lawful' : self.lawful, 
            'honest' : self.honest,
            'income class' : self.income_class, 
            'hereditary' : self.hereditary,
        }