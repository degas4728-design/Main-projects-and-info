from flask import Blueprint, request, jsonify
from web.model.auth_model import SignUpRequest
from di.container import Container

auth_bp = Blueprint("auth", __name__)
container = Container()

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if not data or "login" not in data or "password" not in data:
        return jsonify({"error": "login и password обязательны"}), 400
    success = container.get_auth_service().register(data["login"], data["password"])
    if not success:
        return jsonify({"error": "Пользователь уже существует"}), 409
    return jsonify({"status": "зарегистрирован"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    auth_header = request.headers.get("Authorization", "")
    user_id = container.get_auth_service().authenticate(auth_header)
    if not user_id:
        return jsonify({"error": "Неверные логин или пароль"}), 401
    return jsonify({"uuid": user_id}), 200