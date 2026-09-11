class Gamerepository():

    def save(self, game):
        raise NotImplementedError

    def find_by_id(self, game_id):
        raise NotImplementedError