import copy
import sys
from mesa import Model

class StreetSection:
    def __init__(self, key : int, no_houses : int, income_class : int, 
                    street : str, model : Model, generate : bool = False):
        if no_houses < 1:
            print('something went very wrong')
        self.total_lots = no_houses
        self.empty_lots = copy.deepcopy(self.total_lots)
        self.key = key

        self.income_class = income_class
        self.street = street
        self.model = model
        self.houses = {}
        if generate:
            self.init_houses()

    def init_houses(self):
        # not ready
        section = []
        # for i in range(self.total_lots):
        #     section.append(Home(self.income_class, self.street, self, i, self.city))
        return section
    
    """
    UPDATE SECTION
    """
    def add_house(self, house : {}):
        """
        Adds a house to the section. Input is a dict with information.
        """
        if len(self.houses) > self.total_lots:
            print("Something went wrong when adding th ehouse to the section")
        if house['income class'] != self.income_class:
            print("Incorrect income class")
            print(house['income class'], self.income_class)
            return False
        self.houses[house['key']] = house

    def get_empty_house(self):
        for h in self.houses.values():
            if h.is_empty():
                return h.key
        return False
    
    def add_person_to_house(self, house_key : str, person_key : str):
        """
        Assumes that person is allowed to be there.
        """
        if house_key in self.houses:
            self.houses[house_key].add_person(person_key)
        else:
            return False

    """
    INFO FUNCTIONS
    """
    def summary(self) -> dict:
        return {
            'key' : self.key,
            'houses' : list(self.houses.values())
        }

    def has_space(self) -> bool:
        if self.empty_lots > 1:
            return True 
        return False

    def get_people(self) -> list:
        people = []
        for house in self.houses:
            people.extend(house.get_householdmembers())
        return people
        