from ..utils import * 
from mesa import Agent, Model

class Matchmaker():
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
    
    def end_year(self):
        self.candidate_list = []

    def empty(self) -> bool:
        if self.candidate_list == []:
            return True
        return False

class FriendshipCandidates(Matchmaker): 
    def __init__(self, owner) -> None:
        super().__init__(owner)

    def find_match(self, seeker):
        sample_size = 50
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
            this_is_option = False
            this_is_it = False

            # check geographical distance
            if op['adress']['street'] == seeker['adress']['street']:
                this_is_option = True
            if op['adress']['section'] == seeker['adress']['section']:
                this_is_it = True

            # queers find queers
            op_is_queer = op['situation']['expression']['sexuality expression'] > 0.25 or op['situation']['expression']['gender expression expression'] > 0.25
            seeker_is_queer = seeker['situation']['expression']['sexuality expression'] > 0.25 or seeker['situation']['expression']['gender expression expression'] > 0.25
            if op_is_queer and seeker_is_queer:
                this_is_it = True

            # check if these two already know each other (siblings, eg)
            if self.owner.model.we_know_each_other(op['source'], seeker['source']):
                break

            # discard for friendship if class difference too big
            class_distance = abs(op['income class'][0] - seeker['income class'][0])
            if class_distance > 3:
                break

            # only marry between classes if personality good match
            elif class_distance < 3: 
                personality_distance = get_vector_distance(op['personality'], 
                                seeker['personality'])
                if personality_distance > 0.2:
                    break

            # check age compatibility
            age_matching = age_match(op['age'], seeker['age'])
            if age_matching < 0.8:
                break
            elif age_matching > best_age:
                this_is_option = True
            
            # check personality distance
            personality_distance = get_vector_distance(op['personality'], 
                                   seeker['personality'])
            if personality_distance < best_personality_distance:
                this_is_option = True

            if this_is_it:
                best_option = op
                break
            if this_is_option:   
                best_option = op
                best_personality_distance = personality_distance
                best_age = op['age']
        
        # check if a match was found
        if best_option == {}:
            return False
        self.candidate_list.remove(best_option)
        return best_option    

class MarriageCandidates(Matchmaker):
    def __init__(self, owner) -> None:
        super().__init__(owner)
    
    def find_match(self, seeker):
        # TODO : check for motivation
        sample_size = 500
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

            # Only in-faction marriages allowed through matchmaking
            if op['faction'] != seeker['faction']:
                break

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

class Intention_Manager(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)
        self.male_marriage_intentions = MarriageCandidates(self)
        self.female_marriage_intentions = MarriageCandidates(self)
        self.friend_intentions = FriendshipCandidates(self)

        # stat collection
        self.male_births = []
        self.female_births = []
        self.marriages = []
        self.bachelors = []
        self.bachelorettes = []
        self.lonely_people = []
        self.new_friendships = []
        self.living_people = []
        self.births = []
        self.deaths = []

    """
    Intention management
    """
    def receive_intention(self, intention_msg):
        intention = intention_msg['topic']
        if intention == 'marriage':
            if intention_msg['sex'] == 'f':
                self.female_marriage_intentions.add(intention_msg)
            else:
                self.male_marriage_intentions.add(intention_msg)
        elif intention == 'friendship':
            self.friend_intentions.add(intention_msg)

    """
    PHASES
    """
    def people(self):
        pass

    def lovedeathbirth(self):
        # record stats
        self.bachelors.append(len(self.male_marriage_intentions.candidate_list))
        self.bachelorettes.append(len(self.female_marriage_intentions.candidate_list))
        self.lonely_people.append(len(self.friend_intentions.candidate_list))
        friend_pairs = 0

        # match marriage seekers
        marriage_intention = self.male_marriage_intentions.get()
        while marriage_intention != None:
            partner = self.female_marriage_intentions.find_match(marriage_intention)
            if partner:
                self.model.marry(marriage_intention['source'], partner['source'])
            marriage_intention = self.male_marriage_intentions.get()

        # match friendship seekers
        friend_intention = self.friend_intentions.get()
        while friend_intention != None:
            friend = self.friend_intentions.find_match(friend_intention)
            if friend:
                r_id = self.model.create_relationship(friend_intention['source'], 
                                               friend['source'], 'friend')
                # print(r_id)
                if r_id != False: 
                    friend_pairs += 1
            friend_intention = self.friend_intentions.get()
        self.new_friendships.append(friend_pairs)

        # end this season of the bachelor
        self.male_marriage_intentions.end_year()
        self.female_marriage_intentions.end_year()
        self.friend_intentions.end_year()


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

