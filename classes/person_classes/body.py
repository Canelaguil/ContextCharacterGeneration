import numpy as np
from ..utils import *

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
    return rand_choice(['blue', 'green', 'brown'], p=p)

class Body():
    def __init__(self, person, father_gens, mother_gens, first_gen = False) -> None:
        self.person = person
        self.father_gens = father_gens
        self.mother_gens =  mother_gens
        self.first_gen = first_gen

        # body vars
        self.skin_color = self._set_skin()
        self.hair_type = self._set_hair_type()
        self.hair_color, self.hair_color_code = self._set_hair_color()
        self.eye_color = self._set_eyes()

        # health vars
        self.health = self._set_health()
        self.fertility = self._set_fertility()
        self.disabled = False
        self.disabilities = []
        self.communication_impaired = False
        self.mobility_impaired = False
        self.cognitive_impaired = False
        self.trigger('birth')

    """
    INIT FUNCTIONS
    """
    def _set_skin(self):
        """
        Weighted choice of skin color OR random skin color if first_gen
        """
        if self.first_gen:
            return rand_choice(Body.skins, p=Body.skin_distr)
        else:
            m = self.mother_gens['skin_color']
            f = self.father_gens['skin_color']

            average = (m + f) / 2
            skin_range = abs(f-average) / 2
            skin = normal_in_range(average, skin_range, Body.no_skins, 0, 0)
            return int(skin)                     

    def _set_hair_type(self):
        """
        Hair type based on parents, random if first_gen
        """
        if self.first_gen:
            return [rand_choice(Body.hair_type_seed),
                    rand_choice(Body.hair_type_seed)]
        else:
            mother_hair = self.mother_gens['hair_type']
            father_hair = self.father_gens['hair_type']
            return [rand_choice(mother_hair), 
                    rand_choice(father_hair)]
        
    def _set_hair_color(self):
        """
        Weighted hair_color based on skin color or parents' gens
        """
        if self.first_gen: 
            weights = np.array([abs(a-b) / Body.no_skins * self.skin_color for a, 
                                b in zip(Body.dark_hair_distr, Body.light_hair_distr)])
            hair = rand_choice(list(range(Body.no_hairs)), weights=weights)
            hair = round(hair)
            return Body.hair_colors[hair], hair
        else:
            m = self.mother_gens['hair_color_code']
            f = self.father_gens['hair_color_code']

            average = (m + f) / 2
            hair_range = abs(f-average) / 2

            # modify average with skin modifier (average / Body.no_hairs)
            modified =  average - ((self.skin_color / Body.no_skins) * Body.no_hairs) / 2
            hair = normal_in_range(modified, hair_range, Body.no_hairs, 0, 0)
            return Body.hair_colors[hair], hair

    def _set_eyes(self):
        """
        Assigns eye color either based on the punnett model or with seed
        """
        if self.first_gen:
            if self.skin_color < 0.5 * Body.no_skins:
                p = Body.dark_eye_distr
            else: 
                p = Body.light_eye_distr

            return str(rand_choice(['blue', 'green', 'brown'], p=p))
        else:
            m = self.mother_gens['eye_color'] 
            f = self.father_gens['eye_color']
            return str(punnett_eye_model(m, f))

    def _set_health(self):
        """
        Gets health from normal distribution
        """
        if self.first_gen:
            h = normal_in_range(Body.average_health, 0.1)            
        else:
            m = self.mother_gens['health']
            f = self.father_gens['health']
            loc = (m + f) / 2
            scale = abs(f-loc) / 2 
            h = normal_in_range(loc, scale) 
        return h
    
    def _set_fertility(self):
        """
        Set fertility based on own health
        """
        f = normal_in_range(self.health, 0.05) 
        return f

    """
    BODILY FUNCTIONS
    """
    def yearly_step(self, age):
        report = {}
        report['health'] = self.health_event(age)
        report['death'] = self.mortality_event(age)
        return report

    def health_event(self, age):
        """
        Does something happen health wise this year?
        """
        if age < 12:
            chance = (fair_mod(Body.child_mortality, - (0.01 * age))) * (1 - self.health)
        elif age > Body.old_age:
            chance = (0.15 + (0.05 * age)) * (1 - self.health)
        else:
            chance = 0.02 * (1 - self.health)

        # compose report
        report = {'change' : False, 'value_change' : 0.}
        if rand() < chance:
            report['change'] = True
            loc_impact = 1 - self.health
            scale_impact = loc_impact / 4
            impact = -1 * normal_in_range(loc_impact, scale_impact)

            # chance of gaining disability
            if rand() < 0.1 * impact:
                self.add_disability() 
                report['new_disability'] = self.disabilities[-1]

            old_health = self.health
            self.health_change(impact)
            report['value_change'] = round(self.health - old_health, 3)

        report['new_health'] = self.health
        return report

    def mortality_event(self, age):
        """
        Does the person die this turn?
        """
        if self.health == 0:
            chance = 1
        elif age < 12:
            chance = (fair_mod(Body.child_mortality, - (0.05 * age))) * (1 - self.health)
        elif age > Body.old_age:
            chance = (0.05 + (0.01 * (age - Body.old_age))) * (1 - self.health)
        elif age > 0.5 * Body.old_age:
            years = age - Body.adult_age
            chance = 0.025 * (1 - self.health) + (0.001 * years)
        else:
            chance = 0.05 * (1 - self.health)
        
        if rand() < chance:
            return True
        return False

    """
    TRIGGERS
    """
    def trigger(self, trigger, modifier=0., age=None):
        """
        Returns False if further action is required
        """
        if trigger == 'accident': 
            if rand() < 0.1:
                self.add_disability()
        elif trigger == 'childbirth':
            ch = 0.1 * (1 - self.health)
            if rand() < ch:
                self.person.die()

    def health_change(self, modifier):
        """
        Using the fair math principle, modifies health
        """
        self.health = fair_mod(self.health, modifier, 1, 3)

    def add_disability(self, key='blind', random_d=True):
        """
        Adjusts body to assigned or random disability
        """
        if random_d:
            disability = rand_choice(Body.all_disabilities, 
                                          p=Body.disability_distr)
        else:
            disability = key # to avoid confusion
            
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
            'skin_color' : int(self.skin_color),
            'eye_color' : self.eye_color, 
            'hair_color' : self.hair_color,
            'hair_color_code' : self.hair_color_code,
            'hair_type' : self.hair_type,
            'health' : self.health,
            'fertility' : self.fertility,
            'communication_impaired' : self.communication_impaired,
            'mobility_impaired' : self.mobility_impaired,
            'cognitive_impaired' : self.cognitive_impaired,
            'disabilities' : self.disabilities, 
        }

