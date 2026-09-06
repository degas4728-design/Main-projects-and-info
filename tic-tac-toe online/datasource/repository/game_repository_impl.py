from datasource.database import SessionLocal
from datasource.model.storage import DataGame
from datasource.repository.repository import Gamerepository

class GameRepositoryImpl(Gamerepository):
    def save(self, game):
        db = SessionLocal()
        existing = db.query(DataGame).filter(DataGame.id == game.id).first()
        if existing:
            existing.field_matrix = game.field_matrix
            existing.status = game.status
            existing.game_type = game.game_type
            existing.current_turn = game.current_turn
            existing.players = game.players
            existing.symbols = game.symbols
        else:
            db.add(game)
        db.commit()
        db.close()

    def find_by_id(self, game_id):
        db = SessionLocal()
        result = db.query(DataGame).filter(DataGame.id == game_id).first()
        db.close()
        return result
    
    def find_all(self):
        db = SessionLocal()
        result = db.query(DataGame).all()
        db.close()
        return result