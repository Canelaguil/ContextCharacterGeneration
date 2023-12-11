import copy
import sys
from ..home import Home

class Section:
        def __init__(self, key : int, no_houses : int, income_class : int, 
                     street : str, generate : bool = False):
            self.total_lots = no_houses
            self.empty_lots = copy.deepcopy(self.total_lots)
            self.relative_key = key

            self.income_class = income_class
            self.street = street
            # self.city = city
            self.houses = {}
            if generate:
                self.init_houses()

        def init_houses(self):
            section = []
            for i in range(self.total_lots):
                section.append(Home(self.income_class, self.street, self, i, self.city))
            return section
        
        """
        UPDATE SECTION
        """

        def add_house(self, house : Home):
            """
            Adds a house to the section
            """
            if self.empty_lots < 1:
                return False
            if house.income_class[0] != self.income_class:
                print("Incorrect income class")
                print(house.income_class, self.income_class)
                return False
            self.houses[house.key] = house
            self.empty_lots -= 1

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
        def get_section_summary(self) -> dict:
            summary = {}
            for house in self.houses:
                summary[house.key] = house.household_summary()
            return summary

        def has_space(self) -> bool:
            if self.empty_lots > 1:
                return True 
            return False

        def get_people(self) -> list:
            people = []
            for house in self.houses:
                people.extend(house.get_householdmembers())
            return people
        