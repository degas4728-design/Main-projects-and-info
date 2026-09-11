import uuid

class GameFieldWeb:
    def __init__(self):
        self.matrix = [[0,0,0],
                       [0,0,0],
                       [0,0,0]] 
        
class GameWeb:
    def __init__(self, uuid, field):
        self.uuid = uuid
        self.field = field