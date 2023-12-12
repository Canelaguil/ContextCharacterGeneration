from numpy import random

class Body():
    def __init__(self, father_gens, mother_gens, first_gen = False) -> None:
        self.father_gens = father_gens
        self.mother_gens =  mother_gens
        self.first_gen = first_gen

        # body variables
        self.skin_color = self.set_skin()
        self.hair_type, self.hair_color = self.set_hair()
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

            skin_range = round(Body.no_skins * 0.25)
            high = max(m, f) + skin_range
            high_cap = high if high < Body.no_skins else Body.no_skins - 1
            low = min(m, f) - skin_range
            low_cap = low if low > -1 else 0
            average = (m + f) / 2
            
            skin = random.triangular(low_cap, average, high_cap, 1)
            return round(skin[0])




            # distr = [0 for _ in Body.skins]
            # distr[m] = 0.25
            # if m-1 > 0:
            #     distr[m-1] += 0.1
            #     if distr[m-2] > 0:
            #         distr[m-2] += 0.025
            #     else: 
            #         distr[m-1] += 0.025
            # else:
            #     distr[m] += 0.125
            

            # if m+1
            # distr[f] = 0.25
            
            


    def set_hair(self):
        return None, None
        pass

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

