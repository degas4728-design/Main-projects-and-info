from flask import Flask, request, jsonify
from web.model.game_web import GameWeb, GameFieldWeb
from web.mapper.game_mapper_web import DataConversion
from datasource.mapper.game_mapper import DataConversion as DataMapper
from domain.model.model import Game
from di.container import Container

app = Flask(__name__)


container = Container()
repo = container.get_repository()
service = container.get_service()
@app.route('/game/<uuid>', methods=['POST'])
def make_move(uuid):
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Нет JSON"}), 400
   
    game_web = GameWeb(uuid, GameFieldWeb())
    game_web.field.matrix = data['field']
   
    mapper_web = DataConversion()
    game_domain = mapper_web.web_to_domain(game_web)
    
    original_storage = repo.find_by_id(uuid)
    if original_storage is None:
        return jsonify({"error": "Игра не найдена"}), 404
 
    mapper_data = DataMapper()
    original_domain = mapper_data.storage_to_domain(original_storage)

    if service.valid_field(game_domain, original_domain.field.matrix) == False:
        return jsonify({"error": "Неверный ход"}), 400
    
    service.comp_motion(game_domain.field.matrix)

    game_storage = mapper_data.domain_to_storage(game_domain)
    print("SAVING:", game_storage.field.matrix)
    repo.save(game_storage)

    game_web_response = mapper_web.domain_to_web(game_domain)

    return jsonify({
        "uuid": str(game_web_response.uuid),
        "field": game_web_response.field.matrix,
        "status": service.is_end(game_domain.field.matrix)
    })

@app.route('/game/new', methods=['POST'])
def new_game():

    game = Game()
    mapper = DataMapper()
    game_storage = mapper.domain_to_storage(game)
    repo.save(game_storage)
    
    mapper_web = DataConversion()
    game_web = mapper_web.domain_to_web(game)
    
    return jsonify({
        "uuid": str(game_web.uuid),
        "field": game_web.field.matrix
    })
    
if __name__ == '__main__':
    app.run(debug=True)