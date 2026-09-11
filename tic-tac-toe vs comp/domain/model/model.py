import uuid

class GameField:
    def __init__(self):
        self.matrix = [[0,0,0],
                       [0,0,0],
                       [0,0,0]] 
        
class Game:
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.field = GameField()