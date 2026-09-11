from flask import Flask, request, jsonify
from web.model.game_web import GameWeb, GameFieldWeb
from web.mapper.game_mapper_web import DataConversion
from datasource.mapper.game_mapper import DataConversion as DataMapper
from domain.model.model import Game, GameType, GameStatus
from di.container import Container
from web.route.auth_controller import auth_bp
from web.route.auth_middleware import require_auth
import uuid as uuid_module

app = Flask(__name__)
app.register_blueprint(auth_bp)

container = Container()
repo = container.get_repository()
service = container.get_service()

@app.route('/game/<game_uuid>', methods=['POST'])
@require_auth
def make_move(game_uuid, current_user_id=None):
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Нет JSON"}), 400

    game_web = GameWeb(game_uuid, GameFieldWeb())
    game_web.field.matrix = data['field']

    mapper_web = DataConversion()
    game_domain = mapper_web.web_to_domain(game_web)

    original_storage = repo.find_by_id(game_uuid)
    if original_storage is None:
        return jsonify({"error": "Игра не найдена"}), 404

    mapper_data = DataMapper()
    original_domain = mapper_data.storage_to_domain(original_storage)  

    if original_domain.status in (GameStatus.PLAYER_WIN, GameStatus.DRAW):
        return jsonify({"error": "Игра уже завершена"}), 400

    if original_domain.game_type == GameType.VS_PLAYER:
        if str(original_domain.current_turn) != current_user_id:
            return jsonify({"error": "Сейчас не ваш ход"}), 400

    if not service.valid_field(game_domain, original_domain.field.matrix):
        return jsonify({"error": "Неверный ход"}), 400

    if original_domain.game_type == GameType.VS_COMPUTER:
        service.comp_motion(game_domain.field.matrix)
    else:
        players = original_domain.players
        print("PLAYERS:", players)
        print("CURRENT:", uuid_module.UUID(current_user_id))
        idx = players.index(uuid_module.UUID(current_user_id))
        next_player = players[(idx + 1) % 2]
        game_domain.current_turn = next_player

    game_domain.players = original_domain.players
    game_domain.symbols = original_domain.symbols
    game_domain.game_type = original_domain.game_type
    end_status = service.is_end(game_domain.field.matrix, game_domain)
    game_storage = mapper_data.domain_to_storage(game_domain)
    repo.save(game_storage)

    game_web_response = mapper_web.domain_to_web(game_domain)
    return jsonify({
        "uuid": str(game_web_response.uuid),
        "field": game_web_response.field.matrix,
        "status": end_status,
        "current_turn": str(game_domain.current_turn) if game_domain.current_turn else None
    })

@app.route('/game/new', methods=['POST'])
@require_auth
def new_game(current_user_id=None):
    data = request.get_json()
    game_type = data.get("game_type", "VS_COMPUTER") if data else "VS_COMPUTER"

    game = Game()
    game.game_type = GameType(game_type)
    if game_type == "VS_COMPUTER":
        game.players = [uuid_module.UUID(current_user_id)]
        game.symbols = {uuid_module.UUID(current_user_id): 1}
        game.current_turn = uuid_module.UUID(current_user_id)
        game.status = GameStatus.PLAYER_TURN
    else:
        game.players = [uuid_module.UUID(current_user_id)]
        game.symbols = {uuid_module.UUID(current_user_id): 1}
        game.status = GameStatus.WAITING

    mapper = DataMapper()
    game_storage = mapper.domain_to_storage(game)
    repo.save(game_storage)
    
    mapper_web = DataConversion()
    game_web = mapper_web.domain_to_web(game)
    
    return jsonify({
        "uuid": str(game_web.uuid),
        "field": game_web.field.matrix,
        "game_type": game_type,
        "status": game.status.value
    })

@app.route('/games', methods=['GET'])
@require_auth
def get_games(current_user_id=None):
    all_games = repo.find_all()
    available = [g for g in all_games if g.status == "WAITING"]
    return jsonify([{
        "uuid": str(g.id),
        "status": g.status,
        "players": g.players
    } for g in available])

@app.route('/game/<game_uuid>/join', methods=['POST'])
@require_auth
def join_game(game_uuid, current_user_id=None):
    storage = repo.find_by_id(game_uuid)
    if not storage:
        return jsonify({"error": "Игра не найдена"}), 404
    game = DataMapper().storage_to_domain(storage)
    if len(game.players) >= 2:
        return jsonify({"error": "Игра заполнена"}), 400
    user_id = uuid_module.UUID(current_user_id)
    game.players.append(user_id)
    game.symbols[user_id] = 2
    game.current_turn = game.players[0]
    game.status = GameStatus.PLAYER_TURN
    print(game.players)
    repo.save(DataMapper().domain_to_storage(game))
    return jsonify({"status": "joined", "uuid": str(game.uuid)})

@app.route('/game/<game_uuid>', methods=['GET'])
@require_auth
def get_game(game_uuid, current_user_id=None):
    storage = repo.find_by_id(game_uuid)
    if not storage:
        return jsonify({"error": "Игра не найдена"}), 404
    game = DataMapper().storage_to_domain(storage)
    game_web = DataConversion().domain_to_web(game)
    return jsonify({
        "uuid": str(game_web.uuid),
        "field": game_web.field.matrix,
        "status": game.status.value,
        "game_type": game.game_type.value if game.game_type else None,
        "current_turn": str(game.current_turn) if game.current_turn else None
    })

@app.route('/user/<user_uuid>', methods=['GET'])
@require_auth
def get_user(user_uuid, current_user_id=None):
    user_repo = container.get_auth_service()._user_repo
    user = user_repo.find_by_id(user_uuid)
    if not user:
        return jsonify({"error": "Пользователь не найден"}), 404
    return jsonify({
        "uuid": str(user.id),
        "login": user.login
    })
    
if __name__ == '__main__':
    app.run(debug=True)