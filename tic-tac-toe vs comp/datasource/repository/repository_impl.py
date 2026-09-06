from datasource.repository.repository import Gamerepository
from threading import Lock

class Gamerepositoryimpl(Gamerepository):
    
    def __init__(self):
        self._storage = {}
        self._lock = Lock()


    def save(self, game):
        with self._lock:
            self._storage[game.uuid] = game

    def find_by_id(self, game_id):
        with self._lock:
            for game in self._storage.values():
                if str(game.uuid) == game_id:
                    return game
        
            return None