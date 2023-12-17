import random
from ..utils import *

class Naming():
    def __init__(self, sex, father, mother, surnames, first_gen=False) -> None:
        """
        Generates a name for the person 
        """
        # reads naming system
        if Naming.system == 'medieval':
            self.generator = self.MedievalNameGenerator(sex, father, mother)
        elif Naming.system == 'male-centric': 
            self.generator = self.MaleCentricNameGenerator(sex, father, mother)
        elif Naming.system == 'female-centric': 
            self.generator = self.MaleCentricNameGenerator(sex, father, mother)
        elif Naming.system == 'equal':
            self.generator = self.EqualNameGenerator(sex, father, mother)

        if sex == 'f': 
            self.name = self.generator.get_female_first_name()
        else:
            self.name = self.generator.get_male_first_name()

        self.surname = self.generator.get_surname(surnames, first_gen)

    def full(self):
        """
        Returns string of full name
        """
        return f"{self.name} {self.surname}".strip()

    def first_name(self):
            return str(self.name)
        
    def last_name(self):
        return str(self.surname)

    class MedievalNameGenerator(): 
        def __init__(self, sex, father, mother) -> None:       
            """
            Naming based on late middle-ages Netherlands. 
            Vars are double stored here and in parent for ease of use.
            """
            self.sex = sex
            self.mother = mother
            self.father = father

        def get_female_first_name(self):
            """
            If they have them, the child has a chance of being named after their 
            parent
            """
            if self.mother: 
                if rand() < 0.2:
                    self.name = self.mother
            self.name = rand_choice(Naming.female_names)
            return self.name

        def get_male_first_name(self):
            """
            If they have them, the child has a chance of being named after their 
            parent
            """
            if self.father: 
                if rand() < 0.2:
                    self.name = self.father
            self.name = rand_choice(Naming.male_names)
            return self.name

        def get_surname(self, surnames, first_gen): 
            """
            If parents, child has a chance of being named after them. If a 
            surname was specified, there is a chance of that being given. Else 
            no surname or a random one is returned.

            NOTE: if child is not acknowledged by one of the parents BUT child 
            is not first gen, surname entry [fathersur, mothersur] contains a 
            False at that point. If acknowledged but no name, the string is 
            simply empty
            """
            if first_gen:
                random_name = 0.7 if first_gen else 0.1
                ch = rand()
                if ch < random_name:
                    return rand_choice(Naming.surnames)
                elif ch < 0.8:
                    return surnames
                return ""
            
            # if father's surname is given
            if surnames[0]:
                pass
            ch = rand()
            if ch < 0.3:
                if self.sex == 'f':
                    return f"{self.father}sdochter"
                if self.sex == 'm':
                    return f"{self.father}szoon"
            elif ch < 0.5:
                if rand() < 0.7:
                    return f"van {self.father}"
                else:
                    return f"van {self.mother}"
            return ""
            
    class MaleCentricNameGenerator():
        def __init__(self, sex, father, mother) -> None:
            pass

        def get_female_first_name(self):
            pass

        def get_male_first_name(self):
            pass

        def get_surname(self, surnames, first_gen): 
            pass

    class FemaleCentricNameGenerator():
        def __init__(self, sex, father, mother) -> None:
            pass

        def get_female_first_name(self):
            pass

        def get_male_first_name(self):
            pass

        def get_surname(self, surnames, first_gen): 
            pass


    class EqualNameGenerator():
        def __init__(self, sex, father, mother) -> None:
            pass

        def get_female_first_name(self):
            pass

        def get_male_first_name(self):
            pass

        def get_surname(self, surnames, first_gen): 
            pass
