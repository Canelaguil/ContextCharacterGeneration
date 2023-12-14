import numpy as np
from numpy import random
from random import choices as weighted_choice

def punnett_eye_model(eye1, eye2):
    # source: https://www.verywellhealth.com/genetics-of-eye-color-3421603
    p = {
        'blue' : {
            'blue' : [0.99, 0.009, 0.001], 
            'green' : [0.49, 0.5, 0.01], 
            'brown' : [0.49, 0.01, 0.5],
        }, 
        'green' : {
            'blue' : [0.49, 0.5, 0.01],
            'green' : [0.25, 0.74, 0.01], 
            'brown' : [0.12, 0.38, 0.5], 
        },
        'brown' : {
            'blue' : [0.49, 0.01, 0.5],
            'green' : [0.12, 0.38, 0.5], 
            'brown' : [0.18, 0.07, 0.75], 
        }
    }[eye1][eye2]
    return random.choice(['blue', 'green', 'brown'], p=p)

class Body():
    def __init__(self, father_gens, mother_gens, first_gen = False) -> None:
        self.father_gens = father_gens
        self.mother_gens =  mother_gens
        self.first_gen = first_gen

        # body vars
        self.skin_color = self.set_skin()
        self.hair_type = self.set_hair_type()
        self.hair_color, self.hair_color_code = self.set_hair_color()
        self.eye_color = self.set_eyes()

        # health vars
        self.health = self.set_health()
        self.disabled = False
        self.disabilities = []
        self.communication_impaired = False
        self.mobility_impaired = False
        self.cognitive_impaired = False
        self.trigger('birth')

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
        """
        Assigns eye color either based on the punnett model or with seed
        """
        if self.first_gen:
            if self.skin_color < 0.5 * Body.no_skins:
                p = Body.dark_eye_distr
            else: 
                p = Body.light_eye_distr

            return random.choice(['blue', 'green', 'brown'], p=p)
        else:
            m = self.mother_gens['eye_color'] 
            f = self.father_gens['eye_color']
            return punnett_eye_model(m, f)

    def set_health(self):
        """
        Gets health from normal distribution
        """
        if self.first_gen:
            h = random.normal(Body.average_health, 0.1)            
        else:
            m = self.mother_gens['health']
            f = self.father_gens['health']
            loc = (m + f) / 2
            scale = abs(f-loc) / 2 
            h = random.normal(loc, scale) 
        if h > 1:
                h = 1.0
        elif h < 0:
            h = 0.
        return round(h, 3)

    """
    CHECK BODY
    """
    def yearly_step(self, age):
        pass

    def trigger(self, trigger, modifier=0.):
        if trigger == 'birth': 
            if random.random() < 0.05:
                self.add_disability()


    """
    EVENTS
    """
    def health_change(self, modifier):
        """
        Using the fair math principle, modifies health
        """
        if modifier > 0:
            self.health = self.health + ((1 - self.health) * modifier)
        if modifier < 0: 
            self.health = self.health + (self.health * modifier)

        # the round is not very precise (bc of floats) but that's okay
        self.health = round(self.health, 3)

    def add_disability(self, key='blind', random_d=True):
        """
        Adjusts body to assigned or random disability
        """
        if random_d:
            disability = random.choice(Body.all_disabilities, 
                                          p=Body.disability_distr)
        else:
            disability = key
            
        i = Body.all_disabilities.index(disability)

        # without check if already there: 2x blind is just extra blind
        self.disabilities.append(disability)
        com_impact, mob_impact, cog_impact, health_mod = Body.disability_impact[i]
        self.health_change(health_mod)

        # only change booleans if false
        if not self.mobility_impaired:
            self.mobility_impaired = mob_impact
        if not self.communication_impaired:
            self.communication_impaired = com_impact
        if not self.cognitive_impaired:
            self.cognitive_impaired = cog_impact



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
            'communication_impaired' : self.communication_impaired,
            'mobility impaired' : self.mobility_impaired,
            'cognitive impaired' : self.cognitive_impaired,
            'disabilities' : self.disabilities, 
        }

