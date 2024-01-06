from ..utils import *

class Factions():
    def __init__(self, community) -> None:
        self.factions = {}
        self.faction_names = community['faction_names']
        self.faction_distr = community['faction_distribution']

        # init the factions
        for i, f in enumerate(community['faction_names']):
            mobility = community['faction_mobility'][i]
            relative_mobility = {}
            relative_tot = 0

            # given that someone decides to switch factions, what do they chose?
            for j in range(community['factions']):
                if j != i:
                    relative_tot += mobility[j]
                    relative_mobility[self.faction_names[j]] = mobility[j]
            for k in relative_mobility.keys():
                relative_mobility[k] = relative_mobility[k] / relative_tot
            
            self.factions[f] = {
                'name' : f,
                'mobility' : mobility,
                'relative mobility' : relative_mobility
            }


    def assign_faction(self):
        f = rand_choice(self.faction_names, self.faction_distr)
        return f

    def change_faction(self, old_f):
        new_f = rand_choice(self.factions[old_f]['relative mobility'].keys(), 
                        self.factions[old_f]['relative mobility'].values())
        return new_f
    
    def get_mobility(self, faction):
        return self.factions[faction]['mobility']
