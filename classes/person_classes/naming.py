import random

class Naming():
    def __init__(self, sex, father, mother, surnames, mode='medieval', first_gen=False) -> None:
        if mode == 'medieval':
            self.generator = self.MedievalNameGenerator(sex, father, mother)
        elif mode == 'male-centric': 
            self.generator = self.MaleCentricNameGenerator(sex)
        elif mode == 'female-centric': 
            self.generator = self.MaleCentricNameGenerator(sex)
        elif mode == 'equal':
            self.generator = self.EqualNameGenerator(sex)

        if sex == 'f': 
            self.name = self.generator.get_female_first_name()
        else:
            self.name = self.generator.get_male_first_name()

        self.surname = self.generator.get_surname(surnames, first_gen)

    def full(self):
        """
        Returns string of full name
        """
        return f"{self.name} {self.surname}"


    class MedievalNameGenerator(): 
        def __init__(self, sex, father, mother) -> None:       
            """
            Naming based on late middle-ages Netherlands. 
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
                if random.random() < 0.2:
                    self.name = self.mother
            self.name = random.choice(Naming.female_names)
            return self.name

        def get_male_first_name(self):
            """
            If they have them, the child has a chance of being named after their 
            parent
            """
            if self.father: 
                if random.random() < 0.2:
                    self.name = self.father
            self.name = random.choice(Naming.male_names)
            return self.name

        def get_surname(self, surnames, first_gen): 
            """
            If parents, child has a chance of being named after them. If a 
            surname was specified, there is a chance of that being given. Else 
            no surname or a random one is returned.
            """
            if not first_gen and self.father not in ("", None, self.name) and self.mother not in ("", None, self.name):
                ch = random.random()
                if ch < 0.3:
                    if self.sex == 'f':
                        return f"{self.father}sdochter"
                    if self.sex == 'm':
                        return f"{self.father}szoon"
                elif ch < 0.5:
                    if random.random() < 0.7:
                        return f"van {self.father}"
                    else:
                        return f"van {self.mother}"
            random_name = 0.7 if first_gen else 0.1
            ch = random.random()
            if ch < random_name:
                return random.choice(Naming.surnames)
            elif ch < 0.8:
                return surnames
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