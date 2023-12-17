
class HomoSociologicus():
    def __init__(self, person) -> None:
        self.person = person

    def homo_sociologicus(self):
        return {
            
        }

"""
Homo sociologicus classes
"""
class WomanMA(HomoSociologicus):
    def __init__(self, person) -> None:
        super().__init__(person)

class ManMA(HomoSociologicus):
    def __init__(self, person) -> None:
        super().__init__(person)

class Neutral(HomoSociologicus):
    def __init__(self, person) -> None:
        super().__init__(person)
