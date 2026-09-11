import uuid

class DataGameField:
    def __init__(self):
        self.matrix = [[0,0,0],
                       [0,0,0],
                       [0,0,0]] 
        
class DataGame:
    def __init__(self, uuid, field):
        self.uuid = uuid
        self.field = field