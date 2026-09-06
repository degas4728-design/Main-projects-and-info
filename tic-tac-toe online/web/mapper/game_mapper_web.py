from web.model.game_web import GameFieldWeb, GameWeb
from domain.model.model import GameField, Game
from uuid import UUID

class DataConversion():

    def domain_to_web(self, game):
        web_field = GameFieldWeb()
        web_field.matrix = [row.copy() for row in game.field.matrix]

        return GameWeb(game.uuid, web_field)
    

    def web_to_domain(self, web_game):
        game = Game()

        game.uuid = UUID(web_game.uuid)

        domain_field = GameField()
        domain_field.matrix = [row.copy() for row in web_game.field.matrix]


        game.field = domain_field
        return game