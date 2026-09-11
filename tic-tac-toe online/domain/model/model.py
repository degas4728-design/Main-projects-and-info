import uuid
from enum import Enum

class GameField:
    def __init__(self):
        self.matrix = [[0,0,0],
                       [0,0,0],
                       [0,0,0]] 
        
class Game:
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.field = GameField()
        self.status = GameStatus.WAITING
        self.game_type = None
        self.current_turn = None
        self.players = []      
        self.symbols = {}       


class GameStatus(Enum):
    WAITING = "WAITING"
    PLAYER_TURN = "PLAYER_TURN"
    DRAW = "DRAW"
    PLAYER_WIN = "PLAYER_WIN"

class GameType(Enum):
    VS_COMPUTER = "VS_COMPUTER"
    VS_PLAYER = "VS_PLAYER"