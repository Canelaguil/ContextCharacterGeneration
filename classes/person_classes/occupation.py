
class Occupation():
    def __init__(self, income_class, lawful, honest, hereditary=False) -> None:
        self.lawful = lawful # fluctuation of income
        self.honest = honest # fluctuation of job security
        self.income_class = income_class # income class security
        self.hereditary = hereditary
        pass