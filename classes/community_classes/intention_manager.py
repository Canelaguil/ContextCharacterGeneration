from ..utils import * 
from mesa import Agent, Model

class Candidates():
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
    
    def find_match(self, seeker, for_marriage=True):
        # TODO : check for incest
        # TODO : move in together
        # TODO : check for motivation
        options = rand_choice(self.candidate_list, size=10)
        best_option = {}
        best_personality_distance = 1
        best_class_distance = 2
        # best_age_match = 
        for op in options:
            if for_marriage:
                # discard if class difference too big
                class_distance = abs(op['income class'][0] - seeker['income class'][0])
                if class_distance > 1:
                    break
                # only marry between classes if personality good match
                elif class_distance == 1: 
                    personality_distance = get_vector_distance(op['personality'], 
                                   seeker['personality'])
                    if personality_distance > 0.2:
                        break

            # check age compatibility
            if age_match(op['age'], seeker['age']) < 1:
                break
            
            # check personality distance
            personality_distance = get_vector_distance(op['personality'], 
                                   seeker['personality'])
            if personality_distance < best_personality_distance:
                best_option = op
                best_personality_distance = personality_distance
        
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
        self.male_marriage_intentions = Candidates(self)
        self.female_marriage_intentions = Candidates(self)
        self.friend_intentions = Candidates(self)

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
        marriage_intention = self.male_marriage_intentions.get()
        while marriage_intention != None:
            partner = self.female_marriage_intentions.find_match(marriage_intention)
            if partner:
                self.model.marry(marriage_intention['source'], partner['source'])
            marriage_intention = self.male_marriage_intentions.get()


    def houses(self):
        pass

    def post_processing(self):
        pass

    """
    INFO FUNCTIONS
    """



