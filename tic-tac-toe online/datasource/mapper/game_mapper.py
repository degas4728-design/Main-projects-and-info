from datasource.model.storage import DataGame
from domain.model.model import Game, GameField, GameStatus, GameType
import uuid

class DataConversion:

    def domain_to_storage(self, game: Game) -> DataGame:
        return DataGame(
            id=game.uuid,
            field_matrix=game.field.matrix,
            status=game.status.value,
            game_type=game.game_type.value if game.game_type else None,
            current_turn=str(game.current_turn) if game.current_turn else None,
            players=[str(p) for p in game.players],
            symbols={str(k): v for k, v in game.symbols.items()}
        )

    def storage_to_domain(self, data_game: DataGame) -> Game:
        game = Game()
        game.uuid = data_game.id

        domain_field = GameField()
        domain_field.matrix = data_game.field_matrix
        game.field = domain_field

        game.status = GameStatus(data_game.status) if data_game.status else GameStatus.WAITING
        game.game_type = GameType(data_game.game_type) if data_game.game_type else None
        game.current_turn = uuid.UUID(data_game.current_turn) if data_game.current_turn else None
        game.players = [uuid.UUID(p) for p in data_game.players] if data_game.players else []
        game.symbols = {uuid.UUID(k): v for k, v in data_game.symbols.items()} if data_game.symbols else {}
        return game