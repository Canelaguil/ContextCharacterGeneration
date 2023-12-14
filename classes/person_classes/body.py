import numpy as np
from numpy import random
from random import choices as weighted_choice

class Body():
    def __init__(self, father_gens, mother_gens, first_gen = False) -> None:
        self.father_gens = father_gens
        self.mother_gens =  mother_gens
        self.first_gen = first_gen

        # body variables
        self.skin_color = self.set_skin()
        self.hair_type = self.set_hair_type()
        self.hair_color, self.hair_color_code = self.set_hair_color()
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

            average = (m + f) / 2
            skin_range = abs(f-average) / 2
            skin = round(random.normal(average, skin_range))
            if skin < 0:
                skin = 0
            elif skin >= Body.no_skins:
                skin = Body.no_skins - 1
            return skin                     

    def set_hair_type(self):
        """
        Hair type based on parents, random if first_gen
        """
        if self.first_gen:
            return [random.choice(Body.hair_type_seed),
                    random.choice(Body.hair_type_seed)]
        else:
            mother_hair = self.mother_gens['hair_type']
            father_hair = self.father_gens['hair_type']
            return [random.choice(mother_hair), 
                    random.choice(father_hair)]
        
    def set_hair_color(self):
        """
        Weighted hair_color based on skin color or parents' gens
        """
        if self.first_gen: 
            weights = np.array([abs(a-b) / Body.no_skins * self.skin_color for a, 
                                b in zip(Body.dark_hair_distr, Body.light_hair_distr)])
            print(list(range(Body.no_hairs)))
            hair = weighted_choice(list(range(Body.no_hairs)), weights=weights)
            hair = round(hair[0])
            return Body.hair_colors[hair], hair
        else:
            m = self.mother_gens['hair_color_code']
            f = self.father_gens['hair_color_code']

            average = (m + f) / 2
            hair_range = abs(f-average) / 2

            # modify average with skin modifier (average / Body.no_hairs)
            modified =  average - ((self.skin_color / Body.no_skins) * Body.no_hairs) / 2
            hair = round(random.normal(modified, hair_range))
            if hair < 0:
                hair = 0
            elif hair >= Body.no_hairs:
                hair = Body.no_hairs - 1
            return Body.hair_colors[hair], hair

    def set_eyes(self):
        return None
        pass

    def set_health(self):
        return None

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
            'hair_color_code' : self.hair_color_code,
            'hair_type' : self.hair_type,
            'health' : self.health,
        }

