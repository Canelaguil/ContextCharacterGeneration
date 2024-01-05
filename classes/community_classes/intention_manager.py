from ..utils import * 
from mesa import Agent, Model

class MarriageCandidates():
    def __init__(self, owner) -> None:
        self.owner = owner
        self.candidate_list = []

    def add(self, candidate_advert: dict):
        self.candidate_list.append(candidate_advert)

    def get(self) -> dict:
        if not self.empty():
            msg = self.candidate_list.pop(0)
            return msg
        return None    
    
    def find_match(self, seeker):
        # TODO : check for motivation
        sample_size = 400
        no_candidates = len(self.candidate_list)
        if no_candidates < sample_size:
            size = no_candidates
        else: size = sample_size

        options = rand_choice(self.candidate_list, size=size)
        best_option = {}
        best_personality_distance = 1
        best_age = 80
        # best_age_match = 
        for op in options:
            this_option = False

            # check if these two already know each other (siblings, eg)
            if self.owner.model.we_know_each_other(op['source'], seeker['source']):
                break

            # discard for marriage if class difference too big
            class_distance = abs(op['income class'][0] - seeker['income class'][0])
            if class_distance > 1:
                break

            # only marry between classes if personality good match
            elif class_distance == 1: 
                personality_distance = get_vector_distance(op['personality'], 
                                seeker['personality'])
                if personality_distance > 0.2:
                    break

            # give priority to younger women
            if op['age'] < best_age:                
                this_option = True

            # check age compatibility
            if age_match(op['age'], seeker['age']) < 0.8:
                break
            
            # check personality distance
            personality_distance = get_vector_distance(op['personality'], 
                                   seeker['personality'])
            if personality_distance < best_personality_distance:
                this_option = True

            if this_option:   
                best_option = op
                best_personality_distance = personality_distance
                best_age = op['age']
        
        # check if a match was found
        if best_option == {}:
            return False
        self.candidate_list.remove(best_option)
        return best_option

    def end_year(self):
        self.candidate_list = []

    def empty(self) -> bool:
        if self.candidate_list == []:
            return True
        return False
    

class Intention_Manager(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)
        self.male_marriage_intentions = MarriageCandidates(self)
        self.female_marriage_intentions = MarriageCandidates(self)
        self.friend_intentions = MarriageCandidates(self)

        # stat collection
        self.male_births = []
        self.female_births = []
        self.marriages = []
        self.bachelors = []
        self.bachelorettes = []
        self.living_people = []
        self.births = []
        self.deaths = []

    """
    Intention management
    """
    def receive_intention(self, intention):
        if intention['topic'] == 'marriage':
            if intention['sex'] == 'f':
                self.female_marriage_intentions.add(intention)
            else:
                self.male_marriage_intentions.add(intention)

    """
    PHASES
    """
    def people(self):
        pass

    def relationships(self):
        self.bachelors.append(len(self.male_marriage_intentions.candidate_list))
        self.bachelorettes.append(len(self.female_marriage_intentions.candidate_list))
        # print(f'number of bachelors : {len(self.male_marriage_intentions.candidate_list)}')
        # print(f'number of bachelorettes : {len(self.female_marriage_intentions.candidate_list)}')
        marriage_intention = self.male_marriage_intentions.get()
        while marriage_intention != None:
            partner = self.female_marriage_intentions.find_match(marriage_intention)
            if partner:
                # print(beautify_print(partner))
                # print(beautify_print(marriage_intention))
                # import sys
                # sys.exit()
                self.model.marry(marriage_intention['source'], partner['source'])
            marriage_intention = self.male_marriage_intentions.get()
        self.male_marriage_intentions.end_year()
        self.female_marriage_intentions.end_year()


    def houses(self):
        pass

    def post_processing(self):
        pass

    """
    INFO FUNCTIONS
    """
    def receive_stats(self, new_males, new_females, new_deaths, new_marriages,
                      living_people):
        all = new_males + new_females
        self.male_births.append(new_males)
        self.births.append(all)
        self.deaths.append(new_deaths)
        self.female_births.append(new_females)
        self.marriages.append(new_marriages)
        self.living_people.append(living_people)

    def demographics(self):
        return {
            'male births' : self.male_births, 
            'female births' : self.female_births, 
            'births' : self.births,
            'deaths' : self.deaths,
            'marriages' : self.marriages, 
            'bachelors' : self.bachelors, 
            'bachelorettes' : self.bachelorettes,
            'living people' : self.living_people
        }



