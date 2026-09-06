from datasource.model.storage import DataGameField, DataGame
from domain.model.model import GameField, Game

class DataConversion():

    def domain_to_storage(self, game):
        storage_field = DataGameField()
        storage_field.matrix = [row.copy() for row in game.field.matrix]

        return DataGame(game.uuid, storage_field)
    

    def storage_to_domain(self, data_game):
        game = Game()

        game.uuid = data_game.uuid

        domain_field = GameField()
        domain_field.matrix = [row.copy() for row in data_game.field.matrix]


        game.field = domain_field
        return game