
class GameService():

    def comp_motion(self, field):
        raise NotImplementedError

    def is_end(self, field): 
       raise NotImplementedError

    def valid_field(self, game, original_game):
        raise NotImplementedError