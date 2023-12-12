from numpy import random

class Body():
    def __init__(self, father_gens, mother_gens, first_gen = False) -> None:
        self.father_gens = father_gens
        self.mother_gens =  mother_gens
        self.first_gen = first_gen

        # body variables
        self.skin_color = self.set_skin()
        self.hair_type = self.set_hair_type()
        self.hair_color = self.set_hair_color()
        self.eye_color = self.set_eyes()
        self.health = self.set_health()


    """
    INIT FUNCTIONS
    """
    def set_skin(self):
        """
        Weighted choice of skin color OR random skin color if first_gen
        """
        if self.first_gen: 
            return random.choice(Body.skins, p=Body.skin_distr)
        else:
            m = self.mother_gens['skin_color']
            f = self.father_gens['skin_color']

            skin_range = round(Body.no_skins * 0.1)
            average = (m + f) / 2
            skin = random.normal(average, skin_range)
            if skin < 0:
                skin = 0
            elif skin >= Body.no_skins:
                skin = Body.no_skins - 1
            return round(skin)                     


    def set_hair_type(self):
        if self.first_gen:
            return [random.choice(Body.hair_type_seed),
                    random.choice(Body.hair_type_seed)]
        else:
            mother_hair = self.mother_gens['hair_type']
            father_hair = self.father_gens['hair_type']
            return [random.choice(mother_hair), 
                    random.choice(father_hair)]
        
    def set_hair_color(self):
        return None

    def set_eyes(self):
        return None
        pass

    def set_health(self):
        return None
        pass

    """
    CHECK BODY
    """
    def yearly_step(self, age):
        pass

    """
    INFO FUNCTIONS
    """
    def pass_gens(self):
        return {
            'skin_color' : self.skin_color,
            'eye_color' : self.eye_color, 
            'hair_color' : self.hair_color,
            'hair_type' : self.hair_type,
            'health' : self.health,
        }

