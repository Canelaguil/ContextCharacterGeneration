
class Network():
    def __init__(self, person) -> None:
        self.person = person

    def links(self):
        return {
            'test' : {
                'friend1' : 20, 
                'friend2' : 10, 
                'friend3': 5
            }
        }
    